# 🌊 GDrive Flow (v2.1.0) - Windows Desktop Application

![GDrive Flow Logo](icon.png)

**Phát triển bởi TÔN NGỘ ĐỘC (Developed by TON NGO DOC)**

Ứng dụng Windows Desktop thuần giúp tự động tải xuống danh sách tệp hoặc toàn bộ thư mục (folder) trên Google Drive về máy tính cá nhân.

---

## ✨ Tính Năng Nổi Bật (Phiên Bản v2.1.0)

1. **Cập Nhật Thông Tin Donate Chính Thức**:
   - Nút **`💖 Donate`** hiển thị cửa sổ ủng hộ tác giả qua ngân hàng **TPBank**.
   - **Chủ tài khoản**: `Nguyen Ngoc Thai Ha` | **STK**: `64608121989` kèm nút sao chép tự động.
2. **Biểu Tượng Icon Cờ Song Ngữ (Flag Icons)**:
   - Tích hợp icon **Cờ Việt Nam** (`🇻🇳`) & **Cờ Anh Quốc** (`🇬🇧`) sắc nét trên thanh công cụ chuyển đổi ngôn ngữ.
3. **Lịch Sử Cập Nhật Tương Tác (Interactive Version Changelog)**:
   - Bấm trực tiếp vào nhãn **Phiên Bản (Version Badge)** trên ứng dụng để mở cửa sổ xem toàn bộ lịch sử nâng cấp ứng dụng.
4. **Tính Năng Báo Lỗi Ứng Dụng (Interactive Bug Report)**:
   - Nút **`🐛 Báo Lỗi`** (**`🐛 Report Bug`**) mở popup báo cáo sự cố trực tiếp.
   - Hỗ trợ sao chép toàn bộ nhật ký lỗi (Error Logs) và liên kết nhanh đến **GitHub Issues**.
5. **Chuẩn Hóa Song Ngữ 100% (100% Full Bilingual VI/EN)**:
   - Dịch toàn bộ nhật ký hệ thống (Logs Console), nhãn trạng thái cây thư mục, thẻ tiến trình (Badge), và các hộp thoại thông báo sang Tiếng Anh hoàn chỉnh khi chuyển đổi ngôn ngữ.
6. **Khắc Phục Lỗi Dừng Tải & Treo Đơ Giao Diện (Instant Cancellation & Unblocking)**:
   - Sử dụng lớp ngoại lệ đặc biệt `DownloadCancelledException` thoát lập tức khỏi vòng lặp tải `gdown` mà không bị gdown thử lại trong vô hạn.
   - Khi bấm **`🛑 Dừng Tải`**, giao diện lập tức phản hồi và mở lại các nút chức năng trong 0.001s, không gây đơ treo ứng dụng.
7. **Tự Động Chuẩn Hóa Tên File (Filename Sanitization)**:
   - Tự động thay thế các ký tự đặc biệt không hợp lệ trên Windows (như `:`, `'`, `$`, `!`, `?`, `*`, `<`, `>`, `|`, `"`, `/`, `\`) thành dấu gạch dưới `_`.

---

## 💖 Ủng Hộ Tác Giả (Donate)

Nếu ứng dụng **GDrive Flow** giúp ích cho bạn, bạn có thể ủng hộ tác giả một ly cà phê qua tài khoản ngân hàng bên dưới:

- 🏦 **Ngân hàng**: TPBank (Ngân hàng Tiên Phong)
- 👤 **Chủ tài khoản**: Nguyen Ngoc Thai Ha
- 💳 **Số tài khoản (STK)**: `64608121989`

*Cảm ơn sự ủng hộ chân thành từ bạn để tác giả duy trì và nâng cấp các phiên bản tiếp theo!*

---

## 📋 Lịch Sử Phiên Bản (Changelog)

- **v2.1.0 (Hiện tại)**:
  - Cập nhật thông tin Donate: Chủ tài khoản `Nguyen Ngoc Thai Ha`, STK `64608121989`.
  - Tích hợp biểu tượng icon **Cờ Việt Nam** & **Cờ Anh Quốc** sắc nét trên thanh chuyển ngôn ngữ.
  - Thêm tính năng bấm vào nhãn Phiên bản (Version Badge) để xem Lịch sử cập nhật (Changelog) tương tác.
- **v2.0.0**:
  - Cập nhật chính thức URL Repository: `https://github.com/tonngodoc/GDriveFlow`.
  - Tích hợp nút **`💖 Donate`** hiển thị thông tin ngân hàng TPBank.
- **v1.9.0**:
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
