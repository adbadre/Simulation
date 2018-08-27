

class PhysicianNetwork:

    def __init__(self):
        self.physician = ["DR henry", "DR Jack", "DR boo", "Dr lolo", "Dr Libman", "Dr Niptuk"]

    def __getitem__(self, item):
        return self.physician[item]

    def __len__(self):
        return len(self.physician)
