from pyomo.environ import *

# -----------------------------
# 1. DATA
# -----------------------------

hours = [1, 2, 3]
nodes = ["A", "B"]

# Demand at each node
demand = {
    ("A", 1): 2, ("A", 2): 3, ("A", 3): 2,
    ("B", 1): 6, ("B", 2): 9, ("B", 3): 8
}

# Wind availability (better in A)
wind_cf = {
    ("A", 1): 0.6, ("A", 2): 0.4, ("A", 3): 0.5,
    ("B", 1): 0.2, ("B", 2): 0.1, ("B", 3): 0.2
}

# Solar availability (better in B)
solar_cf = {
    ("A", 1): 0.0, ("A", 2): 0.3, ("A", 3): 0.1,
    ("B", 1): 0.0, ("B", 2): 0.7, ("B", 3): 0.4
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

    

