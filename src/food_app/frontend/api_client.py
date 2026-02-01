import logging
from typing import List, Optional
from food_app.backend.infrastructure.database import SessionLocal
from food_app.backend.infrastructure.models import Food, DailyLog, Recipe, Meal
from food_app.backend.infrastructure.logger import trace_execution
from food_app.backend.services.food_service import FoodService
from food_app.backend.services.recipe_service import RecipeService
from food_app.backend.services.meal_service import MealService
from food_app.backend.services.log_service import DailyLogService
from food_app.backend.domain.food import FoodCreate
from food_app.backend.domain.log import DailyLogCreate

logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self):
        self.db = SessionLocal()
        self.food_service = FoodService(self.db)
        self.recipe_service = RecipeService(self.db, self.food_service)
        self.meal_service = MealService(self.db, self.food_service, self.recipe_service)
        self.log_service = DailyLogService(self.db, self.food_service, self.recipe_service, self.meal_service)

    # Food Methods
    @trace_execution
    def get_active_foods(self) -> List[Food]:
        return self.db.query(Food).filter(Food.is_active == True).all()

    @trace_execution
    def get_food_by_id(self, food_id: int) -> Optional[Food]:
        return self.db.get(Food, food_id)

    @trace_execution
    def create_food(self, data: FoodCreate):
        try:
            res = self.food_service.create(data)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            logger.error(f"ApiClient.create_food error: {e}")
            raise e

    @trace_execution
    def add_custom_unit(self, food_id: int, unit_name: str, grams: float):
        try:
            res = self.food_service.add_unit(food_id, unit_name, grams)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            logger.error(f"ApiClient.add_custom_unit error: {e}")
            raise e

    # Log Methods
    @trace_execution
    def get_logs_by_date(self, log_date) -> List[DailyLog]:
        return self.db.query(DailyLog).filter(DailyLog.log_date == log_date).all()

    @trace_execution
    def log_consumption(self, data: DailyLogCreate):
        try:
            res = self.log_service.log_consumption(data)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            logger.error(f"ApiClient.log_consumption error: {e}")
            raise e

    # Recipe & Meal Methods
    @trace_execution
    def get_all_recipes(self) -> List[Recipe]:
        return self.db.query(Recipe).all()

    @trace_execution
    def get_all_meals(self) -> List[Meal]:
        return self.db.query(Meal).all()

    @trace_execution
    def calculate_food_nutrition(self, food_id: int, quantity: float, unit_name: str):
        return self.food_service.calculate_nutrition(food_id, quantity, unit_name)

    @trace_execution
    def calculate_recipe_nutrition(self, recipe_id: int, quantity: float = 1.0, unit_name: str = "portion"):
        return self.recipe_service.calculate_nutrition(recipe_id, quantity, unit_name)

    @trace_execution
    def calculate_meal_nutrition(self, meal_id: int):
        return self.meal_service.calculate_nutrition(meal_id)

    def close(self):
        self.db.close()
