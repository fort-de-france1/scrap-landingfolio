import json
import os
import time
import requests
# from bs4 import BeautifulSoup

# JSON request
# https://s3.landingfolio.com/inspiration?page=1&sortBy=free-first

headers = {
    "Accept": "image/avif,image/webp,*/*",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) "
                  "Gecko/20100101 Firefox/107.0"

}


def get_data_file(headers):
    """
    Collect data and return a JSON file
    """
    # Send request and save page

    # url = "https://www.landingfolio.com/"
    # r = requests.get(url=url, headers=headers)
    # with open("index.html", "w", encoding="utf-8") as f:
    #     f.write(r.text)

    # with open("index.html") as file:
    #     src = file.read()
    # soup = BeautifulSoup(src, "lxml")
    #
    # pictures = soup.find_all("div", class_="relative group text-center")
    # num = 1
    # for pic in pictures:
    #     link = f"{num} https://www.landingfolio.com" + pic.find("a")["href"]
    #     print(link)
    #     num += 1

    page = 1
    images_count = 0
    result_list = []
    url_image = "https://landingfoliocom.imgix.net/"

    while True:
    # while page <= 2:
        url = f"https://s3.landingfolio.com/inspiration?page={page}&sortBy=free-first"
        response = requests.get(url=url, headers=headers)
        data = response.json()

        if len(data) > 0:
            for item in data:

                desktop_list = []
                mobile_list = []
                title_list = []

                screenshot = item.get("screenshots")

                for pic in screenshot:

                    img_list = pic.get("images")
                    desktop = url_image + img_list.get("desktop")
                    title = pic.get("title")

                    try:
                        mobile = url_image + img_list.get("mobile")
                        mobile_list.append(mobile)
                    except Exception:
                        pass

                    desktop_list.append(desktop)
                    title_list.append(title)

                images_count += len(desktop_list)
                try:
                    images_count += len(mobile_list)
                except Exception:
                    pass

                result_list.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "images": {
                        "desktop": desktop_list,
                        "mobile": mobile_list,
                        "title": title_list
                    },
                })
            print(f"[+] Collect #{page}")
            page += 1
            print(f"[+] Total images collected: {images_count}")
        else:
            with open("result_list.json", "a") as file:
                json.dump(result_list, file, indent=4, ensure_ascii=False)
            return f"[INFO] Work finished"


def download_images(file_path):
    """Download images"""
    try:
        with open(file_path) as file:
            src = json.load(file)
    except Exception as ex:
        return "[INFO] Invalid File path"
    items_len = len(src)
    count = 1

    for item in src[:100]:
        idx = 0
        dir_name = item.get("title")
        desktop = item.get("images").get("desktop")
        mobile = item.get("images").get("mobile")
        title = item.get("images").get("title")

        # Mkdir "data" to collect items
        if not os.path.exists(f"data/{dir_name}"):
            os.mkdir(f"data/{dir_name}")

        for img in desktop:
            r = requests.get(url=img)
            with open(f"data/{dir_name}/{title[idx]}-desktop.png", "wb") as file:
                file.write(r.content)

        try:
            for img in mobile:
                r = requests.get(url=img)
                with open(f"data/{dir_name}/{title[idx]}-mobile.png", "wb") as file:
                    file.write(r.content)
                idx += 1
        except Exception:
            idx += 1

        print(f"[+] Download {count} / {items_len}")
        count += 1
    return "[INFO] Work finished"


def main():
    start_time = time.time()
    # print(get_data_file(headers=headers))
    # print(download_images("result_list.json"))
    end_time = time.time()
    print(f"[INFO] Time process: {end_time - start_time}")


if __name__ == "__main__":
    main()
