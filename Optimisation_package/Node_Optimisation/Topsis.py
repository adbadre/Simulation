import numpy as np
import pandas as pd
from Data_Manager.Hospital_Info_Class import HospitalInfo

class Topsis:

    def __init__(self, alpha, criteria, physician_hospital, expert, patient_name, specialty):
        self.alpha = alpha
        self.criteria = list(criteria)
        self.expert = list(expert)
        self.criteria_importance_matrix = None
        self.physician_grading = []
        self.weight_criteria = None
        self.weight_physicians = []
        self.decision_matrix = None
        self.ideal_solution = None
        self.negative_solution = None
        self.S_top = None
        self.S_worst = None
        self.closeness = []
        self.patient_name = patient_name
        self.specialty = specialty
        self.physicians = physician_hospital.physician_request(specialty)
        print(self.physicians)

    # Criteria importance process
    def criteria_importance_process(self):
        self.criteria_importance_matrix = pd.DataFrame(
            np.random.randint(1, 5, size=(len(self.criteria), len(self.expert) + 1)),
            columns=self.expert + ["patient"],
            index=self.criteria)
        self.criteria_importance_matrix["patient"] = np.dot(self.alpha, self.criteria_importance_matrix["patient"])
        self.criteria_importance_matrix[self.criteria_importance_matrix.columns.difference(['patient'])] = np.dot(
            (1 - self.alpha),
            self.criteria_importance_matrix[self.criteria_importance_matrix.columns.difference(['patient'])])

    # Grading of the physician method ( random number for the moment)
    def physician_grading_process(self):
        for _ in self.physicians:
            self.physician_grading.append(
                pd.DataFrame(np.random.randint(1, 5, size=(len(self.criteria), len(self.expert))),
                             columns=self.expert,
                             index=self.criteria)
                )

    # Weight computation
    def weight_criteria_process(self):
        self.weight_criteria = self.criteria_importance_matrix.mean(axis=1)

    # Decision matrix computation
    def decision_matrix_computation(self):
        for i in range(0, len(self.physicians)):
            self.weight_physicians.append(self.physician_grading[i].mean(axis=1))
        self.decision_matrix = pd.DataFrame(self.weight_physicians, index=self.physicians)
        '''Normalize'''
        self.decision_matrix = self.decision_matrix.div(self.decision_matrix.sum(axis=0), axis=1)
        '''Weighted Decision'''
        self.decision_matrix = self.decision_matrix * self.weight_criteria
        self.decision_matrix = self.decision_matrix.T

    # Compute the solutions (physician ranking)
    def solution_computation(self):
        '''Ideal and Negative Solution'''
        self.ideal_solution = self.decision_matrix.max(axis=1)
        self.negative_solution = self.decision_matrix.min(axis=1)
        '''Separation from ideal and negative solution'''
        self.S_top = (self.decision_matrix.subtract(self.ideal_solution, axis=0).pow(2).sum(0)).pow(0.5)
        self.S_worst = (self.decision_matrix.subtract(self.negative_solution, axis=0).pow(2).sum(0)).pow(0.5)
        self.closeness = self.S_worst / (self.S_worst + self.S_top)
        return self.closeness

    # Fit function
    def fit(self):
        self.criteria_importance_process()
        self.physician_grading_process()
        self.weight_criteria_process()
        self.decision_matrix_computation()
        solution = self.solution_computation()
        p1_fit = pd.DataFrame(solution, columns=[self.patient_name])
        mask = p1_fit.loc[:, self.patient_name] > 0.5
        mask2 = p1_fit.loc[:, self.patient_name] <= 0.5
        p1_fit.loc[mask,  self.patient_name] = 1
        p1_fit.loc[mask2, self.patient_name] = 0
        return p1_fit


