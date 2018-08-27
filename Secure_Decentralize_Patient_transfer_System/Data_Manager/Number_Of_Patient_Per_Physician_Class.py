import pandas as pd
import numpy as np


class NumberOfPatientPerPhysician:

    def __init__(self):
        physician = ["DR henry", "DR Jack", "DR boo", "Dr lolo", "Dr booh", "Dr Libman", "Dr Niptuk"]
        self.patient_by_physician = pd.DataFrame(np.random.randint(1, 2, size=(1, len(physician))),
                                                 columns=physician)

    def __getitem__(self, item):
        return self.patient_by_physician[item]

    def __len__(self):
        return len(self.patient_by_physician)
