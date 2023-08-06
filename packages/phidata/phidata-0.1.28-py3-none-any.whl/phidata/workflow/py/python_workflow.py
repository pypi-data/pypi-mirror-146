from typing import Optional, Callable, List, Any, Dict

from phidata.utils.cli_console import print_error
from phidata.workflow.py.python_workflow_base import (
    PythonWorkflowBase,
    PythonWorkflowBaseArgs,
    EngineType,
)


class PythonWorkflowArgs(PythonWorkflowBaseArgs):
    pass


class PythonWorkflow(PythonWorkflowBase):
    def __init__(
        self,
        name: str,
        entrypoint: Callable[..., bool],
        entrypoint_args: Optional[List] = None,
        entrypoint_kwargs: Optional[Dict] = None,
        task_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
        engine: EngineType = EngineType.DEFAULT,
        # If True, scans the args for SqlTable objects and populates the
        # SqlTable.db_engine value using the SqlTable.db_conn_id
        create_db_engine_from_conn_id: bool = False,
    ) -> None:
        super().__init__()
        try:
            self.args = PythonWorkflowArgs(
                name=name,
                entrypoint=entrypoint,
                entrypoint_args=entrypoint_args,
                entrypoint_kwargs=entrypoint_kwargs,
                task_id=task_id,
                dag_id=dag_id,
                version=version,
                enabled=enabled,
                engine=engine,
                create_db_engine_from_conn_id=create_db_engine_from_conn_id,
            )
        except Exception as e:
            print_error(f"Args for {self.__class__.__name__} are not valid")
            raise
