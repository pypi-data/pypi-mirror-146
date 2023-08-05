from dataclasses import dataclass, InitVar
from datetime import datetime
from typing import Optional

from vectice.models import JobRun
from .job_output import JobOutput


@dataclass
class __Output:
    createdDate: datetime
    updatedDate: datetime
    version: int
    id: int
    jobId: int
    job: InitVar[dict]
    authorId: int
    duration: int
    metadataSource: str
    deletedDate: Optional[datetime]
    description: Optional[str]
    name: Optional[str]
    systemName: Optional[str]

    def __post_init__(self, job: dict):
        self.job = JobOutput(**job)


@dataclass
class JobRunOutput(JobRun, __Output):
    pass
