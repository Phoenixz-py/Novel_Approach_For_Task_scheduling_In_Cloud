import random
import numpy as np

# Define the cloud task scheduling problem
# Customize these values according to your problem
num_tasks = 5
num_vms = 10

tasks_execution_time = np.random.rand(num_tasks)
vms_processing_speed = np.random.rand(num_vms)

# Define the objective function to be optimized (e.g., makespan)
def objective_function(schedule):
    makespan = 0
    vm_loads = np.zeros(num_vms)

    for task_id, vm_id in enumerate(schedule):
        # Use modulo to ensure valid VM indices
        vm_id %= num_vms

        execution_time = tasks_execution_time[task_id] / \
            vms_processing_speed[vm_id]
        vm_loads[vm_id] += execution_time
        if execution_time > makespan:
            makespan = execution_time

    return makespan


def initialize_population(num_wolves, num_vms):
    return [np.array([random.randint(0, num_vms - 1) % num_vms for _ in range(num_tasks)]) for _ in range(num_wolves)]


def get_alpha_beta_delta_wolves(population, objective_function):
    sorted_population = sorted(population, key=lambda x: objective_function(x))
    return sorted_population[0], sorted_population[1], sorted_population[2]


def update_wolves(population, alpha, beta, delta, a=2):
    updated_population = []

    for wolf in population:
        updated_wolf = wolf.copy()

        for i in range(num_tasks):
            A1 = 2 * a * random.random() - a  # Use random module here
            C1 = 2 * random.random()
            D_alpha = abs(C1 * alpha[i] - wolf[i])
            X1 = alpha[i] - A1 * D_alpha

            A2 = 2 * a * random.random() - a  # Use random module here
            C2 = 2 * random.random()
            D_beta = abs(C2 * beta[i] - wolf[i])
            X2 = beta[i] - A2 * D_beta

            A3 = 2 * a * random.random() - a  # Use random module here
            C3 = 2 * random.random()
            D_delta = abs(C3 * delta[i] - wolf[i])
            X3 = delta[i] - A3 * D_delta

            # Ensure the assignment stays within valid VM indices
            updated_wolf[i] = (X1 + X2 + X3) % num_vms  # Use modulo operation

        updated_population.append(updated_wolf)

    return updated_population


def grey_wolf_optimization(num_iterations):
    population = initialize_population(num_wolves=20, num_vms=num_vms)

    for iteration in range(num_iterations):
        # Create a list to store task-to-VM mappings for each wolf
        population_mapping = []

        for wolf in population:
            alpha, beta, delta = get_alpha_beta_delta_wolves(
                population, objective_function)
            wolf = update_wolves([wolf], alpha, beta, delta)[0]

            # After convergence, alpha represents the best solution found
            best_schedule = alpha

            # Create a mapping dictionary for the current wolf's schedule
            task_to_vm_mapping = {}
            for task_id, vm_id in enumerate(best_schedule):
                # Use modulo to ensure valid VM indices
                vm_id %= num_vms

                if vm_id in task_to_vm_mapping:
                    task_to_vm_mapping[vm_id].append(task_id)
                else:
                    task_to_vm_mapping[vm_id] = [task_id]

            population_mapping.append(task_to_vm_mapping)

        # Print the task-to-VM mappings for each wolf in this iteration
        print(f"Iteration {iteration + 1} Population Mapping:")
        for i, mapping in enumerate(population_mapping):
            print(f"  Wolf {i}: {mapping}")

        alpha, beta, delta = get_alpha_beta_delta_wolves(
            population, objective_function)
        population = update_wolves(population, alpha, beta, delta)

    # After the final iteration, alpha represents the best solution found
    best_schedule = alpha
    best_objective_value = objective_function(best_schedule)

    return best_schedule, best_objective_value


# usage
best_schedule, best_objective_value = grey_wolf_optimization(
    num_iterations=100)

# Function to print detailed task-to-VM assignment
def print_task_assignment(schedule):
    for task_id, vm_id in enumerate(schedule):
        print(f"Task {task_id} is assigned to VM {vm_id}.")


print("\nFinal Best Schedule:", best_schedule)
print("Best Objective Value:", best_objective_value)
print_task_assignment(best_schedule)
