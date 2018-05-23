class axis:
	def __init__(self):
		self.h = 0
		self.v = 0

def joystick_control(joy):
	leftAxis = axis()
	rightAxis = axis()
	leftAxis.h = joy.axes[0];
	leftAxis.v = joy.axes[1];
	l2 = joy.axes[2];
	rightAxis.h = joy.axes[3];
	rightAxis.v = joy.axes[4];
	r2 = joy.axes[5];

	u = - (l2 - 1)/3.8 + (r2 - 1)/3.8;
	w = leftAxis.h * 5;
	return u,w