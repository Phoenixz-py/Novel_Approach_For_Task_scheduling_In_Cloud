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


def objective_function(schedule, tasks, vms):
    vm_loads = [0 for _ in range(len(vms))]

    for task_id, vm_id in enumerate(schedule):
        start_time = max(vm_loads[vm_id], tasks[task_id].at)
        execution_time = start_time + tasks[task_id].length / vms[vm_id].mips
        vm_loads[vm_id] = execution_time
    makespan = max(vm_loads)

    return makespan


def initialize_population(num_wolves, num_vms, num_tasks):
    population = []
    for _ in range(num_wolves):
        schedule = [random.randint(0, num_vms - 1) for _ in range(num_tasks)]
        population.append(schedule)
    return population


def get_alpha_beta_delta_wolves(population, tasks, vms):
    sorted_population = sorted(
        population, key=lambda x: objective_function(x, tasks, vms))
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


def grey_wolf_optimization(num_iterations, num_wolves, num_vms, num_tasks, tasks, vms):
    population = initialize_population(num_wolves, num_vms, num_tasks)
    alpha, beta, delta = get_alpha_beta_delta_wolves(population, tasks, vms)
    best_schedule = alpha
    best_objective_value = objective_function(alpha, tasks, vms)
    convergence_curve = []

    for iteration in range(num_iterations):
        for i in range(len(population)):
            population[i] = update_wolf(
                population[i], alpha, beta, delta, num_vms)

        alpha, beta, delta = get_alpha_beta_delta_wolves(
            population, tasks, vms)

        if objective_function(alpha, tasks, vms) < best_objective_value:
            best_schedule = alpha
            best_objective_value = objective_function(alpha, tasks, vms)

        convergence_curve.append(best_objective_value)

        print(
            f"Iteration {iteration + 1}: Best Objective Value is {best_objective_value}")

    return best_schedule, best_objective_value, convergence_curve


def print_task_assignment(schedule):
    for task_id, vm_id in enumerate(schedule):
        print(f"Task {task_id} is assigned to VM {vm_id}.")


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

tasks = [Task(i, random.randint(5000, 8000)) for i in range(num_tasks+1)]
vms = [VM(j, random.randint(3000, 6000)) for j in range(num_vms)]

best_schedule, best_objective_value, convergence_curve = grey_wolf_optimization(
    num_iterations=300, num_wolves=num_wolves, num_vms=num_vms, num_tasks=num_tasks, tasks=tasks, vms=vms)

print("\nFinal Best Schedule:")
print_task_assignment(best_schedule)
print("Best Objective Value:", best_objective_value)

# Call the plot_convergence function to plot the convergence curve
plot_convergence(convergence_curve)
