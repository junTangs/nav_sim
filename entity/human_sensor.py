import math

from nav_sim.entity.sensor import Sensor
from nav_sim.utils.math_utils import distance,norm,recover_norm,clock_angle
from nav_sim.utils.kde_utils import density_map
import matplotlib.pyplot as plt
class HumanSensor(Sensor):
    def __init__(self, config, name, scare_trans, coord_trans) -> None:
        super().__init__(name)
        self.config = config
        self.r = config["r"]
        self.density_map_width  = config["map_width"]
        self.density_map_height  = config["map_height"]
        self.data = None
        self.scare_trans = scare_trans
        self.coord_trans = coord_trans

    def detect(self, robot_states: dict, obstacles: list, humans: list, goals: list) -> dict:
        self.data = {"results": [],"map":None}
        results = {"results": [],'type':'human',"map":None}
        map_samples = []
        xs = []
        ys = []
        for human in humans:
            dist = distance(human.x,human.y,robot_states["x"],robot_states["y"])
            if dist <= self.r:

                dx = (human.x - robot_states["x"])
                dy = (human.y - robot_states["y"])
                x = norm(dx,self.r,-self.r)
                y = norm(dy,self.r,-self.r)

                vx,vy = robot_states["vx"],robot_states["vy"]
                angle = math.radians(clock_angle(vx,vy,dx,dy))
                map_samples.append((self.density_map_width // 2 + dist * self.density_map_width * 0.5 / self.r * math.sin(angle)))
                map_samples.append((self.density_map_height//2+ dist*self.density_map_height*0.5/self.r*math.cos(angle)))



                results["results"].append([x,y])

        map = density_map(self.density_map_height,self.density_map_width,map_samples,self.r*12.8)
        map = map[::-1,:]
        self.data["results"] = results["results"]
        results["map"] = map
        self.data["map"] = map
        return results


Sensor.FACTORY["human"] = HumanSensor



