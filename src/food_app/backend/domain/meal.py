from typing import List, Optional
from .base import BaseSchema
from .food import FoodSchema
from .recipe import RecipeSchema

class MealItemSchema(BaseSchema):
    id: Optional[int] = None
    meal_id: Optional[int] = None
    food_id: Optional[int] = None
    recipe_id: Optional[int] = None
    quantity: float
    unit_name: str
    food: Optional[FoodSchema] = None
    recipe: Optional[RecipeSchema] = None

class MealSchema(BaseSchema):
    id: int
    name: str
    is_active: bool
    items: List[MealItemSchema] = []

class MealCreate(BaseSchema):
    name: str
