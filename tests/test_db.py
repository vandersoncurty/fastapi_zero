from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='testuser', email='test@example.com', password='testpassword'
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'testuser'))

    assert asdict(user) == {
        'id': 1,
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'created_at': time,
        'updated_at': time,
    }
