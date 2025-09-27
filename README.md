# photo-metadata
  
> 🗒️ このREADMEは **日本語と英語の両方** を含みます。
> 📄 **This README includes both English and Japanese versions.**  
> 📘 **English** section is available below: [Go to English version](#photo-metadata-readme-english)  
> 📕 **日本語** セクションはこちらからどうぞ: [日本語版へ移動](#photo-metadata-readme-日本語版)

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/photo-metadata?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/photo-metadata)

# Photo Metadata README (English)

---

`photo-metadata` is a Python library for extracting, manipulating, and writing metadata from photo and video files. It uses ExifTool as a backend and supports a wide range of image and video formats. Full support for Japanese tags is also provided.

## Key Features

* Extract metadata from photos and videos
* Read, write, and delete metadata
* Convenient methods for various metadata operations
* Compare two `Metadata` objects
* Filter multiple files by metadata
* Rename multiple files based on capture date or other metadata

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
    date = md.get_date('%Y年%m月%d日-%H.%M.%S')
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

### photo\_metadata Module

* `get_key_map() -> dict`: Returns the dictionary for Japanese tag conversion
* `set_exiftool_path(exiftool_path: str | Path) -> None`: Set the path to ExifTool
* `get_exiftool_path() -> Path`: Get the current ExifTool path
* `set_jp_tags_json_path(jp_tags_json_path: str | Path) -> None`: Set the path to the Japanese tags JSON file
* `get_jp_tags_json_path() -> Path`: Get the path to the Japanese tags JSON file
* `key_en_to_ja(key_en: str) -> str`: Convert English key to Japanese
* `key_ja_to_en(key_ja: str) -> str`: Convert Japanese key to English

### Metadata Class

* `__init__(self, file_path: str | Path)`
* `display_japanese(self, return_type: Literal["str", "print", "dict"] = "print") -> str`
* `write_metadata_to_file(self, file_path: str = None) -> None`
* `get_metadata_dict(self) -> dict`
* `export_metadata(self, output_path: str = None, format: Literal["json", "csv"] = 'json', lang_ja_metadata: bool = False) -> None`
* `keys(self) -> list[str]`
* `values(self) -> list[Any]`
* `items(self) -> list[tuple[str, Any]]`
* `get_gps_coordinates(self) -> str`
* `export_gps_to_google_maps(self) -> str`
* `get_date(self, format: str = '%Y:%m:%d %H:%M:%S', default_time_zone: str = '+09:00') -> str`
* `get_image_dimensions(self) -> str`
* `get_file_size(self) -> tuple[str, int]`
* `get_model_name(self) -> str`
* `get_lens_name(self) -> str`
* `get_focal_length(self) -> dict`
* `show(self) -> None`
* `get_main_metadata(self) -> dict`
* `contains_key(self, key, exact_match: bool = True)`
* `contains_value(self, value, exact_match: bool = True)`
* `copy(self) -> "Metadata"`
* `@classmethod load_all_metadata(...) -> dict[str, "Metadata"]`

### MetadataBatchProcess Class

* `__init__(self, file_list: list[str], progress_func: Callable[[int], None] | None = None, max_workers: int = 40)`
* `filter_by_custom_condition(self, condition_func: Callable[[Metadata], bool]) -> None`
* `filter_by_metadata(self, keyword_list: list[str], exact_match: bool, all_keys_match: bool, search_by: Literal["either", "value", "key"]) -> None`
* `prepare_rename(self, format_func: Callable[[Metadata], str]) -> None`
* `rename_files(self) -> str`
* `copy(self) -> "MetadataBatchProcess"`

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

## Required Software

ExifTool must be installed on your system. Download it from the [official website](https://exiftool.org/).

---

## License

This library is distributed under the MIT License. ExifTool itself is distributed under the [Artistic License 2.0](https://dev.perl.org/licenses/artistic.html). Please comply with the license when using ExifTool.


- The following third-party libraries are used:  
  - charset_normalizer (MIT License)  
    - https://github.com/jawah/charset_normalizer?tab=MIT-1-ov-file  
  - tqdm (MIT License)  
    - https://github.com/tqdm/tqdm?tab=License-1-ov-file  

- Since version 0.2.3, the dependency has been changed from **chardet** (LGPL v2.1) to **charset-normalizer** (MIT).


# Photo Metadata README 日本語版


---


`photo-metadata`は、写真や動画ファイルからメタデータを抽出、操作、書き込みを行うためのPythonライブラリです。exiftoolをバックエンドで使用し、幅広い画像、動画フォーマットに対応しています。日本語タグのサポートも特徴です。

## 主な機能

- 写真や動画ファイルのメタデータの抽出
- メタデータの読み取り、書き込み、削除
- さまざまなメタデータ操作のための便利なメソッド
- 2つのMetadataオブジェクトの比較
- 複数のファイルをメタデータでフィルター
- 複数のファイルを撮影日時などでリネーム

## インストール


`pip install photo-metadata`

## 依存関係

- [exiftool] (別途インストールが必要です。　パスを通すかフルパスを指定してください)
- [tqdm] (pipで自動でインストールされます。進捗表示用です)
- [charset-normalizer] (pipで自動でインストールされます。 エンコーディング解析用です)



## exiftoolを設定

```python
import photo_metadata

# exiftoolのパスを設定
photo_metadata.set_exiftool_path(exiftool_path)
```

### exiftool_pathのデフォルトは"exiftool"です。　パスが通っている場合は　set_exiftool_path　を実行する必要はありません。

## Metadataクラス

`Metadata`クラスは、メタデータ操作の中心となるクラスです。
```python
from photo_metadata import Metadata
```

### 初期化
```python
metadata = Metadata(file_path="path/to/your/image.jpg")
```
- `file_path` (str): 画像ファイルのパス



### メタデータの取得

メタデータは、辞書のようにアクセスできます。

英語のタグでアクセス
```python
date_time = metadata["EXIF:DateTimeOriginal"]
print(date_time)
```

日本語のタグでアクセス
```python
date_time = metadata[photo_metadata.key_ja_to_en("EXIF:撮影日時")]
print(date_time)
```

### メタデータの変更

メタデータは、辞書のように変更できます。
```python
metadata["EXIF:DateTimeOriginal"] = "2024:02:17 12:34:56"
```

### メタデータの書き込み - 変更をファイルに書き込む


```python
metadata.write_metadata_to_file()
```

### メタデータの削除

メタデータは、`del`ステートメントで削除できます。
```python
del metadata["EXIF:DateTimeOriginal"]
```


### 比較

`==`と`!=`演算子を使用して、2つの`Metadata`オブジェクトを比較できます。
```python
metadata1 = Metadata("image1.jpg")
metadata2 = Metadata("image2.jpg")

if metadata1 == metadata2:
    print("メタデータは同じです")
else:
    print("メタデータは異なります")
```

## 複数のファイルのメタデータを扱う。- MetadataBatchProcessクラス
`MetadataBatchProcess`は複数ファイルのメタデータを処理するためのクラスです。

```python
from photo_metadata import MetadataBatchProcess
```

### 初期化
```python
mbp = MetadataBatchProcess(file_path_list)
```

### __init__メソッド
```python
def __init__(self, file_list: list[str], 
                 progress_func: Callable[[int], None] | None = None, 
                 max_workers: int = 40):
```

### メタデータに特定の値またはキーまたはキーと値どちらかに存在するファイルを見つける
```python
mbp.filter_by_metadata(keyword_list=["NEX-5R", 2012],
                             exact_match=True,
                             all_keys_match=True,
                             search_by="value")


for file, md in mbp.metadata_objects.items():
    
    print(f"{os.path.basename(file)}")
```

この場合はメタデータの値に"NEX-5R", 2012が両方とも、存在したファイルが残る


### メタデータを検証
```python
mbp.filter_by_custom_condition(lambda md: md[photo_metadata.key_ja_to_en("EXIF:F値")] >= 4.0 and md[photo_metadata.key_ja_to_en("EXIF:モデル")] == 'NEX-5R')

for file, md in mbp.metadata_objects.items():
    print(f"{os.path.basename(file)}")
```

この場合はメタデータのEXIF:F値が4.0以上かつ、EXIF:モデルが'NEX-5R'のファイルが残る


### メタデータでリネーム

```python
import os
from tkinter import filedialog

from photo_metadata import MetadataBatchProcess, Metadata


def date(md: Metadata):
    date = md.get_date('%Y年%m月%d日-%H.%M.%S')
    if date == md.error_string:
        raise Exception("Not Found")
    return f"{date}-{MetadataBatchProcess.DUP_SEQ_1_DIGIT}" これは重複連番です。重複したときに数字が増えます。基本は0になります。フォーマットに必ず含めてください。

file_path_list = list(map(os.path.normpath, filedialog.askopenfilenames()))
mbp = MetadataBatchProcess(file_path_list)

# prepare_rename を実行すると new_name_dict が作成され、
# ファイル名のリネームプレビューが可能になります。
mbp.prepare_rename(format_func=date)

print("new_name_dict")
for file, new_name in mbp.new_name_dict.items():
    print(f"{file}\n{new_name}")

print("\nerror_dist")
for file, new_name in mbp.error_files.items():
    print(f"{file}\n{new_name}")

input("リネームするなら enter キーを押してください")

mbp.rename_files()

```

この場合は日付でリネームします。
photo_metadata.MetadataBatchProcess.DUP_SEQ_1_DIGIT これは重複連番です。重複したときに数字が増えます。基本は0になります。フォーマットに必ず含めてください。

```python
if date == md.error_string:
    raise Exception("Not Found")
```
日付が取得できない際はエラーを出してください。








---






## APIリファレンス


### photo_metadata


- `get_key_map() -> dict`: 日本語キー変換用の辞書を取得できます
- `set_exiftool_path(exiftool_path: str | Path) -> None`: exiftoolのパスを設定できます
- `get_exiftool_path() -> Path`: 設定されたexiftoolのパスを取得できます
- `set_jp_tags_json_path(jp_tags_json_path: str | Path) -> None`: 日本語タグのJSONファイルのパスを設定できます
- `get_jp_tags_json_path() -> Path`: 設定された日本語タグのJSONファイルのパスを取得できます`
- `key_en_to_ja(key_en: str) -> str`: 英語のキーを日本語に変換します
- `key_ja_to_en(key_ja: str) -> str`: 日本語のキーを英語に変換します


### photo_metadata.Metadata

- `__init__(self, file_path: str | Path)`: コンストラクタ


- `display_japanese(self, return_type: Literal["str", "print", "dict"] = "print") -> str`: メタデータを日本語のキーで表示できます
- `write_metadata_to_file(self, file_path: str = None) -> None`: メタデータをファイルに書き込む
- `get_metadata_dict(self) -> dict`: メタデータの辞書を取得します
- `export_metadata(self, output_path: str = None, format: Literal["json", "csv"] = 'json', lang_ja_metadata: bool = False) -> None`: メタデータをファイルにエクスポート
- `keys(self) -> list[str]`: メタデータのキーのリストを取得します
- `values(self) -> list[Any]`: メタデータの値のリストを取得します
- `items(self) -> list[tuple[str, Any]]`: メタデータのキーと値のペアのリストを取得します
- `get_gps_coordinates(self) -> str`: GPS座標を取得
- `export_gps_to_google_maps(self) -> str`: GPS情報をGoogleマップのURLに変換
- `get_date(self, format: str = '%Y:%m:%d %H:%M:%S', default_time_zone: str = '+09:00') -> str`: 撮影日時を取得 (日付フォーマットを指定できます)
- `get_image_dimensions(self) -> str`: 画像の寸法を取得
- `get_file_size(self) -> tuple[str, int]`: ファイルサイズを取得
- `get_model_name(self) -> str`: カメラの機種名を取得
- `get_lens_name(self) -> str`: レンズ名を取得
- `get_focal_length(self) -> dict`: 焦点距離を取得
- `show(self) -> None`: ファイルを表示
- `get_main_metadata(self) -> dict`: 主要なメタデータを取得
- `contains_key(self, key, exact_match: bool = True)`: キーが存在するか確認します
- `contains_value(self, value, exact_match: bool = True)`: 値が存在するか確認します
- `copy(self) -> "Metadata"`: Metadataクラスのインスタンスをコピーします
- `@classmethod def load_all_metadata(cls, file_path_list: list[str], progress_func: Callable[[int], None] | None = None, max_workers: int = 40) -> dict[str, "Metadata"]`: 複数のファイルのメタデータを並列処理で高速に取得します。


### photo_metadata.MetadataBatchProcess

- `__init__(self, file_list: list[str], progress_func: Callable[[int], None] | None = None, max_workers: int = 40)`: コンストラクタ
- `filter_by_custom_condition(self, condition_func: Callable[[Metadata], bool]) -> None`: メタデータを任意の関数 (条件) でフィルターします
- `filter_by_metadata(self, keyword_list: list[str], exact_match: bool, all_keys_match: bool, search_by: Literal["either", "value", "key"]) -> None`: メタデータに特定の値またはキーまたはキーと値どちらかに存在するファイルを見つける
- `prepare_rename(self, format_func: Callable[[Metadata], str]) -> None`: リネームの準備をします
- `rename_files(self) -> str`: ファイルをリネームします
- `copy(self) -> "MetadataBatchProcess"`: MetadataBatchProcessクラスのインスタンスをコピーします


---

### このライブラリが気に入ったら、ぜひGitHubで⭐をお願いします！

---




## URL

### pypi
`https://pypi.org/project/photo-metadata/`

### github
`https://github.com/kingyo1205/photo-metadata`

## 注意点

exiftoolが必ず必要です。

このライブラリは、画像やメタデータを処理する際に[ExifTool](https://exiftool.org/)を外部コマンドとして使用しています。

## 必要なソフトウェア

このライブラリを使用するには、ExifToolがシステムにインストールされている必要があります。ExifToolは[公式サイト](https://exiftool.org/)からダウンロードしてインストールしてください。

## ライセンス

このライブラリはMITライセンスの下で配布されています。ただし、ExifTool自体は[Artistic License 2.0](https://dev.perl.org/licenses/artistic.html)の下で配布されています。ExifToolを利用する場合は、そのライセンス条件を遵守してください。

- 以下のサードパーティライブラリを利用しています:  
  - charset_normalizer (MIT License)
    - https://github.com/jawah/charset_normalizer?tab=MIT-1-ov-file
  - tqdm (MIT License)  
    - https://github.com/tqdm/tqdm?tab=License-1-ov-file
- バージョン0.2.3から依存ライブラリを chardet (LGPL v2.1) から charset-normalizer (MIT) に変更
---





