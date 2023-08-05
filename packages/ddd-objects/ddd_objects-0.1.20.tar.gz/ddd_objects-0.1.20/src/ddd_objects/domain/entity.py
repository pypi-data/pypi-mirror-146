from time import time
from typing import Optional


class Entity:
    def get_json(self):
        raise NotImplementedError

class ExpiredEntity(Entity):
    def __init__(self, life_time:Optional[int]=None) -> None:
        self.life_time = life_time
        if self.life_time is None:
            self.expired_time = None
        else:
            self.expired_time = time()+self.life_time.get_value()