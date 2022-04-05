from constructs import Construct
from serverless_secure_file_sharing.resources.tables import Tables
from serverless_secure_file_sharing.utils import LambdaFunction
from serverless_secure_file_sharing.resources.file_sharing_cdn import FileSharingCDN
from serverless_secure_file_sharing.resources.api import RestAPI
from serverless_secure_file_sharing.resources.lambda_layers import LambdaLayers

class UserFunctions(object):
    def __init__(
        self,
        scope: Construct,
        file_sharing_cdn: FileSharingCDN,
        api: RestAPI,
        lambda_layers: LambdaLayers,
        tables: Tables
    ):
        lambda_env = {
            "CDN_BUCKET": file_sharing_cdn.bucket.bucket_name,
            "INVENTORY_TABLE": tables.inventory.table_name
        }


        # GENERATE PRESIGNED UPLOAD URL #
        generate_presigned_upload_url_fn = LambdaFunction(
            scope,
            "GeneratePresignedUploadUrlLambda",
            "generate-presigned-upload-url",
            path="src/user/",
            handler="generate_presigned_upload_url.lambda_handler",
            api_arn=api.api_arn,
            env=lambda_env,
            layers=[lambda_layers.base],
        )
        tables.inventory.grant_read_write_data(generate_presigned_upload_url_fn.function)
        file_sharing_cdn.bucket.grant_put(generate_presigned_upload_url_fn.function)
        file_sharing_cdn.bucket.grant_put_acl(generate_presigned_upload_url_fn.function)


        # GENERATE PRESIGNED DOWNLOAD URL #
        generate_presigned_download_url_fn = LambdaFunction(
            scope,
            "GeneratePresignedDownloadUrlLambda",
            "generate-presigned-download-url",
            path="src/user/",
            handler="generate_presigned_download_url.lambda_handler",
            api_arn=api.api_arn,
            env=lambda_env,
            layers=[lambda_layers.base],
        )
        tables.inventory.grant_read_write_data(generate_presigned_download_url_fn.function)
        file_sharing_cdn.bucket.grant_put(generate_presigned_download_url_fn.function)
        file_sharing_cdn.bucket.grant_read(generate_presigned_download_url_fn.function)


        # DELETE FILE #
        delete_file_fn = LambdaFunction(
            scope,
            "DeleteFileLambda",
            "delete-file",
            path="src/user/",
            handler="delete_file.lambda_handler",
            api_arn=api.api_arn,
            env=lambda_env,
            layers=[lambda_layers.base],
        )
        file_sharing_cdn.bucket.grant_delete(delete_file_fn.function)
        tables.inventory.grant_read_write_data(delete_file_fn.function)