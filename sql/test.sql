.mode column
.headers on
.width 25 15 15 12 10 10

-- 1. A Verdade Física (Alimentos Base 100g)
-- Confere se a importação do CSV/Cadastro salvou os macros normalizados
SELECT 
    id, 
    name, 
    calories_100g as kcal_100g, 
    proteins_100g as prot_100g,
    fiber_100g 
FROM foods
ORDER BY id DESC LIMIT 10;

-- 2. As Unidades (A "Cola" do sistema)
-- Confere se a "unidade" de 350g do Frutifica foi salva
SELECT 
    f.name as food, 
    u.unit_name, 
    u.grams 
FROM food_units u
JOIN foods f ON u.food_id = f.id
ORDER BY u.id DESC LIMIT 10;

-- 3. O Diário (Prova Real do Polimorfismo)
-- Essa query mostra se ele está logando Food, Recipe e Meal na mesma tabela
SELECT 
    l.log_date,
    COALESCE(f.name, r.name, m.name) as item_consumed,
    CASE 
        WHEN l.food_id IS NOT NULL THEN 'Food'
        WHEN l.recipe_id IS NOT NULL THEN 'Recipe'
        WHEN l.meal_id IS NOT NULL THEN 'Meal'
    END as type,
    l.quantity || ' ' || l.unit_name as portion_used,
    l.grams as final_weight_g
FROM daily_logs l
LEFT JOIN foods f ON l.food_id = f.id
LEFT JOIN recipes r ON l.recipe_id = r.id
LEFT JOIN meals m ON l.meal_id = m.id
ORDER BY l.log_date DESC, l.id DESC;