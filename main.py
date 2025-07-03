import car
import controls
import sim_handler
import visualize
from scipy import signal
from matplotlib import pyplot as plt

mass = 1
tilt_model = 10
target = 10

t_des = 3
t_end = 5
dt = 0.001

cSimNameList = [
    '1_exact_tilt_no_friction_ff',
    '2_wrong_tilt_no_friction_ff',
    '3_wrong_tilt_no_friction_bb',
    '4_wrong_tilt_no_friction_P',
    '5_wrong_tilt_no_friction_PI',
    '6_wrong_tilt_friction_PI',
    '7_wrong_tilt_friction_PID',
]

nSim = 2
cSimName = cSimNameList[nSim-1]

if cSimName == '1_exact_tilt_no_friction_ff':
    tilt_real = tilt_model
    c_coeff = 0.0
    feedback = ''
    t_end = 5
elif cSimName in ['2_wrong_tilt_no_friction_ff', '3_wrong_tilt_no_friction_bb', '4_wrong_tilt_no_friction_P', '5_wrong_tilt_no_friction_PI']:
    tilt_real = tilt_model * 1.5
    c_coeff = 0.0
    if cSimName == '2_wrong_tilt_no_friction_ff':
        feedback = ''
        t_end = 10
    if cSimName == '3_wrong_tilt_no_friction_bb':
        feedback = 'bang_bang'
        t_end = 10
    elif cSimName == '4_wrong_tilt_no_friction_P':
        feedback = 'P'
        t_end = 10
    elif cSimName == '5_wrong_tilt_no_friction_PI':
        feedback = 'PI'
        t_end = 10
elif cSimName in ['6_wrong_tilt_friction_PI', '7_wrong_tilt_friction_PID']:
    tilt_real = tilt_model * 1.5
    c_coeff = 0.01
    if cSimName == '6_wrong_tilt_friction_PI':
        feedback = 'PI'
    elif cSimName == '7_wrong_tilt_friction_PID':
        feedback = 'PID'
    t_end = 10

if __name__ == '__main__':
    Car = car.Car(mass, c_coeff, tilt_real)
    Control = controls.Controls(target, t_des, Car, tilt_model, feedback)

    # sys = signal.TransferFunction([1], [mass, c_coeff, 0])
    # w, mag, phase = signal.bode(sys)
    # fig, ax = plt.subplots(figsize=(12, 3))
    # ax.semilogx(w, mag)  # Bode magnitude plot
    # # plt.semilogx(w, phase)  # Bode phase plot
    # fig.show()

    sim_handler.sim_handler(Car, Control, t_end, dt)

    visualize.plot_force(Car, Control, cSimName)

    # visualize.plot_q_time(Car.lpos, Car.ltime, cSimName, 'Position (m)')
    #
    # visualize.plot_q_time(Control.lu, Control.ltimeu, cSimName, 'Control (N)')
    #
    visualize.generate_video(Car, Control, cSimName)
