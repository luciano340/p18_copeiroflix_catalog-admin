import os


class CreateListPagination:
    @staticmethod
    def configure_pagination(mapped_list: list, current_page: int) -> list:
        DEFAULT_PAGE_SIZE = os.environ.get("page_size", 5)
        page_offset = (current_page - 1) * DEFAULT_PAGE_SIZE
        pagination_list = mapped_list[page_offset:page_offset + DEFAULT_PAGE_SIZE]
        return pagination_list