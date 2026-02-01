from .base import BaseService
from ..infrastructure.models import Meal, MealItem
from ..infrastructure.logger import trace_execution
from .nutrition_dataclass import NutritionPerServing
from .food_service import FoodService
from .recipe_service import RecipeService

class MealService(BaseService):
    def __init__(self, db, food_service: FoodService, recipe_service: RecipeService):
        super().__init__(db)
        self.food_service = food_service
        self.recipe_service = recipe_service

    @trace_execution
    def calculate_nutrition(self, meal_id: int) -> NutritionPerServing:
        meal = self.db.get(Meal, meal_id)
        if not meal or not meal.items:
            return NutritionPerServing(0.0, 0.0, 0.0, 0.0, 0.0)
            
        total_cal = total_prot = total_carb = total_fat = total_w = 0.0
        total_sat = total_trans = total_fib = total_sod = total_sug = 0.0
        
        for item in meal.items:
            if item.food_id:
                n = self.food_service.calculate_nutrition(item.food_id, item.quantity, item.unit_name)
            elif item.recipe_id:
                n = self.recipe_service.calculate_nutrition(item.recipe_id, item.quantity, item.unit_name)
            else:
                continue
                
            total_cal += n.calories
            total_prot += n.proteins
            total_carb += n.carbs
            total_fat += n.fats
            total_w += n.weight_grams
            total_sat += n.saturated_fats
            total_trans += n.trans_fats
            total_fib += n.fiber
            total_sod += n.sodium
            total_sug += n.sugar
            
        return NutritionPerServing(
            calories=total_cal,
            proteins=total_prot,
            carbs=total_carb,
            fats=total_fat,
            weight_grams=total_w,
            saturated_fats=total_sat,
            trans_fats=total_trans,
            fiber=total_fib,
            sodium=total_sod,
            sugar=total_sug,
        )

    def create(self, name: str) -> Meal:
        meal = Meal(name=name)
        self.db.add(meal)
        self.db.flush()
        return meal

    def add_item(self, meal_id: int, quantity: float, unit_name: str, food_id: int = None, recipe_id: int = None) -> MealItem:
        item = MealItem(meal_id=meal_id, food_id=food_id, recipe_id=recipe_id, quantity=quantity, unit_name=unit_name)
        self.db.add(item)
        self.db.flush()
        return item
