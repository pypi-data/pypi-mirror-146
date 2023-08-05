import os


def mkdir创建文件夹(path: str):
    """
    :param path:  只能传入文件夹,不能传入具体文件路径
    :return:
    """
    # 检查是否是具体文件路径
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(f"---  创建文件: {path}...  ---")
    else:
        print("---  创建文件: 文件已存在!  ---")
