import random
import numpy as np
from scipy.stats import norm

def bellAge() -> []:
    x = [random.randint(1, 100) for i in range(100)]
    mean = np.mean(x)
    sd = np.std(x)
    pdf = list(map(lambda x: ((x-18) /2) +18, (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)))
    return round(pdf[random.randint(0, 99)])
