import sys
import os
from datetime import date

from food_app.frontend.api_client import ApiClient
from food_app.backend.domain.food import FoodCreate
from food_app.backend.domain.log import DailyLogCreate
from food_app.backend.infrastructure.database import engine
from food_app.backend.infrastructure.base import Base

def setup_db():
    print("--- STEP 1: Setup DB ---")
    # Drop and recreate all tables for a clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database cleared and tables recreated.")

def run_scenario_a(api: ApiClient):
    print("\n--- STEP 2: Scenario A (Frutifica Case) ---")
    
    # 1. Register food: 'Marmita Frutifica'
    # Base Unit: 'g' (Value: 100.0)
    # Macros (per 100g): 112kcal, 9g Prot, 14g Carb, 4g Fat.
    food_data = FoodCreate(
        name="Marmita Frutifica",
        category="Pratos Prontos",
        unit_label="g",
        unit_val=100.0,
        calories=112.0,
        proteins=9.0,
        carbs=14.0,
        fats=4.0
    )
    
    food = api.create_food(food_data)
    print(f"Food created: {food.name} (ID: {food.id})")
    
    # 2. Add Custom Unit: 'unidade' = 350.0g
    api.add_custom_unit(food.id, "unidade", 350.0)
    print("Custom unit 'unidade' (350g) added.")
    
    # 3. Validation
    # Fetch the food back
    fetched_food = api.get_food_by_id(food.id)
    
    # Calculate nutrition for 1 unidade
    nutrition = api.calculate_food_nutrition(food.id, 1.0, "unidade")
    
    expected_calories = 112.0 * 3.5 # 112 per 100g * 3.5 (350g)
    print(f"Calculated Calories for 1 unidade (350g): {nutrition.calories}")
    print(f"Expected Calories: {expected_calories}")
    
    # Assert that calories are approx 392
    assert abs(nutrition.calories - expected_calories) < 0.1, f"Calories mismatch! Got {nutrition.calories}, expected {expected_calories}"
    
    print("SUCCESS: Frutifica Logic is working")
    return food.id

def run_scenario_b(api: ApiClient, food_id: int):
    print("\n--- STEP 3: Scenario B (Logging Consumption) ---")
    
    # Use api_client to log eating '0.5 unidade' of that marmita
    log_data = DailyLogCreate(
        log_date=date.today(),
        loggable_type="food",
        loggable_id=food_id,
        quantity=0.5,
        unit_name="unidade"
    )
    
    log_entry = api.log_consumption(log_data)
    print(f"Logged consumption: {log_entry.quantity} {log_entry.unit_name}")
    
    # Check if the log was saved correctly with the resolved grams (175g)
    # 0.5 * 350g = 175g
    expected_grams = 0.5 * 350.0
    print(f"Resolved Grams in Log: {log_entry.grams}")
    print(f"Expected Grams: {expected_grams}")
    
    assert abs(log_entry.grams - expected_grams) < 0.1, f"Grams mismatch in log! Got {log_entry.grams}, expected {expected_grams}"
    
    print("SUCCESS: Consumption logging with custom units is working")

if __name__ == "__main__":
    try:
        setup_db()
        
        api = ApiClient()
        
        food_id = run_scenario_a(api)
        run_scenario_b(api, food_id)
        
        api.close()
        print("\nALL TESTS PASSED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
