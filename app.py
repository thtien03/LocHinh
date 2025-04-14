import os
import sys
import subprocess
import importlib

# Danh sách các thư viện cần thiết
required_libraries = ['PyQt5', 'Pillow']

def check_and_install_libraries():
    """Kiểm tra và cài đặt các thư viện cần thiết"""
    print("Kiểm tra các thư viện cần thiết...")
    missing_libraries = []
    
    for lib in required_libraries:
        try:
            importlib.import_module(lib)
            print(f"- {lib}: Đã cài đặt")
        except ImportError:
            print(f"- {lib}: Chưa cài đặt")
            missing_libraries.append(lib)
    
    if missing_libraries:
        print("\nĐang cài đặt các thư viện thiếu...")
        for lib in missing_libraries:
            print(f"Cài đặt {lib}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                print(f"- {lib}: Cài đặt thành công")
            except subprocess.CalledProcessError:
                print(f"- {lib}: Cài đặt thất bại")
                return False
    
    return True

def main():
    """Hàm chính khởi chạy ứng dụng"""
    # Thêm thư mục hiện tại vào PATH
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    # Kiểm tra và cài đặt các thư viện cần thiết
    if not check_and_install_libraries():
        input("Bấm Enter để thoát...")
        return
    
    # Import và khởi chạy ứng dụng
    try:
        from PyQt5.QtWidgets import QApplication
        from interface.main_window import MainWindow
        
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Lỗi khi khởi chạy ứng dụng: {str(e)}")
        input("Bấm Enter để thoát...")

if __name__ == "__main__":
    main()
