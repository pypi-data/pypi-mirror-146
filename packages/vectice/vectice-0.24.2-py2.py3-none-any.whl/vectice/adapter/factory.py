import logging

logger = logging.getLogger(__name__)


class LibraryFactory:
    @staticmethod
    def get_library(
        project_token: str, lib: str, auto_log: bool = False, check_remote_repository: bool = False, *args, **kwargs
    ):
        if str(lib).lower() == "mlflow":
            from .mlflow import MlflowAdapter

            return MlflowAdapter(project_token=project_token, auto_log=auto_log, check_remote_repository=check_remote_repository, *args, **kwargs)  # type: ignore
        else:
            raise ValueError(f"Unsupported library: {lib}")
