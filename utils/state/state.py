from abc import ABCMeta, abstractmethod
import numpy as np

class State(metaclass = ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def wrapper(self,frames,**kwargs)->np.ndarray:
        raise NotImplementedError