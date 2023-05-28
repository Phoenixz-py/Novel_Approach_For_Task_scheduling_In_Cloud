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
    return makespan;
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
    const makespan = 0;
    for (const cloudlet of this.cloudlets) {
      makespan += cloudlet.processingTime / this.mips;
    }
    return makespan;
  }
}

class OrderedPerformanceCurve {
  constructor(makespans) {
    this.makespans = makespans;
  }

  plot() {}

  getAverageMakespan() {}
}

function findOptimalSchedulesGreedy(cloudlets) {
  cloudlets.sort((a, b) => a.deadline - b.deadline);

  const datacenters = [];
  for (let i = 0; i < cloudlets.length; i++) {
    datacenters.push(new Datacenter());
  }

  const vms = [];
  for (let i = 0; i < cloudlets.length; i++) {
    vms.push(new VM(cloudlets[i].mips));
  }

  for (let i = 0; i < cloudlets.length; i++) {
    datacenters[i].addCloudlet(cloudlets[i]);
  }

  const makespans = [];
  for (let i = 0; i < datacenters.length; i++) {
    makespans.push(datacenters[i].getMakespan());
  }

  let minMakespan = makespans[0];
  for (let i = 1; i < makespans.length; i++) {
    if (makespans[i] < minMakespan) {
      minMakespan = makespans[i];
    }
  }

  // Find the optimal schedules.
  const optimalSchedules = [];
  for (let i = 0; i < makespans.length; i++) {
    if (makespans[i] == minMakespan) {
      optimalSchedules.push(datacenters[i]);
    }
  }

  // Print the output, not workifn right now

  console.log("The minimum makespan is", minMakespan);
  console.log("The optimal schedules are:");
  for (const optimalSchedule of optimalSchedules) {
    console.log(optimalSchedule);
  }

  return optimalSchedules;
}

const cloudlets = [
  {
    length: 1,
    deadline: 2,
  },
  {
    length: 2,
    deadline: 3,
  },
  {
    length: 3,
    deadline: 4,
  },
];

// Find the optimal schedules.
const optimalSchedules = findOptimalSchedulesGreedy(cloudlets);

//output.
console.log(optimalSchedules);
