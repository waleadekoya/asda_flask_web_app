from app import db
from sqlalchemy.ext.automap import automap_base
from flask_security import RoleMixin, UserMixin

# Connect to existing table
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Product = Base.classes.Product
ProductCategory = Base.classes.ProductCategory

# Creating new database table
db.Model.metadata.reflect(db.engine)
# db.metadata.reflect(db.engine)


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
    extend_existing=True,
)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    def is_active(self):
        return True

    def __repr__(self):
        return "User({})".format(self.email)


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# Custom User Payload
# https://flask-security.readthedocs.io/en/3.0.0/models.html
def get_security_payload(self):
    return {"id": self.id, "name": self.name, "email": self.email}
