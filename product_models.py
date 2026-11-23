from sqlalchemy import create_engine, String, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional
from datetime import datetime


engine = create_engine(
    "sqlite:///product_models.db",
    echo=True
)

class Base(DeclarativeBase):
    pass

# Category Model
class Category(Base):
    __tablename__ = "categorys"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    category_name: Mapped[str | None] = mapped_column(String(100))

    def __repr__(self):
        return (
            f"Product(id={self.id}, "
            f"name='{self.name}', "
            f"price={self.price})"
        )


Base.metadata.create_all(engine)


print("\nTables created successfully!")


with Session(engine) as session:

    categories = [
         {
            "name": "Electronics",
            "description": "Electronic devices and accessories"
        },
        {
            "name": "Books",
            "description": "Books and educational materials"
        },
        {
            "name": "Clothing",
            "description": "Apparel and fashion"
        }
    ]

    for category_data in categories:
        existing = (
            session.query(Category)
            .filter_by(name=category_data["name"])
            .first()
        )

        if not existing:
            session.add(Category(**category_data))
            print(f"Added category: {category_data['name']}")
        else:
            print(f"Category already exists: {category_data['name']}")


    products = [
        {
            "name": "Laptop",
            "price": 899.99,
            "in_stock": True,
            "category_name": "Electronics"
        },
        {
            "name": "Wireless Mouse",
            "price": 24.99,
            "in_stock": True,
            "category_name": "Electronics"
        },
        {
            "name": "Python Programming",
            "price": 39.99,
            "in_stock": True,
            "category_name": "Books"
        },
        {
            "name": "Database Design",
            "price": 59.99,
            "in_stock": False,
            "category_name": "Books"
        },
        {
            "name": "T-Shirt",
            "price": 19.99,
            "in_stock": True,
            "category_name": "Clothing"
        },
        {
            "name": "Jeans",
            "price": 49.99,
            "in_stock": False,
            "category_name": "Clothing"
        }
    ]

    for product_data in products:
        existing = (
            session.query(Product)
            .filter_by(name=product_data["name"])
            .first()
        )

        if not existing:
            session.add(Product(**product_data))
            print(f"Added product: {product_data['name']}")
        else:
            print(f"Product already exists: {product_data['name']}")

    session.commit()



    print("\n=== All Categories ===")
    for category in session.query(Category).all():
        print(category)

    print("\n=== Products In Stock ===")
    for product in (session.query(Product).filter(Product.in_stock == True).all()):
        print(product)

    print("\n=== Products Under $50 ===")
    for product in (session.query(Product).filter(Product.price < 50).all()):
        print(product)