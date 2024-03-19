import typing_extensions

from digital_ocean_python_sdk.paths import PathValues
from digital_ocean_python_sdk.apis.paths.v2_1_clicks import V21Clicks
from digital_ocean_python_sdk.apis.paths.v2_1_clicks_kubernetes import V21ClicksKubernetes
from digital_ocean_python_sdk.apis.paths.v2_account import V2Account
from digital_ocean_python_sdk.apis.paths.v2_account_keys import V2AccountKeys
from digital_ocean_python_sdk.apis.paths.v2_account_keys_ssh_key_identifier import V2AccountKeysSshKeyIdentifier
from digital_ocean_python_sdk.apis.paths.v2_actions import V2Actions
from digital_ocean_python_sdk.apis.paths.v2_actions_action_id import V2ActionsActionId
from digital_ocean_python_sdk.apis.paths.v2_apps import V2Apps
from digital_ocean_python_sdk.apis.paths.v2_apps_id import V2AppsId
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_components_component_name_logs import V2AppsAppIdComponentsComponentNameLogs
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_deployments import V2AppsAppIdDeployments
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_deployments_deployment_id import V2AppsAppIdDeploymentsDeploymentId
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_deployments_deployment_id_cancel import V2AppsAppIdDeploymentsDeploymentIdCancel
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_deployments_deployment_id_components_component_name_logs import V2AppsAppIdDeploymentsDeploymentIdComponentsComponentNameLogs
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_deployments_deployment_id_logs import V2AppsAppIdDeploymentsDeploymentIdLogs
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_logs import V2AppsAppIdLogs
from digital_ocean_python_sdk.apis.paths.v2_apps_tiers import V2AppsTiers
from digital_ocean_python_sdk.apis.paths.v2_apps_tiers_slug import V2AppsTiersSlug
from digital_ocean_python_sdk.apis.paths.v2_apps_tiers_instance_sizes import V2AppsTiersInstanceSizes
from digital_ocean_python_sdk.apis.paths.v2_apps_tiers_instance_sizes_slug import V2AppsTiersInstanceSizesSlug
from digital_ocean_python_sdk.apis.paths.v2_apps_regions import V2AppsRegions
from digital_ocean_python_sdk.apis.paths.v2_apps_propose import V2AppsPropose
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_alerts import V2AppsAppIdAlerts
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_alerts_alert_id_destinations import V2AppsAppIdAlertsAlertIdDestinations
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_rollback import V2AppsAppIdRollback
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_rollback_validate import V2AppsAppIdRollbackValidate
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_rollback_commit import V2AppsAppIdRollbackCommit
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_rollback_revert import V2AppsAppIdRollbackRevert
from digital_ocean_python_sdk.apis.paths.v2_apps_app_id_metrics_bandwidth_daily import V2AppsAppIdMetricsBandwidthDaily
from digital_ocean_python_sdk.apis.paths.v2_apps_metrics_bandwidth_daily import V2AppsMetricsBandwidthDaily
from digital_ocean_python_sdk.apis.paths.v2_cdn_endpoints import V2CdnEndpoints
from digital_ocean_python_sdk.apis.paths.v2_cdn_endpoints_cdn_id import V2CdnEndpointsCdnId
from digital_ocean_python_sdk.apis.paths.v2_cdn_endpoints_cdn_id_cache import V2CdnEndpointsCdnIdCache
from digital_ocean_python_sdk.apis.paths.v2_certificates import V2Certificates
from digital_ocean_python_sdk.apis.paths.v2_certificates_certificate_id import V2CertificatesCertificateId
from digital_ocean_python_sdk.apis.paths.v2_customers_my_balance import V2CustomersMyBalance
from digital_ocean_python_sdk.apis.paths.v2_customers_my_billing_history import V2CustomersMyBillingHistory
from digital_ocean_python_sdk.apis.paths.v2_customers_my_invoices import V2CustomersMyInvoices
from digital_ocean_python_sdk.apis.paths.v2_customers_my_invoices_invoice_uuid import V2CustomersMyInvoicesInvoiceUuid
from digital_ocean_python_sdk.apis.paths.v2_customers_my_invoices_invoice_uuid_csv import V2CustomersMyInvoicesInvoiceUuidCsv
from digital_ocean_python_sdk.apis.paths.v2_customers_my_invoices_invoice_uuid_pdf import V2CustomersMyInvoicesInvoiceUuidPdf
from digital_ocean_python_sdk.apis.paths.v2_customers_my_invoices_invoice_uuid_summary import V2CustomersMyInvoicesInvoiceUuidSummary
from digital_ocean_python_sdk.apis.paths.v2_databases_options import V2DatabasesOptions
from digital_ocean_python_sdk.apis.paths.v2_databases import V2Databases
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid import V2DatabasesDatabaseClusterUuid
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_config import V2DatabasesDatabaseClusterUuidConfig
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_ca import V2DatabasesDatabaseClusterUuidCa
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_online_migration import V2DatabasesDatabaseClusterUuidOnlineMigration
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_online_migration_migration_id import V2DatabasesDatabaseClusterUuidOnlineMigrationMigrationId
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_migrate import V2DatabasesDatabaseClusterUuidMigrate
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_resize import V2DatabasesDatabaseClusterUuidResize
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_firewall import V2DatabasesDatabaseClusterUuidFirewall
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_maintenance import V2DatabasesDatabaseClusterUuidMaintenance
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_backups import V2DatabasesDatabaseClusterUuidBackups
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_replicas import V2DatabasesDatabaseClusterUuidReplicas
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_events import V2DatabasesDatabaseClusterUuidEvents
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_replicas_replica_name import V2DatabasesDatabaseClusterUuidReplicasReplicaName
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_replicas_replica_name_promote import V2DatabasesDatabaseClusterUuidReplicasReplicaNamePromote
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_users import V2DatabasesDatabaseClusterUuidUsers
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_users_username import V2DatabasesDatabaseClusterUuidUsersUsername
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_users_username_reset_auth import V2DatabasesDatabaseClusterUuidUsersUsernameResetAuth
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_dbs import V2DatabasesDatabaseClusterUuidDbs
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_dbs_database_name import V2DatabasesDatabaseClusterUuidDbsDatabaseName
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_pools import V2DatabasesDatabaseClusterUuidPools
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_pools_pool_name import V2DatabasesDatabaseClusterUuidPoolsPoolName
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_eviction_policy import V2DatabasesDatabaseClusterUuidEvictionPolicy
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_sql_mode import V2DatabasesDatabaseClusterUuidSqlMode
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_upgrade import V2DatabasesDatabaseClusterUuidUpgrade
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_topics import V2DatabasesDatabaseClusterUuidTopics
from digital_ocean_python_sdk.apis.paths.v2_databases_database_cluster_uuid_topics_topic_name import V2DatabasesDatabaseClusterUuidTopicsTopicName
from digital_ocean_python_sdk.apis.paths.v2_databases_metrics_credentials import V2DatabasesMetricsCredentials
from digital_ocean_python_sdk.apis.paths.v2_domains import V2Domains
from digital_ocean_python_sdk.apis.paths.v2_domains_domain_name import V2DomainsDomainName
from digital_ocean_python_sdk.apis.paths.v2_domains_domain_name_records import V2DomainsDomainNameRecords
from digital_ocean_python_sdk.apis.paths.v2_domains_domain_name_records_domain_record_id import V2DomainsDomainNameRecordsDomainRecordId
from digital_ocean_python_sdk.apis.paths.v2_droplets import V2Droplets
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id import V2DropletsDropletId
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_backups import V2DropletsDropletIdBackups
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_snapshots import V2DropletsDropletIdSnapshots
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_actions import V2DropletsDropletIdActions
from digital_ocean_python_sdk.apis.paths.v2_droplets_actions import V2DropletsActions
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_actions_action_id import V2DropletsDropletIdActionsActionId
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_kernels import V2DropletsDropletIdKernels
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_firewalls import V2DropletsDropletIdFirewalls
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_neighbors import V2DropletsDropletIdNeighbors
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_destroy_with_associated_resources import V2DropletsDropletIdDestroyWithAssociatedResources
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_destroy_with_associated_resources_selective import V2DropletsDropletIdDestroyWithAssociatedResourcesSelective
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_destroy_with_associated_resources_dangerous import V2DropletsDropletIdDestroyWithAssociatedResourcesDangerous
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_destroy_with_associated_resources_status import V2DropletsDropletIdDestroyWithAssociatedResourcesStatus
from digital_ocean_python_sdk.apis.paths.v2_droplets_droplet_id_destroy_with_associated_resources_retry import V2DropletsDropletIdDestroyWithAssociatedResourcesRetry
from digital_ocean_python_sdk.apis.paths.v2_firewalls import V2Firewalls
from digital_ocean_python_sdk.apis.paths.v2_firewalls_firewall_id import V2FirewallsFirewallId
from digital_ocean_python_sdk.apis.paths.v2_firewalls_firewall_id_droplets import V2FirewallsFirewallIdDroplets
from digital_ocean_python_sdk.apis.paths.v2_firewalls_firewall_id_tags import V2FirewallsFirewallIdTags
from digital_ocean_python_sdk.apis.paths.v2_firewalls_firewall_id_rules import V2FirewallsFirewallIdRules
from digital_ocean_python_sdk.apis.paths.v2_floating_ips import V2FloatingIps
from digital_ocean_python_sdk.apis.paths.v2_floating_ips_floating_ip import V2FloatingIpsFloatingIp
from digital_ocean_python_sdk.apis.paths.v2_floating_ips_floating_ip_actions import V2FloatingIpsFloatingIpActions
from digital_ocean_python_sdk.apis.paths.v2_floating_ips_floating_ip_actions_action_id import V2FloatingIpsFloatingIpActionsActionId
from digital_ocean_python_sdk.apis.paths.v2_functions_namespaces import V2FunctionsNamespaces
from digital_ocean_python_sdk.apis.paths.v2_functions_namespaces_namespace_id import V2FunctionsNamespacesNamespaceId
from digital_ocean_python_sdk.apis.paths.v2_functions_namespaces_namespace_id_triggers import V2FunctionsNamespacesNamespaceIdTriggers
from digital_ocean_python_sdk.apis.paths.v2_functions_namespaces_namespace_id_triggers_trigger_name import V2FunctionsNamespacesNamespaceIdTriggersTriggerName
from digital_ocean_python_sdk.apis.paths.v2_images import V2Images
from digital_ocean_python_sdk.apis.paths.v2_images_image_id import V2ImagesImageId
from digital_ocean_python_sdk.apis.paths.v2_images_image_id_actions import V2ImagesImageIdActions
from digital_ocean_python_sdk.apis.paths.v2_images_image_id_actions_action_id import V2ImagesImageIdActionsActionId
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters import V2KubernetesClusters
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id import V2KubernetesClustersClusterId
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_destroy_with_associated_resources import V2KubernetesClustersClusterIdDestroyWithAssociatedResources
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_destroy_with_associated_resources_selective import V2KubernetesClustersClusterIdDestroyWithAssociatedResourcesSelective
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_destroy_with_associated_resources_dangerous import V2KubernetesClustersClusterIdDestroyWithAssociatedResourcesDangerous
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_kubeconfig import V2KubernetesClustersClusterIdKubeconfig
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_credentials import V2KubernetesClustersClusterIdCredentials
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_upgrades import V2KubernetesClustersClusterIdUpgrades
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_upgrade import V2KubernetesClustersClusterIdUpgrade
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_node_pools import V2KubernetesClustersClusterIdNodePools
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_node_pools_node_pool_id import V2KubernetesClustersClusterIdNodePoolsNodePoolId
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_node_pools_node_pool_id_nodes_node_id import V2KubernetesClustersClusterIdNodePoolsNodePoolIdNodesNodeId
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_node_pools_node_pool_id_recycle import V2KubernetesClustersClusterIdNodePoolsNodePoolIdRecycle
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_user import V2KubernetesClustersClusterIdUser
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_options import V2KubernetesOptions
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_clusters_cluster_id_clusterlint import V2KubernetesClustersClusterIdClusterlint
from digital_ocean_python_sdk.apis.paths.v2_kubernetes_registry import V2KubernetesRegistry
from digital_ocean_python_sdk.apis.paths.v2_load_balancers import V2LoadBalancers
from digital_ocean_python_sdk.apis.paths.v2_load_balancers_lb_id import V2LoadBalancersLbId
from digital_ocean_python_sdk.apis.paths.v2_load_balancers_lb_id_droplets import V2LoadBalancersLbIdDroplets
from digital_ocean_python_sdk.apis.paths.v2_load_balancers_lb_id_forwarding_rules import V2LoadBalancersLbIdForwardingRules
from digital_ocean_python_sdk.apis.paths.v2_monitoring_alerts import V2MonitoringAlerts
from digital_ocean_python_sdk.apis.paths.v2_monitoring_alerts_alert_uuid import V2MonitoringAlertsAlertUuid
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_bandwidth import V2MonitoringMetricsDropletBandwidth
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_cpu import V2MonitoringMetricsDropletCpu
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_filesystem_free import V2MonitoringMetricsDropletFilesystemFree
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_filesystem_size import V2MonitoringMetricsDropletFilesystemSize
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_load_1 import V2MonitoringMetricsDropletLoad1
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_load_5 import V2MonitoringMetricsDropletLoad5
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_load_15 import V2MonitoringMetricsDropletLoad15
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_memory_cached import V2MonitoringMetricsDropletMemoryCached
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_memory_free import V2MonitoringMetricsDropletMemoryFree
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_memory_total import V2MonitoringMetricsDropletMemoryTotal
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_droplet_memory_available import V2MonitoringMetricsDropletMemoryAvailable
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_apps_memory_percentage import V2MonitoringMetricsAppsMemoryPercentage
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_apps_cpu_percentage import V2MonitoringMetricsAppsCpuPercentage
from digital_ocean_python_sdk.apis.paths.v2_monitoring_metrics_apps_restart_count import V2MonitoringMetricsAppsRestartCount
from digital_ocean_python_sdk.apis.paths.v2_projects import V2Projects
from digital_ocean_python_sdk.apis.paths.v2_projects_default import V2ProjectsDefault
from digital_ocean_python_sdk.apis.paths.v2_projects_project_id import V2ProjectsProjectId
from digital_ocean_python_sdk.apis.paths.v2_projects_project_id_resources import V2ProjectsProjectIdResources
from digital_ocean_python_sdk.apis.paths.v2_projects_default_resources import V2ProjectsDefaultResources
from digital_ocean_python_sdk.apis.paths.v2_regions import V2Regions
from digital_ocean_python_sdk.apis.paths.v2_registry import V2Registry
from digital_ocean_python_sdk.apis.paths.v2_registry_subscription import V2RegistrySubscription
from digital_ocean_python_sdk.apis.paths.v2_registry_docker_credentials import V2RegistryDockerCredentials
from digital_ocean_python_sdk.apis.paths.v2_registry_validate_name import V2RegistryValidateName
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_repositories import V2RegistryRegistryNameRepositories
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_repositories_v2 import V2RegistryRegistryNameRepositoriesV2
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_repositories_repository_name_tags import V2RegistryRegistryNameRepositoriesRepositoryNameTags
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_repositories_repository_name_tags_repository_tag import V2RegistryRegistryNameRepositoriesRepositoryNameTagsRepositoryTag
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_repositories_repository_name_digests import V2RegistryRegistryNameRepositoriesRepositoryNameDigests
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_repositories_repository_name_digests_manifest_digest import V2RegistryRegistryNameRepositoriesRepositoryNameDigestsManifestDigest
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_garbage_collection import V2RegistryRegistryNameGarbageCollection
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_garbage_collections import V2RegistryRegistryNameGarbageCollections
from digital_ocean_python_sdk.apis.paths.v2_registry_registry_name_garbage_collection_garbage_collection_uuid import V2RegistryRegistryNameGarbageCollectionGarbageCollectionUuid
from digital_ocean_python_sdk.apis.paths.v2_registry_options import V2RegistryOptions
from digital_ocean_python_sdk.apis.paths.v2_reports_droplet_neighbors_ids import V2ReportsDropletNeighborsIds
from digital_ocean_python_sdk.apis.paths.v2_reserved_ips import V2ReservedIps
from digital_ocean_python_sdk.apis.paths.v2_reserved_ips_reserved_ip import V2ReservedIpsReservedIp
from digital_ocean_python_sdk.apis.paths.v2_reserved_ips_reserved_ip_actions import V2ReservedIpsReservedIpActions
from digital_ocean_python_sdk.apis.paths.v2_reserved_ips_reserved_ip_actions_action_id import V2ReservedIpsReservedIpActionsActionId
from digital_ocean_python_sdk.apis.paths.v2_sizes import V2Sizes
from digital_ocean_python_sdk.apis.paths.v2_snapshots import V2Snapshots
from digital_ocean_python_sdk.apis.paths.v2_snapshots_snapshot_id import V2SnapshotsSnapshotId
from digital_ocean_python_sdk.apis.paths.v2_tags import V2Tags
from digital_ocean_python_sdk.apis.paths.v2_tags_tag_id import V2TagsTagId
from digital_ocean_python_sdk.apis.paths.v2_tags_tag_id_resources import V2TagsTagIdResources
from digital_ocean_python_sdk.apis.paths.v2_volumes import V2Volumes
from digital_ocean_python_sdk.apis.paths.v2_volumes_actions import V2VolumesActions
from digital_ocean_python_sdk.apis.paths.v2_volumes_snapshots_snapshot_id import V2VolumesSnapshotsSnapshotId
from digital_ocean_python_sdk.apis.paths.v2_volumes_volume_id import V2VolumesVolumeId
from digital_ocean_python_sdk.apis.paths.v2_volumes_volume_id_actions import V2VolumesVolumeIdActions
from digital_ocean_python_sdk.apis.paths.v2_volumes_volume_id_actions_action_id import V2VolumesVolumeIdActionsActionId
from digital_ocean_python_sdk.apis.paths.v2_volumes_volume_id_snapshots import V2VolumesVolumeIdSnapshots
from digital_ocean_python_sdk.apis.paths.v2_vpcs import V2Vpcs
from digital_ocean_python_sdk.apis.paths.v2_vpcs_vpc_id import V2VpcsVpcId
from digital_ocean_python_sdk.apis.paths.v2_vpcs_vpc_id_members import V2VpcsVpcIdMembers
from digital_ocean_python_sdk.apis.paths.v2_uptime_checks import V2UptimeChecks
from digital_ocean_python_sdk.apis.paths.v2_uptime_checks_check_id import V2UptimeChecksCheckId
from digital_ocean_python_sdk.apis.paths.v2_uptime_checks_check_id_state import V2UptimeChecksCheckIdState
from digital_ocean_python_sdk.apis.paths.v2_uptime_checks_check_id_alerts import V2UptimeChecksCheckIdAlerts
from digital_ocean_python_sdk.apis.paths.v2_uptime_checks_check_id_alerts_alert_id import V2UptimeChecksCheckIdAlertsAlertId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V2_1CLICKS: V21Clicks,
        PathValues.V2_1CLICKS_KUBERNETES: V21ClicksKubernetes,
        PathValues.V2_ACCOUNT: V2Account,
        PathValues.V2_ACCOUNT_KEYS: V2AccountKeys,
        PathValues.V2_ACCOUNT_KEYS_SSH_KEY_IDENTIFIER: V2AccountKeysSshKeyIdentifier,
        PathValues.V2_ACTIONS: V2Actions,
        PathValues.V2_ACTIONS_ACTION_ID: V2ActionsActionId,
        PathValues.V2_APPS: V2Apps,
        PathValues.V2_APPS_ID: V2AppsId,
        PathValues.V2_APPS_APP_ID_COMPONENTS_COMPONENT_NAME_LOGS: V2AppsAppIdComponentsComponentNameLogs,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS: V2AppsAppIdDeployments,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS_DEPLOYMENT_ID: V2AppsAppIdDeploymentsDeploymentId,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS_DEPLOYMENT_ID_CANCEL: V2AppsAppIdDeploymentsDeploymentIdCancel,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS_DEPLOYMENT_ID_COMPONENTS_COMPONENT_NAME_LOGS: V2AppsAppIdDeploymentsDeploymentIdComponentsComponentNameLogs,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS_DEPLOYMENT_ID_LOGS: V2AppsAppIdDeploymentsDeploymentIdLogs,
        PathValues.V2_APPS_APP_ID_LOGS: V2AppsAppIdLogs,
        PathValues.V2_APPS_TIERS: V2AppsTiers,
        PathValues.V2_APPS_TIERS_SLUG: V2AppsTiersSlug,
        PathValues.V2_APPS_TIERS_INSTANCE_SIZES: V2AppsTiersInstanceSizes,
        PathValues.V2_APPS_TIERS_INSTANCE_SIZES_SLUG: V2AppsTiersInstanceSizesSlug,
        PathValues.V2_APPS_REGIONS: V2AppsRegions,
        PathValues.V2_APPS_PROPOSE: V2AppsPropose,
        PathValues.V2_APPS_APP_ID_ALERTS: V2AppsAppIdAlerts,
        PathValues.V2_APPS_APP_ID_ALERTS_ALERT_ID_DESTINATIONS: V2AppsAppIdAlertsAlertIdDestinations,
        PathValues.V2_APPS_APP_ID_ROLLBACK: V2AppsAppIdRollback,
        PathValues.V2_APPS_APP_ID_ROLLBACK_VALIDATE: V2AppsAppIdRollbackValidate,
        PathValues.V2_APPS_APP_ID_ROLLBACK_COMMIT: V2AppsAppIdRollbackCommit,
        PathValues.V2_APPS_APP_ID_ROLLBACK_REVERT: V2AppsAppIdRollbackRevert,
        PathValues.V2_APPS_APP_ID_METRICS_BANDWIDTH_DAILY: V2AppsAppIdMetricsBandwidthDaily,
        PathValues.V2_APPS_METRICS_BANDWIDTH_DAILY: V2AppsMetricsBandwidthDaily,
        PathValues.V2_CDN_ENDPOINTS: V2CdnEndpoints,
        PathValues.V2_CDN_ENDPOINTS_CDN_ID: V2CdnEndpointsCdnId,
        PathValues.V2_CDN_ENDPOINTS_CDN_ID_CACHE: V2CdnEndpointsCdnIdCache,
        PathValues.V2_CERTIFICATES: V2Certificates,
        PathValues.V2_CERTIFICATES_CERTIFICATE_ID: V2CertificatesCertificateId,
        PathValues.V2_CUSTOMERS_MY_BALANCE: V2CustomersMyBalance,
        PathValues.V2_CUSTOMERS_MY_BILLING_HISTORY: V2CustomersMyBillingHistory,
        PathValues.V2_CUSTOMERS_MY_INVOICES: V2CustomersMyInvoices,
        PathValues.V2_CUSTOMERS_MY_INVOICES_INVOICE_UUID: V2CustomersMyInvoicesInvoiceUuid,
        PathValues.V2_CUSTOMERS_MY_INVOICES_INVOICE_UUID_CSV: V2CustomersMyInvoicesInvoiceUuidCsv,
        PathValues.V2_CUSTOMERS_MY_INVOICES_INVOICE_UUID_PDF: V2CustomersMyInvoicesInvoiceUuidPdf,
        PathValues.V2_CUSTOMERS_MY_INVOICES_INVOICE_UUID_SUMMARY: V2CustomersMyInvoicesInvoiceUuidSummary,
        PathValues.V2_DATABASES_OPTIONS: V2DatabasesOptions,
        PathValues.V2_DATABASES: V2Databases,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID: V2DatabasesDatabaseClusterUuid,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_CONFIG: V2DatabasesDatabaseClusterUuidConfig,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_CA: V2DatabasesDatabaseClusterUuidCa,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_ONLINEMIGRATION: V2DatabasesDatabaseClusterUuidOnlineMigration,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_ONLINEMIGRATION_MIGRATION_ID: V2DatabasesDatabaseClusterUuidOnlineMigrationMigrationId,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_MIGRATE: V2DatabasesDatabaseClusterUuidMigrate,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_RESIZE: V2DatabasesDatabaseClusterUuidResize,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_FIREWALL: V2DatabasesDatabaseClusterUuidFirewall,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_MAINTENANCE: V2DatabasesDatabaseClusterUuidMaintenance,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_BACKUPS: V2DatabasesDatabaseClusterUuidBackups,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_REPLICAS: V2DatabasesDatabaseClusterUuidReplicas,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_EVENTS: V2DatabasesDatabaseClusterUuidEvents,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_REPLICAS_REPLICA_NAME: V2DatabasesDatabaseClusterUuidReplicasReplicaName,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_REPLICAS_REPLICA_NAME_PROMOTE: V2DatabasesDatabaseClusterUuidReplicasReplicaNamePromote,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_USERS: V2DatabasesDatabaseClusterUuidUsers,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_USERS_USERNAME: V2DatabasesDatabaseClusterUuidUsersUsername,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_USERS_USERNAME_RESET_AUTH: V2DatabasesDatabaseClusterUuidUsersUsernameResetAuth,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_DBS: V2DatabasesDatabaseClusterUuidDbs,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_DBS_DATABASE_NAME: V2DatabasesDatabaseClusterUuidDbsDatabaseName,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_POOLS: V2DatabasesDatabaseClusterUuidPools,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_POOLS_POOL_NAME: V2DatabasesDatabaseClusterUuidPoolsPoolName,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_EVICTION_POLICY: V2DatabasesDatabaseClusterUuidEvictionPolicy,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_SQL_MODE: V2DatabasesDatabaseClusterUuidSqlMode,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_UPGRADE: V2DatabasesDatabaseClusterUuidUpgrade,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_TOPICS: V2DatabasesDatabaseClusterUuidTopics,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_TOPICS_TOPIC_NAME: V2DatabasesDatabaseClusterUuidTopicsTopicName,
        PathValues.V2_DATABASES_METRICS_CREDENTIALS: V2DatabasesMetricsCredentials,
        PathValues.V2_DOMAINS: V2Domains,
        PathValues.V2_DOMAINS_DOMAIN_NAME: V2DomainsDomainName,
        PathValues.V2_DOMAINS_DOMAIN_NAME_RECORDS: V2DomainsDomainNameRecords,
        PathValues.V2_DOMAINS_DOMAIN_NAME_RECORDS_DOMAIN_RECORD_ID: V2DomainsDomainNameRecordsDomainRecordId,
        PathValues.V2_DROPLETS: V2Droplets,
        PathValues.V2_DROPLETS_DROPLET_ID: V2DropletsDropletId,
        PathValues.V2_DROPLETS_DROPLET_ID_BACKUPS: V2DropletsDropletIdBackups,
        PathValues.V2_DROPLETS_DROPLET_ID_SNAPSHOTS: V2DropletsDropletIdSnapshots,
        PathValues.V2_DROPLETS_DROPLET_ID_ACTIONS: V2DropletsDropletIdActions,
        PathValues.V2_DROPLETS_ACTIONS: V2DropletsActions,
        PathValues.V2_DROPLETS_DROPLET_ID_ACTIONS_ACTION_ID: V2DropletsDropletIdActionsActionId,
        PathValues.V2_DROPLETS_DROPLET_ID_KERNELS: V2DropletsDropletIdKernels,
        PathValues.V2_DROPLETS_DROPLET_ID_FIREWALLS: V2DropletsDropletIdFirewalls,
        PathValues.V2_DROPLETS_DROPLET_ID_NEIGHBORS: V2DropletsDropletIdNeighbors,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES: V2DropletsDropletIdDestroyWithAssociatedResources,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_SELECTIVE: V2DropletsDropletIdDestroyWithAssociatedResourcesSelective,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_DANGEROUS: V2DropletsDropletIdDestroyWithAssociatedResourcesDangerous,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_STATUS: V2DropletsDropletIdDestroyWithAssociatedResourcesStatus,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_RETRY: V2DropletsDropletIdDestroyWithAssociatedResourcesRetry,
        PathValues.V2_FIREWALLS: V2Firewalls,
        PathValues.V2_FIREWALLS_FIREWALL_ID: V2FirewallsFirewallId,
        PathValues.V2_FIREWALLS_FIREWALL_ID_DROPLETS: V2FirewallsFirewallIdDroplets,
        PathValues.V2_FIREWALLS_FIREWALL_ID_TAGS: V2FirewallsFirewallIdTags,
        PathValues.V2_FIREWALLS_FIREWALL_ID_RULES: V2FirewallsFirewallIdRules,
        PathValues.V2_FLOATING_IPS: V2FloatingIps,
        PathValues.V2_FLOATING_IPS_FLOATING_IP: V2FloatingIpsFloatingIp,
        PathValues.V2_FLOATING_IPS_FLOATING_IP_ACTIONS: V2FloatingIpsFloatingIpActions,
        PathValues.V2_FLOATING_IPS_FLOATING_IP_ACTIONS_ACTION_ID: V2FloatingIpsFloatingIpActionsActionId,
        PathValues.V2_FUNCTIONS_NAMESPACES: V2FunctionsNamespaces,
        PathValues.V2_FUNCTIONS_NAMESPACES_NAMESPACE_ID: V2FunctionsNamespacesNamespaceId,
        PathValues.V2_FUNCTIONS_NAMESPACES_NAMESPACE_ID_TRIGGERS: V2FunctionsNamespacesNamespaceIdTriggers,
        PathValues.V2_FUNCTIONS_NAMESPACES_NAMESPACE_ID_TRIGGERS_TRIGGER_NAME: V2FunctionsNamespacesNamespaceIdTriggersTriggerName,
        PathValues.V2_IMAGES: V2Images,
        PathValues.V2_IMAGES_IMAGE_ID: V2ImagesImageId,
        PathValues.V2_IMAGES_IMAGE_ID_ACTIONS: V2ImagesImageIdActions,
        PathValues.V2_IMAGES_IMAGE_ID_ACTIONS_ACTION_ID: V2ImagesImageIdActionsActionId,
        PathValues.V2_KUBERNETES_CLUSTERS: V2KubernetesClusters,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID: V2KubernetesClustersClusterId,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_DESTROY_WITH_ASSOCIATED_RESOURCES: V2KubernetesClustersClusterIdDestroyWithAssociatedResources,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_SELECTIVE: V2KubernetesClustersClusterIdDestroyWithAssociatedResourcesSelective,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_DANGEROUS: V2KubernetesClustersClusterIdDestroyWithAssociatedResourcesDangerous,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_KUBECONFIG: V2KubernetesClustersClusterIdKubeconfig,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_CREDENTIALS: V2KubernetesClustersClusterIdCredentials,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_UPGRADES: V2KubernetesClustersClusterIdUpgrades,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_UPGRADE: V2KubernetesClustersClusterIdUpgrade,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_NODE_POOLS: V2KubernetesClustersClusterIdNodePools,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_NODE_POOLS_NODE_POOL_ID: V2KubernetesClustersClusterIdNodePoolsNodePoolId,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_NODE_POOLS_NODE_POOL_ID_NODES_NODE_ID: V2KubernetesClustersClusterIdNodePoolsNodePoolIdNodesNodeId,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_NODE_POOLS_NODE_POOL_ID_RECYCLE: V2KubernetesClustersClusterIdNodePoolsNodePoolIdRecycle,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_USER: V2KubernetesClustersClusterIdUser,
        PathValues.V2_KUBERNETES_OPTIONS: V2KubernetesOptions,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_CLUSTERLINT: V2KubernetesClustersClusterIdClusterlint,
        PathValues.V2_KUBERNETES_REGISTRY: V2KubernetesRegistry,
        PathValues.V2_LOAD_BALANCERS: V2LoadBalancers,
        PathValues.V2_LOAD_BALANCERS_LB_ID: V2LoadBalancersLbId,
        PathValues.V2_LOAD_BALANCERS_LB_ID_DROPLETS: V2LoadBalancersLbIdDroplets,
        PathValues.V2_LOAD_BALANCERS_LB_ID_FORWARDING_RULES: V2LoadBalancersLbIdForwardingRules,
        PathValues.V2_MONITORING_ALERTS: V2MonitoringAlerts,
        PathValues.V2_MONITORING_ALERTS_ALERT_UUID: V2MonitoringAlertsAlertUuid,
        PathValues.V2_MONITORING_METRICS_DROPLET_BANDWIDTH: V2MonitoringMetricsDropletBandwidth,
        PathValues.V2_MONITORING_METRICS_DROPLET_CPU: V2MonitoringMetricsDropletCpu,
        PathValues.V2_MONITORING_METRICS_DROPLET_FILESYSTEM_FREE: V2MonitoringMetricsDropletFilesystemFree,
        PathValues.V2_MONITORING_METRICS_DROPLET_FILESYSTEM_SIZE: V2MonitoringMetricsDropletFilesystemSize,
        PathValues.V2_MONITORING_METRICS_DROPLET_LOAD_1: V2MonitoringMetricsDropletLoad1,
        PathValues.V2_MONITORING_METRICS_DROPLET_LOAD_5: V2MonitoringMetricsDropletLoad5,
        PathValues.V2_MONITORING_METRICS_DROPLET_LOAD_15: V2MonitoringMetricsDropletLoad15,
        PathValues.V2_MONITORING_METRICS_DROPLET_MEMORY_CACHED: V2MonitoringMetricsDropletMemoryCached,
        PathValues.V2_MONITORING_METRICS_DROPLET_MEMORY_FREE: V2MonitoringMetricsDropletMemoryFree,
        PathValues.V2_MONITORING_METRICS_DROPLET_MEMORY_TOTAL: V2MonitoringMetricsDropletMemoryTotal,
        PathValues.V2_MONITORING_METRICS_DROPLET_MEMORY_AVAILABLE: V2MonitoringMetricsDropletMemoryAvailable,
        PathValues.V2_MONITORING_METRICS_APPS_MEMORY_PERCENTAGE: V2MonitoringMetricsAppsMemoryPercentage,
        PathValues.V2_MONITORING_METRICS_APPS_CPU_PERCENTAGE: V2MonitoringMetricsAppsCpuPercentage,
        PathValues.V2_MONITORING_METRICS_APPS_RESTART_COUNT: V2MonitoringMetricsAppsRestartCount,
        PathValues.V2_PROJECTS: V2Projects,
        PathValues.V2_PROJECTS_DEFAULT: V2ProjectsDefault,
        PathValues.V2_PROJECTS_PROJECT_ID: V2ProjectsProjectId,
        PathValues.V2_PROJECTS_PROJECT_ID_RESOURCES: V2ProjectsProjectIdResources,
        PathValues.V2_PROJECTS_DEFAULT_RESOURCES: V2ProjectsDefaultResources,
        PathValues.V2_REGIONS: V2Regions,
        PathValues.V2_REGISTRY: V2Registry,
        PathValues.V2_REGISTRY_SUBSCRIPTION: V2RegistrySubscription,
        PathValues.V2_REGISTRY_DOCKERCREDENTIALS: V2RegistryDockerCredentials,
        PathValues.V2_REGISTRY_VALIDATENAME: V2RegistryValidateName,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES: V2RegistryRegistryNameRepositories,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_V2: V2RegistryRegistryNameRepositoriesV2,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_REPOSITORY_NAME_TAGS: V2RegistryRegistryNameRepositoriesRepositoryNameTags,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_REPOSITORY_NAME_TAGS_REPOSITORY_TAG: V2RegistryRegistryNameRepositoriesRepositoryNameTagsRepositoryTag,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_REPOSITORY_NAME_DIGESTS: V2RegistryRegistryNameRepositoriesRepositoryNameDigests,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_REPOSITORY_NAME_DIGESTS_MANIFEST_DIGEST: V2RegistryRegistryNameRepositoriesRepositoryNameDigestsManifestDigest,
        PathValues.V2_REGISTRY_REGISTRY_NAME_GARBAGECOLLECTION: V2RegistryRegistryNameGarbageCollection,
        PathValues.V2_REGISTRY_REGISTRY_NAME_GARBAGECOLLECTIONS: V2RegistryRegistryNameGarbageCollections,
        PathValues.V2_REGISTRY_REGISTRY_NAME_GARBAGECOLLECTION_GARBAGE_COLLECTION_UUID: V2RegistryRegistryNameGarbageCollectionGarbageCollectionUuid,
        PathValues.V2_REGISTRY_OPTIONS: V2RegistryOptions,
        PathValues.V2_REPORTS_DROPLET_NEIGHBORS_IDS: V2ReportsDropletNeighborsIds,
        PathValues.V2_RESERVED_IPS: V2ReservedIps,
        PathValues.V2_RESERVED_IPS_RESERVED_IP: V2ReservedIpsReservedIp,
        PathValues.V2_RESERVED_IPS_RESERVED_IP_ACTIONS: V2ReservedIpsReservedIpActions,
        PathValues.V2_RESERVED_IPS_RESERVED_IP_ACTIONS_ACTION_ID: V2ReservedIpsReservedIpActionsActionId,
        PathValues.V2_SIZES: V2Sizes,
        PathValues.V2_SNAPSHOTS: V2Snapshots,
        PathValues.V2_SNAPSHOTS_SNAPSHOT_ID: V2SnapshotsSnapshotId,
        PathValues.V2_TAGS: V2Tags,
        PathValues.V2_TAGS_TAG_ID: V2TagsTagId,
        PathValues.V2_TAGS_TAG_ID_RESOURCES: V2TagsTagIdResources,
        PathValues.V2_VOLUMES: V2Volumes,
        PathValues.V2_VOLUMES_ACTIONS: V2VolumesActions,
        PathValues.V2_VOLUMES_SNAPSHOTS_SNAPSHOT_ID: V2VolumesSnapshotsSnapshotId,
        PathValues.V2_VOLUMES_VOLUME_ID: V2VolumesVolumeId,
        PathValues.V2_VOLUMES_VOLUME_ID_ACTIONS: V2VolumesVolumeIdActions,
        PathValues.V2_VOLUMES_VOLUME_ID_ACTIONS_ACTION_ID: V2VolumesVolumeIdActionsActionId,
        PathValues.V2_VOLUMES_VOLUME_ID_SNAPSHOTS: V2VolumesVolumeIdSnapshots,
        PathValues.V2_VPCS: V2Vpcs,
        PathValues.V2_VPCS_VPC_ID: V2VpcsVpcId,
        PathValues.V2_VPCS_VPC_ID_MEMBERS: V2VpcsVpcIdMembers,
        PathValues.V2_UPTIME_CHECKS: V2UptimeChecks,
        PathValues.V2_UPTIME_CHECKS_CHECK_ID: V2UptimeChecksCheckId,
        PathValues.V2_UPTIME_CHECKS_CHECK_ID_STATE: V2UptimeChecksCheckIdState,
        PathValues.V2_UPTIME_CHECKS_CHECK_ID_ALERTS: V2UptimeChecksCheckIdAlerts,
        PathValues.V2_UPTIME_CHECKS_CHECK_ID_ALERTS_ALERT_ID: V2UptimeChecksCheckIdAlertsAlertId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V2_1CLICKS: V21Clicks,
        PathValues.V2_1CLICKS_KUBERNETES: V21ClicksKubernetes,
        PathValues.V2_ACCOUNT: V2Account,
        PathValues.V2_ACCOUNT_KEYS: V2AccountKeys,
        PathValues.V2_ACCOUNT_KEYS_SSH_KEY_IDENTIFIER: V2AccountKeysSshKeyIdentifier,
        PathValues.V2_ACTIONS: V2Actions,
        PathValues.V2_ACTIONS_ACTION_ID: V2ActionsActionId,
        PathValues.V2_APPS: V2Apps,
        PathValues.V2_APPS_ID: V2AppsId,
        PathValues.V2_APPS_APP_ID_COMPONENTS_COMPONENT_NAME_LOGS: V2AppsAppIdComponentsComponentNameLogs,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS: V2AppsAppIdDeployments,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS_DEPLOYMENT_ID: V2AppsAppIdDeploymentsDeploymentId,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS_DEPLOYMENT_ID_CANCEL: V2AppsAppIdDeploymentsDeploymentIdCancel,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS_DEPLOYMENT_ID_COMPONENTS_COMPONENT_NAME_LOGS: V2AppsAppIdDeploymentsDeploymentIdComponentsComponentNameLogs,
        PathValues.V2_APPS_APP_ID_DEPLOYMENTS_DEPLOYMENT_ID_LOGS: V2AppsAppIdDeploymentsDeploymentIdLogs,
        PathValues.V2_APPS_APP_ID_LOGS: V2AppsAppIdLogs,
        PathValues.V2_APPS_TIERS: V2AppsTiers,
        PathValues.V2_APPS_TIERS_SLUG: V2AppsTiersSlug,
        PathValues.V2_APPS_TIERS_INSTANCE_SIZES: V2AppsTiersInstanceSizes,
        PathValues.V2_APPS_TIERS_INSTANCE_SIZES_SLUG: V2AppsTiersInstanceSizesSlug,
        PathValues.V2_APPS_REGIONS: V2AppsRegions,
        PathValues.V2_APPS_PROPOSE: V2AppsPropose,
        PathValues.V2_APPS_APP_ID_ALERTS: V2AppsAppIdAlerts,
        PathValues.V2_APPS_APP_ID_ALERTS_ALERT_ID_DESTINATIONS: V2AppsAppIdAlertsAlertIdDestinations,
        PathValues.V2_APPS_APP_ID_ROLLBACK: V2AppsAppIdRollback,
        PathValues.V2_APPS_APP_ID_ROLLBACK_VALIDATE: V2AppsAppIdRollbackValidate,
        PathValues.V2_APPS_APP_ID_ROLLBACK_COMMIT: V2AppsAppIdRollbackCommit,
        PathValues.V2_APPS_APP_ID_ROLLBACK_REVERT: V2AppsAppIdRollbackRevert,
        PathValues.V2_APPS_APP_ID_METRICS_BANDWIDTH_DAILY: V2AppsAppIdMetricsBandwidthDaily,
        PathValues.V2_APPS_METRICS_BANDWIDTH_DAILY: V2AppsMetricsBandwidthDaily,
        PathValues.V2_CDN_ENDPOINTS: V2CdnEndpoints,
        PathValues.V2_CDN_ENDPOINTS_CDN_ID: V2CdnEndpointsCdnId,
        PathValues.V2_CDN_ENDPOINTS_CDN_ID_CACHE: V2CdnEndpointsCdnIdCache,
        PathValues.V2_CERTIFICATES: V2Certificates,
        PathValues.V2_CERTIFICATES_CERTIFICATE_ID: V2CertificatesCertificateId,
        PathValues.V2_CUSTOMERS_MY_BALANCE: V2CustomersMyBalance,
        PathValues.V2_CUSTOMERS_MY_BILLING_HISTORY: V2CustomersMyBillingHistory,
        PathValues.V2_CUSTOMERS_MY_INVOICES: V2CustomersMyInvoices,
        PathValues.V2_CUSTOMERS_MY_INVOICES_INVOICE_UUID: V2CustomersMyInvoicesInvoiceUuid,
        PathValues.V2_CUSTOMERS_MY_INVOICES_INVOICE_UUID_CSV: V2CustomersMyInvoicesInvoiceUuidCsv,
        PathValues.V2_CUSTOMERS_MY_INVOICES_INVOICE_UUID_PDF: V2CustomersMyInvoicesInvoiceUuidPdf,
        PathValues.V2_CUSTOMERS_MY_INVOICES_INVOICE_UUID_SUMMARY: V2CustomersMyInvoicesInvoiceUuidSummary,
        PathValues.V2_DATABASES_OPTIONS: V2DatabasesOptions,
        PathValues.V2_DATABASES: V2Databases,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID: V2DatabasesDatabaseClusterUuid,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_CONFIG: V2DatabasesDatabaseClusterUuidConfig,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_CA: V2DatabasesDatabaseClusterUuidCa,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_ONLINEMIGRATION: V2DatabasesDatabaseClusterUuidOnlineMigration,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_ONLINEMIGRATION_MIGRATION_ID: V2DatabasesDatabaseClusterUuidOnlineMigrationMigrationId,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_MIGRATE: V2DatabasesDatabaseClusterUuidMigrate,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_RESIZE: V2DatabasesDatabaseClusterUuidResize,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_FIREWALL: V2DatabasesDatabaseClusterUuidFirewall,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_MAINTENANCE: V2DatabasesDatabaseClusterUuidMaintenance,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_BACKUPS: V2DatabasesDatabaseClusterUuidBackups,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_REPLICAS: V2DatabasesDatabaseClusterUuidReplicas,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_EVENTS: V2DatabasesDatabaseClusterUuidEvents,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_REPLICAS_REPLICA_NAME: V2DatabasesDatabaseClusterUuidReplicasReplicaName,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_REPLICAS_REPLICA_NAME_PROMOTE: V2DatabasesDatabaseClusterUuidReplicasReplicaNamePromote,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_USERS: V2DatabasesDatabaseClusterUuidUsers,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_USERS_USERNAME: V2DatabasesDatabaseClusterUuidUsersUsername,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_USERS_USERNAME_RESET_AUTH: V2DatabasesDatabaseClusterUuidUsersUsernameResetAuth,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_DBS: V2DatabasesDatabaseClusterUuidDbs,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_DBS_DATABASE_NAME: V2DatabasesDatabaseClusterUuidDbsDatabaseName,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_POOLS: V2DatabasesDatabaseClusterUuidPools,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_POOLS_POOL_NAME: V2DatabasesDatabaseClusterUuidPoolsPoolName,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_EVICTION_POLICY: V2DatabasesDatabaseClusterUuidEvictionPolicy,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_SQL_MODE: V2DatabasesDatabaseClusterUuidSqlMode,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_UPGRADE: V2DatabasesDatabaseClusterUuidUpgrade,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_TOPICS: V2DatabasesDatabaseClusterUuidTopics,
        PathValues.V2_DATABASES_DATABASE_CLUSTER_UUID_TOPICS_TOPIC_NAME: V2DatabasesDatabaseClusterUuidTopicsTopicName,
        PathValues.V2_DATABASES_METRICS_CREDENTIALS: V2DatabasesMetricsCredentials,
        PathValues.V2_DOMAINS: V2Domains,
        PathValues.V2_DOMAINS_DOMAIN_NAME: V2DomainsDomainName,
        PathValues.V2_DOMAINS_DOMAIN_NAME_RECORDS: V2DomainsDomainNameRecords,
        PathValues.V2_DOMAINS_DOMAIN_NAME_RECORDS_DOMAIN_RECORD_ID: V2DomainsDomainNameRecordsDomainRecordId,
        PathValues.V2_DROPLETS: V2Droplets,
        PathValues.V2_DROPLETS_DROPLET_ID: V2DropletsDropletId,
        PathValues.V2_DROPLETS_DROPLET_ID_BACKUPS: V2DropletsDropletIdBackups,
        PathValues.V2_DROPLETS_DROPLET_ID_SNAPSHOTS: V2DropletsDropletIdSnapshots,
        PathValues.V2_DROPLETS_DROPLET_ID_ACTIONS: V2DropletsDropletIdActions,
        PathValues.V2_DROPLETS_ACTIONS: V2DropletsActions,
        PathValues.V2_DROPLETS_DROPLET_ID_ACTIONS_ACTION_ID: V2DropletsDropletIdActionsActionId,
        PathValues.V2_DROPLETS_DROPLET_ID_KERNELS: V2DropletsDropletIdKernels,
        PathValues.V2_DROPLETS_DROPLET_ID_FIREWALLS: V2DropletsDropletIdFirewalls,
        PathValues.V2_DROPLETS_DROPLET_ID_NEIGHBORS: V2DropletsDropletIdNeighbors,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES: V2DropletsDropletIdDestroyWithAssociatedResources,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_SELECTIVE: V2DropletsDropletIdDestroyWithAssociatedResourcesSelective,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_DANGEROUS: V2DropletsDropletIdDestroyWithAssociatedResourcesDangerous,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_STATUS: V2DropletsDropletIdDestroyWithAssociatedResourcesStatus,
        PathValues.V2_DROPLETS_DROPLET_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_RETRY: V2DropletsDropletIdDestroyWithAssociatedResourcesRetry,
        PathValues.V2_FIREWALLS: V2Firewalls,
        PathValues.V2_FIREWALLS_FIREWALL_ID: V2FirewallsFirewallId,
        PathValues.V2_FIREWALLS_FIREWALL_ID_DROPLETS: V2FirewallsFirewallIdDroplets,
        PathValues.V2_FIREWALLS_FIREWALL_ID_TAGS: V2FirewallsFirewallIdTags,
        PathValues.V2_FIREWALLS_FIREWALL_ID_RULES: V2FirewallsFirewallIdRules,
        PathValues.V2_FLOATING_IPS: V2FloatingIps,
        PathValues.V2_FLOATING_IPS_FLOATING_IP: V2FloatingIpsFloatingIp,
        PathValues.V2_FLOATING_IPS_FLOATING_IP_ACTIONS: V2FloatingIpsFloatingIpActions,
        PathValues.V2_FLOATING_IPS_FLOATING_IP_ACTIONS_ACTION_ID: V2FloatingIpsFloatingIpActionsActionId,
        PathValues.V2_FUNCTIONS_NAMESPACES: V2FunctionsNamespaces,
        PathValues.V2_FUNCTIONS_NAMESPACES_NAMESPACE_ID: V2FunctionsNamespacesNamespaceId,
        PathValues.V2_FUNCTIONS_NAMESPACES_NAMESPACE_ID_TRIGGERS: V2FunctionsNamespacesNamespaceIdTriggers,
        PathValues.V2_FUNCTIONS_NAMESPACES_NAMESPACE_ID_TRIGGERS_TRIGGER_NAME: V2FunctionsNamespacesNamespaceIdTriggersTriggerName,
        PathValues.V2_IMAGES: V2Images,
        PathValues.V2_IMAGES_IMAGE_ID: V2ImagesImageId,
        PathValues.V2_IMAGES_IMAGE_ID_ACTIONS: V2ImagesImageIdActions,
        PathValues.V2_IMAGES_IMAGE_ID_ACTIONS_ACTION_ID: V2ImagesImageIdActionsActionId,
        PathValues.V2_KUBERNETES_CLUSTERS: V2KubernetesClusters,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID: V2KubernetesClustersClusterId,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_DESTROY_WITH_ASSOCIATED_RESOURCES: V2KubernetesClustersClusterIdDestroyWithAssociatedResources,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_SELECTIVE: V2KubernetesClustersClusterIdDestroyWithAssociatedResourcesSelective,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_DESTROY_WITH_ASSOCIATED_RESOURCES_DANGEROUS: V2KubernetesClustersClusterIdDestroyWithAssociatedResourcesDangerous,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_KUBECONFIG: V2KubernetesClustersClusterIdKubeconfig,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_CREDENTIALS: V2KubernetesClustersClusterIdCredentials,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_UPGRADES: V2KubernetesClustersClusterIdUpgrades,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_UPGRADE: V2KubernetesClustersClusterIdUpgrade,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_NODE_POOLS: V2KubernetesClustersClusterIdNodePools,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_NODE_POOLS_NODE_POOL_ID: V2KubernetesClustersClusterIdNodePoolsNodePoolId,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_NODE_POOLS_NODE_POOL_ID_NODES_NODE_ID: V2KubernetesClustersClusterIdNodePoolsNodePoolIdNodesNodeId,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_NODE_POOLS_NODE_POOL_ID_RECYCLE: V2KubernetesClustersClusterIdNodePoolsNodePoolIdRecycle,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_USER: V2KubernetesClustersClusterIdUser,
        PathValues.V2_KUBERNETES_OPTIONS: V2KubernetesOptions,
        PathValues.V2_KUBERNETES_CLUSTERS_CLUSTER_ID_CLUSTERLINT: V2KubernetesClustersClusterIdClusterlint,
        PathValues.V2_KUBERNETES_REGISTRY: V2KubernetesRegistry,
        PathValues.V2_LOAD_BALANCERS: V2LoadBalancers,
        PathValues.V2_LOAD_BALANCERS_LB_ID: V2LoadBalancersLbId,
        PathValues.V2_LOAD_BALANCERS_LB_ID_DROPLETS: V2LoadBalancersLbIdDroplets,
        PathValues.V2_LOAD_BALANCERS_LB_ID_FORWARDING_RULES: V2LoadBalancersLbIdForwardingRules,
        PathValues.V2_MONITORING_ALERTS: V2MonitoringAlerts,
        PathValues.V2_MONITORING_ALERTS_ALERT_UUID: V2MonitoringAlertsAlertUuid,
        PathValues.V2_MONITORING_METRICS_DROPLET_BANDWIDTH: V2MonitoringMetricsDropletBandwidth,
        PathValues.V2_MONITORING_METRICS_DROPLET_CPU: V2MonitoringMetricsDropletCpu,
        PathValues.V2_MONITORING_METRICS_DROPLET_FILESYSTEM_FREE: V2MonitoringMetricsDropletFilesystemFree,
        PathValues.V2_MONITORING_METRICS_DROPLET_FILESYSTEM_SIZE: V2MonitoringMetricsDropletFilesystemSize,
        PathValues.V2_MONITORING_METRICS_DROPLET_LOAD_1: V2MonitoringMetricsDropletLoad1,
        PathValues.V2_MONITORING_METRICS_DROPLET_LOAD_5: V2MonitoringMetricsDropletLoad5,
        PathValues.V2_MONITORING_METRICS_DROPLET_LOAD_15: V2MonitoringMetricsDropletLoad15,
        PathValues.V2_MONITORING_METRICS_DROPLET_MEMORY_CACHED: V2MonitoringMetricsDropletMemoryCached,
        PathValues.V2_MONITORING_METRICS_DROPLET_MEMORY_FREE: V2MonitoringMetricsDropletMemoryFree,
        PathValues.V2_MONITORING_METRICS_DROPLET_MEMORY_TOTAL: V2MonitoringMetricsDropletMemoryTotal,
        PathValues.V2_MONITORING_METRICS_DROPLET_MEMORY_AVAILABLE: V2MonitoringMetricsDropletMemoryAvailable,
        PathValues.V2_MONITORING_METRICS_APPS_MEMORY_PERCENTAGE: V2MonitoringMetricsAppsMemoryPercentage,
        PathValues.V2_MONITORING_METRICS_APPS_CPU_PERCENTAGE: V2MonitoringMetricsAppsCpuPercentage,
        PathValues.V2_MONITORING_METRICS_APPS_RESTART_COUNT: V2MonitoringMetricsAppsRestartCount,
        PathValues.V2_PROJECTS: V2Projects,
        PathValues.V2_PROJECTS_DEFAULT: V2ProjectsDefault,
        PathValues.V2_PROJECTS_PROJECT_ID: V2ProjectsProjectId,
        PathValues.V2_PROJECTS_PROJECT_ID_RESOURCES: V2ProjectsProjectIdResources,
        PathValues.V2_PROJECTS_DEFAULT_RESOURCES: V2ProjectsDefaultResources,
        PathValues.V2_REGIONS: V2Regions,
        PathValues.V2_REGISTRY: V2Registry,
        PathValues.V2_REGISTRY_SUBSCRIPTION: V2RegistrySubscription,
        PathValues.V2_REGISTRY_DOCKERCREDENTIALS: V2RegistryDockerCredentials,
        PathValues.V2_REGISTRY_VALIDATENAME: V2RegistryValidateName,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES: V2RegistryRegistryNameRepositories,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_V2: V2RegistryRegistryNameRepositoriesV2,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_REPOSITORY_NAME_TAGS: V2RegistryRegistryNameRepositoriesRepositoryNameTags,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_REPOSITORY_NAME_TAGS_REPOSITORY_TAG: V2RegistryRegistryNameRepositoriesRepositoryNameTagsRepositoryTag,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_REPOSITORY_NAME_DIGESTS: V2RegistryRegistryNameRepositoriesRepositoryNameDigests,
        PathValues.V2_REGISTRY_REGISTRY_NAME_REPOSITORIES_REPOSITORY_NAME_DIGESTS_MANIFEST_DIGEST: V2RegistryRegistryNameRepositoriesRepositoryNameDigestsManifestDigest,
        PathValues.V2_REGISTRY_REGISTRY_NAME_GARBAGECOLLECTION: V2RegistryRegistryNameGarbageCollection,
        PathValues.V2_REGISTRY_REGISTRY_NAME_GARBAGECOLLECTIONS: V2RegistryRegistryNameGarbageCollections,
        PathValues.V2_REGISTRY_REGISTRY_NAME_GARBAGECOLLECTION_GARBAGE_COLLECTION_UUID: V2RegistryRegistryNameGarbageCollectionGarbageCollectionUuid,
        PathValues.V2_REGISTRY_OPTIONS: V2RegistryOptions,
        PathValues.V2_REPORTS_DROPLET_NEIGHBORS_IDS: V2ReportsDropletNeighborsIds,
        PathValues.V2_RESERVED_IPS: V2ReservedIps,
        PathValues.V2_RESERVED_IPS_RESERVED_IP: V2ReservedIpsReservedIp,
        PathValues.V2_RESERVED_IPS_RESERVED_IP_ACTIONS: V2ReservedIpsReservedIpActions,
        PathValues.V2_RESERVED_IPS_RESERVED_IP_ACTIONS_ACTION_ID: V2ReservedIpsReservedIpActionsActionId,
        PathValues.V2_SIZES: V2Sizes,
        PathValues.V2_SNAPSHOTS: V2Snapshots,
        PathValues.V2_SNAPSHOTS_SNAPSHOT_ID: V2SnapshotsSnapshotId,
        PathValues.V2_TAGS: V2Tags,
        PathValues.V2_TAGS_TAG_ID: V2TagsTagId,
        PathValues.V2_TAGS_TAG_ID_RESOURCES: V2TagsTagIdResources,
        PathValues.V2_VOLUMES: V2Volumes,
        PathValues.V2_VOLUMES_ACTIONS: V2VolumesActions,
        PathValues.V2_VOLUMES_SNAPSHOTS_SNAPSHOT_ID: V2VolumesSnapshotsSnapshotId,
        PathValues.V2_VOLUMES_VOLUME_ID: V2VolumesVolumeId,
        PathValues.V2_VOLUMES_VOLUME_ID_ACTIONS: V2VolumesVolumeIdActions,
        PathValues.V2_VOLUMES_VOLUME_ID_ACTIONS_ACTION_ID: V2VolumesVolumeIdActionsActionId,
        PathValues.V2_VOLUMES_VOLUME_ID_SNAPSHOTS: V2VolumesVolumeIdSnapshots,
        PathValues.V2_VPCS: V2Vpcs,
        PathValues.V2_VPCS_VPC_ID: V2VpcsVpcId,
        PathValues.V2_VPCS_VPC_ID_MEMBERS: V2VpcsVpcIdMembers,
        PathValues.V2_UPTIME_CHECKS: V2UptimeChecks,
        PathValues.V2_UPTIME_CHECKS_CHECK_ID: V2UptimeChecksCheckId,
        PathValues.V2_UPTIME_CHECKS_CHECK_ID_STATE: V2UptimeChecksCheckIdState,
        PathValues.V2_UPTIME_CHECKS_CHECK_ID_ALERTS: V2UptimeChecksCheckIdAlerts,
        PathValues.V2_UPTIME_CHECKS_CHECK_ID_ALERTS_ALERT_ID: V2UptimeChecksCheckIdAlertsAlertId,
    }
)
