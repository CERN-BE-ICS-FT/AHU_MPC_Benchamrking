import numpy as np
import casadi as cas
import parameters as param

class air_handling_unit:

    ##-------- Fluid Properties
    Cpa = param.Cpa

    ##-------- Speed to mass flow rate conversion
    b1 = param.b1
    b2 = param.b2

    ##-------- Fan heat gain model parameters
    c1 = param.c1
    c2 = param.c2
    c3 = param.c3

    def __init__(self, Cz, alpha, q, beta, w1, w2):

        ##-------- Zone model parameters
        self.Cz = Cz
        self.alpha = alpha
        self.q = q

        ##-------- Fan heat gain model parameters
        self.beta = beta

        ##-------- Mixing chamber weights update
        self.w1 = w1
        self.w2 = w2


    ##--------- Fan speed to mass flow rate of air
    def speed_to_massflow(self, u1):
        fan_mdot = self.b1 * u1 + self.b2
        return fan_mdot

    ##--------- Damper characteristics model
    def mixing_chamber_linear(self, u2, fan_mdot, Toa, Tza):
        alpha1 = self.w1 * ((fan_mdot * u2) / 100)
        alpha2 = self.w2 * ((fan_mdot * (100-u2)) / 100)
        Tma_next = (alpha1 * Toa + alpha2 * Tza) / fan_mdot
        return Tma_next


    ##--------- Fan heat gain model
    def fan_heat_gain(self, u1, fan_mdot, Tca):
        Tsa_next = Tca + ((self.beta * 1000 * (self.c1 * u1 ** 2 + self.c2 * u1 + self.c3)) / (self.Cpa * fan_mdot))
        return Tsa_next

    ##--------- Zone model
    def zone_model(self):

        ##--------- Casadi variables for defining dynamics
        global Tza_cas, mdot_cas, Tsa_cas, Toa_cas
        Tza_cas = cas.MX.sym('Tza')  # Zone temperature
        mdot_cas = cas.MX.sym('mdot')  # Mass flow rate of air
        Tsa_cas = cas.MX.sym('Tsa')  # Supply air temperature
        Toa_cas = cas.MX.sym('Toa')  # Outside air temperature

        ##--------- Zone Dynamics  (nonlinear ode)
        ode = [((mdot_cas * self.Cpa) / self.Cz) * (Tsa_cas - Tza_cas) + (self.alpha / self.Cz) * (Toa_cas - Tza_cas) + (self.q / self.Cz)]

        ##--------- Function definition ----> ode = f(Tza,mdot,Tsa,Toa)
        f = cas.Function('f', [Tza_cas, mdot_cas, Tsa_cas, Toa_cas], ode, ['Tza', 'mdot', 'Tsa', 'Toa'], ['ode'])
        return f

    ##--------- Integrator for the air handling unit model
    def zone_model_integrator(self, model, dt):

        ##--------- Create the integrator (Fixed step Runge-Kutta-4 integrator)
        M = 1  # RK4 steps per interval
        DT = dt / M  # Discretization step
        x_next = Tza_cas  # Mainly useful when you have multiple intervals between the shooting nodes.

        for j in range(M):
            k1 = model(x_next, mdot_cas, Tsa_cas, Toa_cas)
            k2 = model(x_next + DT / 2 * k1, mdot_cas, Tsa_cas, Toa_cas)
            k3 = model(x_next + DT / 2 * k2, mdot_cas, Tsa_cas, Toa_cas)
            k4 = model(x_next + DT * k3, mdot_cas, Tsa_cas, Toa_cas)
            x_next = x_next + DT / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

        F = cas.Function('F', [Tza_cas, mdot_cas, Tsa_cas, Toa_cas], [x_next], ['Tza_init', 'mdot', 'Tsa', 'Toa'], ['Tza_next'])
        return F

# TODO: Add the heater model
