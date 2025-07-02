import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import patches

green_mpg = '#006c66'
grey_mpg = '#eeeeee'
orange_mpg = '#ef7c00'
dark_blue = '#00b1ea'
blue_mpg = '#0179A0'

def plot_q_time(quantity, time, name, label=None):
    fig, ax = plt.subplots()
    ax.plot(time, quantity)
    ax.set_xlabel('time (s)')
    ax.set_ylabel(label)
    fig.show()
    fig.savefig('Figures/' + name + '.png')

def plot_force(model, control, name, label=None):

    tilt_angle = np.asin(model.tilt_perc / 100)
    g_value = model.mass * 9.81 * np.sin(tilt_angle)
    uff = control.luff
    ufb = control.lufb
    utime = control.ltimeu

    fig, ax = plt.subplots(figsize=(5, 3))
    linew = 4
    ax.plot(utime, uff, color=blue_mpg,linewidth=linew, label='Feedback')
    ax.plot(utime, ufb, color=dark_blue,linewidth=linew, label='Feedforward')
    ax.hlines(g_value,xmin=min(utime),xmax=max(utime),colors=orange_mpg,linewidth=linew,linestyles='--',label='Weight')
    ax.legend()
    ax.set_xlabel('time (s)')
    ax.set_ylabel('Force (N)')

    ax.set_yticks([])
    ax.set_xticks([])
    secax = ax.secondary_xaxis(0, transform=ax.transData)
    # secax.set_xticks([])

    fig.show()
    fig.savefig('Figures/' + name + '.svg')

def generate_video(model, control, name):
    pos = model.lpos
    time = model.ltime
    vel = model.lvel
    t_end = time[-1]

    uff = control.luff
    ufb = control.lufb
    utime = control.ltimeu

    fig, ax = plt.subplots(figsize=(12, 4))

    f_rate = 30.0
    N_frames = int(t_end * f_rate)
    artists = []

    tilt_angle = np.asin(model.tilt_perc/100)
    tilt_deg = tilt_angle / np.pi * 180.0

    Rwheels = 0.1

    # fixed elements
    # color area under
    x_start = -5
    path_start = x_start * np.tan(tilt_angle)
    # space for wheels
    path_start = path_start - 2*Rwheels * np.cos(tilt_angle)
    x_end = 15
    path_end = x_end * np.tan(tilt_angle)
    # space for wheels
    path_end = path_end - 2*Rwheels * np.cos(tilt_angle)
    ax.fill_between([-5, 15], [path_start, path_end], [-2, -2], color=grey_mpg)

    # target point
    width = 2
    height = 1
    sensorDim = 0.5

    cPosx = 0 + 10 * np.cos(tilt_angle)
    cPosy = 0 + 10 * np.sin(tilt_angle)
    # increase distance
    cPosx = cPosx - (height + sensorDim) * np.sin(tilt_angle)
    cPosy = cPosy + (height + sensorDim) * np.cos(tilt_angle)
    c = patches.Circle((cPosx, cPosy), Rwheels*3, color=green_mpg, alpha=0.4)
    target = ax.add_patch(c)
    cPosx = 0 + 10 * np.cos(tilt_angle)
    cPosy = 0 + 10 * np.sin(tilt_angle)
    # increase distance
    cPosx = cPosx - (height + sensorDim) * np.sin(tilt_angle)
    cPosy = cPosy + (height + sensorDim) * np.cos(tilt_angle)
    c = patches.Circle((cPosx, cPosy), Rwheels*2, color='white')
    target = ax.add_patch(c)
    cPosx = 0 + 10 * np.cos(tilt_angle)
    cPosy = 0 + 10 * np.sin(tilt_angle)
    # increase distance
    cPosx = cPosx - (height + sensorDim) * np.sin(tilt_angle)
    cPosy = cPosy + (height + sensorDim) * np.cos(tilt_angle)
    c = patches.Circle((cPosx, cPosy), Rwheels, color=green_mpg, alpha=0.4)
    target = ax.add_patch(c)

    y_pos = 3.5
    ax.arrow(-3, y_pos, 1, 0, width=0.1, length_includes_head=True, color=dark_blue)
    ax.text(-1.5, y_pos, 'Feedforward', ha='left', va='center')

    y_pos = 3.0
    ax.arrow(-3, y_pos, 1, 0, width=0.1, length_includes_head=True, color=blue_mpg)
    ax.text(-1.5, y_pos, 'Feedback', ha='left', va='center')

    y_pos = 2.5
    ax.arrow(-3, y_pos, 1, 0, width=0.1, length_includes_head=True, color=orange_mpg)
    ax.text(-1.5, y_pos, 'Weight', ha='left', va='center')

    for i in range(N_frames):
        frame_time = i * 1.0/f_rate
        idx = (np.abs(time - frame_time)).argmin()
        frame_pos = pos[idx]

        # bottom left corner
        xpos = (frame_pos-width) * np.cos(tilt_angle)
        ypos = (frame_pos-width) * np.sin(tilt_angle)

        # Create a Rectangle patch
        r = patches.Rectangle((xpos, ypos), width, height, angle=tilt_deg, rotation_point='xy',
                              color=green_mpg)
        rect = ax.add_patch(r)
        elemSeq = (rect, )

        # position of first wheel
        cPosx = xpos + width*0.2 * np.cos(tilt_angle)
        cPosy = ypos + width*0.2 * np.sin(tilt_angle)
        # separate from base
        cPosx = cPosx + Rwheels * np.sin(tilt_angle)
        cPosy = cPosy - Rwheels * np.cos(tilt_angle)
        c = patches.Circle((cPosx, cPosy), Rwheels, color=green_mpg)
        circ1 = ax.add_patch(c)

        elemSeq = elemSeq + (circ1,)

        # position of second wheel
        cPosx = xpos + width * 0.8 * np.cos(tilt_angle)
        cPosy = ypos + width * 0.8 * np.sin(tilt_angle)
        # separate from base
        cPosx = cPosx + Rwheels * np.sin(tilt_angle)
        cPosy = cPosy - Rwheels * np.cos(tilt_angle)
        c = patches.Circle((cPosx, cPosy), Rwheels, color=green_mpg)
        circ2 = ax.add_patch(c)

        elemSeq = elemSeq + (circ2,)


        # draw sensor
        x_sensor = xpos + width * np.cos(tilt_angle) - height * np.sin(tilt_angle)
        y_sensor = ypos + width * np.sin(tilt_angle) + height * np.cos(tilt_angle)
        sensor = ax.arrow(x_sensor, y_sensor, -0.5*np.sin(tilt_angle), 0.5*np.cos(tilt_angle),
                            width=0.1, length_includes_head=True, color=green_mpg, head_width=0)
        elemSeq = elemSeq + (sensor,)

        # common factor for forces
        Kmult = 0.8

        draw_friction = 0
        if draw_friction:
            # draw friction
            # center of lower side
            x_friction = xpos+width/2*np.cos(tilt_angle)
            y_friction = ypos+width/2*np.sin(tilt_angle)
            # move lower
            x_friction = x_friction + 0.2*np.sin(tilt_angle)
            y_friction = y_friction - 0.2*np.cos(tilt_angle)
            fric_value = Kmult * vel[idx] * model.c_friction
            if abs(fric_value) > 0:
                friction = ax.arrow(x_friction, y_friction, -fric_value*np.cos(tilt_angle), -fric_value*np.sin(tilt_angle), width=0.1,
                                    length_includes_head=False, color=orange_mpg)

                elemSeq = elemSeq + (friction, )

        # draw Fg
        x_g = xpos + width / 2 * np.cos(tilt_angle)
        y_g = ypos + width / 2 * np.sin(tilt_angle)
        # move to center of rectangle
        x_g = x_g + height / 2 * np.sin(tilt_angle)
        y_g = y_g + height / 2 * np.cos(tilt_angle)
        # draw only along plane
        g_value = Kmult * model.mass * 9.81 * np.sin(tilt_angle)
        Fg = ax.arrow(x_g, y_g, -g_value * np.cos(tilt_angle), -g_value * np.sin(tilt_angle),
                            width=0.1,
                            length_includes_head=False, color=orange_mpg)

        elemSeq = elemSeq + (Fg, )

        # draw feedforward
        # move to right side
        x_force = xpos + width * np.cos(tilt_angle)
        y_force = ypos + width * np.sin(tilt_angle)
        # move up a bit
        x_force = x_force - height * 0.66 * np.sin(tilt_angle)
        y_force = y_force + height * 0.66 * np.cos(tilt_angle)
        force_value = Kmult * uff[idx]
        force_ff = ax.arrow(x_force, y_force, force_value * np.cos(tilt_angle), force_value * np.sin(tilt_angle),
                            width=0.1,
                            length_includes_head=False, color=dark_blue)

        elemSeq = elemSeq + (force_ff, )

        # draw feedback
        # move to right side
        x_force = xpos + width * np.cos(tilt_angle)
        y_force = ypos + width * np.sin(tilt_angle)
        # move up a bit
        x_force = x_force - height * 0.33 * np.sin(tilt_angle)
        y_force = y_force + height * 0.33 * np.cos(tilt_angle)
        force_value = Kmult * ufb[idx]
        if abs(force_value) > 0:
            force_fb = ax.arrow(x_force, y_force, force_value * np.cos(tilt_angle), force_value * np.sin(tilt_angle),
                                width=0.1,
                                length_includes_head=False, color=blue_mpg)
            elemSeq = elemSeq + (force_fb, )

        artists.append(elemSeq)


    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-4, 14)
    ax.set_ylim(-1, 4)

    ax.set_axis_off()

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=1/f_rate*1000)
    fig.show()

    ani.save('Figures/' + name + '.gif')
