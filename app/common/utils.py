import os
import requests


def download_image(image_url, save_dir='images'):
    """
    Download image and save locally
    :param image_url:
    :param save_dir:
    :return:
    """
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        image_name = os.path.basename(image_url)
        image_path = os.path.join(save_dir, image_name)

        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        with open(image_path, 'wb') as image_file:
            for chunk in response.iter_content(chunk_size=8192):
                image_file.write(chunk)

        return image_path

    except requests.RequestException as e:
        print(f"error downloading image: {e}")
        return None
