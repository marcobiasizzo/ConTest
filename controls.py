import numpy as np

class Controls(object):
    def __init__(self, target, time_des, model, expected_tilt, feedback):
        self.target = target
        self.luff = np.array([0.0])
        self.lufb = np.array([0.0])
        self.lu = np.array([0.0])
        self.lerrInt = np.array([0.0])
        self.lerr = np.array([0.0])
        self.tdes = time_des
        self.ltimeu = np.array([0.0])
        self.mass = model.mass
        self.c_coeff = model.c_friction
        self.tilt_perc = expected_tilt
        self.i = 0

        if feedback == 'bang_bang':
            self.feedback = self.bang_bang
        elif feedback == 'P':
            self.feedback = self.P
        elif feedback == 'PI':
            self.feedback = self.PI
        elif feedback == 'PD':
            self.feedback = self.PD
        elif feedback == 'PID':
            self.feedback = self.PID
        elif feedback == '':
            self.feedback = self.no_feedback

    def feedforward(self, time):

        tacc = self.tdes * 0.2   # time for acceleration, equal to deceleration
        vdes = self.target / (self.tdes - tacc)

        Fg = 9.81 * self.mass * self.tilt_perc / 100.0

        if 0 < time < tacc:
            ff_force = Fg + vdes / tacc * self.mass
        elif tacc < time < self.tdes - tacc:
            ff_force = Fg
        elif self.tdes - tacc < time < self.tdes:
            ff_force = Fg - vdes / tacc * self.mass
        else:
            ff_force = Fg

        return ff_force

    def no_feedback(self, pos, t):
        return 0

    def bang_bang(self, pos, t):
        force = 2.0

        if pos - self.target < 0:
            u = force
        elif pos - self.target > 0:
            u = -force
        else:
            u = 0

        return u

    def P(self, pos, t):
        k = 2
        u = k*(self.target - pos)

        return u

    def PI(self, pos, t):
        kP = 2
        kI = 1

        if t > (0.8 * self.tdes):
            err = self.target - pos
            errInt = self.lerrInt[-1] + (self.lerr[-1] + err) * (t - self.ltimeu[-1]) / 2.0
            self.lerrInt = np.append(self.lerrInt, errInt)

            u = err * kP + errInt * kI

        return u

    def PD(self, pos, t):
        kP = 0.01
        kD = self.mass / self.c_coeff * kP

        if t > (0.8 * self.tdes):
            err = self.target - pos
            errDer = (err - self.lerr[-1]) / (t - self.ltimeu[-1])

            u = err * kP + errDer * kD

            self.lerr = np.append(self.lerr, err)

        return u

    def PID(self, pos, t):
        kD = 10
        Mult = 100
        kP = 2*Mult*self.c_coeff/self.mass * kD
        kI = (Mult*self.c_coeff/self.mass)**2 * kD


        if t > (0.8 * self.tdes):
            err = self.target - pos
            errDer = (err - self.lerr[-1]) / (t - self.ltimeu[-1])
            errInt = self.lerrInt[-1] + (self.lerr[-1] + err) * (t - self.ltimeu[-1]) / 2.0
            self.lerrInt = np.append(self.lerrInt, errInt)

            u = err * kP + errDer * kD + errInt * kI

            self.lerr = np.append(self.lerr, err)


            if t > self.i*1.0:
                self.i = self.i + 1


        return u


    def simulation_step(self, dt, pos):

        old_u = self.lu[-1]
        old_time = self.ltimeu[-1]

        t = old_time + dt
        uff = self.feedforward(t)

        # introduce the feedback
        if t > (0.8 * self.tdes):
            ufb = self.feedback(pos, t)
        else:
            ufb = 0

        u = uff + ufb

        sat_lim = 10
        if u > sat_lim:
            u = sat_lim
            ufb = u - uff
        if u < - sat_lim:
            u = - sat_lim
            ufb = u - uff

        self.luff = np.append(self.luff, uff)
        self.lufb = np.append(self.lufb, ufb)
        self.lu = np.append(self.lu, u)
        self.ltimeu = np.append(self.ltimeu, t)


