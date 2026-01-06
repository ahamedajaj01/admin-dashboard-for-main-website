# from fastapi import APIRouter, Depends
# from app.db.supabase import supabase
# from app.schemas.intern import InternCreate, InternUpdate
# from app.auth.deps import get_current_user

# router = APIRouter(
#     prefix="/interns",
#     tags=["Interns"]
# )


# @router.get("/")
# def list_interns():
#     res = (
#         supabase
#         .table("interns")
#         .select("*")
#         .order("start_date", desc=True)
#         .execute()
#     )
#     return res.data



# @router.post("/")
# def create_intern(
#     data: InternCreate,
#     user = Depends(get_current_user)
# ):
#     res = supabase.table("interns").insert(data.dict()).execute()
#     return res.data



# @router.put("/{intern_id}")
# def update_intern(
#     intern_id: str,
#     data: InternUpdate,
#     user = Depends(get_current_user)
# ):
#     res = (
#         supabase
#         .table("interns")
#         .update(data.dict(exclude_unset=True))
#         .eq("id", intern_id)
#         .execute()
#     )
#     return res.data



# @router.delete("/{intern_id}")
# def delete_intern(
#     intern_id: str,
#     user = Depends(get_current_user)
# ):
#     supabase.table("interns").delete().eq("id", intern_id).execute()
#     return {"status": "deleted"}
