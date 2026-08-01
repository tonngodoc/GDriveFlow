# 🌊 GDrive Flow (v2.2.0) - Windows Desktop Application

![GDrive Flow Logo](icon.png)

**Videcoding by TonNgoDoc**

Ứng dụng Windows Desktop thuần giúp tự động tải xuống danh sách tệp hoặc toàn bộ thư mục (folder) trên Google Drive về máy tính cá nhân.

---

## ✨ Tính Năng Nổi Bật (Phiên Bản v2.2.0)

1. **Mặc Định Thu Gọn Cây Thư Mục Tránh Lag**:
   - Mặc định thu gọn các nhánh cây thư mục (*Collapsed tree view by default*) giúp ứng dụng load siêu tốc và cực kỳ mượt mà, không bị đơ lag khi quét folder chứa hàng ngàn tệp.
2. **Thẻ Trạng Thái Danh Sách Tinh Gọn**:
   - Thẻ trạng thái trong cây danh sách hiển thị gọn gàng (`🔵 Đang tải...`, `✅ Hoàn thành`, `❌ Lỗi tải`, `⚠️ Tạm dừng`), không chứa số % gây rối mắt.
3. **Thanh Năng Lượng Tiến Trình % Trực Quan**:
   - Tích hợp 2 thanh năng lượng progress bar tại ô Trạng Thái chính:
     - **📄 Tiến trình File hiện tại**: Hiển thị % download thời gian thực của file đang tải.
     - **📊 Tiến trình Toàn bộ Queue**: Hiển thị % download tổng thể của toàn bộ các file được chọn.
4. **Khử URL Thư Viện Bên Thứ 3 & Chuẩn Hóa Lỗi**:
   - Tự động lọc và khử toàn bộ đường dẫn link thư viện bên thứ 3 (như `wkentaro/gdown`) ra khỏi thông báo lỗi.
   - Bổ sung gợi ý khắc phục chi tiết hướng dẫn mở quyền chia sẻ Google Drive (*"Bất kỳ ai có liên kết đều có thể xem"*).
5. **Cập Nhật Thông Tin Donate Chính Thức**:
   - Nút **`💖 Donate`** hiển thị cửa sổ ủng hộ tác giả qua ngân hàng **TPBank**.
   - **Chủ tài khoản**: `Nguyen Ngoc Thai Ha` | **STK**: `64608121989` kèm nút sao chép tự động.
6. **Biểu Tượng Icon Cờ Song Ngữ (Flag Icons)**:
   - Tích hợp icon **Cờ Việt Nam** (`🇻🇳`) & **Cờ Anh Quốc** (`🇬🇧`) sắc nét trên thanh công cụ chuyển đổi ngôn ngữ.
7. **Lịch Sử Cập Nhật Tương Tác (Interactive Version Changelog)**:
   - Bấm trực tiếp vào nhãn **Phiên Bản (Version Badge)** trên ứng dụng để mở cửa sổ xem toàn bộ lịch sử nâng cấp ứng dụng.
8. **Tính Năng Báo Lỗi Ứng Dụng (Interactive Bug Report)**:
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

- **v2.2.0 (Hiện tại)**:
  - Cập nhật thông tin tác giả chính thức: **Videcoding by TonNgoDoc**.
  - Mặc định giữ thu gọn cây thư mục (Collapsed tree view by default) tránh đơ lag với folder nhiều file.
  - Thẻ trạng thái danh sách chỉ hiển thị gọn ('🔵 Đang tải...', '✅ Hoàn thành', '❌ Lỗi tải'), không chứa số %.
  - Bổ sung 2 thanh năng lượng % tiến trình (File hiện tại & Toàn bộ Queue) ở khu vực Trạng thái chính.
- **v2.1.2**:
  - Sửa triệt để lỗi không hiển thị trạng thái file real-time trong cây thư mục.
  - Đồng bộ thẻ tiến trình hiển thị thời gian thực cho thư mục cha (ví dụ `🔵 3/10` -> `✅ 10/10`).
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
