import os
from typing import List, Tuple


def scan_file_扫描文件(filepath: str, suffix: str) -> List[Tuple[str, str]]:
    """
    扫描文件夹下所有符合条件的文件
    :param filepath:扫描路径
    :param suffix:过滤后缀
    :return:[(文件路径,文件名),...]
    """
    fileList = []
    print("开始扫描【{0}】".format(filepath))
    if not os.path.isdir(filepath):
        print("【{0}】不是目录".format(filepath))
        exit(-1)
    for filename in os.listdir(filepath):
        if os.path.isdir(filepath + "/" + filename):
            fileList.extend(scan_file_扫描文件(filepath + "/" + filename, suffix))
        else:
            if filename.endswith(suffix):
                fileList.append((filepath, filename))
    return fileList


def scan_file_扫描文件夹(filepath: str):
    """
    扫描指定文件夹下所有文件夹(去重)
    """
    dirs = scan_file_扫描文件(filepath=filepath, suffix="")
    dirs_files = [item[0] for item in dirs]
    #
    return list(set(dirs_files))


if __name__ == '__main__':
    path = "/Users/zhangxuewei/Documents/"
    fileLists = scan_file_扫描文件(path, "扫描文件.py")
    for item in fileLists:
        print(item)

    files = scan_file_扫描文件夹(path)
    print(files)
