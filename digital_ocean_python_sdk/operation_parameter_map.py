operation_parameter_map = {
    '/v2/1-clicks/kubernetes-POST': {
        'parameters': [
            {
                'name': 'addon_slugs'
            },
            {
                'name': 'cluster_uuid'
            },
        ]
    },
    '/v2/1-clicks-GET': {
        'parameters': [
            {
                'name': 'type'
            },
        ]
    },
    '/v2/account-GET': {
        'parameters': [
        ]
    },
    '/v2/actions/{action_id}-GET': {
        'parameters': [
            {
                'name': 'action_id'
            },
        ]
    },
    '/v2/actions-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/apps/{app_id}/deployments/{deployment_id}/cancel-POST': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'deployment_id'
            },
        ]
    },
    '/v2/apps/{app_id}/rollback/commit-POST': {
        'parameters': [
            {
                'name': 'app_id'
            },
        ]
    },
    '/v2/apps-POST': {
        'parameters': [
            {
                'name': 'spec'
            },
            {
                'name': 'project_id'
            },
        ]
    },
    '/v2/apps/{app_id}/deployments-POST': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'force_build'
            },
        ]
    },
    '/v2/apps/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/v2/apps/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/v2/apps/{app_id}/components/{component_name}/logs-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'component_name'
            },
            {
                'name': 'type'
            },
            {
                'name': 'follow'
            },
            {
                'name': 'pod_connection_timeout'
            },
        ]
    },
    '/v2/apps/{app_id}/logs-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'type'
            },
            {
                'name': 'follow'
            },
            {
                'name': 'pod_connection_timeout'
            },
        ]
    },
    '/v2/apps/{app_id}/deployments/{deployment_id}/logs-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'deployment_id'
            },
            {
                'name': 'type'
            },
            {
                'name': 'follow'
            },
            {
                'name': 'pod_connection_timeout'
            },
        ]
    },
    '/v2/apps/{app_id}/metrics/bandwidth_daily-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'date'
            },
        ]
    },
    '/v2/apps/{app_id}/deployments/{deployment_id}-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'deployment_id'
            },
        ]
    },
    '/v2/apps/{app_id}/deployments/{deployment_id}/components/{component_name}/logs-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'deployment_id'
            },
            {
                'name': 'component_name'
            },
            {
                'name': 'type'
            },
            {
                'name': 'follow'
            },
            {
                'name': 'pod_connection_timeout'
            },
        ]
    },
    '/v2/apps/tiers/instance_sizes/{slug}-GET': {
        'parameters': [
            {
                'name': 'slug'
            },
        ]
    },
    '/v2/apps/metrics/bandwidth_daily-POST': {
        'parameters': [
            {
                'name': 'app_ids'
            },
            {
                'name': 'date'
            },
        ]
    },
    '/v2/apps/tiers/{slug}-GET': {
        'parameters': [
            {
                'name': 'slug'
            },
        ]
    },
    '/v2/apps-GET': {
        'parameters': [
            {
                'name': 'page'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'with_projects'
            },
        ]
    },
    '/v2/apps/{app_id}/alerts-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
        ]
    },
    '/v2/apps/{app_id}/deployments-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'page'
            },
            {
                'name': 'per_page'
            },
        ]
    },
    '/v2/apps/tiers/instance_sizes-GET': {
        'parameters': [
        ]
    },
    '/v2/apps/regions-GET': {
        'parameters': [
        ]
    },
    '/v2/apps/tiers-GET': {
        'parameters': [
        ]
    },
    '/v2/apps/propose-POST': {
        'parameters': [
            {
                'name': 'spec'
            },
            {
                'name': 'app_id'
            },
        ]
    },
    '/v2/apps/{app_id}/rollback/revert-POST': {
        'parameters': [
            {
                'name': 'app_id'
            },
        ]
    },
    '/v2/apps/{app_id}/rollback-POST': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'deployment_id'
            },
            {
                'name': 'skip_pin'
            },
        ]
    },
    '/v2/apps/{id}-PUT': {
        'parameters': [
            {
                'name': 'spec'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/v2/apps/{app_id}/alerts/{alert_id}/destinations-POST': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'alert_id'
            },
            {
                'name': 'emails'
            },
            {
                'name': 'slack_webhooks'
            },
        ]
    },
    '/v2/apps/{app_id}/rollback/validate-POST': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'deployment_id'
            },
            {
                'name': 'skip_pin'
            },
        ]
    },
    '/v2/customers/my/balance-GET': {
        'parameters': [
        ]
    },
    '/v2/customers/my/invoices/{invoice_uuid}-GET': {
        'parameters': [
            {
                'name': 'invoice_uuid'
            },
        ]
    },
    '/v2/customers/my/invoices/{invoice_uuid}/csv-GET': {
        'parameters': [
            {
                'name': 'invoice_uuid'
            },
        ]
    },
    '/v2/customers/my/invoices/{invoice_uuid}/summary-GET': {
        'parameters': [
            {
                'name': 'invoice_uuid'
            },
        ]
    },
    '/v2/customers/my/invoices/{invoice_uuid}/pdf-GET': {
        'parameters': [
            {
                'name': 'invoice_uuid'
            },
        ]
    },
    '/v2/customers/my/billing_history-GET': {
        'parameters': [
        ]
    },
    '/v2/customers/my/invoices-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/volumes-POST': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'description'
            },
            {
                'name': 'id'
            },
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'name'
            },
            {
                'name': 'size_gigabytes'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'snapshot_id'
            },
            {
                'name': 'filesystem_type'
            },
            {
                'name': 'region'
            },
            {
                'name': 'filesystem_label'
            },
        ]
    },
    '/v2/volumes/{volume_id}/snapshots-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'volume_id'
            },
            {
                'name': 'tags'
            },
        ]
    },
    '/v2/volumes/{volume_id}-DELETE': {
        'parameters': [
            {
                'name': 'volume_id'
            },
        ]
    },
    '/v2/volumes-DELETE': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'region'
            },
        ]
    },
    '/v2/volumes/snapshots/{snapshot_id}-DELETE': {
        'parameters': [
            {
                'name': 'snapshot_id'
            },
        ]
    },
    '/v2/volumes/{volume_id}-GET': {
        'parameters': [
            {
                'name': 'volume_id'
            },
        ]
    },
    '/v2/volumes/snapshots/{snapshot_id}-GET': {
        'parameters': [
            {
                'name': 'snapshot_id'
            },
        ]
    },
    '/v2/volumes-GET': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'region'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/volumes/{volume_id}/snapshots-GET': {
        'parameters': [
            {
                'name': 'volume_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/volumes/{volume_id}/actions/{action_id}-GET': {
        'parameters': [
            {
                'name': 'volume_id'
            },
            {
                'name': 'action_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/volumes/{volume_id}/actions-POST': {
        'parameters': [
            {
                'name': 'volume_id'
            },
            {
                'name': 'type'
            },
            {
                'name': 'region'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'droplet_id'
            },
            {
                'name': 'size_gigabytes'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/volumes/{volume_id}/actions-GET': {
        'parameters': [
            {
                'name': 'volume_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/volumes/actions-POST': {
        'parameters': [
            {
                'name': 'type'
            },
            {
                'name': 'region'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'droplet_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/cdn/endpoints-POST': {
        'parameters': [
            {
                'name': 'origin'
            },
            {
                'name': 'id'
            },
            {
                'name': 'endpoint'
            },
            {
                'name': 'ttl'
            },
            {
                'name': 'certificate_id'
            },
            {
                'name': 'custom_domain'
            },
            {
                'name': 'created_at'
            },
        ]
    },
    '/v2/cdn/endpoints/{cdn_id}-DELETE': {
        'parameters': [
            {
                'name': 'cdn_id'
            },
        ]
    },
    '/v2/cdn/endpoints/{cdn_id}-GET': {
        'parameters': [
            {
                'name': 'cdn_id'
            },
        ]
    },
    '/v2/cdn/endpoints-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/cdn/endpoints/{cdn_id}/cache-DELETE': {
        'parameters': [
            {
                'name': 'files'
            },
            {
                'name': 'cdn_id'
            },
        ]
    },
    '/v2/cdn/endpoints/{cdn_id}-PUT': {
        'parameters': [
            {
                'name': 'cdn_id'
            },
            {
                'name': 'ttl'
            },
            {
                'name': 'certificate_id'
            },
            {
                'name': 'custom_domain'
            },
        ]
    },
    '/v2/certificates-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'type'
            },
            {
                'name': 'dns_names'
            },
            {
                'name': 'private_key'
            },
            {
                'name': 'leaf_certificate'
            },
            {
                'name': 'certificate_chain'
            },
        ]
    },
    '/v2/certificates/{certificate_id}-DELETE': {
        'parameters': [
            {
                'name': 'certificate_id'
            },
        ]
    },
    '/v2/certificates/{certificate_id}-GET': {
        'parameters': [
            {
                'name': 'certificate_id'
            },
        ]
    },
    '/v2/certificates-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/v2/registry/{registry_name}/garbage-collection/{garbage_collection_uuid}-PUT': {
        'parameters': [
            {
                'name': 'registry_name'
            },
            {
                'name': 'garbage_collection_uuid'
            },
            {
                'name': 'cancel'
            },
        ]
    },
    '/v2/registry-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'subscription_tier_slug'
            },
            {
                'name': 'region'
            },
        ]
    },
    '/v2/registry-DELETE': {
        'parameters': [
        ]
    },
    '/v2/registry/{registry_name}/repositories/{repository_name}/digests/{manifest_digest}-DELETE': {
        'parameters': [
            {
                'name': 'registry_name'
            },
            {
                'name': 'repository_name'
            },
            {
                'name': 'manifest_digest'
            },
        ]
    },
    '/v2/registry/{registry_name}/repositories/{repository_name}/tags/{repository_tag}-DELETE': {
        'parameters': [
            {
                'name': 'registry_name'
            },
            {
                'name': 'repository_name'
            },
            {
                'name': 'repository_tag'
            },
        ]
    },
    '/v2/registry-GET': {
        'parameters': [
        ]
    },
    '/v2/registry/{registry_name}/garbage-collection-GET': {
        'parameters': [
            {
                'name': 'registry_name'
            },
        ]
    },
    '/v2/registry/docker-credentials-GET': {
        'parameters': [
            {
                'name': 'expiry_seconds'
            },
            {
                'name': 'read_write'
            },
        ]
    },
    '/v2/registry/subscription-GET': {
        'parameters': [
        ]
    },
    '/v2/registry/{registry_name}/garbage-collections-GET': {
        'parameters': [
            {
                'name': 'registry_name'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/registry/options-GET': {
        'parameters': [
        ]
    },
    '/v2/registry/{registry_name}/repositories-GET': {
        'parameters': [
            {
                'name': 'registry_name'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/registry/{registry_name}/repositoriesV2-GET': {
        'parameters': [
            {
                'name': 'registry_name'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
            {
                'name': 'page_token'
            },
        ]
    },
    '/v2/registry/{registry_name}/repositories/{repository_name}/digests-GET': {
        'parameters': [
            {
                'name': 'registry_name'
            },
            {
                'name': 'repository_name'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/registry/{registry_name}/repositories/{repository_name}/tags-GET': {
        'parameters': [
            {
                'name': 'registry_name'
            },
            {
                'name': 'repository_name'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/registry/{registry_name}/garbage-collection-POST': {
        'parameters': [
            {
                'name': 'registry_name'
            },
        ]
    },
    '/v2/registry/subscription-POST': {
        'parameters': [
            {
                'name': 'tier_slug'
            },
        ]
    },
    '/v2/registry/validate-name-POST': {
        'parameters': [
            {
                'name': 'name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/dbs-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/pools-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'mode'
            },
            {
                'name': 'size'
            },
            {
                'name': 'db'
            },
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'user'
            },
            {
                'name': 'connection'
            },
            {
                'name': 'private_connection'
            },
            {
                'name': 'standby_connection'
            },
            {
                'name': 'standby_private_connection'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/users-POST': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'name'
            },
            {
                'name': 'role'
            },
            {
                'name': 'password'
            },
            {
                'name': 'access_cert'
            },
            {
                'name': 'access_key'
            },
            {
                'name': 'mysql_settings'
            },
            {
                'name': 'settings'
            },
            {
                'name': 'readonly'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/eviction_policy-PUT': {
        'parameters': [
            {
                'name': 'eviction_policy'
            },
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/maintenance-PUT': {
        'parameters': [
            {
                'name': 'day'
            },
            {
                'name': 'hour'
            },
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'description'
            },
            {
                'name': 'pending'
            },
        ]
    },
    '/v2/databases-POST': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'version'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'engine'
            },
            {
                'name': 'semantic_version'
            },
            {
                'name': 'num_nodes'
            },
            {
                'name': 'size'
            },
            {
                'name': 'region'
            },
            {
                'name': 'status'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'private_network_uuid'
            },
            {
                'name': 'db_names'
            },
            {
                'name': 'connection'
            },
            {
                'name': 'private_connection'
            },
            {
                'name': 'standby_connection'
            },
            {
                'name': 'standby_private_connection'
            },
            {
                'name': 'users'
            },
            {
                'name': 'maintenance_window'
            },
            {
                'name': 'project_id'
            },
            {
                'name': 'rules'
            },
            {
                'name': 'version_end_of_life'
            },
            {
                'name': 'version_end_of_availability'
            },
            {
                'name': 'storage_size_mib'
            },
            {
                'name': 'metrics_endpoints'
            },
            {
                'name': 'backup_restore'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/replicas-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'id'
            },
            {
                'name': 'region'
            },
            {
                'name': 'size'
            },
            {
                'name': 'status'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'private_network_uuid'
            },
            {
                'name': 'connection'
            },
            {
                'name': 'private_connection'
            },
            {
                'name': 'storage_size_mib'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/topics-POST': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'name'
            },
            {
                'name': 'replication_factor'
            },
            {
                'name': 'partition_count'
            },
            {
                'name': 'config'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/dbs/{database_name}-DELETE': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'database_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/pools/{pool_name}-DELETE': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'pool_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/topics/{topic_name}-DELETE': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'topic_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}-DELETE': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/replicas/{replica_name}-DELETE': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'replica_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/dbs/{database_name}-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'database_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/config-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/metrics/credentials-GET': {
        'parameters': [
        ]
    },
    '/v2/databases/{database_cluster_uuid}/pools/{pool_name}-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'pool_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/eviction_policy-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/replicas/{replica_name}-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'replica_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/online-migration-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/ca-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/sql_mode-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/topics/{topic_name}-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'topic_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/users/{username}-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'username'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/dbs-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/backups-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases-GET': {
        'parameters': [
            {
                'name': 'tag_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/pools-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/events-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/firewall-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/options-GET': {
        'parameters': [
        ]
    },
    '/v2/databases/{database_cluster_uuid}/replicas-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/topics-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/users-GET': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/migrate-PUT': {
        'parameters': [
            {
                'name': 'region'
            },
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/replicas/{replica_name}/promote-PUT': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'replica_name'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/users/{username}-DELETE': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'username'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/users/{username}/reset_auth-POST': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'username'
            },
            {
                'name': 'mysql_settings'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/resize-PUT': {
        'parameters': [
            {
                'name': 'size'
            },
            {
                'name': 'num_nodes'
            },
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'storage_size_mib'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/online-migration-PUT': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'source'
            },
            {
                'name': 'disable_ssl'
            },
            {
                'name': 'ignore_dbs'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/online-migration/{migration_id}-DELETE': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'migration_id'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/config-PATCH': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'config'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/pools/{pool_name}-PUT': {
        'parameters': [
            {
                'name': 'mode'
            },
            {
                'name': 'size'
            },
            {
                'name': 'db'
            },
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'pool_name'
            },
            {
                'name': 'user'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/firewall-PUT': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'rules'
            },
        ]
    },
    '/v2/databases/metrics/credentials-PUT': {
        'parameters': [
            {
                'name': 'credentials'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/users/{username}-PUT': {
        'parameters': [
            {
                'name': 'settings'
            },
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'username'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/sql_mode-PUT': {
        'parameters': [
            {
                'name': 'sql_mode'
            },
            {
                'name': 'database_cluster_uuid'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/topics/{topic_name}-PUT': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'topic_name'
            },
            {
                'name': 'replication_factor'
            },
            {
                'name': 'partition_count'
            },
            {
                'name': 'config'
            },
        ]
    },
    '/v2/databases/{database_cluster_uuid}/upgrade-PUT': {
        'parameters': [
            {
                'name': 'database_cluster_uuid'
            },
            {
                'name': 'version'
            },
        ]
    },
    '/v2/domains/{domain_name}/records-POST': {
        'parameters': [
            {
                'name': 'domain_name'
            },
            {
                'name': 'id'
            },
            {
                'name': 'type'
            },
            {
                'name': 'name'
            },
            {
                'name': 'data'
            },
            {
                'name': 'priority'
            },
            {
                'name': 'port'
            },
            {
                'name': 'ttl'
            },
            {
                'name': 'weight'
            },
            {
                'name': 'flags'
            },
            {
                'name': 'tag'
            },
        ]
    },
    '/v2/domains/{domain_name}/records/{domain_record_id}-DELETE': {
        'parameters': [
            {
                'name': 'domain_name'
            },
            {
                'name': 'domain_record_id'
            },
        ]
    },
    '/v2/domains/{domain_name}/records/{domain_record_id}-GET': {
        'parameters': [
            {
                'name': 'domain_name'
            },
            {
                'name': 'domain_record_id'
            },
        ]
    },
    '/v2/domains/{domain_name}/records-GET': {
        'parameters': [
            {
                'name': 'domain_name'
            },
            {
                'name': 'name'
            },
            {
                'name': 'type'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/domains/{domain_name}/records/{domain_record_id}-PUT': {
        'parameters': [
            {
                'name': 'type'
            },
            {
                'name': 'domain_name'
            },
            {
                'name': 'domain_record_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'data'
            },
            {
                'name': 'priority'
            },
            {
                'name': 'port'
            },
            {
                'name': 'ttl'
            },
            {
                'name': 'weight'
            },
            {
                'name': 'flags'
            },
            {
                'name': 'tag'
            },
        ]
    },
    '/v2/domains/{domain_name}/records/{domain_record_id}-PATCH': {
        'parameters': [
            {
                'name': 'type'
            },
            {
                'name': 'domain_name'
            },
            {
                'name': 'domain_record_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'data'
            },
            {
                'name': 'priority'
            },
            {
                'name': 'port'
            },
            {
                'name': 'ttl'
            },
            {
                'name': 'weight'
            },
            {
                'name': 'flags'
            },
            {
                'name': 'tag'
            },
        ]
    },
    '/v2/domains-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'ip_address'
            },
            {
                'name': 'ttl'
            },
            {
                'name': 'zone_file'
            },
        ]
    },
    '/v2/domains/{domain_name}-DELETE': {
        'parameters': [
            {
                'name': 'domain_name'
            },
        ]
    },
    '/v2/domains/{domain_name}-GET': {
        'parameters': [
            {
                'name': 'domain_name'
            },
        ]
    },
    '/v2/domains-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/droplets/actions-POST': {
        'parameters': [
            {
                'name': 'type'
            },
            {
                'name': 'name'
            },
            {
                'name': 'tag_name'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/actions/{action_id}-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'action_id'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/actions-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/actions-POST': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'type'
            },
            {
                'name': 'image'
            },
            {
                'name': 'disk'
            },
            {
                'name': 'size'
            },
            {
                'name': 'name'
            },
            {
                'name': 'kernel'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/destroy_with_associated_resources/status-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
        ]
    },
    '/v2/droplets-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'region'
            },
            {
                'name': 'size'
            },
            {
                'name': 'image'
            },
            {
                'name': 'ssh_keys'
            },
            {
                'name': 'backups'
            },
            {
                'name': 'ipv6'
            },
            {
                'name': 'monitoring'
            },
            {
                'name': 'user_data'
            },
            {
                'name': 'private_networking'
            },
            {
                'name': 'volumes'
            },
            {
                'name': 'vpc_uuid'
            },
            {
                'name': 'with_droplet_agent'
            },
            {
                'name': 'names'
            },
        ]
    },
    '/v2/droplets-DELETE': {
        'parameters': [
            {
                'name': 'tag_name'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/destroy_with_associated_resources/dangerous-DELETE': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'X-Dangerous'
            },
        ]
    },
    '/v2/droplets/{droplet_id}-DELETE': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/destroy_with_associated_resources/selective-DELETE': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'floating_ips'
            },
            {
                'name': 'reserved_ips'
            },
            {
                'name': 'snapshots'
            },
            {
                'name': 'volumes'
            },
            {
                'name': 'volume_snapshots'
            },
        ]
    },
    '/v2/droplets/{droplet_id}-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
        ]
    },
    '/v2/droplets-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
            {
                'name': 'tag_name'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/destroy_with_associated_resources-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/backups-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/reports/droplet_neighbors_ids-GET': {
        'parameters': [
        ]
    },
    '/v2/droplets/{droplet_id}/firewalls-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/kernels-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/neighbors-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/snapshots-GET': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/droplets/{droplet_id}/destroy_with_associated_resources/retry-POST': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}/droplets-POST': {
        'parameters': [
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'firewall_id'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}/rules-POST': {
        'parameters': [
            {
                'name': 'firewall_id'
            },
            {
                'name': 'inbound_rules'
            },
            {
                'name': 'outbound_rules'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}/tags-POST': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'firewall_id'
            },
        ]
    },
    '/v2/firewalls-POST': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'id'
            },
            {
                'name': 'status'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'pending_changes'
            },
            {
                'name': 'name'
            },
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'inbound_rules'
            },
            {
                'name': 'outbound_rules'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}-DELETE': {
        'parameters': [
            {
                'name': 'firewall_id'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}-GET': {
        'parameters': [
            {
                'name': 'firewall_id'
            },
        ]
    },
    '/v2/firewalls-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}/droplets-DELETE': {
        'parameters': [
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'firewall_id'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}/rules-DELETE': {
        'parameters': [
            {
                'name': 'firewall_id'
            },
            {
                'name': 'inbound_rules'
            },
            {
                'name': 'outbound_rules'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}/tags-DELETE': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'firewall_id'
            },
        ]
    },
    '/v2/firewalls/{firewall_id}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'firewall_id'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'id'
            },
            {
                'name': 'status'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'pending_changes'
            },
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'inbound_rules'
            },
            {
                'name': 'outbound_rules'
            },
        ]
    },
    '/v2/floating_ips/{floating_ip}/actions/{action_id}-GET': {
        'parameters': [
            {
                'name': 'floating_ip'
            },
            {
                'name': 'action_id'
            },
        ]
    },
    '/v2/floating_ips/{floating_ip}/actions-GET': {
        'parameters': [
            {
                'name': 'floating_ip'
            },
        ]
    },
    '/v2/floating_ips/{floating_ip}/actions-POST': {
        'parameters': [
            {
                'name': 'floating_ip'
            },
            {
                'name': 'type'
            },
            {
                'name': 'droplet_id'
            },
        ]
    },
    '/v2/floating_ips-POST': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'region'
            },
            {
                'name': 'project_id'
            },
        ]
    },
    '/v2/floating_ips/{floating_ip}-DELETE': {
        'parameters': [
            {
                'name': 'floating_ip'
            },
        ]
    },
    '/v2/floating_ips/{floating_ip}-GET': {
        'parameters': [
            {
                'name': 'floating_ip'
            },
        ]
    },
    '/v2/floating_ips-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/functions/namespaces-POST': {
        'parameters': [
            {
                'name': 'region'
            },
            {
                'name': 'label'
            },
        ]
    },
    '/v2/functions/namespaces/{namespace_id}/triggers-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'function'
            },
            {
                'name': 'type'
            },
            {
                'name': 'is_enabled'
            },
            {
                'name': 'scheduled_details'
            },
            {
                'name': 'namespace_id'
            },
        ]
    },
    '/v2/functions/namespaces/{namespace_id}-DELETE': {
        'parameters': [
            {
                'name': 'namespace_id'
            },
        ]
    },
    '/v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}-DELETE': {
        'parameters': [
            {
                'name': 'namespace_id'
            },
            {
                'name': 'trigger_name'
            },
        ]
    },
    '/v2/functions/namespaces/{namespace_id}-GET': {
        'parameters': [
            {
                'name': 'namespace_id'
            },
        ]
    },
    '/v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}-GET': {
        'parameters': [
            {
                'name': 'namespace_id'
            },
            {
                'name': 'trigger_name'
            },
        ]
    },
    '/v2/functions/namespaces-GET': {
        'parameters': [
        ]
    },
    '/v2/functions/namespaces/{namespace_id}/triggers-GET': {
        'parameters': [
            {
                'name': 'namespace_id'
            },
        ]
    },
    '/v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}-PUT': {
        'parameters': [
            {
                'name': 'namespace_id'
            },
            {
                'name': 'trigger_name'
            },
            {
                'name': 'is_enabled'
            },
            {
                'name': 'scheduled_details'
            },
        ]
    },
    '/v2/images/{image_id}/actions/{action_id}-GET': {
        'parameters': [
            {
                'name': 'image_id'
            },
            {
                'name': 'action_id'
            },
        ]
    },
    '/v2/images/{image_id}/actions-GET': {
        'parameters': [
            {
                'name': 'image_id'
            },
        ]
    },
    '/v2/images/{image_id}/actions-POST': {
        'parameters': [
            {
                'name': 'image_id'
            },
            {
                'name': 'type'
            },
            {
                'name': 'region'
            },
        ]
    },
    '/v2/images/{image_id}-DELETE': {
        'parameters': [
            {
                'name': 'image_id'
            },
        ]
    },
    '/v2/images/{image_id}-GET': {
        'parameters': [
            {
                'name': 'image_id'
            },
        ]
    },
    '/v2/images-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'url'
            },
            {
                'name': 'region'
            },
            {
                'name': 'description'
            },
            {
                'name': 'distribution'
            },
            {
                'name': 'tags'
            },
        ]
    },
    '/v2/images-GET': {
        'parameters': [
            {
                'name': 'type'
            },
            {
                'name': 'private'
            },
            {
                'name': 'tag_name'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/images/{image_id}-PUT': {
        'parameters': [
            {
                'name': 'image_id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'name'
            },
            {
                'name': 'distribution'
            },
        ]
    },
    '/v2/kubernetes/registry-POST': {
        'parameters': [
            {
                'name': 'cluster_uuids'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/node_pools-POST': {
        'parameters': [
            {
                'name': 'size'
            },
            {
                'name': 'name'
            },
            {
                'name': 'count'
            },
            {
                'name': 'cluster_id'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'id'
            },
            {
                'name': 'labels'
            },
            {
                'name': 'taints'
            },
            {
                'name': 'auto_scale'
            },
            {
                'name': 'min_nodes'
            },
            {
                'name': 'max_nodes'
            },
            {
                'name': 'nodes'
            },
        ]
    },
    '/v2/kubernetes/clusters-POST': {
        'parameters': [
            {
                'name': 'version'
            },
            {
                'name': 'name'
            },
            {
                'name': 'region'
            },
            {
                'name': 'node_pools'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'id'
            },
            {
                'name': 'cluster_subnet'
            },
            {
                'name': 'service_subnet'
            },
            {
                'name': 'vpc_uuid'
            },
            {
                'name': 'ipv4'
            },
            {
                'name': 'endpoint'
            },
            {
                'name': 'maintenance_policy'
            },
            {
                'name': 'auto_upgrade'
            },
            {
                'name': 'status'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'updated_at'
            },
            {
                'name': 'surge_upgrade'
            },
            {
                'name': 'ha'
            },
            {
                'name': 'registry_enabled'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}-DELETE': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources/dangerous-DELETE': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}/nodes/{node_id}-DELETE': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'node_pool_id'
            },
            {
                'name': 'node_id'
            },
            {
                'name': 'skip_drain'
            },
            {
                'name': 'replace'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}-DELETE': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'node_pool_id'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/upgrades-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/clusterlint-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'run_id'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/credentials-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'expiry_seconds'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/kubeconfig-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'expiry_seconds'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'node_pool_id'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/user-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
        ]
    },
    '/v2/kubernetes/clusters-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/node_pools-GET': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
        ]
    },
    '/v2/kubernetes/options-GET': {
        'parameters': [
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}/recycle-POST': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'node_pool_id'
            },
            {
                'name': 'nodes'
            },
        ]
    },
    '/v2/kubernetes/registry-DELETE': {
        'parameters': [
            {
                'name': 'cluster_uuids'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/clusterlint-POST': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'include_groups'
            },
            {
                'name': 'include_checks'
            },
            {
                'name': 'exclude_groups'
            },
            {
                'name': 'exclude_checks'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources/selective-DELETE': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'load_balancers'
            },
            {
                'name': 'volumes'
            },
            {
                'name': 'volume_snapshots'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'cluster_id'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'maintenance_policy'
            },
            {
                'name': 'auto_upgrade'
            },
            {
                'name': 'surge_upgrade'
            },
            {
                'name': 'ha'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}-PUT': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'node_pool_id'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'count'
            },
            {
                'name': 'labels'
            },
            {
                'name': 'taints'
            },
            {
                'name': 'auto_scale'
            },
            {
                'name': 'min_nodes'
            },
            {
                'name': 'max_nodes'
            },
            {
                'name': 'nodes'
            },
        ]
    },
    '/v2/kubernetes/clusters/{cluster_id}/upgrade-POST': {
        'parameters': [
            {
                'name': 'cluster_id'
            },
            {
                'name': 'version'
            },
        ]
    },
    '/v2/load_balancers/{lb_id}/forwarding_rules-POST': {
        'parameters': [
            {
                'name': 'forwarding_rules'
            },
            {
                'name': 'lb_id'
            },
        ]
    },
    '/v2/load_balancers/{lb_id}/droplets-POST': {
        'parameters': [
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'lb_id'
            },
        ]
    },
    '/v2/load_balancers-POST': {
        'parameters': [
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'region'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'project_id'
            },
            {
                'name': 'ip'
            },
            {
                'name': 'size_unit'
            },
            {
                'name': 'size'
            },
            {
                'name': 'algorithm'
            },
            {
                'name': 'status'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'forwarding_rules'
            },
            {
                'name': 'health_check'
            },
            {
                'name': 'sticky_sessions'
            },
            {
                'name': 'redirect_http_to_https'
            },
            {
                'name': 'enable_proxy_protocol'
            },
            {
                'name': 'enable_backend_keepalive'
            },
            {
                'name': 'http_idle_timeout_seconds'
            },
            {
                'name': 'vpc_uuid'
            },
            {
                'name': 'disable_lets_encrypt_dns_records'
            },
            {
                'name': 'firewall'
            },
            {
                'name': 'tag'
            },
        ]
    },
    '/v2/load_balancers/{lb_id}-DELETE': {
        'parameters': [
            {
                'name': 'lb_id'
            },
        ]
    },
    '/v2/load_balancers/{lb_id}-GET': {
        'parameters': [
            {
                'name': 'lb_id'
            },
        ]
    },
    '/v2/load_balancers-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/load_balancers/{lb_id}/droplets-DELETE': {
        'parameters': [
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'lb_id'
            },
        ]
    },
    '/v2/load_balancers/{lb_id}/forwarding_rules-DELETE': {
        'parameters': [
            {
                'name': 'forwarding_rules'
            },
            {
                'name': 'lb_id'
            },
        ]
    },
    '/v2/load_balancers/{lb_id}-PUT': {
        'parameters': [
            {
                'name': 'lb_id'
            },
            {
                'name': 'droplet_ids'
            },
            {
                'name': 'region'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'project_id'
            },
            {
                'name': 'ip'
            },
            {
                'name': 'size_unit'
            },
            {
                'name': 'size'
            },
            {
                'name': 'algorithm'
            },
            {
                'name': 'status'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'forwarding_rules'
            },
            {
                'name': 'health_check'
            },
            {
                'name': 'sticky_sessions'
            },
            {
                'name': 'redirect_http_to_https'
            },
            {
                'name': 'enable_proxy_protocol'
            },
            {
                'name': 'enable_backend_keepalive'
            },
            {
                'name': 'http_idle_timeout_seconds'
            },
            {
                'name': 'vpc_uuid'
            },
            {
                'name': 'disable_lets_encrypt_dns_records'
            },
            {
                'name': 'firewall'
            },
            {
                'name': 'tag'
            },
        ]
    },
    '/v2/monitoring/alerts-POST': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'description'
            },
            {
                'name': 'alerts'
            },
            {
                'name': 'compare'
            },
            {
                'name': 'enabled'
            },
            {
                'name': 'entities'
            },
            {
                'name': 'type'
            },
            {
                'name': 'value'
            },
            {
                'name': 'window'
            },
        ]
    },
    '/v2/monitoring/alerts/{alert_uuid}-DELETE': {
        'parameters': [
            {
                'name': 'alert_uuid'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/cpu-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/load_5-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/memory_cached-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/apps/cpu_percentage-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
            {
                'name': 'app_component'
            },
        ]
    },
    '/v2/monitoring/metrics/apps/memory_percentage-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
            {
                'name': 'app_component'
            },
        ]
    },
    '/v2/monitoring/metrics/apps/restart_count-GET': {
        'parameters': [
            {
                'name': 'app_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
            {
                'name': 'app_component'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/bandwidth-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'interface'
            },
            {
                'name': 'direction'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/filesystem_free-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/filesystem_size-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/load_15-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/load_1-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/memory_available-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/memory_free-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/metrics/droplet/memory_total-GET': {
        'parameters': [
            {
                'name': 'host_id'
            },
            {
                'name': 'start'
            },
            {
                'name': 'end'
            },
        ]
    },
    '/v2/monitoring/alerts/{alert_uuid}-GET': {
        'parameters': [
            {
                'name': 'alert_uuid'
            },
        ]
    },
    '/v2/monitoring/alerts-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/monitoring/alerts/{alert_uuid}-PUT': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'description'
            },
            {
                'name': 'alerts'
            },
            {
                'name': 'compare'
            },
            {
                'name': 'enabled'
            },
            {
                'name': 'entities'
            },
            {
                'name': 'type'
            },
            {
                'name': 'value'
            },
            {
                'name': 'window'
            },
            {
                'name': 'alert_uuid'
            },
        ]
    },
    '/v2/projects/default/resources-POST': {
        'parameters': [
            {
                'name': 'resources'
            },
        ]
    },
    '/v2/projects/{project_id}/resources-POST': {
        'parameters': [
            {
                'name': 'project_id'
            },
            {
                'name': 'resources'
            },
        ]
    },
    '/v2/projects/{project_id}/resources-GET': {
        'parameters': [
            {
                'name': 'project_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/projects/default/resources-GET': {
        'parameters': [
        ]
    },
    '/v2/projects-POST': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'id'
            },
            {
                'name': 'owner_uuid'
            },
            {
                'name': 'owner_id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'purpose'
            },
            {
                'name': 'environment'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'updated_at'
            },
        ]
    },
    '/v2/projects/{project_id}-DELETE': {
        'parameters': [
            {
                'name': 'project_id'
            },
        ]
    },
    '/v2/projects/{project_id}-GET': {
        'parameters': [
            {
                'name': 'project_id'
            },
        ]
    },
    '/v2/projects/default-GET': {
        'parameters': [
        ]
    },
    '/v2/projects-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/projects/{project_id}-PATCH': {
        'parameters': [
            {
                'name': 'project_id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'id'
            },
            {
                'name': 'owner_uuid'
            },
            {
                'name': 'owner_id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'purpose'
            },
            {
                'name': 'environment'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'updated_at'
            },
            {
                'name': 'is_default'
            },
        ]
    },
    '/v2/projects/{project_id}-PUT': {
        'parameters': [
            {
                'name': 'project_id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'id'
            },
            {
                'name': 'owner_uuid'
            },
            {
                'name': 'owner_id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'purpose'
            },
            {
                'name': 'environment'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'updated_at'
            },
            {
                'name': 'is_default'
            },
        ]
    },
    '/v2/projects/default-PUT': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'id'
            },
            {
                'name': 'owner_uuid'
            },
            {
                'name': 'owner_id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'purpose'
            },
            {
                'name': 'environment'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'updated_at'
            },
            {
                'name': 'is_default'
            },
        ]
    },
    '/v2/projects/default-PATCH': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'id'
            },
            {
                'name': 'owner_uuid'
            },
            {
                'name': 'owner_id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'purpose'
            },
            {
                'name': 'environment'
            },
            {
                'name': 'created_at'
            },
            {
                'name': 'updated_at'
            },
            {
                'name': 'is_default'
            },
        ]
    },
    '/v2/regions-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/reserved_ips/{reserved_ip}/actions/{action_id}-GET': {
        'parameters': [
            {
                'name': 'reserved_ip'
            },
            {
                'name': 'action_id'
            },
        ]
    },
    '/v2/reserved_ips/{reserved_ip}/actions-GET': {
        'parameters': [
            {
                'name': 'reserved_ip'
            },
        ]
    },
    '/v2/reserved_ips/{reserved_ip}/actions-POST': {
        'parameters': [
            {
                'name': 'reserved_ip'
            },
            {
                'name': 'type'
            },
            {
                'name': 'droplet_id'
            },
        ]
    },
    '/v2/reserved_ips-POST': {
        'parameters': [
            {
                'name': 'droplet_id'
            },
            {
                'name': 'region'
            },
            {
                'name': 'project_id'
            },
        ]
    },
    '/v2/reserved_ips/{reserved_ip}-DELETE': {
        'parameters': [
            {
                'name': 'reserved_ip'
            },
        ]
    },
    '/v2/reserved_ips/{reserved_ip}-GET': {
        'parameters': [
            {
                'name': 'reserved_ip'
            },
        ]
    },
    '/v2/reserved_ips-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/account/keys-POST': {
        'parameters': [
            {
                'name': 'public_key'
            },
            {
                'name': 'name'
            },
            {
                'name': 'id'
            },
            {
                'name': 'fingerprint'
            },
        ]
    },
    '/v2/account/keys/{ssh_key_identifier}-DELETE': {
        'parameters': [
            {
                'name': 'ssh_key_identifier'
            },
        ]
    },
    '/v2/account/keys/{ssh_key_identifier}-GET': {
        'parameters': [
            {
                'name': 'ssh_key_identifier'
            },
        ]
    },
    '/v2/account/keys-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/account/keys/{ssh_key_identifier}-PUT': {
        'parameters': [
            {
                'name': 'ssh_key_identifier'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/v2/sizes-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/snapshots/{snapshot_id}-DELETE': {
        'parameters': [
            {
                'name': 'snapshot_id'
            },
        ]
    },
    '/v2/snapshots/{snapshot_id}-GET': {
        'parameters': [
            {
                'name': 'snapshot_id'
            },
        ]
    },
    '/v2/snapshots-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
            {
                'name': 'resource_type'
            },
        ]
    },
    '/v2/tags-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'resources'
            },
        ]
    },
    '/v2/tags/{tag_id}-DELETE': {
        'parameters': [
            {
                'name': 'tag_id'
            },
        ]
    },
    '/v2/tags/{tag_id}-GET': {
        'parameters': [
            {
                'name': 'tag_id'
            },
        ]
    },
    '/v2/tags-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/tags/{tag_id}/resources-POST': {
        'parameters': [
            {
                'name': 'resources'
            },
            {
                'name': 'tag_id'
            },
        ]
    },
    '/v2/tags/{tag_id}/resources-DELETE': {
        'parameters': [
            {
                'name': 'resources'
            },
            {
                'name': 'tag_id'
            },
        ]
    },
    '/v2/uptime/checks-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'type'
            },
            {
                'name': 'target'
            },
            {
                'name': 'regions'
            },
            {
                'name': 'enabled'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}/alerts-POST': {
        'parameters': [
            {
                'name': 'check_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'type'
            },
            {
                'name': 'threshold'
            },
            {
                'name': 'comparison'
            },
            {
                'name': 'notifications'
            },
            {
                'name': 'period'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}/alerts/{alert_id}-DELETE': {
        'parameters': [
            {
                'name': 'check_id'
            },
            {
                'name': 'alert_id'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}-DELETE': {
        'parameters': [
            {
                'name': 'check_id'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}-GET': {
        'parameters': [
            {
                'name': 'check_id'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}/state-GET': {
        'parameters': [
            {
                'name': 'check_id'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}/alerts/{alert_id}-GET': {
        'parameters': [
            {
                'name': 'check_id'
            },
            {
                'name': 'alert_id'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}/alerts-GET': {
        'parameters': [
            {
                'name': 'check_id'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/uptime/checks-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}/alerts/{alert_id}-PUT': {
        'parameters': [
            {
                'name': 'check_id'
            },
            {
                'name': 'alert_id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'type'
            },
            {
                'name': 'threshold'
            },
            {
                'name': 'comparison'
            },
            {
                'name': 'notifications'
            },
            {
                'name': 'period'
            },
        ]
    },
    '/v2/uptime/checks/{check_id}-PUT': {
        'parameters': [
            {
                'name': 'check_id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'type'
            },
            {
                'name': 'target'
            },
            {
                'name': 'regions'
            },
            {
                'name': 'enabled'
            },
        ]
    },
    '/v2/vpcs-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'region'
            },
            {
                'name': 'description'
            },
            {
                'name': 'ip_range'
            },
        ]
    },
    '/v2/vpcs/{vpc_id}-DELETE': {
        'parameters': [
            {
                'name': 'vpc_id'
            },
        ]
    },
    '/v2/vpcs/{vpc_id}-GET': {
        'parameters': [
            {
                'name': 'vpc_id'
            },
        ]
    },
    '/v2/vpcs-GET': {
        'parameters': [
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/vpcs/{vpc_id}/members-GET': {
        'parameters': [
            {
                'name': 'vpc_id'
            },
            {
                'name': 'resource_type'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/v2/vpcs/{vpc_id}-PATCH': {
        'parameters': [
            {
                'name': 'vpc_id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'name'
            },
            {
                'name': 'default'
            },
        ]
    },
    '/v2/vpcs/{vpc_id}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'vpc_id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'default'
            },
        ]
    },
};