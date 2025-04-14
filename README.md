# Ứng dụng Lọc Hình Ảnh

Ứng dụng giúp lọc hình ảnh dựa trên mã số trong tên file.

## Cài đặt

1. Đảm bảo bạn đã cài đặt Python 3.6 trở lên
2. Cài đặt các thư viện cần thiết:

```
pip install -r requirements.txt
```

Hoặc chạy file setup.py để tự động cài đặt:

```
python setup.py
```

## Cách sử dụng

1. Chạy ứng dụng bằng một trong các cách sau:
   - Chạy file `Lochinh.bat` (Khuyến nghị)
   - Chạy `python app.py` (Tự động kiểm tra và cài đặt thư viện)
   - Hoặc chạy `python main.py` 

2. Chọn thư mục chứa hình ảnh cần lọc
3. Nhập mã số để lọc hoặc chọn file txt chứa danh sách mã số
4. Chọn thư mục đầu ra để lưu hình ảnh đã lọc
5. Nhấn nút "Lọc hình ảnh"

## Khắc phục lỗi thường gặp

### Lỗi "QIcon is not defined"
Nếu bạn gặp lỗi này, hãy thử một trong các cách sau:
- Sử dụng file `app.py` thay vì `main.py` để khởi động ứng dụng
- Hoặc cài đặt lại thư viện PyQt5: `pip install --upgrade PyQt5`

### Lỗi "No module named 'PyQt5'"
Cài đặt thư viện PyQt5:
```
pip install PyQt5
```

### Lỗi "No module named 'PIL'"
Cài đặt thư viện Pillow:
```
pip install Pillow
```

### Lỗi khác
Nếu gặp các lỗi khác, hãy đảm bảo đã cài đặt đầy đủ các thư viện cần thiết:
```
pip install -r requirements.txt
```

## Tính năng

- Lọc hình ảnh dựa trên mã số có trong tên file
- Hỗ trợ nhiều định dạng hình ảnh phổ biến (.jpg, .png, .bmp, .gif...)
- Nhập mã số thủ công hoặc từ file txt
- Giao diện người dùng hiện đại và thân thiện

## Tạo file thực thi (.exe)
Nếu muốn tạo file thực thi để chạy ứng dụng mà không cần cài đặt Python:
1. Đảm bảo đã cài đặt pyinstaller: `pip install pyinstaller`
2. Chạy file build.bat hoặc lệnh:
```
python build_exe.py
```
3. File thực thi sẽ được tạo trong thư mục dist
