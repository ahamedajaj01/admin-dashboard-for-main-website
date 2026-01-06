# from fastapi import APIRouter, Depends, HTTPException
# from app.db.supabase import supabase
# from app.schemas.internship import InternshipCreate, InternshipUpdate
# from app.auth.deps import get_current_user

# router = APIRouter(
#     prefix="/internships",
#     tags=["Internships"]
# )


# @router.get("/")
# def list_internships():
#     res = (
#         supabase
#         .table("internships")
#         .select("*")
#         .order("created_at", desc=True)
#         .execute()
#     )
#     return res.data

# @router.post("/")
# def create_internship(
#     data: InternshipCreate,
#     user = Depends(get_current_user)
# ):
#     res = supabase.table("internships").insert(data.dict()).execute()
#     return res.data


# @router.get("/")
# def get_internships():
#     res = supabase.table("internships").select("*").execute()
#     return res.data


# @router.get("/{internship_id}")
# def get_internship(internship_id: str):
#     res = (
#         supabase
#         .table("internships")
#         .select("*")
#         .eq("id", internship_id)
#         .single()
#         .execute()
#     )
#     return res.data


# @router.put("/{internship_id}")
# def update_internship(
#     internship_id: str,
#     data: InternshipUpdate,
#     user = Depends(get_current_user)
# ):
#     res = (
#         supabase
#         .table("internships")
#         .update(data.dict(exclude_unset=True))
#         .eq("id", internship_id)
#         .execute()
#     )
#     return res.data


# @router.delete("/{internship_id}")
# def delete_internship(
#     internship_id: str,
#     user = Depends(get_current_user)
# ):
#     supabase.table("internships").delete().eq("id", internship_id).execute()
#     return {"status": "deleted"}
