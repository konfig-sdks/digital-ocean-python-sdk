from digital_ocean_python_sdk.paths.v2_kubernetes_registry.post import ApiForpost
from digital_ocean_python_sdk.paths.v2_kubernetes_registry.delete import ApiFordelete


class V2KubernetesRegistry(
    ApiForpost,
    ApiFordelete,
):
    pass
