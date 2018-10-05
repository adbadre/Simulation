import pandas as pd
import numpy as np
import random


class SystemInfo:

    def __init__(self, w3, number_of_hospital):
        self.physician = range(0, number_of_hospital*4)
        self.w3 = w3
        self.hospitals = [w3.eth.accounts[i] for i in range(number_of_hospital)]
        self.services = [0, 1]
        a = [random.randint(0, 1) for _ in range(number_of_hospital)]
        a2 = [1-x for x in a]
        self.hospitals_service = pd.DataFrame(data=np.array([a, a2]).T,
                                              index=self.hospitals, columns=self.services) # wont be in at the end
        # Create random assignation for physicians


        label1 = []
        label2 = []
        i = 0
        j = 0
        for _ in self.hospitals:
            for _ in self.services:
                label1.append(i)
                label2.append(j)
                if j == 0:
                    j = 1
                else:
                    j = 0
                    i += 1

        #Physician hospital service
        self.physician_hospital_service = pd.DataFrame(data=np.zeros(shape=(len(self.hospitals)*2, len(self.physician)),
                                                                     dtype=int),
                                                       index=pd.MultiIndex(
                                                           levels=[self.hospitals, self.services],
                                                           labels=[label1, label2]
                                                       ),
                                                       columns=self.physician)
        for ph in self.physician:
            h = random.randint(0, len(self.hospitals) - 1)
            if a[h] == 0:
                self.physician_hospital_service.xs((self.hospitals[h], 1)).loc[ph] = 1
            else:
                self.physician_hospital_service.xs((self.hospitals[h], 0)).loc[ph] = 1

        self.cost_loosing_patient = pd.DataFrame([[400 for _ in range(len(self.hospitals))],
                                                  [600 for _ in range(len(self.hospitals))]],
                                                 index=self.services, columns=self.hospitals).T
        for i in self.hospitals:
            for j in self.services:
                if self.hospitals_service.loc[i, j] == 0:
                    self.cost_loosing_patient.loc[i, j] = 5000000000000000000

        self.bed_hospital = pd.DataFrame(np.random.randint(0, 1000, size=(1, len(self.hospitals))),
                                         columns=self.hospitals)

    def physician_request(self, specialty):
        idx = pd.IndexSlice
        data = self.physician_hospital_service[self.physician_hospital_service.loc[idx[:, specialty], :]>0.5]
        unic = data.apply(pd.Series.nunique)
        data=data.drop(unic[unic == 0].index, axis=1)
        return data.columns.values

