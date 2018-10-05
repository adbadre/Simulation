from web3 import Web3
from Node_Optimisation.Topsis import Topsis
from Mining.Assignement import Assignment
import numpy as np
import pandas as pd
from Data_Manager.Ambulance_Cost_Class import AmbulanceCost
from Data_Manager.Severity_Of_Illness_Class import SeverityOfIllness
from Data_Manager.SystemInfo import SystemInfo
from Data_Manager.Number_Of_Patient_Per_Physician_Class import NumberOfPatientPerPhysician
from Data_Manager.Physician_Network_Class import PhysicianNetwork
from Data_Manager.Patient_Handler_Class import PatientHandler
import matplotlib.pyplot as plt


if __name__ == "__main__":
    acceptance_rate = []
    time_period = []
    for k in range(0, 1):
        time_period.append(k+1)
        hospital_info = SystemInfo(Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc')),4)
        patient = PatientHandler()
        physician = hospital_info.physician


        '''Info on Hospitals of the network'''
        hospitals=hospital_info.hospitals
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
                    hospital_info.physician_request(1), ["e1"], patient[0], "Oncology")
        p2 = Topsis(np.array([0.5, 0.8]), ["cosy", "experience"],
                    hospital_info.physician_request(1), ["e1", "e2"], patient[1], "Oncology")
        p3 = Topsis(np.array([0.2, 0.8, 0.1]), ["cosy", "experience", "remote"],
                    hospital_info.physician_request(0), ["e1", "e3", "e2"], patient[2], "Cardiology")
        p1_fit = p1.fit()
        p2_fit = p2.fit()
        p3_fit = p3.fit()
        '''Creation of weight matrix'''
        patient_physician = pd.DataFrame(index=physician)
        patient_physician = pd.concat([patient_physician, p1_fit, p2_fit, p3_fit], axis=1, sort=True).fillna(0).T
        print(patient_physician)
        '''number of patient by physician'''
        patient_by_physician = [15 for _ in physician]
        print(cost_loosing_patient)
        costs_real=[]
        for value in cost_loosing_patient[0]:
            if value < 10000000:
                costs_real.append(value)
                break
        for value in cost_loosing_patient[1]:
            if value < 10000000:
                costs_real.append(value)
                break
        cost_loosing_patient = pd.DataFrame([np.array(costs_real)], index=["cost"],
                                            columns=cost_loosing_patient.columns).T
        print(cost_loosing_patient)
        number1=0
        number0=0
        for p in patient:
            i = 0
            for v in patient_physician.loc[p,:]:
                if v == 1:
                    if i in hospital_info.physician_request(1):
                        number1 += 1
                    else:
                        number0 += 1
                    break
                i += 1

        patient_service=pd.DataFrame([np.array([number0,number1])],index=["total"],columns=cost_loosing_patient.T.columns).T
        #Physician service
        physician_service0=[]
        physician_service1 = []
        for p in physician:
            if p in hospital_info.physician_request(1):
                physician_service1.append(p)
            else:
                physician_service0.append(p)

        physician_service=[physician_service0,physician_service1]

        a = Assignment(patient, physician, patient_physician,
                       hospitals, hospitals_service, ambulance_cost.ambulance_cost,
                       cost_loosing_patient,
                       bed_hospital, patient_by_physician,
                       hospital_info.physician_hospital_service,patient_service,physician_service)
        a.fit(0.5)


