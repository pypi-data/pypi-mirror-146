from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from .job_run_status import JobRunStatus
from .with_properties import WithProperties
from .with_tags import WithTags


@dataclass
class JobRun(WithTags, WithProperties):

    startDate: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    """"""
    status: str = JobRunStatus.STARTED
    """"""
    endDate: Optional[datetime] = None
    """"""
    name: Optional[str] = None
    """"""
    systemName: Optional[str] = None
    """"""

    def __post_init__(self, *args, **kwargs):
        if self.name is None:
            pass
        elif self.name and len(self.name.strip()) > 0:
            pass
        else:
            raise ValueError(f"The name '{self.name}' passed should not be white spaces or an empty string.")
