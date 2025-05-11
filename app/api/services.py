from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_uninvested_objects(
    model_in,
    session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(model_in).where(
            model_in.fully_invested == False
        ).order_by(
            model_in.create_date
        )
    )
    return objects.scalars().all()


async def close_object_if_invested(
    obj: Union[CharityProject, Donation],
) -> None:
    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


async def invest_money(
    session: AsyncSession,
) -> None:
    projects = await get_uninvested_objects(CharityProject, session)
    if not projects:
        return

    donations = await get_uninvested_objects(Donation, session)
    if not donations:
        return

    for project in projects:
        if project.fully_invested:
            continue

        need_to_invest = project.full_amount - project.invested_amount

        for donation in donations:
            if donation.fully_invested:
                continue

            donate_available = donation.full_amount - donation.invested_amount

            if donate_available <= need_to_invest:
                project.invested_amount += donate_available
                donation.invested_amount = donation.full_amount
                await close_object_if_invested(donation)

                need_to_invest -= donate_available
            else:
                project.invested_amount += need_to_invest
                donation.invested_amount += need_to_invest
                need_to_invest = 0

            if need_to_invest == 0:
                await close_object_if_invested(project)
                break

    await session.commit()