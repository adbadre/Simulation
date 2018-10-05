from web3 import Web3
from BlockchainService.LatestBlock import LatestBlock
from BlockchainService.PhysicianHospitalSpecialty import PhysicianHospitalService
from BlockchainService.TransfertBlock import TransfertBlock
from Data_Manager.SystemInfo import SystemInfo
from Data_Manager.Ambulance_Cost_Class import AmbulanceCost
from pandas import IndexSlice
import time
import numpy as np
from Node_Optimisation.Topsis import Topsis
import pandas as pd
from BlockchainService.ContractFactory import ContractFactory


if __name__ == "__main__":
    w3 = Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc'))
    w3.personal.unlockAccount(w3.eth.accounts[0], '')
    '''
    # Latest Block Contract Test
    test = LatestBlock.get_instance(w3)
    test.set_new_latest_block(w3.eth.accounts[0])
    print(test.get_new_address())
   '''
    # Physician Hospital Service Test
    hospitalInfo = SystemInfo(w3, 5)
    '''test2 = PhysicianHospitalService.get_instance(w3,hospitalInfo.hospitals)
    physician_tab = []

    # Set physician
    i = 0
    for physician in hospitalInfo.physician:
        physician_tab.append(i)
        test2.set_number_of_patient_per_physician(i, 15)
        i += 1
    test2.set_physicians_tab(physician_tab)

    # set the matrix hospital service physician
    idx = IndexSlice

    for hospital in hospitalInfo.hospitals:
        test2.set_hospital_service(hospital, list(hospitalInfo.hospitals_service.loc[hospital, :]))
        for service in hospitalInfo.services:
            print(list(hospitalInfo.physician_hospital_service.loc[idx[hospital, service], :]))
            test2.set_hospital_service_physician(list(hospitalInfo.physician_hospital_service
                                                      .loc[idx[hospital, service], :]),
                                                 hospital,
                                                 service)
    
    print("Set")
    time.sleep(20)
    print(test2.get_physician_service_hospital_by_service(0))
    print(test2.get_physician_service_hospital_by_service(1))
    '''
    '''
    for hospital in hospitalInfo.hospitals:
        j = 0
        for service in hospitalInfo.services:
            print(test2.get_physician_service_hospital_by_hospital(hospital, j))
            j += 1
    
    time.sleep(20)
    print(test2.get_physicians_tab())
    for i in hospitalInfo.physician:
        print(test2.get_number_of_patient_per_physician_by_id(i))
    '''
    '''
    #Transfert Block Test
    hospitalInfo = SystemInfo(w3)
    ambulance_info=AmbulanceCost(range(0, 9), range(0, 3))
    transfertBLockObject = TransfertBlock(w3)

    # Test Patient
    for i in range(0, 9):
        transfertBLockObject.add_patient(i)
    time.sleep(20)

    # Test Physician
    for i in range(0, 9):
        number = Topsis(np.array([0.5, 0.8]), ["cosy", "beautiful"], hospitalInfo, ["e1"], i, "Oncology").fit()
        patient_physician = pd.DataFrame(index=range(0, 6))
        patient_physician = pd.concat([patient_physician, number], axis=1, sort=True).fillna(0).T
        transfertBLockObject.set_patient_matched_physician(i, [int(x) for x in list(patient_physician.loc[i, :])])
        transfertBLockObject.set_severity_of_illness_by_id(i, 20)
    time.sleep(20)

    # Test Hospital
    for hospital in hospitalInfo.hospitals:
        transfertBLockObject.add_hospital(hospital)

    # Test Cost Ambulance
    cost=ambulance_info.ambulance_cost
    time.sleep(20)
    for patient in range(0, 9):
        transfertBLockObject.set_ambulance_cost(patient, list(cost.loc[patient, :]))
    time.sleep(20)

    print(transfertBLockObject.get_patients())
    print(transfertBLockObject.get_hospitals())
    for patient in range(0, 9):
        print(transfertBLockObject.get_ambulance_cost_by_id(patient))

    for i in range(0, 9):
        print(transfertBLockObject.get_number_of_patient_matched_physician_by_id(i))
        print("bouf")
        print(transfertBLockObject.get_severity_of_illness_by_id(i))

    '''
    '''
    # Test Filtres
    myfilter = transfertBLockObject.EventFilter('ReadyForMining')
    eventlist = myfilter.get_all_entries()
    print(eventlist)
    '''
