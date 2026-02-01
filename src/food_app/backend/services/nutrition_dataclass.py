from dataclasses import dataclass

@dataclass(frozen=True)
class NutritionPerServing:
    calories: float
    proteins: float
    carbs: float
    fats: float
    weight_grams: float
    saturated_fats: float = 0.0
    trans_fats: float = 0.0
    fiber: float = 0.0
    sodium: float = 0.0
    sugar: float = 0.0
