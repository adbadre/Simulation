import pandas as pd
import numpy as np


class HospitalInfo:

    def __init__(self, w3):
        self.physician = range(0, 6)
        self.w3 = w3
        self.hospitals = [self.w3.eth.accounts[0], self.w3.eth.accounts[1], self.w3.eth.accounts[2]]
        self.services = [0, 1]
        self.hospitals_service = pd.DataFrame(data=np.array([[1, 1, 1], [0, 1, 1]]).T,
                                              index=self.hospitals, columns=self.services) # wont be in at the end
        self.physician_hospital_service = pd.DataFrame(data=np.array([[0, 0, 0, 1, 0, 0],
                                                                      [1, 0, 0, 0, 0, 0],
                                                                      [0, 0, 1, 0, 0, 0],
                                                                      [0, 0, 1, 0, 0, 0],
                                                                      [0, 0, 0, 0, 1, 0],
                                                                      [0, 0, 0, 0, 0, 1]
                                                                      ]).T,
                                                       index=pd.MultiIndex(
                                                           levels=[self.hospitals, self.services],
                                                           labels=[[0, 0, 1, 1, 2, 2], [0, 1, 0, 1, 0, 1]]
                                                       ),
                                                       columns=self.physician)

        self.cost_loosing_patient = pd.DataFrame(np.random.randint(200,
                                                                   1000,
                                                                   size=(len(self.hospitals), len(self.services))
                                                                   ),
                                                 index=self.hospitals, columns=self.services)
        for i in self.hospitals:
            for j in self.services:
                if self.hospitals_service.loc[i, j] == 0:
                    self.cost_loosing_patient.loc[i, j] = 500000

        self.bed_hospital = pd.DataFrame(np.random.randint(0, 1000, size=(1, len(self.hospitals))),
                                         columns=self.hospitals)

    def physician_request(self, specialty):
        idx = pd.IndexSlice
        data = self.physician_hospital_service[self.physician_hospital_service.loc[idx[:, specialty], :]>0.5]
        unic = data.apply(pd.Series.nunique)
        data=data.drop(unic[unic==0].index,axis=1)
        return data.columns.values
