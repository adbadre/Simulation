from Simulation.BlockChainGenesis import BlockchainGenesis
from web3 import Web3
from Data_Manager.SystemInfo import HospitalInfo
from BlockchainService.TransfertBlock import TransfertBlock
from BlockchainService.ContractFactory import ContractFactory
from pandas import IndexSlice
import time
import numpy as np
from Node_Optimisation.Topsis import Topsis
import pandas as pd
from Data_Manager.Ambulance_Cost_Class import AmbulanceCost



class Simulation:

    def __init__(self):
        self.w3 = Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc'))
        self.genesis = None
        self.LatestBlock = None
        self.PhysicianHospitalService = None
        self.SystemInfo = HospitalInfo(self.w3)

    def init_simulation(self, system_info):
        self.w3.personal.unlockAccount(self.w3.eth.accounts[0], '')
        self.genesis = BlockchainGenesis().genesis(self.w3, self.SystemInfo)
        self.LatestBlock = self.genesis['latest_block']
        self.PhysicianHospitalService = self.genesis['physician_hospital_service']
        print("Simulation Initiated")

    def hospital_agent(self, transfer_block, number_of_patient, hospital_number):
        '''Topsis for each patient with physician with specialty. 0 for the others'''
        # Add Patient
        patients = []
        hospitals = self.PhysicianHospitalService.get_hospital()
        print(hospitals)
        for i in range(0, number_of_patient):
            patient_id = int(str(hospital_number)+"0000"+str(i))
            # Patient Id
            transfer_block.add_patient(patient_id)
            patients.append(patient_id)
            # Matching
            physician_eligibles = self.PhysicianHospitalService.get_physician_service_hospital_by_service(1)
            matching = Topsis(np.array([0.5, 0.8]), ["cosy", "beautiful"], physician_eligibles, ["e1"], i, "Oncology").fit()
            patient_physician = pd.DataFrame(index=range(0, 6))
            patient_physician = pd.concat([patient_physician, matching], axis=1, sort=True).fillna(0).T
            transfer_block.set_patient_matched_physician(patient_id, [int(x) for x in list(patient_physician.loc[i, :])])
            # Severity of illness
            transfer_block.set_severity_of_illness_by_id(patient_id, 20)
            '''
            # Ambulance cost
            ambulance_info = AmbulanceCost([patient_id], hospitals).ambulance_cost.values[0]
            ambulance_info = [int(x) for x in list(ambulance_info)]
            transfer_block.set_ambulance_cost(patient_id, ambulance_info)
            print("patient "+str(i))

        services = self.PhysicianHospitalService.get_hospital(self.w3.eth.accounts[hospital_number])
        self.PhysicianHospitalService.set_number_of_bed_per_hospital(self.w3.eth.accounts[hospital_number],50)
        for service_id in services:
            transfer_block.set_cost_of_loosing_patient_by_id(self, self.w3.eth.accounts[hospital_number],
                                                             service_id,  2000)
        '''
        transfer_block.add_hospital(self.w3.eth.accounts[hospital_number])
        time.sleep(10)
        print("Hospital Agent"+str(hospital_number) +" done")
    def miner_agent(self, transfer_block):
        patients = transfer_block.get_patients()
        print(patients)
        physicians = self.PhysicianHospitalService.get_physicians_tab()
        print(physicians)
        hospitals = transfer_block.get_hospitals()
        print(hospitals)
        '''Severity of illness'''
        illness_severity = []
        for id in patients:
            illness_severity.append(transfer_block.get_severity_of_illness_by_id(id))
        print(illness_severity)

        # services in hospitals
        hospital_service = []
        for hospital in hospitals:
            hospital_service.append(self.PhysicianHospitalService.get_hospital_service(hospital))
        print(hospital_service)
        hospital_service_physician = []
        i=0
        for hospital in hospitals:
            for service in range(len(hospital_service[i])):
                hospital_service_physician.append(self
                                                  .PhysicianHospitalService
                                                  .get_physician_service_hospital_by_hospital(hospital,
                                                                                              service))
        print(hospital_service_physician)
        '''
        # cost of loosing a patient
        cost_loosing_patient = []
        i = 0
        for hospital in hospitals:#### ACHTTTTTTTTTTTTTTTTTUUUUUUUNNGGGGG
            for service in range(len(hospital_service[i])):
                cost_loosing_patient.append(transfer_block.get_cost_of_loosing_patient_by_id(hospital, service))
            i=i+1
        print(cost_loosing_patient)
        # bed per hospital
        bed_hospital = []
        for hospital in hospitals:
            bed_hospital.append(self.PhysicianHospitalService.get_number_of_bed_hospital(hospital))
        print(bed_hospital)
        #ambulance cost between network hospitals
        ambulance_cost = []
        for patient in patients:
            ambulance_cost.append(transfer_block.get_ambulance_cost_by_id(patient))
        print(ambulance_cost)
        print(ambulance_cost)
        '''
        '''Topsis result for each patient with physician with specialty =>1. 0 for the others'''
        patient_matched_physician = []
        for patient in patients:
            patient_matched_physician.append(transfer_block.get_number_of_patient_matched_physician_by_id(patient))
        print(patient_matched_physician)

        '''number of patient by physician'''
        patient_by_physician = []
        for i in physicians:
            patient_by_physician.append(self.PhysicianHospitalService.get_number_of_patient_per_physician_by_id(i))
        print(patient_by_physician)


        '''Creation of weight matrix'''
        '''patient_physician = pd.DataFrame(index=physicians)

        patient_physician = pd.concat([patient_physician, p1_fit, p2_fit, p3_fit], axis=1, sort=True).fillna(0).T

        # solve problem
        a = Assignment(patients, physicians, patient_physician,
                       hospitals, hospitals_service, ambulance_cost,
                       illness_severity, cost_loosing_patient,
                       bed_hospital, patient_by_physician,
                       hospital_service_physician)
        a.fit(0.3)
        '''

    def run(self):
        transfert_block = TransfertBlock(self.w3)
        self.hospital_agent(transfert_block, 10, 1)

    def Simu(self):
        h = HospitalInfo(self.w3)
        self.init_simulation(h)
        t = TransfertBlock(self.w3)
        print(t.get_hospitals())
        self.hospital_agent(t, 10, 1)
        time.sleep(30)
        self.miner_agent(t)

if __name__ == "__main__":
    simu1= Simulation()
    simu1.Simu()
