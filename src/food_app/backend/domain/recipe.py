from typing import List, Optional
from .base import BaseSchema
from .food import FoodSchema

class RecipeIngredientSchema(BaseSchema):
    id: Optional[int] = None
    recipe_id: Optional[int] = None
    food_id: int
    quantity: float
    unit_name: str
    food: Optional[FoodSchema] = None

class RecipeSchema(BaseSchema):
    id: int
    name: str
    portions_yield: int
    is_active: bool
    ingredients: List[RecipeIngredientSchema] = []

class RecipeCreate(BaseSchema):
    name: str
    portions_yield: int
