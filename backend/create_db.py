# run_once.py
from app.database import Base, engine
from app.models import user  # <-- ensure this imports the User model

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✅ Tables dropped and recreated.")
