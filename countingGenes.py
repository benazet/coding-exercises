
print("Calculate the probability for siblings to carry, within them, all their parent's alleles of a particular (heterozygous) gene")
print('siblings | total | positive |  %')

for n in range(1, 10):

    pools = [()]
    for i in range(0, n):
        newPools = []
        for pool in pools:
            newPools.append((('a', 'c'),) + pool)
            newPools.append((('a', 'd'),) + pool)
            newPools.append((('b', 'c'),) + pool)
            newPools.append((('b', 'd'),) + pool)
        pools = newPools

    count = len(pools)
    all = 0
    for pool in pools:
        mum = len(set(mum for mum, dad in pool))
        dad = len(set(dad for mum, dad in pool))
        if mum == 2 and dad == 2:
            all += 1

    print('{:^10}{:>6}{:>11}{:>8.1%}'.format(n,  count, all, all/count))
