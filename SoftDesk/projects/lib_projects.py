"""
Functions lib for the projects app
"""
from typing import Any


def find_obj(_obj, obj_id) -> Any:
    obj = _obj.objects.filter(pk=obj_id)
    return obj