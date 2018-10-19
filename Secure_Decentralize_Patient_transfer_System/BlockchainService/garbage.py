import numpy as np
from Node_Optimisation.Topsis import Topsis
from Data_Manager.SystemInfo import SystemInfo
from web3 import Web3
import pandas as pd
from Data_Manager.Ambulance_Cost_Class import AmbulanceCost
from gurobipy import *
import random


def convert(s):
    i = int(s, 16)                   # convert from hex to a Python int
    return i

'''w3 = Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc'))
w3.personal.unlockAccount(w3.eth.accounts[0], '')
'''
'''hospitalInfo= SystemInfo(w3)

number= Topsis(np.array([0.5, 0.8]), ["cosy", "beautiful"], hospitalInfo, ["e1", "e2"], 1, "Oncology").fit()

patient_physician = pd.DataFrame(index=range(0,6))
patient_physician = pd.concat([patient_physician, number, ], axis=1, sort=True).fillna(0).T

print(list(patient_physician.loc[1,:]))

print(w3.eth.accounts[0])

a=AmbulanceCost([1],[1,2,3])
print(list(a.ambulance_cost.values[0]))
'''
'''
# Create a new model
m = Model("mip1")
m.Params.Threads=4
#m.setParam(GRB.Param.Threads, 4)
# Create variables
x = m.addVar(vtype=GRB.BINARY, name="x")
y = m.addVar(vtype=GRB.BINARY, name="y")
z = m.addVar(vtype=GRB.BINARY, name="z")

# Set objective
m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

# Add constraint: x + 2 y + 3 z <= 4
m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

# Add constraint: x + y >= 1
m.addConstr(x + y >= 1, "c1")

m.optimize()

for v in m.getVars():
    print(v.varName, v.x)

print(len(w3.eth.accounts))
'''
'''a = np.random.randint(2,size=(10,))
number_even = (random.randint(0, int(5/2))) * 2

b = np.zeros(5 ,dtype=int)
print(a[0])
if a[0] == 0:
    number = (random.randint(0, int(5 / 2))) * 2 + 1
else:
    number=(random.randint(0, int(5 / 2))) * 2
print(number)
b[number]=1

print(b)'''
print(pd.DataFrame([[0,1],[2,3]]))


