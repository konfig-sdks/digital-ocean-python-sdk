import typing_extensions

from digital_ocean_python_sdk.apis.tags import TagValues
from digital_ocean_python_sdk.apis.tags.databases_api import DatabasesApi
from digital_ocean_python_sdk.apis.tags.apps_api import AppsApi
from digital_ocean_python_sdk.apis.tags.kubernetes_api import KubernetesApi
from digital_ocean_python_sdk.apis.tags.monitoring_api import MonitoringApi
from digital_ocean_python_sdk.apis.tags.container_registry_api import ContainerRegistryApi
from digital_ocean_python_sdk.apis.tags.droplets_api import DropletsApi
from digital_ocean_python_sdk.apis.tags.firewalls_api import FirewallsApi
from digital_ocean_python_sdk.apis.tags.uptime_api import UptimeApi
from digital_ocean_python_sdk.apis.tags.block_storage_api import BlockStorageApi
from digital_ocean_python_sdk.apis.tags.functions_api import FunctionsApi
from digital_ocean_python_sdk.apis.tags.load_balancers_api import LoadBalancersApi
from digital_ocean_python_sdk.apis.tags.projects_api import ProjectsApi
from digital_ocean_python_sdk.apis.tags.billing_api import BillingApi
from digital_ocean_python_sdk.apis.tags.vpcs_api import VPCsApi
from digital_ocean_python_sdk.apis.tags.cdn_endpoints_api import CDNEndpointsApi
from digital_ocean_python_sdk.apis.tags.domain_records_api import DomainRecordsApi
from digital_ocean_python_sdk.apis.tags.tags_api import TagsApi
from digital_ocean_python_sdk.apis.tags.images_api import ImagesApi
from digital_ocean_python_sdk.apis.tags.ssh_keys_api import SSHKeysApi
from digital_ocean_python_sdk.apis.tags.block_storage_actions_api import BlockStorageActionsApi
from digital_ocean_python_sdk.apis.tags.certificates_api import CertificatesApi
from digital_ocean_python_sdk.apis.tags.domains_api import DomainsApi
from digital_ocean_python_sdk.apis.tags.droplet_actions_api import DropletActionsApi
from digital_ocean_python_sdk.apis.tags.floating_ips_api import FloatingIPsApi
from digital_ocean_python_sdk.apis.tags.project_resources_api import ProjectResourcesApi
from digital_ocean_python_sdk.apis.tags.reserved_ips_api import ReservedIPsApi
from digital_ocean_python_sdk.apis.tags.floating_ip_actions_api import FloatingIPActionsApi
from digital_ocean_python_sdk.apis.tags.image_actions_api import ImageActionsApi
from digital_ocean_python_sdk.apis.tags.reserved_ip_actions_api import ReservedIPActionsApi
from digital_ocean_python_sdk.apis.tags.snapshots_api import SnapshotsApi
from digital_ocean_python_sdk.apis.tags.model1_click_applications_api import Model1ClickApplicationsApi
from digital_ocean_python_sdk.apis.tags.actions_api import ActionsApi
from digital_ocean_python_sdk.apis.tags.account_api import AccountApi
from digital_ocean_python_sdk.apis.tags.regions_api import RegionsApi
from digital_ocean_python_sdk.apis.tags.sizes_api import SizesApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.DATABASES: DatabasesApi,
        TagValues.APPS: AppsApi,
        TagValues.KUBERNETES: KubernetesApi,
        TagValues.MONITORING: MonitoringApi,
        TagValues.CONTAINER_REGISTRY: ContainerRegistryApi,
        TagValues.DROPLETS: DropletsApi,
        TagValues.FIREWALLS: FirewallsApi,
        TagValues.UPTIME: UptimeApi,
        TagValues.BLOCK_STORAGE: BlockStorageApi,
        TagValues.FUNCTIONS: FunctionsApi,
        TagValues.LOAD_BALANCERS: LoadBalancersApi,
        TagValues.PROJECTS: ProjectsApi,
        TagValues.BILLING: BillingApi,
        TagValues.VPCS: VPCsApi,
        TagValues.CDN_ENDPOINTS: CDNEndpointsApi,
        TagValues.DOMAIN_RECORDS: DomainRecordsApi,
        TagValues.TAGS: TagsApi,
        TagValues.IMAGES: ImagesApi,
        TagValues.SSH_KEYS: SSHKeysApi,
        TagValues.BLOCK_STORAGE_ACTIONS: BlockStorageActionsApi,
        TagValues.CERTIFICATES: CertificatesApi,
        TagValues.DOMAINS: DomainsApi,
        TagValues.DROPLET_ACTIONS: DropletActionsApi,
        TagValues.FLOATING_IPS: FloatingIPsApi,
        TagValues.PROJECT_RESOURCES: ProjectResourcesApi,
        TagValues.RESERVED_IPS: ReservedIPsApi,
        TagValues.FLOATING_IP_ACTIONS: FloatingIPActionsApi,
        TagValues.IMAGE_ACTIONS: ImageActionsApi,
        TagValues.RESERVED_IP_ACTIONS: ReservedIPActionsApi,
        TagValues.SNAPSHOTS: SnapshotsApi,
        TagValues._1CLICK_APPLICATIONS: Model1ClickApplicationsApi,
        TagValues.ACTIONS: ActionsApi,
        TagValues.ACCOUNT: AccountApi,
        TagValues.REGIONS: RegionsApi,
        TagValues.SIZES: SizesApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.DATABASES: DatabasesApi,
        TagValues.APPS: AppsApi,
        TagValues.KUBERNETES: KubernetesApi,
        TagValues.MONITORING: MonitoringApi,
        TagValues.CONTAINER_REGISTRY: ContainerRegistryApi,
        TagValues.DROPLETS: DropletsApi,
        TagValues.FIREWALLS: FirewallsApi,
        TagValues.UPTIME: UptimeApi,
        TagValues.BLOCK_STORAGE: BlockStorageApi,
        TagValues.FUNCTIONS: FunctionsApi,
        TagValues.LOAD_BALANCERS: LoadBalancersApi,
        TagValues.PROJECTS: ProjectsApi,
        TagValues.BILLING: BillingApi,
        TagValues.VPCS: VPCsApi,
        TagValues.CDN_ENDPOINTS: CDNEndpointsApi,
        TagValues.DOMAIN_RECORDS: DomainRecordsApi,
        TagValues.TAGS: TagsApi,
        TagValues.IMAGES: ImagesApi,
        TagValues.SSH_KEYS: SSHKeysApi,
        TagValues.BLOCK_STORAGE_ACTIONS: BlockStorageActionsApi,
        TagValues.CERTIFICATES: CertificatesApi,
        TagValues.DOMAINS: DomainsApi,
        TagValues.DROPLET_ACTIONS: DropletActionsApi,
        TagValues.FLOATING_IPS: FloatingIPsApi,
        TagValues.PROJECT_RESOURCES: ProjectResourcesApi,
        TagValues.RESERVED_IPS: ReservedIPsApi,
        TagValues.FLOATING_IP_ACTIONS: FloatingIPActionsApi,
        TagValues.IMAGE_ACTIONS: ImageActionsApi,
        TagValues.RESERVED_IP_ACTIONS: ReservedIPActionsApi,
        TagValues.SNAPSHOTS: SnapshotsApi,
        TagValues._1CLICK_APPLICATIONS: Model1ClickApplicationsApi,
        TagValues.ACTIONS: ActionsApi,
        TagValues.ACCOUNT: AccountApi,
        TagValues.REGIONS: RegionsApi,
        TagValues.SIZES: SizesApi,
    }
)
