from typing import List, Text
from dataclasses import dataclass, field
from .data import Data
import math
import numpy as np
import numpy.typing as npt

MINUTES = 120

@dataclass
class RingBuffer:
    name: Text = ""
    ringbuffer: List[Data] = field(default_factory=list)
    #latencies: npt.ArrayLike = field(default_factory=lambda: np.zeros(shape=0))
    size: int = MINUTES*60
    last_value:Data = None
    total: float = 0

    def add(self,data:Data):
        if len(self.ringbuffer) == self.size:
            first = self.ringbuffer[0]
            self.remove(first)
            self.total -= first.latency
        self.ringbuffer.append(data)
        self.total += data.latency

    def remove(self, position:Data):
        self.ringbuffer.remove(position)

    @property
    def length(self):
        return len(self.ringbuffer)

    def get(self):
        return self.ringbuffer

    @property
    def media(self):
        if self.length > 0:
            return self.total/self.length
        else:
            return 0

    @property
    def desviacion_estandar(self):
        if self.length > 0:
            latencies_diff = np.array([data.latency for data in
                        self.ringbuffer]) - self.media
            return math.sqrt(np.dot(latencies_diff,
                                    latencies_diff))/self.length
        else:
            return 0

    @property
    def mu(self):
        return self.media

    @property
    def sigma(self):
        return self.desviacion_estandar

    def clear(self):
        self.ringbuffer.clear()
        self.total = 0
        self.last_value = None

    def __iter__(self):
        return iter(self.ringbuffer)

    def __repr__(self):
        return f"RingBuffer({self.name}, {self.size}, {self.length}, {self.mu}, {self.sigma})"
