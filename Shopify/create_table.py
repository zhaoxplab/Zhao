from .utils import create_app
from .models import db

app = create_app()

with app.test_request_context():
    db.drop_all()
    db.create_all()
