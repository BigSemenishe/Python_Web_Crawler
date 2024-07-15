import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
import psycopg2
from storage import url_storage

host = "localhost"
user = "postgres"
password = "uT#ookwKAEr98Bchuhie"
db_name = "postgres"

count = 0


def url_extractor(url):
    global connection, url_storage
    all_words = []
    all_links = []
    with open("data_selenium.html", encoding='utf-8') as file:
        response = file.read()
        soup = BeautifulSoup(response, "lxml")
        for link in soup.find_all("a"):
            lnk = urljoin(url, link.get("href"))
            if len(link.text) > 4:
                words = link.text
            else:
                words = "my_null"
            url_storage.append(lnk)
            all_words.append(words.strip())
            all_links.append(lnk.strip())

    i = 0
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    connection.autocommit = True
    print("[INFO] Successfully connected to my_bd!")
    while i < len(all_words):
        if all_words[i] == "my_null":
            i += 1
            continue
        try:
            with connection.cursor() as cursor:
                sql_insert_query = """ INSERT INTO my_bd (main_url, words, link) VALUES (%s, %s, %s)"""
                insert_tuple_1 = (url, all_words[i], all_links[i])
                cursor.execute(sql_insert_query, insert_tuple_1)
        except Exception as ex:
            print(" [ERROR] ", ex)
        i += 1
    connection.close()


def html_parser(url):
    global driver
    try:
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(5)
        for i in range(3):
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(5)
        with open("data_selenium.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        url_extractor(url)
        driver.close()

    except Exception as ex:
        print(" [ERROR] ", ex)
        print("Failed to parse the page!")
        if driver:
            driver.close()


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
    global url_storage, count, connection
    while True:
        command = input("What are you doing next?\n\nWork with url_storage:\n1. Exit\n2. Show \
url_storage\n3. Add url to url_storage\n4. Add a list of urls to url_storage\n5. Delete your url from url_storage\n6. \
Clean url_storage\n\nWork with HTML Parser:\n7. Parse all urls from url_storage and add everything into my_bd\n\n\
Work with my_bd:\n8. Show my_bd\n9. Clean my_bd\n10. Search by words in my_bd\n")
        match command.split():
            case ["1"]:
                print("Goodbye!")
                break
            case ["2"]:
                print("length :", len(url_storage), "\nurl_storage :")
                for element in url_storage:
                    print(element)
                print("\n________________________________")
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
                if len(url_storage) != 0:
                    amount_of_urls_to_parse = int(input("How many urls do you want to parse : "))
                    if amount_of_urls_to_parse <= len(url_storage):
                        while count != amount_of_urls_to_parse:
                            new_list = url_storage
                            url_storage = duplicate(new_list)
                            print("Cleared of duplicates. Keep going...\n")
                            length = len(url_storage)
                            html_parser(url_storage[count])
                            print(f"Link number {count} of {length} parsed successfully!\n")
                            count += 1
                        new_list = url_storage
                        url_storage = duplicate(new_list)
                        print("All pages have been parsed!\n________________________________")
                    else:
                        print("There are not enough urls in the url_storage\n________________________________")
                else:
                    print("Url_storage is empty\n________________________________")
            case ["8"]:
                try:
                    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                    print("[INFO] Successfully connected to my_bd!")
                    with connection.cursor() as cursor:
                        postgreSQL_select_Query = "SELECT * FROM my_bd"
                        cursor.execute(postgreSQL_select_Query)
                        info = cursor.fetchall()
                        print("     Main_url     |      Words      |      Link     ")
                        for row in info:
                            print(row[0], " | ", row[1], " | ", row[2], "\n")
                    connection.close()
                except Exception as ex:
                    print(" [ERROR] ", ex)
                print("\n________________________________")
            case ["9"]:
                try:
                    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                    print("[INFO] Successfully connected to my_bd!")
                    with connection.cursor() as cursor:
                        cursor.execute("""DELETE FROM my_bd""")
                        connection.commit()
                    connection.close()
                except Exception as ex:
                    print(" [ERROR] ", ex)
                print("Cleaned successfully!\n________________________________")
            case ["10"]:
                try:
                    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                    print("[INFO] Successfully connected to my_bd!")
                    with connection.cursor() as cursor:
                        postgreSQL_select_Query = "SELECT * FROM my_bd"
                        cursor.execute(postgreSQL_select_Query)
                        info = cursor.fetchall()
                        needed_words = input("What are the words to search for: ")
                        print("Here's what I found: ")
                        print("     Main_url     |      Words      |      Link     ")
                        for row in info:
                            if needed_words in row[1]:
                                print(row[0], " | ", row[1], " | ", row[2], "\n")
                    connection.close()
                except Exception as ex:
                    print(" [ERROR] ", ex)
                print("\n________________________________")
            case _:  # default
                print(f"Sorry, I couldn't understand {command!r}\n________________________________")

main()
# case ["7"]:
# Очищаем хранилище от дубликатов
# Берём ссылку из хранилища ссылок
# забираем её html код
# достаём из него все ссылки и ключевые слова
# ссылки добавляем в хранилище ссылок
# ключевые слова добавляем в мою базу данных рядом с ссылкой
