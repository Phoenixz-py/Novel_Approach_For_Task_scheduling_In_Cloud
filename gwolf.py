import random
import matplotlib.pyplot as plt


def objective_function(schedule):
    vm_loads = [0 for _ in range(num_vms)]

    for task_id, vm_id in enumerate(schedule):
        start_time = max(vm_loads[vm_id], 0)
        execution_time = start_time + \
            tasks_length[task_id] / vms_processing_speed[vm_id]
        vm_loads[vm_id] = execution_time
    makespan = max(vm_loads)

    return makespan


def initialize_population(num_wolves, num_vms, num_tasks):
    return [[random.randint(0, num_vms - 1) for _ in range(num_tasks)] for _ in range(num_wolves)]


def get_alpha_beta_delta_wolves(population, objective_function):
    sorted_population = sorted(population, key=lambda x: objective_function(x))
    return sorted_population[0], sorted_population[1], sorted_population[2]


def update_wolf(wolf, alpha, beta, delta, num_vms):
    updated_wolf = wolf.copy()
    if wolf == alpha:
        # Do not update alpha (best solution)
        pass
    elif wolf == beta:
        # Beta wolf moves towards alpha wolf
        for task_id in range(len(updated_wolf)):
            if random.random() < 0.5:
                # Randomly choose to update or not
                continue
            # Move the task closer to the corresponding VM of the alpha wolf
            alpha_vm = alpha[task_id]
            current_vm = updated_wolf[task_id]
            if alpha_vm < current_vm:
                updated_wolf[task_id] -= 1
            elif alpha_vm > current_vm:
                updated_wolf[task_id] += 1
            # Ensure the VM assignment is within bounds
            updated_wolf[task_id] = max(
                0, min(updated_wolf[task_id], num_vms - 1))
    elif wolf == delta:
        # Delta wolf moves towards the midpoint between alpha and beta wolves
        for task_id in range(len(updated_wolf)):
            if random.random() < 0.5:
                # Randomly choose to update or not
                continue
            # Calculate the midpoint VM between alpha and beta
            alpha_vm = alpha[task_id]
            beta_vm = beta[task_id]
            midpoint_vm = (alpha_vm + beta_vm) // 2
            current_vm = updated_wolf[task_id]
            if midpoint_vm < current_vm:
                updated_wolf[task_id] -= 1
            elif midpoint_vm > current_vm:
                updated_wolf[task_id] += 1
            # Ensure the VM assignment is within bounds
            updated_wolf[task_id] = max(
                0, min(updated_wolf[task_id], num_vms - 1))
    else:
        # Omega wolves move towards alpha wolf with some randomness
        for task_id in range(len(updated_wolf)):
            if random.random() < 0.5:
                # Randomly choose to update or not
                continue
            # Move the task closer to the corresponding VM of the alpha wolf with randomness
            alpha_vm = alpha[task_id]
            current_vm = updated_wolf[task_id]
            # Introduce some randomness in the movement
            movement = random.randint(-1, 1)
            updated_wolf[task_id] = max(
                0, min(current_vm + movement, num_vms - 1))
    return updated_wolf


def grey_wolf_optimization(num_iterations):
    population = initialize_population(
        num_wolves=num_wolves, num_vms=num_vms, num_tasks=num_tasks)
    alpha, beta, delta = get_alpha_beta_delta_wolves(
        population, objective_function)
    best_schedule = None
    best_objective_value = None
    convergence_curve = []  # List to store objective values

    for iteration in range(num_iterations):
        population_mapping = []

        for i in range(len(population)):
            population[i] = update_wolf(
                population[i], alpha, beta, delta, num_vms)

        alpha, beta, delta = get_alpha_beta_delta_wolves(
            population, objective_function)
        best_schedule = alpha
        best_objective_value = objective_function(alpha)
        # Append objective value
        convergence_curve.append(best_objective_value)

        task_to_vm_mapping = {}
        for task_id, vm_id in enumerate(best_schedule):
            if vm_id in task_to_vm_mapping:
                task_to_vm_mapping[vm_id].append(task_id)
            else:
                task_to_vm_mapping[vm_id] = [task_id]

        population_mapping.append(task_to_vm_mapping)

        print(f"Iteration {iteration + 1} Population Mapping:")
        for i, mapping in enumerate(population_mapping):
            print(f"  Wolf {i}: {mapping}")
        print(f"Objective Function Value is {objective_function(alpha)}")

    return best_schedule, best_objective_value, convergence_curve


def print_task_assignment(schedule):
    for task_id, vm_id in enumerate(schedule):
        print(f"Task {task_id} is assigned to VM {vm_id}.")

# Plotting function
def plot_convergence(convergence_curve):
    plt.plot(convergence_curve)
    plt.xlabel('Iteration')
    plt.ylabel('Objective Function Value')
    plt.title('Convergence Curve')
    plt.grid(True)
    plt.show()


num_tasks = 2000
num_vms = 200
num_wolves = 50

tasks_length = [random.randint(5000, 8000) for i in range(num_tasks)]
vms_processing_speed = [random.randint(3000, 6000) for j in range(num_vms)]

best_schedule, best_objective_value, convergence_curve = grey_wolf_optimization(
    num_iterations=200)

print("\nFinal Best Schedule:", best_schedule)
print("Best Objective Value:", best_objective_value)
print_task_assignment(best_schedule)

# Call the plot_convergence function to plot the convergence curve
plot_convergence(convergence_curve)
