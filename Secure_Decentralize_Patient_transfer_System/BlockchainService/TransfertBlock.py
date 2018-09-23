class TransfertBlock:

    def __init__(self, address, abi, w3):
        self.w3 = w3
        self.contract_object = w3.eth.contract(address=address, abi=abi)

    def add_hospital(self, new_hospital_for_transaction):
        self.contract_object.functions.add_hospital(new_hospital_for_transaction).transact()

    def add_patient(self, patient_id):
        self.contract_object.functions.add_patient(patient_id).transact()

    def add_physician(self, physician_id):
        self.contract_object.functions.add_physician(physician_id).transact()

    def set_ambulance_cost(self, patient_id, cost):
        self.contract_object.functions.set_ambulance_cost(patient_id, cost).transact()

    def set_number_of_patient_per_physician(self, physician, number):
        self.contract_object.functions.set_number_of_patient_per_physician(physician, number).transact()

    def set_patient_matched_physician(self, patient, physicians_matched):
        print(patient, physicians_matched)
        self.contract_object.functions.set_patient_matched_physician(patient, physicians_matched).transact()

    def set_severity_of_illness_by_id(self, patient_id, severity_of_illness):
        self.contract_object.functions.set_severity_of_illness_by_id(patient_id, severity_of_illness).transact()

    def set_previous_block(self, new_previous_block):
        self.contract_object.functions.set_previous_block(new_previous_block).transact()

    def get_patients(self):
        return self.contract_object.functions.get_patients().call()

    def get_hospitals(self):
        return self.contract_object.functions.get_hospitals().call()

    def get_physician(self):
        return self.contract_object.functions.get_physician().call()

    def get_ambulance_cost_by_id(self, patient_id):
        return self.contract_object.functions.get_ambulance_cost_by_id(patient_id).call()

    def get_number_of_patient_per_physician_by_id(self, physician_id):
        return self.contract_object.functions.get_number_of_patient_per_physician_by_id(physician_id).call()

    def get_severity_of_illness_by_id(self, patient_id):
        return self.contract_object.functions.get_severity_of_illness_by_id(patient_id).call()

    def get_number_of_patient_matched_physician_by_id(self, patient_id):
        return self.contract_object.functions.get_number_of_patient_matched_physician_by_id(patient_id).call()

    def solution_filled(self):
        self.contract_object.functions.solution_filled().call()

    def EventFilter(self, name):
        if name=="ReadyForMining":
            return self.contract_object.events.ReadyForMining.createFilter(fromBlock=0, argument_filters={})
        else:
            return self.contract_object.events.TransactionMined.createFilter(fromBlock=0, argument_filters={})

