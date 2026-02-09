from dataclasses import dataclass
import time

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float

class MetricsCollector:
    def __init__(self):
        self.metrics = []

    def record(self, name: str, value: float):
        self.metrics.append(Metric(name, value, time.time()))

metrics_collector = MetricsCollector()
