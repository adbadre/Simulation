from gurobipy import *


class Assignment:

    def __init__(self, patient, physician, physician_matched_patient, hospitals, service,
                 costs_ambulance, severity_of_illness,
                 costs_of_loosing_patient, bed_hospital, patient_by_physician,physician_hospital):
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
        self.physician_hospital = physician_hospital
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
    def set_objective_function(self, w1): #, sigma, F, Z, Y):
        self.model.setObjective(

            w1 * quicksum(self.X[i, j, h] * self.costs_ambulance.loc[i, h]
                          for i in self.patient
                          for j in self.physician
                          for h in self.hospitals)

            + (1 - w1) * quicksum((1 - self.X[i, j, h]) * self.costs_of_loosing_patient.loc[h, s]
                                  for h in self.hospitals
                                  for s in self.service
                                  for i in self.patient
                                  for j in self.physician)
            # + (sigma/2)*(np.linalg.norm(self.X-np.dot(F, Z)+Y/sigma)) ^ 2
        )

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

        self.model.addConstrs(((quicksum(self.X[i, j, h]
                                         * self.physician_patient.loc[i, j]
                                         * self.physician_hospital.xs((h, s)).loc[j]
                                         for h in self.hospitals
                                         for s in self.service
                                         for j in self.physician
                                         )
                                == 1)
                               for i in self.patient),
                              "Patient Must Be Assign Constraint with the right Physician at the right place")

        self.model.addConstrs(((quicksum(self.X[i, j, h] * self.physician_patient.loc[i, j]
                                         for h in self.hospitals
                                         for j in self.physician
                                         )
                                == 1)
                               for i in self.patient),
                              "Physician Location Constraint")

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

    def fit(self, w1):
        self.set_variable()
        self.set_objective_function(w1)
        self.set_constraints()
        self.model.optimize()
        self.display_sol()


