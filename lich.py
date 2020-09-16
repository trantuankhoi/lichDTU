from bs4 import BeautifulSoup, SoupStrainer
import requests

parameters = {
    'discipline' : 'CS',
    'keyword1':'316',
    'hocky' : '70',
    't': '1599613145426'
}

r = requests.get('http://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx', parameters)
soup = BeautifulSoup(r.text, 'html.parser')
url_sub = soup.find_all(class_='hit')[2]['href'] #link sau khi press Search

def XuLyUrlSub(url_sub: str) -> str:
    ##http://courses.duytan.edu.vn/Sites/Home_ChuongTrinhDaoTao.aspx?p=home_listcoursedetail&courseid=48&timespan=70&t=s
    ##http://courses.duytan.edu.vn/Sites/Home_ChuongTrinhDaoTao.aspx?p=home_listcoursedetail&courseid=48×pan=70&t=s    sửa cái này giống như cái trên

    url_sub = url_sub[6:]
    url_sub = "http://courses.duytan.edu.vn/" + url_sub
    replace = url_sub.find("pan") - 1
    url_sub_new = url_sub[:replace] + "&times" + url_sub[replace + 1:]
    return url_sub_new

url_sub = XuLyUrlSub(url_sub)
print(url_sub)

## Init info of sub
list_sub_name = []
list_sub_id = []
list_sub_time = []
list_sub_place = []
list_sub_teacher = []

def get_sub_name(url_sub: str) -> list:
    thu = 'http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid=55&semesterid=70&timespan=70'
    req = requests.get(thu)
    soup = BeautifulSoup(req.text, 'html.parser')
    list_sub_name = soup.find_all(class_="nhom-lop")
    return [str(td_tag.div.string).strip() for td_tag in list_sub_name]

list_sub_name = get_sub_name(url_sub)
print(list_sub_name)



