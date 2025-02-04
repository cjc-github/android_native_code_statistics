import sys
import utils
import os.path

class Preprocess:

    def __init__(self, name, out_path):
        self.apkname = name[:-4].rsplit("/", 1)[1]
        self.name = name
        self.out_path = out_path
        self.Decompile_path = out_path + "/decompile"

    # decompile the apk via apktool tool
    def apktool(self):
        out = os.path.join(self.Decompile_path, self.apkname)
        if not os.path.exists(out):
            cmd = "java -jar apktool_2.6*.jar d -f " + self.name + " -o " + out
            print(cmd)
            os.system(cmd)
        else:
            print(" [+] Has been preocessed by apktool.")

    # report the apk information
    def report(self):
        tmp, tmp1 = [], []
        if utils.judge_apktool(self.Decompile_path, self.apkname) == -1:
            with open("log.file", "a") as f:
                f.write(f"{self.apkname}: apktool decompile failed.\n")
            tmp.append(self.apkname)
        else:
            # apk name
            tmp.append(self.apkname)
            # judge have so file in apk
            tmp.append(utils.judge_so_files(self.Decompile_path, self.apkname))
            # obtain the cpu arch with apk so file
            tmp.append(utils.get_so_files(self.Decompile_path, self.apkname))
            # native-activity
            if utils.get_native_activity(self.Decompile_path, self.apkname) == -1:
                tmp.append(0)
            else:
                tmp.append(1)
            # native
            tmp.append(utils.get_native_methods(self.Decompile_path, self.apkname, self.out_path))
            
            tmp.append(utils.get_so_nums(self.Decompile_path, self.apkname))
            tmp.append(utils.get_have_elf(self.Decompile_path, self.apkname))

            # apk name
            tmp1.append(self.apkname)
            tmp1.append(utils.get_native_methods_types(self.Decompile_path, self.apkname, self.out_path))
        return tmp, tmp1


if __name__ == "__main__":
    apk_path = sys.argv[1]
    out_paths = sys.argv[2]
    pre_deal = Preprocess(apk_path, out_paths)
    pre_deal.apktool()
    pre_deal.report()
