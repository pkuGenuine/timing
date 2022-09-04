from account.models import Account


def add_user_info(user: Account, frontend_dict: dict):
    frontend_dict.update(use_navbar=True)