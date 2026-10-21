from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[CategoryORM]:
        return list(self.db.scalars(select(CategoryORM)).all())

    def get_by_id(self, category_id: str) -> CategoryORM:
        category: CategoryORM | None = self.db.get(CategoryORM, category_id)
        return category

    def create(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete(self, category_id: str) -> bool:
        category = self.get_by_id(category_id)
        if category is None:
            return False
        self.db.delete(category)
        self.db.commit()
        return True
