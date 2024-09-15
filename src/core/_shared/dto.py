
from dataclasses import dataclass


@dataclass
class ListOuputMeta:
    current_page: int
    page_size: int
    total: int