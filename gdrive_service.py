import os
import re
import time
import math
from typing import Callable, List, Dict, Optional, Tuple
import gdown
from gdown.parse_url import parse_url

class DownloadCancelledException(BaseException):
    """Custom exception inheriting from BaseException to bypass gdown's internal retry loops on cancellation."""
    pass


class GDriveItem:
    def __init__(self, file_id: str, name: str = "", relative_path: str = "", size: int = 0):
        self.file_id = file_id
        self.name = name
        self.relative_path = relative_path  # subfolder path relative to root download folder
        self.size = size  # in bytes


class GDriveService:
    def __init__(self):
        pass

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        r"""
        Sanitizes special/invalid characters (: ' $ ! ? * < > | " / \) from filenames
        and replaces them with underscores '_' to prevent Windows filesystem errors.
        """
        if not filename:
            return ""
        name_part, ext_part = os.path.splitext(filename)
        # Replace special characters with '_'
        sanitized_name = re.sub(r'[\/:*?"<>|:\'\$!]+', '_', name_part)
        sanitized_name = sanitized_name.strip(' .')
        if not sanitized_name:
            sanitized_name = "file"
        
        # Also clean extension if special characters exist in extension
        sanitized_ext = re.sub(r'[\/:*?"<>|:\'\$!]+', '_', ext_part)
        return f"{sanitized_name}{sanitized_ext}"

    @staticmethod
    def sanitize_relative_path(rel_path: str) -> str:
        """
        Sanitizes subfolder directory names in a relative path.
        """
        if not rel_path:
            return ""
        parts = rel_path.replace('\\', '/').split('/')
        sanitized_parts = []
        for p in parts:
            if p:
                s = re.sub(r'[\/:*?"<>|:\'\$!]+', '_', p).strip(' .')
                if s:
                    sanitized_parts.append(s)
        return os.path.join(*sanitized_parts) if sanitized_parts else ""

    @staticmethod
    def parse_url_or_id(url_or_id: str) -> Tuple[Optional[str], str]:
        """
        Parses a Google Drive URL or ID using gdown parser.
        Returns: (item_id, item_type) where item_type is 'folder', 'file', or 'unknown'
        """
        url_or_id = url_or_id.strip()
        if not url_or_id:
            return None, "unknown"

        # Folder URL check
        folder_match = re.search(r'folders/([a-zA-Z0-9_-]+)', url_or_id)
        if folder_match:
            return folder_match.group(1), 'folder'

        # File URL check
        file_id, is_download_link = parse_url(url_or_id)
        if file_id:
            return file_id, 'file'

        # Raw ID (typically ~20+ chars alphanumeric with _ and -)
        if re.match(r'^[a-zA-Z0-9_-]{20,}$', url_or_id):
            return url_or_id, 'unknown'

    @staticmethod
    def clean_error_message(err_msg: str) -> str:
        """Removes internal gdown repository URLs and sanitizes error text for end users."""
        if not err_msg:
            return "Unknown error occurred."

        # Strip third-party gdown URLs and FAQ references
        cleaned = re.sub(r'https?://github\.com/wkentaro/gdown[^\s]*', '', err_msg)
        cleaned = re.sub(r'Check FAQ in\s*', '', cleaned)
        cleaned = cleaned.strip(" .:\t\r\n")

        # Detect 401 / permission denied / restricted access
        if "401" in err_msg or "permission" in err_msg.lower() or "access" in err_msg.lower():
            return f"{cleaned}\n💡 Gợi ý: Vui lòng kiểm tra và mở quyền chia sẻ của Google Drive sang 'Bất kỳ ai có liên kết đều có thể xem' (Anyone with the link can view)."

        return cleaned if cleaned else err_msg

    def scan_folder(self, folder_url_or_id: str, status_callback: Optional[Callable[[str], None]] = None) -> List[GDriveItem]:
        """
        Scans a Google Drive folder (including subfolders and files) without requiring Google login.
        Returns a list of GDriveItem objects with sanitized filenames and subfolder paths.
        """
        item_id, item_type = self.parse_url_or_id(folder_url_or_id)
        if not item_id:
            raise Exception("Invalid Google Drive URL or Folder ID.")

        folder_url = f"https://drive.google.com/drive/folders/{item_id}"
        if status_callback:
            status_callback(f"🔍 Analyzing & scanning files from Google Drive...")

        try:
            files_to_download = gdown.download_folder(
                url=folder_url,
                skip_download=True,
                quiet=True
            )
        except Exception as e:
            cleaned_err = self.clean_error_message(str(e))
            raise Exception(f"Không thể lấy danh sách thư mục Google Drive (Folder ID: {item_id}). {cleaned_err}")

        gdrive_items = []
        if files_to_download:
            for item in files_to_download:
                rel_path = getattr(item, 'path', '')
                sub_dir = os.path.dirname(rel_path)
                real_file_name = os.path.basename(rel_path)
                file_id = getattr(item, 'id', '')

                # Sanitize special characters in file names and directory paths!
                clean_file_name = self.sanitize_filename(real_file_name)
                clean_sub_dir = self.sanitize_relative_path(sub_dir)

                if status_callback:
                    status_callback(f"Found: {os.path.join(clean_sub_dir, clean_file_name)}")

                gdrive_items.append(GDriveItem(
                    file_id=file_id,
                    name=clean_file_name,
                    relative_path=clean_sub_dir,
                    size=0
                ))

        return gdrive_items

    def download_file(
        self,
        gdrive_item: GDriveItem,
        destination_dir: str,
        progress_callback: Optional[Callable[[int, int, float, float], None]] = None,
        cancel_check: Optional[Callable[[], bool]] = None
    ) -> str:
        """
        Downloads a single GDriveItem into destination_dir, preserving the sanitized original file name.
        """
        clean_rel_path = self.sanitize_relative_path(gdrive_item.relative_path)
        target_dir = os.path.join(destination_dir, clean_rel_path)
        os.makedirs(target_dir, exist_ok=True)

        start_time = time.time()
        last_time = [start_time]
        last_bytes = [0]

        def _progress_hook(bytes_so_far: int, bytes_total: Optional[int]):
            if cancel_check and cancel_check():
                raise DownloadCancelledException("Download cancelled.")

            total = bytes_total if bytes_total and bytes_total > 0 else 0
            now = time.time()
            elapsed = now - last_time[0]

            if elapsed >= 0.15:
                chunk_bytes = bytes_so_far - last_bytes[0]
                speed = chunk_bytes / elapsed if elapsed > 0 else 0
                percent = (bytes_so_far / total * 100.0) if total > 0 else 50.0

                if progress_callback:
                    progress_callback(bytes_so_far, total, speed, percent)

                last_time[0] = now
                last_bytes[0] = bytes_so_far

        clean_name = self.sanitize_filename(gdrive_item.name)
        if clean_name and not clean_name.startswith("GDrive_File_"):
            target_output_path = os.path.join(target_dir, clean_name)
        else:
            target_output_path = os.path.join(target_dir, "")

        try:
            try:
                saved_path = gdown.download(
                    url=file_url,
                    output=target_output_path,
                    quiet=True,
                    progress=_progress_hook,
                    resume=True
                )
            except DownloadCancelledException:
                raise
            except Exception:
                saved_path = gdown.download(
                    id=gdrive_item.file_id,
                    output=target_output_path,
                    quiet=True,
                    progress=_progress_hook,
                    resume=True
                )
        except DownloadCancelledException:
            raise
        except Exception as err:
            cleaned_err = self.clean_error_message(str(err))
            raise Exception(cleaned_err)

        if not saved_path or not os.path.exists(str(saved_path)):
            raise Exception(f"Không thể tải tệp (ID: {gdrive_item.file_id}). Vui lòng kiểm tra quyền chia sẻ của tệp trên Google Drive.")

        # Post-download check: if gdown auto-saved under a raw filename with special chars, rename it safely!
        raw_saved_path = str(saved_path)
        dir_name = os.path.dirname(raw_saved_path)
        base_name = os.path.basename(raw_saved_path)
        sanitized_base_name = self.sanitize_filename(base_name)

        if base_name != sanitized_base_name:
            final_path = os.path.join(dir_name, sanitized_base_name)
            try:
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.rename(raw_saved_path, final_path)
                return final_path
            except Exception:
                return raw_saved_path

        return raw_saved_path

    @staticmethod
    def format_bytes(size_bytes: int) -> str:
        """Formats byte count to human-readable string (KB, MB, GB)."""
        if size_bytes <= 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    @staticmethod
    def format_speed(speed_bytes_sec: float) -> str:
        """Formats download speed to KB/s or MB/s."""
        if speed_bytes_sec <= 0:
            return "0 KB/s"
        if speed_bytes_sec >= 1024 * 1024:
            return f"{round(speed_bytes_sec / (1024 * 1024), 2)} MB/s"
        return f"{round(speed_bytes_sec / 1024, 1)} KB/s"

    @staticmethod
    def format_time(seconds: float) -> str:
        """Formats seconds into readable mm:ss or hh:mm:ss."""
        if seconds <= 0 or math.isinf(seconds) or math.isnan(seconds):
            return "00:00"
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"
