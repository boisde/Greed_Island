#!/usr/bin/env python3.7
# 注意: 只能把文件放在目标文件夹们所在的dir里面执行.
import os
import pprint
import shutil

CUR_PATH = os.path.abspath(".")
TARGET_DIR_NAMES = [
    # "硅谷.Silicon.Valley.S06",
    # "了不起的麦瑟尔女士.the.marvelous.mrs.maisel.S02",
    # "少年谢尔顿.Young.Sheldon.S03",
    # "良医.The.Good.Doctor.S03",
    # "下辈子我再好好过.Raise.de.wa.Chanto.Shimasu",
    # "傲骨之战.The.Good.Fight.S02",
    # "傲骨之战.The.Good.Fight.S04",
    # "大叔之爱.Ossans.Love",
    # "阿尔罕布拉宫的回忆",
    # "柯明斯基理论.The.Kominsky.Method.S01",
    "[Lilith-Raws] Shingeki no Kyojin - The Final Season",
    "The.Queens.Gambit.S01"
]
TARGET_FILE_TYPE = ".mkv"


def clean_dir(target_dir_name):
    new_target_dir_name = format_file_name(target_dir_name, is_folder=True)
    # create new target folder
    new_folder_path = os.path.join(CUR_PATH, new_target_dir_name)
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
        print("[%s] dir created.\n" % new_folder_path)
    else:
        print("[%s] dir already exists.\n" % new_folder_path)

    # find files to move
    cleaned = []
    for (_dirpath, dirnames, filenames) in os.walk(CUR_PATH):
        # case 1: handle files inside its folder
        for dirname in dirnames:
            if dirname.startswith(target_dir_name) and dirname != target_dir_name:
                print("Putting [%s]..." % dirname)
                # mv the file in it
                son_dir_path = os.path.join(CUR_PATH, dirname)
                for (_, _, files) in os.walk(son_dir_path):
                    for f_name in files:
                        if f_name.endswith(TARGET_FILE_TYPE):
                            f_path = os.path.join(son_dir_path, f_name)
                            print("Moving [%s]..." % f_path)
                            f_name = format_file_name(f_name)
                            dst = shutil.move(f_path, os.path.join(new_folder_path, f_name))
                            if dst:
                                print("Moved to [%s]." % dst)
                cleaned.append(dirname)
        # case 2: handle .mp4 files in Downloads/
        for filename in filenames:
            if filename.startswith(target_dir_name) and os.path.isfile(filename):
                print("Putting [%s]..." % filename)
                # mv the file in it
                filepath = os.path.join(CUR_PATH, filename)
                print("Moving [%s]..." % filepath)
                filename = format_file_name(filename)
                dst = shutil.move(filepath, os.path.join(new_folder_path, filename))
                if dst:
                    print("Moved to [%s]." % dst)
                cleaned.append(filename)

    # delete old folders
    print("\nDeleting folders:")
    pprint.pprint(cleaned)
    for d_or_f in cleaned:
        if os.path.exists(d_or_f):
            if os.path.isdir(d_or_f):
                shutil.rmtree(d_or_f)
            elif os.path.isfile(d_or_f):
                os.remove(d_or_f)


def format_file_name(fn: str, is_folder: bool = False):
    # print(f"fn=[{fn}].")
    if ' ' in fn:
        name_parts = fn.split(' ')
        new_name_parts = []
        for part in name_parts:
            if '[' in part or '-' in part:
                continue
            else:
                new_name_parts.append(part)
        if not is_folder and TARGET_FILE_TYPE not in new_name_parts[-1]:
            new_name_parts.append(TARGET_FILE_TYPE[1:])
        fn = '.'.join(new_name_parts)
    # print(f"new fn=[{fn}].")
    return fn


if __name__ == "__main__":
    for dir in TARGET_DIR_NAMES:
        clean_dir(dir)
