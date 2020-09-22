from bs4 import BeautifulSoup, SoupStrainer
import requests

parameters = {
    'discipline': 'CS',
    'keyword1': '316',
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

    #get sub time
    templst1 = soup.find_all(class_ = "lop")
    for tr_tag in templst1:
        temp1 = tr_tag.td
        temp1 = temp1.findNext("font").text
        list_sub_time.append(temp1)



    result = [list_sub_name, list_sub_id, list_sub_time, list_sub_place, list_sub_teacher]
    return result

print(Get_Data(url_sub))
