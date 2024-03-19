from digital_ocean_python_sdk.paths.v2_registry.get import ApiForget
from digital_ocean_python_sdk.paths.v2_registry.post import ApiForpost
from digital_ocean_python_sdk.paths.v2_registry.delete import ApiFordelete


class V2Registry(
    ApiForget,
    ApiForpost,
    ApiFordelete,
):
    pass
