import argparse
import os
import sys


# 如果不是以.apk结尾，则改成.apk结尾
def deal_apk(apk_name):
    if not apk_name.endswith(".apk"):
        os.rename(apk_name, apk_name + ".apk")
        return apk_name + ".apk"
    return apk_name


# 处理apk目录
def deal_apk_folder(apk_path):
    apk_list = []
    if not os.path.exists(apk_path):
        print(" [!] the folder is not exists.")
        return apk_list

    if os.path.isdir(apk_path):
        for name in os.listdir(apk_path):
            apk_list.append(deal_apk(os.path.join(apk_path, name)))
    elif os.path.isfile(apk_path):
        apk_list.append(apk_path)
    else:
        print(" [!] Invalid path: ", apk_path)

    return apk_list


def main():
    print(" [+] Welcome to using android native code statistics analysis.\n")
    Title = " [+] Welcome to using android native code statistics analysis."
    parser = argparse.ArgumentParser(description=Title)
    parser.add_argument("-i", default="apk", help="input dir.")
    parser.add_argument("-o", default="apk_out", help="output dir.")
    args = parser.parse_args()

    apk_lists = deal_apk_folder(args.i)
    for index, name in enumerate(apk_lists):
        print(index, name)
        # 反编译

        # so文件处理

        # native_method函数处理

        # 保存数据，导出报告

    # 导出统计报告
    print(" [+] done.")


if __name__ == "__main__":
    main()
