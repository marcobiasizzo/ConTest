import numpy as np
import sim_handler

class Car:
    def __init__(self, mass, c_friction, tilt_perc):
        self.mass = mass
        self.c_friction = c_friction
        self.tilt_perc = tilt_perc
        self.lpos = np.array([0.0])
        self.lvel = np.array([0.0])
        self.lacc = np.array([0.0])
        self.ltime = np.array([0.0])

    def dynamics(self, F_ext, vel):
        Fg = 9.81 * self.mass * self.tilt_perc / 100
        F_res = F_ext - self.c_friction * vel - Fg
        acc = F_res / self.mass

        return acc

    def simulation_step(self, dt, u):

        old_pos = self.lpos[-1]
        old_vel = self.lvel[-1]
        old_time = self.ltime[-1]

        t0 = old_time
        y0 = np.array([old_pos, old_vel])
        acc = self.dynamics(u, y0[1])
        dydt = lambda tfunc, yfunc: np.array([yfunc[1], self.dynamics(u, yfunc[1])])

        t, y = sim_handler.rungeKutta(t0, y0, dydt, dt)

        self.lpos = np.append(self.lpos, y[0])
        self.lvel= np.append(self.lvel, y[1])
        self.lacc = np.append(self.lacc, acc)
        self.ltime = np.append(self.ltime, t)

