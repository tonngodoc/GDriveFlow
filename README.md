# 🌊 GDrive Flow (v2.2.1) - Windows & macOS Desktop Application

![GDrive Flow Logo](icon.png)

**Videcoding by TonNgoDoc**

Ứng dụng Desktop thuần (Hỗ trợ **Windows** & **macOS**) giúp tự động tải xuống danh sách tệp hoặc toàn bộ thư mục (folder) trên Google Drive về máy tính cá nhân.

---

## ✨ Tính Năng Nổi Bật (Phiên Bản v2.2.1)

1. **Hỗ Trợ Đa Nền Tảng (Windows & macOS)**:
   - Mã nguồn được tối ưu tương thích 100% trên cả Windows và **macOS** (Apple Silicon M1/M2/M3 & Intel Mac).
   - Tự động nhận diện hệ điều hành và xử lý icon cửa sổ chuẩn xác (`set_window_icon`).
   - Bổ sung kịch bản đóng gói ứng dụng macOS riêng biệt (`build_mac.py`).
2. **Giao Diện Phẳng Loại Bỏ Đường Viền Khung**:
   - Loại bỏ hoàn toàn đường viền khung (`border_width=0`) cho từng dòng tệp/thư mục trong danh sách, chỉ giữ lại màu nền phẳng mềm mại, hiện đại và vô cùng thoáng mắt.
3. **Mặc Định Thu Gọn Cây Thư Mục Tránh Lag**:
   - Mặc định thu gọn các nhánh cây thư mục (*Collapsed tree view by default*) giúp ứng dụng load siêu tốc và cực kỳ mượt mà, không bị đơ lag khi quét folder chứa hàng ngàn tệp.
4. **Thẻ Trạng Thái Danh Sách Tinh Gọn**:
   - Thẻ trạng thái trong cây danh sách hiển thị gọn gàng (`🔵 Đang tải...`, `✅ Hoàn thành`, `❌ Lỗi tải`, `⚠️ Tạm dừng`), không chứa số % gây rối mắt.
5. **Thanh Năng Lượng Tiến Trình % Trực Quan**:
   - Tích hợp 2 thanh năng lượng progress bar tại ô Trạng Thái chính:
     - **📄 Tiến trình File hiện tại**: Hiển thị % download thời gian thực của file đang tải.
     - **📊 Tiến trình Toàn bộ Queue**: Hiển thị % download tổng thể của toàn bộ các file được chọn.
6. **Khử URL Thư Viện Bên Thứ 3 & Chuẩn Hóa Lỗi**:
   - Tự động lọc và khử toàn bộ đường dẫn link thư viện bên thứ 3 (như `wkentaro/gdown`) ra khỏi thông báo lỗi.
   - Bổ sung gợi ý khắc phục chi tiết hướng dẫn mở quyền chia sẻ Google Drive (*"Bất kỳ ai có liên kết đều có thể xem"*).
7. **Cập Nhật Thông Tin Donate Chính Thức**:
   - Nút **`💖 Donate`** hiển thị cửa sổ ủng hộ tác giả qua ngân hàng **TPBank**.
   - **Chủ tài khoản**: `Nguyen Ngoc Thai Ha` | **STK**: `64608121989` kèm nút sao chép tự động.
8. **Biểu Tượng Icon Cờ Song Ngữ (Flag Icons)**:
   - Tích hợp icon **Cờ Việt Nam** (`🇻🇳`) & **Cờ Anh Quốc** (`🇬🇧`) sắc nét trên thanh công cụ chuyển đổi ngôn ngữ.

---

## 💖 Ủng Hộ Tác Giả (Donate)

Nếu ứng dụng **GDrive Flow** giúp ích cho bạn, bạn có thể ủng hộ tác giả một ly cà phê qua tài khoản ngân hàng bên dưới:

- 🏦 **Ngân hàng**: TPBank (Ngân hàng Tiên Phong)
- 👤 **Chủ tài khoản**: Nguyen Ngoc Thai Ha
- 💳 **Số tài khoản (STK)**: `64608121989`

*Cảm ơn sự ủng hộ chân thành từ bạn để tác giả duy trì và nâng cấp các phiên bản tiếp theo!*

---

## 🚀 Hướng Dẫn Chạy & Đóng Gói

### 1. Chạy mã nguồn Python (Windows / macOS)
```bash
python main.py
```

### 2. Đóng gói ứng dụng trên Windows (.exe)
```bash
python build_exe.py
```
Output: `GDriveFlow.exe`.

### 3. Đóng gói ứng dụng trên macOS (.app / binary)
```bash
python build_mac.py
```
Output: `dist/GDriveFlow` hoặc `GDriveFlow_mac`.
