from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
from pathlib import Path
import ast

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def best_selling(request: Request):
    df = pd.read_csv(DATA_DIR / "output_best_selling.csv")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "products": df.to_dict(orient="records"),
        "section_title": "🏆 Best Selling Products",
        "show_recommendation": True
    })


@app.get("/least")
def least_selling(request: Request):
    df = pd.read_csv(DATA_DIR / "output_least_selling.csv")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "products": df.to_dict(orient="records"),
        "section_title": "📉 Least Selling Products",
        "show_recommendation": False
    })


@app.get("/summary")
def summary_view(request: Request):
    df = pd.read_csv(DATA_DIR / "summary.csv")

    # Parse stringified list
    df["categories"] = df["categories"].apply(ast.literal_eval)

    # Explode
    df = df.explode("categories")
    df["categories"] = df["categories"].str.strip().str.lower()
    df = df[df["categories"] != ""]  # Remove empty values

    # Group and aggregate
    grouped = df.groupby("categories").agg({
        "avg_rating": "mean",
        "avg_sentiment": "mean",
        "avg_doRecommend": "mean"
    }).reset_index()

    grouped = grouped.round(2)

    # Prepare for Chart.js
    categories = grouped["categories"].tolist()
    ratings = grouped["avg_rating"].tolist()
    sentiments = grouped["avg_sentiment"].tolist()
    recommends = (grouped["avg_doRecommend"] * 100).tolist()

    return templates.TemplateResponse("summary.html", {
        "request": request,
        "categories": categories,
        "ratings": ratings,
        "sentiments": sentiments,
        "recommends": recommends
    })
