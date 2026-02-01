from datetime import date
from typing import Optional, Literal
from .base import BaseSchema

LoggableType = Literal["food", "recipe", "meal"]

class DailyLogSchema(BaseSchema):
    id: int
    log_date: date
    food_id: Optional[int] = None
    recipe_id: Optional[int] = None
    meal_id: Optional[int] = None
    quantity: float
    unit_name: str
    grams: float

class DailyLogCreate(BaseSchema):
    log_date: date
    loggable_type: LoggableType
    loggable_id: int
    quantity: float
    unit_name: str
