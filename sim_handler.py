
def sim_handler(model, control, t_end, dt):
    t = 0

    while t < t_end:
        model.simulation_step(dt, control.lu[-1])
        control.simulation_step(dt, model.lpos[-1])

        t = t + dt

def rungeKutta(t0, y0, dydt, h):
    # initial conditions t0, y0
    # time derivative of y dydt
    # time integration step h

    "Apply Runge Kutta Formulas to find next value of y"
    k1 = h * dydt(t0, y0)
    k2 = h * dydt(t0 + 0.5 * h, y0 + 0.5 * k1)
    k3 = h * dydt(t0 + 0.5 * h, y0 + 0.5 * k2)
    k4 = h * dydt(t0 + h, y0 + k3)

    # Update next value of y
    y = y0 + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    # Update next value of x
    t = t0 + h

    return t, y
