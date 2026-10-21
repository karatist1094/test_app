from fastapi import status, Depends, APIRouter
from typing import List
from app.api.dependencies import get_category_service
from app.schemas.category import CategoryReadSchema, CategoryCreateUpdateSchema
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("")
def read_(category_service: CategoryService = Depends(get_category_service)) -> List[CategoryReadSchema]:
    return category_service.list_categories()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
        payload: CategoryCreateUpdateSchema,
        category_service: CategoryService = Depends(get_category_service)) -> CategoryReadSchema:
    return category_service.create_category(payload)


@router.patch("/{category_id}")
def update_category(
        category_id: str,
        payload: CategoryCreateUpdateSchema,
        category_service: CategoryService = Depends(get_category_service)) -> CategoryReadSchema:
    return category_service.update_category(category_id, payload)


@router.delete("/{category_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: str,
        category_service: CategoryService = Depends(get_category_service)):
    category_service.delete_category(category_id)