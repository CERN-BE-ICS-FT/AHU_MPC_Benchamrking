import numpy as np

##-------- Setting prediction horizon of MPC
minutes_dt_mpc = 8
mpc_hours = 16
T_mpc = 3600 * mpc_hours
dt_mpc = 60 * minutes_dt_mpc
N_mpc = int(T_mpc / dt_mpc)  # number of control intervals = 120 (currently)

##------  For Mixing Chamber
gamma_ma = 0.95  # Forgetting factor
P_ma = np.identity(2)
update_time_mixing_chamber = 1
w1 = 1
w2 = 1

##------  For Fan Heat Gain
gamma_fan = 0.95  # Forgetting factor
P_fan = 1
update_time_fan_heat_gain = 1

##------  For Return Air Heat Gain
gamma_return = 0.95  # Forgetting factor
P_return = 1
update_time_return_heat_gain = 1

##------ Bounds on the optimization variables
u1_min, u1_max = 1, 100  # Bounds on mass flow rate of air
u2_min, u2_max = 10, 100  # Bounds on the opening of outside air damper

xza_min, xza_max = 17, 26  # Bounds on zone air temperature
xsa_min, xsa_max = 17, 30  # Bounds on supply air temperature
Tsa_min = 16 # Bounds on supply air temperature defined externally

u1_dot = 10  # Rate of change constraint for fan speed
u2_dot = 15  # Rate of change constraint for dampers

xca_dot = 4  # Rate of change constraint for cooling coil
xha_dot = 4  # Rate of change constraint for heating coil

s_min, s_max = 0, 20  # Slack variables for zone air temperature
s1_min, s1_max = 0, 10  # Slack variables for supply air temperature
s2_min, s2_max = 0, 10  # Slack variables for cooled air temperature
s3_min, s3_max = 0, 10  # Slack variables for heated air temperature

##------ Weights of the objective function

##------ Setup the objective of the optimization program
r1 = 1
r2 = 1
r3 = 1
r4 = 0.0001
r5 = 0.0001
r6 = 80
ref = 20

##-------- Air Handling Unit --------##
# Fluid Properties
Cpa = 1.005 * 1000

# Speed to mass flow rate conversion
b1 = 0.08610304
b2 = 5.69558154

# Fan heat gain model parameters
c1 = 9.70520356e-04
c2 = 3.41976882e-02
c3 = 1.25761215e00

# Cooling Coil
Tc_min = 12
eta_cool = 0.9
COP_cool = 2.8

# Heating Coil
Th_max = 30
eta_heat = 0.9
COP_heat = 0.9

# Average Filter Length
filter_len = 5

# Zone parameters
Cz = 137629731.2718317
alpha = -4.782261326777122e-09
q = 23000
