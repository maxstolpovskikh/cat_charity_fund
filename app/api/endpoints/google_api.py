from typing import Any

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (create_spreadsheet, set_user_permissions,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    response_model=list[dict[str, Any]],
    dependencies=[Depends(current_superuser)],
    summary='Создать отчёт'
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await create_spreadsheet(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    projects,
                                    wrapper_services)
    return projects
