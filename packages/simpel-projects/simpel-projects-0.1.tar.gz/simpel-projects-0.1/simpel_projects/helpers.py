from django.core.exceptions import ImproperlyConfigured
from simpel_hookup import core as hook

from .models import Deliverable, Task, WorkOrder


def get_task_childs_models():
    child_models = []
    funcs = hook.get_hooks("REGISTER_TASK_CHILD_MODELS")
    child_classes = [func() for func in funcs]
    for klass in child_classes:
        if issubclass(klass, Task):
            child_models.append(klass)
        else:
            raise ImproperlyConfigured("Hook REGISTER_TASK_CHILD_MODELS should return Deliverable subclass")
    return child_models


def get_deliverable_childs_models():
    child_models = []
    funcs = hook.get_hooks("REGISTER_DELIVERABLE_CHILD_MODELS")
    deliverable_classes = [func() for func in funcs]
    for klass in deliverable_classes:
        if issubclass(klass, Deliverable):
            child_models.append(klass)
        else:
            raise ImproperlyConfigured("Hook REGISTER_DELIVERABLE_CHILD_MODELS should return Deliverable subclass")
    return child_models


def get_workorder_childs_models():
    child_models = []
    funcs = hook.get_hooks("REGISTER_WORKORDER_CHILD_MODELS")
    klasses = [func() for func in funcs]
    for klass in klasses:
        if issubclass(klass, WorkOrder):
            child_models.append(klass)
        else:
            raise ImproperlyConfigured("Hook REGISTER_WORKORDER_CHILD_MODELS should return WorkOrder subclass")
    return child_models
