import requests, datetime
from bs4 import BeautifulSoup

def month_converter(month):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
              'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    return months.index(month) + 1


def url_get_items(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "lxml")
    calendars = soup.find('div', {'class': 'row'})
    items = calendars.find_all('div', {'class': 'col-md-3'})
    return items


def items_get_date(items):
    weekends = []
    for item in items:
        weekend = []
        month = item.find('th', {'class': 'month'})
        weekends_html = item.find_all('td', {'class': ['weekend', 'holiday weekend']})
        if month != None:
            for weekend_html in weekends_html:
                weekend.append(weekend_html.text)

            weekends.append([month_converter(month.text), weekend])

    return weekends


def write_to_file(weekends):
    dt_obj = datetime.datetime.now()
    dt_string = dt_obj.strftime("%Y")
    file = open("hds{}.txt".format(dt_string), 'w')
    for month, days in weekends:
        file.write(str(month))
        for day in days:
            file.write(" {}".format(day))

        file.write("\n")
    file.close()


if __name__ == "__main__":
    url = 'http://www.consultant.ru/law/ref/calendar/proizvodstvennye/#shortday'
    items = url_get_items(url)
    weekends = items_get_date(items)
    write_to_file(weekends)

