from digital_ocean_python_sdk.paths.v2_projects_project_id.get import ApiForget
from digital_ocean_python_sdk.paths.v2_projects_project_id.put import ApiForput
from digital_ocean_python_sdk.paths.v2_projects_project_id.delete import ApiFordelete
from digital_ocean_python_sdk.paths.v2_projects_project_id.patch import ApiForpatch


class V2ProjectsProjectId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
