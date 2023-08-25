from fastapi import APIRouter, Depends, Request, status
from schemas import (ModelInput, Model)
from schemas.response import Response
from fastapi.responses import Response as fastapiResponse
from .auth_endpoints import get_current_active_user
from bson import ObjectId
from utils.helpers import get_now_timestamp

router = APIRouter()


@router.post('/model', response_model=Response)
async def insert_model(request: Request,
                       model_input: ModelInput,
                       user=Depends(get_current_active_user)):

    now = get_now_timestamp()
    model = Model(**model_input.dict(),
                  user=user,
                  last_modified_at=now,
                  created_at=now)
    await model.create()
    id = str(model.id)
    return Response(status=status.HTTP_201_CREATED,
                    message='successfull',
                    data={'id': str(id)})


@router.get('/model')
async def get_all_model(request: Request,
                        user=Depends(get_current_active_user)):
    models: Model = await Model.find(
        Model.user.id == user.id
    ).to_list()

    return Response(data=models, message='successfull', status=status.HTTP_200_OK)


@router.get('/model/{id}')
async def get_model(request: Request,
                    id: str,
                    user=Depends(get_current_active_user)):
    model: Model = await Model.find_one(
        Model.id == ObjectId(id),
        Model.user.id == user.id
    )
    if not model:
        return Response(status=status.HTTP_404_NOT_FOUND, message='not found', data={})

    return Response(data=model, message='successfull', status=status.HTTP_200_OK)


@router.put('/model/{id}')
async def edit_model(request: Request,
                     id: str,
                     model_input: ModelInput,
                     user=Depends(get_current_active_user)):
    model: Model = await Model.find_one(
        Model.id == ObjectId(id),
        Model.user.id == user.id
    )
    if not model:
        return Response(status=status.HTTP_404_NOT_FOUND, message='not found', data={})
    now = get_now_timestamp()
    model.last_modified_at = now
    model.name = model_input.name
    model.design_flow = model_input.design_flow
    model.report_flow = model_input.report_flow
    model.description = model_input.description
    model.is_public = model_input.is_public
    model.usage = model_input.usage
    model.last_modified = model_input.last_modified

    await model.save()
    return Response(data={'id': str(id)}, message='successfull',
                    status=status.HTTP_200_OK)


@router.delete('/model/{id}')
async def delete_model(request: Request,
                       id: str,
                       user=Depends(get_current_active_user)):
    model: Model = await Model.find_one(
        Model.id == ObjectId(id),
        Model.user.id == user.id
    )
    if not model:
        return Response(status=status.HTTP_404_NOT_FOUND, message='not found', data={})
    await model.delete()
    return fastapiResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
