from Node_Optimisation.Topsis import Topsis
from Node_Optimisation.Assignement import Assignment
import numpy as np
import pandas as pd
from Data_Manager.Ambulance_Cost_Class import AmbulanceCost
from Data_Manager.Severity_Of_Illness_Class import SeverityOfIllness
from Data_Manager.Hospital_Info_Class import HospitalInfo
from Data_Manager.Number_Of_Patient_Per_Physician_Class import NumberOfPatientPerPhysician
from Data_Manager.Physician_Network_Class import PhysicianNetwork
from Data_Manager.Patient_Handler_Class import PatientHandler


class Consensus:

    def __init__(self, local_solutions, enforced_constraints, general_solution, sigma, number_of_hospitals):
        self.number_of_hospitals = number_of_hospitals
        self.local_solutions = local_solutions
        self.enforced_constraints = enforced_constraints
        self.general_solution = general_solution
        self.lagrange_multiplier_vector = np.zeros(local_solutions.shape)
        self.k = 0
        self.sigma = sigma
        self.epsilon1 = 0
        self.epsilon2 = 0

    def estimate_global_variable(self):
        old_general_solution = self.general_solution
        self.general_solution = np.dot(np.dot(np.invert(np.dot(self.enforced_constraints.T, self.enforced_constraints)),
                                              self.enforced_constraints.T),
                                       (self.local_solutions + self.lagrange_multiplier_vector / self.sigma)
                                       )
        print(self.enforced_constraints, self.general_solution, old_general_solution)
        self.epsilon2 = np.linalg.norm(self.sigma * np.dot(self.enforced_constraints,
                                                           (self.general_solution - old_general_solution)
                                                           )
                                       )

    def dual_update(self):
        self.lagrange_multiplier_vector = self.lagrange_multiplier_vector \
                                          + self.sigma * (self.local_solutions -
                                                          np.dot(self.enforced_constraints , self.general_solution))

    def fit(self):
        stop = False
        while not stop:
            for hospital in range(0, self.number_of_hospitals):
                self.local_solutions[hospital] = self.local_solutions[hospital, :] ## LOOOOOOOOOOOLLLLLLLL

            self.estimate_global_variable()
            self.dual_update()
            self.epsilon1 = np.linalg.norm(self.local_solutions - np.dot(self.enforced_constraints,
                                                                         self.general_solution)
                                           )
            if self.epsilon1 < 2000000 and self.epsilon2 < 2000000:
                print(self.epsilon1, self.epsilon2)
                stop = True
                print(self.k)
            else:
                self.k = self.k + 1


if __name__ == "__main__":
    patient = PatientHandler()
    physician = PhysicianNetwork()

    '''Severity of illness'''
    illness_severity = SeverityOfIllness(patient)
    print(illness_severity.illness_severity)

    '''Info on Hospitals of the network'''
    hospital_info = HospitalInfo()
    hospitals = hospital_info.hospitals
    # services in hospitals
    hospitals_service = hospital_info.hospitals_service
    # cost of loosing a patient
    cost_loosing_patient = hospital_info.cost_loosing_patient
    # bed per hospital
    bed_hospital = hospital_info.bed_hospital
    print(bed_hospital)
    '''ambulance cost between network hospitals'''
    ambulance_cost = AmbulanceCost(patient, hospital_info.hospitals)
    print(ambulance_cost)
    '''Topsis for each patient with physician with specialty. 0 for the others'''

    p1 = Topsis(np.array([0.5, 0.8]), ["cosy", "beautiful"],
                hospital_info, ["e1"], patient[0], "Oncology")
    p2 = Topsis(np.array([0.5, 0.8]), ["cosy", "experience"],
                hospital_info, ["e1", "e2"], patient[1], "Oncology")
    p3 = Topsis(np.array([0.2, 0.8, 0.1]), ["cosy", "experience", "remote"],
                hospital_info, ["e1", "e3", "e2"], patient[2], "Cardiology")
    p1_fit = p1.fit()
    p2_fit = p2.fit()
    p3_fit = p3.fit()
    '''Creation of weight matrix'''
    patient_physician = pd.DataFrame(index=physician)
    patient_physician = pd.concat([patient_physician, p1_fit, p2_fit, p3_fit], axis=1, sort=True).fillna(0).T

    '''number of patient by physician'''
    patient_by_physician = NumberOfPatientPerPhysician()
    print(patient_by_physician)

    ''' Generating random assignment for test'''
    a = Assignment(patient, physician, patient_physician,
                   hospitals, hospitals_service, ambulance_cost.ambulance_cost,
                   illness_severity, cost_loosing_patient,
                   bed_hospital, patient_by_physician,
                   hospital_info.physician_hospital_service)
    a.fit(0.3)
    sola =[]
    for v in a.model.getVars():
        sola.append(v.x)
    consta = a.model.getConstrs()
    b = Assignment(patient, physician, patient_physician,
                   hospitals, hospitals_service, ambulance_cost.ambulance_cost,
                   illness_severity, cost_loosing_patient,
                   bed_hospital, patient_by_physician,
                   hospital_info.physician_hospital_service)
    b.fit(0.7)
    solb = []
    for v in b.model.getVars():
        solb.append(v.x)
    constb = b.model.getConstrs()
    sol = [sola, solb]
    enforced_constraints = np.full((len(sol), len(sol)), 1)
    general_sol = sol
    consensus = Consensus(np.array(sol), enforced_constraints, np.array(general_sol), 6, 2)
    consensus.fit()
    #### Next update : adding the quadratic contraint in the assignement class to make the solution move. The smart contracts are going to bring all the data.