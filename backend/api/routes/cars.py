import numpy as np
from typing import List, Optional
from fastapi import APIRouter
from fastapi import Depends
from api.utils.auth import authenticate
from core.db.models.listing import Listing
from core.db.models.user import User
from core.db.session import get_async_session
from core.utils.asynchronous.pubsub import publish
from sqlalchemy import select, text
from api.validation.cars import (
    ListingDetailResponse,
    ListingSearchResponse,
    ListingRecommendationResponse,
)

# from api.utils.cache import cached_json_response
# from core.utils.rmq import publish_message

router = APIRouter()
__LISTING_SEARCH_LIMIT = 200
__SIMILARITY_QUERY = """
SELECT *
FROM listings
ORDER BY features <-> '{user_preference}'
LIMIT 20;
"""


@router.get("/detail/{listing_id}")
async def get_listing_details(
    listing_id: int,
    user: dict = Depends(authenticate),
) -> ListingDetailResponse:
    """Get detail information about a particular listing."""
    listing = await get_listing(listing_id)
    await emit_user_detail_interest(user, listing)
    return ListingDetailResponse(**listing.to_dict())


@router.get("/search")
async def search_listings(
    brand: str | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    fuel: str | None = None,
    user: User = Depends(authenticate),
) -> ListingSearchResponse:
    """Search listings based on provided query parameters."""
    # NOTE only some params are supported for simplicity
    # TODO make this endpoint paged
    search_query = {
        "brand": brand,
        "min_year": min_year,
        "max_year": max_year,
        "min_price": min_price,
        "max_price": max_price,
        "fuel": fuel,
    }
    await emit_user_search_interest(user, search_query)
    listings = await query_listings(**search_query)
    return ListingSearchResponse(listings=listings)


@router.get("/recommendations")
async def get_recommendations(
    user: User = Depends(authenticate),
) -> ListingRecommendationResponse:
    """Return car listing recommendations for the authenticated user."""
    recommendations = await similarity_search(user.preference)
    return ListingRecommendationResponse(recommended=recommendations)


async def get_listing(listing_id: int) -> Listing:
    """Get listing details from the DB."""
    async with get_async_session() as session:
        statement = select(Listing).where(Listing.id == listing_id)
        rows = await session.execute(statement)
        row = rows.first()
        return row[0]


async def query_listings(
    brand: Optional[str] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    fuel: Optional[str] = None,
) -> List:
    """Query Listings based on given params."""
    async with get_async_session() as session:
        # NOTE the performance of this query will probably be atrocious
        stmt = select(Listing)
        if brand is not None:
            stmt = stmt.where(Listing.brand == brand)
        if fuel is not None:
            stmt = stmt.where(Listing.fuel == fuel)
        if min_year is not None:
            stmt = stmt.where(Listing.year >= min_year)
        if max_year is not None:
            stmt = stmt.where(Listing.year <= max_year)
        if min_price is not None:
            stmt = stmt.where(Listing.selling_price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Listing.selling_price <= max_price)
        stmt = stmt.limit(__LISTING_SEARCH_LIMIT)
        rows = await session.execute(stmt)
        return list(map(lambda row: row[0].to_dict(), rows))


async def similarity_search(user_preference: np.array):
    """Do euclidean distance similarity search based on user preference vector."""

    def raw_to_structured(row):
        """Extract data corresponding to a ListingShortResponse
        from a raw response.
        """
        return {
            "id": row[0],
            "brand": row[1],
            "name": row[2],
            "selling_price": row[4],
        }

    async with get_async_session() as session:
        query = __SIMILARITY_QUERY.format(
            user_preference=np.array2string(user_preference, separator=",")
        )
        rows = await session.execute(text(query))
        return list(map(raw_to_structured, rows))


async def emit_user_search_interest(user: User, search_query: dict):
    """Emit message to RMQ about user search activity."""
    payload = {
        "user": user.id,
        "search_query": [],
    }
    await publish("interest:search", payload)


async def emit_user_detail_interest(user: User, listing: Listing):
    """Emit message about user Listing interest."""
    payload = {
        "user": user.id,
        "listing": listing.id,
    }
    await publish("interest:detail", payload)
