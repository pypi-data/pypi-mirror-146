import logging
import os
from pathlib import Path
from typing import List, Optional

import isort
from typing_extensions import TypedDict

from lineapy.graph_reader.program_slice import (
    get_program_slice_by_artifact_name,
)
from lineapy.plugins.base import BasePlugin
from lineapy.plugins.task import TaskGraph, TaskGraphEdge
from lineapy.utils.logging_config import configure_logging
from lineapy.utils.utils import prettify

from .utils import load_plugin_template, safe_var_name

logger = logging.getLogger(__name__)
configure_logging()


AirflowDagConfig = TypedDict(
    "AirflowDagConfig",
    {
        "owner": str,
        "retries": int,
        "start_date": str,
        "schedule_interval": str,
        "max_active_runs": int,
        "catchup": str,
    },
    total=False,
)


class AirflowPlugin(BasePlugin):
    def to_airflow(
        self,
        dag_name: str,
        task_names: List[str],
        output_dir_path: Path,
        task_graph: TaskGraph,
        airflow_dag_config: Optional[AirflowDagConfig] = {},
    ) -> None:
        """
        Create an Airflow DAG.

        :param dag_name: Name of the DAG and the python file it is saved in
        :param task_dependencies: Tasks dependencies in graphlib format
            {'B':{'A','C'}}"; this means task A and C are prerequisites for
            task B.
        :param airflow_dag_config: Configs of Airflow DAG model. See
            https://airflow.apache.org/_api/airflow/models/dag/index.html#airflow.models.dag.DAG
            for the full spec.
        """

        AIRFLOW_DAG_TEMPLATE = load_plugin_template("airflow_dag.jinja")
        airflow_dag_config = airflow_dag_config or {}

        full_code = AIRFLOW_DAG_TEMPLATE.render(
            DAG_NAME=dag_name,
            OWNER=airflow_dag_config.get("owner", "airflow"),
            RETRIES=airflow_dag_config.get("retries", 2),
            START_DATE=airflow_dag_config.get("start_date", "days_ago(1)"),
            SCHEDULE_IMTERVAL=airflow_dag_config.get(
                "schedule_interval", "*/15 * * * *"
            ),
            MAX_ACTIVE_RUNS=airflow_dag_config.get("max_active_runs", 1),
            CATCHUP=airflow_dag_config.get("catchup", "False"),
            tasks=task_names,
            task_dependencies=task_graph.get_airflow_dependency(),
        )
        # Sort imports and move them to the top
        full_code = isort.code(full_code, float_to_top=True, profile="black")
        full_code = prettify(full_code)
        (output_dir_path / f"{dag_name}_dag.py").write_text(full_code)
        logger.info(
            f"Added Airflow DAG named {dag_name}_dag. Start a run from the Airflow UI or CLI."
        )

    def sliced_airflow_dag(
        self,
        slice_names: List[str],
        module_name: Optional[str] = None,
        airflow_task_dependencies: TaskGraphEdge = {},
        output_dir: Optional[str] = None,
        airflow_dag_config: Optional[AirflowDagConfig] = {},
    ):
        """
        Creates an Airflow DAG from the sliced code. This includes a python
        file with one function per slice, task dependencies file in Airflow
        format and an example Dockerfile and requirements.txt that can be used
        to run this.

        :param slice_names: list of slice names to be used as tasks.
        :param module_name: name of the Pyhon module the generated code will
            be saved to.
        :param airflow_task_dependencies: tasks dependencies in graphlib format
            {'B':{'A','C'}}"; this means task A and C are prerequisites for
            task B.
        :param output_dir: directory to save the generated code to.
        :param airflow_dag_config: Configs of Airflow DAG model.
        """

        artifacts_code = {}
        task_names = []
        for slice_name in slice_names:
            artifact_var = safe_var_name(slice_name)
            slice_code = get_program_slice_by_artifact_name(
                self.db, slice_name
            )
            artifacts_code[artifact_var] = slice_code
            task_name = f"{artifact_var}"
            task_names.append(task_name)

        task_graph = TaskGraph(
            slice_names,
            {slice: task for slice, task in zip(slice_names, task_names)},
            airflow_task_dependencies,
        )

        module_name = module_name or "_".join(slice_names)
        output_dir_path = Path.cwd()
        if output_dir:
            output_dir_path = Path(os.path.expanduser(output_dir))
            self.prepare_output_dir(
                copy_dst=str(output_dir_path.resolve()),
            )

        logger.info(
            "Pipeline source generated in the directory: %s", output_dir_path
        )
        self.generate_python_module(
            module_name, artifacts_code, output_dir_path
        )
        self.to_airflow(
            module_name,
            task_names,
            output_dir_path,
            task_graph,
            airflow_dag_config,
        )
        self.generate_infra(
            module_name=module_name, output_dir_path=output_dir_path
        )
        return output_dir_path
