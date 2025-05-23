from typing import Any, List

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.services.investment import invest


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ):
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def create_with_investment(
            self,
            obj_in,
            session: AsyncSession,
    ) -> List[dict[str, Any]]:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await invest(session)
        await session.refresh(db_obj)
        return db_obj

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ):
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(
                extract('epoch', CharityProject.close_date) - extract(
                    'epoch', CharityProject.create_date
                )))
        projects = projects.scalars().all()

        res = [
            {
                'name': project.name,
                'delta': str(project.close_date - project.create_date),
                'description': project.description
            }
            for project in projects
        ]

        return res


charity_project_crud = CRUDCharityProject(CharityProject)
