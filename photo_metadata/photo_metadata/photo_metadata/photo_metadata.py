

import datetime, subprocess,concurrent.futures, os, json, pprint, csv, glob, re, copy, collections, tempfile
from inspect import currentframe
from typing import Callable, Literal, Any
from tqdm import tqdm
from uuid import uuid4
import sys
from pathlib import Path


def date_format(date_text: str, old_format: str, new_format: str):
    return datetime.datetime.strptime(date_text, old_format).strftime(new_format)

def find_key(data, keyword, find_is_key, exact_match_):
        
        if isinstance(data, dict):
            for k, v in data.items():
                
                if find_is_key:
                    if isinstance(k, str) and isinstance(keyword, str):
                        if exact_match_:
                            if k == keyword:
                                return True
                        else:
                            if keyword in k:
                                return True
                    else:
                        if v == keyword:
                            return True
                else:
                    if isinstance(v, str) and isinstance(keyword, str):
                        if exact_match_:
                            if v == keyword:
                                return True
                        else:
                            if keyword in v:
                                return True
                    else:
                        if v == keyword:
                            return True

                if isinstance(v, (dict, list)):
                    if find_key(v, keyword, find_is_key, exact_match_):
                        return True
        return False

def get_value(d: dict, key: str, default: Any = None) -> Any:
    
    if key in d:
        return d[key]
    for k, v in d.items():
        if isinstance(v, dict):
            result = get_value(v, key, default)
            if result is not default:
                return result
    return default

def set_value(d: dict, key: str, value: Any) -> None:
    
    if key in d:
        d[key] = value
        return
    for k, v in d.items():
        if isinstance(v, dict):
            set_value(v, key, value)
            return
    d[key] = value

default_exiftool_path = r"exiftool"
default_jp_tags_json_name = r"exiftool_Japanese_tag.json"
default_jp_tags_json_path = os.path.join(os.path.dirname(__file__), default_jp_tags_json_name)

if not os.path.isfile(default_jp_tags_json_path):
    print(f"warning: JP tags json file not found: {default_jp_tags_json_path}")



class Metadata:
    
    EQUALS = "equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    CONTAINS = "contains"
    

    def __init__(self, file_path: str, exiftool_path: str | None = None, japanese: bool = True, jp_tags_json_path: str | None = None):
        
        if jp_tags_json_path is None:
            jp_tags_json_path = default_jp_tags_json_path
        
        if exiftool_path is None:
            exiftool_path = default_exiftool_path
            
        if not os.path.isfile(jp_tags_json_path):
            if japanese:
                raise FileNotFoundError(f"JP tags jsonファイルが見つかりません: {jp_tags_json_path}")
            else:
                raise FileNotFoundError(f"JP tags json file not found: {jp_tags_json_path}")
        
        if not isinstance(file_path, (str, Path)):
            if japanese:
                raise TypeError("file_pathはstrまたはPath型を指定してください。")
            else:
                raise TypeError("file_path must be str or Path.")
        
        if not isinstance(exiftool_path, (str, Path)):    
            if japanese:
                raise TypeError("exiftool_pathはstrまたはPath型を指定してください。")
            else:
                raise TypeError("exiftool_path must be str or Path.")
        
        
        


        self.file_path = file_path
        self.exiftool_path = exiftool_path
        self.jp_tags_json_path = jp_tags_json_path
        self.metadata: dict = None
        self.key_map = None
        self.reverse_key_map = None
        self.japanese_metadata: dict = None
        self.japanese = japanese


        
        if self.japanese:
            self.error_string = "エラー"
        else:
            self.error_string = "error"
        
        if not os.path.isfile(self.file_path):
            if self.japanese:
                raise FileNotFoundError(f"ファイルが見つかりません: {self.file_path}")
            else:
                raise FileNotFoundError(f"file not found: {self.file_path}")
        
        try:
            command_exiftool_text = f'{self.exiftool_path} -G -json "{self.file_path}"'
            
            if sys.platform == "linux":
                result = subprocess.run(command_exiftool_text, capture_output=True, text=True, shell=True, encoding='utf-8', check=True)
            else:
                result = subprocess.run(command_exiftool_text, capture_output=True, text=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW, encoding='utf-8', check=True)
            self.metadata = json.loads(result.stdout)[0]
            self.metadata["SourceFile"] = file_path
            self.japanese_tags_by_keymap_dict()

            

            tags = ["file_path", "file_name", "shooting_date", "model_name", "lens_name", "focal_length", "dimensions", "file_size", "gps", "gps_to_google_maps"]
            ja_tags = ["ファイルパス", "ファイル名", "撮影日時", "機種名", "レンズ名", "焦点距離", "寸法", "ファイルサイズ", "gps", "gps情報のgoogleマップのurl"]
            funcs = [(lambda: self.file_path), (lambda: os.path.basename(self.file_path)), self.get_date, self.get_model_name, self.get_lens_name, self.get_focal_length, self.get_image_dimensions, self.get_file_size,
                     self.get_gps_coordinates, self.export_gps_to_google_maps]
            for tag, ja_tag, func in zip(tags, ja_tags, funcs):
                data = func()
                
                self.metadata[f"original_of_this_lib:{tag}"] = data
                self.japanese_metadata[f"original_of_this_lib:{ja_tag}"] = data

            for tag, ja_tag in zip(tags, ja_tags):
                self.key_map[f"{tag}"] = f"{ja_tag}"
                self.reverse_key_map[f"{ja_tag}"] = f"{tag}"

            
            
        except Exception as e:
            if self.japanese:
                print("\n-----------エラー-----------")
                print(f"ファイル: {self.file_path}")
                #print(f"標準エラー出力: {result.stderr}")
                print(f"例外: {e}")

                self.metadata = None

                print("メタデータを取得できません")
                print("----------------------------")
            else:
                print("\n-----------error-----------")
                print(f"file: {self.file_path}")
                #print(f"stderr : {result.stderr}")
                print(f"exception: {e}")

                self.metadata = None

                print("Failed to get metadata")
                print("----------------------------")

        
    def __getitem__(self, key):
        if not isinstance(key, str):
            if self.japanese:
                raise KeyError("metadataオブジェクト['グループ:タグ']で指定してください。 例: metadataオブジェクト['EXIF:DateTimeOriginal']")
            else:
                raise KeyError("Specify as metadata object['Group:Tag']. Example: metadata object['EXIF:DateTimeOriginal']")
        
        try:
            return self.metadata[key]
        except KeyError:
            try:
                return self.japanese_metadata[key]
            except KeyError:
                if self.japanese:
                    raise KeyError(f"見つかりませんでした: {key}")
                else:
                    raise KeyError(f"not found: {key}")
    
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            if self.japanese:
                raise KeyError("metadataオブジェクト['グループ:タグ'] = 値で指定してください。 例: metadataオブジェクト['EXIF:DateTimeOriginal'] = '2024:02:03 20:46:04'")
            else:
                raise KeyError("Specify as metadata object['Group:Tag'] = value. Example: metadata object['EXIF:DateTimeOriginal'] = '2024:02:03 20:46:04'")

        group, tag = key.split(':')
        if tag.isascii():
            if tag in self.key_map:
                self.metadata[key] = value
                self.japanese_metadata[f"{group}:{self.key_map[tag]}"] = value
            else:
                if self.japanese:
                    print("警告: このキーはself.japanese_metadataに入れる際に日本語に変換されません。")
                else:
                    print("Warning: This key is not converted to Japanese in self.japanese_metadata.")
                self.metadata[key] = value
                self.japanese_metadata[key] = value
        else:
            if tag in self.reverse_key_map:
                self.metadata[f"{group}:{self.reverse_key_map[tag]}"] = value
                self.japanese_metadata[key] = value
            else:
                if self.japanese:
                    print("警告: このキーはself.metadataに入れる際に英語に変換されません。")
                else:
                    print("Warning: This key is not converted to English in self.metadata.")
                self.metadata[key] = value
                self.japanese_metadata[key] = value
        
        return self
    
    def __delitem__(self, key):
        if not isinstance(key, str):
            if self.japanese:
                raise KeyError("metadataオブジェクト['グループ:タグ']で指定してください。 例: del metadataオブジェクト['EXIF:DateTimeOriginal']")
            else:
                raise KeyError("Specify as metadata object['Group:Tag']. Example: del metadata object['EXIF:DateTimeOriginal']")
        
        if key not in self.metadata and key not in self.japanese_metadata:
            if self.japanese:
                raise KeyError(f"見つかりませんでした: {key}")
            else:
                raise KeyError(f"not found: {key}")

        group, tag = key.split(':')
        if tag.isascii():
            if tag in self.key_map:
                del self.metadata[key]
                del self.japanese_metadata[f"{group}:{self.key_map[tag]}"]
            else:
                if self.japanese:
                    print("警告: このキーはself.japanese_metadataから削除されません。")
                else:
                    print("Warning: This key is not deleted from self.japanese_metadata.")
                
                del self.metadata[key]
        
        else:
            if tag in self.reverse_key_map:
                del self.metadata[f"{group}:{self.reverse_key_map[tag]}"]
                del self.japanese_metadata[key]
            else:
                if self.japanese:
                    print("警告: このキーはself.metadataから削除されません。")
                else:
                    print("Warning: This key is not deleted from self.metadata.")
                
                del self.metadata[key]
    
        

    def __str__(self) -> str:

        if self.japanese:
            print_text = f"----------- メタデータ (英語のタグ (キー)) -----------\n{pprint.pformat(self.metadata)}\n\n"
            print_text = print_text + f"----------- メタデータ (日本語のタグ (キー)) -----------\n{pprint.pformat(self.japanese_metadata)}"
        else:
            print_text = f"----------- Metadata (English tags (key)) -----------\n{pprint.pformat(self.metadata)}\n\n"
            print_text = print_text + f"----------- Metadata (Japanese tags (key)) -----------\n{pprint.pformat(self.japanese_metadata)}"
        
        return print_text
    

    def __eq__(self, other: "Metadata"):
        metadata_copy = self.metadata.copy()
        other_metadata_copy = other.metadata.copy()
        
        del metadata_copy["SourceFile"]
        del other_metadata_copy["SourceFile"]

        for key, value in metadata_copy.copy().items():

            if key.split(":")[0] == "File" or key.split(":")[0] == "ExifTool" or key.split(":")[0] == "original_of_this_lib":
                del metadata_copy[key]
        
        for key, value in other_metadata_copy.copy().items():

            if key.split(":")[0] == "File" or key.split(":")[0] == "ExifTool" or key.split(":")[0] == "original_of_this_lib":
                del other_metadata_copy[key]

        s = set(metadata_copy.items()) ^ set(other_metadata_copy.items())
        
        
        return metadata_copy == other_metadata_copy
    
    def __ne__(self, other: "Metadata"):
        metadata_copy = self.metadata.copy()
        other_metadata_copy = other.metadata.copy()
        
        del metadata_copy["SourceFile"]
        del other_metadata_copy["SourceFile"]

        for key, value in metadata_copy.copy().items():

            if key.split(":")[0] == "File" or key.split(":")[0] == "ExifTool" or key.split(":")[0] == "original_of_this_lib":
                del metadata_copy[key]
        
        for key, value in other_metadata_copy.copy().items():

            if key.split(":")[0] == "File" or key.split(":")[0] == "ExifTool" or key.split(":")[0] == "original_of_this_lib":
                del other_metadata_copy[key]
        
        return not metadata_copy == other_metadata_copy

    def japanese_tags_by_keymap_dict(self):
        
        with open(self.jp_tags_json_path, "r", encoding="UTF-8") as jp_tags_json_data:
            self.key_map = json.load(jp_tags_json_data)["exiftool"]
        self.reverse_key_map = {v: k for k, v in self.key_map.items()}

        def rename_keys(d, key_map):

            if isinstance(d, dict):
                new_dict = {}
                for k, v in d.items():
                    if ":" in k:
                        k1, k2 = k.split(":")
                        new_key = key_map.get(k2, k2)
                        new_dict[f"{k1}:{new_key}"] = rename_keys(v, key_map)
                    else:
                        new_key = key_map.get(k, k)
                        new_dict[new_key] = rename_keys(v, key_map)
                return new_dict
            elif isinstance(d, list):
                return [rename_keys(item, key_map) for item in d]
            else:
                return d
        
        self.japanese_metadata = rename_keys(self.metadata, self.key_map)

                    
    
    
    
    def write_metadata_to_file(self, file_path: str = None):
        if file_path is None:
            file_path = self.file_path

        print(file_path)

        write_metadata = {}

        for k, v in self.metadata.items():
            if k.split(":")[0] != "original_of_this_lib":
                write_metadata[k] = v
        
        write_metadata["SourceFile"] = "*"

        

        # メタデータをJSONファイルに一時的に保存
        temp_json = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_json.close()
        print(temp_json.name)
        with open(temp_json.name, 'w', encoding='utf-8') as f:
            json.dump(write_metadata, f, ensure_ascii=False, indent=4)

        try:
            # exiftoolを使用してメタデータを書き込む
            command = f'{self.exiftool_path} -json="{temp_json.name}" -overwrite_original "{file_path}"'
            if sys.platform == "linux":
                result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True, encoding='utf-8')
            else:
                result = subprocess.run(command, capture_output=True, text=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW, check=True, encoding='utf-8')
            if self.japanese:
                print(f"exiftoolの標準出力: {result.stdout}")
                print(f"exiftoolの標準エラー: {result.stderr}")
            else:
                print(f"exiftool standard output: {result.stdout}")
                print(f"exiftool standard error: {result.stderr}")

            if result.returncode != 0:
                if self.japanese:
                    raise RuntimeError(f"メタデータの書き込みに失敗しました。エラー: {result.stderr}")
                else:
                    raise RuntimeError(f"Failed to write metadata. Error: {result.stderr}")

            if self.japanese:
                print(f"メタデータが正常に書き込まれました: {file_path}")
            else:
                print(f"Metadata successfully written to: {file_path}")

        finally:
            # 一時ファイルを削除
            os.unlink(temp_json.name)
            
    
    def export_metadata(self, output_path: str = None, format: str = 'json', lang_ja_metadata: bool = True):
        
        def flatten_dict(d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)
        
        format = format.lower()
        # エクスポートするメタデータを選択
        metadata_to_export = self.japanese_metadata.copy() if lang_ja_metadata else self.metadata.copy()
        
        # output_pathが指定されていない場合、ファイルと同じフォルダに設定
        if output_path is None:
            output_path = os.path.join(os.path.dirname(currentframe().f_back.f_code.co_filename), f"{os.path.basename(self.file_path)}__メタデータ.{format}")

        # メタデータをエクスポート
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_to_export, f, ensure_ascii=False, indent=4)
        elif format == 'csv':
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for key, value in metadata_to_export.items():
                    writer.writerow([key, value])
        else:
            if self.japanese:
                raise ValueError("引数 format に \"csv\" または \"json\" を渡してください")
            else:
                raise ValueError("argument format must be \"csv\" or \"json\"")
    


    def get_gps_coordinates(self):
        degree_symbol = u"\u00B0"
        if "Composite:GPSLatitude" in self.metadata and "Composite:GPSLongitude" in self.metadata:
            location = f'{self.metadata["Composite:GPSLatitude"].replace("deg", degree_symbol).replace(" ", "")} {self.metadata["Composite:GPSLongitude"].replace("deg", degree_symbol).replace(" ", "")}'
            return location
        else:
            return self.error_string

    def export_gps_to_google_maps(self):
        coordinates = self.get_gps_coordinates()
        if coordinates != self.error_string:
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={coordinates}"
            return google_maps_url
        else:
            return coordinates


    def get_date(self, format: str = '%Y:%m:%d %H:%M:%S', default_time_zone: str = '+09:00'):
        if "EXIF:DateTimeOriginal" in self.metadata:
            date = self.metadata["EXIF:DateTimeOriginal"]
            date = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S').strftime(format)
        elif "QuickTime:CreateDate" in self.metadata:
            if self.metadata["QuickTime:CreateDate"] == "0000:00:00 00:00:00":
                return self.error_string
            if "QuickTime:TimeZone" in self.metadata:
                dt = datetime.datetime.strptime(self.metadata["QuickTime:CreateDate"], '%Y:%m:%d %H:%M:%S')
                tz = datetime.datetime.strptime(self.metadata["QuickTime:TimeZone"].replace("+", ""), "%H:%M")
                tz = datetime.timedelta(hours=int(tz.strftime("%H")), minutes=int(tz.strftime("%M")))
                date = dt + tz
                date = date.strftime(format)
            else:
                dt = datetime.datetime.strptime(self.metadata["QuickTime:CreateDate"], '%Y:%m:%d %H:%M:%S')
                tz = datetime.datetime.strptime(default_time_zone.replace("+", ""), "%H:%M")
                tz = datetime.timedelta(hours=int(tz.strftime("%H")), minutes=int(tz.strftime("%M")))
                date = dt + tz
                date = date.strftime(format)
        else:
            date = self.error_string
        return date
    
    def get_image_dimensions(self):
        if "Composite:ImageSize" in self.metadata:
            size = self.metadata["Composite:ImageSize"]
            size_x, size_y = size.split("x")
        else:
            return self.error_string
        return size_x, size_y
    
    def get_file_size(self):

        if self.file_path is None:
            if self.japanese:
                raise ValueError("file_path がNoneです")
            else:
                raise ValueError("file_path is None")

        if not os.path.exists(self.file_path):
            if self.japanese:
                raise FileNotFoundError(f"ファイルが見つかりません: {self.file_path}")
            else:
                raise FileNotFoundError(f"file not found: {self.file_path}")
        # ファイルサイズをバイト単位で取得
        file_size_bytes = os.path.getsize(self.file_path)
        
        # 桁数に応じて適切な単位に変換
        if file_size_bytes < 1024:
            return f"{file_size_bytes} B", file_size_bytes
        elif file_size_bytes < 1024**2:
            file_size_kb = file_size_bytes / 1024
            return f"{file_size_kb:.3f} KB", file_size_bytes
        elif file_size_bytes < 1024**3:
            file_size_mb = file_size_bytes / (1024**2)
            return f"{file_size_mb:.3f} MB", file_size_bytes
        else:
            file_size_gb = file_size_bytes / (1024**3)
            return f"{file_size_gb:.3f} GB", file_size_bytes
    
    

    def get_model_name(self):
        if "EXIF:Model" in self.metadata:
            model_name = self.metadata["EXIF:Model"]
        elif "XML:DeviceModelName" in self.metadata:
            model_name = self.metadata["XML:DeviceModelName"]
        else:
            model_name = self.error_string
        return model_name
    
    def get_lens_name(self):
        if "EXIF:LensModel" in self.metadata:
            lens = self.metadata["EXIF:LensModel"]
        else:
            lens = self.error_string
        return lens

    def get_focal_length(self):
        focal_length_dict = {}
        if "EXIF:FocalLength" in self.metadata:
            focal_length = self.metadata["EXIF:FocalLength"]
        else:
            focal_length = self.error_string
        
        if self.japanese:
            focal_length_dict["焦点距離"] = focal_length
        else:
            focal_length_dict["Focal_Length"] = focal_length
        
        if "EXIF:FocalLengthIn35mmFormat" in self.metadata:
            focal_length35 = self.metadata["EXIF:FocalLengthIn35mmFormat"]
        else:
            focal_length35 = self.error_string
        
        if self.japanese:
            focal_length_dict["35mm換算_焦点距離"] = focal_length35
        else:
            focal_length_dict["Focal_Length_35mm"] = focal_length35
        
        return focal_length_dict

    def get_main_metadata(self):

        english_keys = {
            "ファイルパス": "File_Path",
            "ファイル名": "File_Name",
            "撮影日時": "Date",
            "機種名": "Model_Name",
            "レンズ名": "Lens_Name",
            "F値": "F_Number",
            "シャッタースピード": "Exposure_Time",
            "ISO": "ISO",
            "焦点距離": "Focal_Length",
            "35mm換算_焦点距離": "Focal_Length_35mm",
            "画像サイズ": "Image_Size",
            "ファイルサイズ": "File_Size"}
        
        md_dict = {}
        md_dict["ファイルパス"] = self.file_path
        md_dict["ファイル名"] = os.path.basename(self.file_path)
        md_dict["撮影日時"] = self.get_date()
        md_dict["機種名"] = self.get_model_name()
        md_dict["レンズ名"] = self.get_lens_name()
        for m, jm in zip(["FNumber", "ExposureTime", "ISO"], ["F値", "シャッタースピード", "ISO"]):
            try:
                data = self.metadata[f"EXIF:{m}"]
            except KeyError:
                data = "エラー"
            md_dict[jm] = data
        
        focal_length = self.get_focal_length()
        if focal_length != "エラー":
           
            md_dict["焦点距離"] = focal_length["焦点距離"]
            md_dict["35mm換算_焦点距離"] = focal_length["35mm換算_焦点距離"]
            
        
        md_dict["画像サイズ"] = self.get_image_dimensions()
        md_dict["ファイルサイズ"] = self.get_file_size()

        if self.japanese:
            return md_dict
        else:
            md_dict = {english_keys[k]: v for k, v in md_dict.items()}

        return md_dict
    
    def show(self):
        if self.file_path is None:
            if self.japanese:
                raise ValueError("ファイルパスがNoneです。")
            else:
                raise ValueError("file path is None.")
        if not os.path.isfile(self.file_path):
            if self.japanese:
                raise FileNotFoundError(f"ファイルが見つかりません: {self.file_path}")
            else:
                raise FileNotFoundError(f"file not found: {self.file_path}")
        
        os.startfile(self.file_path)

    def validate_metadata(self, match_all: bool, *conditions: tuple[str, str | int | float, str]) -> bool:
        for key, value, comparison in conditions:
            try:
                metadata_value = self[key]
            except KeyError:
                if match_all:
                    return False
                else:
                    continue
            
            if isinstance(metadata_value, (int, float)) and isinstance(value, (int, float)):
                if comparison == self.EQUALS and metadata_value != value:
                    if match_all:
                        return False
                elif comparison == self.GREATER_THAN and metadata_value <= value:
                    if match_all:
                        return False
                elif comparison == self.LESS_THAN and metadata_value >= value:
                    if match_all:
                        return False
                elif comparison == self.GREATER_THAN_OR_EQUAL and metadata_value < value:
                    if match_all:
                        return False
                elif comparison == self.LESS_THAN_OR_EQUAL and metadata_value > value:
                    if match_all:
                        return False
                
                    
            elif isinstance(metadata_value, str) and isinstance(value, str):
                if comparison == self.EQUALS and metadata_value != value:
                    if match_all:
                        return False
                elif comparison == self.CONTAINS and value not in metadata_value:
                    if match_all:
                        return False
            
            if not match_all:
                return True
        
        return match_all

    
    def contains_key(self, key_name: str, japanese_tags: bool = True, exact_match: bool = True):
        return find_key(self.japanese_metadata, key_name, True, exact_match) if japanese_tags else find_key(self.metadata, key_name, True, exact_match)

    def contains_value(self, key_name: str, japanese_tags: bool = True, exact_match: bool = True):
        return find_key(self.japanese_metadata, key_name, False, exact_match) if japanese_tags else find_key(self.metadata, key_name, False, exact_match)

    def print_jp_tags_json_dict(self):
        pprint.pprint(self.key_map)

    def copy(self):
        return copy.deepcopy(self)
        
    @classmethod
    def get_metadata_obj_dict(cls, file_path_list: list[str], exiftool_path: str = default_exiftool_path, progress_func: Callable[[int], None] | None = None, japanese: bool = True, max_workers: int = 40) -> dict[str, "Metadata"]:
        
        def get_metadata_obj(file_path: str):
            return file_path, Metadata(file_path, exiftool_path, japanese=japanese)
        
        file_list_len = len(file_path_list)
        metadata_obj_dict = {}
        # 並列処理のためのExecutorを作成
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            
            # ファイルパスのリストをsubmitメソッドに渡し、Futureオブジェクトのリストを作成
            futures_text = [executor.submit(get_metadata_obj, file_path) for file_path in file_path_list]

            progress = 0

            for future in tqdm(concurrent.futures.as_completed(futures_text), dynamic_ncols=True, total=file_list_len):
            # 処理結果を取得
                result_file, result_md = future.result()
                metadata_obj_dict[result_file] = result_md

                progress += 1

                if not progress_func is None:
                    progress_func((progress * 100) // file_list_len)
        if not progress_func is None:
            progress_func(100)

        return metadata_obj_dict
    

class MetadataBatchProcess:
    
    DUP_SEQ_1_DIGIT = "重複連番1桁"
    DUP_SEQ_2_DIGIT = "重複連番2桁"
    DUP_SEQ_3_DIGIT = "重複連番3桁"
    DUP_SEQ_4_DIGIT = "重複連番4桁"
    NUMBER = "連番"

    dup_seq_list = [DUP_SEQ_1_DIGIT, DUP_SEQ_2_DIGIT, DUP_SEQ_3_DIGIT, DUP_SEQ_4_DIGIT]

    def __init__(self, file_list: list[str], exiftool_path: str = default_exiftool_path, progress_func: Callable[[int], None] | None = None, japanese: bool = True, max_workers: int = 40):
        self.file_list = list(map(os.path.normpath, file_list))
        self.exiftool_path = exiftool_path
        self.jp_tags_json_path = default_jp_tags_json_path
        self.progress_func = progress_func

        self.metadata_objects: dict[str, Metadata] = Metadata.get_metadata_obj_dict(self.file_list, exiftool_path=self.exiftool_path, progress_func=self.progress_func, japanese=japanese, max_workers=max_workers)
    

    def filter_by_metadata_validate(self, conditions: list[tuple[str, str, str]], match_all: bool):
        new_metadata_objects = {}
        new_file_list = []

        for file, md in self.metadata_objects.items():
            if md.validate_metadata(match_all, *tuple(conditions)):
                new_file_list.append(file)
                new_metadata_objects[file] = md

        self.file_list = new_file_list
        self.metadata_objects = new_metadata_objects


    
        
    

    def filter_by_metadata(self, keyword_list: list[str], exact_match: bool, all_keys_match: bool, search_by: Literal["either", "value", "key"], japanese_tags: bool = True):
        new_metadata_objects = {}
        new_file_list = []

        for file, md in self.metadata_objects.items():
            temp_file_metadata_list = []
            for keyword in keyword_list:
                if search_by == "key":
                    find_result_key = md.contains_key(keyword, japanese_tags=japanese_tags, exact_match=exact_match)
                    temp_file_metadata_list.append([file, md, find_result_key])
                
                if search_by == "value":
                    find_result_value = md.contains_value(keyword, japanese_tags=japanese_tags, exact_match=exact_match)
                    temp_file_metadata_list.append([file, md, find_result_value])

                if search_by == "either":
                    find_result_key = md.contains_key(keyword, japanese_tags=japanese_tags, exact_match=exact_match)
                    find_result_value = md.contains_value(keyword, japanese_tags=japanese_tags, exact_match=exact_match)

                    temp_file_metadata_list.append([file, md, any([find_result_key, find_result_value])])


            if all_keys_match:
                if all([b[2] for b in temp_file_metadata_list]):
                    new_file_list.append(file)
                    new_metadata_objects[file] = md
            else:
                if any([b[2] for b in temp_file_metadata_list]):
                    new_file_list.append(file)
                    new_metadata_objects[file] = md

        self.file_list = new_file_list.copy()
        self.metadata_objects = new_metadata_objects.copy()
    
    
    

    def rename_load(self, format_func: Callable[[Metadata], str]):
        self.format_func = format_func

        def incrementer():
            count = 0
            def increment():
                nonlocal count
                count += 1
                return count
            return increment

        def add_duplicate_sequence_number(input_dict: dict):
            duplicate_count = {}
            renamed_files = {}
            i = incrementer()
            for key, value in tqdm(input_dict.items()):
                if value not in duplicate_count:
                    duplicate_count[value] = 0
                else:
                    duplicate_count[value] += 1
                
                
                n = i()
                
                
                renamed_files[key] = value + (duplicate_count[value], n)
            
            return renamed_files
        
        dir_path = os.path.dirname(self.file_list[0])
        all_files = glob.glob(os.path.join(dir_path, "*.*"))
        
        not_selected_files = list(set(all_files) - set(self.file_list))
        not_selected_files = [os.path.basename(n) for n in not_selected_files]

        

        error_files = {}
        base_name_dict = {}
        name_dict = {}
        new_name_dict = {}

        for file, md_obj in self.metadata_objects.items():
            ext = os.path.splitext(file)[1].upper()
            if ext == ".JPG" or ext == ".jpg":
                ext = ".JPEG"
                
            try:
                base_name = self.format_func(md_obj)

                if "GPS情報が見つかりませんでした" in base_name or "撮影日時 取得 失敗" in base_name or "モデル情報が見つかりませんでした" in base_name:
                    error_files[file] = "エラー"
                else:
                    for d in self.dup_seq_list:
                        if d in base_name:
                            r = re.search(r'重複連番(.+)桁', base_name).group(1)
                            count_digit = int(r)
                            base_name = base_name.replace(d, '<RN>')

                            
                    base_name_dict[file] = (base_name, ext)

            except Exception as e:
                error_files[file] = "エラー"
                print(e)

        base_name_dict = sorted(base_name_dict.items(), key=lambda x: x[0])
        base_name_dict = dict((x, y) for x, y in base_name_dict)
        
        base_name_dict = add_duplicate_sequence_number(base_name_dict)
        
        t = tqdm(total=len(base_name_dict))

        for for_count, (file_path, (base_name, ext, dup_num, number)) in enumerate(base_name_dict.items()):
            count_is_file = 0

            if "連番" in f"{base_name}{ext}" and "<RN>" in f"{base_name}{ext}":
                new_name = f"{base_name.replace('<RN>', str(dup_num).zfill(count_digit))}{ext}"
                new_name = new_name.replace("連番", number)

            elif "連番" in f"{base_name}{ext}":
                new_name = f"{base_name}{ext}".replace("連番", str(number))

            elif "<RN>" in f"{base_name}{ext}":
                new_name = f"{base_name.replace('<RN>', str(dup_num).zfill(count_digit))}{ext}"

            if os.path.basename(file_path) != new_name:
                while new_name in not_selected_files:
                    count_is_file += 1
                    new_name = f"{base_name.replace('<RN>', str(count_is_file).zfill(count_digit))}{ext}"
                    if os.path.basename(file_path) == new_name:
                        break
        
            if new_name == os.path.basename(file_path):
                new_name = "リネーム前後のファイル名が同じです"
            name_dict[file_path] = new_name

            t.update(for_count + 1)

        for file, name in name_dict.items():
            if name == "リネーム前後のファイル名が同じです":
                error_files[file] = "リネーム前後のファイル名が同じです"
            else:
                new_name_dict[file] = name
        
        self.new_name_dict = new_name_dict
        self.error_files = error_files
    
    def rename(self):
        total = len(self.new_name_dict) * 2
        t = tqdm(total=total)
        temp_dict = {}
        count = 0
        for file, new_name in self.new_name_dict.items():
            dir_name = os.path.dirname(file)
            temp_name = f"{uuid4()}{os.path.splitext(new_name)[1]}"
            temp_path = os.path.join(dir_name, temp_name)
            os.rename(file, temp_path)
            temp_dict[temp_path] = new_name

            count += 1
            t.update(count)
            if not self.progress_func is None:
                self.progress_func((count * 100) // total)
        
        for temp_path, new_name in temp_dict.items():
            os.rename(temp_path, os.path.join(os.path.dirname(temp_path), new_name))

            count += 1
            t.update(count)
            if not self.progress_func is None:
                self.progress_func((count * 100) // total)
        
        return "リネーム完了!!"
    
    def copy(self):
        return copy.deepcopy(self)

        






            

















    
        
    



