import os


# build the apk download link 
perfix = "https://f-droid.org/repo/"
input_folder = "fdroid_apk_out"
output_folder = "fdroid_urlink_20250204"

if __name__=="__main__":
    for i in os.listdir(input_folder):
        file = i.replace("_out", ".txt")
        # print(i.replace("_out", ".txt"))

        file_path = os.path.join(output_folder, file)
        with open(file_path, "w") as f1:

            report_path = os.path.join(input_folder, i, "report.txt")
            print(report_path)
            with open(report_path,"r") as f:
                lines = f.readlines()
                for index, value in enumerate(lines):
                    if index >= 1:
                        apk_name = value.strip()[2:].split("'")[0] + ".apk"
                        # print(apk_name)
                        f1.write(perfix+apk_name+"\n")
    print("done.")