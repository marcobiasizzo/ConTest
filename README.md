The goal is to move the cart in the position where the antenna is at the center of the target.

A feedforwad control is applied to move the cart.
In the first example the model applied for the feedforward corresponds to the simulation.
In the other example a different tilt angle is considered.

The feedforward controller has been tuned considering the 10% of tilt and the absence of friction
Feedforward condtroller 
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/1_exact_tilt_no_friction_ff.gif)

If the real tilt is differenent from the expected one, e.g. 15% tilt, the feedforard controller will fail

And a simple controller like the BangBang or the Proportional will not work in this case
Feedforward - with 15% tilt
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/2_wrong_tilt_no_friction_ff.gif)

BangBang - with 15% tilt
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/3_wrong_tilt_no_friction_bb.gif)

Proportional - with 15% tilt
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/4_wrong_tilt_no_friction_P.gif)

The PID controller is necessary in this case to obtain the convergence.
It also works if the friction is introduced in the simulation.

PID controller - with 15% tilt and friction
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/7_wrong_tilt_friction_PID.gif)
