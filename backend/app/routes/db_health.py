from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/db")
def check_database_connection(user = Depends(get_current_user)):
    try:
        # This calls PostgREST root — no tables required
        supabase.postgrest.session.get("/").raise_for_status()

        return {
            "database": "supabase",
            "connected": True,
            "status": "ok"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "database": "supabase",
                "connected": False,
                "error": str(e)
            }
        )
