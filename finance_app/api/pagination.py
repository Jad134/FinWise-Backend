from rest_framework.pagination import PageNumberPagination


class ExpensePagination(PageNumberPagination):
    page_size = 5  # Standardwert pro Seite
    page_size_query_param = 'page_size'  # Ermöglicht `?page_size=20`
    max_page_size = 100  # Begrenzung, damit API nicht überlastet wird
