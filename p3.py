from pulp import *

t, p, max = input().split()
t = int(t) # number of toys
p = int(p) # number of special packages
max = int(max) # max production capacity

# variable to store the problem data
prob = LpProblem("UbiquityInc_Daily_Profit", LpMaximize)
total_toys = 0
goal = 0
toys = [0]

for i in range(1, t + 1):
    l, c = input().split()
    l = int(l) # profit per toy
    c = int(c) # production capacity per toy
    toy_var = LpVariable("Toy" + str(i), 0, c, LpInteger)  # toy variables
    package_var = LpVariable("Package" + str(i), 0, c, LpInteger) # package variables
    toys.append({"l": l, "c": c, "toy_var": toy_var, "package_var": package_var})
    prob += package_var <= toy_var, "PackageConstraint" + str(i) # package constraint
    goal += (toy_var - package_var) * l
    total_toys += toy_var - package_var

for m in range(1, p + 1):
    i, j, k, l = input().split()
    i = int(i) # toy 1
    j = int(j) # toy 2
    k = int(k) # toy 3
    l = int(l) # profit per special package
    # pick the minimum production capacity of the 3 toys
    min_package_var = LpVariable("MinPackage" + str(m), 0, None, LpInteger) 
    prob += min_package_var <= toys[i]["package_var"], f"MinPackageConstraint{i}_{m}"
    prob += min_package_var <= toys[j]["package_var"], f"MinPackageConstraint{j}_{m}"
    prob += min_package_var <= toys[k]["package_var"], f"MinPackageConstraint{k}_{m}"
    toys[i]["package_var"] -= min_package_var
    toys[j]["package_var"] -= min_package_var
    toys[k]["package_var"] -= min_package_var
    goal += min_package_var * l
    total_toys += min_package_var * 3

prob += total_toys <= max, "Production Capacity"  # production capacity constraint
prob += goal, "Maximize Profit" 
prob.solve(GLPK(msg=0))

max_profit = value(prob.objective)
print(int(max_profit))
