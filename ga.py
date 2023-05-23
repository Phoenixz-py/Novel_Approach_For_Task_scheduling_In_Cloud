import random


def function(arr):
    return arr[0] + 2 * arr[1] + 3 * arr[2] + 4 * arr[3]


chromosomes = [
    [12, 5, 23, 8],
    [2, 21, 18, 3],
    [10, 4, 13, 14],
    [20, 1, 10, 6],
    [1, 4, 13, 19],
    [20, 5, 17, 1]
]
value = 30
n_parameters = 4
n_chromosomes = 6


def initialize():
    for i in range(n_chromosomes):
        chromosome = []
        for j in range(n_parameters):
            chromosome.append(random.randrange(0, value))
        chromosomes.append(chromosome)


def evaluate():
    f = []
    for chromosome in chromosomes:
        f.append(function(chromosome) - 30)
    return f


def select(f):
    fi = []
    p = []
    c = []
    total = 0
    for obj in f:
        v = 1 / (1 + obj)
        fi.append(v)
        total += v
    cp = 0
    for j in range(len(fi)):
        prob = fi[j] / total
        cp += prob
        p.append(prob)
        c.append(cp)
    return fi, p, c


# initialize()
f_obj = evaluate()
fitness, probability, cumulative = select(f_obj)


for i in range(n_chromosomes):
    print("{}   {}  {}    {} {}".format(chromosomes[i], f_obj[i], fitness[i], probability[i], cumulative[i]))
