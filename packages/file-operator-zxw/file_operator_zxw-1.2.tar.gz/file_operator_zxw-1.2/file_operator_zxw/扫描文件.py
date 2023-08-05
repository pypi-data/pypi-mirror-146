import os


def scan_file_path(filepath, suffix):
    """
    扫描文件夹下所有符合条件的文件
    :param filepath:
    :param suffix:
    :return:
    """
    fileList = []
    print("开始扫描【{0}】".format(filepath))
    if not os.path.isdir(filepath):
        print("【{0}】不是目录".format(filepath))
        exit(-1)
    for filename in os.listdir(filepath):
        if os.path.isdir(filepath + "/" + filename):
            fileList.extend(scan_file_path(filepath + "/" + filename, suffix))
        else:
            if filename.endswith(suffix):
                fileList.append((filepath, filename))
    return fileList


def scan_path(filepath):
    """
    扫描指定文件夹下所有文件夹(去重)
    """
    dirs = scan_file_path(filepath=filepath, suffix="")
    dirs_files = [item[0] for item in dirs]
    #
    return list(set(dirs_files))


if __name__ == '__main__':
    path = "/Users/zhangxuewei/Documents/GitHub/pyAutoWeigh/comm公用函数"
    fileLists = scan_file_path(path, "扫描文件.py")

    for item in fileLists:
        print(item)

    files = scan_path(path)
    print(files)
