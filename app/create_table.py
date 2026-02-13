from app.database import engine, Base
from app.models import practitioner

Base.metadata.create_all(bind=engine)
print("succesfully craated")