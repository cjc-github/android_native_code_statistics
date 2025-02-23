
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
    file_path = "androzoo_out/report_type.txt"
    print(get_num(file_path))