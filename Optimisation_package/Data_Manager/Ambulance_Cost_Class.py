import pandas as pd
import numpy as np


class AmbulanceCost:

    def __init__(self, patient, hospital):
        self.ambulance_cost = pd.DataFrame(np.random.randint(100, 2000000, size=(len(patient), len(hospital))) / 100,
                                           index=patient, columns=hospital)

    def __getitem__(self, item):
        return self.ambulance_cost[item]
