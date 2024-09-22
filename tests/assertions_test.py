import pytest
from core.libs.assertions import assert_auth, assert_true, assert_valid, assert_found
from core.libs.exceptions import FyleError

def test_assert_auth_pass():
    """Test that assert_auth does not raise an error for true condition."""
    assert_auth(True)  # Should not raise

def test_assert_auth_fail():
    """Test that assert_auth raises a FyleError for false condition."""
    with pytest.raises(FyleError) as exc_info:
        assert_auth(False)
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == 'UNAUTHORIZED'

def test_assert_true_pass():
    """Test that assert_true does not raise an error for true condition."""
    assert_true(True)  # Should not raise

def test_assert_true_fail():
    """Test that assert_true raises a FyleError for false condition."""
    with pytest.raises(FyleError) as exc_info:
        assert_true(False)
    assert exc_info.value.status_code == 403
    assert exc_info.value.message == 'FORBIDDEN'

def test_assert_valid_pass():
    """Test that assert_valid does not raise an error for true condition."""
    assert_valid(True)  # Should not raise

def test_assert_valid_fail():
    """Test that assert_valid raises a FyleError for false condition."""
    with pytest.raises(FyleError) as exc_info:
        assert_valid(False)
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == 'BAD_REQUEST'

def test_assert_found_pass():
    """Test that assert_found does not raise an error for non-None object."""
    assert_found('object')  # Should not raise

def test_assert_found_fail():
    """Test that assert_found raises a FyleError for None object."""
    with pytest.raises(FyleError) as exc_info:
        assert_found(None)
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == 'NOT_FOUND'
