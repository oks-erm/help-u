from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """
    A pagination class for the Message viewset.

    This class allows for pagination of the Message queryset with a page size
    of 50, and a maximum page size of 100. The page size can be customized
    through the page_size_query_param query parameter in the request.
    """
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100
