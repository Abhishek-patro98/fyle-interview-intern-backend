from core.models.users import User

def test_get_by_id(create_user):
    """Test retrieving a user by ID."""
    user = User.get_by_id(create_user.id)
    assert user is not None
    assert user.id == create_user.id
    assert user.username == 'Abhi_patro'
    assert user.email == 'abhipatro@gmail.com'

def test_get_by_email(create_user):
    """Test retrieving a user by email."""
    user = User.get_by_email('abhipatro@gmail.com')
    assert user is not None
    assert user.email == 'abhipatro@gmail.com'
    assert user.username == 'Abhi_patro'

def test_user_repr(create_user):
    """Test the __repr__ method of the User class."""
    user = create_user  # Use the fixture to create a user instance
    
    # Expected string representation
    expected_repr = f'<User {user.username!r}>'
    
    # Assert that the repr method returns the expected string
    assert repr(user) == expected_repr
