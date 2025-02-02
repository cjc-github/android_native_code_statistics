import os


# get home num
def get_home_num():
    category_txt = "category.txt"
    num = 0
    with open(category_txt, "r") as f:
        lines = f.readlines()
        for index, value in enumerate(lines):
            if index % 3 == 1:
                num += int(value)
    print("home num: ", num)
    return num


# get apk num
def get_apk_num():
    total_lines = 0
    folder_path = "fdroid_urlink_20250201"

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                total_lines += len(lines)

    print(total_lines)
    return total_lines


def main():
    get_home_num()
    get_apk_num()


if __name__ == "__main__":
    main()
