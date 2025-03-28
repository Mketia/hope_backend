from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any
from django.db.models import Model

@dataclass
class RepositoryResponse:
    success: bool
    data: Optional[Union[Dict, List, Model]]
    message: str

@dataclass
class APIResponse:
    success: bool
    data: Optional[Union[Dict, List, Model]]
    message: str
    status: Optional[Any]  