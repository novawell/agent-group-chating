from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

@dataclass
class Expertise:
    subject: str
    description: Optional[str]
    attributes: Optional[Dict[str, Any]]