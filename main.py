from ahu import air_handling_unit
from mpc import model_predictive_controller
import parameters as param
from casadi import *
import time
import signal 
from utils_v2 import calculate_inputs
from config_v2 import TIMEOUT
import argparse
import csv

##------  Model intialization
ahu_model = air_handling_unit(
    param.Cz, param.alpha, param.q, param.gamma_fan, param.w1, param.w2
)
zone_model = ahu_model.zone_model()
zone_model_discrete = ahu_model.zone_model_integrator(zone_model, param.dt_mpc)

##------  Model predictive controller intialization
opti = Opti()  # Intialize Opti stack
mpc = model_predictive_controller(
    opti, param.dt_mpc, param.N_mpc, param.Th_max, param.Tc_min, ahu_model
)
mpc.define_variables_and_parameters()
mpc.set_constraints()
mpc.set_objective(param.r4)

##------ Solver related settings
# Warm start solver
sol_prev = []  # current solution
warm_start = False

##------  Solver specific settings
p_opts = {"expand": True, "ipopt.print_level": 0, "print_time": 0}
s_opts = {"max_iter": 1000}
opti.solver("ipopt", p_opts, s_opts)

# Set the parameters to use inside the function 
Tsa_min = 16

# This is the function that will be called when the alarm goes off
def handle_alarm(signum, frame):
    raise TimeoutError()
    
# Set the function to be called on alarm
signal.signal(signal.SIGALRM, handle_alarm)

def mpc_function(job_id: int):
    Toa, temperature_inputs, actuator_inputs = calculate_inputs(job_id)
    # Start the alarm
    signal.alarm(TIMEOUT)  # You want the function to stop after timeout
    try:
        start = time.time()
        init_cond = temperature_inputs
        actuators = actuator_inputs
        sol = mpc.solve(
        init_cond, actuators, Toa, Tsa_min, warm_start, sol_prev
        )
        end = time.time()
        total_time = end - start
        signal.alarm(0)
        full_array = np.concatenate(([Toa], temperature_inputs, actuator_inputs, [total_time]))
        print('Solver succeeded...')
        print('Toa, Tza, Tma, Tha, Tca, Tsa, omega,  dout, Total_time')
        print(full_array)
        return full_array
    except RuntimeError:
        full_array = np.zeros(9)
        full_array[0] = Toa
        full_array[1:6] = temperature_inputs
        full_array[6:8] = actuator_inputs
        full_array[-1] = -300
        print('Runtime error due to infeaseablity in constraints etc...', full_array)
        return full_array
    except TimeoutError:
        full_array = np.zeros(9)
        full_array[0] = Toa
        full_array[1:6] = temperature_inputs
        full_array[6:8] = actuator_inputs
        full_array[-1] = -700
        print('Function execution took too long, stopping...', full_array)
        return full_array

# mpc_function(job_id=1166)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an integer job_id for the mpc_function.")
    parser.add_argument("job_id", type=int, help="An integer job_id for the mpc_function.")
    args = parser.parse_args()
    
    result = mpc_function(args.job_id)
    
    # with open(f'results/result_{args.job_id}.csv', 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     csvwriter.writerow(result)
    