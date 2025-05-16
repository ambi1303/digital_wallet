# create_db.py
from app.database import Base, engine
from app.models import user
from app.models import transaction


Base.metadata.create_all(bind=engine)
