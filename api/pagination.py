from rest_framework.pagination import PageNumberPagination


class CatalogPagination(PageNumberPagination):
    page_size = 20  # Количество элементов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100