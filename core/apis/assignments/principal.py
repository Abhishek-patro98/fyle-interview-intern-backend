from flask import Blueprint, request
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum,GradeEnum
from .schema import AssignmentGradeSchema,AssignmentSchema

principal_assignments_resources = Blueprint('prinicpal_assignments_resources', __name__)

@principal_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_principal_assignments(p):
    """Returns list of all submitted and graded for the principal."""

    #Fetch all assignments in the "SUBMITTED" or "GRADED" STATE
    submitted_and_graded_assignments = Assignment.get_assignments_by_state(['SUBMITTED','GRADED'])

    #Serialize the assignments
    assignment_dump = AssignmentSchema().dump(submitted_and_graded_assignments, many=True)

    #Return the assignments
    return APIResponse.respond(data=assignment_dump)



@principal_assignments_resources.route('/grade', methods=['POST'], strict_slashes=False)
@decorators.authenticate_principal
def grade_assignments(p):
    """Grade or re-grade an assignment"""
    data = request.json
    assignment_id = data.get('id')
    grade = data.get('grade')

    # Check for missing parameters
    if assignment_id is None or grade is None:
        return APIResponse.respond_with_error('Assignment ID and grade are required', 400)

      # Fetch the assignment by ID
    assignment = Assignment.get_assignment_by_id(assignment_id)  
    # Replace with your logic to fetch assignment
    if assignment is None:
        return APIResponse.respond_with_error('Assignment not found', 400)
    
    
      # Check if assignment state is 'DRAFT'
    if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.respond_with_error('Assignment in draft state cannot be graded', 400)
    
    if grade not in [g.value for g in GradeEnum]:  # Assuming GradeEnum has a value attribute
        return APIResponse.respond_with_error('Invalid grade', 400)

    # Validate input using schema
    validated_data = AssignmentGradeSchema().load(data)

    assignment_id = validated_data['id']
    grade = validated_data['grade']

    # Grade the assignment
    try:
        assignment = Assignment.mark_grade(assignment_id, grade, p)
    except AssertionError as e:
        return APIResponse.respond_with_error(str(e), 400)  # Handle specific validation errors
    except Exception as e:
        return APIResponse.respond_with_error('An unexpected error occurred: ' + str(e), 500)

    # Serialize the updated assignment
    assignment_schema = AssignmentSchema()
    result = assignment_schema.dump(assignment)

    # Return the updated assignment
    return APIResponse.respond(data=result)


