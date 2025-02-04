import sys
import os.path
import argparse

from Preprocess import Preprocess


report_file = "report.txt"
report_type_file = "report_type.txt"
log_file = "log.txt"


def deal_apk(apk_name):
    if not apk_name.endswith(".apk"):
        os.rename(apk_name, apk_name + ".apk")
        return apk_name + ".apk"
    return apk_name


def deal_apk_folder(apk_path):
    apk_list = []
    if not os.path.exists(apk_path):
        print(" [!] the folder is not exists.")
        sys.exit(0)
    elif not os.listdir(apk_path):
        print(" [!] the folder is empty.")
        sys.exit(1)
    for name in os.listdir(apk_path):
        app_path = os.path.join(apk_path, name)
        re = deal_apk(app_path)
        apk_list.append(re)
    return apk_list


# using python main.py -i apk -o out
if __name__ == '__main__':
    print(" [+] Welcome to using Native Analysis.\n")
    Title = " [+] Welcome to using Native Analysis."
    parser = argparse.ArgumentParser(description=Title)
    parser.add_argument("-i", default="apk", help="input dir.")
    parser.add_argument("-o", default="apk_out", help="output dir.")
    args = parser.parse_args()

    if not os.path.exists(args.i):
        print("APK file does not the exist!", file=sys.stderr)
    apk_lists = deal_apk_folder(args.i)
    out_folder = args.o

    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    # report file path
    report_file_path = os.path.join(out_folder, report_file)
    report_type_file_path = os.path.join(out_folder, report_type_file)
    log_file_path = os.path.join(out_folder, log_file)

    with open(report_file_path, "a") as f:
        f.write(
            "apk_name, have_lib, [arm64-v8a, armeabi-v7a, armeabi, x86, x86_64, mips, mips64, other], native-activity, "
            "([jni_method_total_num, static_num, nostatic_num], [total_all_type, total_basic_type, total_icc_type, "
            "total_complex_type, total_complex_type]), "
            "[so_total_num, so_Java_num, so_onLoad_num], [have_other_elf, have_pwd_zip]\n")

    for i, apk in enumerate(apk_lists):
        print("[+] No." + str(i), ":", apk)
        pre_deal = Preprocess(apk, out_folder)
        # using apktool to decompile the apk
        pre_deal.apktool()

        # save the basic information to report.txt
        tmp, tmp1 = pre_deal.report()
        with open(report_file_path, "a") as f:
            f.write(str(tmp) + "\n")

        with open(report_type_file_path, "a") as f:
            f.write(str(tmp1) + "\n")
