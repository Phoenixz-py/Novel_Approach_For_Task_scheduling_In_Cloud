import random


class Task:
    def __init__(self, task_id, length, at, deadline):
        self.id = task_id
        self.at = at
        self.length = length
        self.deadline = deadline

    def __str__(self):
        return "t" + str(self.id)

    def __repr__(self):
        return "t" + str(self.id)


class VM:
    def __init__(self, vm_id, mips, cost, energy):
        self.id = vm_id
        self.mips = mips
        self.energy = energy
        self.cost = cost

    def __str__(self):
        return "vm" + str(self.id)

    def __repr__(self):
        return "vm" + str(self.id)


class Group:
    chromosomes = []
    n_chromosomes = 3

    def __init__(self, vmlist, tasklist):
        self.vms = vmlist
        self.tasks = tasklist
    # def __str__(self):


tasks = []
n_tasks = 5
n_vms = 3
vms = []
j = 0
for i in range(1, n_tasks + 1):
    tasks.append(Task(i, i * 100, j, 100))
    j += 1

for i in range(1, n_vms + 1):
    vms.append(VM(i, i * 1000, 1000 + i * 100, 5000 * i))

# for i in tasks:
#     print(i)
#     print(i.at)
#     print(i.length)
#     print(i.deadline)

# for i in vms:
#     print()
#     print(i.mips)
#     print(i.energy)
#     print(i.cost)


# here we are taking number of groups as 1
n_groups = 1
g = Group(tasks, vms)


def calc_makespan(chromosome):
    busy_time = {}
    for task in chromosome:
        if task not in busy_time:
            busy_time[chromosome[task]] = task.length / chromosome[task].mips
        else:
            busy_time[chromosome[task]] += task.length / chromosome[task].mips
    return max(busy_time.values())


for i in range(g.n_chromosomes):
    chromosome = {}
    for vm in g.vms:
        chromosome[vm] = g.tasks[random.randrange(0, n_vms)]
    # print(chromosome.keys())
    g.chromosomes.append(chromosome)

for i in g.chromosomes:
    print(calc_makespan(i))
