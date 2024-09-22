from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum
from core.libs.assertions import FyleError

from .schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump,status_code=200)


@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    
    #validate that content is not true
    if incoming_payload.get('content') is None:
        return APIResponse.respond_with_error('Content cannot be null', 400)

    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    try:
        submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)
        
        assignment = Assignment.get_assignment_by_id(submit_assignment_payload.id)

        if assignment is None:
            return APIResponse.respond_with_error('Assignment not found', 404)

        if assignment.state != AssignmentStateEnum.DRAFT:
            return APIResponse.respond_with_error('only a draft assignment can be submitted', 400)

        submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        auth_principal=p
        )
        db.session.commit()
        submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
        return APIResponse.respond(data=submitted_assignment_dump,status_code=200)
    
    
    except FyleError as fe:
        return APIResponse.respond_with_error(fe.message,fe.status_code)
    except Exception as e:
        return APIResponse.respond_with_error(str(e), 400)