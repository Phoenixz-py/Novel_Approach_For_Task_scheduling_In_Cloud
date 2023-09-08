import random
import matplotlib.pyplot as plt
class Task:
    def __init__(self, task_id, length, at=0, deadline=0):
        self.id = task_id
        self.at = at
        self.length = length
        self.deadline = deadline

    def __str__(self):
        return "Task " + str(self.id)

    def __repr__(self):
        return "Task " + str(self.id)

class VM:
    def __init__(self, vm_id, mips, cost=1000, energy=1000):
        self.id = vm_id
        self.mips = mips
        self.energy = energy
        self.cost = cost

    def __str__(self):
        return "VM " + str(self.id)

    def __repr__(self):
        return "VM " + str(self.id)

def calculate_makespan(chromosome):
    vm_completion_times = {vm: 0 for vm in vms}
    total_delay = 0  # To calculate the total delay

    for task, assigned_vm in chromosome.items():
        task_length = task.length
        vm = assigned_vm
        start_time = max(vm_completion_times[vm], task.at)  # Start time considering VM's completion time or task's arrival time
        completion_time = start_time + task_length

        # Calculate delay (time past the deadline)
        delay = max(0, completion_time - task.deadline)
        total_delay += delay

        vm_completion_times[vm] = completion_time

    makespan = max(vm_completion_times.values())
    return makespan, total_delay

def initialize_population(pop_size):
    population = []
    for _ in range(pop_size):
        chromosome = {task: random.choice(vms) for task in tasks}
        population.append(chromosome)
    return population

def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    roulette_spin = random.uniform(0, total_fitness)
    current_sum = 0

    for i, fitness in enumerate(fitness_values):
        current_sum += fitness
        if current_sum >= roulette_spin:
            return population[i]

def two_point_crossover(parent1, parent2):
    keys = list(parent1.keys())
    random.shuffle(keys)
    crossover_point1 = random.randint(0, len(keys) - 1)
    crossover_point2 = random.randint(crossover_point1 + 1, len(keys))

    child1 = {}
    child2 = {}

    for key in keys:
        if crossover_point1 <= keys.index(key) < crossover_point2:
            child1[key] = parent2[key]
            child2[key] = parent1[key]
        else:
            child1[key] = parent1[key]
            child2[key] = parent2[key]

    return child1, child2

def swap_mutation(chromosome):
    mutated_chromosome = chromosome.copy()
    task_keys = list(mutated_chromosome.keys())  # Convert keys to a list
    task1, task2 = random.sample(task_keys, 2)
    mutated_chromosome[task1], mutated_chromosome[task2] = mutated_chromosome[task2], mutated_chromosome[task1]
    return mutated_chromosome

def evaluate_population(pop_size, num_generations):
    makespan_histories = []

    for size in pop_size:
        print(f"Evaluating Population Size {size}")
        best_solution, best_makespan, makespan_history , total_delay_history= genetic_algorithm(tasks, vms, size, num_generations)
        makespan_histories.append((size, makespan_history))

    return makespan_histories

def genetic_algorithm(tasks, vms, pop_size, num_generations):
    population = initialize_population(pop_size)
    best_solution = None
    best_makespan = float('inf')
    best_total_delay = float('inf')

    makespan_history = []  # To store makespan values over iterations
    total_delay_history = []  # To store total delay values over iterations

    for generation in range(num_generations):
        fitness_values = [1 / calculate_makespan(chromosome)[0] for chromosome in population]
        total_fitness = sum(fitness_values)

        if total_fitness == 0:
            break

        normalized_fitness = [fitness / total_fitness for fitness in fitness_values]

        new_population = []

        for _ in range(pop_size // 2):
            parent1 = roulette_wheel_selection(population, normalized_fitness)
            parent2 = roulette_wheel_selection(population, normalized_fitness)
            child1, child2 = two_point_crossover(parent1, parent2)

            if random.random() < mutation_rate:
                child1 = swap_mutation(child1)

            if random.random() < mutation_rate:
                child2 = swap_mutation(child2)

            new_population.extend([child1, child2])

        population = new_population

        current_best_index = min(range(len(population)), key=lambda x: calculate_makespan(population[x])[0])
        current_best_makespan, current_total_delay = calculate_makespan(population[current_best_index])

        if current_best_makespan < best_makespan:
            best_solution = population[current_best_index]
            best_makespan = current_best_makespan
            best_total_delay = current_total_delay

        makespan_history.append(best_makespan)  # Collect makespan values
        total_delay_history.append(best_total_delay)  # Collect total delay values

      #  print(f"Generation {generation + 1} - Best Makespan: {best_makespan} - Best Total Delay: {best_total_delay}")

    return best_solution, best_makespan, makespan_history, total_delay_history

if __name__ == "__main__":
    n_tasks = 1000
    n_vms = 300
    n_chromosomes = 10
    mutation_rate = 0.1

    tasks = [Task(i, i * 10000,deadline=(i+1) * 10000) for i in range(1, n_tasks + 1)]
    vms = [VM(i, i * 1000) for i in range(1, n_vms + 1)]

    # Define a list of different population sizes to evaluate
    population_sizes = [10, 20, 30, 40, 50]

    makespan_histories = []
    total_delay_histories = []

    for size in population_sizes:
        print(f"Evaluating Population Size {size}")
        best_solution, best_makespan, makespan_history, total_delay_history = genetic_algorithm(tasks, vms, size, 1000)
        makespan_histories.append((size, makespan_history))
        total_delay_histories.append((size, total_delay_history))

    # Plot the makespan improvement for different population sizes
    for size, makespan_history in makespan_histories:
        plt.plot(range(1, len(makespan_history) + 1), makespan_history, label=f"Pop Size {size}")

    plt.xlabel("Generation")
    plt.ylabel("Makespan")
    plt.title("Makespan Improvement Over Generations for Different Population Sizes")
    plt.legend()
    plt.show()

    # Plot the total delay improvement for different population sizes
    for size, total_delay_history in total_delay_histories:
        plt.plot(range(1, len(total_delay_history) + 1), total_delay_history, label=f"Pop Size {size}")

    plt.xlabel("Generation")
    plt.ylabel("Total Delay")
    plt.title("Total Delay Improvement Over Generations for Different Population Sizes")
    plt.legend()
    plt.show()