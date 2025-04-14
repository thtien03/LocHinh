"""
Script cài đặt tự động cho ứng dụng Lọc Hình Ảnh
Chạy file này để cài đặt các thư viện cần thiết
"""
import subprocess
import sys
import os

def check_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        return True
    except:
        return False

def install_requirements():
    print("Đang cài đặt các thư viện cần thiết...")
    
    # Kiểm tra file requirements.txt
    if not os.path.exists("requirements.txt"):
        print("Không tìm thấy file requirements.txt, tạo file mới...")
        with open("requirements.txt", "w") as f:
            f.write("PyQt5==5.15.6\nPillow==9.0.1\n")
    
    # Cài đặt thư viện từ requirements.txt
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Cài đặt thành công!")
        return True
    except subprocess.CalledProcessError:
        print("Lỗi khi cài đặt thư viện")
        return False

def create_directory_structure():
    print("Kiểm tra cấu trúc thư mục...")
    directories = ["interface", "utils"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Đã tạo thư mục {directory}")
            
            # Tạo file __init__.py trong thư mục
            with open(os.path.join(directory, "__init__.py"), "w") as f:
                f.write("# Tệp tin này để đánh dấu thư mục là một gói Python\n")

if __name__ == "__main__":
    print("===== THIẾT LẬP ỨNG DỤNG LỌC HÌNH ẢNH =====")
    
    # Kiểm tra pip
    if not check_pip():
        print("Không tìm thấy pip. Vui lòng cài đặt pip trước.")
        sys.exit(1)
    
    # Tạo cấu trúc thư mục
    create_directory_structure()
    
    # Cài đặt các thư viện
    if install_requirements():
        print("\nThiết lập hoàn tất!")
        print("Bạn có thể chạy ứng dụng bằng lệnh: python main.py")
    else:
        print("\nThiết lập chưa hoàn tất. Vui lòng kiểm tra lỗi và thử lại.")

from setuptools import setup, find_packages

setup(
    name="App_LocHinh",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "Pillow",  # Cần thiết cho xử lý hình ảnh
    ],
    author="Trần Hữu Tiến",
    description="Ứng dụng lọc hình ảnh",
    python_requires=">=3.6",
)
