import numpy as np
from Node_Optimisation.Topsis import Topsis
from Data_Manager.SystemInfo import HospitalInfo
from web3 import Web3
import pandas as pd
from Data_Manager.Ambulance_Cost_Class import AmbulanceCost


def convert(s):
    i = int(s, 16)                   # convert from hex to a Python int
    return i

w3 = Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc'))
w3.personal.unlockAccount(w3.eth.accounts[0], '')

hospitalInfo= HospitalInfo(w3)

number= Topsis(np.array([0.5, 0.8]), ["cosy", "beautiful"], hospitalInfo, ["e1", "e2"], 1, "Oncology").fit()

patient_physician = pd.DataFrame(index=range(0,6))
patient_physician = pd.concat([patient_physician, number, ], axis=1, sort=True).fillna(0).T

print(list(patient_physician.loc[1,:]))

print(convert(w3.eth.accounts[0]))

a=AmbulanceCost([1],[1,2,3])
print(list(a.ambulance_cost.values[0]))

