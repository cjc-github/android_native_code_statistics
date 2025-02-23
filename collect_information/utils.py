import stat
import os.path
import xml.dom
import xml.dom.minidom


# list all files
def list_all_files(file_name):
    _files = []
    list_file = os.listdir(file_name)
    for i in range(0, len(list_file)):
        path = os.path.join(file_name, list_file[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files


# if decompile the apk failed via apktool, then return -1
def judge_apktool(decom_path, name):
    decompile_path = os.path.join(decom_path, name)
    xml_path = os.path.join(decompile_path, "AndroidManifest.xml")
    if not os.path.exists(xml_path) or os.path.getsize(xml_path) == 0:
        return -1

def judge_so_files(decom_path, name):
    decompile_path = os.path.join(decom_path, name)
    if not os.path.exists(os.path.join(decompile_path, "lib")):
        return 0
    else:
        return 1


def get_so_nums(decom_path, name):
    tmp = [0, 0, 0]
    apkUrl = os.path.join(decom_path, name)
    set0 = set()
    set1 = set()
    if not os.path.exists(os.path.join(apkUrl, "lib")):
        return tmp
    else:
        for abilist in os.listdir(apkUrl + "/lib"):
            slibs = os.path.join(apkUrl + "/lib", abilist)
            if os.path.isdir(slibs):
                for soList in os.listdir(slibs):

                    soFilePath = os.path.join(slibs, soList)
                    if soList not in set0 and soFilePath.endswith(".so"):
                        set1.add(soFilePath)
                    set0.add(soList)
        tmp[0] = len(set1)
        stat, dyna = 0, 0
        for set_1 in set1:
            cmd = "nm -D " + set_1 + " | grep 'Java_' | wc -l"
            datas = os.popen(cmd)
            for i in datas:
                if i.strip() != "0":
                    stat += 1

            cmd = "nm -D " + set_1 + " | grep 'JNI_OnLoad' | wc -l"
            datas = os.popen(cmd)
            for i in datas:
                if i.strip() != "0":
                    dyna += 1
        tmp[1], tmp[2] = stat, dyna
        return tmp


# return so files path
def get_so_files(decom_path, name):
    # arm64-v8a, armeabi-v7a, armeabi, x86, x86_64, mips, mips64, other
    all_archs = ["arm64-v8a", "armeabi-v7a", "armeabi", "x86", "x86_64", "mips", "mips64", "other"]
    tmp = [0, 0, 0, 0, 0, 0, 0, 0]
    decompile_path = os.path.join(decom_path, name)
    if not os.path.exists(os.path.join(decompile_path, "lib")):
        return tmp
    else:
        parent_abi = os.path.join(decompile_path, "lib")
        abi_list = os.listdir(parent_abi)
        if "arm64-v8a" in abi_list:
            tmp[0] = 1
        if "armeabi-v7a" in abi_list:
            tmp[1] = 1
        if "armeabi" in abi_list:
            tmp[2] = 1
        if "x86" in abi_list:
            tmp[3] = 1
        if "x86_64" in abi_list:
            tmp[4] = 1
        if "mips" in abi_list:
            tmp[5] = 1
        if "mips64" in abi_list:
            tmp[6] = 1
        for i in abi_list:
            if i not in all_archs:
                tmp[7] = 1
    return tmp


# 获取native-activity
def get_native_activity(decom_path, name):
    decompile_path = os.path.join(decom_path, name)
    if not os.path.exists(os.path.join(decompile_path, "AndroidManifest.xml")):
        print(" [*]" + name + " is not exist.")
        with open("log.file", "a") as f:
            f.write(f"{name}: is not exist.\n")
        return -1
    else:
        tags = ""
        Manifest = os.path.join(decompile_path, "AndroidManifest.xml")
        DOMTree = xml.dom.minidom.parse(Manifest)
        collection = DOMTree.documentElement
        Results = collection.getElementsByTagName("activity")

        for result in Results:
            activity_name = result.getAttribute("android:name")
            if activity_name == "android.app.NativeActivity":
                # print(activity_name)
                return 1


        # for result in Results:
        #     metas = result.getElementsByTagName("meta-data")
        #     for meta in metas:
        #         if meta and meta.getAttribute("android:value") == "native-activity":
        #             tags = tags + result.getAttribute("android:name") + ","
        # if tags[:-1] != "":
        #     return 1
    return -1



# 通过分析反编译的smali代码，找出native函数（静态注册和动态注册都ok）
# 如果为android,androidx,kotlin,com.google开头的目录，不进行分析
def get_native_methods_types(decom_path, name, out):
    total_num = 0
    type_dict = {}
    decompile_path = os.path.join(decom_path, name)

    total_all_type, total_basic_type, total_icc_type, total_complex_type = 0, 0, 0, 0
    for file_name in os.listdir(decompile_path):
        smali_path = os.path.join(decompile_path, file_name)
        if file_name.startswith("smali") and os.path.isdir(smali_path):
            result, stat, dyna = smali_folder(smali_path)
            # deal the para and return type
            for i in result:
                res = create_types(i)
                total_num += len(res[0]) + 1
                # 类型个数
                total_all_type += len(res[0]) + 1
                # 基础类型
                for j in res[0]:
                    if j not in type_dict:
                        type_dict[j] = 1
                    else:
                        type_dict[j] += 1
                if res[1][0] not in type_dict:
                    type_dict[res[1][0]] = 1
                else:
                    type_dict[res[1][0]] += 1
    return total_num, type_dict


# 通过分析反编译的smali代码，找出native函数（静态注册和动态注册都ok）
# 如果为android,androidx,kotlin,com.google开头的目录，不进行分析
def get_native_methods(decom_path, name, out):
    complex_set = set()
    decompile_path = os.path.join(decom_path, name)
    jni_num, jni_stat_num, jni_dyna_num = 0, 0, 0
    # 所有类型个数，基础类型，icc类型，复杂类型
    basic_type = ["void", "boolean", "byte", "short", "char", "int", "long", "float", "double", "java.lang.String",
                  "boolean[]", "byte[]", "short[]", "char[]", "int[]", "long[]", "float[]", "double[]",
                  "java.lang.String[]",
                  "boolean[][]", "byte[][]", "short[][]", "char[][]", "int[][]", "long[][]", "float[][]",
                  "double[][]", "java.lang.String[][]"]
    # Ljava/lang/Object;
    icc_type = ["Landroid/app/Activity;", "Landroid/app/PendingIntent;",
                "Landroid/content/Context;", "Landroid/content/Intent", "Landroid/os/Bundle;",
                "Landroid/app/Application;"]

    total_all_type, total_basic_type, total_icc_type, total_complex_type = 0, 0, 0, 0
    for file_name in os.listdir(decompile_path):
        smali_path = os.path.join(decompile_path, file_name)
        if file_name.startswith("smali") and os.path.isdir(smali_path):
            result, stat, dyna = smali_folder(smali_path)
            # deal the para and return type
            for i in result:
                res = create_types(i)
                # 类型个数
                total_all_type += len(res[0]) + 1
                # 基础类型
                for j in res[0]:
                    if j in basic_type:
                        total_basic_type += 1
                    elif j in icc_type:
                        total_icc_type += 1
                    else:
                        print("complex:", j)
                        complex_set.add(j)
                        total_complex_type += 1
                if res[1][0] in basic_type:
                    total_basic_type += 1
                elif res[1][0] in icc_type:
                    total_icc_type += 1
                else:
                    print("complex:", res[1][0])
                    complex_set.add(res[1][0])
                    total_complex_type += 1
            # print(result)
            jni_num += len(result)
            jni_stat_num += stat
            jni_dyna_num += dyna

    return [jni_num, jni_stat_num, jni_dyna_num], [total_all_type, total_basic_type, total_icc_type, total_complex_type]


# 添加不分析的代码
def judgethird(file):
    if file.split("/")[4] == "android":
        return False
    if file.split("/")[4] == "androidx":
        return False
    if file.split("/")[4] == "com" and file.split("/")[5] == "google" and file.split("/")[5] == "sun":
        return False
    return True


# 处理smali文件，返回规范的jni函数
def smali_folder(file_name):
    results = set()
    for file in list_all_files(file_name):
        file = file.replace("//", "/")
        # 非第三方库
        if judgethird(file):
            with open(file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith(".method ") > 0 and line.find(" native ") > 0:
                        method = "L" + file.split("/", 4)[-1][:-6] + ";." + line.split(" ")[-1].replace("(", ":(")
                        if line.find(" static ") > 0:
                            method = method.strip() + " 1"
                        else:
                            method = method.strip() + " 0"
                        results.add(method)
    # 区别static和非static
    stat, dyna = 0, 0
    for i in results:
        if i[-1] == "1":
            stat += 1
        else:
            dyna += 1
    return results, stat, dyna


# 处理返回值
def deal2(dict1, func_re):
    data = ""
    j = 0
    for i in range(len(func_re)):
        if func_re[i] == '[':
            j = j + 1
        elif func_re[i] in dict1:
            data = dict1.get(func_re[i])
            for _ in range(j):
                data = data + "[]"
    return data


# 处理函数中的参数
def deal1(dict1, str1):
    # 处理jawa/smali中的复杂类型
    stack = []
    tlist = []
    l = -1
    r = -1
    for i in range(len(str1)):
        # 避免存在Lcom/wiyun/engine/nodes/Director$IDirectorLifecycleListener;
        if str1[i] == 'L' and l == -1:
            l = i
        elif str1[i] == ';':
            r = i
            if l != -1 and r != -1:
                line = str1[l:r + 1]
                stack.append(line)
                l = -1
                r = -1
    # 复杂类型中的$替换
    for strg in stack:
        str1 = str1.replace(strg, "O", 1)
    # 保存下复杂类型，方便import等操作
    for strg in stack:
        ort = strg[1:-1].replace("/", ".")
        if "$" not in ort:
            stim = "import " + ort + ";"
    # 将数据拆分成单个数据类型
    j = 0
    for i in range(len(str1)):
        if str1[i] != '[':
            line = str1[j:i + 1]
            j = i + 1
            tlist.append(line)

    # 类型转换，变成java的基础类型
    object1 = 0
    list1 = []
    # 数据类型转换
    for stg in tlist:
        tnk = ""
        num = 0
        for i in range(len(stg)):
            if stg[i] == '[':
                num = num + 1
            elif stg[i] == 'O':
                # ob = stack[object1]
                # object1 = object1 + 1
                # ob = ob.split("/")[len(ob.split("/")) - 1]
                # ob = ob.split("$")[len(ob.split("$")) - 1]
                # ob = ob.replace(";", "")
                # tnk = tnk + ob
                tnk = tnk + stack[object1]
            else:
                if dict1.get(stg[i]):
                    tnk = tnk + dict1.get(stg[i])
        for i in range(num):
            tnk = tnk + "[]"
        list1.append(tnk)
    return list1


# 返回参数类型列表
def create_types(func):
    dict1 = {"V": "void",
             "Z": "boolean",
             "B": "byte",
             "S": "short",
             "C": "char",
             "I": "int",
             "J": "long",
             "F": "float",
             "D": "double",
             "T": "java.lang.String"}
    func_para = func.split("(")[1].split(")")[0]
    func_re = func.split(" ")[0].split(")")[1]
    func_para = func_para.replace("Ljava/lang/String;", "T")
    func_re = func_re.replace("Ljava/lang/String;", "T")
    list = []
    data1 = deal1(dict1, func_para)
    data2 = deal1(dict1, func_re)
    list.append(data1)
    list.append(data2)
    return list


# 判断文件是否是elf文件
def is_ELFfile(filepath):
    if not os.path.exists(filepath):
        print(' [*] file path {} doesnot exits'.format(filepath))
        return False
    try:
        FileStates = os.stat(filepath)
        FileMode = FileStates[stat.ST_MODE]
        if not stat.S_ISREG(FileMode) or stat.S_ISLNK(FileMode):
            return False
        with open(filepath, 'rb') as f:
            header = (bytearray(f.read(4))[1:4]).decode(encoding="utf-8")
            if header in ["ELF"]:
                return True
    except UnicodeDecodeError as e:
        pass

    return False


# 判断assets,res,original中是否存在elf文件
def get_have_elf(decom, apkname):
    flag1, flag2 = 0, 0
    deco_path = os.path.join(decom, apkname)
    if os.path.exists(deco_path):
        # 主要是遍历3个目录：assets,original,res
        assets = os.path.join(deco_path, "assets")
        if os.path.exists(assets):
            file_lists = list_all_files(assets)
            for file in file_lists:
                name = file.split("/")[-1]
                if is_ELFfile(file):
                    flag1 += 1
                if name.endswith(".zip"):
                    try:
                        cmd = "unzip -o -P 123456 -q " + file + " -d " + file[:-4] + "-zip"
                        os.system(cmd)
                        # 对zip内的数据进行分析
                        zip_files = list_all_files(file[:-4] + "-zip")
                        if len(zip_files) == 0:
                            flag2 += 1
                        for zipfile in zip_files:
                            if is_ELFfile(zipfile):
                                flag1 += 1
                    except Exception as e:
                        print("unzip failed.")
            return [flag1, flag2]
        else:
            return [0, 0]
