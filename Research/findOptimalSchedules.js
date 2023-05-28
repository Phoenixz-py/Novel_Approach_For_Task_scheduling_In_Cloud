class Datacenter {
  constructor() {
    this.vms = [];
    this.cloudlets = [];
  }

  addVM(vm) {
    this.vms.push(vm);
  }

  addCloudlet(cloudlet) {
    this.cloudlets.push(cloudlet);
  }

  getMakespan() {
    let makespan = 0;
    for (let i = 0; i < this.cloudlets.length; i++) {
      makespan += this.cloudlets[i].length;
    }

    // Convert the Python code to JavaScript.
    const busy_time = {};
    for (const task of this.cloudlets) {
      if (!busy_time[task]) {
        busy_time[task] = task.length / this.cloudlets.mips;
      } else {
        busy_time[task] += task.length / this.cloudlets.mips;
      }
    }

    // Return the maximum busy time.
    return Math.max(...Object.values(busy_time));
  }
}

class VM {
  constructor(mips) {
    this.mips = mips;
  }

  addCloudlet(cloudlet) {
    this.cloudlets.push(cloudlet);
  }

  getMakespan() {
    let makespan = 0;
    for (let i = 0; i < this.cloudlets.length; i++) {
      makespan += this.cloudlets[i].length;
    }

    // Convert the Python code to JavaScript.
    const busy_time = {};
    for (const task of this.cloudlets) {
      if (!busy_time[task]) {
        busy_time[task] = task.length / this.cloudlets.mips;
      } else {
        busy_time[task] += task.length / this.cloudlets.mips;
      }
    }

    // Return the maximum busy time.
    return Math.max(...Object.values(busy_time));
  }
}

class OrderedPerformanceCurve {
  constructor(makespans) {
    this.makespans = makespans;
  }

  plot() {
    
  }

  getAverageMakespan() {
    
  }
}

function findOptimalSchedules(cloudlets, datacenters) {

  // Sort the cloudlets by deadline.
  cloudlets.sort((a, b) => a.deadline - b.deadline);

  // Initialize the makespans array.
  let makespans = [];
  for (let i = 0; i < datacenters.length; i++) {
    makespans.push(datacenters[i].makespan);
  }

  // Initialize the optimal schedules array.
  const optimalSchedules = [];

  // Iterate through the cloudlets.
  for (let i = 0; i < cloudlets.length; i++) {

    // Find the datacenter with the minimum makespan.
    const minMakespan = Math.min(...makespans);

    // Assign the cloudlet to the datacenter with the minimum makespan.
    optimalSchedules.push({
      "cloudlet": cloudlets[i],
      "datacenter": datacenters[makespans.indexOf(minMakespan)]
    });

    // Update the makespans array.
    makespans = [];
    for (let j = 0; j < datacenters.length; j++) {
      makespans.push(datacenters[j].makespan);
    }
  }

  // Return the optimal schedules.
  return optimalSchedules;
}


const cloudlets = [
  {
    "length": 1,
    "deadline": 2
  },
  {
    "length": 2,
    "deadline": 3
  },
  {
    "length": 3,
    "deadline": 4
  }
];

const datacenters = [
  {
    "capacity": 1,
    "makespan": 1
  },
  {
    "capacity": 2,
    "makespan": 2
  },
  {
    "capacity": 3,
    "makespan": 3
  }
];

const optimalSchedules = findOptimalSchedules(cloudlets, datacenters);

console.log(optimalSchedules);
