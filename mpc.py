import parameters as param

class model_predictive_controller:
    ##-------- Bounds on the optimization variables
    u1_min, u1_max = param.u1_min, param.u1_max  # Bounds on mass flow rate of air
    u2_min, u2_max = param.u2_min, param.u2_max  # Bounds on the opening of outside air damper
    xza_min, xza_max = param.xza_min, param.xza_max   # Bounds on zone air temperature
    xsa_max =  param.xsa_max  # Bounds on supply air temperature
    u1_dot = param.u1_dot  # Rate of change constraint for fan speed
    u2_dot = param.u2_dot  # Rate of change constraint for the dampers
    xca_dot = param.xca_dot  # Rate of change constraint for the cooling coil
    xha_dot = param.xha_dot  # Rate of change constraint for the heating coil
    s_min, s_max = param.s_min, param.s_max  # Slack variables for zone air temperature
    s1_min, s1_max = param.s1_min, param.s1_max  # Slack variables for supply air temperature
    s2_min, s2_max = param.s2_min, param.s2_max  # Slack variables for cooled air temperature
    s3_min, s3_max = param.s3_min, param.s3_max  # Slack variables for heated air temperature

    def __init__(self, opti, dt, N, xh_max, xc_min, ahu_model):

        ##-------- Prediction horizon for model predictive controller
        self.opti = opti
        self.dt = dt
        self.N = N
        ##-------- Capacity of the heating and cooling coil (must be consistent with the supply temperature bounds)
        self.xh_max = xh_max
        self.xc_min = xc_min
        ##--------
        self.ahu_model = ahu_model

    ##--------  Define the variables and parameters involved in the optimization program
    def define_variables_and_parameters(self):

        ##-------- Variables
        global xza, xma, xha, xca, xsa, u1, u2, s, s1, s2, s3, xoa, u1_init, u2_init, xz_init, xmix_init, xh_init, xc_init, xs_init, xsa_min

        ##-------- State variables
        xza = self.opti.variable(1, self.N + 1)  # Zone air temperature
        xma = self.opti.variable(1, self.N + 1)  # Mix air temperature
        xha = self.opti.variable(1, self.N + 1)  # Heated air temperature (off coil temperature)
        xca = self.opti.variable(1, self.N + 1)  # Cooled air temperature (off coil temperature)
        xsa = self.opti.variable(1, self.N + 1)  # Supply air temperature

        ##-------- Input variables
        u1 = self.opti.variable(1, self.N)  # Mass flow rate
        u2 = self.opti.variable(1, self.N)  # Outside air damper opening

        ##-------- Slack variables
        s = self.opti.variable(1, self.N)  # Slack variable for zone temperature
        s1 = self.opti.variable(1, self.N)  # Slack variable for
        s2 = self.opti.variable(1, self.N)  # Slack variable for
        s3 = self.opti.variable(1, self.N)  # Slack variable for

        ##-------- Parameter of the optimization program
        xoa = self.opti.parameter(1, self.N)  # Outside air temeprature (Disturbance variable)
        xsa_min = self.opti.parameter(1, self.N)  # Time varying bound on the supply temperature
        u1_init = self.opti.parameter()  # Variable to impose rate of change constraint on variable u1[0]
        u2_init = self.opti.parameter()  # Variable to impose rate of change constraint on variable u2[0]

        xz_init = self.opti.parameter()  # Initial condition for zone temperature
        xmix_init = self.opti.parameter()  # Initial condition for mixed air temperature
        xh_init = self.opti.parameter()  # Initial condition for heated air temperature
        xc_init = self.opti.parameter()  # Initial condition for cooled air temperature
        xs_init = self.opti.parameter()  # Initial condition for supply air temperature

    def set_constraints(self):

        ##-------- Setup the optimization program
        for k in range(self.N):
            ##-------- Zone Dynamics
            fan_mdot = self.ahu_model.speed_to_massflow(u1[k])
            zone_model = self.ahu_model.zone_model()
            zone_model_discrete = self.ahu_model.zone_model_integrator(zone_model, self.dt)
            self.opti.subject_to(xza[k + 1] == zone_model_discrete(xza[k], fan_mdot, xsa[k], xoa[k]))

            ##-------- Mixing chamber dynamics u2, fan_mdot, Toa, Tza
            self.opti.subject_to(xma[k + 1] == self.ahu_model.mixing_chamber_linear(u2[k], fan_mdot, xoa[k], xza[k]))

            ## Heating coil
            self.opti.subject_to(xha[k + 1] >= xma[k + 1])
            self.opti.subject_to(xha[k + 1] <= self.xh_max + s2[k])

            ## Cooling coil
            self.opti.subject_to(xca[k + 1] <= xha[k + 1])
            self.opti.subject_to(xca[k + 1] >= self.xc_min - s3[k])

            ## Fan coil
            self.opti.subject_to(xsa[k + 1] == self.ahu_model.fan_heat_gain(u1[k], fan_mdot, xca[k + 1]))

            ## Actuator constraints
            self.opti.subject_to(u1[k] >= self.u1_min)
            self.opti.subject_to(u1[k] <= self.u1_max)

            self.opti.subject_to(u2[k] >= self.u2_min)
            self.opti.subject_to(u2[k] <= self.u2_max)

            ## Supply temperature constraints
            self.opti.subject_to(xsa[k+1] >= xsa_min[k] - s1[k])
            self.opti.subject_to(xsa[k+1] <= self.xsa_max + s1[k])

            ## State constraints
            self.opti.subject_to(xza[k+1] >= self.xza_min - s[k])
            self.opti.subject_to(xza[k+1] <= self.xza_max + s[k])

            ## Slack constraints
            self.opti.subject_to(s[k] >= self.s_min)
            self.opti.subject_to(s[k] <= self.s_max)

            self.opti.subject_to(s1[k] >= self.s1_min)
            self.opti.subject_to(s1[k] <= self.s1_max)

            self.opti.subject_to(s2[k] >= self.s2_min)
            self.opti.subject_to(s2[k] <= self.s2_max)

            self.opti.subject_to(s3[k] >= self.s3_min)
            self.opti.subject_to(s3[k] <= self.s3_max)

        ## Rate of change constraints for cooling and heating coil
        for k in range(self.N):
            self.opti.subject_to(xha[k + 1] - xha[k] <= self.xha_dot)
            self.opti.subject_to(xha[k + 1] - xha[k] >= -self.xha_dot)
            self.opti.subject_to(xca[k + 1] - xca[k] <= self.xca_dot)
            self.opti.subject_to(xca[k + 1] - xca[k] >= -self.xca_dot)


        ## Rate of change constraints for the dampers
        for k in range(self.N - 1):
            self.opti.subject_to(u2[k + 1] - u2[k] <= self.u2_dot)
            self.opti.subject_to(u2[k + 1] - u2[k] >= -self.u2_dot)

        self.opti.subject_to(u2[0] - u2_init <= self.u2_dot)
        self.opti.subject_to(u2[0] - u2_init >= -self.u2_dot)

        ## Rate of change constraints for the mass flow rate
        for k in range(self.N - 1):
            self.opti.subject_to(u1[k + 1] - u1[k] <= self.u1_dot)
            self.opti.subject_to(u1[k + 1] - u1[k] >= -self.u1_dot)

        self.opti.subject_to(u1[0] - u1_init <= self.u1_dot)
        self.opti.subject_to(u1[0] - u1_init >= -self.u1_dot)

        ## Terminal constraints are already taken care of

        ## Initial Conditions
        self.opti.subject_to(xza[0] == xz_init)
        self.opti.subject_to(xma[0] == xmix_init)
        self.opti.subject_to(xsa[0] == xs_init)
        self.opti.subject_to(xha[0] == xh_init)
        self.opti.subject_to(xca[0] == xc_init)

    def set_objective(self, r4):
        ##-------- Setup the objective of the optimization program
        J = 0
        r1 = param.r1
        r2 = param.r2
        r3 = param.r3
        r5 = param.r5
        r6 = param.r6
        ref = 20

        ##-------- Speed to mass flow rate conversion
        b1 = param.b1
        b2 = param.b2

        ##-------- Fan heat gain model parameters
        c1 = param.c1
        c2 = param.c2
        c3 = param.c3

        ##-------- Cooling Coil
        eta_cool = param.eta_cool
        COP_cool = param.COP_cool
        Cpa = 1.005

        ##-------- Heating Coil
        eta_heat = param.eta_heat
        COP_heat = param.COP_heat


        for k in range(self.N):
            J = J + r1 * (c1 * u1[k] ** 2 + c2 * u1[k] + c3) + r2 * (1 / (eta_heat * COP_heat)) * ((b1 * u1[k] + b2) * Cpa * (xha[k + 1] - xma[k + 1])) + r3 * (1 / (eta_cool * COP_cool)) * ((b1 * u1[k] + b2) * Cpa * (xha[k + 1] - xca[k + 1])) + r4 * (xca[k + 1] - xca[k]) ** 2 + r5 * (xza[k + 1] - ref) ** 2 + r6 * s[k]**2 + r6 * s1[k]**2 + r6 * s2[k]**2 + r6 * s3[k]**2

        self.opti.minimize(J)  # Set J as the objective function


    def solve(self, init_cond, slewrate_init, Toa, Tsa_min , warm_start, sol_prev):

        ##-------- Initial condition
        self.opti.set_value(xz_init, init_cond[0])
        self.opti.set_value(xmix_init, init_cond[1])
        self.opti.set_value(xh_init, init_cond[2])
        self.opti.set_value(xc_init, init_cond[3])
        self.opti.set_value(xs_init, init_cond[4])

        ##-------- Rate of change constraint
        self.opti.set_value(u1_init, slewrate_init[0])
        self.opti.set_value(u2_init, slewrate_init[1])

        ##-------- Disturbance variable
        self.opti.set_value(xoa, Toa)
        self.opti.set_value(xsa_min, Tsa_min)

        ##-------- Initialize the solution of the solver
        if warm_start == True:
            self.opti.set_initial(sol_prev.value_variables())
        else:
            self.opti.set_initial(u1, 1)
            self.opti.set_initial(u2, 10)

        sol = self.opti.solve()
        status = self.opti.return_status()

        u1_open_loop = sol.value(u1)
        u2_open_loop = sol.value(u2)
        xmix_open_loop = sol.value(xma)
        xh_open_loop = sol.value(xha)
        xc_open_loop = sol.value(xca)
        xs_open_loop = sol.value(xsa)
        xz_open_loop = sol.value(xza)

        return [status, u1_open_loop[0], u2_open_loop[0], xmix_open_loop[1], xh_open_loop[1], xc_open_loop[1],
                xs_open_loop[1],xz_open_loop[1], sol]