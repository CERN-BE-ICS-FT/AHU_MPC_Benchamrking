import numpy as np

CPU_CORES = 32

# Number of times to run each instance of the program where inputs are fixed. This is done in order to account for variations in computation time
REPITITION = 5
TIMEOUT = 60  # In seconds. Terminate the program in 60 seconds if the MPC is not solved within that time-frame

#[Toa, Tza, dout, omega, Tha_step, Tca_step]
NUM_INPUTS = 6
NUM_UNIQUE_VALUES = [10, 5, 10, 10, 3, 3]


Toa_CHOICES = list(range(-10, 40, 5))
Tza_CHOICES = list(range(17, 27, 2))
dout_CHOICES = list(range(10, 101, 10))
omega_CHOICES = list(range(0, 91, 10))
omega_CHOICES[0] = 1
Tha_step_CHOICES = [0, 2, 4]
Tca_step_CHOICES = [0, 2, 4]


CHOICE_array = [
    Toa_CHOICES,
    Tza_CHOICES,
    dout_CHOICES,
    omega_CHOICES,
    Tha_step_CHOICES,
    Tca_step_CHOICES
]