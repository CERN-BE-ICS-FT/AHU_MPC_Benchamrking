import numpy as np
from config_v2 import *
import parameters as param

##--------- Damper characteristics model
#mixing_chamber
def generate_Tma(dout, omega, Toa, Tza):
        fan_mdot = param.b1 * omega + param.b2
        alpha1 = param.w1 * ((fan_mdot * dout) / 100)
        alpha2 = param.w2 * ((fan_mdot * (100-dout)) / 100)
        Tma = (alpha1 * Toa + alpha2 * Tza) / fan_mdot
        return Tma

##--------- Fan heat gain model
#fan_heat_gain
def generate_Tsa(omega, Tca):
        fan_mdot = param.b1 * omega + param.b2
        Tsa = Tca + ((param.gamma_fan * 1000 * (param.c1 * omega ** 2 + param.c2 * omega + param.c3)) / (param.Cpa * fan_mdot))
        return Tsa

# __________________________________________________________________________________________________________________________________________________________________
# Thefunction converts an integer to a baseN representation.
# The goal is e.g. - Convert a job id to Temprature and actuator inputs. And this function forms the first step.

# Lets say you have 6 inputs [Toa, Tza, dout, omega, Tha_step, Tca_step] and set of unique values for each inputs e.g. 10 x 5 x 10 x 10 x 3 x 3 input Grid (with 45000 inputs points)

# then for a job id e.g. 1166, the input array generated is - [0 1 4 1 3 1]. Here each element in the list represents the nth unique input value. 
# E.g. For the 3rd input, 5th unique value is selected. Note - Index starts from 0 and goes until 4.
# __________________________________________________________________________________________________________________________________________________________________

# __________________________________________________________________________________________________________________________________________________________________
#Logic
# Tza - Sweep
# Tma - Generate
# Tha - Sweep (> Tma, Coil constraints), xha_dot = 4 
# Tca - Sweep (< Tha, Coil Constraint), xca_dot = 4
# Tsa - Generate
# Toa - Sweep
# Tma - Generate based on model on doa and Toa
# dout - Sweep 10 to 100
# omega - Sweep 1 to 90
# __________________________________________________________________________________________________________________________________________________________________

def convert_to_baseN(decimal_number, base_N, digit_length):
    if decimal_number == 0:
        return np.zeros(digit_length, dtype=int)

    baseN_digits = []
    step_index = 0
    while decimal_number > 0:
        decimal_number, remainder = divmod(decimal_number, base_N[step_index])
        baseN_digits.insert(0, str(remainder))
        step_index+=1

    input_str = "".join(baseN_digits).zfill(digit_length)
    input_str_array = list(input_str)
    input_array = np.array(input_str_array, dtype=int)
    return input_array

# __________________________________________________________________________________________________________________________________________________________________
# Examples
# base for each onput - base_N = [10, 5, 10, 10, 3, 3]
# has to be reversed to get the correct order. i.e. the number first has to be divided by 3 NOT 10!
# base_N = [10, 5, 10, 10, 3, 3]
# reversed_base_N = base_N[::-1]
# reversed_base_N
# __________________________________________________________________________________________________________________________________________________________________


# __________________________________________________________________________________________________________________________________________________________________
# This function takes the index for [Toa, Tza, dout, omega, Tha_step, Tca_step] generated above and selects the actual values values
# E.g. For input array - [0 1 4 1 2 1] - for the 6th input, 2nd choice is selected 
# Choices are defined in config file
# __________________________________________________________________________________________________________________________________________________________________


def calculate_inputs(job_id):
    baseN_array = convert_to_baseN(
        job_id, NUM_UNIQUE_VALUES, NUM_INPUTS
    )
    # Reverse the baseN_array
    baseN_array = baseN_array[::-1]

    selected_choices = []
    for input_CHOICE, idx in zip(CHOICE_array, baseN_array):
        selected_choices.append(input_CHOICE[idx])
    
    Toa, Tza, dout, omega, Tha_step, Tca_step = selected_choices
    Tma = generate_Tma(dout, omega, Toa, Tza)
    Tha = Tma + Tha_step
    Tca = Tha - Tca_step
    Tsa = generate_Tsa(omega, Tca)
    temprature_inputs = np.array([Tza, Tma, Tha, Tca, Tsa])
    actuator_inputs = np.array([omega, dout])
    return Toa, temprature_inputs, actuator_inputs