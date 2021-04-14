import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from multiprocessing.pool import ThreadPool
load_dotenv()

# # Create client from url providing anonymous public read access.
# service = BlobServiceClient(account_url=os.environ.get("AZURE_URL"))

# block_blob_service = BlockBlobService(account_url=os.environ.get("AZURE_URL"))
# generator = block_blob_service.list_blobs("tif-images")

# zf = zipfile.ZipFile("tif-images" + '.zip', mode='w',
#                      compression=zipfile.ZIP_DEFLATED)

# for blob in generator:
#     b = service.get_blob_to_bytes(container_name, )


class AzureBlobFileDownloader:
    def __init__(self):
        print("Initializing AzureBlobFileDownloader")

        # Initialize the connect to Azure storage account
        self.blob_service_client = BlobServiceClient(
            account_url=os.environ.get("AZURE_URL"))
        self.container = self.blob_service_client.get_container_client(
            os.environ.get("BLOB_CONTAINER"))

    def download_all_blobs_in_container(self):
        # get a list of blobs

        blobs = self.container.list_blobs()
        result = self.run(blobs)
        print(result)

    def run(self, blobs):
        # Download 10 files at a time!
        with ThreadPool(processes=int(10)) as pool:
            return pool.map(self.save_blob_locally, blobs)

    def save_blob_locally(self, blob):
        file_name = blob.name
        print(file_name)
        byts = self.container.get_blob_client(blob).download_blob().readall()

        # Get full path to the file
        download_file_path = os.path.join(
            os.environ.get("LOCAL_BLOB_PATH"), file_name)
        # for nested blobs, create local path as well
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

        with open(download_file_path, "wb") as file:
            file.write(byts)
        return file_name
