from BlockchainService.ContractFactory import ContractFactory


class PhysicianHospitalService:
    __PhysicianHospitalService_object = None
    __contract_object = None
    __contract_info=None
    __w3 = None

    @staticmethod
    def get_instance(*args):
        if PhysicianHospitalService.__contract_object is None or len(args) > 0:
            PhysicianHospitalService(args[0], args[1])
        return PhysicianHospitalService.__PhysicianHospitalService_object

    def __init__(self, w3,hospital_accounts):
        PhysicianHospitalService.__w3 = w3
        with open(
                "C:\\Users\\badre\\OneDrive\\Bureau\\theses\\Secure_Decentralize_Patient_transfer_System\\Blockchain_Contracts\\PhysicianHospitalServiceContract.sol") as file:
            contract_code = file.read()
        contract = ContractFactory(contract_code, 'PhysicianHospitalServiceContract', w3.eth.accounts[0], w3,hospital_accounts)
        PhysicianHospitalService.__contract_info = contract.deploy_contract('')
        PhysicianHospitalService.__contract_object = w3.eth.contract(address=PhysicianHospitalService.__contract_info[0]
                                                                     , abi=PhysicianHospitalService.__contract_info[1])
        PhysicianHospitalService.__PhysicianHospitalService_object = self

    def set_hospital_service_physician(self, physician, hospital, id_service):
        self.__contract_object.functions.set_hospital_service_physician(physician, hospital, id_service).transact()

    def set_hospital_service(self, hospital, services):
        self.__contract_object.functions.set_hospital_service(hospital, services).transact()

    def set_physicians_tab(self, new_physicians_tab):
        self.__contract_object.functions.set_physicians_tab(new_physicians_tab).transact()

    def set_number_of_patient_per_physician(self, physician, number):
        self.__contract_object.functions.set_number_of_patient_per_physician(physician, number).transact()

    def set_number_of_bed_per_hospital(self, hospital, number_of_bed):
        self.__contract_object.functions.set_number_of_bed_per_hospital(hospital, number_of_bed).transact()

    def delete_hospital_service(self, hospital, id_service):
        self.__contract_object.functions.delete_hospital_service(hospital, id_service).transact()

    def get_physician_service_hospital_by_hospital(self, hospital, service):
        return self.__contract_object.functions.get_physician_service_hospital_by_hospital(hospital, service).call()

    def get_physicians_tab(self):
        return self.__contract_object.functions.get_physicians_tab().call()

    def get_hospital_service(self, hospital):
        return self.__contract_object.functions.get_hospital_service(hospital).call()

    def get_hospital(self):
        return self.__contract_object.functions.get_hospital().call()

    def get_physician_service_hospital_by_service(self, id_service):
        return self.__contract_object.functions.get_physician_service_hospital_by_service(id_service).call()

    def get_number_of_patient_per_physician_by_id(self, physician_id):
        return self.__contract_object.functions.get_number_of_patient_per_physician_by_id(physician_id).call()

    def get_number_of_bed_per_hospital(self, hospital):
        return self.__contract_object.functions. get_number_of_bed_per_hospital(hospital).call()
