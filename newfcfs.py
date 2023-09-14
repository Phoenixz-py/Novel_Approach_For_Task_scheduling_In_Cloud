import random


class Task:
    def __init__(self, task_id, execution_time):
        self.task_id = task_id
        self.execution_time = execution_time


class VM:
    def __init__(self, vm_id, mips):
        self.vm_id = vm_id
        self.mips = mips


def execute_task(vm, task):
    execution_time = task.execution_time / vm.mips
    print(f"Executing Task {task.task_id} on VM {vm.vm_id} for {execution_time:.2f} seconds.")
    return execution_time


def generate_random_tasks_and_vms(num_tasks, num_vms):
    tasks = [Task(task_id, random.randint(1000, 10000)) for task_id in range(num_tasks)]
    vms = [VM(vm_id, random.uniform(100, 1000)) for vm_id in range(num_vms)]
    print("Generated Tasks:")
    for task in tasks:
        print(f"Task {task.task_id}: Execution Time = {task.execution_time}")

    # Print the generated VMs
    print("\nGenerated VMs:")
    for vm in vms:
        print(f"VM {vm.vm_id}: MIPS = {vm.mips}")
    return tasks, vms


def calculate_makespan(vms, tasks):
    total_time = 0
    vm_times = [0] * len(vms)

    for task in tasks:
        available_vms = [(vm, vm_times[vm.vm_id] / vm.mips) for vm in vms]
        available_vms.sort(key=lambda x: x[1])
        vm, task_time = available_vms[0]

        execution_time = execute_task(vm, task)

        vm_times[vm.vm_id] += execution_time
        total_time = max(total_time, vm_times[vm.vm_id])

    return total_time


if __name__ == "__main__":
    num_tasks = 5
    num_vms = 3

    tasks, vms = generate_random_tasks_and_vms(num_tasks, num_vms)

    makespan = calculate_makespan(vms, tasks)
    print(f"Total Makespan: {makespan:.2f} seconds")
