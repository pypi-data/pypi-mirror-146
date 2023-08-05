from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TypeVar

from .job_type import JobType

JobAndChildTypes = TypeVar("JobAndChildTypes", bound="Job")


@dataclass
class Job:
    name: str
    """"""
    type: Optional[str] = JobType.OTHER
    """
    see possible values in py:class:: JobType
    """
    description: Optional[str] = None
    """"""
    project: Optional[str] = None
    """"""

    def __post_init__(self, *args, **kwargs):
        if self.name is None:
            raise ValueError(f"The name: '{self.name}' passed can not be None.")
        elif self.name and len(self.name.strip()) > 0:
            pass
        else:
            raise ValueError(f"The name '{self.name}' passed should not be white spaces or an empty string.")

    def with_description(self: JobAndChildTypes, description: str) -> JobAndChildTypes:
        """ """
        self.description = description
        return self

    def with_type(self: JobAndChildTypes, job_type: str) -> JobAndChildTypes:
        """ """
        self.type = job_type
        return self
