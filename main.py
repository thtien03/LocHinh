import sys

try:
    from PyQt5.QtWidgets import QApplication
    from interface.main_window import MainWindow
except ModuleNotFoundError:
    print("Lỗi: Không tìm thấy thư viện PyQt5")
    print("Vui lòng cài đặt thư viện bằng lệnh: pip install PyQt5")
    print("Hoặc sử dụng lệnh: pip install -r requirements.txt")
    print("Nếu bạn đã cài đặt pip, mở Command Prompt và chạy lệnh trên")
    print("Sau khi cài đặt xong, chạy lại ứng dụng này")
    sys.exit(1)
except ImportError as e:
    print(f"Lỗi khi import module: {str(e)}")
    print("Vui lòng kiểm tra cấu trúc thư mục và các tệp tin")
    sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
