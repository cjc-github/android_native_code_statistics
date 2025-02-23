
import os


if __name__ == "__main__":
    category_list = ["connectivity", "development", "games", "graphics", "internet", "money", "multimedia", "navigation", "phone-sms", "reading", "science-education", "security", "sports-health", "system", "theming", "time", "writing"]
    for i in category_list:
        try:
            cmd = f"python main.py -i /home/test/fdroid_apk/{i} -o /home/test/fdroid_apk_out/{i}_out"
            # print(cmd)
            os.system(cmd)
        except Exception as e:
            print(e)