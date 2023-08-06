from typing import Optional, Callable, Tuple, Any, Dict
from typing_extensions import Protocol
from functools import wraps, partial

from phidata.workflow.py.python_workflow import PythonWorkflow, EngineType
from phidata.utils.cli_console import print_error
from phidata.utils.log import logger


class WorkflowFunction(Protocol):
    def __call__(self, **kwargs) -> bool:
        ...


def create_workflow(func: WorkflowFunction) -> Callable[..., PythonWorkflow]:
    """Converts a function into a python workflow"""

    wraps(func)

    def wrapper(
        *args,
        name: Optional[str] = None,
        task_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
        engine: EngineType = EngineType.DEFAULT,
        # when True, scans the args/kwargs for SqlTable objects and populates the
        # SqlTable.db_engine value using the SqlTable.db_conn_id
        create_db_engine_from_conn_id: bool = True,
        **kwargs,
    ) -> PythonWorkflow:
        # logger.info(f"args: {args}")
        # logger.info(f"kwargs: {kwargs}")
        try:
            workflow_name = name or func.__class__.__name__
            # create a partial function that can be called by the workflow runner
            entrypoint = partial(func, *args, **kwargs)
            # create a list for args because they're passed as a tuple by default
            entrypoint_args_list = list(args) if args is not None else None
            wf = PythonWorkflow(
                name=workflow_name,
                entrypoint=entrypoint,
                entrypoint_args=entrypoint_args_list,
                entrypoint_kwargs=kwargs,
                task_id=task_id,
                dag_id=dag_id,
                version=version,
                enabled=enabled,
                engine=engine,
                create_db_engine_from_conn_id=create_db_engine_from_conn_id,
            )
            return wf
        except Exception as e:
            print_error("Could not create workflow for: {}".format(func))
            print_error(e)
            raise

    return wrapper


"""
How to use create_workflow:

@create_workflow
def test_wf(param, **kwargs):
    return True

wf = test_wf(param="yum")

dp = DataProduct(name="dp", workflows=[wf])
"""
