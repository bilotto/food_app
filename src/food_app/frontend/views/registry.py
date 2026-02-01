import streamlit as st
from food_app.frontend.constants import get_text, FOOD_CATEGORIES, COMMON_UNITS
from food_app.backend.domain.food import FoodCreate

def render_registry(api_client):
    st.header(get_text("registry_header"))
    
    with st.form("food_registry_form"):
        name = st.text_input(get_text("food_name"))
        category = st.selectbox(get_text("category"), options=FOOD_CATEGORIES)
        
        st.subheader("Seção A: Base Nutricional")
        st.info("Insira os valores nutricionais para a quantidade base (ex: por 100g ou 100ml).")
        
        c1, c2 = st.columns(2)
        with c1:
            base_unit = st.selectbox(get_text("unit_label"), options=["g", "ml"])
        with c2:
            base_val = st.number_input(get_text("base_quantity_label"), min_value=0.1, value=100.0)
            
        n1, n2, n3, n4 = st.columns(4)
        calories = n1.number_input(get_text("calories_label"), min_value=0.0, value=0.0)
        proteins = n2.number_input(get_text("proteins_label"), min_value=0.0, value=0.0)
        carbs = n3.number_input(get_text("carbs_label"), min_value=0.0, value=0.0)
        fats = n4.number_input(get_text("fats_label"), min_value=0.0, value=0.0)
        
        with st.expander(get_text("advanced_details")):
            a1, a2, a3 = st.columns(3)
            fiber = a1.number_input(get_text("fiber_label"), min_value=0.0, value=0.0)
            sat_fat = a2.number_input(get_text("sat_fat_label"), min_value=0.0, value=0.0)
            sodium = a3.number_input(get_text("sodium_label"), min_value=0.0, value=0.0)
            
            a4, a5 = st.columns(2)
            sugar = a4.number_input(get_text("sugar_label"), min_value=0.0, value=0.0)
            trans_fat = a5.number_input(get_text("trans_fat_label"), min_value=0.0, value=0.0)

        st.divider()
        st.subheader("Seção B: Unidade de Medida (Opcional)")
        has_serving = st.checkbox(get_text("has_serving_unit"))
        
        s1, s2 = st.columns(2)
        serving_unit_raw = s1.selectbox(get_text("serving_unit_name"), options=COMMON_UNITS, disabled=not has_serving)
        
        # Handle custom unit name
        serving_unit_name = serving_unit_raw
        if serving_unit_raw == "Outro..." and has_serving:
            serving_unit_name = st.text_input("Especifique a unidade", placeholder="ex: pote, embalagem")
            
        serving_weight = s2.number_input(get_text("serving_unit_weight"), min_value=0.1, value=100.0, disabled=not has_serving)

        submitted = st.form_submit_button(get_text("btn_register"))
        if submitted:
            if not name or not category:
                st.error(get_text("registry_required"))
            elif has_serving and serving_unit_raw == "Outro..." and not serving_unit_name:
                st.error("Por favor, especifique o nome da unidade customizada.")
            else:
                try:
                    # 1. Create Food with Base Data
                    food_data = FoodCreate(
                        name=name,
                        category=category,
                        unit_label=base_unit,
                        unit_val=base_val,
                        calories=calories,
                        proteins=proteins,
                        carbs=carbs,
                        fats=fats,
                        fiber=fiber if fiber > 0 else None,
                        saturated_fats=sat_fat if sat_fat > 0 else None,
                        sodium=sodium if sodium > 0 else None,
                        sugar=sugar if sugar > 0 else None,
                        trans_fats=trans_fat if trans_fat > 0 else None
                    )
                    new_food = api_client.create_food(food_data)
                    
                    # 2. Add Serving Unit if requested
                    if has_serving and serving_unit_name:
                        # We need a method in api_client to add units, or use food_service directly if allowed
                        # Since ApiClient is our abstraction, let's assume it has add_food_unit
                        api_client.food_service.add_unit(new_food.id, serving_unit_name, serving_weight)
                        api_client.db.commit()
                    
                    st.success(get_text("registry_success").format(name=name))
                except Exception as e:
                    st.error(get_text("registry_error").format(error=str(e)))
