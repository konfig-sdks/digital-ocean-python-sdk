from digital_ocean_python_sdk.paths.v2_droplets.get import ApiForget
from digital_ocean_python_sdk.paths.v2_droplets.post import ApiForpost
from digital_ocean_python_sdk.paths.v2_droplets.delete import ApiFordelete


class V2Droplets(
    ApiForget,
    ApiForpost,
    ApiFordelete,
):
    pass
