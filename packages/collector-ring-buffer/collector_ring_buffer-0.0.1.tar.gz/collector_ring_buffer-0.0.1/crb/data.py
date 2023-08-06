from typing import NamedTuple
from datetime import datetime

class Data(NamedTuple):
    dt_gen: datetime
    latency: float
  
    def dict(self):
        return self._asdict()

    @property
    def delta_time(self):
        return self.latency
