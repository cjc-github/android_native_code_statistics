import os


# build the apk download link 
perfix = "https://f-droid.org/repo/"
input_folder = "fdroid_apk_out"
output_folder = "fdroid_urlink_20250204"

if __name__=="__main__":

    apk_set = set()
    for i in os.listdir(input_folder):

        report_path = os.path.join(input_folder, i, "report.txt")
        print(report_path)
        with open(report_path,"r") as f:
            lines = f.readlines()
            for index, value in enumerate(lines):
                if index >= 1:
                    if value.strip() not in apk_set:
                        apk_set.add(value.strip())
                    else:
                        print("repeat:", value)

    # record the apk report 
    with open("fdroid_report.txt", "w") as f:
        for i in apk_set:
            f.write(i+"\n")
    print("done.")