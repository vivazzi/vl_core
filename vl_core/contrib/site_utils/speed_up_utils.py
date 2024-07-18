from abc import ABC, abstractmethod


class BaseSpeedUp(ABC):
    accelerated = False

    @abstractmethod
    def speed_up(self):
        return {}
