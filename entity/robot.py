
from pygame.sprite import Sprite
import math
from nav_sim.utils.math_utils import rotate



class Robot(Sprite):
    def __init__(self,config,dt) -> None:
        super().__init__()
        self.config = config
        self.x = 0
        self.y = 0
        self.r = 0
        
        # inherit parameters
        self.vx = 0 # m/s
        self.vy = 0 # m/s
        self.v = 0 # m/s
        self.omega = 0 # rad/s
        self.theta = 0 # degree

        self.dt = dt 
        self.image = None
        self.rect = None
        
        self.sensors = {}
        
        self.setup()
    
    def setup(self):
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r']
        self.vx = math.cos(self.config['theta'])
        self.vy = math.sin(self.config['theta'])
        self.theta = self.config['theta']
        
        # appearance
        self.image = pygame.image.load(self.config['image'])
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.image = pygame.transform.rotate(self.image,self.theta)
        
    def add_sensor(self,sensor:callable):
        self.sensors[sensor.name] = sensor
        return
        
    def update(self):
        self.theta = self.theta + math.degrees(self.omega*self.dt)
        self.vx = self.v*math.cos(math.radians(self.theta))
        self.vy = self.v*math.sin(math.radians(self.theta))
        self.x = self.x + self.vx*self.dt
        self.y = self.y + self.vy*self.dt
        # appearance
        self.rect.center = (self.x,self.y)
        self.image = pygame.transform.rotate(self.image,self.theta)
        return 
        
    def control(self,v,omega):
        self.v = v
        self.omega = omega
        return
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)
           
    @property
    def states(self):
        return {'x':self.x,'y':self.y,'r':self.r,'theta':self.theta}
        
    def sensor_states(self,obs_pos:list)-> dict:
        results = {}
        for sensor,sensor_fn in self.sensors.items():
            results[sensor] = sensor_fn(self.states,obs_pos)
        return results
        
        
        
        
    