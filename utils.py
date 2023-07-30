import numpy as np
from config import *

# __________________________________________________________________________________________________________________________________________________________________
# Thefunction converts an integer to a baseN representation.
# The goal is e.g. - Convert a job id to Temprature inputs. And this function forms the first step.
# Lets say you have 6 temprature inputs [Tza, Tma, Tha, Tca, Tsa, Toa] and 5 unique values for each inputs i.e. 5 x 5 ... x 5 input Grid
# then for a job id e.g. 1166, the input array generated is - [0 1 4 1 3 1]. Here each element in the list represents the nth unique input value.
# For the 3rd input, 5th unique value is selected. Note - Index starts from 0 and goes until 4.
# __________________________________________________________________________________________________________________________________________________________________


def convert_to_baseN(decimal_number, N, digit_length):
    if decimal_number == 0:
        return np.zeros(digit_length, dtype=int)

    baseN_digits = []
    while decimal_number > 0:
        decimal_number, remainder = divmod(decimal_number, N)
        baseN_digits.insert(0, str(remainder))
        input_str = "".join(baseN_digits).zfill(digit_length)
        input_str_array = list(input_str)
        input_array = np.array(input_str_array, dtype=int)
    return input_array


# __________________________________________________________________________________________________________________________________________________________________
# This function takes the input array for [Tza, Tma, Tha, Tca, Tsa, Toa] generated above and coverts it to temprature values
# For input array - [0 1 4 1 3 1], you have to multiply by the step size for each inputs set by the user.
# Lets say the step size for 5th input is 3, and the first unique value is 17. Then the final input is 17 +(3  * 3.25) = 26.75
# __________________________________________________________________________________________________________________________________________________________________


def calculate_temperature_inputs(job_id):
    baseN_array = convert_to_baseN(
        job_id, NUM_UNIQUE_TEMPERATURE_VALUES, NUM_TEMPERATURE_INPUTS
    )
    temperature_inputs = (baseN_array * MULTIPLIER_ARRAY) + OFFSET_ARRAY
    return temperature_inputs


job_id = 1166
temperature_inputs = calculate_temperature_inputs(job_id)
print("Example - For job id 1166, the temprature inputs are :", temperature_inputs)

