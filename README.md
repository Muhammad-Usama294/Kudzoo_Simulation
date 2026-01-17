# 🌱 Kudzoo Simulation - Byzantine Fault Tolerant Consensus

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![BFT](https://img.shields.io/badge/BFT-Consensus-green.svg)
![Distributed Systems](https://img.shields.io/badge/Distributed-Systems-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A Python-based simulation of the Kudzu BFT consensus protocol for distributed systems research. This project provides a comprehensive implementation of Byzantine Fault Tolerant consensus with AVID (Asynchronous Verifiable Information Dispersal) for educational and research purposes.

## 🎯 Features

### 🛡️ BFT Consensus Protocol
- **Byzantine Fault Tolerance**: Tolerates up to `f` Byzantine faults with `n = 3f + 1` replicas
- **View-based Consensus**: Structured view management for reliable consensus progression
- **Leader Election and Rotation**: Automatic leader selection based on view number with smart rotation to skip failed nodes
- **Dynamic Path Selection**: Fast path and slow path consensus based on vote collection

### 🔐 AVID (Asynchronous Verifiable Information Dispersal)
- **Merkle Tree-based Verification**: Cryptographic proof system for data authenticity
- **Fragment Distribution**: Data is split into `n` fragments with `p` parity fragments using Reed-Solomon erasure coding
- **Cryptographic Proof Verification**: Each replica verifies Merkle proofs before voting
- **Fault-tolerant Data Encoding**: Enables reconstruction even with missing fragments

### 🔄 Replica Management
- **Multi-replica Coordination**: Supports dynamic replica configurations (tested with 4-7 nodes)
- **Socket-based Communication**: Efficient TCP socket communication between replicas
- **Process Pool Execution**: CPU-intensive encoding operations handled by ProcessPoolExecutor
- **Asynchronous Message Handling**: Non-blocking message processing with threading

### ⚡ Fault Injection
- **Message Delay Simulation**: Configurable network latency (milliseconds)
- **Message Drop Simulation**: Probabilistic message loss (0.0 - 1.0)
- **Byzantine Behavior Testing**: Simulate various failure scenarios
- **Node Kill/Resurrection**: Dynamic fault injection through dashboard

### 📊 Coordinator/Monitoring System
- **Real-time Replica Status Tracking**: Live monitoring of all replica states
- **Vote Collection Monitoring**: Track voting progress per block
- **Block Finalization Tracking**: Monitor consensus completion
- **Fault Status Dashboard**: Visual representation of node health (HEALTHY, SLOW, DEAD)
- **Metrics Aggregation**: Cumulative statistics on finalized blocks and consensus paths

### 📈 Performance Metrics
- **Fragment Distribution Tracking**: Monitor AVID fragment dissemination
- **Vote Collection Analysis**: Track voting patterns and thresholds
- **Consensus Latency Measurement**: Measure time to finalization
- **Fast vs. Slow Path Statistics**: Compare consensus path efficiency

## 🛠️ Technologies Used

- **Language**: Python 3.x
- **Networking**: Socket programming (TCP)
- **Concurrency**: 
  - Threading for message handling
  - ProcessPoolExecutor for parallel encoding
- **Cryptography**: 
  - SHA-256 hashing
  - Merkle Trees for verification
  - Reed-Solomon erasure coding (`reedsolo`)
- **Communication**: JSON-based message passing
- **Web Framework**: 
  - Flask (REST API for coordinator)
  - Streamlit (interactive dashboard)
- **Data Processing**: Pandas, Plotly for visualization

## 🏗️ System Architecture

```
Kudzoo_Simulation/
├── Coordinator (Port 5000)
│   ├── Flask REST API
│   ├── Replica Registration
│   ├── Fault Injection Manager
│   ├── Vote Aggregation
│   └── Metrics Collection
│
├── Replicas (Ports 6000+)
│   ├── Consensus Protocol Engine
│   ├── AVID Encoding/Verification
│   ├── Inter-replica Communication
│   └── View Management
│
├── Dashboard (Port 8501)
│   ├── Real-time Monitoring
│   ├── Fault Injection UI
│   └── Metrics Visualization
│
└── Core Components
    ├── Merkle Tree Cryptography
    ├── Reed-Solomon Encoding
    ├── Fragment Distribution
    └── Byzantine Fault Tolerance
```

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Muhammad-Usama294/Kudzoo_Simulation.git
cd Kudzoo_Simulation

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
The `requirements.txt` includes:
- `flask==3.0.0` - Web framework for coordinator API
- `requests==2.31.0` - HTTP client for inter-component communication
- `streamlit==1.30.0` - Interactive dashboard framework
- `reedsolo==1.7.0` - Reed-Solomon erasure coding library
- `plotly==5.18.0` - Advanced visualization library
- `pandas==2.2.0` - Data manipulation and analysis

## 🚀 How to Run

### Quick Start (Automated Launcher)

The easiest way to start the simulation is using the interactive launcher:

```bash
python launcher.py
```

The launcher will:
1. **Prompt for configuration** (N, f, p parameters with validation)
2. **Start the coordinator** on port 5000
3. **Launch N replicas** on ports 6000, 6001, 6002, ...
4. **Open the dashboard** at http://localhost:8501

Example session:
```
========================================
   🌱 KUDZU BFT SIMULATOR SETUP   
========================================
Enter Total Nodes (N) [Press Enter for 7]: 4
Enter Byzantine Faults (f) [Press Enter for 1]: 1
Enter Passive/Slow Nodes (p) [Press Enter for 1]: 1

✅ Configuration Accepted: N=4, f=1, p=1

--- STARTING KUDZU BFT SIMULATION (N=4, F=1, P=1) ---
1. Launching Coordinator...
2. Launching 4 Replicas...
3. Launching Dashboard...

✅ SYSTEM ONLINE
   -> Dashboard: http://localhost:8501
   -> Press Ctrl+C to stop
```

### Manual Start (Advanced)

For more control, start each component manually:

```bash
# Terminal 1: Start the coordinator
python -m core.coordinator --n 4 --f 1 --p 1

# Terminal 2-5: Start replicas (one per terminal)
python -m core.replica --id 0 --n 4 --f 1 --p 1
python -m core.replica --id 1 --n 4 --f 1 --p 1
python -m core.replica --id 2 --n 4 --f 1 --p 1
python -m core.replica --id 3 --n 4 --f 1 --p 1

# Terminal 6: Start the dashboard
streamlit run ui/dashboard.py

# Access monitoring dashboard at:
# http://localhost:8501
```

## ⚙️ Configuration Parameters

| Parameter | Description | Default | Constraints |
|-----------|-------------|---------|-------------|
| `n` | Total number of replicas | 7 | `n ≥ 3f + 2p + 1` |
| `f` | Maximum Byzantine faults tolerated | 1 | `f < n/3` |
| `p` | Number of parity/slow replicas | 1 | `p < n/2` |

### Port Configuration
- **Coordinator**: Port 5000 (HTTP API)
- **Replicas**: Port 6000 + replica_id (TCP)
- **Dashboard**: Port 8501 (Streamlit)

### Example Configurations

```bash
# Minimal setup (4 nodes, 1 fault)
N=4, f=1, p=1

# Standard setup (7 nodes, 2 faults)
N=7, f=2, p=1

# Large deployment (10 nodes, 3 faults)
N=10, f=3, p=1
```

## 🔬 Protocol Overview

### BFT Consensus Flow

The Kudzu consensus protocol operates in the following phases:

1. **Leader Selection**
   - Leader for view `v` is replica `(v mod n)`
   - Smart rotation skips DEAD nodes automatically
   - View number increments with each new block proposal

2. **Block Proposal (AVID Distribution)**
   - Leader encodes block data using Reed-Solomon encoding
   - Data split into `n` fragments with `(n-k)` parity fragments
   - Merkle tree constructed from all fragments
   - Each fragment distributed with its Merkle proof

3. **Fragment Verification**
   - Each replica receives its fragment and proof
   - Verifies Merkle proof against root hash
   - Proof validation ensures data authenticity and integrity

4. **Voting Phase**
   - After successful verification, replica broadcasts VOTE message
   - Votes include block ID and source replica ID
   - All replicas collect votes from the network

5. **Finalization**
   - **Fast Path**: Block finalized when `(n - p)` votes collected
   - **Slow Path**: Block finalized when `(n - f - p)` votes collected (after timeout)
   - Finalization triggers metric reporting to coordinator

### AVID Protocol Details

```
Original Data (bytes)
      ↓
[Reed-Solomon Encoding]
      ↓
n data fragments + (n-k) parity fragments
      ↓
[Merkle Tree Construction]
      ↓
Root Hash + Individual Proofs
      ↓
[Fragment Distribution]
      ↓
Each replica gets: [fragment, proof, root]
      ↓
[Verification]
      ↓
verify_proof(fragment, proof, root, index) → bool
```

**Key Properties:**
- **Integrity**: Merkle proofs ensure fragment authenticity
- **Availability**: Data reconstructible from any `k` fragments
- **Verifiability**: Each replica independently verifies its fragment
- **Fault Tolerance**: Tolerates up to `(n-k)` missing fragments

## 🌐 Network Architecture

```
Coordinator (HTTP Server - Port 5000)
     ↓
   Report API (/report, /inject_block, /fault)
     ↓
┌─────────────────────────┐
│  Replica 0 (Leader v=0) │──┐
│  Port: 6000             │  │
└─────────────────────────┘  │
                              │ Broadcast Network
┌─────────────────────────┐  │ (Proposals & Votes)
│  Replica 1              │←─┤ 
│  Port: 6001             │  │ TCP Sockets
└─────────────────────────┘  │
                              │
┌─────────────────────────┐  │
│  Replica 2              │←─┤
│  Port: 6002             │  │
└─────────────────────────┘  │
                              │
┌─────────────────────────┐  │
│  Replica 3              │←─┘
│  Port: 6003             │
└─────────────────────────┘
```

**Message Types:**
- `INJECT`: Coordinator → Leader (trigger block proposal)
- `PROPOSAL`: Leader → All Replicas (AVID fragments)
- `VOTE`: Replica → All Replicas (vote for block)
- `FAULT`: Coordinator → Replica (inject faults)

## 🧩 Key Classes and Methods

### `KudzuReplica` (core/replica.py)

The main replica class implementing the BFT consensus protocol.

**Key Methods:**

```python
def __init__(self, replica_id, n, f, p)
    # Initialize replica with ID, total replicas, fault tolerance, and parity
    # Sets up socket server on port 6000 + replica_id
    # Creates ProcessPoolExecutor for encoding tasks

def propose_block(self, view)
    # Leader logic for block proposal
    # Encodes data, builds Merkle tree, distributes fragments
    # Called when replica receives INJECT message

def handle_proposal(self, msg)
    # Process incoming PROPOSAL messages
    # Verify Merkle proof for received fragment
    # Broadcast VOTE if verification succeeds

def handle_vote(self, msg)
    # Process VOTE messages from other replicas
    # Track votes per block ID
    # Finalize block when threshold reached (fast/slow path)

def broadcast(self, msg)
    # Send message to all replicas except self
    # Uses multithreading for parallel transmission
    # Applies fault injection (delay, drop)

def _send(self, target_id, msg)
    # Send message to specific replica
    # Implements fault injection logic
    # TCP socket connection with timeout

def run(self)
    # Main event loop
    # Registers with coordinator
    # Listens for incoming messages
```

### `MerkleTree` (core/crypto.py)

Cryptographic verification using Merkle trees.

**Key Methods:**

```python
def __init__(self, data_fragments)
    # Build Merkle tree from fragment list
    # Compute root hash

def _hash(self, data)
    # SHA-256 hashing function

def _build_tree(self, leaves)
    # Construct tree bottom-up
    # Pair-wise hashing until single root

def get_proof(self, index)
    # Generate Merkle proof for fragment at index
    # Returns list of sibling hashes

@staticmethod
def verify_proof(fragment, proof, root, index)
    # Verify fragment authenticity
    # Recompute path from leaf to root
    # Returns True if root matches
```

### `worker_encode(data_bytes, n, k)` (core/crypto.py)

Parallel encoding function for AVID.

```python
def worker_encode(data_bytes, n, k)
    # Reed-Solomon encoding with (n-k) parity
    # Split into n fragments
    # Build Merkle tree and generate proofs
    # Returns: (fragments, root, proofs)
```

### Coordinator API (core/coordinator.py)

Flask REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register` | POST | Replica registration |
| `/inject_block` | POST | Trigger new block proposal |
| `/report` | POST | Receive replica reports (fragments, votes, finalization) |
| `/fault` | POST | Inject faults into specific replica |
| `/metrics` | GET | Retrieve system metrics and status |

## 💉 Fault Injection

The system supports dynamic fault injection for testing Byzantine behavior:

### Via Dashboard UI
1. Open dashboard at http://localhost:8501
2. Use "Fault Injection" sidebar controls
3. Select target node (0 to n-1)
4. Click "💀 Kill" to simulate node failure (100% message drop)
5. Click "✅ Reset" to restore node to healthy state

### Programmatic Injection

```python
# Inject message delay (milliseconds)
replica.faults['delay'] = 100  # 100ms latency

# Inject message drop probability (0.0 - 1.0)
replica.faults['drop'] = 0.2   # 20% packet loss

# Simulate complete node failure
replica.faults['drop'] = 1.0   # 100% packet loss (DEAD)
```

### Fault Behaviors

| Fault Type | Parameter | Effect | Status |
|------------|-----------|--------|--------|
| Delay | `delay > 0` | Network latency simulation | SLOW |
| Drop | `0 < drop < 0.5` | Packet loss | SLOW |
| Kill | `drop ≥ 0.5` | Node failure | DEAD |
| Reset | `delay=0, drop=0` | Normal operation | HEALTHY |

### Coordinator Response

When a leader is marked DEAD, the coordinator automatically:
1. Skips the DEAD leader
2. Increments view number
3. Selects next living replica as leader
4. Retries up to N times until finding healthy leader

## 🔍 Research Context

This simulation is based on research in distributed systems and Byzantine fault tolerance:

### Core Concepts

- **Byzantine Fault Tolerance**: System tolerates arbitrary (malicious) failures
- **Asynchronous Consensus**: No assumptions about message timing
- **Verifiable Information Dispersal**: Cryptographically provable data distribution
- **Erasure Coding**: Efficient redundancy via Reed-Solomon codes

### Theoretical Foundation

The implementation follows principles from:
- **Byzantine Generals Problem** (Lamport et al.)
- **PBFT** - Practical Byzantine Fault Tolerance (Castro & Liskov)
- **HotStuff** - Linear consensus protocol
- **Kudzu** - Asynchronous BFT with dual-path optimization

### Key Properties

- **Safety**: At most one block finalized per view
- **Liveness**: System makes progress with ≤ f Byzantine faults
- **Agreement**: All honest replicas agree on finalized blocks
- **Validity**: Only valid blocks proposed by honest leaders are finalized

## 💡 Use Cases

### 🎓 Education
- **Learn BFT Consensus**: Understand Byzantine fault tolerance in practice
- **Study Distributed Algorithms**: See consensus protocols in action
- **Explore Cryptographic Proofs**: Understand Merkle tree verification
- **Analyze Network Protocols**: Observe message passing and coordination

### 🔬 Research
- **Test Byzantine Strategies**: Experiment with different fault patterns
- **Evaluate Consensus Variants**: Modify protocol parameters
- **Study Performance Trade-offs**: Analyze fast path vs. slow path
- **Develop New Mechanisms**: Prototype consensus improvements

### 🧪 Simulation
- **Model Distributed Behavior**: Simulate real-world distributed systems
- **Analyze Fault Scenarios**: Test system behavior under failures
- **Validate Theoretical Models**: Compare simulation with analytical results
- **Demonstrate Protocol Properties**: Verify safety and liveness

### 📊 Benchmarking
- **Measure Consensus Latency**: Track time to finalization
- **Evaluate Throughput**: Test blocks per second
- **Compare Path Efficiency**: Fast path vs. slow path statistics
- **Stress Test**: Run with large N and high fault rates

## 🚧 Future Enhancements

### Short-term Goals
- [ ] Enhanced web-based visualization dashboard with real-time charts
- [ ] Additional fault injection scenarios (network partitions, crash-recovery)
- [ ] Performance profiling and bottleneck analysis
- [ ] Configurable timeout mechanisms for slow path transitions
- [ ] Persistent logging of all consensus rounds

### Medium-term Goals
- [ ] Network partition simulation (split-brain scenarios)
- [ ] Recovery mechanism implementation (catch-up protocols)
- [ ] Multi-threaded replica processing for improved throughput
- [ ] Database persistence for consensus history and replay
- [ ] Advanced metrics: throughput graphs, latency histograms

### Long-term Goals
- [ ] Support for multiple concurrent consensus instances
- [ ] Integration with real blockchain systems
- [ ] Heterogeneous fault models (crash vs. Byzantine)
- [ ] Formal verification of protocol properties
- [ ] Docker containerization for distributed deployment

## 📚 Academic References

### Foundational Papers

1. **Byzantine Generals Problem**
   - Lamport, L., Shostak, R., & Pease, M. (1982). "The Byzantine Generals Problem." ACM Transactions on Programming Languages and Systems.

2. **Practical Byzantine Fault Tolerance (PBFT)**
   - Castro, M., & Liskov, B. (1999). "Practical Byzantine Fault Tolerance." OSDI.

3. **Asynchronous Consensus Protocols**
   - Cachin, C., Kursawe, K., & Shoup, V. (2005). "Random Oracles in Constantinople: Practical Asynchronous Byzantine Agreement using Cryptography." Journal of Cryptology.

4. **Erasure Coding and Information Dispersal**
   - Rabin, M. O. (1989). "Efficient Dispersal of Information for Security, Load Balancing, and Fault Tolerance." Journal of the ACM.

### Modern BFT Systems

5. **HotStuff: BFT Consensus with Linearity and Responsiveness**
   - Yin, M., et al. (2019). "HotStuff: BFT Consensus with Linearity and Responsiveness." PODC.

6. **Tendermint: Consensus without Mining**
   - Buchman, E. (2016). "Tendermint: Byzantine Fault Tolerance in the Age of Blockchains."

### Related Topics

7. **Information Dispersal Algorithms**
   - Cachin, C., & Tessaro, S. (2005). "Asynchronous Verifiable Information Dispersal."

8. **Reed-Solomon Codes**
   - Reed, I. S., & Solomon, G. (1960). "Polynomial Codes over Certain Finite Fields."

## 🤝 Contributing

We welcome contributions to the Kudzoo Simulation project! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: Open an issue describing the bug and steps to reproduce
- 💡 **Suggest Features**: Share ideas for new features or improvements
- 📖 **Improve Documentation**: Fix typos, clarify explanations, add examples
- 🔧 **Submit Code**: Fork, develop, and submit pull requests

### Development Workflow

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Kudzoo_Simulation.git
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** with clear, focused commits
5. **Test thoroughly** - ensure existing functionality isn't broken
6. **Submit a pull request** with a clear description of changes

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular
- Write docstrings for public methods

### Testing

Before submitting:
- Test with various configurations (different N, f, p values)
- Verify fault injection scenarios work correctly
- Ensure no regression in existing features
- Test both automated launcher and manual startup

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 Muhammad Usama

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

This simulation is built for educational and research purposes to help students and researchers understand Byzantine Fault Tolerant consensus protocols. Special thanks to the distributed systems research community for foundational work in this area.

---

**Repository**: [Muhammad-Usama294/Kudzoo_Simulation](https://github.com/Muhammad-Usama294/Kudzoo_Simulation)

**Questions or Issues?** Open an issue on GitHub or contact the maintainer.

🌱 *Building reliable distributed systems, one consensus at a time.*
