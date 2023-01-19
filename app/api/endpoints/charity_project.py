from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_active,
                                check_project_exists,
                                check_project_has_investment,
                                check_project_updated_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.models.donation import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import donation_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    new_project = await donation_process(new_project, Donation, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude={'close_date'}
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    project = await check_project_active(project, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if not obj_in.full_amount:
        project = await project_crud.update(
            project, obj_in, session
        )
        return project
    await check_project_updated_amount(
        obj_in.full_amount,
        project.invested_amount,
        session
    )
    project = await project_crud.update(project, obj_in, session)
    project = await donation_process(project, Donation, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    await check_project_has_investment(project, session)
    project = await project_crud.remove(project, session)
    return project
