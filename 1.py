import random


def fitness(board):
    fit = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if board[i] == board[j]:
                continue
            if abs(board[j] - board[i]) == j - i:
                continue
            fit += 1
    return fit


def init_population(size):
    first_population = []
    for i in range(size):
        first_population.append([random.randint(1, 8) for _ in range(8)])
    return first_population


def cross(gen1, gen2):
    rnd_pos = random.randint(1, 7)

    new_gen1 = gen1[:rnd_pos]
    for i in range(8 - rnd_pos):
        new_gen1.append(gen2[rnd_pos + i])
    new_gen2 = gen2[:rnd_pos]
    for i in range(8 - rnd_pos):
        new_gen2.append(gen1[rnd_pos + i])

    return new_gen1, new_gen2


def mutate(gen):
    rnd_pos = random.randint(0, 7)
    rnd_inc = random.randint(1, 7)
    gen[rnd_pos] += rnd_inc
    if gen[rnd_pos] > 8:
        gen[rnd_pos] -= 8


def reproduce(population, total_size, must_select):
    best_fits = []
    for i in range(must_select):
        best_fits.append([[], 0])

    for i in population:
        f = fitness(i)
        if f > best_fits[0][1]:
            best_fits[0][0] = i
            best_fits[0][1] = f
            best_fits = sorted(best_fits, key=lambda element: element[1])

    return_gens = []
    remain = total_size - must_select

    rnd_select = random.sample(range(0, len(population)), remain)
    for i in rnd_select:
        return_gens.append(population[i])
    for i in best_fits:
        return_gens.append(i[0])

    return return_gens


mutation_prob = 0.1
size = 50

# crossover_prob is 0.8
prob_list = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

population = init_population(size)
best_fit = 0  # the score of the solution. Best is 28.
best_sol = []   # The solution of the problem (position of each queen).
generation_num = 0

while best_fit < 28:
    generation_num += 1
    total_gens = population.copy()

    # pair off
    rnd_pair = random.sample(range(0, size), size)

    # cross over
    for i in range(0, size - 1, 2):
        if prob_list[random.randint(0, 9)]:
            new_gens = cross(population[rnd_pair[i]], population[rnd_pair[i + 1]])
            total_gens.append(new_gens[0])
            total_gens.append(new_gens[1])

    # mutation
    for i in total_gens:
        rnd1 = random.randint(1, int(1 / mutation_prob))
        if rnd1 == 1:
            mutate(i)

    # reproduce
    population = reproduce(total_gens, size, int(0.2 * len(total_gens)))

    # new best
    for i in population:
        if fitness(i) > best_fit:
            best_fit = fitness(i)
            best_sol = i

    print("Best solution:", best_sol, "\tScore:", best_fit)

print('---------------------------')
print('- Final solution:', best_sol, '\n- Number of generation:', generation_num)
