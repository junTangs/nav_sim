import math

from nav_sim.entity.sensor import Sensor
from nav_sim.utils.math_utils import distance, norm, recover_norm, clock_angle
from nav_sim.utils.kde_utils import density_map
import matplotlib.pyplot as plt
import pygame


class HumanSensor(Sensor):
    def __init__(self, config, name, scare_trans, coord_trans) -> None:
        super().__init__(name)
        self.config = config
        self.r = config["r"]
        self.density_map_width = config["map_width"]
        self.density_map_height = config["map_height"]
        self.use_density_map = config["density_map"]
        self.out_num = config["out_num"]
        self.is_sort = config["sort"]
        self.data = None
        self.scare_trans = scare_trans
        self.coord_trans = coord_trans

    def detect(self, robot_states: dict, obstacles: list, humans: list, goals: list) -> dict:
        self.data = {"results": [], "map": None, "pos": None}
        results = {"results": [], 'type': 'human', "map": None}
        map_samples = []
        xs = []
        ys = []
        for human in humans:
            dist = distance(human.x, human.y, robot_states["x"], robot_states["y"])
            if dist <= self.r:

                dx = (human.x - robot_states["x"])
                dy = (human.y - robot_states["y"])

                vx, vy = robot_states["vx"], robot_states["vy"]
                angle = math.radians(clock_angle(vx, vy, dx, dy))

                # map_samples.append((self.density_map_width // 2 + dist * self.density_map_width * 0.5 / self.r * math.sin(angle)))
                # map_samples.append((self.density_map_height//2+ dist*self.density_map_height*0.5/self.r*math.cos(angle)))

                map_samples.append((self.density_map_width // 2 + dx * self.density_map_width*0.5/ self.r))
                map_samples.append((self.density_map_height // 2 + dy * self.density_map_height*0.5/ self.r))


                results["results"].append([angle, dist, human.vx, human.vy, human.r, human.x,human.y])
                if len(results["results"]) >= self.out_num:
                    break

        if self.use_density_map:
            map = density_map(self.density_map_height, self.density_map_width, map_samples,1)
            map = map[::-1, :]
        else:
            map = None


        if self.is_sort:
            results["results"] = sorted(results["results"], key=lambda x: (x[2], x[1], x[0]))

        if len(results["results"]) < self.out_num:
            results["results"].extend([[0, 0, 0, 0, 0, 0, 0]] * (self.out_num - len(results["results"])))
        self.data["results"] = results["results"]

        results["map"] = map
        self.data["map"] = map
        self.data["pos"] = (robot_states["x"], robot_states["y"])
        return results

    def draw(self, screen):
        x, y = self.coord_trans(*self.data["pos"])
        r, _ = self.scare_trans(self.r, self.r)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), r, width=2)


Sensor.FACTORY["human"] = HumanSensor
