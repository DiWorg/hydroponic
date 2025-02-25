from rest_framework.pagination import PageNumberPagination

"""
Definition of pagination classes for the Hydroponic API.
"""


class AddPageNumberPagination(PageNumberPagination):
    """
    A custom pagination class.

    Attributes:
        page_size: Default number of items per page.
        max_page_size: Maximum allowed page size.
        page_query_param: The query parameter for the page number.
        page_size_query_param: The query parameter for page size.
    """

    page_size = 10
    max_page_size = 100
    page_query_param = "page"
    page_size_query_param = "page_size"
