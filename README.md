# Photo Metadata
Python library to read and write photo and video metadata (EXIF, IPTC, XMP) using exiftool.

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/photo-metadata?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/photo-metadata)
  
> 🗒️ このREADMEは **日本語と英語の両方** を含みます。
> 📄 **This README includes both English and Japanese versions.**  
> 📘 **English** section is available below: [Go to English version](#photo-metadata-readme-english)  
> 📕 **日本語** セクションはこちらからどうぞ: [日本語版へ移動](#photo-metadata-readme-日本語版)



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
- [chardet] (pipで自動でインストールされます。 エンコーディング解析用です)

## 使い方

### Metadataクラス

`Metadata`クラスは、メタデータ操作の中心となるクラスです。
```python
from photo_metadata import Metadata
```

#### 初期化
```python
metadata = Metadata(file_path="path/to/your/image.jpg")
```
- `file_path` (str): 画像ファイルのパス



#### メタデータの取得

メタデータは、辞書のようにアクセスできます。

英語のタグでアクセス
```python
date_time = metadata["EXIF:DateTimeOriginal"]
print(date_time)
```

日本語のタグでアクセス
```python
date_time_jp = metadata[photo_metadata.key_ja_to_en("EXIF:レンズモデル")]
print(date_time_jp)
```

#### メタデータの変更

メタデータは、辞書のように変更できます。
```python
metadata["EXIF:DateTimeOriginal"] = "2024:02:17 12:34:56"

#### メタデータの書き込み
```
変更をファイルに書き込む

```python
metadata.write_metadata_to_file()
```

#### メタデータの削除

メタデータは、`del`ステートメントで削除できます。
```python
del metadata["EXIF:DateTimeOriginal"]
```

#### その他の関数やメソッド
- `get_key_map()`: 日本語キー変換用の辞書を取得できます
- `set_exiftool_path(exiftool_path: str | Path) -> None:`: exiftoolのパスを設定できます
- `get_exiftool_path() -> Path`: 設定されたexiftoolのパスを取得できます
- `set_jp_tags_json_path(jp_tags_json_path: str | Path) -> None:`: 日本語タグのJSONファイルのパスを設定できます
- `get_jp_tags_json_path() -> Path`: 設定された日本語タグのJSONファイルのパスを取得できます`
- `key_en_to_ja(key_en: str) -> str:`: 英語のキーを日本語に変換します
- `key_ja_to_en(key_ja: str) -> str:`: 日本語のキーを英語に変換します
- `display_japanese(self, return_type: Literal["str", "print", "dict"] = "print") -> str:`: メタデータを日本語のキーで表示できます
- `get_date(self, format: str = '%Y:%m:%d %H:%M:%S')`: 撮影日時を取得 (日付フォーマットを指定できます)
- `get_model_name(self)`: カメラの機種名を取得
- `get_lens_name(self)`: レンズ名を取得
- `get_focal_length(self)`: 焦点距離を取得
- `get_image_dimensions(self)`: 画像の寸法を取得
- `get_file_size(self)`: ファイルサイズを取得
- `get_gps_coordinates(self)`: GPS座標を取得
- `export_gps_to_google_maps(self)`: GPS情報をGoogleマップのURLに変換
- `write_metadata_to_file(self, file_path: str = None)`: メタデータをファイルに書き込む
- `export_metadata(self, output_path: str = None, format: Literal["json", "csv"] = 'json', lang_ja_metadata: bool = False):`: メタデータをファイルにエクスポート
- `show(self)`: ファイルを表示します
- `@classmethod def load_all_metadata(cls, file_path_list: list[str], progress_func: Callable[[int], None] | None = None, max_workers: int = 40) -> dict[str, "Metadata":`: 複数のファイルのメタデータを並列処理で高速に取得します。


exiftool_pathのデフォルトは"exiftool"です



#### 比較

`==`と`!=`演算子を使用して、2つの`Metadata`オブジェクトを比較できます。
```python
metadata1 = Metadata("image1.jpg")
metadata2 = Metadata("image2.jpg")

if metadata1 == metadata2:
    print("メタデータは同じです")
else:
    print("メタデータは異なります")
```


### MetadataBatchProcessクラス
`MetadataBatchProcess`は複数ファイルのメタデータを処理するためのクラスです。

```python
from photo_metadata import MetadataBatchProcess
```

#### 初期化
```python
mbp = MetadataBatchProcess(file_path_list)
```

##### __init__メソッド
```python
def __init__(self, file_list: list[str], 
                 progress_func: Callable[[int], None] | None = None, 
                 max_workers: int = 40):
```

#### メタデータに特定の値またはキーまたはキーと値どちらかに存在するファイルを見つける
```python
mbp.filter_by_metadata(keyword_list=["NEX-5R", 2012],
                             exact_match=True,
                             all_keys_match=True,
                             search_by="value")


for file, md in mbp.metadata_objects.items():
    
    print(f"{os.path.basename(file)}")
```

この場合はメタデータの値に"NEX-5R", 2012が両方とも、存在したファイルが残る


#### メタデータを検証
```python
mbp.filter_by_custom_condition(lambda md: md[photo_metadata.key_ja_to_en("EXIF:F値")] >= 4.0 and md[photo_metadata.key_ja_to_en("EXIF:モデル")] == 'NEX-5R')

for file, md in mbp.metadata_objects.items():
    print(f"{os.path.basename(file)}")
```

この場合はメタデータのEXIF:F値が4.0以上かつ、EXIF:モデルが'NEX-5R'のファイルが残る


#### メタデータでリネーム

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
mr = MetadataBatchProcess(file_path_list)

# prepare_rename を実行すると new_name_dict が作成され、
# ファイル名のリネームプレビューが可能になります。
mr.prepare_rename(format_func=date)

print("new_name_dict")
for file, new_name in mr.new_name_dict.items():
    print(f"{file}\n{new_name}")

print("\nerror_dist")
for file, new_name in mr.error_files.items():
    print(f"{file}\n{new_name}")

input("リネームするなら enter キーを押してください")

mr.rename_files()
```

この場合は日付でリネームします。
photo_metadata.MetadataBatchProcess.DUP_SEQ_1_DIGIT これは重複連番です。重複したときに数字が増えます。基本は0になります。フォーマットに必ず含めてください。

```python
if date == md.error_string:
    raise Exception("Not Found")
```
日付が取得できない際はエラーを出してください。








### エラー処理

ライブラリは、ファイルが見つからない場合や、無効な引数が提供された場合に例外を発生させます。

## URL

### pypi
`https://pypi.org/project/photo-metadata/`

### github
`https://github.com/kingyo1205/photo-metadata`

## 注意点

exiftoolが必ず必要です。


## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。



このライブラリは、画像やメタデータを処理する際に[ExifTool](https://exiftool.org/)を外部コマンドとして使用しています。

## 必要なソフトウェア

このライブラリを使用するには、ExifToolがシステムにインストールされている必要があります。ExifToolは[公式サイト](https://exiftool.org/)からダウンロードしてインストールしてください。

## ライセンス

このライブラリはMITライセンスの下で配布されています。ただし、ExifTool自体は[Artistic License 2.0](https://dev.perl.org/licenses/artistic.html)の下で配布されています。ExifToolを利用する場合は、そのライセンス条件を遵守してください。

## Photo Metadata README (English)


---

`photo-metadata` is a Python library for extracting, manipulating, and writing metadata from photo and video files.  
It uses `exiftool` as its backend, supporting a wide range of image and video formats.  
Support for **Japanese metadata tags** is one of its key features.

## Features

- Extract metadata from photo and video files
- Read, write, and delete metadata
- Handy methods for various metadata operations
- Compare two `Metadata` objects
- Filter multiple files based on metadata
- Rename multiple files based on metadata such as date taken

## Installation

```bash
pip install photo-metadata
```

## Dependencies

- [ExifTool] (must be installed separately — either add it to PATH or specify the full path)
- [tqdm] (installed automatically via pip — for progress display)
- [chardet] (installed automatically via pip — for encoding detection)

## Usage

### Metadata Class

The `Metadata` class is the main interface for working with metadata.

```python
from photo_metadata import Metadata
```

#### Initialization

```python
metadata = Metadata(file_path="path/to/your/image.jpg")
```
- `file_path` (str): Path to the image file

#### Access Metadata

Metadata can be accessed like a dictionary.

Access using English tags:
```python
date_time = metadata["EXIF:DateTimeOriginal"]
print(date_time)
```

Access using Japanese tags:
```python
date_time_jp = metadata[photo_metadata.key_ja_to_en("EXIF:レンズモデル")]
print(date_time_jp)
```

#### Modify Metadata

Metadata can be modified like a dictionary.
```python
metadata["EXIF:DateTimeOriginal"] = "2024:02:17 12:34:56"
```

#### Write Metadata to File

```python
metadata.write_metadata_to_file()
```

#### Delete Metadata

```python
del metadata["EXIF:DateTimeOriginal"]
```

#### Additional Methods

- `get_key_map()`: Returns the key translation dictionary (JP to EN)
- `set_exiftool_path(exiftool_path: str | Path)`: Set the path to exiftool
- `get_exiftool_path()`: Get the currently set path to exiftool
- `set_jp_tags_json_path(path)`: Set path to the JSON file containing Japanese tags
- `get_jp_tags_json_path()`: Get the path to the Japanese tag JSON
- `key_en_to_ja(key_en: str)`: Translate an English key to Japanese
- `key_ja_to_en(key_ja: str)`: Translate a Japanese key to English
- `display_japanese(return_type: Literal["str", "print", "dict"] = "print")`: Display metadata using Japanese keys
- `get_date(format='%Y:%m:%d %H:%M:%S')`: Get the date the photo was taken
- `get_model_name()`: Get camera model
- `get_lens_name()`: Get lens name
- `get_focal_length()`: Get focal length
- `get_image_dimensions()`: Get image dimensions
- `get_file_size()`: Get file size
- `get_gps_coordinates()`: Get GPS coordinates
- `export_gps_to_google_maps()`: Convert GPS data to Google Maps URL
- `write_metadata_to_file(file_path: str = None)`: Write metadata to file
- `export_metadata(output_path=None, format='json', lang_ja_metadata=False)`: Export metadata to JSON or CSV
- `show()`: Open the file
- `@classmethod load_all_metadata(cls, file_path_list, progress_func=None, max_workers=40)`: Load metadata from multiple files in parallel

exiftool_path defaults to "exiftool"

#### Comparison

You can compare two `Metadata` objects using `==` or `!=`.

```python
metadata1 = Metadata("image1.jpg")
metadata2 = Metadata("image2.jpg")

if metadata1 == metadata2:
    print("Metadata is the same")
else:
    print("Metadata is different")
```

---

### MetadataBatchProcess Class

The `MetadataBatchProcess` class handles batch metadata operations for multiple files.

```python
from photo_metadata import MetadataBatchProcess
```

#### Initialization

```python
mbp = MetadataBatchProcess(file_path_list)
```

##### `__init__` method

```python
def __init__(self, file_list: list[str], 
             progress_func: Callable[[int], None] | None = None, 
             max_workers: int = 40)
```

#### Filter Files by Metadata (Key or Value)

```python
mbp.filter_by_metadata(keyword_list=["NEX-5R", 2012],
                       exact_match=True,
                       all_keys_match=True,
                       search_by="value")

for file, md in mbp.metadata_objects.items():
    print(f"{os.path.basename(file)}")
```

This filters files containing both "NEX-5R" and "2012" in their metadata values.

#### Custom Filtering with Lambda

```python
mbp.filter_by_custom_condition(lambda md: md[photo_metadata.key_ja_to_en("EXIF:F値")] >= 4.0 and md[photo_metadata.key_ja_to_en("EXIF:モデル")] == 'NEX-5R')

for file, md in mbp.metadata_objects.items():
    print(f"{os.path.basename(file)}")
```

This filters files where F-number ≥ 4.0 and the camera model is 'NEX-5R'.

#### Rename Files Using Metadata

```python
import os
from tkinter import filedialog
from photo_metadata import MetadataBatchProcess, Metadata

def date(md: Metadata):
    date = md.get_date('%Y年%m月%d日-%H.%M.%S')
    if date == md.error_string:
        raise Exception("Not Found")
    return f"{date}-{MetadataBatchProcess.DUP_SEQ_1_DIGIT}"

file_path_list = list(map(os.path.normpath, filedialog.askopenfilenames()))
mr = MetadataBatchProcess(file_path_list)

mr.prepare_rename(format_func=date)

print("new_name_dict")
for file, new_name in mr.new_name_dict.items():
    print(f"{file}\n{new_name}")

print("\nerror_dist")
for file, new_name in mr.error_files.items():
    print(f"{file}\n{new_name}")

input("Press Enter to rename the files")

mr.rename_files()
```

This example renames files based on the date the photo was taken.  
You must include `MetadataBatchProcess.DUP_SEQ_1_DIGIT` in the format to avoid name collisions.

```python
if date == md.error_string:
    raise Exception("Not Found")
```

Throw an error if the date is not found.

---

### Error Handling

The library raises exceptions when files are missing or invalid arguments are provided.

## URLs

- **PyPI**: [https://pypi.org/project/photo-metadata/](https://pypi.org/project/photo-metadata/)  
- **GitHub**: [https://github.com/kingyo1205/photo-metadata](https://github.com/kingyo1205/photo-metadata)

---

## Notes

ExifTool is **required** for this library to function.

## License

This project is licensed under the MIT License.

## Required Software

This library uses [ExifTool](https://exiftool.org/) as an external command for handling image and metadata.

Please make sure ExifTool is installed on your system. You can download it from the [official site](https://exiftool.org/).

> ⚠️ Note: While this library is MIT-licensed, ExifTool itself is distributed under the  
> [Artistic License 2.0](https://dev.perl.org/licenses/artistic.html).  
> You must comply with ExifTool's license when using it.

---






