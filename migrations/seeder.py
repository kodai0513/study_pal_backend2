import bcrypt
from sqlmodel import Session, or_

from app.db.session import _engine  # type: ignore
from app.models.model import Role, User


def seed():
    with Session(_engine) as session:
        # すでにデータがあるかチェック
        from sqlmodel import select

        statement = select(User).where(
            User.id == "f2b021a4-8026-4c4d-bc23-0cf4f6cd389b"
        )
        result = session.exec(statement)
        if result.first() is None:
            user = User(
                id="f2b021a4-8026-4c4d-bc23-0cf4f6cd389b",
                email="xxxxxx@test.coco.com",
                name="admin",
                nick_name="admin",
                password=bcrypt.hashpw(
                    "password".encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8"),
            )
            session.add(user)
        else:
            print("Already user seeded.")

        create_roles = [
            Role(id="9cef0e5d-acbe-45f3-b92d-9cac165df3ba", name="owner"),
            Role(id="152eaea0-97f6-4fdc-8bc9-efef073d549b", name="member"),
            Role(id="bc14831b-5dcd-4069-97f0-9f7562272eb4", name="guest"),
        ]

        statement = select(Role).where(
            or_(
                Role.id == "9cef0e5d-acbe-45f3-b92d-9cac165df3ba",
                Role.id == "152eaea0-97f6-4fdc-8bc9-efef073d549b",
                Role.id == "bc14831b-5dcd-4069-97f0-9f7562272eb4",
            )
        )
        results = session.exec(statement)
        role_id_to_role = {result.id: result for result in results}
        for role in create_roles:
            if role.id in role_id_to_role:
                print(f"Alredy role role_id: {id}")
            else:
                session.add(role)
        session.commit()
        print("Seed complete.")


if __name__ == "__main__":
    seed()
