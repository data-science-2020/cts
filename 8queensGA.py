import random


def initial_population(size):  # making random sequences
    return [random.randint(1, nq) for _ in range(nq)]


def score(sequence):
    horizontal_collisions = sum([sequence.count(queen) - 1 for queen in sequence]) / 2
    diagonal_collisions = 0

    n = len(sequence)
    left_diagonal = [0] * 2 * n
    right_diagonal = [0] * 2 * n
    for i in range(n):
        left_diagonal[i + sequence[i] - 1] += 1
        right_diagonal[len(sequence) - i + sequence[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter / (n - abs(i - n + 1))

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))  # 28-(2+3)=23


def probability(sequence, score):
    return score(sequence) / maxFitness


def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def cross_over(x, y):  # doing cross_over between two sequences
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]


def mutate(x):  # randomly changing the value of a random index of a sequence
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x


def genetic_queen(population, score):
    mutation_probability = 0.03
    new_population = []
    probabilities = [probability(n, score) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities)  # best sequence 1
        y = random_pick(population, probabilities)  # best sequence 2
        child = cross_over(x, y)  # creating two new sequences from the best 2 sequences
        if random.random() < mutation_probability:
            child = mutate(child)
        print_sequence(child)
        new_population.append(child)
        if score(child) == maxFitness: break
    return new_population


def print_sequence(seq):
    print("Sequence = {},  Score = {}"
          .format(str(seq), score(seq)))


if __name__ == "__main__":
    nq = 8
    maxFitness = (nq * (nq - 1)) / 2
    population = [initial_population(nq) for _ in range(100)]

    generation = 1

    while not maxFitness in [score(seq) for seq in population]:
        print("=== Generation {} ===".format(generation))
        population = genetic_queen(population, score)
        print("")
        print("Maximum Score = {}".format(max([score(n) for n in population])))
        generation += 1
    seq_out = []
    print("Solved in Generation {}!".format(generation - 1))
    for seq in population:
        if score(seq) == maxFitness:            
            print("One of the solutions: ")
            seq_out = seq
            print_sequence(seq)


