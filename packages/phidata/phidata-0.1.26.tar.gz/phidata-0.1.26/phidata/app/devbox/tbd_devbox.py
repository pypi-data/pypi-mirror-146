from collections import OrderedDict
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from typing_extensions import Literal

from pydantic import BaseModel

from phidata.app.db import DbApp
from phidata.app import PhidataApp, PhidataAppArgs
from phidata.infra.docker.resource.network import DockerNetwork
from phidata.infra.docker.resource.container import DockerContainer
from phidata.infra.docker.resource.group import (
    DockerResourceGroup,
    DockerBuildContext,
)
from phidata.infra.k8s.create.apps.v1.deployment import CreateDeployment
from phidata.infra.k8s.create.core.v1.config_map import CreateConfigMap
from phidata.infra.k8s.create.core.v1.container import CreateContainer
from phidata.infra.k8s.create.core.v1.volume import (
    CreateVolume,
    EmptyDirVolumeSource,
    HostPathVolumeSource,
    VolumeType,
)
from phidata.infra.k8s.create.common.port import CreatePort
from phidata.infra.k8s.create.group import CreateK8sResourceGroup
from phidata.infra.k8s.resource.group import (
    K8sResourceGroup,
    K8sBuildContext,
)
from phidata.utils.common import (
    get_image_str,
    get_default_container_name,
    get_default_configmap_name,
    get_default_secret_name,
    get_default_service_name,
    get_default_volume_name,
    get_default_deploy_name,
    get_default_pod_name,
)
from phidata.utils.cli_console import print_error, print_info
from phidata.utils.log import logger

default_devbox_name: str = "devbox"


class DevboxDevModeArgs(BaseModel):
    install_phidata_dev: bool = True
    phidata_volume_name: str = "devbox-phidata-volume"
    phidata_dir_path: Path = Path.home().joinpath("p", "philab", "phidata")
    phidata_dir_container_path: str = "/phidata"


class DevboxArgs(PhidataAppArgs):
    name: str = default_devbox_name
    version: str = "1"
    enabled: bool = True

    # Image args
    image_name: str = "phidata/devbox"
    image_tag: str = "1"
    entrypoint: Optional[Union[str, List]] = None
    command: Optional[Union[str, List]] = None

    # Mount the workspace directory on the container
    mount_workspace: bool = True
    workspace_volume_name: str = "devbox-workspace-volume"
    # Path to mount the workspace volume under
    # This is the parent directory for the workspace on the container
    # i.e. the ws is mounted as a subdir in this dir
    # eg: if ws name is: idata, workspace path would be: /usr/local/devbox/idata
    workspace_parent_container_path: str = "/usr/local/devbox"

    # Install python dependencies using a requirements.txt file
    install_requirements: bool = True
    # Path to the requirements.txt file relative to the workspace root
    requirements_file_path: str = "requirements.txt"

    # Mount aws config on the container
    mount_aws_config: bool = False
    # Aws config dir on the host
    aws_config_path: Path = Path.home().resolve().joinpath(".aws")
    # Aws config dir on the container
    aws_config_container_path: str = "/root/.aws"

    # Configure airflow
    # If init_airflow = True, this devbox initializes airflow
    init_airflow: bool = True
    # If use_products_as_airflow_dags = True
    # set the AIRFLOW__CORE__DAGS_FOLDER to the products_dir
    use_products_as_airflow_dags: bool = True
    # If use_products_as_airflow_dags = False
    # set the AIRFLOW__CORE__DAGS_FOLDER to the airflow_dags_path
    # airflow_dags_path is the directory in the container containing the airflow dags
    airflow_dags_path: Optional[str] = None
    # Creates an airflow user with username: test, pass: test
    create_airflow_test_user: bool = False
    airflow_executor: Literal[
        "DebugExecutor",
        "LocalExecutor",
        "SequentialExecutor",
        "CeleryExecutor",
        "CeleryKubernetesExecutor",
        "DaskExecutor",
        "KubernetesExecutor",
    ] = "SequentialExecutor"

    # Only on docker: mount airflow home from container to host machine
    # Useful when debugging the airflow conf
    mount_airflow_home: bool = False
    # Path to the dir on host machine relative to the workspace root
    airflow_home_dir: str = "airflow"
    # Path to airflow home
    airflow_home_container_path: str = "/usr/local/airflow"

    # Configure airflow db
    # If True, initialize the airflow_db on this devbox
    # If None, value is derived from init_airflow i.e. initialize the airflow_db if init_airflow = True
    #   Locally, airflow_db uses sqllite
    # If using the devbox with an external Airflow db, set init_airflow_db = False
    init_airflow_db: Optional[bool] = None
    wait_for_airflow_db: bool = False
    # Connect to database using DbApp
    airflow_db_app: Optional[DbApp] = None
    # Connect to database manually
    airflow_db_user: Optional[str] = None
    airflow_db_password: Optional[str] = None
    airflow_db_schema: Optional[str] = None
    airflow_db_host: Optional[str] = None
    airflow_db_port: Optional[str] = None
    airflow_db_driver: str = "postgresql+psycopg2"
    # Airflow db connections in the format { conn_id: conn_url }
    # converted to env var: AIRFLOW_CONN__conn_id = conn_url
    db_connections: Optional[Dict] = None

    # Configure airflow scheduler
    # Init Airflow scheduler as a deamon process
    init_airflow_scheduler: bool = False

    # Configure airflow webserver
    # Init Airflow webserver when the container starts
    init_airflow_webserver: bool = False
    # webserver port on the container
    airflow_webserver_container_port: int = 8080
    # webserver port on the host machine
    airflow_webserver_host_port: int = 8080
    # webserver port name on K8sContainer
    airflow_webserver_port_name: str = "http"

    # Configure the container
    container_name: Optional[str] = None
    # Only used by the DockerContainer
    container_detach: bool = True
    container_auto_remove: bool = True
    container_remove: bool = True
    # Add env variables to container env
    env: Optional[Dict[str, str]] = None
    # Read env variables from a file in yaml format
    env_file: Optional[Path] = None
    # Configure the ConfigMap used for env variables that are not Secret
    config_map_name: Optional[str] = None
    # Configure the Secret used for env variables that are Secret
    secret_name: Optional[str] = None
    # Read secrets from a file in yaml format
    secrets_file: Optional[Path] = None

    # Configure the databox deploy
    deploy_name: Optional[str] = None
    pod_name: Optional[str] = None

    # Other args
    load_examples: bool = False
    print_env_on_load: bool = True
    dev_mode: Optional[DevboxDevModeArgs] = None


class Devbox(PhidataApp):
    def __init__(
        self,
        name: str = default_devbox_name,
        version: str = "1",
        enabled: bool = True,
        # Image args,
        image_name: str = "phidata/devbox",
        image_tag: str = "1",
        entrypoint: Optional[Union[str, List]] = None,
        command: Optional[Union[str, List]] = None,
        # Mount the workspace directory on the container,
        mount_workspace: bool = True,
        workspace_volume_name: str = "devbox-workspace-volume",
        # Path to mount the workspace volume under,
        # This is the parent directory for the workspace on the container,
        # i.e. the ws is mounted as a subdir in this dir,
        # eg: if ws name is: idata, workspace path would be: /usr/local/devbox/idata,
        workspace_parent_container_path: str = "/usr/local/devbox",
        # Install python dependencies using a requirements.txt file,
        install_requirements: bool = True,
        # Path to the requirements.txt file relative to the workspace root,
        requirements_file_path: str = "requirements.txt",
        # Mount aws config on the container,
        mount_aws_config: bool = False,
        # Aws config dir on the host,
        aws_config_path: Path = Path.home().resolve().joinpath(".aws"),
        # Aws config dir on the container,
        aws_config_container_path: str = "/root/.aws",
        # Configure airflow,
        # If init_airflow = True, this devbox initializes airflow,
        init_airflow: bool = True,
        # If use_products_as_airflow_dags = True,
        # set the AIRFLOW__CORE__DAGS_FOLDER to the products_dir,
        use_products_as_airflow_dags: bool = True,
        # If use_products_as_airflow_dags = False,
        # set the AIRFLOW__CORE__DAGS_FOLDER to the airflow_dags_path,
        # airflow_dags_path is the directory in the container containing the airflow dags,
        airflow_dags_path: Optional[str] = None,
        # Creates an airflow user with username: test, pass: test,
        create_airflow_test_user: bool = False,
        # Only on docker: mount airflow home from container to host machine,
        # Useful when debugging the airflow conf,
        mount_airflow_home: bool = False,
        airflow_executor: Literal[
            "DebugExecutor",
            "LocalExecutor",
            "SequentialExecutor",
            "CeleryExecutor",
            "CeleryKubernetesExecutor",
            "DaskExecutor",
            "KubernetesExecutor",
        ] = "SequentialExecutor",
        # Path to the dir on host machine relative to the workspace root,
        airflow_home_dir: str = "airflow",
        # Path to airflow home,
        airflow_home_container_path: str = "/usr/local/airflow",
        # Configure airflow db,
        # If True, initialize the airflow_db on this devbox,
        # If None, value is derived from init_airflow i.e. initialize the airflow_db if init_airflow = True,
        #   Locally, airflow_db uses sqllite,
        # If using the devbox with an external Airflow db, set init_airflow_db = False,
        init_airflow_db: Optional[bool] = None,
        wait_for_airflow_db: bool = False,
        # Connect to database using DbApp,
        airflow_db_app: Optional[DbApp] = None,
        # Connect to database manually,
        airflow_db_user: Optional[str] = None,
        airflow_db_password: Optional[str] = None,
        airflow_db_schema: Optional[str] = None,
        airflow_db_host: Optional[str] = None,
        airflow_db_port: Optional[str] = None,
        airflow_db_driver: str = "postgresql+psycopg2",
        # Airflow db connections in the format { conn_id: conn_url },
        # converted to env var: AIRFLOW_CONN__conn_id = conn_url,
        db_connections: Optional[Dict] = None,
        # Configure airflow scheduler,
        # Init Airflow scheduler as a deamon process,
        init_airflow_scheduler: bool = False,
        # Configure airflow webserver,
        # Init Airflow webserver when the container starts,
        init_airflow_webserver: bool = False,
        # webserver port on the container,
        airflow_webserver_container_port: int = 8080,
        # webserver port on the host machine,
        airflow_webserver_host_port: int = 8080,
        # webserver port name on K8sContainer,
        airflow_webserver_port_name: str = "http",
        # Configure the container,
        container_name: Optional[str] = None,
        # Only used by the DockerContainer,
        container_detach: bool = True,
        container_auto_remove: bool = True,
        container_remove: bool = True,
        # Add env variables to container env,
        env: Optional[Dict[str, str]] = None,
        # Read env variables from a file in yaml format,
        env_file: Optional[Path] = None,
        # Configure the ConfigMap used for env variables that are not Secret,
        config_map_name: Optional[str] = None,
        # Configure the Secret used for env variables that are Secret,
        secret_name: Optional[str] = None,
        # Read secrets from a file in yaml format,
        secrets_file: Optional[Path] = None,
        # Configure the databox deploy,
        deploy_name: Optional[str] = None,
        pod_name: Optional[str] = None,
        # Other args,
        load_examples: bool = False,
        print_env_on_load: bool = True,
        dev_mode: Optional[DevboxDevModeArgs] = None,
        # If True, skip resource creation if active resources with the same name exist.
        use_cache: bool = True,
        # If True, log extra debug messages
        use_verbose_logs: bool = False,
    ):
        super().__init__()
        try:
            self.args: DevboxArgs = DevboxArgs(
                name=name,
                version=version,
                enabled=enabled,
                image_name=image_name,
                image_tag=image_tag,
                entrypoint=entrypoint,
                command=command,
                mount_workspace=mount_workspace,
                workspace_volume_name=workspace_volume_name,
                workspace_parent_container_path=workspace_parent_container_path,
                install_requirements=install_requirements,
                requirements_file_path=requirements_file_path,
                mount_aws_config=mount_aws_config,
                aws_config_path=aws_config_path,
                aws_config_container_path=aws_config_container_path,
                init_airflow=init_airflow,
                use_products_as_airflow_dags=use_products_as_airflow_dags,
                airflow_dags_path=airflow_dags_path,
                create_airflow_test_user=create_airflow_test_user,
                airflow_executor=airflow_executor,
                mount_airflow_home=mount_airflow_home,
                airflow_home_dir=airflow_home_dir,
                airflow_home_container_path=airflow_home_container_path,
                init_airflow_db=init_airflow_db,
                wait_for_airflow_db=wait_for_airflow_db,
                airflow_db_app=airflow_db_app,
                airflow_db_user=airflow_db_user,
                airflow_db_password=airflow_db_password,
                airflow_db_schema=airflow_db_schema,
                airflow_db_host=airflow_db_host,
                airflow_db_port=airflow_db_port,
                airflow_db_driver=airflow_db_driver,
                db_connections=db_connections,
                init_airflow_scheduler=init_airflow_scheduler,
                init_airflow_webserver=init_airflow_webserver,
                airflow_webserver_container_port=airflow_webserver_container_port,
                airflow_webserver_host_port=airflow_webserver_host_port,
                airflow_webserver_port_name=airflow_webserver_port_name,
                container_name=container_name,
                container_detach=container_detach,
                container_auto_remove=container_auto_remove,
                container_remove=container_remove,
                env=env,
                env_file=env_file,
                config_map_name=config_map_name,
                secret_name=secret_name,
                secrets_file=secrets_file,
                deploy_name=deploy_name,
                pod_name=pod_name,
                load_examples=load_examples,
                print_env_on_load=print_env_on_load,
                dev_mode=dev_mode,
                use_cache=use_cache,
                use_verbose_logs=use_verbose_logs,
            )
        except Exception as e:
            logger.error(f"Args for {self.__class__.__name__} are not valid")
            raise

    def get_container_name(self) -> str:
        return self.args.container_name or get_default_container_name(self.args.name)

    def get_env_data_from_file(self) -> Optional[Dict[str, str]]:
        import yaml

        env_file_path = self.args.env_file
        if (
            env_file_path is not None
            and env_file_path.exists()
            and env_file_path.is_file()
        ):
            logger.debug(f"Reading {env_file_path}")
            env_data_from_file = yaml.safe_load(env_file_path.read_text())
            if env_data_from_file is not None and isinstance(env_data_from_file, dict):
                return env_data_from_file
            else:
                print_error(f"Invalid env_file: {env_file_path}")
        return None

    def get_secret_data_from_file(self) -> Optional[Dict[str, str]]:
        import yaml

        secrets_file_path = self.args.secrets_file
        if (
            secrets_file_path is not None
            and secrets_file_path.exists()
            and secrets_file_path.is_file()
        ):
            logger.debug(f"Reading {secrets_file_path}")
            secret_data_from_file = yaml.safe_load(secrets_file_path.read_text())
            if secret_data_from_file is not None and isinstance(
                secret_data_from_file, dict
            ):
                return secret_data_from_file
            else:
                print_error(f"Invalid secrets_file: {secrets_file_path}")
        return None

    ######################################################
    ## Docker Resources
    ######################################################

    def init_airflow_on_docker_container(self, container: DockerContainer) -> None:
        """
        Initialize airflow on a docker container
        """

        if not self.args.init_airflow:
            return

        # Update init_airflow_db arg if None
        if self.args.init_airflow_db is None:
            self.args.init_airflow_db = True

        # Workspace paths
        workspace_name = self.workspace_root_path.stem
        workspace_root_container_path = Path(
            self.args.workspace_parent_container_path
        ).joinpath(workspace_name)
        products_dir_container_path = workspace_root_container_path.joinpath(
            self.products_dir
        )

        # Airflow db connection
        airflow_db_user = self.args.airflow_db_user
        airflow_db_password = self.args.airflow_db_password
        airflow_db_schema = self.args.airflow_db_schema
        airflow_db_host = self.args.airflow_db_host
        airflow_db_port = self.args.airflow_db_port
        airflow_db_driver = self.args.airflow_db_driver
        if self.args.airflow_db_app is not None and isinstance(
            self.args.airflow_db_app, DbApp
        ):
            logger.debug(
                f"Reading Airflow db connection from DbApp: {self.args.airflow_db_app.name}"
            )
            if airflow_db_user is None:
                airflow_db_user = self.args.airflow_db_app.get_db_user()
            if airflow_db_password is None:
                airflow_db_password = self.args.airflow_db_app.get_db_password()
            if airflow_db_schema is None:
                airflow_db_schema = self.args.airflow_db_app.get_db_schema()
            if airflow_db_host is None:
                airflow_db_host = self.args.airflow_db_app.get_db_host_docker()
            if airflow_db_port is None:
                airflow_db_port = self.args.airflow_db_app.get_db_port_docker()
            if airflow_db_driver is None:
                airflow_db_driver = self.args.airflow_db_app.get_db_driver()
        db_connection_url = f"{airflow_db_driver}://{airflow_db_user}:{airflow_db_password}@{airflow_db_host}:{airflow_db_port}/{airflow_db_schema}"

        airflow_env: Dict[str, Any] = {
            "INIT_AIRFLOW": str(self.args.init_airflow),
            "INIT_AIRFLOW_DB": str(self.args.init_airflow_db),
            "WAIT_FOR_AIRFLOW_DB": str(self.args.wait_for_airflow_db),
            "AIRFLOW_DB_USER": str(airflow_db_user),
            "AIRFLOW_DB_PASSWORD": str(airflow_db_password),
            "AIRFLOW_SCHEMA": str(airflow_db_schema),
            "AIRFLOW_DB_HOST": str(airflow_db_host),
            "AIRFLOW_DB_PORT": str(airflow_db_port),
            "INIT_AIRFLOW_SCHEDULER": str(self.args.init_airflow_scheduler),
            "INIT_AIRFLOW_WEBSERVER": str(self.args.init_airflow_webserver),
            "AIRFLOW__CORE__LOAD_EXAMPLES": str(self.args.load_examples),
            "CREATE_AIRFLOW_TEST_USER": str(self.args.create_airflow_test_user),
            "AIRFLOW__CORE__EXECUTOR": str(self.args.airflow_executor),
        }
        # Set the AIRFLOW__CORE__SQL_ALCHEMY_CONN
        if "None" not in db_connection_url:
            airflow_env["AIRFLOW__CORE__SQL_ALCHEMY_CONN"] = db_connection_url
        # Set the AIRFLOW__CORE__DAGS_FOLDER
        if self.args.mount_workspace and self.args.use_products_as_airflow_dags:
            airflow_env["AIRFLOW__CORE__DAGS_FOLDER"] = str(products_dir_container_path)
        elif self.args.airflow_dags_path is not None:
            airflow_env["AIRFLOW__CORE__DAGS_FOLDER"] = self.args.airflow_dags_path
        # Set the AIRFLOW__CONN_ variables
        if self.args.db_connections is not None:
            for conn_id, conn_url in self.args.db_connections.items():
                try:
                    af_conn_id = str("AIRFLOW_CONN_{}".format(conn_id)).upper()
                    airflow_env[af_conn_id] = conn_url
                except Exception as e:
                    logger.exception(e)
                    continue
        # Update the container.environment to include airflow_env
        container.environment.update(airflow_env)

        # Open the airflow webserver port if init_airflow_webserver = True
        if self.args.init_airflow_webserver:
            ws_port: Dict[str, int] = {
                str(
                    self.args.airflow_webserver_container_port
                ): self.args.airflow_webserver_host_port,
            }
            if container.ports is None:
                container.ports = {}
            container.ports.update(ws_port)

    def get_docker_rg(
        self, docker_build_context: DockerBuildContext
    ) -> Optional[DockerResourceGroup]:

        app_name = self.args.name
        logger.debug(f"Building {app_name} DockerResourceGroup")

        # Workspace paths
        workspace_name = self.workspace_root_path.stem
        workspace_root_container_path = Path(
            self.args.workspace_parent_container_path
        ).joinpath(workspace_name)
        requirements_file_container_path = workspace_root_container_path.joinpath(
            self.args.requirements_file_path
        )
        scripts_dir_container_path = workspace_root_container_path.joinpath(
            self.scripts_dir
        )
        storage_dir_container_path = workspace_root_container_path.joinpath(
            self.storage_dir
        )
        meta_dir_container_path = workspace_root_container_path.joinpath(self.meta_dir)
        products_dir_container_path = workspace_root_container_path.joinpath(
            self.products_dir
        )
        notebooks_dir_container_path = workspace_root_container_path.joinpath(
            self.notebooks_dir
        )
        workspace_config_dir_container_path = workspace_root_container_path.joinpath(
            self.workspace_config_dir
        )

        # Container Environment
        container_env: Dict[str, Any] = {
            # Env variables used by data workflows and data assets
            "PHI_WORKSPACE_PARENT": str(self.args.workspace_parent_container_path),
            "PHI_WORKSPACE_ROOT": str(workspace_root_container_path),
            "PHI_SCRIPTS_DIR": str(scripts_dir_container_path),
            "PHI_STORAGE_DIR": str(storage_dir_container_path),
            "PHI_META_DIR": str(meta_dir_container_path),
            "PHI_PRODUCTS_DIR": str(products_dir_container_path),
            "PHI_NOTEBOOKS_DIR": str(notebooks_dir_container_path),
            "PHI_WORKSPACE_CONFIG_DIR": str(workspace_config_dir_container_path),
            "INSTALL_REQUIREMENTS": str(self.args.install_requirements),
            "REQUIREMENTS_FILE_PATH": str(requirements_file_container_path),
            # Print env when the container starts
            "PRINT_ENV_ON_LOAD": str(self.args.print_env_on_load),
            # Dev mode args
            "INSTALL_PHIDATA_DEV": str(self.args.dev_mode.install_phidata_dev)
            if self.args.dev_mode is not None
            else str(False),
            "PHIDATA_DIR_PATH": self.args.dev_mode.phidata_dir_container_path
            if self.args.dev_mode is not None
            else str(False),
        }
        # Update the container env using env_file
        env_data_from_file = self.get_env_data_from_file()
        if env_data_from_file is not None:
            container_env.update(env_data_from_file)
        # Update the container env with user provided env
        if self.args.env is not None and isinstance(self.args.env, dict):
            container_env.update(self.args.env)

        # Container Volumes
        # container_volumes is a dictionary which configures the volumes to mount
        # inside the container. The key is either the host path or a volume name,
        # and the value is a dictionary with 2 keys:
        #   bind - The path to mount the volume inside the container
        #   mode - Either rw to mount the volume read/write, or ro to mount it read-only.
        # For example:
        # {
        #   '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
        #   '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}
        # }
        container_volumes = {}
        # Create a volume for the workspace dir
        if self.args.mount_workspace:
            workspace_root_path_str = str(self.workspace_root_path)
            workspace_root_container_path_str = str(workspace_root_container_path)
            logger.debug(f"Mounting: {workspace_root_path_str}")
            logger.debug(f"\tto: {workspace_root_container_path_str}")
            container_volumes[workspace_root_path_str] = {
                "bind": workspace_root_container_path_str,
                "mode": "rw",
            }
        # Create a volume for aws credentials
        if self.args.mount_aws_config:
            aws_config_path_str = str(self.args.aws_config_path)
            logger.debug(f"Mounting: {aws_config_path_str}")
            logger.debug(f"\tto: {self.args.aws_config_container_path}")
            container_volumes[aws_config_path_str] = {
                "bind": self.args.aws_config_container_path,
                "mode": "ro",
            }
            container_env[
                "AWS_CONFIG_FILE"
            ] = f"{self.args.aws_config_container_path}/config"
            container_env[
                "AWS_SHARED_CREDENTIALS_FILE"
            ] = f"{self.args.aws_config_container_path}/credentials"
        # Create a volume for Phidata dev mode if dev_mode is enabled
        if self.args.dev_mode is not None:
            # mount the phidata directory if install_phidata_dev = True
            if (
                self.args.dev_mode.install_phidata_dev
                and self.args.dev_mode.phidata_dir_path is not None
            ):
                phidata_dir_absolute_path_str = str(self.args.dev_mode.phidata_dir_path)
                logger.debug(f"Mounting: {phidata_dir_absolute_path_str}")
                logger.debug(f"\tto: {self.args.dev_mode.phidata_dir_container_path}")
                container_volumes[phidata_dir_absolute_path_str] = {
                    "bind": self.args.dev_mode.phidata_dir_container_path,
                    "mode": "rw",
                }
        # Mount airflow home if needed (experimental)
        if self.args.mount_airflow_home is not None:
            airflow_home_path_str = str(
                self.workspace_root_path.joinpath(self.args.airflow_home_dir)
            )
            airflow_home_container_path_str = str(self.args.airflow_home_container_path)
            logger.debug(f"Mounting: {airflow_home_path_str}")
            logger.debug(f"\tto: {airflow_home_container_path_str}")
            container_volumes[airflow_home_path_str] = {
                "bind": airflow_home_container_path_str,
                "mode": "rw",
            }

        # Create the container
        docker_container = DockerContainer(
            name=self.get_container_name(),
            image=get_image_str(self.args.image_name, self.args.image_tag),
            entrypoint=self.args.entrypoint,
            command=self.args.command,
            detach=self.args.container_detach,
            auto_remove=self.args.container_auto_remove,
            remove=self.args.container_remove,
            stdin_open=True,
            tty=True,
            environment=container_env,
            network=docker_build_context.network,
            volumes=container_volumes,
            use_cache=self.args.use_cache,
            use_verbose_logs=self.args.use_verbose_logs,
        )
        # Initialize airflow on container
        self.init_airflow_on_docker_container(docker_container)
        # logger.debug(f"Devbox Container Env: {docker_container.environment}")

        docker_rg = DockerResourceGroup(
            name=app_name,
            enabled=self.args.enabled,
            network=DockerNetwork(name=docker_build_context.network),
            containers=[docker_container],
        )
        return docker_rg

    def init_docker_resource_groups(
        self, docker_build_context: DockerBuildContext
    ) -> None:
        docker_rg = self.get_docker_rg(docker_build_context)
        if docker_rg is not None:
            if self.docker_resource_groups is None:
                self.docker_resource_groups = OrderedDict()
            self.docker_resource_groups[docker_rg.name] = docker_rg

    ######################################################
    ## K8s Resources
    ######################################################

    def init_airflow_on_k8s_container(
        self, container: CreateContainer, k8s_resource_group: CreateK8sResourceGroup
    ) -> None:
        """
        Initialize airflow on a k8s container
        """

        if not self.args.init_airflow:
            return

        # Update init_airflow_db arg if None
        if self.args.init_airflow_db is None:
            self.args.init_airflow_db = True

        airflow_cm = CreateConfigMap(
            cm_name=get_default_configmap_name("devbox-airflow"),
            app_name=self.args.name,
            data={
                "INIT_AIRFLOW": str(self.args.init_airflow),
                "INIT_AIRFLOW_DB": str(self.args.init_airflow_db),
                "WAIT_FOR_AIRFLOW_DB": str(self.args.wait_for_airflow_db),
                "AIRFLOW_DB_CONN_URL": self.args.airflow_db_conn_url,
                "AIRFLOW_DB_CONN_PORT": self.args.airflow_db_conn_port,
                "AIRFLOW_DB_USER": self.args.airflow_db_user,
                "AIRFLOW_DB_PASSWORD": self.args.airflow_db_password,
                "AIRFLOW_SCHEMA": self.args.airflow_schema,
                "INIT_AIRFLOW_SCHEDULER": str(self.args.init_airflow_scheduler),
                "INIT_AIRFLOW_WEBSERVER": str(self.args.init_airflow_webserver),
                "CREATE_AIRFLOW_TEST_USER": str(self.args.init_airflow_webserver),
                "AIRFLOW__CORE__LOAD_EXAMPLES": str(self.args.load_examples),
            },
        )

        # Add airflow_cm to container env and
        if container.envs_from_configmap is None:
            container.envs_from_configmap = []
        container.envs_from_configmap.append(airflow_cm.cm_name)
        if k8s_resource_group.config_maps is None:
            k8s_resource_group.config_maps = []
        k8s_resource_group.config_maps.append(airflow_cm)

        # Set the AIRFLOW__CORE__DAGS_FOLDER
        if self.args.mount_workspace and self.args.use_products_as_airflow_dags:
            projects_dir_container_path = Path(
                self.args.workspace_parent_container_path
            ).joinpath(self.args.workspace_dir_path.stem, self.args.projects_dir)
            airflow_cm.data["AIRFLOW__CORE__DAGS_FOLDER"] = projects_dir_container_path
        elif self.args.airflow_dags_path is not None:
            airflow_cm.data["AIRFLOW__CORE__DAGS_FOLDER"] = self.args.airflow_dags_path
        if self.args.db_connections is not None:
            for conn_id, conn_url in self.args.db_connections.items():
                try:
                    af_conn_id = str("AIRFLOW_CONN_{}".format(conn_id)).upper()
                    airflow_cm.data[af_conn_id] = conn_url
                except Exception as e:
                    logger.exception(e)
                    continue
        # Open the airflow webserver port if init_airflow_webserver = True
        if self.args.init_airflow_webserver:
            ws_port = CreatePort(
                name=self.args.airflow_webserver_port_name,
                container_port=self.args.airflow_webserver_container_port,
            )
            if container.ports is None:
                container.ports = []
            container.ports.append(ws_port)

    def get_devbox_k8s_rg(
        self, k8s_build_context: K8sBuildContext
    ) -> Optional[K8sResourceGroup]:
        logger.debug(f"Init Devbox K8sResourceGroup")

        # Set the Devbox Env
        # Devbox Config-Map is a dict of environment variables which are not secrets.
        # The keys of this configmap will become env variables in the devbox container
        workspace_dir_container_path = Path(
            self.args.workspace_parent_container_path
        ).joinpath(self.args.workspace_dir_path.stem)
        projects_dir_container_path = workspace_dir_container_path.joinpath(
            self.args.projects_dir
        )
        devbox_cm = CreateConfigMap(
            cm_name=get_default_configmap_name(self.args.name),
            app_name=self.args.name,
            data={
                # Env variables used by data workflows and data assets
                "PHI_DATA_DIR": self.args.data_dir_container_path,
                "PHI_PROJECTS_DIR": str(projects_dir_container_path),
                "PHI_WORKSPACE_DIR": str(workspace_dir_container_path),
                "PHI_WORKSPACE_PARENT": str(self.args.workspace_parent_container_path),
                # Configure python packages to install
                "INSTALL_REQUIREMENTS": str(self.args.install_requirements),
                "REQUIREMENTS_FILE_PATH": self.args.requirements_file_container_path,
                # Print these env variables when the container is loaded
                "PRINT_ENV_ON_LOAD": str(self.args.print_env_on_load),
                # Dev mode args
                "INSTALL_PHIDATA_DEV": str(self.args.dev_mode.install_phidata_dev)
                if self.args.dev_mode is not None
                else str(False),
                "PHIDATA_DIR_PATH": self.args.dev_mode.phidata_dir_container_path
                if self.args.dev_mode is not None
                else str(False),
            },
        )
        # Update the devbox env with user provided env
        if self.args.env is not None and isinstance(self.args.env, dict):
            devbox_cm.data.update(self.args.env)

        # Devbox Volumes
        devbox_volumes = []
        # Create a volume for the requirements file
        # if install_requirements = True
        if self.args.install_requirements:
            requirements_file_absolute_path = str(
                self.args.workspace_dir_path.joinpath(self.args.requirements_file_path)
            )
            logger.debug(f"Mounting: {requirements_file_absolute_path}")
            logger.debug(f"\tto: {self.args.requirements_file_container_path}")
            requirements_volume = CreateVolume(
                volume_name=self.args.requirements_volume_name,
                app_name=self.args.name,
                mount_path=self.args.requirements_file_container_path,
                volume_type=VolumeType.HOST_PATH,
                host_path=HostPathVolumeSource(path=requirements_file_absolute_path),
            )
            devbox_volumes.append(requirements_volume)
        # Create a volume for the data dir
        # if create_data_volume = True
        if self.args.create_data_volume:
            if (
                self.args.use_host_path_for_data_volume
                and self.args.data_dir_path is not None
            ):
                data_dir_absolute_path = str(
                    self.args.workspace_dir_path.joinpath(self.args.data_dir_path)
                )
                logger.debug(f"Mounting: {data_dir_absolute_path}")
                logger.debug(f"\tto: {self.args.data_dir_container_path}")
                data_volume = CreateVolume(
                    volume_name=self.args.data_dir_volume_name,
                    app_name=self.args.name,
                    mount_path=self.args.data_dir_container_path,
                    volume_type=VolumeType.HOST_PATH,
                    host_path=HostPathVolumeSource(
                        path=data_dir_absolute_path,
                    ),
                )
                devbox_volumes.append(data_volume)
            elif self.args.use_empty_dir_for_data_volume:
                logger.debug(f"Mounting EmptyDir")
                logger.debug(f"\tto: {self.args.data_dir_container_path}")
                data_volume = CreateVolume(
                    volume_name=self.args.data_dir_volume_name,
                    app_name=self.args.name,
                    mount_path=self.args.data_dir_container_path,
                    volume_type=VolumeType.EMPTY_DIR,
                    empty_dir=EmptyDirVolumeSource(),
                )
                devbox_volumes.append(data_volume)
        # Create a volume for the projects dir
        # if mount_workspace = True
        if self.args.mount_workspace:
            if self.args.use_host_path_for_workspace:
                ws_dir_container_path_str = str(
                    Path(self.args.workspace_parent_container_path).joinpath(
                        self.args.workspace_dir_path.stem
                    )
                )
                ws_dir_path_str = str(self.args.workspace_dir_path)
                logger.debug(f"Mounting: {ws_dir_path_str}")
                logger.debug(f"\tto: {ws_dir_container_path_str}")
                workspace_volume = CreateVolume(
                    volume_name=self.args.workspace_volume_name,
                    app_name=self.args.name,
                    mount_path=ws_dir_container_path_str,
                    volume_type=VolumeType.HOST_PATH,
                    host_path=HostPathVolumeSource(
                        path=ws_dir_path_str,
                    ),
                )
                devbox_volumes.append(workspace_volume)
        # Airflow conf file
        if self.args.mount_airflow_dir:
            airflow_dir_file_absolute_path = str(
                self.args.workspace_dir_path.joinpath(self.args.airflow_dir_path)
            )
            logger.debug(f"Mounting: {airflow_dir_file_absolute_path}")
            logger.debug(f"\tto: {self.args.airflow_dir_container_path}")
            airflow_dir_volume = CreateVolume(
                volume_name=self.args.airflow_volume_name,
                app_name=self.args.name,
                mount_path=self.args.airflow_dir_container_path,
                volume_type=VolumeType.HOST_PATH,
                host_path=HostPathVolumeSource(path=airflow_dir_file_absolute_path),
            )
            devbox_volumes.append(airflow_dir_volume)
        # Create a volume for Phidata dev mode
        # if dev_mode is enabled
        if self.args.dev_mode is not None:
            # mount the phidata directory if install_phidata_dev = True
            if (
                self.args.dev_mode.install_phidata_dev
                and self.args.dev_mode.phidata_dir_path is not None
            ):
                phidata_dir_absolute_path = str(self.args.dev_mode.phidata_dir_path)
                logger.debug(f"Mounting: {phidata_dir_absolute_path}")
                logger.debug(f"\tto: {self.args.dev_mode.phidata_dir_container_path}")
                phidata_volume = CreateVolume(
                    volume_name=self.args.dev_mode.phidata_volume_name,
                    app_name=self.args.name,
                    mount_path=self.args.dev_mode.phidata_dir_container_path,
                    volume_type=VolumeType.HOST_PATH,
                    host_path=HostPathVolumeSource(
                        path=phidata_dir_absolute_path,
                    ),
                )
                devbox_volumes.append(phidata_volume)

        # Create the devbox container
        devbox_k8s_container = CreateContainer(
            container_name=f"{self.args.name}-container",
            app_name=self.args.name,
            image_name=self.args.image_name,
            image_tag=self.args.image_tag,
            # Equivalent to docker images CMD
            args=self.args.command,
            # Equivalent to docker images ENTRYPOINT
            command=self.args.entrypoint,
            envs_from_configmap=[devbox_cm.cm_name],
            volumes=devbox_volumes,
        )
        devbox_deployment = CreateDeployment(
            deploy_name=f"{self.args.name}-deploy",
            pod_name=f"{self.args.name}-pod",
            app_name=self.args.name,
            namespace=k8s_build_context.namespace,
            service_account_name=k8s_build_context.service_account_name,
            containers=[devbox_k8s_container],
            volumes=devbox_volumes,
            labels=k8s_build_context.labels,
        )
        devbox_k8s_resource_group = CreateK8sResourceGroup(
            name=self.args.name,
            enabled=self.args.enabled,
            config_maps=[devbox_cm],
            deployments=[devbox_deployment],
        )
        # Initialize airflow on container
        self.init_airflow_on_k8s_container(
            devbox_k8s_container, devbox_k8s_resource_group
        )
        return devbox_k8s_resource_group.create()

    def init_k8s_resource_groups(self, k8s_build_context: K8sBuildContext) -> None:
        devbox_k8s_rg: Optional[K8sResourceGroup] = self.get_devbox_k8s_rg(
            k8s_build_context
        )
        # logger.debug("devbox_k8s_rg: {}".format(devbox_k8s_rg))
        if devbox_k8s_rg is not None:
            if self.k8s_resource_groups is None:
                self.k8s_resource_groups = OrderedDict()
            self.k8s_resource_groups[devbox_k8s_rg.name] = devbox_k8s_rg
