
class PatientHandler:

    def __init__(self):
        self.patient = ["Jack", "Franck", "Henry"]

    def __getitem__(self, item):
        return self.patient[item]

    def __len__(self):
        return len(self.patient)