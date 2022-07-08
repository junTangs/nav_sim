STATES ={}


from nav_sim.utils.state.d_sensor_state import DistSensorState
from nav_sim.utils.state.joint_state import JointState

STATES['d_sensor'] = DistSensorState
STATES['joint'] = JointState