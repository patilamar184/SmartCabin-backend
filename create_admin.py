from app.database.database import SessionLocal
from app.models.admin import Admin
from app.core.security import hash_password

db = SessionLocal()

try:
    email = "admin@smartcabin.com"
    password = "Admin@12345"

    existing_admin = db.query(Admin).filter(
        Admin.email == email
    ).first()

    if existing_admin:
        print("Admin already exists.")
    else:
        admin = Admin(
            name="Platform Admin",
            email=email,
            hashed_password=hash_password(password),
            is_active=True
        )

        db.add(admin)
        db.commit()

        print("Admin account created successfully.")

finally:
    db.close()