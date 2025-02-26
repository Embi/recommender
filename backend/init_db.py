#!/usr/bin/env python3
import pandas as pd
from sqlalchemy import text
from pathlib import Path
import numpy as np

from core.db.models.user import User
from core.db.models.listing import Listing
from core.db.models.base import Base
from core.db.session import get_session, get_engine

INITIAL_USER_PREFERENCE = np.array(
    [
        0.01295045,  # price range [0,1]
        0.53571429,  # age range [0,1]
        1.0,  # manual
        0.0,  # automatic
        1.0,  # petrol
        0.0,  # diesel
        0.0,  # cNG
        0.0,  # lPG
        0.0,  # electric
        0.0,  # brands:
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,  # Hyundai
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]
)


def initialize_db():
    with get_session() as session:
        session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    Base.metadata.create_all(get_engine())


def populate_with_random_users(count: int):
    def generate_user(user_id: int):
        return {
            "email": f"john{user_id}@example.com",
            "first_name": f"John{user_id}",
            "surname": "Doe",
            "preference": INITIAL_USER_PREFERENCE,
        }

    with get_session() as session:
        for i in range(count):
            user = generate_user(i)
            session.add(User(**user))
        session.commit()


def __listings_to_features(listings: pd.DataFrame) -> pd.DataFrame:
    """Vectorize listing features."""
    # Numerical features
    year_min, year_max = 1992, 2020
    norm_year = (listings["year"] - year_min) / (year_max - year_min)

    price_min, price_max = (
        listings["selling_price"].min(),
        listings["selling_price"].max(),
    )
    norm_price = (listings["selling_price"] - price_min) / (
        price_max - price_min
    )

    features = {
        "price": norm_price,
        "year": norm_year,
    }

    # Categorical features
    for category in listings["transmission"].unique():
        category_vector = listings["transmission"] == category
        features[f"transmission_{category}"] = category_vector.astype(
            np.float64
        )

    for category in listings["fuel"].unique():
        category_vector = listings["fuel"] == category
        features[f"fuel_{category}"] = category_vector.astype(np.float64)

    for category in listings["brand"].unique():
        category_vector = listings["brand"].apply(lambda x: category in x)
        features[f"brand_{category}"] = category_vector.astype(np.float64)

    return pd.DataFrame(features)


def populate_with_listings(listings_path: Path):
    """Read listings from the given csv file, enrich them with feature vectors
    and insert into the Listing psql table.
    """

    def add_brand(listing):
        """Extract brand from car full name."""
        if "Land" in listing["name"]:
            return "Land Rover"
        else:
            return listing["name"].split()[0]

    df_listings = pd.read_csv(listings_path)
    df_listings["brand"] = df_listings.apply(add_brand, axis=1)
    df_features = __listings_to_features(df_listings)
    df_listings["features"] = df_listings.apply(
        lambda row: df_features.iloc[row.name].to_numpy(), axis=1
    )

    listings = df_listings.to_dict(orient="records")
    with get_session() as session:
        for item in listings:
            session.add(Listing(**item))
        session.commit()


def drop_db():
    Base.metadata.drop_all(get_engine())


if __name__ == "__main__":
    initialize_db()
    populate_with_random_users(50)
    populate_with_listings(Path("backend/assets/car_data.csv"))
