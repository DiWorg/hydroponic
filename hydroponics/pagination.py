from rest_framework.pagination import PageNumberPagination


class AddPageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_query_param = "page"
    page_size_query_param = "page_size"
