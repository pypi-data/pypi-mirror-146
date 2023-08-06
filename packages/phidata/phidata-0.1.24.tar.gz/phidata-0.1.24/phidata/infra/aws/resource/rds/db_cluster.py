from typing import Optional, Any, Dict, List, Literal

from botocore.exceptions import ClientError

from phidata.infra.aws.api_client import AwsApiClient
from phidata.infra.aws.resource.base import AwsResource
from phidata.infra.aws.resource.cloudformation import CloudFormationStack
from phidata.utils.cli_console import print_info, print_error, print_warning
from phidata.utils.log import logger


class DbCluster(AwsResource):
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html
    """

    resource_type = "DbCluster"
    service_name = "rds"

    # Name of the cluster.
    name: str
    # The name of the database engine to be used for this DB cluster.
    engine: Literal["aurora", "aurora-mysql", "aurora-postgresql", "mysql", "postgres"]
    # The compute and memory capacity of each DB instance in the Multi-AZ DB cluster, for example db.m6g.xlarge.
    # Not all DB instance classes are available in all Amazon Web Services Regions, or for all database engines.
    # This setting is required to create a Multi-AZ DB cluster.
    db_instance_class: Optional[str] = None

    # The version number of the database engine to use.
    engine_version: Optional[str] = None
    # The port number on which the instances in the DB cluster accept connections.
    port: Optional[int] = None
    # The name of the master user for the DB cluster.
    # Constraints:
    #   Must be 1 to 16 letters or numbers.
    #   First character must be a letter.
    #   Can't be a reserved word for the chosen database engine.
    master_username: Optional[str] = None
    # The password for the master database user. This password can contain any printable ASCII character
    # except "/", """, or "@".
    # Constraints: Must contain from 8 to 41 characters.
    master_user_password: Optional[str] = None

    # A list of Availability Zones (AZs) where DB instances in the DB cluster can be created.
    availability_zones: Optional[List[str]] = None
    # The number of days for which automated backups are retained.
    # Default: 1
    # Constraints: Must be a value from 1 to 35
    backup_retention_period: Optional[int] = None
    # A value that indicates that the DB cluster should be associated with the specified CharacterSet.
    character_set_name: Optional[str] = None
    # The name for your database of up to 64 alphanumeric characters.
    # If you do not provide a name, Amazon RDS doesn't create a database in the DB cluster you are creating.
    database_name: Optional[str] = None
    # The DB cluster identifier. This parameter is stored as a lowercase string.
    # If None, use the name as the dbcluster_identifier
    # Constraints:
    #   Must contain from 1 to 63 letters, numbers, or hyphens.
    #   First character must be a letter.
    #   Can't end with a hyphen or contain two consecutive hyphens.
    dbcluster_identifier: Optional[str] = None
    # The name of the DB cluster parameter group to associate with this DB cluster.
    # If you do not specify a value, then the default DB cluster parameter group for the specified DB engine and version is used.
    # Constraints: If supplied, must match the name of an existing DB cluster parameter group.
    dbcluster_parameter_group_name: Optional[str] = None

    # The VPC CloudFormationStack to use
    vpc_stack: Optional[CloudFormationStack] = None
    # A list of EC2 VPC security groups to associate with this DB cluster.
    vpc_security_group_ids: Optional[List[str]] = None
    # A DB subnet group to associate with this DB cluster.
    # This setting is required to create a Multi-AZ DB cluster.
    db_subnet_group_name: Optional[str] = None
    # A value that indicates that the DB cluster should be associated with the specified option group.
    option_group_name: Optional[str] = None
    # The daily time range during which automated backups are created if automated backups are enabled
    # using the BackupRetentionPeriod parameter.
    # The default is a 30-minute window selected at random from an 8-hour block of time for each
    # Amazon Web Services Region.
    # Constraints:
    #   Must be in the format hh24:mi-hh24:mi .
    #   Must be in Universal Coordinated Time (UTC).
    #   Must not conflict with the preferred maintenance window.
    #   Must be at least 30 minutes.
    preferred_backup_window: Optional[str] = None
    # The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).
    # Format: ddd:hh24:mi-ddd:hh24:mi
    # The default is a 30-minute window selected at random from an 8-hour block of time for each
    # Amazon Web Services Region, occurring on a random day of the week.
    # Valid Days: Mon, Tue, Wed, Thu, Fri, Sat, Sun.
    # Constraints: Minimum 30-minute window.
    preferred_maintenance_window: Optional[str] = None
    # The Amazon Resource Name (ARN) of the source DB instance or DB cluster
    # if this DB cluster is created as a read replica.
    replication_source_identifier: Optional[str] = None
    # Tags to assign to the DB cluster.
    tags: Optional[List[Dict[str, str]]] = None
    # A value that indicates whether the DB cluster is encrypted.
    storage_encrypted: Optional[bool] = None
    # The Amazon Web Services KMS key identifier for an encrypted DB cluster.
    kms_key_id: Optional[str] = None
    # A value that indicates whether to enable mapping of Amazon Web Services Identity and Access Management (IAM)
    # accounts to database accounts. By default, mapping isn't enabled.
    enable_iamdatabase_authentication: Optional[bool] = None
    # The target backtrack window, in seconds. To disable backtracking, set this value to 0.
    # Default: 0
    backtrack_window: Optional[int] = None
    # The list of log types that need to be enabled for exporting to CloudWatch Logs.
    # The values in the list depend on the DB engine being used.
    # RDS for MySQL: Possible values are error , general , and slowquery .
    # RDS for PostgreSQL: Possible values are postgresql and upgrade .
    # Aurora MySQL: Possible values are audit , error , general , and slowquery .
    # Aurora PostgreSQL: Possible value is postgresql .
    enable_cloudwatch_logs_exports: Optional[List[str]] = None
    # The DB engine mode of the DB cluster,
    # either provisioned , serverless , parallelquery , global , or multimaster .
    engine_mode: Optional[Literal["provisioned", "serverless", "parallelquery", "global", "multimaster"]] = None
    # For DB clusters in serverless DB engine mode, the scaling properties of the DB cluster.
    scaling_configuration: Optional[Dict[str, Any]] = None
    # A value that indicates whether the DB cluster has deletion protection enabled.
    # The database can't be deleted when deletion protection is enabled. By default, deletion protection isn't enabled.
    deletion_protection: Optional[bool] = None
    # The global cluster ID of an Aurora cluster that becomes the primary cluster in the new global database cluster.
    global_cluster_identifier: Optional[str] = None
    # A value that indicates whether to enable the HTTP endpoint for an Aurora Serverless v1 DB cluster.
    # By default, the HTTP endpoint is disabled.
    # When enabled, the HTTP endpoint provides a connectionless web service API for running SQL queries on the
    # Aurora Serverless v1 DB cluster. You can also query your database from inside the RDS console with the query editor.
    enable_http_endpoint: Optional[bool] = None
    # A value that indicates whether to copy all tags from the DB cluster to snapshots of the DB cluster.
    # The default is not to copy them.
    copy_tags_to_snapshot: Optional[bool] = None
    # The Active Directory directory ID to create the DB cluster in.
    # For Amazon Aurora DB clusters, Amazon RDS can use Kerberos authentication to authenticate users that connect to
    # the DB cluster.
    domain: Optional[str] = None
    # Specify the name of the IAM role to be used when making API calls to the Directory Service.
    domain_iamrole_name: Optional[str] = None
    enable_global_write_forwarding: Optional[bool] = None
    # The amount of storage in gibibytes (GiB) to allocate to each DB instance in the Multi-AZ DB cluster.
    allocated_storage: Optional[int] = None
    # Specifies the storage type to be associated with the DB cluster.
    # This setting is required to create a Multi-AZ DB cluster.
    # Valid values: io1
    # When specified, a value for the Iops parameter is required.
    # Default: io1
    storage_type: Optional[str] = None
    # The amount of Provisioned IOPS (input/output operations per second) to be initially allocated for each DB
    # instance in the Multi-AZ DB cluster.
    iops: Optional[int] = None
    # A value that indicates whether the DB cluster is publicly accessible.
    # When the DB cluster is publicly accessible, its Domain Name System (DNS) endpoint resolves to the private IP
    # address from within the DB cluster's virtual private cloud (VPC). It resolves to the public IP address from
    # outside of the DB cluster's VPC. Access to the DB cluster is ultimately controlled by the security group it uses.
    # That public access isn't permitted if the security group assigned to the DB cluster doesn't permit it.
    # When the DB cluster isn't publicly accessible, it is an internal DB cluster with a DNS name
    # that resolves to a private IP address.
    publicly_accessible: Optional[bool] = None
    # A value that indicates whether minor engine upgrades are applied automatically to the DB cluster during the
    # maintenance window. By default, minor engine upgrades are applied automatically.
    auto_minor_version_upgrade: Optional[bool] = None
    # The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB cluster.
    # To turn off collecting Enhanced Monitoring metrics, specify 0. The default is 0.
    # If MonitoringRoleArn is specified, also set MonitoringInterval to a value other than 0.
    # Valid Values: 0, 1, 5, 10, 15, 30, 60
    monitoring_interval: Optional[int] = None
    # The Amazon Resource Name (ARN) for the IAM role that permits RDS to send
    # Enhanced Monitoring metrics to Amazon CloudWatch Logs.
    monitoring_role_arn: Optional[str] = None
    enable_performance_insights: Optional[bool] = None
    performance_insights_kmskey_id: Optional[str] = None
    performance_insights_retention_period: Optional[int] = None
    # The ID of the region that contains the source for the db cluster.
    source_region: Optional[str] = None

    # provided by api on create
    # DBCluster returned on read
    db_cluster: Optional[Dict] = None

    def get_db_cluster_identifier(self):
        return self.dbcluster_identifier or self.name

    def _create(self, aws_client: AwsApiClient) -> bool:
        """Creates the DbCluster

        Args:
            aws_client: The AwsApiClient for the current cluster
        """

        logger.debug(
            "Creating {} | {}".format(
                self.get_resource_type(), self.get_resource_name()
            )
        )
        try:
            # create a dict of args which are not null, otherwise aws type validation fails
            non_null_args = {}

            non_null_args["DBClusterIdentifier"] = self.get_db_cluster_identifier()
            if self.engine_version:
                non_null_args["EngineVersion"] = self.engine_version
            if self.port:
                non_null_args["Port"] = self.port
            if self.master_username:
                non_null_args["MasterUsername"] = self.master_username
            if self.master_user_password:
                non_null_args["MasterUserPassword"] = self.master_user_password
            if self.availability_zones:
                non_null_args["AvailabilityZones"] = self.availability_zones
            if self.backup_retention_period:
                non_null_args["BackupRetentionPeriod"] = self.backup_retention_period
            if self.character_set_name:
                non_null_args["CharacterSetName"] = self.character_set_name
            if self.database_name:
                non_null_args["DatabaseName"] = self.database_name
            if self.dbcluster_parameter_group_name:
                non_null_args["DBClusterParameterGroupName"] = self.dbcluster_parameter_group_name
            if self.option_group_name:
                non_null_args["OptionGroupName"] = self.option_group_name
            if self.preferred_backup_window:
                non_null_args["PreferredBackupWindow"] = self.preferred_backup_window
            if self.preferred_maintenance_window:
                non_null_args["PreferredMaintenanceWindow"] = self.preferred_maintenance_window
            if self.replication_source_identifier:
                non_null_args["ReplicationSourceIdentifier"] = self.replication_source_identifier
            if self.tags:
                non_null_args["Tags"] = self.tags
            if self.storage_encrypted:
                non_null_args["StorageEncrypted"] = self.storage_encrypted
            if self.kms_key_id:
                non_null_args["KmsKeyId"] = self.kms_key_id
            if self.enable_iamdatabase_authentication:
                non_null_args["EnableIamdatabaseAuthentication"] = self.enable_iamdatabase_authentication
            if self.backtrack_window:
                non_null_args["BacktrackWindow"] = self.backtrack_window
            if self.enable_cloudwatch_logs_exports:
                non_null_args["EnableCloudwatchLogsExports"] = self.enable_cloudwatch_logs_exports
            if self.engine_mode:
                non_null_args["EngineMode"] = self.engine_mode
            if self.scaling_configuration:
                non_null_args["ScalingConfiguration"] = self.scaling_configuration
            if self.deletion_protection:
                non_null_args["DeletionProtection"] = self.deletion_protection
            if self.global_cluster_identifier:
                non_null_args["GlobalClusterIdentifier"] = self.global_cluster_identifier
            if self.enable_http_endpoint:
                non_null_args["EnableHttpEndpoint"] = self.enable_http_endpoint
            if self.copy_tags_to_snapshot:
                non_null_args["CopyTagsToSnapshot"] = self.copy_tags_to_snapshot
            if self.domain:
                non_null_args["Domain"] = self.domain
            if self.domain_iamrole_name:
                non_null_args["DomainIAMRoleName"] = self.domain_iamrole_name
            if self.enable_global_write_forwarding:
                non_null_args["EnableGlobalWriteForwarding"] = self.enable_global_write_forwarding
            if self.db_instance_class:
                non_null_args["DBClusterInstanceClass"] = self.db_instance_class
            if self.allocated_storage:
                non_null_args["AllocatedStorage"] = self.allocated_storage
            if self.storage_type:
                non_null_args["StorageType"] = self.storage_type
            if self.iops:
                non_null_args["Iops"] = self.iops
            if self.publicly_accessible:
                non_null_args["PubliclyAccessible"] = self.publicly_accessible
            if self.auto_minor_version_upgrade:
                non_null_args["AutoMinorVersionUpgrade"] = self.auto_minor_version_upgrade
            if self.monitoring_interval:
                non_null_args["MonitoringInterval"] = self.monitoring_interval
            if self.monitoring_role_arn:
                non_null_args["MonitoringRoleArn"] = self.monitoring_role_arn
            if self.enable_performance_insights:
                non_null_args["EnablePerformanceInsights"] = self.enable_performance_insights
            if self.performance_insights_kmskey_id:
                non_null_args["PerformanceInsightsKMSKeyId"] = self.performance_insights_kmskey_id
            if self.performance_insights_retention_period:
                non_null_args["PerformanceInsightsRetentionPeriod"] = self.performance_insights_retention_period
            if self.source_region:
                non_null_args["SourceRegion"] = self.source_region

            vpc_security_group_ids = self.vpc_security_group_ids
            if vpc_security_group_ids is None:
                if self.vpc_stack is not None:
                    vpc_stack_sg = self.vpc_stack.get_security_group(aws_client=aws_client)
                    if vpc_stack_sg is not None:
                        logger.debug(f"Using SecurityGroup: {vpc_stack_sg}")
                        vpc_security_group_ids = [vpc_stack_sg]
            if vpc_security_group_ids is not None:
                non_null_args["VpcSecurityGroupIds"] = vpc_security_group_ids

            db_subnet_group_name = self.db_subnet_group_name
            if db_subnet_group_name is None:
                if self.vpc_stack is not None:
                    private_subnets = self.vpc_stack.get_private_subnets(aws_client=aws_client)
                    if private_subnets is not None:
                        logger.debug(f"Creating DbSubnetGroup for: {private_subnets}")
                        # db_subnet_group_name = [vpc_stack_sg]
            if db_subnet_group_name is not None:
                non_null_args["DBSubnetGroupName"] = self.db_subnet_group_name

            ## Create cluster
            # Get the service_client
            service_client = self.get_service_client(aws_client)
            # logger.debug(f"ServiceClient: {service_client}")
            # logger.debug(f"ServiceClient type: {type(service_client)}")

            print_info(f"Creating DbCluster: {self.name}")
            create_response = service_client.create_db_cluster(
                Engine=self.engine,
                **non_null_args,
            )
            logger.debug(f"DbCluster: {create_response}")
            logger.debug(f"DbCluster type: {type(create_response)}")

            self.db_cluster = create_response.get("DBCluster", None)
            if create_response is not None:
                print_info(f"DbCluster created: {self.name}")
                logger.debug(f"DbCluster: {self.db_cluster}")
                self.active_resource = self.db_cluster
                return True
        except Exception as e:
            print_error(f"{self.get_resource_type()} could not be created, this operation is known to be buggy.")
            print_error("Please try again.")
            print_error(e)
        return False

    def _read(self, aws_client: AwsApiClient) -> Optional[Any]:
        """Returns the DbCluster

        Args:
            aws_client: The AwsApiClient for the current cluster
        """
        logger.debug(
            "Reading {} {}".format(self.get_resource_type(), self.get_resource_name())
        )
        try:
            service_client = self.get_service_client(aws_client)
            db_cluster_identifier = self.get_db_cluster_identifier()
            describe_response = service_client.describe_db_clusters(DBClusterIdentifier=db_cluster_identifier)
            logger.debug(f"DbClusters: {describe_response}")
            logger.debug(f"DbClusters type: {type(describe_response)}")

            db_clusters_list = describe_response.get("DBClusters", None)
            if db_clusters_list is not None and isinstance(db_clusters_list, list):
                for _db_cluster in db_clusters_list:
                    _cluster_identifier = _db_cluster.get("DBClusterIdentifier", None)
                    if _cluster_identifier == db_cluster_identifier:
                        self.db_cluster = _db_cluster
                        break

            if self.db_cluster is None:
                logger.debug("No DbCluster found")
                return None

            logger.debug(f"DbCluster found: {db_cluster_identifier}")
            logger.debug(f"DbCluster: {self.db_cluster}")
            self.active_resource = self.db_cluster
        except ClientError as ce:
            logger.debug(f"ClientError: {ce}")
            pass
        except Exception as e:
            print_error(f"Received error while reading {self.get_resource_type()}.")
            print_error("Please try again.")
            print_error(e)
        return self.active_resource

    def _delete(self, aws_client: AwsApiClient) -> bool:
        """Deletes the DbCluster

        Args:
            aws_client: The AwsApiClient for the current cluster
        """

        logger.debug(
            "Deleting {} | {}".format(
                self.get_resource_type(), self.get_resource_name()
            )
        )
        try:
            # Delete the DbCluster
            service_client = self.get_service_client(aws_client)
            self.active_resource = None

            db_cluster_identifier = self.get_db_cluster_identifier()
            delete_response = service_client.delete_db_cluster(DBClusterIdentifier=db_cluster_identifier)
            logger.debug(f"Delete Cluster response: {delete_response}")
            print_info(f"DbCluster deleted: {db_cluster_identifier}")
            return True
        except Exception as e:
            print_error(f"{self.get_resource_type()} could not be deleted, this operation is known to be buggy.")
            print_error("Please try again or delete resources manually.")
            print_error(e)
        return False
