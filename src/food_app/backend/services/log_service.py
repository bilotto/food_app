from datetime import date
from .base import BaseService
from ..infrastructure.models import DailyLog
from ..domain.log import DailyLogCreate, LoggableType
from .food_service import FoodService
from .recipe_service import RecipeService
from .meal_service import MealService

class DailyLogService(BaseService):
    def __init__(self, db, food_service: FoodService, recipe_service: RecipeService, meal_service: MealService):
        super().__init__(db)
        self.food_service = food_service
        self.recipe_service = recipe_service
        self.meal_service = meal_service

    def _resolve_grams(self, loggable_type: LoggableType, loggable_id: int, quantity: float, unit_name: str) -> float:
        if loggable_type == "food":
            n = self.food_service.calculate_nutrition(loggable_id, quantity, unit_name)
            return n.weight_grams
        if loggable_type == "recipe":
            n = self.recipe_service.calculate_nutrition(loggable_id, quantity, unit_name)
            return n.weight_grams
        if loggable_type == "meal":
            n = self.meal_service.calculate_nutrition(loggable_id)
            return n.weight_grams
        return 0.0

    def log_consumption(self, data: DailyLogCreate) -> DailyLog:
        grams = self._resolve_grams(data.loggable_type, data.loggable_id, data.quantity, data.unit_name)
        
        food_id = data.loggable_id if data.loggable_type == "food" else None
        recipe_id = data.loggable_id if data.loggable_type == "recipe" else None
        meal_id = data.loggable_id if data.loggable_type == "meal" else None
        
        entry = DailyLog(
            log_date=data.log_date,
            food_id=food_id,
            recipe_id=recipe_id,
            meal_id=meal_id,
            quantity=data.quantity,
            unit_name=data.unit_name,
            grams=grams,
        )
        self.db.add(entry)
        self.db.flush()
        return entry
