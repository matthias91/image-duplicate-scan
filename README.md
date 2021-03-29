# Image duplicate scan
Scans a directory recursivly for duplicate images and moves the duplicates to a trash directory.

For comparing two images the function `average_hash()` for the package [imagehash](https://pypi.org/project/ImageHash/) is used.


## Usage
```
python scan.py scan --root_scan_dir=test/img --trash_dir=test/trash
```