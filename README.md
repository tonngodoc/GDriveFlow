# 🌊 GDrive Flow (v1.9.0) - Windows Desktop Application

![GDrive Flow Logo](icon.png)

**Phát triển bởi TÔN NGỘ ĐỘC (Developed by TON NGO DOC)**

Ứng dụng Windows Desktop thuần giúp tự động tải xuống danh sách tệp hoặc toàn bộ thư mục (folder) trên Google Drive về máy tính cá nhân.

---

## ✨ Tính Năng Nổi Bật (Phiên Bản v1.9.0)

1. **Đổi Tên Thương Hiệu & Logo Mới (GDrive Flow Branding)**:
   - Chính thức đổi tên ứng dụng và GitHub Repository thành **GDrive Flow**.
   - Thiết kế Logo thương hiệu kết hợp biểu tượng Google Drive và luồng tải sóng động hiện đại.
2. **Tối Ưu Bộ Chuyển Đổi Ngôn Ngữ Tinh Gọn**:
   - Chuyển đổi ngôn ngữ rút gọn hiển thị bằng biểu tượng cờ (`🇻🇳` / `🇬🇧`) tinh tế, tối ưu diện tích giao diện.
3. **Tính Năng Báo Lỗi Ứng Dụng (Interactive Bug Report)**:
   - Nút **`🐛 Báo Lỗi`** (**`🐛 Report Bug`**) mở popup báo cáo sự cố trực tiếp.
   - Hỗ trợ sao chép toàn bộ nhật ký lỗi (Error Logs) và liên kết nhanh đến **GitHub Issues**.
4. **Chuẩn Hóa Song Ngữ 100% (100% Full Bilingual VI/EN)**:
   - Dịch toàn bộ nhật ký hệ thống (Logs Console), nhãn trạng thái cây thư mục, thẻ tiến trình (Badge), và các hộp thoại thông báo sang Tiếng Anh hoàn chỉnh khi chuyển đổi ngôn ngữ.
5. **Khắc Phục Lỗi Dừng Tải & Treo Đơ Giao Diện (Instant Cancellation & Unblocking)**:
   - Sử dụng lớp ngoại lệ đặc biệt `DownloadCancelledException` thoát lập tức khỏi vòng lặp tải `gdown` mà không bị gdown thử lại trong vô hạn.
   - Khi bấm **`🛑 Dừng Tải`**, giao diện lập tức phản hồi và mở lại các nút chức năng trong 0.001s, không gây đơ treo ứng dụng.
6. **Thông Tin Tác Giả & Bản Quyền**:
   - Ghi nhận thông tin chính thức: **Phát triển bởi TÔN NGỘ ĐỘC**.
7. **Tính Năng Tải Lại Các File Lỗi (Retry Failed Downloads)**:
   - Nút **`🔄 Tải Lại File Lỗi`** tự động lọc và tải lại toàn bộ các file bị đứt nối mạng hoặc lỗi.
8. **Tự Động Chuẩn Hóa Tên File (Filename Sanitization)**:
   - Tự động thay thế các ký tự đặc biệt không hợp lệ trên Windows (như `:`, `'`, `$`, `!`, `?`, `*`, `<`, `>`, `|`, `"`, `/`, `\`) thành dấu gạch dưới `_`.

---

## 📋 Lịch Sử Phiên Bản (Changelog)

- **v1.9.0 (Hiện tại)**:
  - Đổi tên chính thức thành **GDrive Flow**.
  - Thiết kế và tích hợp Logo thương hiệu mới.
  - Rút gọn nút chuyển ngôn ngữ chỉ hiển thị lá cờ (`🇻🇳` / `🇬🇧`).
- **v1.8.0**:
  - Thêm tính năng **`🐛 Báo Lỗi`** (`Bug Report`) tích hợp copy log và mở GitHub Issues.
  - Dịch toàn bộ Nhật ký (Logs), Cây thư mục (Folder tree), Trạng thái (Badges) và Thông báo sang tiếng Anh chuẩn xác 100%.
- **v1.7.0**:
  - Sửa lỗi nút **`🛑 Dừng Tải`** không dừng được do vòng lặp retry mặc định của `gdown`.
  - Áp dụng `DownloadCancelledException` (BaseException) giúp dừng tức thì và giải phóng giao diện ngay lập tức khi người dùng hủy.
- **v1.6.0**:
  - Thêm thông tin tác giả **Phát triển bởi TÔN NGỘ ĐỘC**.
  - Tích hợp đa ngôn ngữ song ngữ Tiếng Việt & English kèm nút chuyển đổi tức thì trên giao diện.
- **v1.5.0**:
  - Thêm nút **`🔄 Tải Lại File Lỗi`** cho phép lọc và Retry tải lại các tệp bị lỗi.
- **v1.4.0**:
  - Chuyển sang cập nhật Badge status O(1), loại bỏ thanh progress bar dòng để triệt tiêu giật lag.
- **v1.3.0**:
  - Tự động đổi ký tự đặc biệt (`: ' $ ! ? * < > | " / \`) thành `_`.
- **v1.2.0**:
  - Đổi tên ứng dụng thành **DriveFlow Pro**.
- **v1.1.0**:
  - Chuyển sang Light Theme (giao diện màu sáng).
- **v1.0.0**:
  - Tải tự động folder/file qua thư viện `gdown`.

---

## 🚀 Hướng Dẫn Chạy & Đóng Gói

### 1. Chạy mã nguồn Python
```bash
python main.py
```

### 2. Đóng gói ứng dụng Windows .exe
```bash
python build_exe.py
```
Output: `D:\GDownloader\GDriveFlow.exe`.
