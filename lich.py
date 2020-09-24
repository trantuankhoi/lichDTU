from bs4 import BeautifulSoup, SoupStrainer
import requests
from xlwt import Workbook
import re
import pandas as pd

parameters = {
    'discipline': 'ENG',
    'keyword1': '116',
    'hocky': '70',
    't': '1599613145426'
}

r = requests.get(
    'http://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx', parameters)
soup = BeautifulSoup(r.text, 'html.parser')
url_sub = soup.find_all(class_='hit')[2]['href']  # link sau khi press Search


def XuLyUrlSub(url_sub: str) -> str:
    # http://courses.duytan.edu.vn/Sites/Home_ChuongTrinhDaoTao.aspx?p=home_listcoursedetail&courseid=55&timespan=70&t=s
    # http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid=55&semesterid=70&timespan=70
    url = "http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid=55&semesterid=70&timespan=70"
    courseid = url_sub[73:url_sub.find("×pan")]
    return url.replace(url[85:87], courseid)


url_sub = XuLyUrlSub(url_sub)
print(url_sub)

'''
# Init info of sub
list_sub_name = []
list_sub_id = []
list_sub_time = []
list_sub_place = []
list_sub_teacher = []


def get_sub_name(url_sub: str) -> list:
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    list_sub_name = soup.find_all(class_="nhom-lop")
    return [str(td_tag.div.string).strip() for td_tag in list_sub_name]


list_sub_name = get_sub_name(url_sub)
print(list_sub_name)


def get_sub_id(url_sub: str):
    result = []
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    list_sub_id = soup.find_all(class_="lop")
    for tr_tag in list_sub_id:
        temp = tr_tag.td.a
        td_tag = temp.parent
        next_td_tag = td_tag.findNext("td")
        result.append(next_td_tag)
    return result


print(get_sub_id(url_sub)) '''


def Get_Data(url_sub: str):
    # init list
    list_sub_name = []
    list_sub_id = []
    list_sub_date = []
    list_sub_time = []
    list_sub_place = []
    list_sub_teacher = []    

    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')

    # get sub name
    temp = soup.find_all(class_="nhom-lop")
    list_sub_name =  [str(td_tag.div.string).strip() for td_tag in temp]

    # get sub ID
    templst = soup.find_all(class_="lop")
    for tr_tag in templst:
        temp = tr_tag.td.a
        td_tag = temp.parent
        next_td_tag = td_tag.findNext("td")
        list_sub_id.append(str(next_td_tag.text).strip())
    for mem in list_sub_id:
        if mem == "":
            list_sub_id.remove(mem)

    # get sub date
    templst = soup.find_all(style = "font-weight:normal; color:#4682B4;")
    for mem in templst:
        if mem.text != "":
            list_sub_date.append(mem.text)

    # get sub time
    templst = soup.find_all("font", style = "font-weight:normal; color:#4682B4;")
    for mem in templst:
        td_tag = mem.parent
        br_tag = td_tag.br
        date = br_tag.previous_element
        list_sub_time.append(date)

    # get sub place and teacher
    templst = soup.find_all(style = "text-align: center; vertical-align: top;")
    for mem in templst:
        temp = mem.findNext("td")
        temp1 = temp.get_text()
        list_sub_place.append(str(temp1))

    # get sub lec
    templst = soup.find(style = "width: 130px;")
    for mem in templst:
        tr_tag = mem.parent
        tr_tag_next = tr_tag.findNext("tr")
        tinchi = str(tr_tag_next.text).strip()
    key = tinchi.find("(")
    tinchi = int(tinchi[key+1])
    Lec = []
    for i in range(0, len(list_sub_id)):
        Lec.append(tinchi)

    f = len(list_sub_date)/ len(list_sub_name) # số buổi học trong 1 tuần (tần số)
    F = [f]*len(list_sub_id)
    # Lec (result[6]) là số tín chỉ
    result = [list_sub_name, list_sub_id, F,list_sub_date, list_sub_time, list_sub_place, Lec]
    return result

info = Get_Data(url_sub)

def init_excel(info: list):
    wb = Workbook()
    sheet1 = wb.add_sheet("sheet 1")

    # hàng trước cột sau
    sheet1.write(0, 0, "STT")
    sheet1.write(0, 1, "Name")
    sheet1.write(0, 2, "ID")
    sheet1.write(0, 3, "Date")
    sheet1.write(0, 4, "Time")
    sheet1.write(0, 5, "Place")
    sheet1.write(0, 6, "Instructor")
    sheet1.write(0, 7, "Lec")
    sheet1.write(0, 8, "F")

    # dán dữ liệu trong info vào excel
    row = 1
    col = 0
    n = len(info[0])
    for i in range(0, n):
        sheet1.write(row + i, col + 0, i + 1)
        sheet1.write(row + i, col + 1, info[0][i]) # name trong list la 0
        sheet1.write(row + i, col + 2, info[1][i]) # id
        sheet1.write(row + i, col + 3, info[3][i]) # date
        sheet1.write(row + i, col + 4, re.sub('[ ]+', ' ', info[4][i].rstrip().lstrip())) # time
        sheet1.write(row + i, col + 6, re.sub('([\n\r])', ' ', info[5][2 * i + 1].strip()))
        sheet1.write(row + i, col + 5, re.sub('([\n\r])', ' ', info[5][2 * i].strip())) # place
        sheet1.write(row + i, col + 7, info[6][i]) # Lec
        sheet1.write(row + i, col + 8, info[2][i]) # F

    wb.save("info.xls") 

init_excel(info)
print("Init excel file!")

