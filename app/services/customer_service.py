from sqlalchemy.orm import Session

from app.repositories.customer_repository import (
    get_customer,
    get_customers,
    create_customer as create_customer_repository,
    update_customer as update_customer_repository,
    patch_customer as patch_customer_repository,
    delete_customer as delete_customer_repository,
)


def find_customer(
    db: Session,
    customer_id: int
):
    return get_customer(db, customer_id)


def list_customers(db: Session):
    return get_customers(db)


def create_customer(
    db: Session,
    name: str,
    role: str
):
    try:
        customer = create_customer_repository(
            db=db,
            name=name,
            role=role
        )

        db.commit()
        db.refresh(customer)

        return customer

    except Exception:
        db.rollback()
        raise


def update_customer(
    db: Session,
    customer_id: int,
    name: str,
    role: str
):
    try:
        customer = update_customer_repository(
            db=db,
            customer_id=customer_id,
            name=name,
            role=role
        )

        if customer is None:
            return None

        db.commit()
        db.refresh(customer)

        return customer

    except Exception:
        db.rollback()
        raise    

def patch_customer(
    db: Session,
    customer_id: int,
    name: str = None,
    role: str = None
):
    try:
        customer = patch_customer_repository(
            db=db,
            customer_id=customer_id,
            name=name,
            role=role
        )

        if customer is None:
            return None

        db.commit()
        db.refresh(customer)

        return customer

    except Exception:
        db.rollback()
        raise    

##delete customer
def delete_customer(db: Session, customer_id: int):
    try:
        customer = delete_customer_repository(
            db=db,
            customer_id=customer_id
        )

        if customer is None:
            return None

        db.commit()

        return customer

    except Exception:
        db.rollback()
        raise