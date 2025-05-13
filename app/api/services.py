from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

#from app.crud.charity_project import charity_project_crud
#from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def close_object_if_invested(
    obj: Union[CharityProject, Donation],
):
    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


async def invest_money(
    session: AsyncSession,
):
    projects_query = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(False)
        ).order_by(
            CharityProject.create_date
        )
    )
    projects = projects_query.scalars().all()
    if not projects:
        return

    donations_query = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False)
        ).order_by(
            Donation.create_date
        )
    )
    donations = donations_query.scalars().all()
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
                if donation.full_amount == donation.invested_amount:
                    donation.fully_invested = True
                    donation.close_date = datetime.now()

                need_to_invest -= donate_available
            else:
                project.invested_amount += need_to_invest
                donation.invested_amount += need_to_invest
                need_to_invest = 0

            if need_to_invest == 0:
                if project.full_amount == project.invested_amount:
                    project.fully_invested = True
                    project.close_date = datetime.now()
                break

    await session.commit()