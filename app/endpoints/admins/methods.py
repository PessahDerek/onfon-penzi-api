from app.models.admin_model import Admin
from app.extensions import bcrypt, db


def seed_admin(username: str, password: str) -> Admin:
    try:
        new_admin = Admin()
        new_admin.username = username
        new_admin.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.add(new_admin)
        db.session.commit()
        return new_admin
    except Exception as e:
        raise Exception(e)
