import streamlit as st
from food_app.frontend.constants import get_text

def render_nutrition_metrics(total_kcal, total_prot, total_carb, total_fat, goal_kcal=2000):
    m1, m2, m3, m4 = st.columns(4)
    
    kcal_delta = int(total_kcal - goal_kcal)
    m1.metric(
        get_text("metric_calories"), 
        f"{int(total_kcal)} / {goal_kcal} kcal", 
        delta=f"{kcal_delta}", 
        delta_color="inverse"
    )
    m2.metric(get_text("metric_protein"), f"{total_prot:.1f}g")
    m3.metric(get_text("metric_carbs"), f"{total_carb:.1f}g")
    m4.metric(get_text("metric_fat"), f"{total_fat:.1f}g")
