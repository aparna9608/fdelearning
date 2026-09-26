from sqlalchemy.orm import Session

from models import Customer


def get_customer(
    db: Session,
    customer_id: int
):
    return (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )


def get_customers(db: Session):
    return db.query(Customer).all()


def create_customer(
    db: Session,
    name: str,
    role: str
):
    customer = Customer(
        name=name,
        role=role
    )

    db.add(customer)

    return customer

##update customer
def update_customer(
    db: Session,
    customer_id: int,
    name: str,
    role: str
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if customer is None:
        return None

    customer.name = name
    customer.role = role

    return customer

##patch customer
def patch_customer(
    db: Session,
    customer_id: int,
    name: str | None = None,
    role: str | None = None
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if customer is None:
        return None

    if name is not None:
        customer.name = name

    if role is not None:
        customer.role = role

    return customer

##delete customer
def delete_customer(db: Session, customer_id: int):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if customer is None:
        return None

    db.delete(customer)

    return customer