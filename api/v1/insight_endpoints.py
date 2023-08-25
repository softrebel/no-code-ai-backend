from fastapi import APIRouter, Depends, Request, status
from models import (InsightInputModel, InsightModel)
from models.response import Response
from fastapi.responses import Response as fastapiResponse
from .auth_endpoints import get_current_active_user
from bson import ObjectId
router = APIRouter()


@router.post('/insight', response_model=Response)
async def insert_insight(request: Request,
                         insight_input: InsightInputModel,
                         user=Depends(get_current_active_user)):

    insight = InsightModel(**insight_input.dict(), user=user)
    await insight.create()
    id = str(insight.id)
    return Response(status=status.HTTP_201_CREATED,
                    message='successfull',
                    data={'id': str(id)})


@router.get('/insight/{id}')
async def get_insight(request: Request,
                      id: str,
                      user=Depends(get_current_active_user)):
    insight: InsightModel = await InsightModel.find_one(
        InsightModel.id == ObjectId(id),
        InsightModel.user.id == user.id
    )
    if not insight:
        return Response(status=status.HTTP_404_NOT_FOUND, message='not found', data={})

    return Response(data=insight, message='successfull', status=status.HTTP_200_OK)


@router.put('/insight/{id}')
async def edit_insight(request: Request,
                       id: str,
                       insight_input: InsightInputModel,
                       user=Depends(get_current_active_user)):
    insight: InsightModel = await InsightModel.find_one(
        InsightModel.id == ObjectId(id),
        InsightModel.user.id == user.id
    )
    if not insight:
        return Response(status=status.HTTP_404_NOT_FOUND, message='not found', data={})

    insight.name = insight_input.name
    insight.settingData = insight_input.settingData
    insight.mtag = insight_input.mtag
    insight.rtag = insight_input.rtag
    insight.description = insight_input.description
    insight.access = insight_input.access
    insight.image = insight_input.image
    insight.canvas = insight_input.canvas

    await insight.save()
    return Response(data={'id': str(id)}, message='successfull', status=status.HTTP_200_OK)


@router.delete('/insight/{id}')
async def delete_insight(request: Request,
                         id: str,
                         user=Depends(get_current_active_user)):
    insight: InsightModel = await InsightModel.find_one(
        InsightModel.id == ObjectId(id),
        InsightModel.user.id == user.id
    )
    if not insight:
        return Response(status=status.HTTP_404_NOT_FOUND, message='not found', data={})
    await insight.delete()
    return fastapiResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
