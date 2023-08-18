import random


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


class Group:
    chromosomes = []
    vms = []
    tasks = []
    n_chromosomes = 0

    def __init__(self, vmlist=None, tasklist=None, n_chromosomes=3):
        self.n_chromosomes = n_chromosomes
        self.vms = vmlist
        self.tasks = tasklist
    # def __str__(self):


def calc_makespan(chromosomes):
    busy_time = {}
    for task in chromosomes:
        if task not in busy_time:
            busy_time[chromosomes[task]] = task.length / chromosomes[task].mips
        else:
            busy_time[chromosomes[task]] += task.length / chromosomes[task].mips
    return max(busy_time.values())


tasks = []
n_tasks = 5  # input1
n_vms = 3  # input2
vms = []
j = 0
for i in range(n_tasks):
    tasks.append(Task(i, random.randrange(100, 500)))

for i in range(n_vms):
    vms.append(VM(i, random.randrange(1000, 5000)))

print("""
 Tasks 
 """)
for i in tasks:
    print(f"Generated Task {i.id} with Length {i.length}")

print("""
 Virtual Machines 
 """)

for i in vms:
    print(f"Created VM {i.id} with MIPS =  {i.mips}")

print("""
""")
# here we are taking number of groups as 1
# entry point


n_groups = 1
group_list = [Group(3)]  # main input
tg = n_tasks // n_groups

for g in group_list:
    if n_groups == 1:
        g.vms = vms
        g.tasks = tasks
    else:
        pass
    for i in range(g.n_chromosomes):
        chromosome = {}
        for tasks in g.tasks:
            # chromosome[tasks] = g.vms[random.randrange(0, n_vms)]
            chromosome[tasks] = random.choice(g.vms)
        print(f"{chromosome}")
        g.chromosomes.append(chromosome)
    epoch = 0
    while epoch != 1:
        fitness_values = []
        for i in range(g.n_chromosomes):
            fitness_values.append(calc_makespan(g.chromosomes[i]))
        # print(fitness_values)
        tot_makespan = 0
        for i in g.chromosomes:
            tot_makespan += calc_makespan(i)  # some doubt regarding addition present here

        s_prob = []
        c_prob = []
        cp = 0
        p = 0
        for i in range(g.n_chromosomes):
            p = calc_makespan(g.chromosomes[i]) / tot_makespan
            cp += p
            s_prob.append(p)
            c_prob.append(cp)

        rw_values = []

        print("""
        Roulette Wheel Selection
        """)

        for i in range(g.n_chromosomes):
            rw = random.uniform(0, 1)
            rw_values.append(rw)
            j = 0
            while j < g.n_chromosomes and rw > c_prob[j]:
                j += 1
            g.chromosomes[i] = g.chromosomes[j]
            print(f"New Chromosome[{i + 1}] = Chromosome[{j + 1}]")

        print("""
        """)

        # for i in range(g.n_chromosomes):
        #     print(f"{c_prob[i]:.3f}   {rw_values[i]:.3f}")

        # two -point crossover has been done
        print("""
        CrossOver Process """)
        for i in range(0, g.n_chromosomes - 1, 2):
            cr_point = random.randrange(0, len(g.tasks) - 2)
            print(" CrossOver Point = ", cr_point)
            print(f""" Before CrossOver 
            in Chromosome[{i}]
            {g.chromosomes[i]}
            C1 = {g.tasks[cr_point]} : {g.chromosomes[i][g.tasks[cr_point]]} 
            C2 = {g.tasks[cr_point + 1]} : {g.chromosomes[i][g.tasks[cr_point + 1]]}
            in Chromosome[{i + 1}]
            {g.chromosomes[i + 1]}
            C1 = {g.tasks[cr_point]}: {g.chromosomes[i + 1][g.tasks[cr_point]]}
            C2 = {g.tasks[cr_point + 1]} : {g.chromosomes[i + 1][g.tasks[cr_point + 1]]}""")
            g.chromosomes[i][g.tasks[cr_point]], g.chromosomes[i + 1][g.tasks[cr_point]] = g.chromosomes[i + 1][
                g.tasks[cr_point]], g.chromosomes[i][g.tasks[cr_point]]
            g.chromosomes[i][g.tasks[cr_point + 1]], g.chromosomes[i + 1][g.tasks[cr_point + 1]] = g.chromosomes[i + 1][
                g.tasks[cr_point + 1]], g.chromosomes[i][g.tasks[cr_point + 1]]
            print(f""" After CrossOver 
            in Chromosome[{i}]
            {g.chromosomes[i]}
            C1 = {g.tasks[cr_point]} : {g.chromosomes[i][g.tasks[cr_point]]}
            C2 = {g.tasks[cr_point + 1]} : {g.chromosomes[i][g.tasks[cr_point + 1]]} 
            in Chromosome[{i + 1}]
            {g.chromosomes[i + 1]}
            C1 = {g.tasks[cr_point]} : {g.chromosomes[i + 1][g.tasks[cr_point]]}
            C2 = {g.tasks[cr_point + 1]} : {g.chromosomes[i + 1][g.tasks[cr_point + 1]]}""")
        print()
        print("Chromosomes After CrossOver :")
        for i in range(g.n_chromosomes):
            print(f"Chromosome[{i}] = {g.chromosomes[i]}")

        epoch += 1

print("""
""")
