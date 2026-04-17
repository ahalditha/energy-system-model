# Energy System Optimization Model ⚡

This project implements a data-driven energy system optimization model using Python and Pyomo. It simulates electricity generation, capacity expansion, and transmission between two interconnected nodes under a cost-minimization framework.

The model uses:
- Hourly electricity demand data (imported from CSV files)
- Renewable generation profiles (wind and solar capacity factors)
- Linear optimization to determine optimal generation dispatch and capacity investments

This project is inspired by academic energy system modelling approaches and serves as a simplified implementation of real-world power system optimization problems.

## 📌 Overview

The model determines the optimal mix of:
- Wind generation
- Solar generation
- Gas generation
- Transmission capacity between nodes

It minimizes total system cost while meeting demand constraints.

## 📊 Data Sources

- Demand data: manually extracted and structured from reference study
- Wind and solar profiles: representative capacity factor time series
- Time resolution: hourly (24-hour simplified case)

Note: This is a simplified representation of real-world datasets such as ENTSO-E (demand) and ERA5 (renewables), used in large-scale energy system models.

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
