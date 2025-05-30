from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationAdminDB, DonationCreate, DonationDB

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationAdminDB],
    dependencies=[Depends(current_superuser)],
    summary='Список всех пожертвований'
)
async def get_all(
        session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'},
    summary='Список ваших пожертвований'
)
async def get_my(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_by_user(
        session=session, user=user
    )


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary='Создать пожертвование'
)
async def create(
        donation_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await donation_crud.create_with_investment(
        donation_in, session, user
    )
