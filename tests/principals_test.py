from core.models.assignments import AssignmentStateEnum,GradeEnum

def test_principal_repr(create_principal):
    """Test the __repr__ method of the Principal model."""
    principal = create_principal  # Assuming create_principal fixture creates a Principal instance

    # Expected output
    expected_repr = f'<Principal {principal.id}>'
    
    # Assert that the __repr__ method returns the expected output
    assert repr(principal) == expected_repr




def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment(client, h_principal, setup_draft_assignment2):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': setup_draft_assignment2.id,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )
    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal,test_regrade_principal_assignment_setup):
    assignment = test_regrade_principal_assignment_setup
    assert assignment is not None
    assert assignment.state != AssignmentStateEnum.DRAFT

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment.id,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

def test_grade_non_existent_assignment(client, h_principal):
    """Failure case: Grading a non-existent assignment should return an error."""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 999,  # Assuming this ID does not exist
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert 'Assignment not found' in response.json['error']

def test_grade_with_missing_parameters(client, h_principal):
    """Failure case: Missing parameters should return an error."""
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 4},  # Missing 'grade'
        headers=h_principal
    )

    assert response.status_code == 400
    assert 'Assignment ID and grade are required' in response.json['error']

    response = client.post(
        '/principal/assignments/grade',
        json={'grade': GradeEnum.A.value},  # Missing 'id'
        headers=h_principal
    )

    assert response.status_code == 400
    assert 'Assignment ID and grade are required' in response.json['error']

def test_grade_with_invalid_grade(client, h_principal,principal_invalid_grade_assignment):
    """Failure case: Grading with an invalid grade should return an error."""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': principal_invalid_grade_assignment.id,
            'grade': 'Z'  # Invalid grade
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert 'Invalid grade' in response.json['error']  

    
def test_get_all_teachers(client, h_principal):
    """Test to ensure that the principal can view all teachers."""
    response = client.get(
        '/principal/teachers',  # Assuming this is the endpoint for fetching teachers
        headers=h_principal
    )

    assert response.status_code == 200
    data = response.json['data']
    assert isinstance(data, list)  # Ensure that a list is returned
    assert len(data) > 0  # Ensure that teachers exist
    for teacher in data:
        assert 'id' in teacher
        assert 'user_id' in teacher

