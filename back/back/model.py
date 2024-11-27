from back import db
from flask_security import UserMixin, RoleMixin


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


# Define User and Role models with mixins
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship(
        "Role", secondary="roles_users", backref=db.backref("users", lazy="dynamic")
    )
    cart = db.relationship(
        "Cart", backref="users", lazy=True, cascade="all, delete-orphan"
    )
    products = db.relationship(
        "Product", backref="managers", lazy=True, cascade="all, delete-orphan"
    )
    active = db.Column(db.Boolean)

    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=True)
    expiry = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    subcat_id = db.Column(db.Integer, db.ForeignKey("subcategory.id"), nullable=False)
    upload_id = db.Column(db.Integer, db.ForeignKey("upload.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    cart = db.relationship(
        "Cart", backref="products", lazy=True, cascade="all, delete-orphan"
    )
    description = db.Column(db.String(500))

    def __repr__(self):
        return f"Product('{self.name}', '{self.expiry}', '{self.description}')"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.expiry}', '{self.description}')"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    subcats = db.relationship(
        "Subcategory", backref="cat", lazy=True, cascade="all, delete-orphan"
    )
    upload_id = db.Column(db.Integer, db.ForeignKey("upload.id"), nullable=False)
    approval = db.Column(db.String(20), default="admin")

    def __repr__(self):
        return f"Cat('{self.name}', '{self.image_file}')"


class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    upload_id = db.Column(db.Integer, db.ForeignKey("upload.id"), nullable=False)
    products = db.relationship(
        "Product", backref="subcat", lazy=True, cascade="all, delete-orphan"
    )
    approval = db.Column(db.String(20), default="admin")

    def __repr__(self):
        return f"Subcat('{self.name}', '{self.image_file}')"


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    subcat = db.relationship(
        "Subcategory", backref="upload", lazy=True, cascade="all, delete-orphan"
    )
    cat = db.relationship(
        "Category", backref="upload", lazy=True, cascade="all, delete-orphan"
    )
    product = db.relationship(
        "Product", backref="upload", lazy=True, cascade="all, delete-orphan"
    )
