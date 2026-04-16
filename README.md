# Energy System Optimization Model ⚡

This project is a simplified energy system optimization model built using Python and Pyomo. It simulates electricity generation and transmission between two nodes using cost-minimization.

## 📌 Overview

The model determines the optimal mix of:
- Wind generation
- Solar generation
- Gas generation
- Transmission capacity between nodes

It minimizes total system cost while meeting demand constraints.

## 🧠 Key Features

- Multi-node energy system (Node A and B)
- Hourly demand balancing
- Renewable generation constraints using capacity factors
- Transmission flow limits
- Cost-based optimization using linear programming

## ⚙️ Technologies Used

- Python
- Pyomo
- HiGHS Solver

## 📊 Model Components

### Decision Variables
- Generation: wind, solar, gas
- Capacity: wind, solar, gas, transmission
- Power flow between nodes

### Constraints
- Demand satisfaction at each node
- Generation limits based on capacity
- Transmission capacity limits

### Objective
Minimize:
- Generation cost (gas)
- Capacity investment cost (wind, solar, gas, transmission)

## 🚀 How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the model:
   python test.py
## 📈 Example Output

- Optimal capacities for each energy source
- Power flow between nodes
- Hourly dispatch results

## 💡 Future Improvements

- Add storage (battery systems)
- Expand to multiple nodes
- Include emissions constraints
- Add visualization of results

---

## 👩‍💻 Author

Ahalditha  
Master’s in Sustainable Energy Engineering (Lund University)
