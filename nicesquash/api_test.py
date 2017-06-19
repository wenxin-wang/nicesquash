from api import NiceHashAPI

nicehash = NiceHashAPI('149QWefQoWKR1zJXLCNRWooXFTG3XV3VSa', min_wait=1)


if __name__ == '__main__':
    #nicehash.print_stats()
    #print(nicehash.get_workers())
    print(nicehash.get_prices())
