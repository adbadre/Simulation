import pandas as pd
import numpy as np


class SeverityOfIllness:

    def __init__(self, patient):
        self.illness_severity = pd.DataFrame(np.random.randint(1, 5, size=(1, len(patient))),
                                             index=['severity'], columns=patient)

    def __getitem__(self, item):
        return self.illness_severity[item]
