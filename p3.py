from pulp import *

def create_auxiliary_structures(package_dict, t, p):
    aux = {i: [] for i in range(1, t + 1)}
    packages = []

    for i in range(1, p + 1):
        l = package_dict[i]
        for toy_id in l[:3]:
            aux[toy_id].append(i)
        packages.append(l)

    return aux, packages

def define_decision_variables(toys, packages):
    toy_vars = {i: LpVariable(f"toy{i}", 0, toy[1], LpInteger) for i, toy in toys.items()}
    
    package_vars = {
        k: LpVariable(f"pack{k}", 0, min(toys[pack[0]][1] for pack in packages[k - 1:k]), LpInteger)
        for k in range(1, len(packages) + 1)
    }

    return toy_vars, package_vars

def set_objective_function(prob, toys, packages, toy_vars, package_vars):
    prob += lpSum([toys[i][0] * toy_vars[i] for i in range(1, len(toys) + 1)]) + \
            lpSum([packages[k - 1][3] * package_vars[k] for k in range(1, len(packages) + 1)])

def set_constraints(prob, toys, aux, toy_vars, package_vars):
    for i in range(1, len(toys) + 1):
        prob += lpSum([package_vars[j] for j in aux[i]]) + toy_vars[i] <= toys[i][1]

def set_goal_constraint(prob, toy_vars, package_vars, max):
    goal = lpSum(list(toy_vars.values())) + lpSum(3 * list(package_vars.values())) <= max
    prob += goal

def solve_optimization_problem():
    t, p, max = map(int, input().split())
    toys = {i: list(map(int, input().split())) for i in range(1, t + 1)}
    package_dict = {i: list(map(int, input().split())) for i in range(1, p + 1)}
    aux, packages = create_auxiliary_structures(package_dict, t, p)

    prob = LpProblem("UbiquityInc_Daily_Profit", LpMaximize)

    toy_vars, package_vars = define_decision_variables(toys, packages)
    set_objective_function(prob, toys, packages, toy_vars, package_vars)
    set_constraints(prob, toys, aux, toy_vars, package_vars)
    set_goal_constraint(prob, toy_vars, package_vars, max)

    prob.solve(GLPK(msg = 0))
    max_profit = int(value(prob.objective))
    print(max_profit)

solve_optimization_problem()
