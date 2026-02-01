from typing import Optional
from sqlalchemy.orm import Session
from .base import BaseService
from ..infrastructure.models import Food, FoodUnit
from ..domain.food import FoodCreate
from ..infrastructure.logger import trace_execution
from .nutrition_dataclass import NutritionPerServing

class FoodService(BaseService):
    def _grams_for_food(self, food_id: int, quantity: float, unit_name: str) -> float:
        unit_lower = unit_name.lower()
        if unit_lower in ("g", "ml"):
            return quantity
        food = self.db.get(Food, food_id)
        if not food:
            return 0.0
        unit_row = next((u for u in food.units if u.unit_name.lower() == unit_lower), None)
        grams_per_unit = unit_row.grams if unit_row else 100.0
        return quantity * grams_per_unit

    def _nutrition_for_grams(self, food: Food, grams: float) -> NutritionPerServing:
        ratio = grams / 100.0
        return NutritionPerServing(
            calories=food.calories_100g * ratio,
            proteins=food.proteins_100g * ratio,
            carbs=food.carbs_100g * ratio,
            fats=food.fats_100g * ratio,
            weight_grams=grams,
            saturated_fats=(food.saturated_fats_100g or 0.0) * ratio,
            trans_fats=(food.trans_fats_100g or 0.0) * ratio,
            fiber=(food.fiber_100g or 0.0) * ratio,
            sodium=(food.sodium_100g or 0.0) * ratio,
            sugar=(food.sugar_100g or 0.0) * ratio,
        )

    @trace_execution
    def calculate_nutrition(self, food_id: int, quantity: float, unit_name: str) -> NutritionPerServing:
        food = self.db.get(Food, food_id)
        if not food:
            return NutritionPerServing(0.0, 0.0, 0.0, 0.0, 0.0)
        grams = self._grams_for_food(food_id, quantity, unit_name)
        return self._nutrition_for_grams(food, grams)

    @trace_execution
    def create(self, data: FoodCreate) -> Food:
        is_liquid = data.unit_label.lower() in ("ml", "l")
        ratio_to_100 = 100.0 / data.unit_val
        food = Food(
            name=data.name,
            category=data.category,
            is_liquid=is_liquid,
            is_active=True,
            calories_100g=data.calories * ratio_to_100,
            proteins_100g=data.proteins * ratio_to_100,
            carbs_100g=data.carbs * ratio_to_100,
            fats_100g=data.fats * ratio_to_100,
            saturated_fats_100g=data.saturated_fats * ratio_to_100 if data.saturated_fats is not None else None,
            trans_fats_100g=data.trans_fats * ratio_to_100 if data.trans_fats is not None else None,
            fiber_100g=data.fiber * ratio_to_100 if data.fiber is not None else None,
            sodium_100g=data.sodium * ratio_to_100 if data.sodium is not None else None,
            sugar_100g=data.sugar * ratio_to_100 if data.sugar is not None else None,
        )
        self.db.add(food)
        self.db.flush()
        if data.unit_label.lower() not in ("g", "ml"):
            self.db.add(FoodUnit(food_id=food.id, unit_name=data.unit_label, grams=data.unit_val))
        self.db.flush()
        return food

    def add_unit(self, food_id: int, unit_name: str, grams: float) -> FoodUnit:
        existing = (
            self.db.query(FoodUnit)
            .filter(FoodUnit.food_id == food_id, FoodUnit.unit_name == unit_name)
            .first()
        )
        if existing:
            existing.grams = grams
            return existing
        unit = FoodUnit(food_id=food_id, unit_name=unit_name, grams=grams)
        self.db.add(unit)
        self.db.flush()
        return unit
