from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_uninvested(
    model,
    session: AsyncSession,
):
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
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def distribute_donation(
    donation: Donation,
    projects: List[CharityProject]
):
    updated_projects = []
    donation_used = False
    for project in projects:
        if project.fully_invested:
            continue
        need_to_invest = project.full_amount - project.invested_amount
        donate_available = donation.full_amount - donation.invested_amount
        if donate_available <= need_to_invest:
            project.invested_amount += donate_available
            donation.invested_amount = donation.full_amount
            await close(donation)
            donation_used = True
            if project.full_amount == project.invested_amount:
                await close(project)
            updated_projects.append(project)
            break
        else:
            project.invested_amount = project.full_amount
            donation.invested_amount += need_to_invest
            await close(project)
            updated_projects.append(project)
            if donation.full_amount == donation.invested_amount:
                await close(donation)
                donation_used = True
                break

    return updated_projects, donation_used


async def process_donations(
    donations: List[Donation],
    projects: List[CharityProject],
    session: AsyncSession
):
    if not donations or not projects:
        return
    for donation in donations:
        if donation.fully_invested:
            continue
        updated_projects, donation_used = await distribute_donation(
            donation, projects
        )
        if updated_projects or donation_used:
            await session.commit()


async def invest(
    session: AsyncSession,
):
    projects = await get_uninvested(CharityProject, session)
    donations = await get_uninvested(Donation, session)
    await process_donations(donations, projects, session)