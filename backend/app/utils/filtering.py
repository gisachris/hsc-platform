from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FilterParam(BaseModel):
    field: str = Field(..., description="Target field to filter on")
    operator: str = Field(
        "eq", description="Comparison operator: eq, ne, gt, gte, lt, lte, lk (like), in"
    )
    value: Any = Field(..., description="Filter comparison value")


class QueryFilters(BaseModel):
    filters: List[FilterParam] = Field(
        default_factory=list, description="List of individual field filters"
    )

    @classmethod
    def parse_query_params(cls, query_params: Dict[str, str]) -> "QueryFilters":
        """
        Parses filter parameters from flat query dictionaries.
        E.g. filter__name__lk=google -> field='name', operator='lk', value='google'
        """
        parsed_filters = []
        for key, val in query_params.items():
            if key.startswith("filter__"):
                parts = key.split("__")
                if len(parts) == 3:
                    _, field, operator = parts
                    parsed_filters.append(
                        FilterParam(field=field, operator=operator, value=val)
                    )
                elif len(parts) == 2:
                    _, field = parts
                    parsed_filters.append(
                        FilterParam(field=field, operator="eq", value=val)
                    )
        return cls(filters=parsed_filters)
