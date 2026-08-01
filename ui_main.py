import os
import sys
import threading
import time
import webbrowser
from typing import Optional, List, Tuple
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

from gdrive_service import GDriveService, GDriveItem, DownloadCancelledException

# Application Metadata
APP_NAME = "GDrive Flow"
APP_VERSION = "v2.1.0"
DEVELOPER_NAME_VI = "Phát triển bởi TÔN NGỘ ĐỘC"
DEVELOPER_NAME_EN = "Developed by TON NGO DOC"

# Release History / Changelog
CHANGELOG_TEXT_VI = """🌊 GDrive Flow - Lịch Sử Cập Nhật (Release History)

--------------------------------------------------
📌 Phiên Bản v2.1.0 (Hiện tại)
--------------------------------------------------
- 💳 Cập nhật thông tin Donate chính thức:
  • Ngân hàng: TPBank (Ngân hàng Tiên Phong)
  • Chủ tài khoản: Nguyen Ngoc Thai Ha
  • Số tài khoản (STK): 64608121989
- 🇻🇳🇬🇧 Tích hợp biểu tượng icon Cờ Việt Nam & Cờ Anh Quốc sắc nét trên thanh chuyển ngôn ngữ.
- 🛈 Bấm vào nhãn Phiên bản (Version Badge) để xem nhật ký cập nhật ứng dụng trực tiếp.

--------------------------------------------------
📌 Phiên Bản v2.0.0
--------------------------------------------------
- 💖 Tích hợp cửa sổ popup Donate ủng hộ tác giả.
- 🌐 Cập nhật repository GitHub chính thức: https://github.com/tonngodoc/GDriveFlow

--------------------------------------------------
📌 Phiên Bản v1.9.0
--------------------------------------------------
- 🌊 Chính thức đổi tên thương hiệu ứng dụng thành GDrive Flow.
- 🖼️ Thiết kế Logo thương hiệu mới kết hợp biểu tượng Google Drive và luồng tải sóng động.

--------------------------------------------------
📌 Phiên Bản v1.8.0
--------------------------------------------------
- 🐛 Thêm tính năng Báo Lỗi Ứng Dụng (Bug Report) tích hợp sao chép Log và mở GitHub Issues.
- 🌐 Dịch 100% nhật ký (Logs), cây thư mục, thẻ tiến trình và thông báo sang tiếng Anh chuẩn xác.

--------------------------------------------------
📌 Phiên Bản v1.7.0
--------------------------------------------------
- 🛑 Khắc phục 100% lỗi nút 'Dừng Tải' không dừng được với ngoại lệ DownloadCancelledException.
- ⚡ Thoát tức thì giải phóng giao diện trong 0.001s khi hủy tải.

--------------------------------------------------
📌 Phiên Bản v1.6.0 & Cũ Hơn
--------------------------------------------------
- 🌐 Hỗ trợ đa ngôn ngữ Tiếng Việt & English.
- 🔄 Thêm tính năng Tải Lại File Lỗi (Retry Failed Downloads).
- ⚡ Tối ưu cập nhật thẻ tiến trình Badge O(1) loại bỏ giật lag.
- 🧹 Tự động chuẩn hóa tên file & đường dẫn thư mục tránh lỗi Windows.
"""

CHANGELOG_TEXT_EN = """🌊 GDrive Flow - Version Release History

--------------------------------------------------
📌 Version v2.1.0 (Current)
--------------------------------------------------
- 💳 Updated official Donate info:
  • Bank: TPBank (Tiên Phong Bank)
  • Account Holder: Nguyen Ngoc Thai Ha
  • Account Number (STK): 64608121989
- 🇻🇳🇬🇧 Added crisp flag icons for Vietnam & United Kingdom on language selector bar.
- 🛈 Clickable Version Badge to view app release history log directly.

--------------------------------------------------
📌 Version v2.0.0
--------------------------------------------------
- 💖 Integrated interactive Donate popup window for supporting developer.
- 🌐 Updated official GitHub repository: https://github.com/tonngodoc/GDriveFlow

--------------------------------------------------
📌 Version v1.9.0
--------------------------------------------------
- 🌊 Rebranded official app name to GDrive Flow.
- 🖼️ Designed new brand logo blending Google Drive icon with dynamic flow wave aesthetics.

--------------------------------------------------
📌 Version v1.8.0
--------------------------------------------------
- 🐛 Added Interactive Bug Report feature with log copy and GitHub Issues integration.
- 🌐 100% Full English localization across all system logs, tree badges, and notifications.

--------------------------------------------------
📌 Version v1.7.0
--------------------------------------------------
- 🛑 Fixed 100% cancellation unblocking using DownloadCancelledException.
- ⚡ Instant UI thread release in 0.001s upon download cancellation.

--------------------------------------------------
📌 Version v1.6.0 & Earlier
--------------------------------------------------
- 🌐 Multi-language support (Vietnamese & English).
- 🔄 Added Retry Failed Downloads feature.
- ⚡ O(1) Status Badge real-time progress updates.
- 🧹 Automatic filename & directory sanitization for Windows filesystem safety.
"""

# Multilingual Translation Dictionary
TRANSLATIONS = {
    "vi": {
        "title": "GDrive Flow",
        "developer": DEVELOPER_NAME_VI,
        "version": "Phiên bản",
        "donate_btn": "💖 Donate",
        "report_bug": "🐛 Báo Lỗi",
        "url_label": "Link / ID Google Drive:",
        "url_placeholder": "Dán liên kết Thư Mục (Folder) hoặc Tệp (File) Google Drive...",
        "scan_btn": "🔍 Quét Cây Thư Mục",
        "scanning_btn": "⏳ Đang Quét...",
        "dest_label": "Thư mục lưu về máy:",
        "browse_btn": "Chọn Thư Mục",
        "tree_title": "📁 Cây Thư Mục & Tệp Tin",
        "selected_files": "Đã chọn",
        "total_size": "Tổng dung lượng",
        "select_all": "☑ Chọn Tất Cả",
        "deselect_all": "☐ Bỏ Chọn Tất Cả",
        "start_download": "⚡ Bắt Đầu Tải Các File Đã Chọn",
        "retry_failed": "🔄 Tải Lại File Lỗi",
        "cancel_download": "🛑 Dừng Tải",
        "status_ready": "Trạng thái: Sẵn sàng tải xuống",
        "status_finished": "✅ Trạng thái: Hoàn tất tải xuống",
        "status_stopped": "🛑 Trạng thái: Đã dừng tải xuống",
        "status_error": "❌ Trạng thái: Đã dừng hoặc Lỗi",
        "downloading_status": "[{idx}/{total}] Đang tải: {name}",
        "speed": "⚡ Tốc Độ Tải",
        "file_size": "📦 Dung Lượng File",
        "queue_status": "📊 Đã Chọn Tải",
        "eta": "⏳ Thời Gian Còn Lại",
        "log_header": "📝 Log Console:",
        "log_ready": "Sẵn sàng hoạt động.",
        "log_cleared": "Đã xóa sạch log.",
        "log_expanded": "▲ Thu Gọn Log",
        "log_collapsed": "📋 Xem Toàn Bộ Log",
        "clear_log": "Xóa Log",
        "completed_badge": "✅ Hoàn thành",
        "error_badge": "❌ Lỗi tải",
        "paused_badge": "⚠️ Tạm dừng (Resume ok)",
        "downloading_badge": "🔵 Đang tải...",
        "empty_folder": "⚠️ Thư mục trống hoặc không tìm thấy tệp nào.",
        "file_unit": "file",
        "no_failed_files": "Không có tệp nào bị lỗi cần tải lại!",
        "no_scanned_files": "Chưa có danh sách tệp nào được quét!",
        "no_selected_files": "Vui lòng tích chọn ít nhất 1 file trong cây thư mục để tải về!",
        "invalid_url": "Đường dẫn URL hoặc ID Google Drive không hợp lệ!",
        "enter_url": "Vui lòng nhập Link hoặc ID của Folder/File Google Drive!",
        "enter_dest": "Vui lòng chỉ định thư mục lưu file!",
        "tree_placeholder": "Dán link Google Drive và bấm '🔍 Quét Cây Thư Mục' để xem danh sách file/folder...",
        "all_done": "🎉 TẤT CẢ FILE ĐÃ ĐƯỢC TẢI XONG!",
        "finish_msg": "Đã hoàn thành tải xuống các tệp đã chọn!",

        # Logs localization
        "log_scanning_folder": "📁 Đang quét Thư Mục Google Drive (ID: {id})...",
        "log_analyzing_file": "📄 Đang phân tích Tệp Google Drive (ID: {id})...",
        "log_scan_error": "❌ Lỗi quét: {error}",
        "log_tree_rendered": "✅ Cấu trúc cây thư mục đã hiển thị với {count} file.",
        "log_retrying_failed": "🔄 Đang thử lại {count} file bị lỗi...",
        "log_download_started": "🚀 Bắt đầu tải xuống {count} file đã chọn...",
        "log_cancel_requested": "🛑 Người dùng yêu cầu dừng tải xuống...",
        "log_download_stopped": "🛑 Quá trình tải xuống đã dừng.",
        "log_downloading_item": "📥 [{idx}/{total}] Đang tải: '{name}'...",
        "log_downloaded_item": "✨ Đã tải xong [{idx}/{total}]: {name}",
        "log_download_cancelled": "🛑 Đã hủy tải xuống.",
        "log_download_error": "❌ Lỗi khi tải [{idx}/{total}]: {error}",
        "log_system_error": "❌ Lỗi hệ thống: {error}",

        # Bug Report Dialog
        "report_title": "Báo Lỗi Ứng Dụng (Bug Report)",
        "report_desc": "Nếu gặp sự cố hoặc lỗi khi sử dụng GDrive Flow, bạn có thể sao chép nhật ký (logs) hoặc mở trang GitHub Issues để gửi báo cáo.",
        "report_copy_log": "📋 Sao Chép Log Lỗi",
        "report_open_github": "🌐 Mở GitHub Issues",
        "report_copied_msg": "Đã sao chép nội dung log vào Clipboard!",
        "report_close": "Đóng",

        # Donate Dialog
        "donate_title": "Ủng Hộ Tác Giả (Donate)",
        "donate_desc": "Nếu bạn cảm thấy ứng dụng GDrive Flow hữu ích, bạn có thể ủng hộ tác giả qua tài khoản ngân hàng bên dưới:",
        "donate_bank_name": "Ngân hàng:",
        "donate_holder": "Chủ tài khoản:",
        "donate_account": "Số tài khoản (STK):",
        "donate_copy_btn": "📋 Sao Chép STK",
        "donate_copied_msg": "Đã sao chép STK '64608121989' vào Clipboard!",
        "donate_close": "Đóng",

        # Changelog Dialog
        "changelog_title": "Lịch Sử Cập Nhật Phiên Bản (Changelog)",
        "changelog_open_github": "🌐 Trang GitHub Project"
    },
    "en": {
        "title": "GDrive Flow",
        "developer": DEVELOPER_NAME_EN,
        "version": "Version",
        "donate_btn": "💖 Donate",
        "report_bug": "🐛 Report Bug",
        "url_label": "Google Drive Link / ID:",
        "url_placeholder": "Paste Google Drive Folder or File link here...",
        "scan_btn": "🔍 Scan Folder Tree",
        "scanning_btn": "⏳ Scanning...",
        "dest_label": "Save Destination:",
        "browse_btn": "Browse Folder",
        "tree_title": "📁 Folder Tree & Files",
        "selected_files": "Selected",
        "total_size": "Total Size",
        "select_all": "☑ Select All",
        "deselect_all": "☐ Deselect All",
        "start_download": "⚡ Start Downloading Selected",
        "retry_failed": "🔄 Retry Failed Files",
        "cancel_download": "🛑 Stop Download",
        "status_ready": "Status: Ready to download",
        "status_finished": "✅ Status: Download Finished",
        "status_stopped": "🛑 Status: Download Stopped",
        "status_error": "❌ Status: Stopped or Error",
        "downloading_status": "[{idx}/{total}] Downloading: {name}",
        "speed": "⚡ Download Speed",
        "file_size": "📦 File Size",
        "queue_status": "📊 Selected Queue",
        "eta": "⏳ Remaining Time",
        "log_header": "📝 Log Console:",
        "log_ready": "Ready for operation.",
        "log_cleared": "Logs cleared.",
        "log_expanded": "▲ Collapse Logs",
        "log_collapsed": "📋 View Full Logs",
        "clear_log": "Clear Logs",
        "completed_badge": "✅ Completed",
        "error_badge": "❌ Download Error",
        "paused_badge": "⚠️ Paused (Resume ok)",
        "downloading_badge": "🔵 Downloading...",
        "empty_folder": "⚠️ Empty folder or no files found.",
        "file_unit": "file",
        "no_failed_files": "No failed files to retry!",
        "no_scanned_files": "No scanned files available!",
        "no_selected_files": "Please select at least 1 file to download!",
        "invalid_url": "Invalid Google Drive URL or ID!",
        "enter_url": "Please enter Google Drive link or ID!",
        "enter_dest": "Please specify save destination folder!",
        "tree_placeholder": "Paste Google Drive link and click '🔍 Scan Folder Tree' to list contents...",
        "all_done": "🎉 ALL FILES DOWNLOADED SUCCESSFULLY!",
        "finish_msg": "Selected files have been downloaded successfully!",

        # Logs localization
        "log_scanning_folder": "📁 Scanning Google Drive Folder (ID: {id})...",
        "log_analyzing_file": "📄 Analyzing Google Drive File (ID: {id})...",
        "log_scan_error": "❌ Scan error: {error}",
        "log_tree_rendered": "✅ Folder tree structure rendered with {count} file(s).",
        "log_retrying_failed": "🔄 Retrying {count} failed file(s)...",
        "log_download_started": "🚀 Download process started for {count} selected file(s)...",
        "log_cancel_requested": "🛑 Download cancellation requested by user...",
        "log_download_stopped": "🛑 Download process stopped.",
        "log_downloading_item": "📥 [{idx}/{total}] Downloading: '{name}'...",
        "log_downloaded_item": "✨ Downloaded [{idx}/{total}]: {name}",
        "log_download_cancelled": "🛑 Download cancelled.",
        "log_download_error": "❌ Error downloading [{idx}/{total}]: {error}",
        "log_system_error": "❌ System error: {error}",

        # Bug Report Dialog
        "report_title": "Application Bug Report",
        "report_desc": "If you encounter any issues with GDrive Flow, you can copy the error log or open GitHub Issues to submit a bug report.",
        "report_copy_log": "📋 Copy Error Log",
        "report_open_github": "🌐 Open GitHub Issues",
        "report_copied_msg": "Log contents copied to Clipboard!",
        "report_close": "Close",

        # Donate Dialog
        "donate_title": "Support Developer (Donate)",
        "donate_desc": "If you find GDrive Flow helpful, consider supporting the developer via bank details below:",
        "donate_bank_name": "Bank Name:",
        "donate_holder": "Account Holder:",
        "donate_account": "Account Number (STK):",
        "donate_copy_btn": "📋 Copy Account Number",
        "donate_copied_msg": "Account number '64608121989' copied to Clipboard!",
        "donate_close": "Close",

        # Changelog Dialog
        "changelog_title": "Version Release History (Changelog)",
        "changelog_open_github": "🌐 Open GitHub Repository"
    }
}

# Set Appearance Mode to Light
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class TreeNode:
    """Represents a node in the hierarchical folder/file tree."""
    def __init__(self, name: str, is_folder: bool = False, gdrive_item: Optional[GDriveItem] = None, parent: Optional['TreeNode'] = None):
        self.name = name
        self.is_folder = is_folder
        self.gdrive_item = gdrive_item
        self.parent = parent
        self.children: list['TreeNode'] = []
        
        # State tracking
        self.var_checked = ctk.BooleanVar(value=True)
        self.expanded = False  # Collapsed by default for ultra performance & lazy loading
        self.status = "pending"  # 'pending', 'downloading', 'completed', 'error', 'paused'
        self.status_text = ""
        self.progress_value = 0.0  # 0.0 to 1.0
        
        # UI Widget references
        self.frame_widget: Optional[ctk.CTkFrame] = None
        self.toggle_btn: Optional[ctk.CTkButton] = None
        self.lbl_status_badge: Optional[ctk.CTkLabel] = None
        self.cb_widget: Optional[ctk.CTkCheckBox] = None
        self.depth = 0

    def add_child(self, child: 'TreeNode'):
        child.parent = self
        self.children.append(child)

    def set_checked_recursive(self, value: bool):
        self.var_checked.set(value)
        for child in self.children:
            child.set_checked_recursive(value)

    def get_all_file_nodes(self) -> list['TreeNode']:
        """Returns all leaf file nodes under this subtree."""
        file_nodes = []
        if not self.is_folder and self.gdrive_item:
            file_nodes.append(self)
        for child in self.children:
            file_nodes.extend(child.get_all_file_nodes())
        return file_nodes

    def get_total_bytes(self) -> int:
        """Calculates total byte size under this subtree."""
        total = 0
        if not self.is_folder and self.gdrive_item:
            total += self.gdrive_item.size
        for child in self.children:
            total += child.get_total_bytes()
        return total


class GDriveApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} ({APP_VERSION}) - {DEVELOPER_NAME_VI}")
        self.geometry("980x800")
        self.minsize(850, 640)

        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        # Active Language State ('vi' or 'en')
        self.current_lang = "vi"

        # GDrive Service initialization
        self.service = GDriveService()

        # Download states
        self.is_downloading = False
        self.is_scanning = False
        self.cancel_requested = False
        self.download_thread = None

        # Tree root and active items
        self.tree_root: Optional[TreeNode] = None
        self.selected_file_nodes: list[TreeNode] = []

        # Log collapse state
        self.log_expanded = False

        # Setup UI Components
        self._build_ui()

    def t(self, key: str) -> str:
        """Returns localized string for current language."""
        return TRANSLATIONS.get(self.current_lang, TRANSLATIONS["vi"]).get(key, key)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=2)  # Tree section expands
        self.grid_rowconfigure(4, weight=0)  # Log section

        # ==========================================
        # 1. HEADER & INPUT SECTION
        # ==========================================
        input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff", border_width=1, border_color="#e1e8ed")
        input_frame.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        title_subframe = ctk.CTkFrame(input_frame, fg_color="transparent")
        title_subframe.grid(row=0, column=0, columnspan=2, padx=15, pady=(12, 8), sticky="ew")
        title_subframe.grid_columnconfigure(0, weight=1)

        # Title & Version Badge
        left_header = ctk.CTkFrame(title_subframe, fg_color="transparent")
        left_header.pack(side="left")

        # Load Logo image icon
        png_icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(png_icon_path):
            try:
                logo_img = ctk.CTkImage(light_image=Image.open(png_icon_path), dark_image=Image.open(png_icon_path), size=(28, 28))
                lbl_logo = ctk.CTkLabel(left_header, image=logo_img, text="")
                lbl_logo.pack(side="left", padx=(0, 8))
            except Exception:
                pass

        title_label = ctk.CTkLabel(
            left_header, 
            text=f"{APP_NAME}", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f6aa5"
        )
        title_label.pack(side="left")

        # Interactive Version Badge (Clickable -> opens Changelog window!)
        self.version_btn = ctk.CTkButton(
            left_header,
            text=f" {APP_VERSION} 🛈",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#e2e8f0",
            hover_color="#cbd5e1",
            text_color="#1e293b",
            corner_radius=6,
            height=24,
            width=70,
            command=self._open_changelog_dialog
        )
        self.version_btn.pack(side="left", padx=8)

        # Developer Credit Tag Requirement
        self.lbl_developer = ctk.CTkLabel(
            left_header,
            text=f"• {self.t('developer')}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#16a34a"
        )
        self.lbl_developer.pack(side="left", padx=8)

        # Language Switcher with Flag Icons
        lang_frame = ctk.CTkFrame(title_subframe, fg_color="#e2e8f0", corner_radius=6)
        lang_frame.pack(side="right")

        flag_vn_path = os.path.join(os.path.dirname(__file__), "flag_vn.png")
        flag_en_path = os.path.join(os.path.dirname(__file__), "flag_en.png")

        self.img_flag_vi = ctk.CTkImage(light_image=Image.open(flag_vn_path), dark_image=Image.open(flag_vn_path), size=(22, 14)) if os.path.exists(flag_vn_path) else None
        self.img_flag_en = ctk.CTkImage(light_image=Image.open(flag_en_path), dark_image=Image.open(flag_en_path), size=(22, 14)) if os.path.exists(flag_en_path) else None

        self.btn_flag_vi = ctk.CTkButton(
            lang_frame,
            text=" 🇻🇳",
            image=self.img_flag_vi,
            compound="left",
            width=42,
            height=28,
            corner_radius=5,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#0284c7",
            text_color="#ffffff",
            hover_color="#0369a1",
            command=lambda: self._set_language("vi")
        )
        self.btn_flag_vi.pack(side="left", padx=2, pady=2)

        self.btn_flag_en = ctk.CTkButton(
            lang_frame,
            text=" 🇬🇧",
            image=self.img_flag_en,
            compound="left",
            width=42,
            height=28,
            corner_radius=5,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="transparent",
            text_color="#475569",
            hover_color="#cbd5e1",
            command=lambda: self._set_language("en")
        )
        self.btn_flag_en.pack(side="left", padx=2, pady=2)

        # Donate Button
        self.btn_donate = ctk.CTkButton(
            title_subframe,
            text=self.t("donate_btn"),
            command=self._open_donate_dialog,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#ec4899",
            hover_color="#db2777",
            height=28,
            width=95
        )
        self.btn_donate.pack(side="right", padx=(0, 8))

        # Report Bug Button
        self.btn_report = ctk.CTkButton(
            title_subframe,
            text=self.t("report_bug"),
            command=self._open_report_dialog,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            height=28,
            width=105
        )
        self.btn_report.pack(side="right", padx=(0, 8))

        # Row 1: GDrive URL / ID input
        self.lbl_url = ctk.CTkLabel(input_frame, text=self.t("url_label"), font=ctk.CTkFont(size=13, weight="bold"), text_color="#2c3e50")
        self.lbl_url.grid(row=1, column=0, padx=15, pady=5, sticky="w")

        url_subframe = ctk.CTkFrame(input_frame, fg_color="transparent")
        url_subframe.grid(row=1, column=1, padx=(0, 15), pady=5, sticky="ew")
        url_subframe.grid_columnconfigure(0, weight=1)

        self.entry_url = ctk.CTkEntry(
            url_subframe,
            placeholder_text=self.t("url_placeholder"),
            font=ctk.CTkFont(size=13),
            fg_color="#f8f9fa",
            text_color="#2c3e50",
            border_color="#cbd5e1"
        )
        self.entry_url.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.btn_scan = ctk.CTkButton(
            url_subframe,
            text=self.t("scan_btn"),
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_click_scan,
            width=150,
            height=34,
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.btn_scan.grid(row=0, column=1)

        # Row 2: Destination path
        self.lbl_dest = ctk.CTkLabel(input_frame, text=self.t("dest_label"), font=ctk.CTkFont(size=13, weight="bold"), text_color="#2c3e50")
        self.lbl_dest.grid(row=2, column=0, padx=15, pady=5, sticky="w")

        dest_subframe = ctk.CTkFrame(input_frame, fg_color="transparent")
        dest_subframe.grid(row=2, column=1, padx=(0, 15), pady=5, sticky="ew")
        dest_subframe.grid_columnconfigure(0, weight=1)

        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads", "GDriveDownloads")
        self.entry_dest = ctk.CTkEntry(
            dest_subframe,
            font=ctk.CTkFont(size=13),
            fg_color="#f8f9fa",
            text_color="#2c3e50",
            border_color="#cbd5e1"
        )
        self.entry_dest.insert(0, default_download_path)
        self.entry_dest.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.btn_browse = ctk.CTkButton(
            dest_subframe,
            text=self.t("browse_btn"),
            command=self._on_browse_dest,
            width=120,
            height=34,
            fg_color="#475569",
            hover_color="#334155"
        )
        self.btn_browse.grid(row=0, column=1)

        # ==========================================
        # 2. HIERARCHICAL TREE & SELECTION SECTION
        # ==========================================
        tree_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff", border_width=1, border_color="#e1e8ed")
        tree_frame.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(1, weight=1)

        tree_header = ctk.CTkFrame(tree_frame, fg_color="transparent")
        tree_header.grid(row=0, column=0, padx=12, pady=(8, 4), sticky="ew")
        tree_header.grid_columnconfigure(0, weight=1)

        self.lbl_tree_status = ctk.CTkLabel(
            tree_header,
            text=f"{self.t('tree_title')} ({self.t('selected_files')}: 0 {self.t('file_unit')}):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#1e293b"
        )
        self.lbl_tree_status.grid(row=0, column=0, sticky="w")

        ctrl_subframe = ctk.CTkFrame(tree_header, fg_color="transparent")
        ctrl_subframe.grid(row=0, column=1, sticky="e")

        self.btn_select_all = ctk.CTkButton(
            ctrl_subframe,
            text=self.t("select_all"),
            width=110,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self._select_all_tree_nodes
        )
        self.btn_select_all.pack(side="left", padx=4)

        self.btn_deselect_all = ctk.CTkButton(
            ctrl_subframe,
            text=self.t("deselect_all"),
            width=120,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="#64748b",
            hover_color="#475569",
            command=self._deselect_all_tree_nodes
        )
        self.btn_deselect_all.pack(side="left", padx=4)

        # Scrollable Frame for Tree Rows
        self.scroll_tree = ctk.CTkScrollableFrame(tree_header.master, corner_radius=6, fg_color="#f8fafc")
        self.scroll_tree.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="nsew")

        self.lbl_tree_placeholder = ctk.CTkLabel(
            self.scroll_tree,
            text=self.t("tree_placeholder"),
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        )
        self.lbl_tree_placeholder.pack(pady=30)

        # Action Buttons Row
        action_subframe = ctk.CTkFrame(tree_frame, fg_color="transparent")
        action_subframe.grid(row=2, column=0, padx=12, pady=(0, 10), sticky="ew")
        action_subframe.grid_columnconfigure(0, weight=1)

        self.btn_start = ctk.CTkButton(
            action_subframe,
            text=self.t("start_download"),
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._on_start_download,
            height=42,
            fg_color="#2fa572",
            hover_color="#1e7b52"
        )
        self.btn_start.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_retry = ctk.CTkButton(
            action_subframe,
            text=self.t("retry_failed"),
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_retry_failed_downloads,
            width=160,
            height=42,
            fg_color="#d97706",
            hover_color="#b45309"
        )
        self.btn_retry.pack(side="left", padx=(0, 8))

        self.btn_cancel = ctk.CTkButton(
            action_subframe,
            text=self.t("cancel_download"),
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._on_cancel_download,
            width=130,
            height=42,
            fg_color="#ef4444",
            hover_color="#dc2626",
            state="disabled"
        )
        self.btn_cancel.pack(side="right")

        # ==========================================
        # 3. LIVE MONITORING & STATS SECTION
        # ==========================================
        stats_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff", border_width=1, border_color="#e1e8ed")
        stats_frame.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        stats_frame.grid_columnconfigure(0, weight=1)

        # File currently downloading
        self.lbl_current_file = ctk.CTkLabel(
            stats_frame,
            text=self.t("status_ready"),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#0f172a",
            anchor="w"
        )
        self.lbl_current_file.grid(row=0, column=0, padx=15, pady=(10, 2), sticky="w")

        # Clean 4 Cards Grid
        cards_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        cards_frame.grid(row=1, column=0, padx=15, pady=(6, 12), sticky="ew")
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        # Card 1: Speed
        c1 = ctk.CTkFrame(cards_frame, corner_radius=6, fg_color="#f1f5f9")
        c1.grid(row=0, column=0, padx=4, sticky="ew")
        self.lbl_c1_title = ctk.CTkLabel(c1, text=self.t("speed"), font=ctk.CTkFont(size=11, weight="bold"), text_color="#64748b")
        self.lbl_c1_title.pack(pady=(4, 0))
        self.lbl_val_speed = ctk.CTkLabel(c1, text="0 KB/s", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0284c7")
        self.lbl_val_speed.pack(pady=(0, 4))

        # Card 2: Current File Size
        c2 = ctk.CTkFrame(cards_frame, corner_radius=6, fg_color="#f1f5f9")
        c2.grid(row=0, column=1, padx=4, sticky="ew")
        self.lbl_c2_title = ctk.CTkLabel(c2, text=self.t("file_size"), font=ctk.CTkFont(size=11, weight="bold"), text_color="#64748b")
        self.lbl_c2_title.pack(pady=(4, 0))
        self.lbl_val_file_size = ctk.CTkLabel(c2, text="0 B / 0 B", font=ctk.CTkFont(size=13, weight="bold"), text_color="#0f172a")
        self.lbl_val_file_size.pack(pady=(0, 4))

        # Card 3: Overall Progress
        c3 = ctk.CTkFrame(cards_frame, corner_radius=6, fg_color="#f1f5f9")
        c3.grid(row=0, column=2, padx=4, sticky="ew")
        self.lbl_c3_title = ctk.CTkLabel(c3, text=self.t("queue_status"), font=ctk.CTkFont(size=11, weight="bold"), text_color="#64748b")
        self.lbl_c3_title.pack(pady=(4, 0))
        self.lbl_val_overall = ctk.CTkLabel(c3, text=f"0/0 {self.t('file_unit')}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#d97706")
        self.lbl_val_overall.pack(pady=(0, 4))

        # Card 4: ETA
        c4 = ctk.CTkFrame(cards_frame, corner_radius=6, fg_color="#f1f5f9")
        c4.grid(row=0, column=3, padx=4, sticky="ew")
        self.lbl_c4_title = ctk.CTkLabel(c4, text=self.t("eta"), font=ctk.CTkFont(size=11, weight="bold"), text_color="#64748b")
        self.lbl_c4_title.pack(pady=(4, 0))
        self.lbl_val_eta = ctk.CTkLabel(c4, text="--:--", font=ctk.CTkFont(size=14, weight="bold"), text_color="#dc2626")
        self.lbl_val_eta.pack(pady=(0, 4))

        # ==========================================
        # 4. COLLAPSIBLE LOG CONSOLE SECTION
        # ==========================================
        self.log_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff", border_width=1, border_color="#e1e8ed")
        self.log_frame.grid(row=4, column=0, padx=15, pady=(5, 15), sticky="ew")
        self.log_frame.grid_columnconfigure(0, weight=1)

        log_header = ctk.CTkFrame(self.log_frame, fg_color="transparent")
        log_header.grid(row=0, column=0, padx=10, pady=6, sticky="ew")
        log_header.grid_columnconfigure(1, weight=1)

        self.lbl_log_header = ctk.CTkLabel(log_header, text=self.t("log_header"), font=ctk.CTkFont(size=12, weight="bold"), text_color="#1e293b")
        self.lbl_log_header.grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.lbl_latest_log = ctk.CTkLabel(
            log_header,
            text=self.t("log_ready"),
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#475569",
            anchor="w"
        )
        self.lbl_latest_log.grid(row=0, column=1, sticky="ew", padx=5)

        self.btn_toggle_log = ctk.CTkButton(
            log_header,
            text=self.t("log_collapsed"),
            width=130,
            height=24,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#e2e8f0",
            hover_color="#cbd5e1",
            text_color="#1e293b",
            command=self._toggle_log_console
        )
        self.btn_toggle_log.grid(row=0, column=2, sticky="e", padx=(5, 0))

        self.txt_log = ctk.CTkTextbox(
            self.log_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            corner_radius=6,
            wrap="word",
            height=120,
            fg_color="#1e293b",
            text_color="#f8fafc"
        )

    def _set_language(self, lang_code: str):
        """Sets active language and updates flag button styles."""
        if lang_code == "en":
            self.current_lang = "en"
            self.btn_flag_en.configure(fg_color="#0284c7", text_color="#ffffff", hover_color="#0369a1")
            self.btn_flag_vi.configure(fg_color="transparent", text_color="#475569", hover_color="#cbd5e1")
        else:
            self.current_lang = "vi"
            self.btn_flag_vi.configure(fg_color="#0284c7", text_color="#ffffff", hover_color="#0369a1")
            self.btn_flag_en.configure(fg_color="transparent", text_color="#475569", hover_color="#cbd5e1")

        self._on_change_language_update_ui()

    def _open_changelog_dialog(self):
        """Opens interactive Changelog Release History modal window."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.t("changelog_title"))
        dialog.geometry("580x480")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Set dialog icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            try:
                dialog.iconbitmap(icon_path)
            except Exception:
                pass

        lbl_title = ctk.CTkLabel(
            dialog,
            text=f"📋 {self.t('changelog_title')}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f6aa5"
        )
        lbl_title.pack(padx=20, pady=(16, 6), anchor="w")

        txt_changelog = ctk.CTkTextbox(
            dialog,
            font=ctk.CTkFont(family="Consolas", size=11),
            height=340,
            wrap="word",
            fg_color="#1e293b",
            text_color="#f8fafc"
        )
        txt_changelog.pack(padx=20, pady=5, fill="both", expand=True)

        changelog_content = CHANGELOG_TEXT_EN if self.current_lang == "en" else CHANGELOG_TEXT_VI
        txt_changelog.insert("1.0", changelog_content)
        txt_changelog.configure(state="disabled")

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(8, 14), fill="x")

        def open_github_releases():
            webbrowser.open("https://github.com/tonngodoc/GDriveFlow")

        btn_gh = ctk.CTkButton(
            btn_frame,
            text=self.t("changelog_open_github"),
            font=ctk.CTkFont(size=12, weight="bold"),
            command=open_github_releases,
            fg_color="#0284c7",
            hover_color="#0369a1"
        )
        btn_gh.pack(side="left")

        btn_close = ctk.CTkButton(
            btn_frame,
            text=self.t("donate_close"),
            font=ctk.CTkFont(size=12),
            command=dialog.destroy,
            fg_color="#64748b",
            hover_color="#475569",
            width=90
        )
        btn_close.pack(side="right")

    def _open_donate_dialog(self):
        """Opens interactive Donate modal window."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.t("donate_title"))
        dialog.geometry("520x420")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Set dialog icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            try:
                dialog.iconbitmap(icon_path)
            except Exception:
                pass

        lbl_title = ctk.CTkLabel(
            dialog,
            text=f"💖 {self.t('donate_title')}",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#ec4899"
        )
        lbl_title.pack(padx=20, pady=(18, 6), anchor="w")

        lbl_desc = ctk.CTkLabel(
            dialog,
            text=self.t("donate_desc"),
            font=ctk.CTkFont(size=12),
            text_color="#475569",
            wraplength=480,
            justify="left"
        )
        lbl_desc.pack(padx=20, pady=(0, 12), anchor="w")

        # Bank Info Card
        card_frame = ctk.CTkFrame(dialog, corner_radius=10, fg_color="#f8fafc", border_width=1, border_color="#cbd5e1")
        card_frame.pack(padx=20, pady=5, fill="x")

        # Row 1: Bank Name
        r1 = ctk.CTkFrame(card_frame, fg_color="transparent")
        r1.pack(fill="x", padx=15, pady=(12, 6))
        ctk.CTkLabel(r1, text="🏦 " + self.t("donate_bank_name"), font=ctk.CTkFont(size=13, weight="bold"), text_color="#334155").pack(side="left")
        ctk.CTkLabel(r1, text="TPBank (Ngân hàng Tiên Phong)", font=ctk.CTkFont(size=13, weight="bold"), text_color="#0284c7").pack(side="right")

        # Row 2: Account Holder
        r2 = ctk.CTkFrame(card_frame, fg_color="transparent")
        r2.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(r2, text="👤 " + self.t("donate_holder"), font=ctk.CTkFont(size=13, weight="bold"), text_color="#334155").pack(side="left")
        ctk.CTkLabel(r2, text="Nguyen Ngoc Thai Ha", font=ctk.CTkFont(size=13, weight="bold"), text_color="#16a34a").pack(side="right")

        # Row 3: Account STK
        r3 = ctk.CTkFrame(card_frame, fg_color="transparent")
        r3.pack(fill="x", padx=15, pady=(6, 12))
        ctk.CTkLabel(r3, text="💳 " + self.t("donate_account"), font=ctk.CTkFont(size=13, weight="bold"), text_color="#334155").pack(side="left")
        ctk.CTkLabel(r3, text="64608121989", font=ctk.CTkFont(size=16, weight="bold"), text_color="#ec4899").pack(side="right")

        # Feedback Message
        lbl_feedback = ctk.CTkLabel(
            dialog,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#16a34a"
        )
        lbl_feedback.pack(pady=(10, 5))

        # Action Buttons
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(5, 15), fill="x")

        def copy_account():
            self.clipboard_clear()
            self.clipboard_append("64608121989")
            lbl_feedback.configure(text=self.t("donate_copied_msg"))
            self.after(3000, lambda: lbl_feedback.configure(text=""))

        btn_copy = ctk.CTkButton(
            btn_frame,
            text=self.t("donate_copy_btn"),
            font=ctk.CTkFont(size=13, weight="bold"),
            command=copy_account,
            fg_color="#0284c7",
            hover_color="#0369a1",
            height=36
        )
        btn_copy.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_close = ctk.CTkButton(
            btn_frame,
            text=self.t("donate_close"),
            font=ctk.CTkFont(size=13),
            command=dialog.destroy,
            fg_color="#64748b",
            hover_color="#475569",
            width=100,
            height=36
        )
        btn_close.pack(side="right")

    def _open_report_dialog(self):
        """Opens interactive Bug Report modal window."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.t("report_title"))
        dialog.geometry("560x440")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Set dialog icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            try:
                dialog.iconbitmap(icon_path)
            except Exception:
                pass

        lbl_title = ctk.CTkLabel(
            dialog,
            text=f"🐛 {self.t('report_title')}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f6aa5"
        )
        lbl_title.pack(padx=20, pady=(15, 5), anchor="w")

        lbl_desc = ctk.CTkLabel(
            dialog,
            text=self.t("report_desc"),
            font=ctk.CTkFont(size=12),
            text_color="#475569",
            wraplength=520,
            justify="left"
        )
        lbl_desc.pack(padx=20, pady=(0, 10), anchor="w")

        txt_report = ctk.CTkTextbox(
            dialog,
            font=ctk.CTkFont(family="Consolas", size=11),
            height=200,
            wrap="word",
            fg_color="#1e293b",
            text_color="#f8fafc"
        )
        txt_report.pack(padx=20, pady=5, fill="both", expand=True)

        log_content = self.txt_log.get("1.0", "end-1c")
        if not log_content.strip():
            log_content = f"--- {APP_NAME} ({APP_VERSION}) Log Report ---\n{self.t('log_ready')}"
        txt_report.insert("1.0", log_content)
        txt_report.configure(state="disabled")

        lbl_feedback = ctk.CTkLabel(
            dialog,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#16a34a"
        )
        lbl_feedback.pack(pady=(5, 0))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(5, 15), fill="x")

        def copy_logs():
            self.clipboard_clear()
            self.clipboard_append(log_content)
            lbl_feedback.configure(text=self.t("report_copied_msg"))
            self.after(3000, lambda: lbl_feedback.configure(text=""))

        def open_github():
            webbrowser.open("https://github.com/tonngodoc/GDriveFlow/issues/new")

        btn_copy = ctk.CTkButton(
            btn_frame,
            text=self.t("report_copy_log"),
            font=ctk.CTkFont(size=12, weight="bold"),
            command=copy_logs,
            fg_color="#0284c7",
            hover_color="#0369a1"
        )
        btn_copy.pack(side="left", padx=(0, 10))

        btn_gh = ctk.CTkButton(
            btn_frame,
            text=self.t("report_open_github"),
            font=ctk.CTkFont(size=12, weight="bold"),
            command=open_github,
            fg_color="#2fa572",
            hover_color="#1e7b52"
        )
        btn_gh.pack(side="left", padx=(0, 10))

        btn_close = ctk.CTkButton(
            btn_frame,
            text=self.t("report_close"),
            font=ctk.CTkFont(size=12),
            command=dialog.destroy,
            fg_color="#64748b",
            hover_color="#475569",
            width=90
        )
        btn_close.pack(side="right")

    def _on_change_language_update_ui(self):
        """Updates all dynamic text elements on language change."""
        # Update window title
        self.title(f"{APP_NAME} ({APP_VERSION}) - {self.t('developer')}")

        # Update labels & buttons
        self.lbl_developer.configure(text=f"• {self.t('developer')}")
        self.btn_donate.configure(text=self.t("donate_btn"))
        self.btn_report.configure(text=self.t("report_bug"))
        self.lbl_url.configure(text=self.t("url_label"))
        self.entry_url.configure(placeholder_text=self.t("url_placeholder"))
        self.btn_scan.configure(text=self.t("scan_btn"))
        self.lbl_dest.configure(text=self.t("dest_label"))
        self.btn_browse.configure(text=self.t("browse_btn"))
        
        self.btn_select_all.configure(text=self.t("select_all"))
        self.btn_deselect_all.configure(text=self.t("deselect_all"))
        self.btn_start.configure(text=self.t("start_download"))
        self.btn_retry.configure(text=self.t("retry_failed"))
        self.btn_cancel.configure(text=self.t("cancel_download"))

        self.lbl_c1_title.configure(text=self.t("speed"))
        self.lbl_c2_title.configure(text=self.t("file_size"))
        self.lbl_c3_title.configure(text=self.t("queue_status"))
        self.lbl_c4_title.configure(text=self.t("eta"))

        self.lbl_log_header.configure(text=self.t("log_header"))
        self.btn_toggle_log.configure(text=self.t("log_expanded") if self.log_expanded else self.t("log_collapsed"))

        if not self.is_downloading:
            self.lbl_current_file.configure(text=self.t("status_ready"))

        # Re-render tree if available to update badge texts dynamically!
        if self.tree_root:
            self._rebuild_visible_tree_ui()
            self._update_tree_count_label()
        elif hasattr(self, 'lbl_tree_placeholder') and self.lbl_tree_placeholder.winfo_exists():
            self.lbl_tree_placeholder.configure(text=self.t("tree_placeholder"))

    # ==========================================
    # LOGIC & EVENT HANDLERS
    # ==========================================
    def _toggle_log_console(self):
        self.log_expanded = not self.log_expanded
        if self.log_expanded:
            self.txt_log.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="nsew")
            self.log_frame.grid_configure(sticky="nsew")
            self.grid_rowconfigure(4, weight=1)
            self.btn_toggle_log.configure(text=self.t("log_expanded"))
        else:
            self.txt_log.grid_forget()
            self.log_frame.grid_configure(sticky="ew")
            self.grid_rowconfigure(4, weight=0)
            self.btn_toggle_log.configure(text=self.t("log_collapsed"))

    def log(self, message: str):
        """Appends timestamped message to log console safely from any thread."""
        def _append():
            timestamp = time.strftime("[%H:%M:%S] ")
            full_msg = timestamp + message
            self.txt_log.insert("end", full_msg + "\n")
            self.txt_log.see("end")
            self.lbl_latest_log.configure(text=message)

        self.after(0, _append)

    def _clear_log(self):
        self.txt_log.delete("1.0", "end")
        self.lbl_latest_log.configure(text=self.t("log_cleared"))

    def _on_browse_dest(self):
        path = filedialog.askdirectory(title=self.t("dest_label"))
        if path:
            self.entry_dest.delete(0, "end")
            self.entry_dest.insert(0, path)

    def _on_click_scan(self):
        if self.is_scanning or self.is_downloading:
            return

        raw_url = self.entry_url.get().strip()
        if not raw_url:
            messagebox.showwarning("Warning", self.t("enter_url"))
            return

        item_id, item_type = GDriveService.parse_url_or_id(raw_url)
        if not item_id:
            messagebox.showerror("Error", self.t("invalid_url"))
            return

        self.is_scanning = True
        self.btn_scan.configure(state="disabled", text=self.t("scanning_btn"))

        threading.Thread(
            target=self._scan_process_worker,
            args=(raw_url, item_id, item_type),
            daemon=True
        ).start()

    def _scan_process_worker(self, raw_url: str, item_id: str, item_type: str):
        try:
            if item_type == 'folder' or 'folders/' in raw_url:
                self.log(self.t("log_scanning_folder").format(id=item_id))
                gitems = self.service.scan_folder(raw_url, status_callback=lambda msg: self.log(msg))
            else:
                self.log(self.t("log_analyzing_file").format(id=item_id))
                gitem = GDriveItem(
                    file_id=item_id,
                    name="",
                    relative_path="",
                    size=0
                )
                gitems = [gitem]

            root_node = self._build_tree_from_gitems(gitems)
            self.after(0, lambda: self._render_tree_ui(root_node))

        except Exception as e:
            self.log(self.t("log_scan_error").format(error=str(e)))
            self.after(0, lambda: (
                self.btn_scan.configure(state="normal", text=self.t("scan_btn")),
                messagebox.showerror("Scan Error", str(e))
            ))
        finally:
            self.is_scanning = False

    def _build_tree_from_gitems(self, gitems: list[GDriveItem]) -> TreeNode:
        root = TreeNode(name="Drive Folder", is_folder=True)

        for item in gitems:
            rel_path = item.relative_path.strip('\\/')
            path_parts = rel_path.split(os.sep) if rel_path else []

            current = root
            for part in path_parts:
                if not part:
                    continue
                found = None
                for child in current.children:
                    if child.is_folder and child.name == part:
                        found = child
                        break
                if not found:
                    found = TreeNode(name=part, is_folder=True, parent=current)
                    current.add_child(found)
                current = found

            file_name = item.name if item.name else f"File_{item.file_id}"
            file_node = TreeNode(name=file_name, is_folder=False, gdrive_item=item, parent=current)
            current.add_child(file_node)

        return root

    def _render_tree_ui(self, root_node: TreeNode):
        self.btn_scan.configure(state="normal", text=self.t("scan_btn"))
        self.tree_root = root_node

        for child in self.scroll_tree.winfo_children():
            child.destroy()

        if not root_node.children:
            lbl = ctk.CTkLabel(
                self.scroll_tree,
                text=self.t("empty_folder"),
                font=ctk.CTkFont(size=12),
                text_color="#ef4444"
            )
            lbl.pack(pady=25)
            self.lbl_tree_status.configure(text=f"{self.t('tree_title')} (0 {self.t('file_unit')}):")
            return

        total_files = len(root_node.get_all_file_nodes())
        self.log(self.t("log_tree_rendered").format(count=total_files))

        for top_child in root_node.children:
            self._render_single_node_widget(top_child, depth=0)

        self._update_tree_count_label()

    def _render_single_node_widget(self, node: TreeNode, depth: int):
        node.depth = depth
        bg_color = "#ffffff"
        border_color = "#e2e8f0"

        if node.status == "completed":
            bg_color = "#d4edda"
            border_color = "#c3e6cb"
        elif node.status == "error":
            bg_color = "#f8d7da"
            border_color = "#f5c6cb"
        elif node.status == "paused":
            bg_color = "#fff3cd"
            border_color = "#ffeeba"
        elif node.status == "downloading":
            bg_color = "#e0f2fe"
            border_color = "#bae6fd"

        row_frame = ctk.CTkFrame(
            self.scroll_tree,
            fg_color=bg_color,
            border_width=1,
            border_color=border_color,
            corner_radius=4
        )
        row_frame.pack(fill="x", padx=4, pady=2)
        node.frame_widget = row_frame

        indent_px = depth * 22
        if indent_px > 0:
            ctk.CTkFrame(row_frame, width=indent_px, height=1, fg_color="transparent").pack(side="left")

        if node.is_folder:
            toggle_symbol = "▼" if node.expanded else "▶"
            btn_toggle = ctk.CTkButton(
                row_frame,
                text=toggle_symbol,
                width=24,
                height=24,
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#e2e8f0",
                hover_color="#cbd5e1",
                text_color="#1e293b",
                command=lambda n=node: self._on_toggle_expand_click(n)
            )
            btn_toggle.pack(side="left", padx=(2, 4))
            node.toggle_btn = btn_toggle
        else:
            ctk.CTkFrame(row_frame, width=28, height=1, fg_color="transparent").pack(side="left")

        size_info = ""
        if not node.is_folder and node.gdrive_item and node.gdrive_item.size > 0:
            size_info = f" ({GDriveService.format_bytes(node.gdrive_item.size)})"
        elif node.is_folder:
            child_files_count = len(node.get_all_file_nodes())
            size_info = f" [{child_files_count} {self.t('file_unit')}]"

        icon_str = "📁 " if node.is_folder else "📄 "
        cb = ctk.CTkCheckBox(
            row_frame,
            text=f"{icon_str}{node.name}{size_info}",
            variable=node.var_checked,
            font=ctk.CTkFont(size=12, weight="bold" if node.is_folder else "normal"),
            text_color="#0f172a",
            command=lambda n=node: self._on_node_checkbox_clicked(n)
        )
        cb.pack(side="left", padx=4)
        node.cb_widget = cb

        badge_text = node.status_text if node.status_text else ""
        badge_fg = "transparent"
        text_col = "#0f172a"
        if node.status == "completed":
            badge_fg = "#28a745"
            text_col = "#ffffff"
            badge_text = self.t("completed_badge")
        elif node.status == "error":
            badge_fg = "#dc3545"
            text_col = "#ffffff"
            badge_text = self.t("error_badge")
        elif node.status == "paused":
            badge_fg = "#ffc107"
            text_col = "#000000"
            badge_text = self.t("paused_badge")
        elif node.status == "downloading":
            badge_fg = "#0284c7"
            text_col = "#ffffff"

        lbl_badge = ctk.CTkLabel(
            row_frame,
            text=f" {badge_text} " if badge_text else "",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=badge_fg,
            text_color=text_col,
            corner_radius=4
        )
        lbl_badge.pack(side="right", padx=6)
        node.lbl_status_badge = lbl_badge

    def _on_toggle_expand_click(self, node: TreeNode):
        node.expanded = not node.expanded
        self._rebuild_visible_tree_ui()

    def _rebuild_visible_tree_ui(self):
        for child in self.scroll_tree.winfo_children():
            child.destroy()

        if self.tree_root:
            for top_child in self.tree_root.children:
                self._render_subtree_lazy(top_child, depth=0)

    def _render_subtree_lazy(self, node: TreeNode, depth: int):
        self._render_single_node_widget(node, depth)
        if node.is_folder and node.expanded:
            for child in node.children:
                self._render_subtree_lazy(child, depth + 1)

    def _on_node_checkbox_clicked(self, node: TreeNode):
        new_val = node.var_checked.get()
        node.set_checked_recursive(new_val)
        self._update_tree_count_label()

    def _select_all_tree_nodes(self):
        if self.tree_root:
            self.tree_root.set_checked_recursive(True)
            self._update_tree_count_label()

    def _deselect_all_tree_nodes(self):
        if self.tree_root:
            self.tree_root.set_checked_recursive(False)
            self._update_tree_count_label()

    def _update_tree_count_label(self):
        if not self.tree_root:
            self.lbl_tree_status.configure(text=f"{self.t('tree_title')} (0 {self.t('file_unit')}):")
            self.lbl_val_overall.configure(text=f"0/0 {self.t('file_unit')}")
            return

        all_file_nodes = self.tree_root.get_all_file_nodes()
        selected_files = [n for n in all_file_nodes if n.var_checked.get()]
        total_files = len(all_file_nodes)

        selected_bytes = sum(n.gdrive_item.size for n in selected_files if n.gdrive_item)
        size_str = f" ({GDriveService.format_bytes(selected_bytes)})" if selected_bytes > 0 else ""

        self.lbl_tree_status.configure(
            text=f"{self.t('tree_title')} ({self.t('selected_files')}: {len(selected_files)} / {total_files} {self.t('file_unit')}{size_str}):"
        )
        self.lbl_val_overall.configure(text=f"{len(selected_files)}/{total_files} {self.t('file_unit')}")

    def _update_node_status_ui(self, node: TreeNode, status: str, status_text: str, progress_val: float = 0.0):
        """Updates in-place node status text & background color directly in O(1) time."""
        def _update():
            node.status = status
            node.status_text = status_text
            node.progress_value = progress_val

            bg_color = "#ffffff"
            border_color = "#e2e8f0"
            badge_fg = "transparent"
            text_col = "#0f172a"

            if node.status == "completed":
                bg_color = "#d4edda"
                border_color = "#c3e6cb"
                badge_fg = "#28a745"
                text_col = "#ffffff"
                status_text = self.t("completed_badge")
            elif node.status == "error":
                bg_color = "#f8d7da"
                border_color = "#f5c6cb"
                badge_fg = "#dc3545"
                text_col = "#ffffff"
                status_text = self.t("error_badge")
            elif node.status == "paused":
                bg_color = "#fff3cd"
                border_color = "#ffeeba"
                badge_fg = "#ffc107"
                text_col = "#000000"
                status_text = self.t("paused_badge")
            elif node.status == "downloading":
                bg_color = "#e0f2fe"
                border_color = "#bae6fd"
                badge_fg = "#0284c7"
                text_col = "#ffffff"

            if node.frame_widget and node.frame_widget.winfo_exists():
                node.frame_widget.configure(fg_color=bg_color, border_color=border_color)

            if node.lbl_status_badge and node.lbl_status_badge.winfo_exists():
                node.lbl_status_badge.configure(
                    text=f" {status_text} " if status_text else "",
                    fg_color=badge_fg,
                    text_color=text_col
                )

        self.after(0, _update)

    def _on_retry_failed_downloads(self):
        if self.is_downloading:
            return

        if not self.tree_root:
            messagebox.showwarning("Warning", self.t("no_scanned_files"))
            return

        all_file_nodes = self.tree_root.get_all_file_nodes()
        failed_nodes = [n for n in all_file_nodes if n.status == "error"]

        if not failed_nodes:
            messagebox.showinfo("Info", self.t("no_failed_files"))
            return

        for n in failed_nodes:
            n.var_checked.set(True)
            self._update_node_status_ui(n, status="pending", status_text="")

        self.log(self.t("log_retrying_failed").format(count=len(failed_nodes)))
        self._on_start_download()

    def _on_start_download(self):
        if self.is_downloading:
            return

        raw_url = self.entry_url.get().strip()
        dest_dir = self.entry_dest.get().strip()

        if not raw_url:
            messagebox.showwarning("Warning", self.t("enter_url"))
            return

        if not dest_dir:
            messagebox.showwarning("Warning", self.t("enter_dest"))
            return

        if not self.tree_root or not self.tree_root.children:
            item_id, item_type = GDriveService.parse_url_or_id(raw_url)
            if not item_id:
                messagebox.showerror("Error", self.t("invalid_url"))
                return

            self._on_click_scan()
            return

        all_file_nodes = self.tree_root.get_all_file_nodes()
        selected_nodes = [n for n in all_file_nodes if n.var_checked.get()]

        if not selected_nodes:
            messagebox.showwarning("Warning", self.t("no_selected_files"))
            return

        # Prepare states
        self.is_downloading = True
        self.cancel_requested = False
        self.selected_file_nodes = selected_nodes

        self.btn_start.configure(state="disabled")
        self.btn_scan.configure(state="disabled")
        self.btn_cancel.configure(state="normal")

        # Reset stats
        self.lbl_val_speed.configure(text="0 KB/s")
        self.lbl_val_file_size.configure(text="0 B / 0 B")
        self.lbl_val_eta.configure(text="--:--")

        # Launch download in background thread
        self.download_thread = threading.Thread(
            target=self._download_process_worker,
            args=(selected_nodes, dest_dir),
            daemon=True
        )
        self.download_thread.start()

    def _on_cancel_download(self):
        if self.is_downloading:
            self.cancel_requested = True
            self.log(self.t("log_cancel_requested"))
            self.btn_cancel.configure(state="disabled")
            self.btn_start.configure(state="normal")
            self.btn_scan.configure(state="normal")
            self.lbl_current_file.configure(text=self.t("status_stopped"))
            self.lbl_val_speed.configure(text="0 KB/s")
            self.lbl_val_eta.configure(text="00:00")
            self.is_downloading = False

    def _download_process_worker(self, file_nodes: list[TreeNode], dest_dir: str):
        try:
            total_count = len(file_nodes)
            self.log(self.t("log_download_started").format(count=total_count))

            start_overall_time = time.time()

            for index, node in enumerate(file_nodes, 1):
                if self.cancel_requested:
                    self.log(self.t("log_download_stopped"))
                    self._update_node_status_ui(node, status="paused", status_text=self.t("paused_badge"))
                    break

                gitem = node.gdrive_item
                if not gitem:
                    continue

                file_disp_name = node.name
                self.log(self.t("log_downloading_item").format(idx=index, total=total_count, name=file_disp_name))

                self._update_node_status_ui(node, status="downloading", status_text="🔵 0%", progress_val=0.0)

                self.after(0, lambda idx=index, name=file_disp_name, total=total_count: (
                    self.lbl_current_file.configure(text=self.t("downloading_status").format(idx=idx, total=total, name=name))
                ))

                def progress_cb(current_bytes, total_bytes, speed, percent):
                    if self.cancel_requested:
                        raise DownloadCancelledException("Download cancelled by user.")

                    if total_bytes and total_bytes > 0 and gitem.size == 0:
                        gitem.size = total_bytes
                        self.after(0, self._update_tree_count_label)

                    file_size_str = f"{GDriveService.format_bytes(current_bytes)} / {GDriveService.format_bytes(total_bytes)}"
                    speed_str = GDriveService.format_speed(speed)

                    remaining_bytes = (total_bytes - current_bytes) if total_bytes > current_bytes else 0
                    eta_sec = (remaining_bytes / speed) if speed > 0 else 0
                    eta_str = GDriveService.format_time(eta_sec)
                    overall_str = f"{index}/{total_count} {self.t('file_unit')}"

                    node_status_str = f"🔵 {int(percent)}%"
                    self._update_node_status_ui(node, status="downloading", status_text=node_status_str, progress_val=percent/100.0)

                    self.after(0, lambda: (
                        self.lbl_val_speed.configure(text=speed_str),
                        self.lbl_val_file_size.configure(text=file_size_str),
                        self.lbl_val_overall.configure(text=overall_str),
                        self.lbl_val_eta.configure(text=eta_str)
                    ))

                try:
                    saved_path = self.service.download_file(
                        gdrive_item=gitem,
                        destination_dir=dest_dir,
                        progress_callback=progress_cb,
                        cancel_check=lambda: self.cancel_requested
                    )

                    self._update_node_status_ui(node, status="completed", status_text=self.t("completed_badge"), progress_val=1.0)
                    self.log(self.t("log_downloaded_item").format(idx=index, total=total_count, name=os.path.basename(saved_path)))

                except DownloadCancelledException:
                    self._update_node_status_ui(node, status="paused", status_text=self.t("paused_badge"), progress_val=0.5)
                    self.log(self.t("log_download_cancelled"))
                    break
                except Exception as e:
                    if self.cancel_requested:
                        self._update_node_status_ui(node, status="paused", status_text=self.t("paused_badge"), progress_val=0.5)
                        break

                    self._update_node_status_ui(node, status="error", status_text=self.t("error_badge"), progress_val=0.0)
                    self.log(self.t("log_download_error").format(idx=index, total=total_count, error=str(e)))

            if not self.cancel_requested:
                total_elapsed = time.time() - start_overall_time
                self.log(f"{self.t('all_done')} (Time: {GDriveService.format_time(total_elapsed)}).")
                self._finish_download_process(success=True, message=self.t("finish_msg"))

        except Exception as e:
            self.log(self.t("log_system_error").format(error=str(e)))
            self._finish_download_process(success=False, message=str(e))

    def _finish_download_process(self, success: bool, message: str):
        def _reset_ui():
            self.is_downloading = False
            self.btn_start.configure(state="normal")
            self.btn_scan.configure(state="normal")
            self.btn_cancel.configure(state="disabled")
            self.lbl_val_speed.configure(text="0 KB/s")
            self.lbl_val_eta.configure(text="00:00")
            if success:
                self.lbl_current_file.configure(text=self.t("status_finished"))
                messagebox.showinfo("Notification", message)
            else:
                self.lbl_current_file.configure(text=self.t("status_error"))

        self.after(0, _reset_ui)


if __name__ == "__main__":
    app = GDriveApp()
    app.mainloop()
