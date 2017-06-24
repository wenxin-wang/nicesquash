import csv
import sys
import os
from subprocess import check_output, check_call, PIPE

tag_idx = 3
influx_url = os.environ['INFLUX_URL']
influx_auth = os.environ['INFLUX_AUTH']
queries = ('name,pci.device_id,pci.sub_device_id,fan.speed,'
           'utilization.gpu,utilization.memory,temperature.gpu,power.draw,'
           'clocks.current.graphics,clocks.current.sm,clocks.current.memory,'
           'memory.used')
fields = queries.split(',')


def query():
    lines = check_output(
        ['nvidia-smi', '--query-gpu=' + queries, '--format=csv'],
        universal_newlines=True)
    lines = lines.replace(', ', ',').split('\n')[1:]
    reader = csv.reader(lines)
    return reader


def join_kv(keys, values):
    return ','.join(['%s=%s' % (k, v) for k, v in zip(keys, values)])


def to_influx(reader, host):
    lines = []
    for data in reader:
        if not data:
            continue
        data[0] = data[0].replace(' ', '_')
        for i in range(tag_idx, len(data)):
            data[i] = data[i].split(' ', 1)[0]
        line = 'smi,host=%s,' % host + join_kv(
            fields[:tag_idx], data[:tag_idx]) + ' ' + join_kv(
                fields[tag_idx:], data[tag_idx:])
        lines.append(line)
    return lines


def curl(lines):
    check_call(
        [
            'curl', '-i', '-XPOST', influx_url, '-u', influx_auth,
            '--data-binary', '\n'.join(lines)
        ],
        stdout=PIPE,
        stderr=PIPE)


if __name__ == '__main__':
    lines = to_influx(query(), sys.argv[1])
    curl(lines)
