STATES ={}


from nav_sim.utils.state.d_sensor_state import DistSensorState
from nav_sim.utils.state.joint_state import JointState
from nav_sim.utils.state.d_sensor_state_16 import DistSensorState16

STATES['d_sensor'] = DistSensorState
STATES['joint'] = JointState
STATES['d_sensor_16'] = DistSensorState16