The feedforward controller has been tuned considering the 10% of tilt and the absence of friction
Feedforward condtroller 
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/1_exact_tilt_no_friction_ff.gif)

If the real tilt is differenent from the expected one, e.g. 15% tilt, the feedforard controller will fail

And a simple controller like the BangBang or the Proportional will not work in this case
BangBang - with 15% tilt
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/2_wrong_tilt_no_friction_ff.gif)

Proportional - with 15% tilt
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/3_wrong_tilt_no_friction_bb.gif)

PID controller - with 15% tilt and friction
![alt text](https://github.com/marcobiasizzo/ConTest/blob/master/Figures/7_wrong_tilt_friction_PID.gif)
