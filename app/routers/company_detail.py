"""
Enhanced company detail endpoint with normalized metadata.
Uses Motor (async MongoDB) for non-blocking queries.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from bson import ObjectId
from app.db_motor import get_collection
from app.utils.normalization import normalize_business_response
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/companies", tags=["Company Detail"])


@router.get("/{id}/detail")
async def get_company_detail(id: str) -> Dict[str, Any]:
    """
    Get detailed company information by ID with fully normalized metadata.

    Returns complete business data including:
    - All core fields (name, location, rating, etc.)
    - Lead score and tier
    - Completeness flags
    - Enrichment fields needed
    - Email data (if enriched)
    """
    coll = get_collection()

    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid company ID format")

    try:
        business = await coll.find_one({"_id": oid})

        if not business:
            raise HTTPException(status_code=404, detail="Company not found")

        business["_id"] = str(business["_id"])
        normalized = normalize_business_response(business)
        return normalized

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching company detail: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{id}/score-breakdown")
async def get_score_breakdown(id: str) -> Dict[str, Any]:
    """
    Get detailed lead score breakdown for a company.
    Returns just the lead scoring data with detailed breakdown.
    """
    coll = get_collection()

    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid company ID format")

    try:
        business = await coll.find_one({"_id": oid})

        if not business:
            raise HTTPException(status_code=404, detail="Company not found")

        lead_score = business.get("lead_score", {})

        if not lead_score or not lead_score.get("total_score"):
            return {
                "company_id": id,
                "company_name": business.get("name", ""),
                "lead_score": {
                    "message": "Lead score not yet calculated."
                }
            }

        return {
            "company_id": id,
            "company_name": business.get("name", ""),
            "lead_score": lead_score
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching score breakdown: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
