AGRI AI CLOUD DEMO - BẢN CÔNG KHAI CHỈ XEM
===========================================

MỤC ĐÍCH
--------
Đây là bản demo công khai dùng để trình diễn giao diện AgriAI.
TẤT CẢ SỐ LIỆU ĐỀU LÀ GIẢ LẬP, KHÔNG PHẢI KẾT QUẢ THỰC NGHIỆM.

AN TOÀN DỮ LIỆU
---------------
- Không chứa agriai_demo.sqlite3.
- Không chứa thư mục uploads hoặc ảnh thí nghiệm.
- Không chứa weights/best.pt hoặc trọng số AI khác.
- Không có form tải ảnh, form nhập dữ liệu hay thao tác ghi dữ liệu.
- Các bộ lọc và điều khiển chỉ thay đổi phần hiển thị trong phiên xem.

CÁC TỆP CẦN ĐƯA LÊN GITHUB
--------------------------
Chỉ tải 3 tệp ở thư mục này:
1. app.py
2. requirements.txt
3. README_VI.txt (tùy chọn)

KHÔNG tải lên các tệp hoặc thư mục của bản nghiên cứu cục bộ, nhất là:
- agriai_demo.sqlite3
- uploads/
- weights/
- Ảnh gốc của mẫu nghiên cứu
- Tệp secrets, mật khẩu, token hoặc thông tin cá nhân

CHẠY THỬ TRÊN MÁY TÍNH (NẾU ĐÃ CÓ PYTHON)
-----------------------------------------
pip install -r requirements.txt
streamlit run app.py

TRIỂN KHAI LÊN STREAMLIT COMMUNITY CLOUD
----------------------------------------
1. Tạo một GitHub repository RIÊNG cho bản demo này; chọn Private.
2. Chỉ upload app.py và requirements.txt (có thể thêm README_VI.txt).
3. Vào https://share.streamlit.io và đăng nhập bằng GitHub.
4. Nếu cần, cấp quyền cho Streamlit truy cập repository Private.
5. Chọn Create app > Yup, I have an app.
6. Chọn repository vừa tạo, branch main, file path app.py.
7. Deploy.
8. Sau khi triển khai, vào App settings > Sharing.
9. Chọn "This app is public and searchable" nếu muốn bất kỳ ai có link đều mở được.
10. Thử mở link ở cửa sổ ẩn danh hoặc trên điện thoại chưa đăng nhập.

LƯU Ý
-----
Repository Private giúp giữ mã nguồn khỏi công khai. Nếu đặt ứng dụng Public,
người có link có thể xem giao diện và dữ liệu giả lập. Hãy kiểm tra lại repo
trước khi triển khai. Ứng dụng này không dùng dữ liệu nghiên cứu thật.
