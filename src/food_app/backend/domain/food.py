from typing import List, Optional
from .base import BaseSchema

class FoodUnitSchema(BaseSchema):
    id: Optional[int] = None
    food_id: Optional[int] = None
    unit_name: str
    grams: float

class FoodCreate(BaseSchema):
    name: str
    category: str
    unit_label: str
    unit_val: float
    calories: float
    proteins: float
    carbs: float
    fats: float
    saturated_fats: Optional[float] = None
    trans_fats: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None
    sugar: Optional[float] = None

class FoodSchema(BaseSchema):
    id: int
    name: str
    category: str
    is_liquid: bool
    is_active: bool
    calories_100g: float
    proteins_100g: float
    carbs_100g: float
    fats_100g: float
    saturated_fats_100g: Optional[float] = None
    trans_fats_100g: Optional[float] = None
    fiber_100g: Optional[float] = None
    sodium_100g: Optional[float] = None
    sugar_100g: Optional[float] = None
    units: List[FoodUnitSchema] = []
