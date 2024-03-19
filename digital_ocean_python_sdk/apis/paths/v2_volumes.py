from digital_ocean_python_sdk.paths.v2_volumes.get import ApiForget
from digital_ocean_python_sdk.paths.v2_volumes.post import ApiForpost
from digital_ocean_python_sdk.paths.v2_volumes.delete import ApiFordelete


class V2Volumes(
    ApiForget,
    ApiForpost,
    ApiFordelete,
):
    pass
