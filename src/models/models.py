from extensions import db, ma
from datetime import datetime


class Brand(db.Model):
    __tablename__ = "brands"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100),
        nullable=False,
        comment="The name of the brand, e.g., Nike, Adidas, etc.",
    )
    description = db.Column(db.String(255), comment="A brief description of the brand.")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100),
        nullable=False,
        comment="The name of the product category, e.g., shoes, shirts, etc.",
    )
    description = db.Column(
        db.String(255), comment="A brief description of the category."
    )


class Sport(db.Model):
    __tablename__ = "sports"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100),
        nullable=False,
        comment="The name of the sport associated with the product, e.g., football, basketball.",
    )


class Gender(db.Model):
    __tablename__ = "genders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(50),
        nullable=False,
        comment="The target gender for the product, e.g., male, female, unisex.",
    )


class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        comment="The country of origin for the product, e.g., USA, China.",
    )


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False, comment="The name of the product.")

    description = db.Column(
        db.Text, nullable=False, comment="A detailed description of the product."
    )

    price = db.Column(
        db.Float, nullable=False, comment="The regular price of the product."
    )

    discount_price = db.Column(db.Float, comment="The discounted price, if applicable.")

    image_url = db.Column(db.String(255), comment="URL to the product's image.")

    brand_id = db.Column(
        db.Integer,
        db.ForeignKey("brands.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key linking to the brand associated with the product.",
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key linking to the product's category.",
    )

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sports.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key linking to the sport associated with the product.",
    )

    gender_id = db.Column(
        db.Integer,
        db.ForeignKey("genders.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key linking to the target gender for the product.",
    )

    country_id = db.Column(
        db.Integer,
        db.ForeignKey("countries.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key linking to the country of origin for the product.",
    )

    composition = db.Column(
        db.String(255), comment="The composition or material of the product."
    )

    # Relationships
    brand = db.relationship("Brand", backref="products")
    category = db.relationship("Category", backref="products")
    sport = db.relationship("Sport", backref="products")
    gender = db.relationship("Gender", backref="products")
    country = db.relationship("Country", backref="products")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(500),
        unique=True,
        nullable=False,
        comment="The user's email, used for login and communication.",
    )

    password = db.Column(
        db.String(350), nullable=False, comment="The hashed password of the user."
    )

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key that connects the user to a role.",
    )

    email_verified = db.Column(
        db.Boolean,
        default=False,
        comment="Indicates whether the user's email has been verified.",
    )

    reset_token = db.Column(
        db.String(128), nullable=True, comment="Token used for password recovery."
    )

    reset_token_expiry = db.Column(
        db.DateTime,
        nullable=True,
        comment="Expiration date of the password recovery token.",
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        comment="The timestamp when the user account was created.",
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="The timestamp when the user account was last updated.",
    )

    # Relationship to the Role model
    role = db.relationship("Role", back_populates="users")


# Model for roles


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
        comment="The name of the role, e.g., 'admin', 'user'.",
    )

    # One role can have many users
    users = db.relationship("User", back_populates="role")
