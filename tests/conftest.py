import pytest
import json
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum,GradeEnum
from sqlalchemy.exc import IntegrityError
from core.models.principals import Principal
from core.models.users import User
from core.models.students import Student
from core.models.teachers import Teacher
from core.libs import helpers
from tests import app  
from flask import Flask


@pytest.fixture
def client():
    return app.test_client()



@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers


@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers

@pytest.fixture
def create_user():
    """Fixture to create a user in the database."""
    user = User(username='Abhi_patro',
    email='abhipatro@gmail.com',
    created_at=helpers.get_utc_now(),
    updated_at=helpers.get_utc_now())
    db.session.add(user)
    db.session.commit()
    
    yield user

    # Teardown (remove user after test)
    db.session.delete(user)
    db.session.commit()

@pytest.fixture
def create_student(create_user):
    """Fixture to create a student linked to a user."""
    student = Student(user_id=create_user.id)
    db.session.add(student)
    db.session.commit()
    
    yield student 

    db.session.delete(student)
    db.session.commit()

@pytest.fixture
def create_teacher(create_user):
    """Fixture to create a teacher linked to a user."""
    teacher = Teacher(user_id=create_user.id)
    db.session.add(teacher)
    db.session.commit()

    yield teacher  # Provide the created teacher to the test

    db.session.delete(teacher)  # Clean up after the test
    db.session.commit()

@pytest.fixture
def create_assignment(create_student, create_teacher):
    """Fixture to create an assignment linked to a student and a teacher."""
    assignment = Assignment(
        student_id=create_student.id,
        teacher_id=create_teacher.id,
        content="Sample assignment content",
        grade=None,  # Assuming the assignment is created without a grade
        state=AssignmentStateEnum.DRAFT
    )
    db.session.add(assignment)
    db.session.commit()
    yield assignment

    # Cleanup after the test
    db.session.delete(assignment)
    db.session.commit()

@pytest.fixture
def create_principal(create_user):
    """Fixture to create a principal linked to a user."""
    principal = Principal(user_id=create_user.id)
    db.session.add(principal)
    db.session.commit()
    
    yield principal

    # Cleanup
    db.session.delete(principal)
    db.session.commit()


def test_create_user(client):
    """Test creating a new user."""
    new_user = User(username='Abhi_patro', email='abhipatro@gmail.com',
    created_at=helpers.get_utc_now(),
    updated_at=helpers.get_utc_now())
    db.session.add(new_user)
    db.session.commit()

    assert new_user.id is not None  # Ensure user has an ID
    assert new_user.username == 'Abhi_patro'
    assert new_user.email == 'abhipatro@gmail.com'

@pytest.fixture
def setup_draft_assignment(client, h_principal):
    draft_assignment = Assignment(
        student_id=1,
        teacher_id=None,
        content="Draft assignment content",
        state=AssignmentStateEnum.DRAFT  
    )
    try:
        db.session.add(draft_assignment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
    return draft_assignment

@pytest.fixture
def setup_draft_assignment2(client, h_principal):
    draft_assignment = Assignment(
        student_id=1,
        teacher_id=None,
        content="Draft assignment content",
        state=AssignmentStateEnum.GRADED  
    )
    try:
        db.session.add(draft_assignment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
    return draft_assignment


@pytest.fixture
def setup_assignment(client):
    # Create an assignment with ID 4 that is not in DRAFT state
    assignment = Assignment(
        student_id=1,
        teacher_id=None,
        content="Existing assignment content",
        state=AssignmentStateEnum.SUBMITTED  # Ensure it's in a valid state for grading
    )
    db.session.add(assignment)
    db.session.commit()

@pytest.fixture
def setup_assignment_for_submission(client):
    # Create an assignment with ID 2 in the DRAFT state
    try:
        assignment = Assignment(
            student_id=1,
            teacher_id=2,
            content="Some assignment content",
            state=AssignmentStateEnum.DRAFT  # Ensure it's in DRAFT state
        )
        db.session.add(assignment)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

@pytest.fixture
def setup_assignments_for_student_1(client):

    assignment = Assignment(
    student_id=1,
    teacher_id=2,
    content="Test assignment content",
    state=AssignmentStateEnum.DRAFT
    )
    db.session.add(assignment)
    db.session.commit()

@pytest.fixture
def setup_assignments_for_student_2(client):
    assignment = Assignment(
        student_id=2,
        teacher_id=2,
        content="Test assignment content",
        state=AssignmentStateEnum.DRAFT
    )
    db.session.add(assignment)
    db.session.commit()

@pytest.fixture
def setup_assignment_for_submission():
    # Create a draft assignment with teacher_id=2 and student_id=1
    assignment = Assignment(
        student_id=1,  # Assuming student_id 1 is the one submitting the assignment
        teacher_id=2,
        content="This is a test assignment.",
        state=AssignmentStateEnum.DRAFT,  # Make sure the assignment is in the DRAFT state
    )
    
    # Add the assignment to the session and commit
    db.session.add(assignment)
    db.session.commit()
    
    yield assignment

    # Teardown: Clean up by removing the assignment after the test
    db.session.delete(assignment)
    db.session.commit()

@pytest.fixture
def setup_assignment_for_grading(client):
    # Create an assignment submitted to teacher 1 and not teacher 2
    assignment = Assignment(
        student_id=1,  # Assuming this student exists
        teacher_id=1,  # Assign to teacher 1
        content="Assignment content.",
        state=AssignmentStateEnum.SUBMITTED,
        
    )
    
    # Add the assignment to the session and commit
    db.session.add(assignment)
    db.session.commit()
    
    yield assignment  # This allows the test to access the created assignment

    # Teardown: Clean up by removing the assignment after the test
    db.session.delete(assignment)
    db.session.commit()

@pytest.fixture
def setup_draft_grade_assignment(client):
    """Create a draft assignment for testing grading."""
    assignment = Assignment(
        
        student_id=1,   # Adjust if necessary
        teacher_id=1,  # Adjust if necessary
        content="This assignment is in draft state.",
        state=AssignmentStateEnum.DRAFT,  # Ensure the assignment is in DRAFT state
    )

    # Add the assignment to the session and commit
    db.session.add(assignment)
    db.session.commit()

    yield assignment  # Provide the assignment for use in the test

    # Teardown: Clean up by removing the assignment after the test
    db.session.delete(assignment)
    db.session.commit()


@pytest.fixture
def test_regrade_principal_assignment_setup(client):
    # Create a graded assignment with ID 4
    assignment = Assignment(
        student_id=1,
        teacher_id=1,
        content="This assignment is already graded.",
        grade=GradeEnum.B.value,  # Assuming GradeEnum.B is defined
        state=AssignmentStateEnum.GRADED
    )
    
    # Add the assignment to the session and commit
    db.session.add(assignment)
    db.session.commit()
    
    yield assignment

    # Teardown: Clean up by removing the assignment after the test
    db.session.delete(assignment)
    db.session.commit()

@pytest.fixture
def principal_invalid_grade_assignment(client):
    # Create a valid assignment with ID 4
    assignment = Assignment(
        student_id=1,
        teacher_id=1,
        content="This is a test assignment.",
        grade=GradeEnum.A.value,  # Set to a valid grade initially
        state=AssignmentStateEnum.GRADED  # Set the state to something other than DRAFT
    )

    # Add the assignment to the session and commit
    db.session.add(assignment)
    db.session.commit()

    yield assignment

    # Teardown: Clean up by removing the assignment after the test
    db.session.delete(assignment)
    db.session.commit()

@pytest.fixture
def create_assignments():
    """Fixture to create multiple assignment entries for testing."""
    assignments = [
        Assignment(student_id=1, teacher_id=1, content="Assignment 1", state=AssignmentStateEnum.SUBMITTED),
        Assignment(student_id=1, teacher_id=2, content="Assignment 2", state=AssignmentStateEnum.GRADED),
        Assignment(student_id=2, teacher_id=2, content="Assignment 3", state=AssignmentStateEnum.DRAFT),
    ]
    
    db.session.add_all(assignments)
    db.session.commit()
    
    yield assignments  # Yield assignments for use in tests
    
    # Cleanup code: Delete all assignments after tests
    for assignment in assignments:
        db.session.delete(assignment)
    db.session.commit()


