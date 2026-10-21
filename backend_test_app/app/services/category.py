from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryReadSchema, CategoryCreateUpdateSchema


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> List[CategoryReadSchema]:
        categories_orm = self.category_repository.get_all()
        return [CategoryReadSchema.model_validate(category) for category in categories_orm]

    def create_category(self, category_create: CategoryCreateUpdateSchema) -> CategoryReadSchema:
        categories_orm = self.category_repository.create(name=category_create.name)

        self.db.commit()
        return CategoryReadSchema.model_validate(categories_orm)

    def update_category(self, category_id: str, category_update: CategoryCreateUpdateSchema) -> CategoryReadSchema:
        category_for_update = self.category_repository.get_by_id(category_id)

        if category_update is None:
            raise HTTPException(status_code=404, detail="Category not found")

        category_for_update.name = category_update.name
        self.db.commit()
        return CategoryReadSchema.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        if not self.category_repository.delete(category_id):
            raise HTTPException(status_code=404, detail="Category not found")
