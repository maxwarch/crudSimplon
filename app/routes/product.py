# from ..models.product_model import Product, ProductCreate, ProductUpdate
from app.models.model import Product, ProductCreate, ProductUpdate

from typing import Annotated, List, Union
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from pydantic import ValidationError
import sqlalchemy
from sqlmodel import Session, create_engine, select

from app.security import get_current_username


def get_engine(req):
    return create_engine(req.app.conn_str)


router = APIRouter(
    prefix="/crud",
    responses={404: {"description": "Not found"}},
)


# CREATE
@router.post("/product", tags=["Product"], status_code=201, response_model=Product, dependencies=[Depends(get_current_username)])
def post_product(req: Request,
                 product: Annotated[
                     ProductCreate,
                     Body(
                         examples=[
                             {
                                 "Name": "testMaxK",
                                 "SafetyStockLevel": 15,
                                 "ProductNumber": "BZ-2036",
                                 "ReorderPoint": 375,
                                 "StandardCost": 100,
                                 "ListPrice": 0,
                                 "DaysToManufacture": 5,
                                 "SellStartDate": "2024-12-24T11:14:37.224Z"
                             }
                         ]
                     )
                 ]):
    try:
        db_product = Product.model_validate(product)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))

    with Session(get_engine(req)) as session:
        try:
            session.add(db_product)
            session.commit()
            session.refresh(db_product)

            return db_product
        except sqlalchemy.exc.IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"{str(e).split('\n')[0]}")


# READ
@router.get("/products/{page}/{limit}", tags=["Products"], response_model=List[Product])
@router.get("/products/{page}", tags=["Products"], response_model=List[Product])
@router.get("/products", tags=["Products"], response_model=List[Product])
def get_products(req: Request, page: Union[int, None] = 1, limit: Union[int, None] = 10):
    page = page if page >= 1 else 1
    page = (page - 1) * limit

    with Session(get_engine(req)) as session:
        query = select(Product).order_by(Product.ProductID).offset(page).limit(limit)
        p = session.exec(query).all()

        if len(p) > 0:
            return p


@router.get("/product/{product_id}", tags=["Product"])
def get_product(req: Request, product_id: int):
    with Session(get_engine(req)) as session:
        query = select(Product).where(Product.ProductID == product_id)
        print(query)

        product_db = session.get(Product, product_id)

        if not product_db:
            raise HTTPException(status_code=404, detail=f"No product for this id {product_id}")

        return product_db


# UPDATE
@router.patch("/product", tags=["Product"], response_model=Product, dependencies=[Depends(get_current_username)])
def patch_product(req: Request,
                  product_id: int,
                  product: Annotated[
                      ProductUpdate,
                      Body(
                          examples=[
                              {
                                  "Name": "testMaxK2",
                                  "SafetyStockLevel": 12
                              }
                          ]
                      )
                  ]):

    with Session(get_engine(req)) as session:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        try:
            product_data = product.model_dump(exclude_unset=True)
            db_product.sqlmodel_update(product_data)
            session.add(db_product)
            session.commit()
            session.refresh(db_product)
            return db_product
        except sqlalchemy.exc.IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"{e.split('\n')[0]}")


# DELETE
@router.delete("/product", tags=["Product"], dependencies=[Depends(get_current_username)])
def delete_product(req: Request, product_id: int):
    with Session(get_engine(req)) as session:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        session.delete(db_product)
        session.commit()

    return True
