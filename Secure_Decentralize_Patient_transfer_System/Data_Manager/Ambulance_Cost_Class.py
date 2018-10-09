import pandas as pd
import numpy as np
from Data_Manager.SystemInfo import SystemInfo
from web3 import Web3


class AmbulanceCost:

    def __init__(self, patient, hospital, specialty, severity_of_illness, miles_distance):
        self.ambulance_cost = None
        self.patient = patient
        self.hospital = hospital
        self.miles_distance = pd.DataFrame(miles_distance.values, index=hospital, columns=[patient]).T
        self.mileage_rate = 40

        self.specialty = specialty
        self.severity_of_illness = severity_of_illness
        self.RVU = pd.DataFrame(np.array([1.0, 1.6, 1.2, 1.9, 2.75, 3.25]), index=range(1, 7), columns=["RVU"])
        self.GPCI = 0.9683169
        self.CF = 220.74
        self.set_cost()

    def set_cost(self):
        costs = []
        for patient in self.miles_distance.index:
            distances = self.miles_distance.loc[patient, :]
            patient_costs = []
            for distance in distances:
                cost = self.RVU.loc[self.severity_of_illness, "RVU"]*self.CF*self.GPCI\
                       + distance*40
                patient_costs.append(cost)
            costs.append(patient_costs)
        self.ambulance_cost = pd.DataFrame(costs, index=[self.patient], columns=self.hospital).values[0]

    def __getitem__(self, item):
        return self.ambulance_cost[item]

    def __len__(self):
        return len(self.ambulance_cost)


