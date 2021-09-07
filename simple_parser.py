import time
import requests
from bs4 import BeautifulSoup as bs
from pony.orm import *
import logging
from tkinter import *
import tkinter.scrolledtext
import unittest

log = logging.getLogger("news")
log.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(funcName)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
log.addHandler(sh)

db = Database()


class News(db.Entity):
    date = Required(str)
    news = Required(str)
    link = Required(str)


db.bind(provider="postgres", user="test", password="12345678", host="localhost", database="news1")
db.generate_mapping(create_tables=True)


@db_session
def write_db(date, news, link):
    for r in News.select(lambda p: p.link == link):
        if link == r.link:
            print("такая запись уже существует")
            log.warning(f"запись '{news}' не добавлена, т.к. уже присутствует в базе")
            break
    else:
        News(date=date, news=news, link=link)
        log.info(f"запись '{news}' добавлена в базу")


@db_session
def get_news_count_from_db(date):
    # news_count = len(News.select(lambda p: p.date == date)[:])
    print(type(News))
    news_count = count(n for n in News if n.date == date)
    print(news_count)
    return news_count


@db_session
def read_db(date):
    news_db = News.select(lambda p: p.date == date)[:]
    return news_db


@db_session
def exist_news(date):
    exist_or_not = News.exists(date=date)
    return exist_or_not

@db_session
def delete_news(date):
    News.select(date=date).delete()

def get_news_from_db(date):
    ltxt.delete("1.0", END)
    log.info(f"выводим данные за {date}")
    news_count = get_news_count_from_db(date=date)
    if news_count != 0:
        news_db = read_db(date=date)
        for r in news_db:
            ltxt.insert(INSERT, date)
            ltxt.insert(INSERT, " ")
            ltxt.insert(INSERT, r.news)
            ltxt.insert(INSERT, "\n")
            ltxt.insert(INSERT, r.link)
            ltxt.insert(INSERT, "\n")
            ltxt.insert(INSERT, "-----")
            ltxt.insert(INSERT, "\n")
    else:
        ltxt.insert(INSERT, f"Новостей за данную дату {date} нет")


def request_data():
    res = requests.get(url="https://lenta.ru")
    if res.status_code == 200:
        html_doc = bs(res.text, features="html.parser")
        name_of_new = html_doc.findAll("a", class_="titles")

        for name in name_of_new:
            url = name.get("href")
            if url.split("/")[3] != time.strftime("%m") or url.split("/")[4] != time.strftime("%d"):
                continue
            main_url = "https://lenta.ru" + name["href"]
            news = name.text
            date = time.strftime("%d/%m/%Y")
            write_db(date=date, news=news, link=main_url)
        ltxt.delete("1.0", END)
        ltxt.insert(INSERT, "Done")


def click_parse():
    request_data()


def click_read_db():
    day = day_entry.get()
    month = month_entry.get()
    date = day + "/" + month + "/" + "2021"
    print(f"date_read {date}")
    get_news_from_db(date=date)


window = Tk()
window.title("Simple parser")
window.geometry("1000x500")
lbl_day = Label(master=window, text="Число")
lbl_day.place(x=720, y=55)
lbl_month = Label(master=window, text="Месяц")
lbl_month.place(x=810, y=55)
btn_parse = Button(master=window, width=10, height=1, text="Parse", bg="green", fg="yellow", command=click_parse)
btn_parse.place(x=900, y=10)
btn_read_db = Button(master=window, width=10, height=1, text="Read DB", bg="green", fg="yellow", command=click_read_db)
btn_read_db.place(x=900, y=50)
day_entry = Entry(master=window, width=2)
day_entry.place(x=770, y=55)
month_entry = Entry(master=window, width=2)
month_entry.place(x=860, y=55)
ltxt = tkinter.scrolledtext.ScrolledText(master=window)
ltxt.place(x=1, y=1)
window.mainloop()

# class Tests(unittest.TestCase):
#     def test_write_exist_db(self):
#         delete_news(date="00/00/0000")
#         write_db(date="00/00/0000", news="test_news", link="test_link")
#         exist = exist_news(date="00/00/0000")
#         self.assertEqual(exist, True)
#
#     def test_read_db(self):
#         test_news = read_db(date="00/00/0000")
#         self.assertEqual(test_news[0].date, "00/00/0000")
#
# 
# if __name__ == "__main__":
#     unittest.main()
