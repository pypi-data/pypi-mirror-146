# Importing NumPy as "np"
import numpy as np

class Multiplication:
    def __init__(self, multiplier):
        self.multiplier = multiplier

    def multiply(self, number):
        return np.dot(number, self.multiplier)