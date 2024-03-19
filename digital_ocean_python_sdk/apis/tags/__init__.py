# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from digital_ocean_python_sdk.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    DATABASES = "Databases"
    APPS = "Apps"
    KUBERNETES = "Kubernetes"
    MONITORING = "Monitoring"
    CONTAINER_REGISTRY = "Container Registry"
    DROPLETS = "Droplets"
    FIREWALLS = "Firewalls"
    UPTIME = "Uptime"
    BLOCK_STORAGE = "Block Storage"
    FUNCTIONS = "Functions"
    LOAD_BALANCERS = "Load Balancers"
    PROJECTS = "Projects"
    BILLING = "Billing"
    VPCS = "VPCs"
    CDN_ENDPOINTS = "CDN Endpoints"
    DOMAIN_RECORDS = "Domain Records"
    TAGS = "Tags"
    IMAGES = "Images"
    SSH_KEYS = "SSH Keys"
    BLOCK_STORAGE_ACTIONS = "Block Storage Actions"
    CERTIFICATES = "Certificates"
    DOMAINS = "Domains"
    DROPLET_ACTIONS = "Droplet Actions"
    FLOATING_IPS = "Floating IPs"
    PROJECT_RESOURCES = "Project Resources"
    RESERVED_IPS = "Reserved IPs"
    FLOATING_IP_ACTIONS = "Floating IP Actions"
    IMAGE_ACTIONS = "Image Actions"
    RESERVED_IP_ACTIONS = "Reserved IP Actions"
    SNAPSHOTS = "Snapshots"
    _1CLICK_APPLICATIONS = "1-Click Applications"
    ACTIONS = "Actions"
    ACCOUNT = "Account"
    REGIONS = "Regions"
    SIZES = "Sizes"
