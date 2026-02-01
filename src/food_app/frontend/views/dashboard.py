import streamlit as st
import pandas as pd
from datetime import date
from food_app.frontend.constants import get_text
from food_app.frontend.components.metrics import render_nutrition_metrics
from food_app.backend.domain.log import DailyLogCreate

def render_dashboard(api_client):
    st.header(get_text("dashboard_header"))
    
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_date = st.date_input(get_text("select_date"), date.today())
    
    goal_kcal = 2000
    
    # Fetch logs
    try:
        logs = api_client.get_logs_by_date(selected_date)
    except Exception as e:
        st.error(f"Error fetching logs: {e}")
        logs = []
    
    total_kcal = total_prot = total_carb = total_fat = 0.0
    log_data = []
    
    if logs:
        for log in logs:
            try:
                if log.food_id:
                    n = api_client.calculate_food_nutrition(log.food_id, log.quantity, log.unit_name)
                    name = log.food.name if log.food else "Unknown Food"
                elif log.recipe_id:
                    n = api_client.calculate_recipe_nutrition(log.recipe_id, log.quantity, log.unit_name)
                    name = log.recipe.name if log.recipe else "Unknown Recipe"
                elif log.meal_id:
                    n = api_client.calculate_meal_nutrition(log.meal_id)
                    name = log.meal.name if log.meal else "Unknown Meal"
                else:
                    continue
                
                if n:
                    total_kcal += n.calories
                    total_prot += n.proteins
                    total_carb += n.carbs
                    total_fat += n.fats
                    
                    log_data.append({
                        "Name": name,
                        "Quantity": f"{log.quantity} {log.unit_name}",
                        "Calories": round(n.calories, 1),
                        "Protein": round(n.proteins, 1),
                        "Carbs": round(n.carbs, 1),
                        "Fat": round(n.fats, 1)
                    })
            except Exception as e:
                st.warning(f"Error processing log entry: {e}")

    render_nutrition_metrics(total_kcal, total_prot, total_carb, total_fat, goal_kcal)

    st.subheader(get_text("daily_log_subheader"))
    if log_data:
        st.dataframe(pd.DataFrame(log_data), width="stretch")
    else:
        st.info(get_text("no_logs"))

    st.divider()
    st.subheader(get_text("log_consumption_header"))
    
    try:
        all_foods = api_client.get_active_foods()
    except Exception as e:
        st.error(f"Error fetching foods: {e}")
        all_foods = []

    if not all_foods:
        st.info("No data yet. Please go to 'Food Registry' to add some.")
        return

    with st.form("log_food_form"):
        food_options = {f"{f.name} ({f.category})": f.id for f in all_foods}
        
        selected_food_name = st.selectbox(get_text("select_food"), options=list(food_options.keys()))
        food_id = food_options[selected_food_name] if selected_food_name else None
        
        q_col1, q_col2 = st.columns(2)
        with q_col1:
            quantity = st.number_input(get_text("quantity"), min_value=0.0, value=100.0, step=1.0)
        with q_col2:
            available_units = ["g", "ml"]
            if food_id:
                food_obj = api_client.get_food_by_id(food_id)
                if food_obj:
                    available_units += [u.unit_name for u in food_obj.units]
            unit = st.selectbox(get_text("unit"), options=list(set(available_units)))

        submitted = st.form_submit_button(get_text("btn_log"))
        if submitted:
            try:
                log_create = DailyLogCreate(
                    log_date=selected_date,
                    loggable_type="food",
                    loggable_id=food_id,
                    quantity=quantity,
                    unit_name=unit
                )
                api_client.log_consumption(log_create)
                st.success(get_text("log_success").format(quantity=quantity, unit=unit, name=selected_food_name))
                st.rerun()
            except Exception as e:
                st.error(get_text("log_error").format(error=str(e)))
