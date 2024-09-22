from core.libs.exceptions import FyleError

def test_fyle_error_initialization():
    """Test FyleError initialization."""
    error = FyleError(status_code=400, message="An error occurred.")
    assert error.status_code == 400
    assert error.message == "An error occurred."

def test_fyle_error_to_dict():
    """Test FyleError to_dict method."""
    error = FyleError(status_code=404, message="Not Found")
    assert error.to_dict() == {'message': 'Not Found'}
