# LichDTU

TÊN BIẾN:
- parameters: lưu thông tin input, hay dùng trong thư viện requests
- url_sub: link sau khi nhấn nút tìm kiếm
- list_sub...: danh sách thông tin môn học như tên, mã lớp, thời gian, giảng viên được sắp xếp cố định theo list trong url sub

MỤC TIÊU:
- Nhập thông tin ở parameters vào http://courses.duytan.edu.vn/Sites/Home_ChuongTrinhDaoTao.aspx?p=home_coursesearch, sau đó ta được link ở url sub,
bước này thực hiện ở dòng 11, 12, 13
- Ta được url_sub nhưng chưa hoàn chỉnh nên phải thực hiện hàm XuLyUrlSub để có link như mẫu
- Khởi tạo các list để lưu thông tin môn học như tên, mã lớp, ... với số list tùy thuộc vào chức năng, có thể bổ sung thêm
- Hàm get_url_name dùng để lưu tên môn học như CS 316 A, CS 316 AA, CS 316 C trong link 
  http://courses.duytan.edu.vn/Sites/Home_ChuongTrinhDaoTao.aspx?p=home_listcoursedetail&courseid=55&timespan=70&t=s
 - Tương tự với list_sub_id, list_sub_time,...
 Nhưng mà t bị bí đoạn ni mấy ngày r :(
