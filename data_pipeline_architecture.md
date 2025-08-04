# Kiến trúc Hệ thống Xử lý Dữ liệu

| ID  | Giai đoạn                    | Mô tả Yêu cầu                                                                                                                                                 | Công cụ Đề xuất                          |
| --- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| 1.0 | Thu thập Dữ liệu             | - Tự động gọi Amazon API để lấy dữ liệu (doanh thu, sản phẩm, tồn kho, marketing, v.v.) theo lịch trình <br> - Lưu file thô vào MinIO.                        | - Amazon API <br> - Airflow <br> - MinIO |
| 2.0 | Lưu trữ Dữ liệu              | - Thiết lập MinIO làm Data Lake để lưu dữ liệu thô <br> - PostgreSQL làm Data Warehouse cho dữ liệu đã được cấu trúc, sẵn sàng cho phân tích.                 | - MinIO <br> - PostgreSQL                |
| 3.0 | Xử lý & Chuyển đổi (ETL)     | - Xây dựng các script (Python) để đọc dữ liệu thô từ MinIO, thực hiện làm sạch, chuyển đổi <br> - Lưu dữ liệu đã được làm sạch vào các bảng trong PostgreSQL. | - Airflow <br> - Python                  |
| 4.0 | Điều phối & Giám sát         | - Sử dụng Airflow để điều phối toàn bộ pipeline (API -> MinIO -> PostgreSQL) <br> - Giám sát trạng thái và gửi cảnh báo khi có lỗi.                           | - Airflow                                |
| 5.0 | Quản lý & Triển khai (CI/CD) | - Lưu trữ toàn bộ code (DAGs, scripts) trên GitLab <br> - Dùng Jenkins để tự động kiểm tra và triển khai code mới lên môi trường Airflow.                     | - GitLab <br> - Jenkins                  |
| 6.0 | Truy cập & Phân tích         | - Kết nối các công cụ BI vào PostgreSQL để người dùng cuối có thể tự tạo báo cáo <br> - Dashboard với dữ liệu được làm mới tự động.                           | - PostgreSQL <br> - Power BI             |
