import csv
import os
from datetime import date
from sqlalchemy.orm import Session

from food_app.backend.infrastructure.database import engine, SessionLocal
from food_app.backend.infrastructure.base import Base
from food_app.backend.infrastructure.logger import setup_logging, get_logger
from food_app.backend.services.food_service import FoodService
from food_app.backend.services.recipe_service import RecipeService
from food_app.backend.services.meal_service import MealService
from food_app.backend.services.log_service import DailyLogService
from food_app.backend.domain.food import FoodCreate
from food_app.backend.domain.log import DailyLogCreate

logger = get_logger(__name__)

def main():
    setup_logging()
    # Create tables
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # Initialize services
        food_service = FoodService(db)
        recipe_service = RecipeService(db, food_service)
        meal_service = MealService(db, food_service, recipe_service)
        log_service = DailyLogService(db, food_service, recipe_service, meal_service)

        # 1. Create Food
        oats_data = FoodCreate(
            name="Oats",
            category="Grains",
            unit_label="g",
            unit_val=100.0,
            calories=389.0,
            proteins=16.9,
            carbs=66.3,
            fats=6.9
        )
        oats = food_service.create(oats_data)
        food_service.add_unit(oats.id, "tablespoon", 10.0)
        db.commit()
        logger.info(f"Created Food: {oats.name} (id={oats.id})")

        # 2. Create Recipe
        pancakes = recipe_service.create(name="Pancakes", portions_yield=2)
        recipe_service.add_ingredient(pancakes.id, oats.id, 40.0, "g")
        db.commit()
        logger.info(f"Created Recipe: {pancakes.name} (id={pancakes.id})")

        # 3. Create Meal containing a Recipe
        breakfast = meal_service.create(name="My Breakfast")
        meal_service.add_item(breakfast.id, quantity=2.0, unit_name="tablespoon", food_id=oats.id)
        meal_service.add_item(breakfast.id, quantity=1.0, unit_name="portion", recipe_id=pancakes.id)
        db.commit()
        logger.info(f"Created Meal: {breakfast.name} (id={breakfast.id}) with 2 tbsp oats + 1 portion pancakes")

        # 4. Calculate Nutrition
        meal_nut = meal_service.calculate_nutrition(breakfast.id)
        logger.info(f"Meal Nutrition: {meal_nut.calories:.0f} kcal, {meal_nut.proteins:.1f}g P, {meal_nut.weight_grams:.0f}g")

        # 5. Log Consumption
        log_data = DailyLogCreate(
            log_date=date.today(),
            loggable_type="meal",
            loggable_id=breakfast.id,
            quantity=1.0,
            unit_name="meal"
        )
        log_entry = log_service.log_consumption(log_data)
        db.commit()
        logger.info(f"Logged consumption for {log_entry.log_date}")

        # Load CSV if exists
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(project_root, "data", "frutifica.csv")
        if os.path.exists(csv_path):
            load_csv(db, food_service, csv_path)

def load_csv(db: Session, food_service: FoodService, csv_path: str):
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.get('nome', '')
            portion = row.get('porcao', 0)
            calories = row.get('kcal', 0)
            proteins = row.get('proteina', 0)
            carbs = row.get('carboidrato', 0)
            fats = row.get('gordura', 0)
            weight_g = row.get('peso_g', 0)
            quantity_type = row.get('tipo_quantidade', '')

            logger.info(f"Loading food from CSV: {name}")
            food_data = FoodCreate(
                name=name,
                category="Food",
                unit_label="g",
                unit_val=float(portion),
                calories=float(calories),
                proteins=float(proteins),
                carbs=float(carbs),
                fats=float(fats),
                saturated_fats=float(row.get('gordura_saturada', 0)) if row.get('gordura_saturada') else None,
                trans_fats=float(row.get('gordura_trans', 0)) if row.get('gordura_trans') else None,
                fiber=float(row.get('fibra', 0)) if row.get('fibra') else None,
                sodium=float(row.get('sodio_mg', 0)) if row.get('sodio_mg') else None,
                sugar=float(row.get('acucar_total', 0)) if row.get('acucar_total') else None,
            )
            food = food_service.create(food_data)
            food_service.add_unit(food.id, quantity_type, float(weight_g))
            db.commit()

if __name__ == "__main__":
    main()
