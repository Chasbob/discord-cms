from typing import List


def make_crud(model):
    class CRUD:
        def list(db, **kwargs) -> List[model]:
            items = db.query(model).filter_by(**kwargs).all()
            return items

        def count(db, **kwargs) -> int:
            count = db.query(model).filter_by(**kwargs).count()
            return count

        def get(db, **kwargs) -> model:
            item = db.query(model).filter_by(**kwargs).first()
            return item

        def create(db, **kwargs) -> model:
            item = model(**kwargs)
            db.add(item)
            db.commit()
            db.refresh(item)

            return item

        def create_from_dict(db, obj) -> model:
            item = model(obj)
            db.add(item)
            db.commit()
            db.refresh(item)

            return item

        def get_or_create(db, **kwargs) -> model:
            # item = CRUD.get(db, **kwargs)
            if (item := CRUD.get(db, **kwargs)):
                return item
            else:
                return CRUD.create(db, **kwargs)

        def delete(db, **kwargs) -> None:
            count = db.query(model).filter_by(**kwargs).delete()
            db.commit()
            return count > 0

    return CRUD
