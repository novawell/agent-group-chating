from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

@dataclass
class Expertise:
    subject: str
    description: Optional[str] = field(default=None)
    attributes: Optional[Dict[str, Any]] = field(default=None)