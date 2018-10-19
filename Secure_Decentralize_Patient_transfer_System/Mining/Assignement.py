from gurobipy import *
import random

class Assignment:

    def __init__(self, patient, physician, physician_matched_patient, hospitals, service,
                 costs_ambulance, costs_of_loosing_patient, bed_hospital, patient_by_physician,
                 physician_hospital, patient_service, physician_service, *args):
        self.patient = patient
        self.physician = physician
        self.physician_patient = physician_matched_patient  # Matrix
        self.hospitals = hospitals
        self.service = service
        self.costs_ambulance = costs_ambulance  # Matrix
        self.costs_of_loosing_patient = costs_of_loosing_patient  # matrix hospital/service
        self.bed_hospital = bed_hospital  # matrix
        self.patient_by_physician = patient_by_physician  # vector physician and number
        self.physician_hospital = physician_hospital
        self.model = Model("Patient Assignment")
        self.time = False
        if len(args) == 0:
            self.model.setParam(GRB.Param.Threads, 8)
        else:
            self.model.setParam(GRB.Param.Threads, args[0])
            self.time = True
        self.patient_service = patient_service
        self.physician_service = physician_service
        self.X = {}

    # Variable definition
    def set_variable(self):
        for i in self.patient:
            for j in self.physician:
                for h in self.hospitals:
                    self.X[i, j, h] = self.model.addVar(lb=0, ub=1, vtype=GRB.BINARY,
                                                        name="patient " + str(i) + " with physician " + str(j)
                                                             + " at hospital " + str(h) +
                                                             " attribution " + str(self.physician_patient.loc[i, j]))

    # Objective function definition
    def set_objective_function(self, w1):  # , sigma, F, Z, Y):
        self.model.setObjective(

            w1 * quicksum(self.X[i, j, h] * self.costs_ambulance.loc[i, h]
                          for i in self.patient
                          for j in self.physician
                          for h in self.hospitals)
            + (1 - w1) * quicksum((self.patient_service.loc[s, 'total'] - quicksum(self.X[i, j, h]
                                                                                   for i in self.patient
                                                                                   for j in self.physician_service[s]
                                                                                   for h in self.hospitals)
                                   )
                                  *
                                  self.costs_of_loosing_patient.loc[s, "cost"]
                                  for s in self.service
                                  )
        )

    ''''+ (1 - w1) * (quicksum(( 1-self.X[i, j, h]) * self.costs_of_loosing_patient.loc[h, s]
                                     for h in self.hospitals
                                     for s in self.service
                                     for i in self.patient
                                     for j in self.physician_patient.loc[i, :]))

               # + (sigma/2)*(np.linalg.norm(self.X-np.dot(F, Z)+Y/sigma)) ^ 2'''

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
                                <= 1)
                               for i in self.patient),
                              "Patient Can Be Assign Constraint")

        self.model.addConstrs(((self.X[i, j, h]
                                ==
                                self.X[i, j, h]
                                * self.physician_patient.loc[i, j]
                                ) for i in self.patient
                               for h in self.hospitals
                               for j in self.physician),
                              "If Assigned , then have to be assigned with the good physician")

        self.model.addConstrs(((self.X[i, j, h]
                                ==
                                quicksum(self.X[i, j, h]
                                         * self.physician_patient.loc[i, j]
                                         * self.physician_hospital.xs((h, s)).loc[j]
                                         for s in self.service
                                         )
                                ) for i in self.patient
                               for h in self.hospitals
                               for j in self.physician),
                              "If Assigned , then the physician must in the good hospital ")

        self.model.addConstrs(((quicksum(self.X[i, j, h]
                                         for i in self.patient
                                         )
                                <= self.patient_by_physician[j])
                               for j in self.physician
                               for h in self.hospitals),
                              "Physician have a max number of  patient possible Constraint")

    # Solution displaying
    def display_sol(self):
        yes = 0
        try:
            for v in self.model.getVars():
                if v.x == 1:
                    assigned = True
                    physician_acceptance = random.random()
                    if physician_acceptance < 0.05:
                        assigned = False
                    if assigned:
                        yes += 1
                        print(v.varName)
                    else:
                        print(v.varName, "Rejected!!")
            print("Assigned:"+str(yes))
            assignment = yes/float(len(self.patient))
            print("Rate:"+str(yes/float(len(self.patient))))
        except Exception:
            assignment = 0
            print("No Solution")
        return assignment

    def fit(self, w1):
        self.set_variable()
        self.set_objective_function(w1)
        self.set_constraints()
        self.model.optimize()
        if not self.time:
            return self.display_sol()
        else:
            return self.model.Runtime
