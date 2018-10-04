from BlockchainService.LatestBlock import LatestBlock
from BlockchainService.PhysicianHospitalSpecialty import PhysicianHospitalService
from BlockchainService.ContractFactory import ContractFactory
from pandas import IndexSlice


class BlockchainGenesis:

    def __init__(self,):
        self.LatestBlock = None
        self.PhysicianHospitalService = None
        pass

    def set_latest_block(self, w3):
        # Latest Block Contract
        self.LatestBlock = LatestBlock.get_instance(w3)

    def set_physician_hospital_service(self, w3, system_info):
        # Physician Hospital Service
        self.PhysicianHospitalService = PhysicianHospitalService.get_instance(w3)
        physician_tab = []
        # Set physician
        for physician in system_info.physician:
            physician_tab.append(physician)
            self.PhysicianHospitalService.set_number_of_patient_per_physician(physician, 15)
        self.PhysicianHospitalService.set_physicians_tab(physician_tab)
        # Set the matrix hospital service physician
        idx = IndexSlice
        for hospital in system_info.hospitals:
            j = 0
            self.PhysicianHospitalService.set_hospital_service(hospital, list(system_info.hospitals_service
                                                                              .loc[hospital, :]))
            for service in system_info.services:
                print(list(system_info.physician_hospital_service.loc[idx[hospital, service], :]))
                self.PhysicianHospitalService.set_hospital_service_physician(list(system_info
                                                                                  .physician_hospital_service
                                                                                  .loc[idx[hospital, service], :]),
                                                                             hospital,
                                                                             j)
                j += 1

    def genesis(self, w3, hospital_info):
        w3.personal.unlockAccount(w3.eth.accounts[0], '')
        self.set_latest_block(w3)
        self.set_physician_hospital_service(w3, hospital_info)
        return {'latest_block': self.LatestBlock, 'physician_hospital_service': self.PhysicianHospitalService}
