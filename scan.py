from PIL import Image
import imagehash
import fire
from pathlib import Path
import logging
import os
logging.basicConfig(level=logging.INFO)


image_extensions = ["jpg", "png"]

def scan(root_scan_dir, trash_dir):
    logging.info("Start scan")

    image_hash_map = {}

    root_dir = Path(root_scan_dir)
    trash_dir = Path(trash_dir)
    image_list = _list_files(root_dir, image_extensions)

    logging.info("Found {} images".format(len(image_list)))
    for image_path in image_list:
        hash = _get_image_hash(image_path)
        if not hash:
            logging.info("Hash error: {}".format(image_path))
            os.rename(image_path, trash_dir / image_path.name)
        if hash not in image_hash_map:
            image_hash_map[hash] = image_path
        else:
            logging.info("Duplicate found: {}".format(image_path))
            try:
                os.rename(image_path, trash_dir / image_path.name)
            except OSError as ex:
                logging.error("Unable to move image: {}: {}".format(image_path, ex))


def count_images(root_scan_dir):
    root_dir = Path(root_scan_dir)
    image_list = _list_files(root_dir, image_extensions)
    logging.info("Found {} images".format(len(image_list)))


def _get_image_hash(image_path):
    try:
        hash = imagehash.average_hash(Image.open(image_path))
        return hash
    except:
        return None
    

def _list_files(root_dir: Path, extensions: list):
    result = []
    for e in extensions:
        for img_path in root_dir.glob('**/*.{}'.format(e)):
            result.append(img_path)
            logging.debug(img_path.name)
    return result


if __name__ == '__main__':
    fire.Fire({
        'scan': scan,
        'count': count_images,
    })
