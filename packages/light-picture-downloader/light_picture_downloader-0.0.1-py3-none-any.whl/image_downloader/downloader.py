import requests
import shutil
import wget
from Exceptions import FileRetrievalException, FileTypeError

destination_folder = "./pictures"

accepted_extensions = ['jpeg', 'jpg', 'png']


def download_picture(pic_url: str, check_for_file_extension=True):
    filename = pic_url.split('/')[-1]

    is_image = False
    if check_for_file_extension:
        for i in accepted_extensions:
            if str.__contains__(filename, i):
                is_image = True
                break
    print(f"ExtensionCheck: {check_for_file_extension}")
    if is_image or not check_for_file_extension:
        req = requests.get(pic_url, stream=True)

        if req.status_code == 200:

            req.raw.decode_content = True

            with open(f"{destination_folder}/{filename}", 'wb') as file:
                shutil.copyfileobj(req.raw, file)

            return filename
        else:
            raise FileRetrievalException(f"Request unsuccessful, {pic_url} responded with code {req.status_code}")
    else:
        raise FileTypeError(
            f"The url {pic_url} does not contain a reference to the image file type or the present extension is not included among the accepted extensions")


def download_picture_as(pic_url: str, filename: str, check_for_file_extension=True, extension=None):
    file = pic_url.split('/')[-1]

    is_image = False

    if check_for_file_extension:
        for i in ['jpeg', 'jpg', 'png']:
            if str.__contains__(file, i):
                is_image = True
                break

    if not isinstance(extension, str):
        print("looking for extension")
        if "." in file:
            print("found")
            extension = file.split(".")[-1]
            print(extension)

    if is_image or not check_for_file_extension:
        req = requests.get(pic_url, stream=True)

        if req.status_code == 200:

            req.raw.decode_content = True

            if isinstance(extension, str):
                with open(f"{destination_folder}/{filename}.{extension}", 'wb') as file:
                    shutil.copyfileobj(req.raw, file)
                return f"{filename}.{extension}"
            else:
                with open(f"{destination_folder}/{filename}", 'wb') as file:
                    shutil.copyfileobj(req.raw, file)
                return f"{filename}"
        else:
            raise FileRetrievalException(f"Request unsuccessful, {pic_url} responded with code {req.status_code}")
    else:
        raise FileTypeError(
            f"The url {pic_url} does not contain a reference to the image file type or the present extension is not included among the accepted extensions")


def download_data_from_url(content_url):
    # Use wget download method to download specified url.
    filename = wget.download(content_url)

    print('Successfully Downloaded: ', filename)


def add_accepted_extension(extension: str):
    if extension not in accepted_extensions:
        accepted_extensions.append(extension)


def reset_accepted_extensions():
    accepted_extensions = ['jpeg', 'jpg', 'png']


if __name__ == "__main__":
    print(download_picture_as("https://images.freeimages.com/images/large-previews/8b1/cat-1525070.jpg", "cat"))
