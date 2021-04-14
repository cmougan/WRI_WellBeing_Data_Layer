from dssg.dataio.azure_blob_downloader import *


def main():
    azure_blob_file_downloader = AzureBlobFileDownloader()
    azure_blob_file_downloader.download_all_blobs_in_container()


if __name__ == "__main__":
    main()
