import os

def get_num(file_path):
    num = 0
    with open(file_path, "r") as f:
        lines = f.readlines()
        for i in lines:
            map = i.split("{")[1].split("}")[0]
            
            for i in map.split(","):
                if "Ljava/lang/Object;" in i:
                    print(i)
                    num += int(i.split(":")[1])
    return num

if __name__ == "__main__":
    total_num = 0
    out_path = "fdroid_apk_out"
    for i in os.listdir(out_path):
        file_path = os.path.join(out_path, i, "report_type.txt")
        total_num += get_num(file_path)
        print(get_num(file_path))

    print("total_num:", total_num)