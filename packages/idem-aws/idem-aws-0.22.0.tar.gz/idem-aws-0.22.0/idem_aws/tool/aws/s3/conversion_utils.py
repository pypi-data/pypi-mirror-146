import json
from typing import Any
from typing import Dict


def convert_raw_bucket_notification_to_present(
    hub, raw_resource: Dict[str, Any], bucket_name: str
) -> Dict[str, Any]:
    """
    Convert the s3 bucket notification configurations response to a common format

    Args:
        raw_resource: List of s3 bucket notification configurations
        bucket_name: Name of the bucket on which notification needs to be configured.

    Returns:
        A dictionary of s3 bucket notification configurations
    """
    translated_resource = {}
    raw_resource.pop("ResponseMetadata", None)

    if raw_resource:
        translated_resource["name"] = bucket_name
        translated_resource["resource_id"] = bucket_name + "-notifications"
        translated_resource["notifications"] = raw_resource
    return translated_resource


def convert_raw_public_access_block_to_present(
    hub, bucket_name: str, public_access_block_configuration: Dict
) -> Dict[str, Any]:

    translated_resource = {
        "name": f"{bucket_name}-public-access-block",
        "bucket": bucket_name,
        "public_access_block_configuration": json.loads(
            json.dumps(public_access_block_configuration)
        ),
        "resource_id": bucket_name,
    }
    return translated_resource
