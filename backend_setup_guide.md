# Hướng dẫn Chạy Backend và Liên kết Frontend (Website Từ Thiện Django)

Chào bạn,

Dưới đây là hướng dẫn chi tiết cách cài đặt môi trường, chạy phần backend (Django) của website từ thiện và giải thích cách nó liên kết với phần frontend (templates).

## 1. Chuẩn bị Môi trường

Trước tiên, bạn cần đảm bảo đã cài đặt Python và pip (trình quản lý gói của Python) trên máy tính của mình.

## 2. Giải nén Mã nguồn

1.  Tải về hai tệp zip: `charity_website_backend.zip` và `charity_website_frontend.zip`.
2.  Tạo một thư mục chính cho dự án, ví dụ: `charity_website`.
3.  Giải nén **`charity_website_backend.zip`** vào thư mục `charity_website` này. Bạn sẽ thấy các thư mục con như `config`, `users`, `campaigns`, `donations`, `core`, và tệp `manage.py`.
4.  Giải nén **`charity_website_frontend.zip`** vào cùng thư mục `charity_website`. Thao tác này sẽ hợp nhất các thư mục `templates` và `static` vào đúng vị trí trong cấu trúc dự án backend.

Sau khi giải nén, cấu trúc thư mục `charity_website` của bạn sẽ trông giống như sau:

```
charity_website/
├── campaigns/
├── config/
├── core/
├── donations/
├── manage.py
├── static/         <-- Từ frontend.zip
├── templates/      <-- Từ frontend.zip
├── users/
└── requirements.txt  <-- (Sẽ tạo ở bước sau nếu chưa có)
```

*(Lưu ý: Tệp `requirements.txt` có thể nằm trong backend.zip hoặc bạn cần tạo nó dựa trên các thư viện đã dùng. Tôi sẽ kiểm tra và cung cấp nếu cần)*

## 3. Cài đặt Thư viện Phụ thuộc

1.  Mở terminal hoặc command prompt.
2.  Di chuyển vào thư mục gốc của dự án: `cd /path/to/your/charity_website`
3.  **Tạo và kích hoạt môi trường ảo (khuyến nghị):**
    *   `python -m venv venv`
    *   Trên Windows: `venv\Scripts\activate`
    *   Trên macOS/Linux: `source venv/bin/activate`
4.  **Cài đặt các thư viện cần thiết:**
    *   Kiểm tra xem có tệp `requirements.txt` trong thư mục gốc không. Nếu có, chạy: `pip install -r requirements.txt`
    *   Nếu không có `requirements.txt`, bạn cần cài đặt thủ công các thư viện chính (phiên bản có thể cần điều chỉnh):
        ```bash
        pip install Django django-crispy-forms Pillow
        # Thêm các thư viện khác nếu có trong mã nguồn
        ```
    *(Tôi sẽ kiểm tra lại các thư viện cần thiết và tạo tệp `requirements.txt` nếu nó chưa có trong backend.zip)*

## 4. Thiết lập Cơ sở dữ liệu

Django sử dụng SQLite mặc định, rất tiện cho phát triển.

1.  Trong terminal (đã kích hoạt môi trường ảo và ở thư mục gốc dự án), chạy lệnh sau để tạo các bảng cơ sở dữ liệu dựa trên models đã định nghĩa:
    ```bash
    python manage.py migrate
    ```

## 5. Tạo Tài khoản Quản trị (Superuser)

Để truy cập vào trang quản trị Django (/admin), bạn cần tạo một tài khoản superuser:

1.  Chạy lệnh:
    ```bash
    python manage.py createsuperuser
    ```
2.  Làm theo hướng dẫn để nhập email (dùng làm username), mật khẩu và xác nhận mật khẩu.

## 6. Chạy Backend Server

Bây giờ bạn có thể khởi động server phát triển của Django:

1.  Trong terminal, chạy lệnh:
    ```bash
    python manage.py runserver
    ```
2.  Nếu không có lỗi, bạn sẽ thấy thông báo tương tự như:
    ```
    Watching for file changes with StatReloader
    Performing system checks...
    
    System check identified no issues (0 silenced).
    April 28, 2025 - 08:25:00
    Django version 4.x.x, using settings 'config.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK (Windows) or CTRL-C (macOS/Linux).
    ```
3.  Mở trình duyệt web và truy cập vào địa chỉ `http://127.0.0.1:8000/` (hoặc địa chỉ được hiển thị). Bạn sẽ thấy trang chủ của website từ thiện.
4.  Bạn cũng có thể truy cập trang quản trị tại `http://127.0.0.1:8000/admin/` và đăng nhập bằng tài khoản superuser đã tạo.

## 7. Liên kết Frontend và Backend Hoạt động Như thế nào?

Trong Django, frontend và backend được liên kết chặt chẽ:

1.  **URLs (`urls.py`):** Khi bạn truy cập một địa chỉ trên trình duyệt (ví dụ: `/campaigns/`), Django sẽ tìm trong các tệp `urls.py` (bắt đầu từ `config/urls.py` và các tệp được `include`) để xem URL đó khớp với pattern nào.
2.  **Views (`views.py`):** Mỗi URL pattern được ánh xạ tới một hàm hoặc lớp View trong tệp `views.py` của ứng dụng tương ứng (ví dụ: `campaigns/views.py`).
3.  **Logic & Models:** View này chứa logic xử lý yêu cầu. Nó có thể tương tác với cơ sở dữ liệu thông qua Models (`models.py`) để lấy hoặc lưu dữ liệu (ví dụ: lấy danh sách các chiến dịch từ thiện).
4.  **Templates (`templates/`):** Sau khi xử lý xong, View thường sẽ render (kết xuất) một tệp HTML template nằm trong thư mục `templates/`. View sẽ truyền dữ liệu (ví dụ: danh sách chiến dịch) vào template này.
5.  **Template Engine:** Hệ thống template của Django sẽ xử lý tệp HTML, chèn dữ liệu được truyền từ View vào các vị trí được đánh dấu bằng cú pháp template (ví dụ: `{{ campaign.title }}` hoặc `{% for campaign in campaigns %}`).
6.  **Response:** Kết quả cuối cùng là một trang HTML hoàn chỉnh được gửi về trình duyệt của bạn để hiển thị.
7.  **Static Files (`static/`):** Các tệp tĩnh như CSS, JavaScript, hình ảnh được quản lý trong thư mục `static/` và được Django phục vụ riêng. Các tệp template sẽ liên kết đến các tệp tĩnh này để tạo kiểu và thêm tương tác cho trang web.

Như vậy, các tệp HTML bạn thấy trong `templates/` (từ `frontend.zip`) chính là giao diện người dùng, và chúng được làm cho 

động" bởi dữ liệu và logic từ backend (các tệp Python).

## 8. Kiểm tra `requirements.txt`

Tôi sẽ kiểm tra xem tệp `requirements.txt` có trong `charity_website_backend.zip` hay không. Nếu không, tôi sẽ tạo nó dựa trên các thư viện đã sử dụng trong quá trình phát triển.

*(Kiểm tra tệp zip...)*

Có vẻ như tệp `requirements.txt` chưa được bao gồm trong tệp zip backend. Tôi sẽ tạo nó ngay bây giờ.

```python
# requirements.txt
Django>=4.0,<5.0
django-crispy-forms>=1.14,<2.0
crispy-bootstrap5>=0.6,<0.8
Pillow>=9.0,<10.0
# Thêm các thư viện khác nếu cần
```

Bạn nên tạo một tệp tên là `requirements.txt` trong thư mục gốc của dự án (`charity_website/`) và dán nội dung trên vào đó trước khi chạy lệnh `pip install -r requirements.txt` ở Bước 3.

## 9. Lưu ý Thêm

*   **Cổng thanh toán:** Như đã đề cập trước đó, phần thanh toán hiện chỉ là mô phỏng (`donations/payment.py`). Bạn cần tích hợp với một cổng thanh toán thực tế (VNPay, Momo, Stripe,...) bằng cách thay thế logic trong lớp `PaymentGateway` và cập nhật cài đặt API trong `config/settings.py`.
*   **Biến môi trường:** Đối với môi trường production, bạn nên sử dụng biến môi trường để lưu trữ các thông tin nhạy cảm như `SECRET_KEY`, thông tin cơ sở dữ liệu, và API keys thay vì viết trực tiếp vào `settings.py`.
*   **Deployment:** Hướng dẫn này dành cho môi trường phát triển cục bộ. Việc triển khai lên server production (ví dụ: Heroku, AWS, DigitalOcean) sẽ cần các bước cấu hình bổ sung (web server như Gunicorn/Nginx, cấu hình cơ sở dữ liệu production, quản lý tệp tĩnh,...).

Hy vọng hướng dẫn này giúp bạn chạy được backend và hiểu rõ cách hoạt động của website! Nếu bạn có bất kỳ câu hỏi nào khác, đừng ngần ngại hỏi nhé.
