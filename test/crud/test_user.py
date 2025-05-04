from pytest import Session
import pytest
from app.crud.user import update_user
from app.models.user import User
from app.schemas.user import UserUpdate


def test_update_user_status_change(db: Session, test_user: User):
    """Test updating a user's status."""
    user_update_data = UserUpdate(
        status="inactive"
    )
    updated_user = update_user(db, test_user.id, user_update_data)

    assert updated_user is not None
    assert updated_user.status == "inactive"

def test_update_user_email_change(db: Session, test_user: User):
    """Test updating a user's email."""
    user_update_data = UserUpdate(
        email="updatedemail@example.com"
    )
    updated_user = update_user(db, test_user.id, user_update_data)

    assert updated_user is not None
    assert updated_user.email == "updatedemail@example.com"

def test_update_user_invalid_id(db: Session):
    """Test updating a user with an invalid ID."""
    user_update_data = UserUpdate(
        firstname="InvalidID"
    )
    updated_user = update_user(db, user_id=-1, user_data=user_update_data)

    assert updated_user is None

def test_update_user_empty_update(db: Session, test_user: User):
    """Test updating a user with an empty update object."""
    user_update_data = UserUpdate()  # No fields provided
    updated_user = update_user(db, test_user.id, user_update_data)

    assert updated_user is not None
    assert updated_user.firstname == test_user.firstname
    assert updated_user.lastname == test_user.lastname
    assert updated_user.phone_number == test_user.phone_number

def test_update_user_multiple_fields(db: Session, test_user: User):
    """Test updating multiple fields of a user."""
    user_update_data = UserUpdate(
        firstname="Multi",
        lastname="Field",
        phone_number="1112223333",
        address="456 Updated Street"
    )
    updated_user = update_user(db, test_user.id, user_update_data)

    assert updated_user is not None
    assert updated_user.firstname == "Multi"
    assert updated_user.lastname == "Field"
    assert updated_user.phone_number == "1112223333"
    assert updated_user.address == "456 Updated Street"

def test_update_user_invalid_email_format(db: Session, test_user: User):
    """Test updating a user with an invalid email format."""
    user_update_data = UserUpdate(
        email="invalid-email-format"
    )
    with pytest.raises(ValueError):
        update_user(db, test_user.id, user_update_data)

def test_update_user_role_change(db: Session, test_user: User):
    """Test updating a user's role."""
    user_update_data = UserUpdate(
        role="teacher"
    )
    updated_user = update_user(db, test_user.id, user_update_data)

    assert updated_user is not None
    assert updated_user.role == "teacher"
