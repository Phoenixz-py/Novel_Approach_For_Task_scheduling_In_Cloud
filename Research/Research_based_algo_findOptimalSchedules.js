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

// function findOptimalSchedules(cloudlets) {
//   // Create a list of data centers.
//   const datacenters = [];
//   for (let i = 0; i < cloudlets.length; i++) {
//     datacenters.push(new Datacenter());
//   }

//   // Create a list of virtual machines.
//   const vms = [];
//   for (let i = 0; i < cloudlets.length; i++) {
//     vms.push(new VM(cloudlets[i].mips));
//   }

//   // Randomly assign each virtual machine to a data center.
//   for (let i = 0; i < datacenters.length; i++) {
//     datacenters[Math.floor(Math.random() * datacenters.length)].addVM(vms[i]);
//   }

//   // Randomly assign each cloudlet to a virtual machine.
//   for (let i = 0; i < cloudlets.length; i++) {
//     datacenters[Math.floor(Math.random() * vms.length)].addCloudlet(cloudlets[i]);
//   }

//   // Calculate the makespan for each schedule.
//   const makespans = [];
//   for (let i = 0; i < datacenters.length; i++) {
//     makespans.push(datacenters[i].getMakespan());
//   }

//   // Find the minimum makespan.
//   let minMakespan = makespans[0];
//   for (let i = 1; i < makespans.length; i++) {
//     if (makespans[i] < minMakespan) {
//       minMakespan = makespans[i];
//     }
//   }

//   // Find the optimal schedules.
//   const optimalSchedules = [];
//   for (let i = 0; i < makespans.length; i++) {
//     if (makespans[i] == minMakespan) {
//       optimalSchedules.push(datacenters[i]);
//     }
//   }

//   // Return the list of optimal schedules.
//   return optimalSchedules;
// }

// Create a list of cloudlets.


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

// Find the optimal schedules.
const optimalSchedules = findOptimalSchedulesGreedy(cloudlets);

//output.
console.log(optimalSchedules);


