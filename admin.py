from os import environ
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import User
from app.models import Admin

if "SQLALCHEMY_DATABASE_URI" not in environ:
    load_dotenv()

SQLALCHEMY_DATABASE_URI = environ['SQLALCHEMY_DATABASE_URI']

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    pool_size=1,
    max_overflow=2
)

factory = sessionmaker(bind=engine)


class AdminController:
    def __init__(self) -> None:
        self.session = factory()

    def print(self):
        admin_list: list[Admin] = self.session.query(Admin).all()

        id_length = 8

        print("| admin id |  user id |      created at     | user email")
        for admin in admin_list:
            print(
                "| ",
                admin.id,
                " " * (id_length - len(str(admin.id))),
                " | ",
                admin.user,
                " " * (id_length - len(str(admin.user))),
                " | ",
                admin.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                " |      ",
                self.session.query(User).filter_by(
                    id=admin.user
                ).with_entities(
                    User.email
                ).first().email,
                sep=""
            )

    def select(self, user_id: int) -> Admin:
        return self.session.query(Admin).filter_by(
            user=user_id
        ).first()

    def search(self, user_id: int) -> User:
        return self.session.query(User).filter_by(
            id=user_id
        ).first()

    def update(self, obj):
        if isinstance(obj, int):
            user_id: int = obj

            ad = Admin()
            ad.user = user_id
            ad.created_at = datetime.now()

            self.session.add(ad)
            self.session.commit()
        else:
            ad: Admin = obj
            self.session.delete(ad)
            self.session.commit()


if __name__ == "__main__":
    ac = AdminController()
    ac.print()

    try:
        user_id = int(input("user_id: "))
    except (TypeError, ValueError):
        print("Wrong user_id inputed, program exited!")
        exit(2)

    admin = ac.select(user_id)

    if admin is None:
        print("Normal user selected.")
        ac.update(user_id)
    else:
        print("Admin selected.")
        ac.update(admin)

    print()
    ac.print()
