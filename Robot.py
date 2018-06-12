
class Robot:
	def __init__(self):
		self.x = 0; self.y = 0; self.th = 0
		self.dx = 0; self.dy = 0; self.dth = 0
		self.kp_u = 0; self.kp_w = 0; self.ki_u = 0; self.ki_w = 0; self.kd_u = 0; self.kd_w = 0
		self.id = 3
		self.u = 0; self.w = 0
		self.straegy = ''
		self.control_option = 4