from abc import ABCMeta,abstractclassmethod, abstractmethod
import re


class Reward(metaclass = ABCMeta):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def setup(self,goals,humans,obstacles,robot,**kwargs):
        raise NotImplementedError
    
    
    @abstractmethod
    def reward(self,goals,humans,obstacles,robot,finish,collide,**kwargs)->float:
        raise NotImplementedError
        