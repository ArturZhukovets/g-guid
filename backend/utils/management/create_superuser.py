from core.hashing import Hasher
from db.db import SessionLocal
from db.models.exersices import Exercise
from db.models.users import User


def manage_create_superuser():
    with SessionLocal() as session:
        while True:
            username = input("Enter the username: ")
            password = input("Enter the password (more then 4 symbols): ")
            user = User(
                name=username,
                password=Hasher.get_password_hash(password),
                is_superuser=True,
            )
            try:
                session.add(user)
                session.commit()
                break
            except Exception as ex:
                print(ex)
                is_stop = input("Try it again? [y, n]: ")
                if is_stop == "n":
                    print("You exit from superuser creation script")
                    break
        print(f"The superuser - {user.name} was successfully created!")
