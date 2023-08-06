from . import queries
from . import templates
from . import utils
from . import outputs

from ._dtos import ModelExecutionDTO

from typing import Optional

CURRENT_EVENT: Optional[ModelExecutionDTO] = None


def set_current_event(event: ModelExecutionDTO):
    """
    Put an execution event into a global variable, for external use

    Parameters
    ----------
    event: ModelExecutionDTO
    """

    global CURRENT_EVENT
    CURRENT_EVENT = event


def get_current_event():
    global CURRENT_EVENT
    return CURRENT_EVENT
