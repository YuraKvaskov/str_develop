from drf_spectacular.utils import OpenApiExample
from rest_framework import status

repair_kit_search_example = OpenApiExample(
    'Search Repair Kits by Article',
    value={'search': 'K740-RK-01'},
    request_only=True,
    response_only=False,
    status_codes=[status.HTTP_200_OK],
)

repair_kit_filter_example = OpenApiExample(
    'Filter Repair Kits by Group and is_hit',
    value={'groups__name': 'Прокладки', 'is_hit': 'false'},
    request_only=True,
    response_only=False,
    status_codes=[status.HTTP_200_OK],
)


spare_part_search_example = OpenApiExample(
    'Search Spare Parts by Name',
    value={'search': 'фильтр'},
    request_only=True,
    response_only=False,
    status_codes=[status.HTTP_200_OK],
)

spare_part_filter_example = OpenApiExample(
    'Filter Spare Parts by EngineCat and is_hit',
    value={'engine_cat': 1, 'is_hit': 'true'},
    request_only=True,
    response_only=False,
    status_codes=[status.HTTP_200_OK],
)