import os
from fastapi import APIRouter, Depends, Request, status
from schemas import File
from schemas.response import Response
from fastapi.responses import FileResponse, Response as fastapiResponse
from .auth_endpoints import get_current_active_user
from fastapi import UploadFile
from configs.settings import settings
import uuid
from bson import ObjectId

router = APIRouter()


@router.post("/file", response_model=Response)
async def upload_file(
    request: Request, file: UploadFile, user=Depends(get_current_active_user)
):
    id = str(user.id)
    content_type = file.content_type
    original_filename = file.filename
    filename = str(uuid.uuid4())
    contents = await file.read()
    file_dir = settings.FILES_PATH
    path = f"{file_dir}/{id}"
    if not os.path.exists(path):
        os.mkdir(path=path)
    with open(f"{path}/{filename}", "wb") as f:
        f.write(contents)

    file = File(
        filename=filename,
        original_filename=original_filename,
        content_type=content_type,
        path=path,
        user=user,
    )
    await file.create()
    return Response(
        status=status.HTTP_200_OK,
        message="successfull",
        data={"id": str(file.id), "filename": filename},
    )


@router.get("/file")
async def get_all_files(request: Request, user=Depends(get_current_active_user)):
    files = await File.find(File.user.id == user.id).to_list()
    return Response(status=status.HTTP_200_OK, message="successfull", data=files)


@router.get("/file/{file_id}")
async def get_file(
    request: Request, file_id: str, user=Depends(get_current_active_user)
):
    file = await File.find_one(File.id == ObjectId(file_id), File.user.id == user.id)
    if not file:
        return Response(status=status.HTTP_404_NOT_FOUND, message="not found", data={})

    return Response(status=status.HTTP_200_OK, message="successfull", data=file)


@router.get("/file/{file_id}/download")
async def download_file(
    request: Request, file_id: str, user=Depends(get_current_active_user)
):
    id = str(user.id)
    file_dir = settings.FILES_PATH

    file = await File.find_one(File.id == ObjectId(file_id), File.user.id == user.id)
    if not file:
        return Response(status=status.HTTP_404_NOT_FOUND, message="not found", data={})
    filename = file.filename
    original_filename = file.original_filename
    path = f"{file_dir}/{id}/{filename}"
    if not os.path.exists(path):
        return Response(status=status.HTTP_404_NOT_FOUND, message="not found", data={})

    return FileResponse(
        path=path, filename=original_filename, media_type=file.content_type
    )


@router.delete("/file/{file_id}")
async def delete_file(
    request: Request, file_id: str, user=Depends(get_current_active_user)
):
    id = str(user.id)

    file = await File.find_one(File.id == ObjectId(file_id), File.user.id == user.id)
    if not file:
        return Response(status=status.HTTP_404_NOT_FOUND, message="not found", data={})
    filename = file.filename
    file_dir = settings.FILES_PATH
    path = f"{file_dir}/{id}/{filename}"
    if not os.path.exists(path):
        return Response(status=status.HTTP_404_NOT_FOUND, message="not found", data={})
    os.remove(path)
    await file.delete()
    return fastapiResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
