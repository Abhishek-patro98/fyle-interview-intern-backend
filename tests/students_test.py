from core.models.students import Student

def test_get_assignments_student_1(client, h_student_1,setup_assignments_for_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2,setup_assignments_for_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400
    assert 'Content cannot be null' in response.json['error']

def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1,setup_assignment_for_submission):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': setup_assignment_for_submission.id, 
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == 'only a draft assignment can be submitted'

def test_student_creation(create_student):
    """Test creating and retrieving a student."""
    student = create_student
    assert student.id is not None  # Ensure student has an ID
    assert student.user_id == create_student.user_id  # Ensure the user ID is correctly linked

    # Retrieve the student by ID
    retrieved_student = Student.query.get(student.id)
    assert retrieved_student is not None
    assert retrieved_student.id == student.id
    assert retrieved_student.user_id == student.user_id

def test_student_repr(create_student):
    """Test the __repr__ method of the Student class."""
    student = create_student  # Use the fixture to create a student instance
    
    # Expected string representation
    expected_repr = f'<Student {student.id!r}>'
    
    # Assert that the repr method returns the expected string
    assert repr(student) == expected_repr

