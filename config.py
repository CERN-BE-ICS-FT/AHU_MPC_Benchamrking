import numpy as np

CPU_CORES = 32

# Number of times to run each instance of the program where inputs are fixed. This is done in order to account for variations in computation time
REPITITION = 5
TIMEOUT = 60  # In seconds. Terminate the program in 60 seconds if the MPC is not solved within that time-frame

# [Tza, Tma, Tha, Tca, Tsa, Toa]
NUM_TEMPERATURE_INPUTS = 6
NUM_UNIQUE_TEMPERATURE_VALUES = 5

# In the paper the Zone Air Temprature - Tza_Min and Tza_Max are constraints which are set to 20 and 24
# In the code, parameters.py, it is set as xza_min, xza_max = 17, 26
Tza_OFFSET = 17
Tza_MAX = 26

# Mixed Air
Tma_OFFSET = 0
Tma_MAX = 30

# Hot Air Temprature is bound by heating coil. In parameter.py Th_max = 30 is set.
Tha_OFFSET = 12
Tha_MAX = 30

# Cold Air Temprature is bound by cooling coil. In both the paer and In parameter.py Tc_min = 12 is set
Tca_OFFSET = 12
Tca_MAX = 30

# In the paper the Supply Air Temprature - Tsa_Min and Tsa_Max are constraints which are set to 16 and 30
# In the code, parameters.py, it is set as xsa_min, xsa_max = 17, 30
Tsa_OFFSET = 17
Tsa_min = 17
Tsa_MAX = 30


# Outside Air Temprature is an Observable. It has to be queried via an API provided by weather stations
# Usually the resonsable range Toa_min, Toa_max = -20, 40
Toa_OFFSET = 0
Toa_MAX = 30

# Actuators Fan Speed and Outside Airdamper
# Also turn these into inputs (Current fan speed and Damper posiions) ?
omega, dout = 1, 10
omega_MAX, dout_MAX = 100, 100


Tza_STEP_SIZE = (Tza_MAX - Tza_OFFSET) / (NUM_UNIQUE_TEMPERATURE_VALUES - 1)
Tma_STEP_SIZE = (Tma_MAX - Tma_OFFSET) / (NUM_UNIQUE_TEMPERATURE_VALUES - 1)
Tha_STEP_SIZE = (Tha_MAX - Tha_OFFSET) / (NUM_UNIQUE_TEMPERATURE_VALUES - 1)
Tca_STEP_SIZE = (Tca_MAX - Tca_OFFSET) / (NUM_UNIQUE_TEMPERATURE_VALUES - 1)
Tsa_STEP_SIZE = (Tsa_MAX - Tsa_OFFSET) / (NUM_UNIQUE_TEMPERATURE_VALUES - 1)
Toa_STEP_SIZE = (Toa_MAX - Toa_OFFSET) / (NUM_UNIQUE_TEMPERATURE_VALUES - 1)

MULTIPLIER_ARRAY = np.array(
    [Tza_STEP_SIZE, Tma_STEP_SIZE, Tha_STEP_SIZE, Tca_STEP_SIZE, Tsa_STEP_SIZE, Toa_STEP_SIZE]
)

OFFSET_ARRAY = np.array(
    [Tza_OFFSET, Tma_OFFSET, Tha_OFFSET, Tca_OFFSET, Tsa_OFFSET, Toa_OFFSET]
)
