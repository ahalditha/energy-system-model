import pandas as pd
from pyomo.environ import *

# -----------------------------
# 1. DATA
# -----------------------------

hours = list(range(1, 25))
nodes = ["A", "B"]

# Demand at each node from CSV files
demand_A_data = pd.read_csv("data/demand_A.csv", encoding="utf-8")
demand_B_data = pd.read_csv("data/demand_B.csv", encoding="utf-8")

demand = {}

for _, row in demand_A_data.iterrows():
    demand[("A", int(row["hour"]))] = float(row["demand"])

for _, row in demand_B_data.iterrows():
    demand[("B", int(row["hour"]))] = float(row["demand"])

# Wind availability (better in A)
wind_cf = {
    ("A", 1): 0.60, ("A", 2): 0.58, ("A", 3): 0.55, ("A", 4): 0.53,
    ("A", 5): 0.50, ("A", 6): 0.48, ("A", 7): 0.45, ("A", 8): 0.42,
    ("A", 9): 0.40, ("A", 10): 0.38, ("A", 11): 0.36, ("A", 12): 0.35,
    ("A", 13): 0.34, ("A", 14): 0.36, ("A", 15): 0.38, ("A", 16): 0.40,
    ("A", 17): 0.43, ("A", 18): 0.46, ("A", 19): 0.50, ("A", 20): 0.54,
    ("A", 21): 0.57, ("A", 22): 0.59, ("A", 23): 0.60, ("A", 24): 0.61,

    ("B", 1): 0.22, ("B", 2): 0.21, ("B", 3): 0.20, ("B", 4): 0.19,
    ("B", 5): 0.18, ("B", 6): 0.17, ("B", 7): 0.16, ("B", 8): 0.15,
    ("B", 9): 0.14, ("B", 10): 0.13, ("B", 11): 0.12, ("B", 12): 0.12,
    ("B", 13): 0.11, ("B", 14): 0.12, ("B", 15): 0.13, ("B", 16): 0.14,
    ("B", 17): 0.15, ("B", 18): 0.17, ("B", 19): 0.18, ("B", 20): 0.19,
    ("B", 21): 0.20, ("B", 22): 0.21, ("B", 23): 0.22, ("B", 24): 0.23
}

# Solar availability (better in B)
solar_cf = {
    ("A", 1): 0.00, ("A", 2): 0.00, ("A", 3): 0.00, ("A", 4): 0.00,
    ("A", 5): 0.02, ("A", 6): 0.05, ("A", 7): 0.10, ("A", 8): 0.18,
    ("A", 9): 0.28, ("A", 10): 0.38, ("A", 11): 0.45, ("A", 12): 0.48,
    ("A", 13): 0.46, ("A", 14): 0.40, ("A", 15): 0.30, ("A", 16): 0.20,
    ("A", 17): 0.10, ("A", 18): 0.04, ("A", 19): 0.01, ("A", 20): 0.00,
    ("A", 21): 0.00, ("A", 22): 0.00, ("A", 23): 0.00, ("A", 24): 0.00,

    ("B", 1): 0.00, ("B", 2): 0.00, ("B", 3): 0.00, ("B", 4): 0.00,
    ("B", 5): 0.03, ("B", 6): 0.08, ("B", 7): 0.15, ("B", 8): 0.25,
    ("B", 9): 0.38, ("B", 10): 0.52, ("B", 11): 0.62, ("B", 12): 0.68,
    ("B", 13): 0.65, ("B", 14): 0.56, ("B", 15): 0.42, ("B", 16): 0.28,
    ("B", 17): 0.15, ("B", 18): 0.06, ("B", 19): 0.01, ("B", 20): 0.00,
    ("B", 21): 0.00, ("B", 22): 0.00, ("B", 23): 0.00, ("B", 24): 0.00
}

# Costs
gas_cost = 5
wind_cost = 1
solar_cost = 2
gas_capacity_cost = 1
line_cost = 0.5

# Transmission capacity

# -----------------------------
# 2. MODEL
# -----------------------------

model = ConcreteModel()

model.T = Set(initialize=hours)
model.N = Set(initialize=nodes)

# Dispatch variables
model.wind = Var(model.N, model.T, domain=NonNegativeReals)
model.solar = Var(model.N, model.T, domain=NonNegativeReals)
model.gas = Var(model.N, model.T, domain=NonNegativeReals)

# Capacity variables
model.wind_capacity = Var(model.N, domain=NonNegativeReals)
model.solar_capacity = Var(model.N, domain=NonNegativeReals)
model.gas_capacity = Var(model.N, domain=NonNegativeReals)
model.line_capacity = Var(domain=NonNegativeReals)

# Power flow (A → B)
model.flow = Var(model.T, domain=Reals)

# -----------------------------
# 3. OBJECTIVE
# -----------------------------

def obj_rule(m):
    return (
        sum(gas_cost * m.gas[n, t] for n in m.N for t in m.T)
        + sum(wind_cost * m.wind_capacity[n] for n in m.N)
        + sum(solar_cost * m.solar_capacity[n] for n in m.N)
        + sum(gas_capacity_cost * m.gas_capacity[n] for n in m.N)+ line_cost * m.line_capacity
    )

model.obj = Objective(rule=obj_rule, sense=minimize)

# -----------------------------
# 4. CONSTRAINTS
# -----------------------------

# Demand balance
def demand_rule(m, n, t):
    if n == "A":
        return m.wind[n, t] + m.solar[n, t] + m.gas[n, t] - m.flow[t] >= demand[(n, t)]
    else:
        return m.wind[n, t] + m.solar[n, t] + m.gas[n, t] + m.flow[t] >= demand[(n, t)]

model.demand = Constraint(model.N, model.T, rule=demand_rule)

# Wind limits
def wind_rule(m, n, t):
    return m.wind[n, t] <= wind_cf[(n, t)] * m.wind_capacity[n]

model.wind_limit = Constraint(model.N, model.T, rule=wind_rule)

# Solar limits
def solar_rule(m, n, t):
    return m.solar[n, t] <= solar_cf[(n, t)] * m.solar_capacity[n]

model.solar_limit = Constraint(model.N, model.T, rule=solar_rule)

# Gas limits
def gas_rule(m, n, t):
    return m.gas[n, t] <= m.gas_capacity[n]

model.gas_limit = Constraint(model.N, model.T, rule=gas_rule)

# Transmission limit
def flow_upper(m, t):
    return m.flow[t] <= m.line_capacity

model.flow_upper = Constraint(model.T, rule=flow_upper)
def flow_lower(m, t):
    return m.flow[t] >= -m.line_capacity

model.flow_lower = Constraint(model.T, rule=flow_lower)


# -----------------------------
# 5. SOLVE
# -----------------------------

solver = SolverFactory("highs")
solver.solve(model)

# -----------------------------
# 6. RESULTS
# -----------------------------

print("Optimal capacities:")
print("Line capacity:", model.line_capacity.value)

for n in model.N:
    print(f"{n} Wind:", model.wind_capacity[n].value)
    print(f"{n} Solar:", model.solar_capacity[n].value)
    print(f"{n} Gas:", model.gas_capacity[n].value)
    print("------")

for t in model.T:
    print(f"Hour {t}")
    print(f" Flow A→B: {model.flow[t].value}")
    for n in model.N:
        print(f" {n} Wind: {model.wind[n,t].value}")
        print(f" {n} Solar: {model.solar[n,t].value}")
        print(f" {n} Gas: {model.gas[n,t].value}")
    print("------")

    

