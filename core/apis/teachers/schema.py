from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from core.models.assignments import Teacher
from core import db

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        sqla_session = db.session

    id = fields.Int()
    user_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def initiate_class(self, data, **kwargs):
        """Convert the deserialized data into a Teacher instance."""
        return Teacher(**data)