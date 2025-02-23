
import sys
sys.path.append("..")

from controllers import supabase_handler
from fastapi import APIRouter, HTTPException


image_router = APIRouter(prefix="/image")

@image_router.get("/latest")
async def fetch_latest_image_from_supabase():
    try:
        image_url = await supabase_handler.fetch_latest_image_from_supabase()
        if image_url:
            return {"status": 200, "image_url": image_url}
        else:
            return {"status": 200, "image_url": None}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))