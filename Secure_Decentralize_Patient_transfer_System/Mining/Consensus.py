import numpy as np
import pandas as pd


class Consensus:

    def __init__(self, local_solutions, enforced_constraints, general_solution, sigma, number_of_hospitals):
        self.number_of_hospitals = number_of_hospitals
        self.local_solutions = local_solutions
        self.enforced_constraints = enforced_constraints
        self.general_solution = general_solution
        self.lagrange_multiplier_vector = np.zeros(local_solutions.shape)
        self.k = 0
        self.sigma = sigma
        self.epsilon1 = 0
        self.epsilon2 = 0

    def estimate_global_variable(self):
        old_general_solution = self.general_solution
        self.general_solution = np.dot(np.dot(np.invert(np.dot(self.enforced_constraints.T, self.enforced_constraints)),
                                       self.enforced_constraints.T),
                                       (self.local_solutions + self.lagrange_multiplier_vector/self.sigma)
                                       )
        self.epsilon2 = np.linalg.norm(self.sigma * np.dot(self.enforced_constraints,
                                                           (self.general_solution - old_general_solution)
                                                           )
                                       )

    def dual_update(self):
        self.lagrange_multiplier_vector = self.lagrange_multiplier_vector \
                                          + self.sigma * (self.local_solutions -
                                                          self.enforced_constraints * self.general_solution)

    def fit(self):
        stop = False
        while not stop:
            for hospital in range(0, self.number_of_hospitals):
                self.local_solutions[hospital] = "coucou"

            self.estimate_global_variable()
            self.dual_update()
            self.epsilon1 = np.linalg.norm(self.local_solutions - np.dot(self.enforced_constraints,
                                                                         self.general_solution)
                                           )
            if self.epsilon1 < 2000000 and self.epsilon2 < 2000000:
                stop = True
            else:
                self.k = self.k+1
