# -*- coding: utf-8 -*-
"""Energy_Cost_Optimisation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18t18B9XVKOQp0cXO5xscq1ld6rMt5ezV
"""

import numpy as np
import ast
from scipy.optimize import linprog
import pandas as pd

# X (Decision Variable Vector) = [X1,X2,X3,X4,X5] all are in Kgs
# Objective function = Minimize Z = C1X1 + C2X2 + C3X3 + C4X4 + C5X5
# Cis are the cost coefficients, units are in Ksh/Kg

cost_coeff = np.array(ast.literal_eval(input('Enter The Energy Costs for the processes 1 to 5: ')))

# Inequality Constraints, here Pis are the demand values
# 1) X1 - X2 ≥ P1 , Yarn
# 2) 0.93X4 - X5 ≥ P2 , Grey Fabric
# 3) 0.96X5 ≥ P3 ,  Finished Fabric
inequality_coeff = np.array([[1, -1, 0, 0, 0], [0, 0, 0, 0.93, -1], [0, 0, 0, 0, 0.96]])
demand_products = np.array(ast.literal_eval(input('Enter The demand for the products: ')))

# Equality Constraints
# 1) 0.97X2 - X4 = 0
# 2) 0.07X4 + 0.03X2 - X3 = 0
equality_coeff = np.array([[0, 0.97, 0, -1, 0], [0, 0.03, -1, 0.07, 0]])
equality_balance = np.zeros(2)

# Time Constraints, here
# X1t1 + X2t2 + X4t4  + X5t5 ≤ T, here ti are fixed for the processes, T is total available time
# t1 = 0.007, t2 = -0.007, t3 = 0 , t4 = 0.013, t5 = 0.0062
time_coeff = np.array([0.007, -0.007, 0, 0.013, 0.0062])
T = int(input('Enter The total Available time here per month: '))

# Non-Negativity Constraints
# Xi ≥ 0  ∀ i ∈ [1,5]
bounds = [(0, None)] * 5

# creating the data for the model, scipy takes only upper bound inequalities,
# so to convert lower bound inequalities into upper bound, multiply entire inequality by -1
total_inequality_constraints = np.vstack((-1 * inequality_coeff, time_coeff))
total_demand_const = np.append(-1 * demand_products, T)

# creating the solver
res = linprog(cost_coeff, A_ub=total_inequality_constraints, b_ub=total_demand_const,
              A_eq=equality_coeff, b_eq=equality_balance, bounds=bounds, method='simplex')

# Storing the output in the dataframe
df = pd.DataFrame(index = ['X1','X2','X3','X4','X5', 'Minimal Energy Cost'],data = {'Optimal Values':np.append(res.x,res.fun)})
pd.options.display.float_format = '{:.2f}'.format
print(df)

import pandas as pd
index = ['Spinning', 'Sizing', 'Rewinding', 'Weaving', 'Wet Processing']
spinning_cost = 50 * 24159.38 * 100 / 2813025.09
sizing_cost = 23759.38 * 7 * 100 / 2813025.09
rewinding_cost = 100 * 40 * 2326.04 / 2813025.09
weaving_cost = 100 * 15 * 23046.59 / 2813025.09
wet_processing_cost = 100 * 48 * 20833.33 / 2813025.09
cost_table = pd.DataFrame({
    'Cost Percentage': [spinning_cost, sizing_cost, rewinding_cost, weaving_cost, wet_processing_cost]
}, index=index)

print(cost_table)

import matplotlib.pyplot as plt
plt.bar(cost_table.index,cost_table['Cost Percentage'])
plt.title('Percentage Costs for each process')
plt.xlabel('Process')
plt.ylabel('Percentage Cost')
