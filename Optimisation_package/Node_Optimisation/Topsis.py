import numpy as np
import pandas as pd


class Topsis:

    def __init__(self, alpha, criteria, physicians, expert):
        self.alpha = alpha
        self.criteria = list(criteria)
        self.physicians = list(physicians)
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

    def criteria_importance_process(self):
        self.criteria_importance_matrix = pd.DataFrame(
            np.random.randint(1, 5, size=(len(self.criteria), len(self.expert) + 1)),
            columns=self.expert + ["patient"],
            index=self.criteria)
        self.criteria_importance_matrix["patient"] = np.dot(self.alpha, self.criteria_importance_matrix["patient"])
        self.criteria_importance_matrix[self.criteria_importance_matrix.columns.difference(['patient'])] = np.dot(
            (1 - self.alpha),
            self.criteria_importance_matrix[self.criteria_importance_matrix.columns.difference(['patient'])])

    def physician_grading_process(self):
        for _ in self.physicians:
            self.physician_grading.append(
                pd.DataFrame(np.random.randint(1, 5, size=(len(self.criteria), len(self.expert))),
                             columns=self.expert,
                             index=self.criteria)
                )

    def weight_criteria_process(self):
        self.weight_criteria = self.criteria_importance_matrix.mean(axis=1)

    def decision_matrix_computation(self):
        for i in range(0, len(self.physicians)):
            self.weight_physicians.append(self.physician_grading[i].mean(axis=1))
        self.decision_matrix = pd.DataFrame(self.weight_physicians, index=self.physicians)
        '''Normalize'''
        self.decision_matrix = self.decision_matrix.div(self.decision_matrix.sum(axis=0), axis=1)
        '''Weighted Decision'''
        self.decision_matrix = self.decision_matrix * self.weight_criteria
        self.decision_matrix = self.decision_matrix.T

    def solution_computation(self):
        '''Ideal and Negative Solution'''
        self.ideal_solution = self.decision_matrix.max(axis=1)
        self.negative_solution = self.decision_matrix.min(axis=1)
        '''Separation from ideal and negative solution'''
        self.S_top = (self.decision_matrix.subtract(self.ideal_solution, axis=0).pow(2).sum(0)).pow(0.5)
        self.S_worst = (self.decision_matrix.subtract(self.negative_solution, axis=0).pow(2).sum(0)).pow(0.5)
        self.closeness = self.S_worst / (self.S_worst + self.S_top)
        return self.closeness

    def fit(self):
        self.criteria_importance_process()
        self.physician_grading_process()
        self.weight_criteria_process()
        self.decision_matrix_computation()
        solution = self.solution_computation()
        return solution


'''if __name__=="__main__":
    t=Topsis(np.array([0.5,0.5]), ["cosy", "beautifull"], ["DR henry", "DR Jack","DR boo"], ["e1", "e2"])
    print(t.fit())
'''
