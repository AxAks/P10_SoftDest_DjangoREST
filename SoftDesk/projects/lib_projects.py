"""
Functions lib for the projects app
"""
from typing import Any

from rest_framework.generics import get_object_or_404


def find_obj_by_id(_obj, obj_id) -> Any:
    obj = get_object_or_404(_obj.objects.filter(pk=obj_id))
    return obj
