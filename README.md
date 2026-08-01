# 🌊 GDrive Flow (v2.1.2) - Windows Desktop Application

![GDrive Flow Logo](icon.png)

**Phát triển bởi TÔN NGỘ ĐỘC (Developed by TON NGO DOC)**

Ứng dụng Windows Desktop thuần giúp tự động tải xuống danh sách tệp hoặc toàn bộ thư mục (folder) trên Google Drive về máy tính cá nhân.

---

## ✨ Tính Năng Nổi Bật (Phiên Bản v2.1.2)

1. **Hiển Thị Trạng Thái Real-Time 100% Cây Thư Mục**:
   - Khắc phục triệt để lỗi không hiện trạng thái file khi chưa bấm xổ thư mục.
   - Mặc định mở rộng cây thư mục (*Expanded tree view*) ngay sau khi quét, giúp mọi thẻ trạng thái (Pending, 🔵 Downloading, ✅ Completed, ❌ Error) hiển thị trực tiếp.
   - Tự động tính toán và hiển thị thẻ tiến trình thời gian thực cho thư mục cha (ví dụ `🔵 3/10` -> `✅ 10/10`).
2. **Khử URL Thư Viện Bên Thứ 3 & Chuẩn Hóa Lỗi**:
   - Tự động lọc và khử toàn bộ đường dẫn link thư viện bên thứ 3 (như `wkentaro/gdown`) ra khỏi thông báo lỗi.
   - Bổ sung gợi ý khắc phục chi tiết hướng dẫn mở quyền chia sẻ Google Drive (*"Bất kỳ ai có liên kết đều có thể xem"*).
3. **Cập Nhật Thông Tin Donate Chính Thức**:
   - Nút **`💖 Donate`** hiển thị cửa sổ ủng hộ tác giả qua ngân hàng **TPBank**.
   - **Chủ tài khoản**: `Nguyen Ngoc Thai Ha` | **STK**: `64608121989` kèm nút sao chép tự động.
4. **Biểu Tượng Icon Cờ Song Ngữ (Flag Icons)**:
   - Tích hợp icon **Cờ Việt Nam** (`🇻🇳`) & **Cờ Anh Quốc** (`🇬🇧`) sắc nét trên thanh công cụ chuyển đổi ngôn ngữ.
5. **Lịch Sử Cập Nhật Tương Tác (Interactive Version Changelog)**:
   - Bấm trực tiếp vào nhãn **Phiên Bản (Version Badge)** trên ứng dụng để mở cửa sổ xem toàn bộ lịch sử nâng cấp ứng dụng.
6. **Tính Năng Báo Lỗi Ứng Dụng (Interactive Bug Report)**:
   - Nút **`🐛 Báo Lỗi`** (**`🐛 Report Bug`**) mở popup báo cáo sự cố trực tiếp.
   - Hỗ trợ sao chép toàn bộ nhật ký lỗi (Error Logs) và liên kết nhanh đến **GitHub Issues**.

---

## 💖 Ủng Hộ Tác Giả (Donate)

Nếu ứng dụng **GDrive Flow** giúp ích cho bạn, bạn có thể ủng hộ tác giả một ly cà phê qua tài khoản ngân hàng bên dưới:

- 🏦 **Ngân hàng**: TPBank (Ngân hàng Tiên Phong)
- 👤 **Chủ tài khoản**: Nguyen Ngoc Thai Ha
- 💳 **Số tài khoản (STK)**: `64608121989`

*Cảm ơn sự ủng hộ chân thành từ bạn để tác giả duy trì và nâng cấp các phiên bản tiếp theo!*

---

## 📋 Lịch Sử Phiên Bản (Changelog)

- **v2.1.2 (Hiện tại)**:
  - Sửa triệt để lỗi không hiển thị trạng thái file real-time trong cây thư mục.
  - Mặc định mở rộng cây thư mục (Expanded tree view) giúp mọi trạng thái file hiển thị trực tiếp 100%.
  - Tự động đồng bộ và hiển thị thẻ tiến trình thời gian thực cho thư mục cha (ví dụ `🔵 3/10` -> `✅ 10/10`).
- **v2.1.1**:
  - Khử toàn bộ link bên thứ 3 (`wkentaro/gdown`) trong thông báo lỗi.
  - Bổ sung hướng dẫn mở quyền chia sẻ Google Drive ('Bất kỳ ai có liên kết đều có thể xem').
- **v2.1.0**:
  - Cập nhật thông tin Donate: Chủ tài khoản `Nguyen Ngoc Thai Ha`, STK `64608121989`.
  - Tích hợp biểu tượng icon **Cờ Việt Nam** & **Cờ Anh Quốc** sắc nét trên thanh chuyển ngôn ngữ.
  - Thêm tính năng bấm vào nhãn Phiên bản (Version Badge) để xem Lịch sử cập nhật (Changelog) tương tác.

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
