# Localization constants for Yazio Based
# Default language: PT-BR

TEXTS = {
    "pt": {
        "app_title": "Yazio Based - Rastreador de Nutrição",
        "sidebar_title": "Yazio Based",
        "nav_dashboard": "Dashboard & Diário",
        "nav_registry": "Registro de Alimentos",
        "nav_kitchen": "Cozinha (Receitas/Refeições)",
        
        "dashboard_header": "Dashboard & Diário",
        "select_date": "Selecione a Data",
        "goal_kcal": "Meta: 2000 kcal",
        "metric_calories": "Calorias",
        "metric_protein": "Proteínas",
        "metric_carbs": "Carboidratos",
        "metric_fat": "Gorduras",
        "daily_log_subheader": "Diário do Dia",
        "no_logs": "Nenhum registro para esta data.",
        "log_consumption_header": "Registrar Consumo",
        "select_food": "Selecione o Alimento",
        "quantity": "Quantidade",
        "unit": "Unidade",
        "btn_log": "Registrar Consumo",
        "log_success": "Registrado {quantity} {unit} de {name}",
        "log_error": "Erro ao registrar consumo: {error}",
        
        "registry_header": "Registrar Novo Alimento",
        "food_name": "Nome do Alimento",
        "category": "Categoria (ex: Frutas, Laticínios)",
        "unit_label": "Rótulo da Unidade (ex: 'xícara', 'fatia', 'g')",
        "unit_val": "Valor da Unidade em gramas/ml",
        "nutrients_per_unit": "Nutrientes (por Valor da Unidade)",
        "calories_label": "Calorias (kcal)",
        "proteins_label": "Proteínas (g)",
        "carbs_label": "Carboidratos (g)",
        "fats_label": "Gorduras (g)",
        "advanced_details": "Detalhes Avançados (Micronutrientes)",
        "fiber_label": "Fibra (g)",
        "sat_fat_label": "Gordura Saturada (g)",
        "sodium_label": "Sódio (mg)",
        "sugar_label": "Açúcar (g)",
        "trans_fat_label": "Gordura Trans (g)",
        "btn_register": "Registrar Alimento",
        "registry_success": "Alimento '{name}' registrado com sucesso!",
        "registry_error": "Erro ao registrar alimento: {error}",
        "registry_required": "Nome e Categoria são obrigatórios.",
        
        "kitchen_header": "Cozinha (Receitas & Refeições)",
        "tab_recipes": "Receitas",
        "tab_meals": "Refeições",
        "existing_recipes": "Receitas Existentes",
        "existing_meals": "Refeições Existentes",
        "no_recipes": "Nenhuma receita encontrada.",
        "no_meals": "Nenhuma refeição encontrada.",
        "nutrition_per_portion": "**Nutrição por porção:** {kcal:.1f} kcal | P: {p:.1f}g | C: {c:.1f}g | F: {f:.1f}g",
        "total_nutrition": "**Nutrição Total:** {kcal:.1f} kcal | P: {p:.1f}g | C: {c:.1f}g | F: {f:.1f}g",
        "has_serving_unit": "Este item possui uma unidade de medida padrão? (ex: pote, embalagem)",
        "serving_unit_name": "Nome da Unidade (ex: pote, fatia)",
        "serving_unit_weight": "Peso da Unidade (g/ml)",
        "base_quantity_label": "Quantidade Base (g/ml)",
    }
}

FOOD_CATEGORIES = ["Carnes", "Grãos", "Laticínios", "Vegetais", "Pratos Prontos", "Outros"]
COMMON_UNITS = ["g", "ml", "fatia", "unidade", "colher", "Outro..."]

DEFAULT_LANG = "pt"

def get_text(key, lang=DEFAULT_LANG):
    return TEXTS.get(lang, TEXTS[DEFAULT_LANG]).get(key, key)
