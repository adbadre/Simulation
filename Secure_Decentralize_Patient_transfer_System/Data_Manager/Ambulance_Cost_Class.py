import pandas as pd
import numpy as np


class AmbulanceCost:

    def __init__(self, patient, hospital):
        self.ambulance_cost = pd.DataFrame(np.random.randint(600, 800, size=(len(patient), len(hospital))),
                                           index=patient, columns=hospital)

    def __getitem__(self, item):
        return self.ambulance_cost[item]

    def __len__(self):
        return len(self.ambulance_cost)
