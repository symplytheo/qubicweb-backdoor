from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomJSONRenderer(JSONRenderer):
    """
    Custom JSON Renderer to enforce consistent response shape.

    Format:
    {
        "success": bool,
        "message": str,
        "data": dict | list | None,
        "errors": dict | list | None
    }
    """

    status_code_messages = {
        status.HTTP_200_OK: "Request completed successfully.",
        status.HTTP_201_CREATED: "Resource created successfully.",
        status.HTTP_202_ACCEPTED: "Request accepted for processing.",
        status.HTTP_204_NO_CONTENT: "Request completed successfully.",
        status.HTTP_400_BAD_REQUEST: "Bad request. Please check your payload.",
        status.HTTP_401_UNAUTHORIZED: "Valid authentication required.",
        status.HTTP_403_FORBIDDEN: "Permission denied.",
        status.HTTP_404_NOT_FOUND: "Resource not found.",
        status.HTTP_405_METHOD_NOT_ALLOWED: "Method not allowed.",
        status.HTTP_409_CONFLICT: "Conflict occurred.",
        status.HTTP_422_UNPROCESSABLE_ENTITY: "Validation failed.",
        status.HTTP_429_TOO_MANY_REQUESTS: "Too many requests.",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error.",
    }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None

        # Default structure
        response_data = {
            "success": False,
            "message": None,
            # "data": None,
            # "errors": None,
        }

        # Skip wrapping for non-JSON (e.g., Browsable API, file downloads)
        # if response and response.accepted_media_type != "application/json":
        #     return super().render(data, accepted_media_type, renderer_context)

        status_code = getattr(response, "status_code", 500)

        if response and response.exception:
            # Error response
            response_data["errors"] = data
            # prefer error message from details if available
            if isinstance(data, dict) and "detail" in data:
                response_data["message"] = data["detail"]
            else:
                response_data["message"] = self.status_code_messages.get(status_code, "An error occurred.")
        else:
            # Success response
            response_data["success"] = True
            response_data["data"] = data
            # if a custom message is provided in the data, use it
            if isinstance(data, dict) and "message" in data:
                response_data["message"] = data.pop("message")
            else:
                response_data["message"] = self.status_code_messages.get(status_code, "Operation was successful.")

        return super().render(response_data, accepted_media_type, renderer_context)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = 10  # default
    max_page_size = 100  # prevent abuse

    def get_paginated_response(self, data):
        return Response(
            {
                "items": data,
                "meta": {
                    "page": self.page.number,
                    "limit": self.get_page_size(self.request),
                    "total_pages": self.page.paginator.num_pages,
                    "total_items": self.page.paginator.count,
                },
            }
        )
