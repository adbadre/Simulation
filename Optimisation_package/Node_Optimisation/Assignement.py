from gurobipy import *

from Node_Optimisation.Topsis import Topsis
import numpy as np
import pandas as pd


class Assignment:

    def __init__(self, patient, physician, physician_matched_patient, hospitals, service,
                 costs_ambulance, severity_of_illness,
                 costs_of_loosing_patient, bed_hospital, patient_by_physician):
        self.patient = patient
        self.physician = physician
        self.physician_patient = physician_matched_patient  # Matrix
        self.hospitals = hospitals
        self.service = service
        self.costs_ambulance = costs_ambulance  # Matrix
        self.severity_of_illness = severity_of_illness  # Vector patient
        self.costs_of_loosing_patient = costs_of_loosing_patient  # matrix hospital/service
        self.bed_hospital = bed_hospital  # matrix
        self.patient_by_physician = patient_by_physician  # vector physician and number
        self.model = Model("Patient Assignment")
        self.X = {}

    # Variable definition
    def set_variable(self):
        for i in self.patient:
            for j in self.physician:
                for h in self.hospitals:
                    self.X[i, j, h] = self.model.addVar(lb=0, ub=1, vtype=GRB.BINARY,
                                                        name="patient " + i + " with physician " + j + " at hospital "
                                                             + h +
                                                             " attribution " + str(self.physician_patient.loc[i, j]))

    # Objective function definition
    def set_objective_function(self, w1, w2):
        self.model.setObjective(

            w1 * quicksum(self.X[i, j, h] * self.costs_ambulance.loc[i, j]
                          for i in self.patient
                          for j in self.physician
                          for h in self.hospitals)

            + w2 * quicksum((1 - self.X[i, j, h]) * self.costs_of_loosing_patient.loc[h, s]
                            for h in self.hospitals
                            for s in self.service
                            for i in self.patient
                            for j in self.physician))

    # Constraint definitions
    def set_constraints(self):
        self.model.addConstrs(((quicksum(self.X[i, j, h]
                                         for i in self.patient
                                         for j in self.physician
                                         )
                                <= self.bed_hospital[h])
                               for h in self.hospitals),
                              "Bed Constraint")

        self.model.addConstrs(((quicksum(self.X[i, j, h]
                                         for h in self.hospitals
                                         for j in self.physician
                                         )
                                == 1)
                               for i in self.patient),
                              "Patient Must Be Assign Constraint")

        self.model.addConstrs(((quicksum(self.X[i, j, h] * self.physician_patient.loc[i, j]
                                         for h in self.hospitals
                                         for j in self.physician
                                         )
                                == 1)
                               for i in self.patient),
                              "Patient Must Be Assign Constraint")

        self.model.addConstrs(((quicksum(self.X[i, j, h]
                                         for i in self.patient
                                         )
                                <= self.patient_by_physician[j])
                               for j in self.physician
                               for h in self.hospitals),
                              "Physician have a max number of  patient possible Constraint")

    # Solution displaying
    def display_sol(self):
        for v in self.model.getVars():
            if v.x == 1:
                print(v.varName, v.x)

# test main
if __name__ == "__main__":
    patient = ["Jack", "Franck", "Henry"]
    physician = ["DR henry", "DR Jack", "DR boo", "Dr lolo", "Dr booh", "Dr Libman", "Dr Niptuk"]
    hospitals = ['Chicago', 'Milwaukee', 'Springfield']
    services = ["cardiology", "bones", "neurology", "reflexology"]

    '''Severity of illness'''
    illness_severity = pd.DataFrame(np.random.randint(1, 5, size=(1, len(patient))),
                                    index=['severity'], columns=patient)
    print(illness_severity)

    '''Service in Hospitals'''
    hospitals_service = pd.DataFrame(np.random.randint(0, 2, size=(len(hospitals), len(services))),
                                     index=hospitals, columns=services)

    '''ambulance cost between network hospitals'''
    ambulance_cost = pd.DataFrame(np.random.randint(100, 2000000, size=(len(patient), len(physician))) / 100,
                                  index=patient, columns=physician)
    print(ambulance_cost)
    '''Topsis for each patient with physician with specialty. 0 for the others'''
    p1 = Topsis(np.array([0.5, 0.8]), ["cosy", "beautiful"],
                [physician[0], physician[1], physician[2]], ["e1"])
    p2 = Topsis(np.array([0.5, 0.8]), ["cosy", "experience"],
                [physician[4], physician[2], physician[1], physician[6]], ["e1", 'e2'])
    p3 = Topsis(np.array([0.2, 0.8, 0.1]), ["cosy", "experience", "remote"],
                [physician[0], physician[1], physician[2], physician[5]], ["e1", 'e2'])
    p1_fit = pd.DataFrame(p1.fit(), columns=[patient[0]])
    mask = p1_fit.loc[:, patient[0]] > 0.5
    p1_fit.loc[mask, patient[0]] = 1
    p2_fit = pd.DataFrame(p2.fit(), columns=[patient[1]])
    mask = p2_fit.loc[:, patient[1]] > 0.5
    p2_fit.loc[mask, patient[1]] = 1
    p3_fit = pd.DataFrame(p3.fit(), columns=[patient[2]])
    mask = p3_fit.loc[:, patient[2]] > 0.5
    p3_fit.loc[mask, patient[2]] = 1
    '''Creation of weight matrix'''
    patient_physician = pd.DataFrame(index=physician)
    patient_physician = pd.concat([patient_physician, p1_fit, p2_fit, p3_fit], axis=1, sort=True).fillna(0).T
    print(patient_physician)
    ''' cost of loosing a patient'''
    cost_loosing_patient = pd.DataFrame(np.random.randint(200, 1000, size=(len(hospitals), len(services))),
                                        index=hospitals, columns=services)
    for i in hospitals:
        for j in services:
            if hospitals_service.loc[i, j] == 0:
                cost_loosing_patient.loc[i, j] = 500000
    print(cost_loosing_patient)

    '''bed per hospital'''
    bed_hospital = pd.DataFrame(np.random.randint(0, 1000, size=(1, len(hospitals))),
                                columns=hospitals)
    print(bed_hospital)
    '''number of patient by physician'''
    patient_by_physician = pd.DataFrame(np.random.randint(0, 10, size=(1, len(physician))),
                                        columns=physician)
    print(patient_by_physician)

    a = Assignment(patient, physician, patient_physician,
                   hospitals, hospitals_service, ambulance_cost,
                   illness_severity, cost_loosing_patient,
                   bed_hospital, patient_by_physician
                   )
    a.set_variable()
    a.set_objective_function(0.3, 0.3)
    a.set_constraints()
    a.model.optimize()
    a.display_sol()
