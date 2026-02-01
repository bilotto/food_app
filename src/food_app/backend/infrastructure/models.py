from datetime import date
from typing import List, Optional

from sqlalchemy import (
    CheckConstraint,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    is_liquid: Mapped[bool] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    calories_100g: Mapped[float] = mapped_column(Float, nullable=False)
    proteins_100g: Mapped[float] = mapped_column(Float, nullable=False)
    carbs_100g: Mapped[float] = mapped_column(Float, nullable=False)
    fats_100g: Mapped[float] = mapped_column(Float, nullable=False)

    # Expanded nutrition
    saturated_fats_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    trans_fats_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fiber_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sodium_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sugar_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    units: Mapped[List["FoodUnit"]] = relationship(
        "FoodUnit", back_populates="food", cascade="all, delete-orphan"
    )


class FoodUnit(Base):
    __tablename__ = "food_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id", ondelete="CASCADE"), nullable=False)
    unit_name: Mapped[str] = mapped_column(String(64), nullable=False)
    grams: Mapped[float] = mapped_column(Float, nullable=False)

    food: Mapped["Food"] = relationship("Food", back_populates="units")
    __table_args__ = (UniqueConstraint("food_id", "unit_name", name="uq_food_unit"),)


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    portions_yield: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan"
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_name: Mapped[str] = mapped_column(String(64), nullable=False)

    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")
    food: Mapped["Food"] = relationship("Food")


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    items: Mapped[List["MealItem"]] = relationship(
        "MealItem", back_populates="meal", cascade="all, delete-orphan"
    )


class MealItem(Base):
    __tablename__ = "meal_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id", ondelete="CASCADE"), nullable=False)
    food_id: Mapped[Optional[int]] = mapped_column(ForeignKey("foods.id", ondelete="CASCADE"), nullable=True)
    recipe_id: Mapped[Optional[int]] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_name: Mapped[str] = mapped_column(String(64), nullable=False)

    meal: Mapped["Meal"] = relationship("Meal", back_populates="items")
    food: Mapped[Optional["Food"]] = relationship("Food")
    recipe: Mapped[Optional["Recipe"]] = relationship("Recipe")

    __table_args__ = (
        CheckConstraint(
            "(food_id IS NOT NULL AND recipe_id IS NULL) OR (food_id IS NULL AND recipe_id IS NOT NULL)",
            name="ck_meal_item_single_source",
        ),
    )


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    log_date: Mapped[date] = mapped_column(Date, nullable=False)
    food_id: Mapped[Optional[int]] = mapped_column(ForeignKey("foods.id", ondelete="CASCADE"), nullable=True)
    recipe_id: Mapped[Optional[int]] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), nullable=True)
    meal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("meals.id", ondelete="CASCADE"), nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_name: Mapped[str] = mapped_column(String(64), nullable=False)
    grams: Mapped[float] = mapped_column(Float, nullable=False)

    food: Mapped[Optional["Food"]] = relationship("Food")
    recipe: Mapped[Optional["Recipe"]] = relationship("Recipe")
    meal: Mapped[Optional["Meal"]] = relationship("Meal")

    __table_args__ = (
        CheckConstraint(
            "(food_id IS NOT NULL AND recipe_id IS NULL AND meal_id IS NULL)"
            " OR (food_id IS NULL AND recipe_id IS NOT NULL AND meal_id IS NULL)"
            " OR (food_id IS NULL AND recipe_id IS NULL AND meal_id IS NOT NULL)",
            name="ck_daily_log_single_loggable",
        ),
    )
