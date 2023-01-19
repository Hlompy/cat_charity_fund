from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationMy
from app.services.investment import donation_process

router = APIRouter()


@router.post(
    '/',
    response_model=DonationMy,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation, session, user
    )
    new_donation = await donation_process(new_donation, CharityProject, session)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=List[DonationMy],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> List[DonationMy]:
    user_donations = await donation_crud.get_by_user(user, session)
    return user_donations
