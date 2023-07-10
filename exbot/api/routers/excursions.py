import secrets
from typing import Annotated, List
from datetime import datetime

import fastapi
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from utils.tools import save_file_from_response, save_addition_files
from database import base, crud, schemas

router = APIRouter(
    prefix="/api/excursions",
    tags=["Excursions"],
    dependencies=[Depends(crud.admins.get_current_admin)],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_excursion(
        title: str,
        intro: str,
        description: str,
        image: UploadFile,
        is_published: bool,
        session: AsyncSession = Depends(base.get_session),
):
    num_of_ex = await crud.excursions.get_number_of_excursions(db=session)
    image_path = save_file_from_response(
        folder=f"ex_{num_of_ex + 1}", file=image.file, filename=image.filename
    )
    excursion = schemas.ExcursionCreate(
        title=title,
        intro=intro,
        description=description,
        image=image_path,
        is_published=is_published,
    )

    await crud.excursions.create_excursion(excursion=excursion, db=session)
    return {
        "message": f"Excursion {excursion.title} was successfully created",
        "excursion": excursion,
    }


@router.get("/")
async def get_excursions(session: AsyncSession = Depends(base.get_session)):
    excursions = await crud.excursions.get_excursions(db=session)
    return {"excursions": excursions}


@router.get("/{pk}", response_model=schemas.Excursion)
async def retrieve_excursion(
        pk: int, session: AsyncSession = Depends(base.get_session)
):
    excursion = await crud.excursions.retrieve_excursion(pk, session)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    return excursion


@router.put("/{pk}", response_model=schemas.Excursion)
async def update_excursion(
        pk: int,
        data: schemas.ExcursionCreate,
        session: AsyncSession = Depends(base.get_session),
):
    excursion = await crud.excursions.retrieve_excursion(pk, session)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    return await crud.excursions.update_excursion(excursion, data, session)


@router.delete("/{pk}")
async def delete_excursion_endpoint(
        pk: int, session: AsyncSession = Depends(base.get_session)
):
    excursion = await crud.excursions.retrieve_excursion(pk, session)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    await crud.excursions.delete_excursion(excursion, session)
    return {f"Excursion {pk} successfully deleted"}


@router.post("/questions/{excursion_id}")
async def create_excursion_questions(
        excursion_id: int,
        question_id: int,
        place_picture: UploadFile,
        answer: str,
        hint: str,
        question_image: UploadFile,
        correct: str,
        final: str,
        addition: List[UploadFile],
        session: AsyncSession = Depends(base.get_session),
):
    folder_name = f"ex_{excursion_id}"
    place_picture_path = save_file_from_response(
        folder=f"{folder_name}/{question_id}",
        file=place_picture.file,
        filename=place_picture.filename,
    )
    question_image_path = save_file_from_response(
        folder=f"{folder_name}/{question_id}",
        file=question_image.file,
        filename=question_image.filename,
    )
    addition_content = save_addition_files(
        folder=f"{folder_name}/{question_id}/addition", files=addition
    ) if addition else None

    question = schemas.QuestionCreate(
        id=question_id,
        place=place_picture_path,
        answer=answer,
        hint=hint,
        text=question_image_path,
        correct=correct,
        addition=addition_content,
        final=final,
    )
    question = await crud.questions.create_question(
        question=question, db=session, excursion_id=excursion_id
    )
    return question
