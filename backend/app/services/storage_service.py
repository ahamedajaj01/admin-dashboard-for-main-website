# app/services/storage_service.py

import logging
from app.config import SUPABASE_URL, SUPABASE_STORAGE_BUCKET
from supabase import create_client
from app.config import SUPABASE_SERVICE_ROLE_KEY

logger = logging.getLogger(__name__)
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def resolve_image_url(value: str) -> str:
    if not value:
        return ""

    # old Appwrite URL → return as-is
    if value.startswith("http"):
        return value

     # NEW: public bucket URL (no signing)
    return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/{value}"