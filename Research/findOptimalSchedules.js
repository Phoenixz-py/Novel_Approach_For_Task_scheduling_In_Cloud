// class Datacenter {
//   constructor() {
//     this.vms = [];
//     this.cloudlets = [];
//   }

//   addVM(vm) {
//     this.vms.push(vm);
//   }

//   addCloudlet(cloudlet) {
//     this.cloudlets.push(cloudlet);
//   }

//   getMakespan() {
//     let makespan = 0;
//     for (let i = 0; i < this.cloudlets.length; i++) {
//       makespan += this.cloudlets[i].length;
//     }
//     return makespan;
//   }
// }

// class VM {
//   constructor(mips) {
//     this.mips = mips;
//     this.cloudlets = [];
//   }

//   addCloudlet(cloudlet) {
//     this.cloudlets.push(cloudlet);
//   }

//   getMakespan() {
//     let makespan = 0;
//     for (const cloudlet of this.cloudlets) {
//       makespan += cloudlet.length / this.mips;
//     }
//     return makespan;
//   }
// }

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
    return Math.max(...busy_time.values());
  }
}

class VM {
  constructor(mips) {
    this.mips = mips;
    this.cloudlets = [];
  }

  addCloudlet(cloudlet) {
    this.cloudlets.push(cloudlet);
  }

  getMakespan() {
    let makespan = 0;
    for (const cloudlet of this.cloudlets) {
      makespan += cloudlet.length / this.mips;
    }

    // Convert the Python code to JavaScript.
    const busy_time = {};
    for (const task of this.cloudlets) {
      if (!busy_time[task]) {
        busy_time[task] = task.length / this.mips;
      } else {
        busy_time[task] += task.length / this.mips;
      }
    }

    // Return the maximum busy time.
    return Math.max(...busy_time.values());
  }
}


class OrderedPerformanceCurve {
  constructor(makespans) {
    this.makespans = makespans;
  }

  plot() {
    console.log("Plotting the makespans:", this.makespans);
    // Plot the makespans on a graph.
  }

  getAverageMakespan() {
    const totalMakespan = this.makespans.reduce(
      (sum, makespan) => sum + makespan,
      0
    );
    const averageMakespan = totalMakespan / this.makespans.length;
    return averageMakespan;
  }
}

function findOptimalSchedulesBranchAndBound(cloudlets) {
  // Create a list of all possible schedules.
  const allSchedules = [];

  // Recursively generate all possible schedules.
  function generateSchedules(cloudlets, currentSchedule) {
    if (cloudlets.length === 0) {
      allSchedules.push(currentSchedule);
    } else {
      for (let i = 0; i < cloudlets.length; i++) {
        const newSchedule = currentSchedule.slice();
        newSchedule.push(cloudlets[i]);
        generateSchedules(cloudlets.slice(i + 1), newSchedule);
      }
    }
  }

  // Sort the schedules by makespan.
  generateSchedules(cloudlets, []);
  allSchedules.sort((a, b) => a.makespan - b.makespan);

  // Find the minimum makespan.
  let minMakespan = allSchedules[0].makespan;

  // Find the optimal schedules.
  const optimalSchedules = [];
  for (const schedule of allSchedules) {
    if (schedule.makespan === minMakespan) {
      optimalSchedules.push(schedule);
    }
  }

  // Return the optimal schedules.
  return optimalSchedules;
}


const cloudlets = [
  {
    length: 1,
    deadline: 2,
    mips: 100,
  },
  {
    length: 2,
    deadline: 3,
    mips: 200,
  },
  {
    length: 3,
    deadline: 4,
    mips: 300,
  },
];

const optimalSchedules = findOptimalSchedulesBranchAndBound(cloudlets);

console.log(optimalSchedules);