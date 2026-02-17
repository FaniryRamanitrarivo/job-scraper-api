from pydantic import BaseModel, Field
from typing import List, Optional


class ExtractConfig(BaseModel):
    selector: str
    attribute: Optional[str] = "href"
    regex: Optional[str] = None
    wait_for_load: bool = False


class NavigationStep(BaseModel):
    name: str
    extract: ExtractConfig


class PaginationConfig(BaseModel):
    type: Optional[str] = "parameter_increment"
    parameter: Optional[str] = "?page=<PNum>"
    selector: Optional[str] = None
    max_pages: Optional[int] = 50
    wait_for_load: bool = False


class ScrapingPayload(BaseModel):
    entry_points: List[str] = Field(default_factory=list)
    navigation: Optional[List[NavigationStep]] = None
    product_links: ExtractConfig
    pagination: Optional[PaginationConfig] = None
