# photo-metadata

`photo-metadata`は、写真や動画ファイルからメタデータを抽出、操作、書き込みを行うためのPythonライブラリです。exiftoolをバックエンドで使用し、幅広い画像、動画フォーマットに対応しています。日本語タグのサポートも特徴です。

## 主な機能

- 写真や動画ファイルのメタデータの抽出
- メタデータの日本語タグのサポート (一部のexiftoolのタグは日本語に対応していません)
- メタデータの読み取り、書き込み、削除
- さまざまなメタデータ操作のための便利なメソッド
- 2つのMetadataオブジェクトの比較
- 複数のファイルをメタデータでフィルター
- 複数のファイルを撮影日時などでリネーム

## インストール


`pip install photo-metadata`

## 依存関係

- [exiftool] (別途インストールが必要です)

## 使い方

### Metadataクラス

`Metadata`クラスは、メタデータ操作の中心となるクラスです。
```
from photo_metadata import Metadata
```

#### 初期化
```
metadata = Metadata(file_path="path/to/your/image.jpg", exiftool_path="path/to/exiftool.exe", japanese=True)
```
- `file_path` (str): 画像ファイルのパス
- `exiftool_path` (str, optional): ExifTool実行ファイルのパス。デフォルトは`exiftool`
- `japanese` (bool, optional): デフォルトは`True`

#### 例外

- `FileNotFoundError`: 指定されたファイルが見つからない場合
- `TypeError`: 引数の型が正しくない場合

#### メタデータの取得

メタデータは、辞書のようにアクセスできます。

英語のタグでアクセス
```
date_time = metadata["EXIF:DateTimeOriginal"]
print(date_time)
```

日本語のタグでアクセス
```
date_time_jp = metadata["EXIF:撮影日時"]
print(date_time_jp)
```

#### メタデータの変更

メタデータは、辞書のように変更できます。
```
metadata["EXIF:DateTimeOriginal"] = "2024:02:17 12:34:56"
```
変更をファイルに書き込む
```
metadata.write_metadata_to_file()
```

#### メタデータの削除

メタデータは、`del`ステートメントで削除できます。
```
del metadata["EXIF:DateTimeOriginal"]
```

#### その他のメソッド

- `get_date(format: str = '%Y:%m:%d %H:%M:%S')`: 撮影日時を取得 (日付フォーマットを指定できます)
- `get_model_name()`: カメラの機種名を取得
- `get_lens_name()`: レンズ名を取得
- `get_focal_length()`: 焦点距離を取得
- `get_image_dimensions()`: 画像の寸法を取得
- `get_file_size()`: ファイルサイズを取得
- `get_gps_coordinates()`: GPS座標を取得
- `export_gps_to_google_maps()`: GPS情報をGoogleマップのURLに変換
- `write_metadata_to_file(file_path: str = None)`: メタデータをファイルに書き込む
- `validate_metadata(match_all: bool, *conditions: tuple[str, str | int | float, str]) -> bool:`: メタデータを検証できます
- `show()`: ファイルを表示します
- `get_metadata_obj_dict(cls, file_path_list: list[str], exiftool_path: str = default_exiftool_path, progress_func: Callable[[int], None] = None, japanese: bool = True, max_workers: int = 40) -> dict[str, "Metadata"]`: 複数のファイルのメタデータを並列処理で高速に取得します。

exiftool_path引数のデフォルトは"exiftool"です。


#### 比較

`==`と`!=`演算子を使用して、2つの`Metadata`オブジェクトを比較できます。
```
metadata1 = Metadata("image1.jpg")
metadata2 = Metadata("image2.jpg")

if metadata1 == metadata2:
    print("メタデータは同じです")
else:
    print("メタデータは異なります")
```


### MetadataBatchProcessクラス
`MetadataBatchProcess`は複数ファイルのメタデータを処理するためのクラスです。

```
from photo_metadata import MetadataBatchProcess
```

#### 初期化
```
mbp = MetadataBatchProcess(file_path_list)
```

##### __init__メソッド
```
def __init__(self, file_list: list[str], exiftool_path: str = default_exiftool_path, progress_func: Callable[[int], None] = None, japanese: bool = True, max_workers: int = 40)
```

#### メタデータに特定の値またはキーまたはキーと値どちらかに存在するファイルを見つける
```
mbp.filter_by_metadata(keyword_list=["NEX-5R", 2012],
                             exact_match=True,
                             all_keys_match=True,
                             search_by="value")


for file, md in mbp.metadata_objects.items():
    
    print(f"{os.path.basename(file)}")
```

この場合はメタデータの値に"NEX-5R", 2012が両方とも、存在したファイルが残る


#### メタデータを検証
```
keyword_list = [("EXIF:F値", 4.0, Metadata.GREATER_THAN_OR_EQUAL), ("EXIF:モデル", 'NEX-5R', Metadata.EQUALS)]


mbp.filter_by_metadata_validate(conditions=keyword_list, match_all=True)

for file, md in mbp.metadata_objects.items():
    print(f"{os.path.basename(file)}")
```

この場合はメタデータのEXIF:F値が4.0以上かつ、EXIF:モデルが'NEX-5R'のファイルが残る


#### メタデータでリネーム

```
import photo_metadata, os
from tkinter import filedialog



def date(md: photo_metadata.Metadata): 

    date = md.get_date('%Y年%m月%d日-%H.%M.%S')
    if date == md.error_string:
        raise Exception("Not Found")
    return f"{date}-{photo_metadata.MetadataBatchProcess.DUP_SEQ_1_DIGIT}"

file_path_list = list(map(os.path.normpath, filedialog.askopenfilenames()))
mr = photo_metadata.MetadataBatchProcess(file_path_list)

mr.rename_load(format_func=date)

print("new_name_dict")
for file, new_name in mr.new_name_dict.items():
    print(f"{file}\n{new_name}")

print("\nerror_dict")
for file, new_name in mr.error_files.items():
    print(f"{file}\n{new_name}")

input("リネームするなら enter キーを押してください")

mr.rename()
```

この場合は日付でリネームします。
photo_metadata.MetadataBatchProcess.DUP_SEQ_1_DIGIT これは重複連番です。重複したときに数字が増えます。基本は0になります。フォーマットに必ず含めてください。

```
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
作者はWindows 11, Python 3.10.11 で動作を確認しています。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。



このライブラリは、画像やメタデータを処理する際に[ExifTool](https://exiftool.org/)を外部コマンドとして使用しています。

## 必要なソフトウェア

このライブラリを使用するには、ExifToolがシステムにインストールされている必要があります。ExifToolは[公式サイト](https://exiftool.org/)からダウンロードしてインストールしてください。

## ライセンス

このライブラリはMITライセンスの下で配布されています。ただし、ExifTool自体は[Artistic License 2.0](https://dev.perl.org/licenses/artistic.html)の下で配布されています。ExifToolを利用する場合は、そのライセンス条件を遵守してください。

