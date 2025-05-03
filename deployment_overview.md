# Tổng quan về Triển khai (Deployment) Ứng dụng Django

Chào bạn,

Hướng dẫn trước (`backend_setup_guide.md`) tập trung vào việc chạy ứng dụng trên máy cục bộ cho mục đích phát triển. Để đưa website từ thiện của bạn lên môi trường internet công cộng (production), bạn cần thực hiện các bước triển khai (deployment) phức tạp hơn. Dưới đây là tổng quan về các khái niệm và bước chính liên quan:

## 1. Chọn Nhà Cung cấp Dịch vụ Lưu trữ (Hosting Provider)

Nơi bạn sẽ chạy ứng dụng của mình. Có nhiều lựa chọn:

*   **Platform as a Service (PaaS):** Các nền tảng như Heroku, PythonAnywhere, Google App Engine đơn giản hóa quá trình triển khai bằng cách quản lý nhiều phần cơ sở hạ tầng cho bạn. Thường phù hợp cho người mới bắt đầu hoặc các dự án nhỏ/trung bình.
*   **Infrastructure as a Service (IaaS):** Các nhà cung cấp như AWS (EC2), Google Cloud (Compute Engine), DigitalOcean (Droplets) cung cấp máy chủ ảo. Bạn có toàn quyền kiểm soát nhưng cũng cần tự cấu hình mọi thứ (hệ điều hành, web server, database,...).
*   **Serverless:** Các dịch vụ như AWS Lambda, Google Cloud Functions cho phép chạy mã mà không cần quản lý server, nhưng có thể yêu cầu cấu trúc lại ứng dụng.

## 2. Cấu hình Cơ sở dữ liệu Production

SQLite không phù hợp cho môi trường production vì giới hạn về hiệu năng và khả năng xử lý đồng thời. Bạn nên chuyển sang một hệ quản trị cơ sở dữ liệu mạnh mẽ hơn như:

*   **PostgreSQL:** Lựa chọn phổ biến và được khuyến nghị cho Django.
*   **MySQL/MariaDB:** Cũng là lựa chọn tốt.

Bạn cần cài đặt và cấu hình cơ sở dữ liệu này trên server hoặc sử dụng dịch vụ cơ sở dữ liệu được quản lý (ví dụ: AWS RDS, Heroku Postgres).

## 3. Web Server Gateway Interface (WSGI) Server

Server phát triển (`manage.py runserver`) không đủ mạnh mẽ và an toàn cho production. Bạn cần một WSGI server chuyên dụng để chạy ứng dụng Django của bạn, ví dụ:

*   **Gunicorn:** Phổ biến, dễ sử dụng.
*   **uWSGI:** Mạnh mẽ, nhiều tùy chọn cấu hình.

WSGI server sẽ nhận yêu cầu từ client (thông qua reverse proxy) và chuyển tiếp chúng đến ứng dụng Django của bạn.

## 4. Reverse Proxy Server

Một web server như Nginx hoặc Apache thường được đặt trước WSGI server để hoạt động như một reverse proxy. Nhiệm vụ của nó bao gồm:

*   **Phục vụ tệp tĩnh (Static Files):** CSS, JavaScript, hình ảnh nên được phục vụ trực tiếp bởi Nginx/Apache để giảm tải cho ứng dụng Django.
*   **Caching:** Lưu trữ các phản hồi thường xuyên để tăng tốc độ.
*   **Load Balancing:** Phân phối yêu cầu đến nhiều instance của ứng dụng nếu cần.
*   **SSL/TLS Termination:** Xử lý mã hóa HTTPS.
*   **Chuyển tiếp yêu cầu:** Gửi các yêu cầu động (không phải tệp tĩnh) đến WSGI server (Gunicorn/uWSGI).

## 5. Quản lý Tệp Tĩnh (Static Files)

Trong production, bạn cần tập hợp tất cả các tệp tĩnh từ các ứng dụng Django và thư mục `static` chính vào một nơi duy nhất để reverse proxy có thể phục vụ chúng.

1.  Cấu hình `STATIC_ROOT` trong `settings.py` để chỉ định thư mục đích.
2.  Chạy lệnh: `python manage.py collectstatic`
3.  Cấu hình Nginx/Apache để phục vụ các tệp từ thư mục `STATIC_ROOT` này khi URL bắt đầu bằng `STATIC_URL`.

## 6. Cấu hình Bảo mật và Môi trường

*   **`DEBUG = False`:** **Rất quan trọng!** Đặt `DEBUG = False` trong `settings.py` để tránh lộ thông tin nhạy cảm khi có lỗi.
*   **`ALLOWED_HOSTS`:** Chỉ định các tên miền (domain) mà ứng dụng của bạn được phép phục vụ. Ví dụ: `ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']`.
*   **`SECRET_KEY`:** Giữ bí mật khóa này. Không bao giờ commit nó vào kho mã nguồn công khai. Sử dụng biến môi trường hoặc các hệ thống quản lý bí mật.
*   **Biến Môi trường:** Lưu trữ các cài đặt nhạy cảm (khóa API, mật khẩu database, `SECRET_KEY`) trong biến môi trường thay vì viết trực tiếp vào code.
*   **HTTPS:** Cấu hình SSL/TLS (thường tại reverse proxy) để mã hóa toàn bộ lưu lượng truy cập.

## 7. Quy trình Triển khai Tự động (Optional)

Để việc cập nhật ứng dụng dễ dàng hơn, bạn có thể thiết lập các quy trình CI/CD (Continuous Integration/Continuous Deployment) sử dụng các công cụ như GitHub Actions, GitLab CI, Jenkins để tự động hóa việc kiểm thử, build, và triển khai mã nguồn mới lên server.

---

Triển khai một ứng dụng Django là một quá trình gồm nhiều bước và đòi hỏi kiến thức về quản trị hệ thống. Hướng dẫn chi tiết sẽ phụ thuộc rất nhiều vào nhà cung cấp dịch vụ lưu trữ và các công nghệ cụ thể bạn chọn.

Nếu bạn quyết định triển khai ứng dụng này, tôi có thể cung cấp hướng dẫn chi tiết hơn cho một nền tảng cụ thể (ví dụ: Heroku hoặc DigitalOcean với Gunicorn và Nginx) nếu bạn cho biết lựa chọn của mình.
