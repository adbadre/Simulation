from Simulation_Package.BlockChainGenesis import BlockchainGenesis
from web3 import Web3
from Data_Manager.SystemInfo import SystemInfo
from BlockchainService.TransfertBlock import TransfertBlock
from BlockchainService.ContractFactory import ContractFactory
from pandas import IndexSlice
from Mining.Assignement import Assignment
import time
import numpy as np
from Node_Optimisation.Topsis import Topsis
import pandas as pd
from Data_Manager.Ambulance_Cost_Class import AmbulanceCost
import random
import matplotlib.pyplot as plt



class Simulation:

    def __init__(self, time_span, number_of_hospital, max_number_of_patient_per_hospital):
        self.w3 = Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc'))
        self.genesis = None
        self.LatestBlock = None
        self.PhysicianHospitalService = None
        self.TransferBLockABI = None
        self.SystemInfo = SystemInfo(self.w3, number_of_hospital)
        self.acceptance_rate_values = []
        self.time_span = [x+1 for x in range(0, time_span)]
        self.number_of_hospital = number_of_hospital
        self.max_number_of_patient_per_hospital = max_number_of_patient_per_hospital

    def init_simulation(self):
        self.w3.personal.unlockAccount(self.w3.eth.accounts[0], '')
        self.genesis = BlockchainGenesis().genesis(self.w3, self.SystemInfo)
        self.LatestBlock = self.genesis['latest_block']
        self.PhysicianHospitalService = self.genesis['physician_hospital_service']
        print("Simulation Initiated")

    def hospital_agent(self, number_of_patient, hospital_number):
        '''Topsis for each patient with physician with specialty. 0 for the others'''
        transfer_block_info = [self.LatestBlock.get_potential_block_address(), self.TransferBLockABI]
        transfer_block = TransfertBlock(self.w3, transfer_block_info, self.SystemInfo.hospitals)
        # Add Patient
        patients = []
        hospitals = self.PhysicianHospitalService.get_hospital()
        hospitals = [str(x) for x in hospitals]
        physicians = self.PhysicianHospitalService.get_physicians_tab()
        service_requested = self.SystemInfo.hospitals_service.loc[self.w3.eth.accounts[hospital_number], 0]
        service = 0
        self.w3.personal.unlockAccount(self.w3.eth.accounts[0], '')
        if service_requested == 0:
            service = 1
        transfer_block.add_service_count(service, number_of_patient)
        for i in range(0, number_of_patient):
            patient_id = int(str(hospital_number)+"0000"+str(i))
            # Patient Id
            transfer_block.add_patient(patient_id)
            patients.append(patient_id)
            # Matching

            physician_eligibles = self.PhysicianHospitalService.get_physician_service_hospital_by_service(service)
            matching = Topsis(np.array([0.5, 0.8]), ["cosy", "beautiful"], physician_eligibles, ["e1", "e2", "e3"],
                              patient_id, str(service)).fit()
            patient_physician = pd.DataFrame(index=physicians)
            patient_physician = pd.concat([patient_physician, matching], axis=1, sort=True).fillna(0).T
            transfer_block.set_patient_matched_physician(patient_id,
                                                         [int(x) for x in list(patient_physician.loc[patient_id, :])])
            # Severity of illness
            transfer_block.set_severity_of_illness_by_id(patient_id, 20)
            # Ambulance cost
            ambulance_info = AmbulanceCost([patient_id], hospitals).ambulance_cost.values[0]
            ambulance_info = [int(x) for x in list(ambulance_info)]
            transfer_block.set_ambulance_cost(patient_id, ambulance_info)

        services = self.PhysicianHospitalService.get_hospital_service(self.w3.eth.accounts[hospital_number])
        self.PhysicianHospitalService.set_number_of_bed_per_hospital(self.w3.eth.accounts[hospital_number],50)
        for service_id in services:
            transfer_block.set_cost_of_loosing_patient_by_id(self.w3.eth.accounts[hospital_number],
                                                             service_id,  500)
        transfer_block.add_hospital(self.w3.eth.accounts[hospital_number])
        print("Hospital Agent "+str(hospital_number) +" done")

    def miner_agent(self):
        print("Mining Initiated")
        transfer_block_info = [self.LatestBlock.get_potential_block_address(), self.TransferBLockABI]
        transfer_block = TransfertBlock(self.w3, transfer_block_info, self.SystemInfo.hospitals)
        patients = transfer_block.get_patients()
        physicians = self.PhysicianHospitalService.get_physicians_tab()
        hospitals = transfer_block.get_hospitals()

        # services in hospitals
        hospital_service = []
        for hospital in hospitals:
            hospital_service.append(self.PhysicianHospitalService.get_hospital_service(hospital))
        hospital_service_df = pd.DataFrame(data=hospital_service,
                                           index=hospitals, columns=range(len(hospital_service[0])))

        # Physician in services
        hospital_service_physician = []
        i = 0
        for hospital in hospitals:
            for service in range(len(hospital_service[i])):
                hospital_service_physician.append(self
                                                  .PhysicianHospitalService
                                                  .get_physician_service_hospital_by_hospital(hospital,
                                                                                              service))
            i += 1
        hos = []
        serv = []
        i = 0
        for _ in hospitals:
            for service in range(len(hospital_service[0])):
                hos.append(i)
                serv.append(service)
            i = i+1
        hospital_service_physician = pd.DataFrame(hospital_service_physician,
                                                   index=pd.MultiIndex(
                                                       levels=[hospitals, range(len(hospital_service[0]))],
                                                       labels=[hos, serv]
                                                       ),
                                                   columns = physicians)

        # Cost of loosing a patient
        cost_loosing_patient = []
        i = 0
        for hospital in hospitals:
            s=[]
            for service in range(len(hospital_service[0])):
                s.append(transfer_block.get_cost_of_loosing_patient_by_id(hospital, service))
            cost_loosing_patient.append(s)
            i = i+1
        cost_loosing_patient = pd.DataFrame(cost_loosing_patient,
                                            index=hospitals,
                                            columns=range(len(hospital_service_df.columns)))

        # Bed per hospital
        bed_hospital = []
        for hospital in hospitals:
            bed_hospital.append(self.PhysicianHospitalService.get_number_of_bed_per_hospital(hospital))
        bed_hospital = pd.DataFrame(bed_hospital, index=hospitals).T

        # Ambulance cost between network hospitals
        ambulance_cost = []
        for patient in patients:
            ambulance_cost.append(transfer_block.get_ambulance_cost_by_id(patient))
        ambulance_cost = pd.DataFrame(ambulance_cost, index=patients, columns=hospitals)

        # Topsis result for each patient with physician with specialty =>1. 0 for the others
        patient_matched_physician = []
        for patient in patients:
            patient_matched_physician.append(pd.DataFrame(transfer_block.
                                                          get_number_of_patient_matched_physician_by_id(patient),
                                                          index=physicians, columns=[patient]).T)
        patient_matched_physician = pd.concat(patient_matched_physician, axis=0, sort=True)

        # Number of patient by physician
        patient_by_physician = []
        for i in physicians:
            patient_by_physician.append(self.PhysicianHospitalService.get_number_of_patient_per_physician_by_id(i))
        patient_by_physician = pd.DataFrame(patient_by_physician, index=physicians).T

        costs_real = []
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
        patient_service = transfer_block.get_service_count()

        patient_service = pd.DataFrame(np.array([patient_service]), index=["total"],
                                       columns=cost_loosing_patient.T.columns).T
        print(patient_service)
        # Physician service
        physician_service0 = []
        physician_service1 = []
        for p in physicians:
            if p in self.PhysicianHospitalService.get_physician_service_hospital_by_service(1):
                physician_service1.append(p)
            else:
                physician_service0.append(p)

        physician_service = [physician_service0, physician_service1]
        print(physician_service)
        self.w3.personal.unlockAccount(self.w3.eth.accounts[0], '')
        self.w3.miner.stop()
        a = Assignment(patients, physicians, patient_matched_physician,
                       hospitals, range(len(hospital_service[0])), ambulance_cost,
                       cost_loosing_patient,
                       bed_hospital, patient_by_physician,
                       hospital_service_physician,patient_service,physician_service)

        a.fit(0.5)

        print("Mining Over")

        self.w3.miner.start(8)

    def run_assignment_rate(self):
        self.init_simulation()

        for times in self.time_span:
            print("Time:"+str(times))
            CurrentTransferBLock = TransfertBlock(self.w3, self.SystemInfo.hospitals)
            self.LatestBlock.set_potential_block_address(CurrentTransferBLock.contract_info[0])
            self.TransferBLockABI = CurrentTransferBLock.contract_info[1]
            for hospital_number in range(0, self.number_of_hospital):
                random.seed(8750)
                self.hospital_agent(random.randint(1, self.max_number_of_patient_per_hospital), hospital_number)
            self.miner_agent()
            self.w3.personal.unlockAccount(self.w3.eth.accounts[0], '')
            CurrentTransferBLock.set_previous_block(self.LatestBlock.get_potential_block_address())

    def run_computation_power(self):
        self.init_simulation()
        CurrentTransferBLock = TransfertBlock(self.w3, self.SystemInfo.hospitals)
        self.LatestBlock.set_potential_block_address(CurrentTransferBLock.contract_info[0])
        self.TransferBLockABI = CurrentTransferBLock.contract_info[1]
        for hospital_number in range(0, self.number_of_hospital):
            random.seed(8750)
            self.hospital_agent(random.randint(1, self.max_number_of_patient_per_hospital), hospital_number)
        self.miner_agent()

    def plot_assignment_rate(self):
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(self.time_span, self.acceptance_rate_values, color="red")
        plt.show()

    def plot_computational_time(self):
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(self.time_span, self.acceptance_rate_values, color="red")
        plt.show()



if __name__ == "__main__":
    s = Simulation(1, 9, 20)
    s.run_assignment_rate()
    s.plot_assignment_rate()
