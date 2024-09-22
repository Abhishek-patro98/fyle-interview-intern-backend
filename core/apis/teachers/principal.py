from flask import Blueprint,Request
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core import db

from .schema import TeacherSchema
principal_assignments_resources = Blueprint('prinicpal_assignments_resources', __name__)

@principal_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_principal_teachers(p):
    """Returns list of all teachers for the principal."""

    #fetch all teachers
    all_teachers = Teacher.get_all_teachers()

    #Serialize the teachers
    teachers_dump = TeacherSchema().dump(all_teachers,many=True)
    
    #Return the assignments
    return APIResponse.respond(data=teachers_dump,status_code=200)