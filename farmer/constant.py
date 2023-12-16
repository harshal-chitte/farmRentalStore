
from enum import Enum

class FILTER_FIELDS(Enum):
    BRAND = "p_brand__id"
    CATEGORY = "p_category__id"
    PRICE = "p_price"


class UrlConst(Enum):
    API_URL = 'http://127.0.0.1:8000/api'
    
FILTER_LIST = ["brand", "category", "price"]