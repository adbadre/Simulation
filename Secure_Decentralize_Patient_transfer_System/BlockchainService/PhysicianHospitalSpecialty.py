class PhysicianHospitalService:
    __PhysicianHospitalService_object = None
    __contract_object = None
    __w3 = None

    @staticmethod
    def get_instance(*args):
        if PhysicianHospitalService.__contract_object is None:
            print(args[0], args[1])
            PhysicianHospitalService(args[0], args[1], args[2])
        return PhysicianHospitalService.__PhysicianHospitalService_object

    def __init__(self, address, abi, w3):
        PhysicianHospitalService.__w3 = w3
        PhysicianHospitalService.__contract_object = w3.eth.contract(address=address, abi=abi)
        PhysicianHospitalService.__PhysicianHospitalService_object = self

    def set_hospital_service_physician(self, physician, hospital, id_service):
        self.__contract_object.functions.set_hospital_service_physician(physician, hospital, id_service).transact()


    def set_physicians_tab(self, new_physicians_tab):
        self.__w3.eth.waitForTransactionReceipt(
            self.__contract_object.functions.set_physicians_tab(new_physicians_tab).transact())


    def delete_hospital_service(self, hospital, id_service):
        self.functions.delete_hospital_service(hospital, id_service).transact()

    def get_physician_service_hospital_by_hospital(self, hospital, service):
        return self.__contract_object.functions.get_physician_service_hospital_by_hospital(hospital, service).call()
