from digital_ocean_python_sdk.paths.v2_apps_id.get import ApiForget
from digital_ocean_python_sdk.paths.v2_apps_id.put import ApiForput
from digital_ocean_python_sdk.paths.v2_apps_id.delete import ApiFordelete


class V2AppsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
