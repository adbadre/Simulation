from BlockchainService.ContractFactory import ContractFactory
class TransfertBlock:

    def __init__(self, w3):
        self.w3 = w3
        with open(
                "C:\\Users\\badre\\OneDrive\\Bureau\\theses\\Secure_Decentralize_Patient_transfer_System\\Blockchain_Contracts\\TransfertBlock.sol") as file:
            contract_code = file.read()
        contract = ContractFactory(contract_code, 'TransfertBlock', w3.eth.accounts[0], w3)
        contract_info = contract.deploy_contract('')
        self.contract_object = w3.eth.contract(address=contract_info[0], abi= contract_info[1])

    def add_hospital(self, new_hospital_for_transaction):
        self.contract_object.functions.add_hospital(new_hospital_for_transaction).transact()

    def add_patient(self, patient_id):
        self.contract_object.functions.add_patient(patient_id).transact()

    def set_ambulance_cost(self, patient_id, cost):
        self.contract_object.functions.set_ambulance_cost(patient_id, cost).transact()

    def set_patient_matched_physician(self, patient, physicians_matched):
        print(patient, physicians_matched)
        self.contract_object.functions.set_patient_matched_physician(patient, physicians_matched).transact()

    def set_severity_of_illness_by_id(self, patient_id, severity_of_illness):
        self.contract_object.functions.set_severity_of_illness_by_id(patient_id, severity_of_illness).transact()

    def set_cost_of_loosing_patient_by_id(self, hospital,  service_id,  cost):
        self.contract_object.functions.set_cost_of_loosing_patient_by_id(hospital, service_id, cost).transact()

    def set_previous_block(self, new_previous_block):
        self.contract_object.functions.set_previous_block(new_previous_block).transact()

    def set_number_of_bed_hospital(self, hospital, number_of_bed):
        self.contract_object.functions.set_previous_block(hospital, number_of_bed).transact()

    def get_patients(self):
        return self.contract_object.functions.get_patients().call()

    def get_hospitals(self):
        return self.contract_object.functions.get_hospitals().call()

    def get_ambulance_cost_by_id(self, patient_id):
        return self.contract_object.functions.get_ambulance_cost_by_id(patient_id).call()

    def get_severity_of_illness_by_id(self, patient_id):
        return self.contract_object.functions.get_severity_of_illness_by_id(patient_id).call()

    def get_cost_of_loosing_patient_by_id(self, hospital, service):
        return self.contract_object.functions.get_cost_of_loosing_patient_by_id(hospital, service).call()

    def get_number_of_patient_matched_physician_by_id(self, patient_id):
        return self.contract_object.functions.get_number_of_patient_matched_physician_by_id(patient_id).call()

    def get_number_of_bed_hospital(self, hospital):
        return self.contract_object.functions. get_number_of_bed_hospital(hospital).call()

    def solution_filled(self):
        self.contract_object.functions.solution_filled().call()

    def EventFilter(self, name):
        if name=="ReadyForMining":
            return self.contract_object.events.ReadyForMining.createFilter(fromBlock=0, argument_filters={})
        else:
            return self.contract_object.events.TransactionMined.createFilter(fromBlock=0, argument_filters={})

