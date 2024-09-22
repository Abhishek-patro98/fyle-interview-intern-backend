from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data,status_code=200):
        return make_response(jsonify(data=data),status_code)
    
    @classmethod
    def respond_with_error(cls, message, status_code=400):
        """Respond with an error message."""
        return make_response(jsonify({"error": message}), status_code)