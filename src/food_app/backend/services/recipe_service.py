from .base import BaseService
from ..infrastructure.models import Recipe, RecipeIngredient
from ..infrastructure.logger import trace_execution
from .nutrition_dataclass import NutritionPerServing
from .food_service import FoodService

class RecipeService(BaseService):
    def __init__(self, db, food_service: FoodService):
        super().__init__(db)
        self.food_service = food_service

    @trace_execution
    def calculate_nutrition(
        self,
        recipe_id: int,
        quantity: float = 1.0,
        unit_name: str = "portion",
    ) -> NutritionPerServing:
        recipe = self.db.get(Recipe, recipe_id)
        if not recipe or not recipe.ingredients:
            return NutritionPerServing(0.0, 0.0, 0.0, 0.0, 0.0)
        
        total_cal = total_prot = total_carb = total_fat = total_w = 0.0
        total_sat = total_trans = total_fib = total_sod = total_sug = 0.0
        
        for ing in recipe.ingredients:
            n = self.food_service.calculate_nutrition(ing.food_id, ing.quantity, ing.unit_name)
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
            
        weight_per_portion = total_w / recipe.portions_yield
        grams = weight_per_portion * quantity
        if grams <= 0:
            return NutritionPerServing(0.0, 0.0, 0.0, 0.0, 0.0)
            
        ratio = grams / weight_per_portion
        return NutritionPerServing(
            calories=(total_cal / recipe.portions_yield) * ratio,
            proteins=(total_prot / recipe.portions_yield) * ratio,
            carbs=(total_carb / recipe.portions_yield) * ratio,
            fats=(total_fat / recipe.portions_yield) * ratio,
            weight_grams=grams,
            saturated_fats=(total_sat / recipe.portions_yield) * ratio,
            trans_fats=(total_trans / recipe.portions_yield) * ratio,
            fiber=(total_fib / recipe.portions_yield) * ratio,
            sodium=(total_sod / recipe.portions_yield) * ratio,
            sugar=(total_sug / recipe.portions_yield) * ratio,
        )

    @trace_execution
    def create(self, name: str, portions_yield: int) -> Recipe:
        recipe = Recipe(name=name, portions_yield=portions_yield)
        self.db.add(recipe)
        self.db.flush()
        return recipe

    def add_ingredient(self, recipe_id: int, food_id: int, quantity: float, unit_name: str) -> RecipeIngredient:
        ing = RecipeIngredient(recipe_id=recipe_id, food_id=food_id, quantity=quantity, unit_name=unit_name)
        self.db.add(ing)
        self.db.flush()
        return ing
