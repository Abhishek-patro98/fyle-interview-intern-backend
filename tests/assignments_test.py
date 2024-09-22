from core.models.assignments import AssignmentStateEnum,GradeEnum,Assignment
from core.models.principals import Principal

def test_assignment_creation(create_assignment):
    """Test that an assignment is created with the correct attributes."""
    assignment = create_assignment

    assert assignment.id is not None  # Check that the ID was assigned
    assert assignment.student_id == create_assignment.student_id
    assert assignment.teacher_id == create_assignment.teacher_id
    assert assignment.content == "Sample assignment content"
    assert assignment.grade is None  # Assuming no grade assigned initially
    assert assignment.state == AssignmentStateEnum.DRAFT

def test_assignment_repr(create_assignment):
    """Test the __repr__ method of the Assignment model."""
    assignment = create_assignment
    expected_repr = f'<Assignment {assignment.id!r}>'
    assert repr(assignment) == expected_repr


def test_assignment_state_enum():
    """Test the values of AssignmentStateEnum."""
    assert AssignmentStateEnum.DRAFT == 'DRAFT'
    assert AssignmentStateEnum.SUBMITTED == 'SUBMITTED'
    assert AssignmentStateEnum.GRADED == 'GRADED'

    # Check that the enum contains the expected states
    assert AssignmentStateEnum.DRAFT in AssignmentStateEnum.__members__.values()
    assert AssignmentStateEnum.SUBMITTED in AssignmentStateEnum.__members__.values()
    assert AssignmentStateEnum.GRADED in AssignmentStateEnum.__members__.values()

    # Ensure the enum can be accessed as a list
    expected_states = ['DRAFT', 'SUBMITTED', 'GRADED']
    assert [state.value for state in AssignmentStateEnum] == expected_states

def test_grade_enum():
    """Test the GradeEnum class."""
    assert GradeEnum.A == 'A'
    assert GradeEnum.B == 'B'
    assert GradeEnum.C == 'C'
    assert GradeEnum.D == 'D'

    # Check that the enum members are unique
    assert len(set(GradeEnum)) == len(GradeEnum.__members__)


def test_assignment_get_by_id(create_assignments):
    """Test the get_by_id method to retrieve an assignment by ID."""
    first_assignment = create_assignments[0]

    # Test retrieving the first assignment by ID
    found_assignment = Assignment.get_by_id(first_assignment.id)

    assert found_assignment is not None
    assert found_assignment.id == first_assignment.id
    assert found_assignment.content == first_assignment.content

def test_upsert_update(create_assignment):
    """Test the upsert method for updating an existing assignment."""
    updated_assignment = Assignment(id=create_assignment.id, content="Updated Content", state=AssignmentStateEnum.DRAFT)
    
    result = Assignment.upsert(updated_assignment)
    
    assert result.id == create_assignment.id
    assert result.content == "Updated Content"
