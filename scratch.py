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