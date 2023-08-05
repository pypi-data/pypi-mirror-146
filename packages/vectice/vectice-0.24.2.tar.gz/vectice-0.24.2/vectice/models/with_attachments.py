from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Tuple, List, Any, BinaryIO, TypeVar
from abc import ABC, abstractmethod


class WithAttachmentsTrait(ABC):
    T = TypeVar("T", bound="WithAttachmentsTrait")

    @abstractmethod
    def with_attachments(self, files: List[str]):
        """Accepts a list of file paths and then attaches the files to the modelversion that is created.
        e.g ["filepath/image.png", r"User/path/metrics.json"]

        :param files: The list of files
        :return: ModelVersionArtifact
        """
        pass


@dataclass
class WithAttachments(WithAttachmentsTrait):
    artifact_type: Optional[str] = None
    """"""
    files: Optional[List[Tuple[str, Tuple[Any, BinaryIO]]]] = None
    """"""

    def with_attachments(self, files: List[str]):
        self.files = []
        logging.info(f"{self.__class__.__name__} Attaching files...")
        for file in files:
            curr_file = None
            try:
                curr_file = ("file", (file, open(file, "rb")))
            except Exception:
                logging.warning(f"{self.__class__.__name__}: did not read {file}.")
                pass
            if curr_file:
                self.files += [curr_file]
        return self


class WithDelegatedAttachments(WithAttachmentsTrait, ABC):
    T = TypeVar("T", bound="WithDelegatedAttachments")

    @abstractmethod
    def _get_attachment(self) -> WithAttachmentsTrait:
        pass

    def with_attachments(self: T, files: List[str]) -> T:
        self._get_attachment().with_attachments(files)
        return self
