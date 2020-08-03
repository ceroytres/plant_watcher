

class LuxModel():

    def __init__(self, m: float, b: float, R: float, Vin: float):

        self.m = m
        self.b = b
        self.R = R
        self.Vin = Vin

    def v2lux(self, Vout: float)->float:

        R_ldr = self.v2r(Vout)

        lux = self.r2lux(R_ldr)

        return lux

    def v2r(self, Vout: float)->float:

        R_ldr = self.R * (self.Vin/Vout - 1 )
        return max([R_ldr,0])

    def r2lux(self, R):

        lux = (R**self.m) * (10 ** self.b)

        return lux






        