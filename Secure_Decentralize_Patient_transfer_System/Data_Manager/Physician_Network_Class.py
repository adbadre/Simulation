import pandas as pd
import numpy as np


class PhysicianNetwork:

    def __init__(self):
        self.physician = ["DR henry", "DR Jack", "DR boo", "Dr lolo", "Dr Libman", "Dr Niptuk"]

    def __getitem__(self, item):
        return self.physician[item]
