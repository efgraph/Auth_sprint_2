from app import app
from db.config import db
from service.account import AccountService
from service.exceptions import UserAlreadyExists

with app.app_context():
    account_service = AccountService(db)
    try:
        account_service.register('admin', 'admin', 'admin@admin.com', True)
    except UserAlreadyExists:
        pass