from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum, auto
import json

@dataclass
class RequestMixin:
    @classmethod
    def from_request(cls, request):
        values = request.get("input")
        return cls(**values)

    def to_json(self):
        return json.dumps(asdict(self))

@dataclass
class validatedResponse(RequestMixin):
  order_id: Optional[str]
  order_valid: Optional[bool]

@dataclass
class Mutation(RequestMixin):
  placeAndValidateOrder: Optional[validatedResponse]

@dataclass
class placeAndValidateOrderArgs(RequestMixin):
  item_list: List[str]
  user_id: str