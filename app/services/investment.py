from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.base import AbstractBaseModel


async def get_uninvested(
    model,
    session: AsyncSession,
) -> List:
    """Получает неинвестированные объекты модели."""
    objects = await session.execute(
        select(model).where(
            model.fully_invested.is_(False)
        ).order_by(
            model.create_date
        )
    )
    return objects.scalars().all()


async def close(
    obj: Union[CharityProject, Donation]
):
    """Закрывает объект как полностью проинвестированный."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def invest_funds(
    sources: List[AbstractBaseModel],
    targets: List[AbstractBaseModel],
    session: AsyncSession
) -> None:
    """Распределяет средства между источниками и целями инвестирования."""
    for source in sources:
        await session.refresh(source)
        if source.fully_invested:
            continue
        for target in targets:
            if target.fully_invested:
                continue
            invest_amount = min(
                source.available_amount,
                target.available_amount
            )
            if invest_amount > 0:
                source.invest(invest_amount)
                target.invest(invest_amount)
            if source.fully_invested:
                break
        await session.commit()


async def invest(session: AsyncSession) -> None:
    """Инвестирует пожертвования в благотворительные проекты."""
    projects = await get_uninvested(CharityProject, session)
    donations = await get_uninvested(Donation, session)
    await invest_funds(donations, projects, session)