import re
import os.path
import requests
import traceback

from math import ceil
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime

current_date = datetime.now().strftime("%Y%m%d")

folder_name = f"fdroid_urlink_{current_date}"

# Define the URL of the F-Droid website
url = 'https://f-droid.org/zh_Hans/packages/'
home_url = 'https://f-droid.org'

category_txt = "category.txt"

# Proxy settings (replace with actual proxy if needed)
proxies = {
    'http': 'http://192.168.0.106:7890',
    'https': 'http://192.168.0.106:7890',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3858.400 QQBrowser/10.7.4309.40'}


def extract_number(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    else:
        return None


def generate_category_url(category_url):
    return home_url + category_url


def get_last_segment(url):
    if not url:
        return None

    segments = [segment for segment in url.split('/') if segment]

    if segments:
        return segments[-1]
    else:
        return None


# download the first page
def downFirstTxt(url, sub_folder):
    print("download the url link: ", url)
    reponse = requests.get(url, proxies=proxies, headers=headers, timeout=(10, 20))
    soup = BeautifulSoup(reponse.text, "lxml")
    context = soup.find("div", id="package-list")
    lists = context.find_all("a")
    num = 1
    with open(sub_folder, "a+") as f:
        for list_1 in lists:
            if num <= 30:
                # Check if the link_tag is not None
                url_link = home_url + list_1['href']
                print("[+] download the apk:", url_link)
                f.write(url_link + "\n")
            num = num + 1


def downTxt(url, sub_folder):
    print("download the url link: ", url)
    reponse = requests.get(url, proxies=proxies, headers=headers, timeout=(10, 20))
    soup = BeautifulSoup(reponse.text, "lxml")
    context = soup.find("div", id="news-content")
    lists = context.find_all("div")
    num = 1
    with open(sub_folder, "a+") as f:
        for list_1 in lists:
            # print(list_1)
            if num <= 30:
                # purl = home_url + list_1.find("a")['href']
                # url_link = home_url + list_1.find('a', class_='post-link')['href']
                # Assuming list_1 is already defined and contains valid HTML content

                # Find the <a> tag
                # link_tag = list_1.find('a', class_='post-link')
                link_tag = list_1.find("a")

                # Check if the link_tag is not None
                if link_tag is not None and 'href' in link_tag.attrs:
                    url_link = home_url + link_tag['href']
                    print("[+] download the apk:", url_link)

                    # reponse1 = requests.get(url_link, proxies=proxies, headers=headers, timeout=(10, 20))
                    # selector = etree.HTML(reponse1.text)
                    # # print("74", selector)
                    # # # get the apk
                    # link = selector.xpath('//*[@id="latest"]/p[3]/b/a/@href')
                    # link = str(link)[2:-2]
                    # print(link)
                    f.write(url_link + "\n")


                # get the tar.gz
                # link1 = selector.xpath('//*[@id="latest"]/p[2]/a/@href')
                # link1 = str(link1)[2:-2]
                # print(link1)
            num = num + 1


def obtain_url_category():
    # Send a GET request to the URL using the specified proxies
    response = requests.get(url, proxies=proxies, headers=headers, timeout=(3, 10))
    # response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        # soup = BeautifulSoup(response.text, 'html.parser')
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

        # Find the div containing the post content
        post_content = soup.find('div', class_='post-content')

        # Get all <p> tags within the post content
        paragraphs = post_content.find_all('p')

        # List to store links and data
        links_and_data = []

        # Iterate through each <p> tag
        for p in paragraphs:
            # Get the text content of the <p> tag
            text = p.get_text(strip=True)
            # Find the first <a> tag within the <p> tag
            link = p.find('a')
            # Get the href attribute if the <a> tag exists
            link_url = link['href'] if link else None

            # Append the text and link to the list
            links_and_data.append({
                'category': get_last_segment(link_url),
                'num': extract_number(text),
                'link': generate_category_url(link_url)
            })

        # Print the collected text and links
        # for item in links_and_data:
        #     print(f"Category: {item['category']}, Num: {item['num']}, Link: {item['link']}")

        return links_and_data
    else:
        # Print an error message if the request failed
        print(f"Request failed, status code: {response.status_code}")


def main():
    # Attempt to obtain the category information
    try:
        print("\nStep1 >>> Obtain the category information")
        if os.path.exists(category_txt):
            print("the category file is exist.")
        else:
            links_and_data = obtain_url_category()
            with open(category_txt, "w") as f:
                for i in links_and_data:
                    f.write(i['category'] + '\n')
                    f.write(str(i['num']) + '\n')
                    f.write(i['link'] + '\n')
            print("obtain the category info.")

        print("\nStep2 >>> Download the apk link")
        # obtain the apk download link
        with open(category_txt, "r") as f:
            lines = f.readlines()
            for index, value in enumerate(lines):
                if index % 3 == 0:
                    # create the file
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)

                    sub_folder = os.path.join(folder_name, value.strip() + ".txt")
                    if not os.path.exists(sub_folder):
                        # os.makedirs(sub_folder)
                        with open(sub_folder, "w") as f:
                            f.write("")

                    print(f" [+] enter the {sub_folder} folder")
                elif index % 3 == 1:
                    # print(int(value.strip()))
                    # obtain the category apk num
                    x = ceil(int(value.strip()) / 30)
                    for j in range(1, x + 1):
                        base_url = lines[index + 1].strip()
                        print("download the " + str(j) + " page")
                        if j == 1:
                            downFirstTxt(base_url, sub_folder)
                        else:
                            url1 = base_url + str(j) + "/index.html"
                            downTxt(url1, sub_folder)

    except Exception as e:
        # Print any exceptions that occur
        # Get detailed information about the exception
        tb_info = traceback.extract_tb(e.__traceback__)
        # Get the last traceback information
        last_trace = tb_info[-1] if tb_info else None
        line_number = last_trace.lineno if last_trace else None
        print(f"An error occurred: {e}")
        print(f"Error occurred on line {line_number}")


if __name__ == "__main__":
    main()
