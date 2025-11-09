# photo-metadata

Python library to extract, read, modify, and write photo and video metadata (EXIF, IPTC, XMP) using ExifTool. Supports JPEG, RAW, and video files. 


---

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/photo-metadata?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/photo-metadata)  

---
  

> 📕 [README_Japanese](https://github.com/kingyo1205/photo-metadata/blob/main/README_Japanese.md)



---

# Photo Metadata

`photo-metadata` is a Python library for extracting, manipulating, and writing metadata from photo and video files. It uses ExifTool as a backend and supports a wide range of image and video formats. Full support for Japanese tags is also provided.

## Key Features

* Extract metadata from photos and videos
* Read, write, and delete metadata
* Convenient methods for various metadata operations
* Compare two `Metadata` objects
* Filter multiple files by metadata
* Rename multiple files based on capture date or other metadata

---

## Supported OS

- **Windows**
- **Linux**

---

## Installation

```bash
pip install photo-metadata
```

## Dependencies

- [ExifTool] (needs to be installed separately; either add to PATH or provide full path)
- [tqdm] (automatically installed via pip; used for progress display)
- [charset-normalizer] (automatically installed via pip; used for encoding detection)

---

## Configuring ExifTool

```python
import photo_metadata

# Set the path to ExifTool
photo_metadata.set_exiftool_path(exiftool_path)
```

### Notes

The default `exiftool_path` is `"exiftool"`. If ExifTool is already in your PATH, calling `set_exiftool_path` is not required.

---

## Metadata Class

The `Metadata` class is the core class for working with metadata.

```python
from photo_metadata import Metadata
```

### Initialization

```python
metadata = Metadata(file_path="path/to/your/image.jpg")
```

* `file_path` (str): Path to the image file

### Accessing Metadata

Metadata can be accessed like a dictionary.

**Access using English tags:**

```python
date_time = metadata["EXIF:DateTimeOriginal"]
print(date_time)
```

**Access using Japanese tags:**

```python
date_time = metadata[photo_metadata.key_ja_to_en("EXIF:撮影日時")]
print(date_time)
```

### Modifying Metadata

You can modify metadata like a dictionary:

```python
metadata["EXIF:DateTimeOriginal"] = "2024:02:17 12:34:56"
```

### Writing Metadata to File

```python
metadata.write_metadata_to_file()
```

### Deleting Metadata

Metadata can be deleted using the `del` statement:

```python
del metadata["EXIF:DateTimeOriginal"]
```

### Comparison

Two `Metadata` objects can be compared using `==` and `!=`:

```python
metadata1 = Metadata("image1.jpg")
metadata2 = Metadata("image2.jpg")

if metadata1 == metadata2:
    print("Metadata is identical")
else:
    print("Metadata is different")
```

---

## Working with Multiple Files – MetadataBatchProcess Class

`MetadataBatchProcess` allows you to process metadata for multiple files.

```python
from photo_metadata import MetadataBatchProcess
```

### Initialization

```python
mbp = MetadataBatchProcess(file_path_list)
```

### Filter Files by Metadata

```python
mbp.filter_by_metadata(
    keyword_list=["NEX-5R", 2012],
    exact_match=True,
    all_keys_match=True,
    search_by="value"
)

for file, md in mbp.metadata_objects.items():
    print(f"{os.path.basename(file)}")
```

This example keeps files whose metadata values include both `"NEX-5R"` and `2012`.

### Filter Using Custom Conditions

```python
mbp.filter_by_custom_condition(
    lambda md: md[photo_metadata.key_ja_to_en("EXIF:F値")] >= 4.0
    and md[photo_metadata.key_ja_to_en("EXIF:モデル")] == 'NEX-5R'
)

for file, md in mbp.metadata_objects.items():
    print(f"{os.path.basename(file)}")
```

This example keeps files where the EXIF F-number is ≥ 4.0 and the camera model is `'NEX-5R'`.

### Rename Files Using Metadata

```python
import os
from tkinter import filedialog
from photo_metadata import MetadataBatchProcess, Metadata

def date(md: Metadata):
    date = md.get_date('%Y-%m-%d_%H.%M.%S', default_time_zone="+00:00")
    if date == md.error_string:
        raise Exception("Not Found")
    return f"{date}-{MetadataBatchProcess.DUP_SEQ_1_DIGIT}"  # This is a duplicate sequence. It increments if duplicates exist, starting from 0. Must be included in the format.

file_path_list = list(map(os.path.normpath, filedialog.askopenfilenames()))
mbp = MetadataBatchProcess(file_path_list)

# Prepare rename creates new_name_dict for preview
mbp.prepare_rename(format_func=date)

print("new_name_dict")
for file, new_name in mbp.new_name_dict.items():
    print(f"{file}\n{new_name}")

print("\nerror_dist")
for file, new_name in mbp.error_files.items():
    print(f"{file}\n{new_name}")

input("Press Enter to rename files")

mbp.rename_files()
```

---

## API Reference

### photo_metadata

* `get_key_map() -> dict`: Returns a dictionary for Japanese key conversion.
* `set_exiftool_path(exiftool_path: str | Path) -> None`: Sets the path to exiftool.
* `get_exiftool_path() -> Path`: Returns the configured path to exiftool.
* `set_jp_tags_json_path(jp_tags_json_path: str | Path) -> None`: Sets the path to the Japanese tags JSON file.
* `get_jp_tags_json_path() -> Path`: Returns the configured path to the Japanese tags JSON file.
* `key_en_to_ja(key_en: str) -> str`: Converts an English key to its Japanese equivalent.
* `key_ja_to_en(key_ja: str) -> str`: Converts a Japanese key to its English equivalent.

### photo_metadata.Metadata

* `__init__(self, file_path: str | Path)`: Constructor.

* `display_japanese(self, return_type: Literal["str", "print", "dict"] = "print") -> str`: Displays metadata using Japanese keys.

* `write_metadata_to_file(self, file_path: str = None) -> None`: Writes metadata to a file.

* `get_metadata_dict(self) -> dict`: Returns the metadata as a dictionary.

* `export_metadata(self, output_path: str = None, format: Literal["json", "csv"] = 'json', lang_ja_metadata: bool = False) -> None`: Exports metadata to a file.

* `keys(self) -> list[str]`: Returns a list of metadata keys.

* `values(self) -> list[Any]`: Returns a list of metadata values.

* `items(self) -> list[tuple[str, Any]]`: Returns a list of key-value pairs for metadata.

* `get_gps_coordinates(self) -> str`: Returns GPS coordinates.

* `export_gps_to_google_maps(self) -> str`: Converts GPS information to a Google Maps URL.

* `get_date(self, format: str = '%Y:%m:%d %H:%M:%S', default_time_zone: str = '+00:00') -> str`: Returns the capture date (customizable date format).

* `get_image_dimensions(self) -> str`: Returns image dimensions.

* `get_file_size(self) -> tuple[str, int]`: Returns the file size.

* `get_model_name(self) -> str`: Returns the camera model name.

* `get_lens_name(self) -> str`: Returns the lens name.

* `get_focal_length(self) -> dict`: Returns focal length information.

* `show(self) -> None`: Displays the file.

* `get_main_metadata(self) -> dict`: Returns major metadata fields.

* `contains_key(self, key, exact_match: bool = True)`: Checks whether the specified key exists.

* `contains_value(self, value, exact_match: bool = True)`: Checks whether the specified value exists.

* `copy(self) -> "Metadata"`: Copies the instance of the Metadata class.

* `@classmethod def load_all_metadata(cls, file_path_list: list[str], progress_func: Callable[[int], None] | None = None, max_workers: int = 40) -> dict[str, "Metadata"]`: Efficiently loads metadata from multiple files in parallel.

### photo_metadata.MetadataBatchProcess

* `__init__(self, file_list: list[str], progress_func: Callable[[int], None] | None = None, max_workers: int = 40)`: Constructor.
* `filter_by_custom_condition(self, condition_func: Callable[[Metadata], bool]) -> None`: Filters metadata using a custom condition function.
* `filter_by_metadata(self, keyword_list: list[str], exact_match: bool, all_keys_match: bool, search_by: Literal["either", "value", "key"]) -> None`: Finds files containing specific values, keys, or either in their metadata.
* `prepare_rename(self, format_func: Callable[[Metadata], str]) -> None`: Prepares files for renaming.
* `rename_files(self) -> str`: Renames the files.
* `copy(self) -> "MetadataBatchProcess"`: Copies the instance of the MetadataBatchProcess class.


---

### If you find this library useful, please consider giving it a ⭐ on GitHub!

---

## URLs

* PyPI: `https://pypi.org/project/photo-metadata/`
* GitHub: `https://github.com/kingyo1205/photo-metadata`

---

## Notes

ExifTool is required. This library uses [ExifTool](https://exiftool.org/) as an external command to process image and video metadata.

---

## About AI-assisted Code Generation

Some parts of the code in this repository were generated or assisted by AI tools such as ChatGPT and Gemini CLI.
No generated content that cannot be used in open-source projects like LMArena is included.

---

## Required Software

ExifTool must be installed on your system. Download it from the [official website](https://exiftool.org/).

---

## License

This library is distributed under the MIT License.  
However, ExifTool itself is distributed under the [Artistic License 2.0](https://dev.perl.org/licenses/artistic.html).  
If you use ExifTool, please make sure to comply with its license terms.

### Dependencies and Licenses

(Verified in 2025 / Based on information listed on PyPI)

| Library                                                            | License |
| -----------------------------------------------------------------  | -------- |
| [charset_normalizer](https://pypi.org/project/charset-normalizer/) | MIT      |
| [tqdm](https://pypi.org/project/tqdm/)                             | MIT      |

---




