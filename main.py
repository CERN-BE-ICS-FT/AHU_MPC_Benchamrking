from ahu import air_handling_unit
from mpc import model_predictive_controller
import parameters as param
from casadi import *
import time
import signal 
from utils import calculate_temperature_inputs
from config import TIMEOUT

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
Tsa_min, omega_init, dout_init = 16, 1, 10

# This is the function that will be called when the alarm goes off
def handle_alarm(signum, frame):
    raise TimeoutError()
    
# Set the function to be called on alarm
signal.signal(signal.SIGALRM, handle_alarm)

def mpc_function(job_id):
    temperature_inputs = calculate_temperature_inputs(job_id)
    # Start the alarm
    signal.alarm(TIMEOUT)  # You want the function to stop after timeout
    try:
        start = time.time()
        init_cond = temperature_inputs[:5]
        actuators = np.array([omega_init, dout_init])
        sol = mpc.solve(
        init_cond, actuators, temperature_inputs[5], Tsa_min, warm_start, sol_prev
        )
        solver_status = sol[0]
        omega_simulation = sol[1]
        dout = sol[2]
        drec = 100 - dout
        Tma = sol[3]
        Tha = sol[4]
        Tca = sol[5]
        Tsa = sol[6]
        end = time.time()
        total_time = end - start
        print('Solver Status', solver_status)
        print('Fan Speed ::', omega_simulation, 'OA Damper ::', dout, 'RA Damper ::', drec, 'MA Temp ::', Tma, 'HA Temp ::',
              Tha, 'CA Temp ::', Tca, 'SA Temp ::', Tsa, 'Total time ::', total_time)
        signal.alarm(0)
        return total_time
    except TimeoutError:
        print('Function execution took too long, stopping...')
        return TIMEOUT

mpc_function(job_id=1166)