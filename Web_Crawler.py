import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from storage import url_storage
from storage import my_bd


count = 0


def url_extractor(url):
    global my_bd
    all_words = []
    with open("data_selenium.html", encoding='utf-8') as file:
        response = file.read()
        soup = BeautifulSoup(response, "lxml")
        for link in soup.find_all("a"):
            lnk = urljoin(url, link.get("href"))
            url_storage.append(lnk)
            word = link.text
            all_words.append(word)
    my_dict = {"link": url, "words": all_words}
    my_bd.append(my_dict)


def html_parser(url):
    try:
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(5)
        with open("data_selenium.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        url_extractor(url)
        driver.close()
    except Exception as ex:
        print(ex)
        print("Page parsed unsuccessfully!")


def duplicate(lst):
    seen = {}
    new_list = [seen.setdefault(x, x) for x in lst if x not in seen]
    return new_list


def add_list_of_urls_to_url_storage():
    user_url = input("Write your list of urls, use ',' as a whitespace: ").split(',')
    url_storage.extend(user_url)


def add_url_to_url_storage():
    user_url = input("Write your url: ")
    url_storage.append(user_url)


def delete_your_url_from_url_storage():
    user_url = input("Write your url: ")
    if user_url in url_storage:
        url_storage.pop(url_storage.index(user_url))


def clear_url_storage(lst):
    if len(lst) > 0:
        while len(lst) > 0:
            lst.pop(-1)


def main():
    global url_storage
    global count
    while True:
        command = input("What are you doing next?\n\nWork with url_storage:\n1. Exit\n2. Show \
url_storage\n3. Add url to url_storage\n4. Add a list of urls to url_storage\n5. Delete your url from url_storage\n6. \
Clear url_storage\n\nWork with HTML Parser:\n7. Parse all urls from url_storage\n")
        match command.split():
            case ["1"]:
                print("Goodbye!")
                break
            case ["2"]:
                print(url_storage, "\n________________________________")
            case ["3"]:
                add_url_to_url_storage()
                print("Successfully!\n________________________________")
            case ["4"]:
                add_list_of_urls_to_url_storage()
                print("Successfully!\n________________________________")
            case ["5"]:
                delete_your_url_from_url_storage()
                print("Successfully!\n________________________________")
            case ["6"]:
                clear_url_storage(url_storage)
                print("Successfully!\n________________________________")
            case ["7"]:
                while count < len(url_storage):
                    new_list = url_storage
                    url_storage = duplicate(new_list)
                    print("Cleared of duplicates. Keep going...\n")
                    length = len(url_storage)
                    html_parser(url_storage[count])
                    print(f"Link number {count} of {length} parsed successfully!\n")
                    count += 1
                print("There are no pages left in the url_storage for parsing")

            case _:  # default
                print(f"Sorry, I couldn't understand {command!r}\n________________________________")


main()
# Очищаем хранилище от дубликатов
# Берём ссылку из хранилища ссылок
# забираем её html код
# достаём из него все ссылки и ключевые слова
# ссылки добавляем в хранилище ссылок
# ключевые слова добавляем в мою базу данных рядом с ссылкой
