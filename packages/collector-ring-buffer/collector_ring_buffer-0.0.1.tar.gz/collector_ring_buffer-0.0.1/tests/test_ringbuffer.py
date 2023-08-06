from unittest import TestCase
from datetime import datetime
from crb import (RingBuffer, Data)
import math

class TestRingBuffer(TestCase):
        
    def test_add(self):
        data = [3.0, 4, 4, 5.4, 1, 4.3, 5, 6.2]
        dataset = [Data(dt_gen=datetime.now(), latency=d) 
                        for d in data]
        ring_buffer = RingBuffer()
        for item in dataset:
            ring_buffer.add(item)
        latencies = [d.latency for d in ring_buffer]
        self.assertEqual(data, latencies)

    def test_media(self):
        data = [3.0, 4, 4, 5.4, 1, 4.3, 5, 6.2]

        dataset = [Data(dt_gen=datetime.now(), latency=d) 
                        for d in data]

        ring_buffer = RingBuffer()
        for item in dataset:
            ring_buffer.add(item)
        media = sum(data)/len(data)
        self.assertEqual(media, ring_buffer.media)

    def test_desv_std(self):
        data = [3.0, 4, 4, 5.4, 1, 4.3, 5, 6.2]

        dataset = [Data(dt_gen=datetime.now(), latency=d) 
                        for d in data]

        ring_buffer = RingBuffer()
        for item in dataset:
            ring_buffer.add(item)
        media = sum(data)/len(data)
        dev_std = math.sqrt(sum([(e-media)**2 for e in data]))/len(data)
        self.assertEqual(dev_std, ring_buffer.desviacion_estandar)


    def test_limit_datalength(self):
        data = [3.0, 4, 4, 5.4, 1, 4.3, 5, 6.2]

        dataset = [Data(dt_gen=datetime.now(), latency=d) 
                        for d in data]

        size = 2
        ring_buffer = RingBuffer(size=size)
        for item in dataset:
            ring_buffer.add(item)
        media = sum(data[-size::])/size
        dev_std = math.sqrt(sum([(e-media)**2 for e in data[-size::]]))/size
        self.assertEqual(dev_std, ring_buffer.desviacion_estandar)



if __name__ == "__main__":
    unittest.main()
