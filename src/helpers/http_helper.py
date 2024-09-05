from flask import jsonify
from datetime import datetime


class HttpHelper:
    # Define different response types as constants
    retOK = "OK"
    retError = "ERROR"
    retCreated = "CREATED"
    retNotFound = "NOTFOUND"
    retForbidden = "FORBIDDEN"
    retConflict = "CONFLICT"
    retErrorServer = "ERRORSERVER"
    retUnauthorized = "UNAUTHORIZED"
    retUnprocessableContent = "UNPROCESSABLECONTENT"

    @staticmethod
    def response(result, data=None, cache=False):
        """
        Format the HTTP response based on the result status and return a JSON response.

        Args:
            result (str): The result type (e.g., OK, ERROR).
            data (dict): The data to be included in the response.
            cache (bool): Whether the response should be cached or not.

        Returns:
            Response: A formatted Flask JSON response with status code.
        """
        # Map result constants to HTTP status codes
        result_to_code = {
            HttpHelper.retOK: 200,
            HttpHelper.retError: 400,
            HttpHelper.retCreated: 201,
            HttpHelper.retNotFound: 404,
            HttpHelper.retForbidden: 403,
            HttpHelper.retConflict: 409,
            HttpHelper.retErrorServer: 500,
            HttpHelper.retUnprocessableContent: 422,
            HttpHelper.retUnauthorized: 401,
        }

        # Get the corresponding status code or default to 500 (server error)
        code = result_to_code.get(result, 500)

        # Format the JSON response
        response = {
            "result": result,
            "data": data if data is not None else {},
            "dedicated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        }

        # Add a field for processing time if available
        if hasattr(HttpHelper, "start_time"):
            response["consumption"] = round(
                datetime.utcnow().timestamp() - HttpHelper.start_time, 2
            )

        # Create the response with the appropriate status code
        resp = jsonify(response), code

        # Add cache control headers if necessary
        if cache:
            resp[0].headers["Cache-Control"] = "max-age=600, public"
        else:
            resp[0].headers["Cache-Control"] = "no-store"

        return resp

    @staticmethod
    def set_start_time(start_time):
        """
        Set the start time for calculating response consumption time.

        Args:
            start_time (float): The start time (as a timestamp).
        """
        HttpHelper.start_time = start_time
