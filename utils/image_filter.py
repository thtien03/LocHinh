import os
import shutil
from PyQt5.QtCore import pyqtSignal

class ImageFilter:
    def __init__(self):
        # Cập nhật định dạng hình ảnh được hỗ trợ với nhiều định dạng phổ biến hơn
        self.supported_formats = [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
            '.webp', '.svg', '.ico', '.heic', '.heif', '.raw', '.cr2',
            '.nef', '.arw', '.dng', '.psd', '.xcf', '.ai', '.pdf'
        ]
        
    def is_image_file(self, filename):
        """Kiểm tra xem file có phải là hình ảnh không dựa vào phần mở rộng"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.supported_formats
    
    def match_code(self, filename, codes):
        """Kiểm tra xem tên file có chứa một trong các mã số không"""
        # Loại bỏ phần mở rộng
        name_without_ext = os.path.splitext(filename)[0]
        
        for code in codes:
            if code in name_without_ext:
                return True
        return False
    
    def filter_images(self, input_folder, output_folder, codes, progress_callback=None):
        """
        Lọc và sao chép hình ảnh từ thư mục đầu vào sang thư mục đầu ra dựa trên danh sách mã.
        
        Args:
            input_folder (str): Đường dẫn thư mục chứa hình ảnh cần lọc
            output_folder (str): Đường dẫn thư mục lưu hình ảnh đã lọc
            codes (list): Danh sách các mã để lọc hình ảnh
            progress_callback (function): Hàm callback để cập nhật tiến trình
            
        Returns:
            tuple: (summary_message, results_dict) - Thông báo tổng kết và từ điển kết quả cho từng mã
        """
        # Kiểm tra thư mục đầu vào
        if not os.path.exists(input_folder):
            return "Thư mục đầu vào không tồn tại!", {}
            
        # Tạo thư mục đầu ra nếu chưa tồn tại
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Lấy danh sách tất cả các file trong thư mục đầu vào
        all_files = []
        for root, _, files in os.walk(input_folder):
            for file in files:
                if self.is_image_file(file):
                    all_files.append(os.path.join(root, file))
        
        # Khởi tạo biến đếm và từ điển kết quả
        total_copied = 0
        results_dict = {code: False for code in codes}  # False = chưa tìm thấy hình nào
        
        # Xử lý từng file
        for i, file_path in enumerate(all_files):
            file_name = os.path.basename(file_path)
            
            # Kiểm tra xem file có chứa bất kỳ mã nào trong danh sách không
            for code in codes:
                if code in file_name:
                    # Đường dẫn đầu ra
                    dest_path = os.path.join(output_folder, file_name)
                    
                    # Sao chép file
                    try:
                        shutil.copy2(file_path, dest_path)
                        total_copied += 1
                        results_dict[code] = True  # Đánh dấu đã tìm thấy hình cho mã này
                    except Exception:
                        # Nếu có lỗi khi sao chép, vẫn giữ nguyên trạng thái False cho mã này
                        pass
                    break
            
            # Cập nhật tiến trình
            if progress_callback:
                progress = int((i + 1) / len(all_files) * 100)
                progress_callback.emit(progress)
        
        # Tính toán số mã đã tìm thấy hình
        successful_codes = sum(1 for success in results_dict.values() if success)
        
        # Tạo thông báo tổng kết
        summary = f"Đã lọc và sao chép {total_copied} hình ảnh cho {successful_codes}/{len(codes)} mã số."
        
        # Nếu có mã không tìm thấy, bổ sung thông báo
        if successful_codes < len(codes):
            summary += f"\nKhông tìm thấy hình ảnh cho {len(codes) - successful_codes} mã số."
        
        return summary, results_dict
