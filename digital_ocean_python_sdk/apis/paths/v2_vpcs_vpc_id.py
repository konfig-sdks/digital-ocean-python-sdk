from digital_ocean_python_sdk.paths.v2_vpcs_vpc_id.get import ApiForget
from digital_ocean_python_sdk.paths.v2_vpcs_vpc_id.put import ApiForput
from digital_ocean_python_sdk.paths.v2_vpcs_vpc_id.delete import ApiFordelete
from digital_ocean_python_sdk.paths.v2_vpcs_vpc_id.patch import ApiForpatch


class V2VpcsVpcId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
