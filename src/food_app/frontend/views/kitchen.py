import streamlit as st
from food_app.frontend.constants import get_text

def render_kitchen(api_client):
    st.header(get_text("kitchen_header"))
    
    tab1, tab2 = st.tabs([get_text("tab_recipes"), get_text("tab_meals")])
    
    with tab1:
        st.subheader(get_text("existing_recipes"))
        try:
            recipes = api_client.get_all_recipes()
            if recipes:
                for r in recipes:
                    with st.expander(f"{r.name} ({r.portions_yield} porções)"):
                        n = api_client.calculate_recipe_nutrition(r.id)
                        if n:
                            st.write(get_text("nutrition_per_portion").format(kcal=n.calories, p=n.proteins, c=n.carbs, f=n.fats))
            else:
                st.info("No data yet.")
        except Exception as e:
            st.info("No data yet.")
            
    with tab2:
        st.subheader(get_text("existing_meals"))
        try:
            meals = api_client.get_all_meals()
            if meals:
                for m in meals:
                    with st.expander(m.name):
                        n = api_client.calculate_meal_nutrition(m.id)
                        if n:
                            st.write(get_text("total_nutrition").format(kcal=n.calories, p=n.proteins, c=n.carbs, f=n.fats))
            else:
                st.info("No data yet.")
        except Exception as e:
            st.info("No data yet.")
