from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ExecutionContext:
    """
    Carries state throughout the request lifecycle.
    """
    request_id: str
    user_id: str
    start_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_metric(self, key: str, value: Any):
        self.metadata[key] = value
