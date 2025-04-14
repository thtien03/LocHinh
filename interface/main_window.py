import os
import webbrowser
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QLineEdit, 
                            QTextEdit, QProgressBar, QMessageBox, QGroupBox,
                            QRadioButton, QButtonGroup, QFrame,
                            QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from utils.image_filter import ImageFilter

class FilterThread(QThread):
    progress_update = pyqtSignal(int)
    finished_signal = pyqtSignal(str, dict)
    
    def __init__(self, image_filter, input_folder, output_folder, codes):
        super().__init__()
        self.image_filter = image_filter
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.codes = codes
        
    def run(self):
        result_message, results_dict = self.image_filter.filter_images(
            self.input_folder, 
            self.output_folder, 
            self.codes, 
            self.progress_update
        )
        self.finished_signal.emit(result_message, results_dict)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_filter = ImageFilter()
        self.input_folder = ""
        self.output_folder = ""
        self.codes = []
        self.init_ui()
        
    def init_ui(self):
        # Thiết lập cửa sổ chính
        self.setWindowTitle("Ứng dụng Lọc Hình Ảnh")
        self.setMinimumSize(1200, 600)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QGroupBox {
                border: 1px solid #d0d7de;
                border-radius: 8px;
                margin-top: 1.5ex;
                font-weight: bold;
                background-color: #ffffff;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #0969da;
            }
            QPushButton {
                background-color: #0969da;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #0452bc;
            }
            QPushButton:pressed {
                background-color: #0347a5;
            }
            QPushButton:disabled {
                background-color: #8cb4e8;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 10px;
                background-color: #ffffff;
                font-size: 14px;
                min-height: 40px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #0969da;
            }
            QProgressBar {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                text-align: center;
                background-color: #ffffff;
                min-height: 25px;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background-color: #0969da;
                border-radius: 6px;
            }
            QRadioButton {
                font-size: 14px;
                margin: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QLabel {
                font-size: 14px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f2f5;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #d0d7de;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a7b0;
            }
        """)
        
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Tiêu đề với phông chữ lớn và màu sắc rõ ràng
        title_label = QLabel("ỨNG DỤNG LỌC HÌNH ẢNH (by Trần Hữu Tiến)")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("""
            color: #0969da; 
            margin-bottom: 20px;
            padding: 10px;
            background-color: #ffffff;
            border-radius: 8px;
            border-bottom: 3px solid #0969da;
        """)
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(title_label)
        
        # Tạo layout cho phần chính của ứng dụng
        content_layout = QHBoxLayout()
        
        # Phần bên trái: Thư mục đầu vào và đầu ra
        left_panel = QVBoxLayout()
        
        # Nhóm chọn thư mục đầu vào với biểu tượng
        input_group = QGroupBox("Thư mục hình ảnh đầu vào")
        input_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        input_layout = QVBoxLayout()
        
        input_desc = QLabel("Chọn thư mục chứa hình ảnh cần lọc:")
        input_desc.setStyleSheet("color: #57606a; font-size: 13px;")
        input_layout.addWidget(input_desc)
        
        input_field_layout = QHBoxLayout()
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText("Đường dẫn thư mục chứa hình ảnh cần lọc...")
        self.input_path_edit.setReadOnly(True)
        
        input_browse_btn = QPushButton("Chọn thư mục")
        input_browse_btn.setIcon(QIcon())
        input_browse_btn.clicked.connect(self.browse_input_folder)
        
        input_field_layout.addWidget(self.input_path_edit, 4)
        input_field_layout.addWidget(input_browse_btn, 1)
        input_layout.addLayout(input_field_layout)
        
        input_group.setLayout(input_layout)
        left_panel.addWidget(input_group)
        
        # Nhóm thư mục đầu ra
        output_group = QGroupBox("Thư mục đầu ra")
        output_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        output_layout = QVBoxLayout()
        
        output_desc = QLabel("Chọn thư mục lưu hình ảnh sau khi lọc:")
        output_desc.setStyleSheet("color: #57606a; font-size: 13px;")
        output_layout.addWidget(output_desc)
        
        output_field_layout = QHBoxLayout()
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("Đường dẫn thư mục lưu hình ảnh đã lọc...")
        self.output_path_edit.setReadOnly(True)
        
        output_browse_btn = QPushButton("Chọn thư mục")
        output_browse_btn.setIcon(QIcon())
        output_browse_btn.clicked.connect(self.browse_output_folder)
        
        output_field_layout.addWidget(self.output_path_edit, 4)
        output_field_layout.addWidget(output_browse_btn, 1)
        
        output_layout.addLayout(output_field_layout)
        
        output_group.setLayout(output_layout)
        left_panel.addWidget(output_group)
        
        # Thêm phần tiến trình
        progress_group = QGroupBox("Tiến trình")
        progress_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #0969da;")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        
        progress_group.setLayout(progress_layout)
        left_panel.addWidget(progress_group)
        
        # Thêm một khoảng trống giãn ra
        left_panel.addStretch()
        
        # Phần bên phải: Mã lọc
        right_panel = QVBoxLayout()
        
        # Nhóm mã lọc
        filter_group = QGroupBox("Mã số để lọc hình ảnh")
        filter_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        filter_layout = QVBoxLayout()
        
        # Thêm mô tả
        filter_desc = QLabel("Nhập mã số để tìm và lọc hình ảnh tương ứng:")
        filter_desc.setStyleSheet("color: #57606a; font-size: 13px;")
        filter_layout.addWidget(filter_desc)
        
        # Thêm radio buttons để chọn phương thức nhập mã
        input_method_layout = QHBoxLayout()
        
        method_frame = QFrame()
        method_frame.setStyleSheet("""
            QFrame {
                background-color: #f6f8fa;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        method_layout = QHBoxLayout(method_frame)
        method_layout.setContentsMargins(10, 5, 10, 5)
        
        self.input_method_group = QButtonGroup(self)
        
        self.manual_input_radio = QRadioButton("Nhập mã thủ công")
        self.manual_input_radio.setChecked(True)
        self.file_input_radio = QRadioButton("Chọn file TXT")
        
        self.input_method_group.addButton(self.manual_input_radio)
        self.input_method_group.addButton(self.file_input_radio)
        
        method_layout.addWidget(self.manual_input_radio)
        method_layout.addWidget(self.file_input_radio)
        method_layout.addStretch()
        
        input_method_layout.addWidget(method_frame)
        filter_layout.addLayout(input_method_layout)
        
        # Container cho nhập mã thủ công
        self.manual_input_container = QWidget()
        manual_layout = QVBoxLayout(self.manual_input_container)
        manual_layout.setContentsMargins(0, 10, 0, 0)
        
        code_layout = QHBoxLayout()
        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("Nhập mã số để lọc (phân cách bằng dấu phẩy, khoảng trắng hoặc Enter)...")
        
        add_code_btn = QPushButton("Thêm mã")
        add_code_btn.setIcon(QIcon())
        add_code_btn.clicked.connect(self.add_code)
        
        clear_code_btn = QPushButton("Xóa mã")
        clear_code_btn.setStyleSheet("""
            background-color: #d73a49;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
            min-height: 40px;
        """)
        clear_code_btn.setIcon(QIcon())
        clear_code_btn.clicked.connect(self.clear_codes)
        
        code_layout.addWidget(self.code_edit, 4)
        code_layout.addWidget(add_code_btn, 1)
        code_layout.addWidget(clear_code_btn, 1)
        
        self.codes_edit = QTextEdit()
        self.codes_edit.setPlaceholderText("Danh sách mã số sẽ hiển thị ở đây...")
        self.codes_edit.setStyleSheet("""
            QTextEdit {
                background-color: #f6f8fa;
                border: 1px solid #d0d7de;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)
        
        manual_layout.addLayout(code_layout)
        manual_layout.addWidget(self.codes_edit)
        
        # Container cho chọn file TXT
        self.file_input_container = QWidget()
        file_layout = QVBoxLayout(self.file_input_container)
        file_layout.setContentsMargins(0, 10, 0, 0)
        
        file_desc = QLabel("Chọn file TXT chứa danh sách mã số (mỗi mã trên một dòng hoặc phân cách bằng dấu phẩy):")
        file_desc.setStyleSheet("color: #57606a; font-size: 13px;")
        file_layout.addWidget(file_desc)
        
        code_file_layout = QHBoxLayout()
        self.code_file_edit = QLineEdit()
        self.code_file_edit.setPlaceholderText("Đường dẫn file TXT chứa danh sách mã số...")
        self.code_file_edit.setReadOnly(True)
        
        code_file_btn = QPushButton("Chọn file TXT")
        code_file_btn.setIcon(QIcon())
        code_file_btn.clicked.connect(self.browse_code_file)
        
        code_file_layout.addWidget(self.code_file_edit, 4)
        code_file_layout.addWidget(code_file_btn, 1)
        
        file_layout.addLayout(code_file_layout)
        file_layout.addStretch()
        
        # Thêm containers vào layout chính
        filter_layout.addWidget(self.manual_input_container)
        filter_layout.addWidget(self.file_input_container)
        
        # Kết nối radio buttons với việc hiển thị/ẩn các containers
        self.manual_input_radio.toggled.connect(self.toggle_input_method)
        self.file_input_radio.toggled.connect(self.toggle_input_method)
        
        # Khởi tạo hiển thị ban đầu
        self.toggle_input_method()
        
        filter_group.setLayout(filter_layout)
        right_panel.addWidget(filter_group)
        
        # Thêm các panel vào layout chính
        content_layout.addLayout(left_panel, 1)  # Tỷ lệ 40%
        content_layout.addLayout(right_panel, 1)  # Tỷ lệ 60%
        
        main_layout.addLayout(content_layout)
        
        # Nút thực hiện
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        # Tạo frame cho nút
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        btn_container_layout = QHBoxLayout(button_frame)
        btn_container_layout.setContentsMargins(20, 10, 20, 10)
        
        self.filter_btn = QPushButton("LỌC HÌNH ẢNH")
        self.filter_btn.setMinimumHeight(60)
        self.filter_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.filter_btn.clicked.connect(self.start_filtering)
        self.filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #2da44e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2c974b;
            }
            QPushButton:pressed {
                background-color: #298e46;
            }
        """)
        
        reset_btn = QPushButton("Đặt lại")
        reset_btn.setMinimumHeight(60)
        reset_btn.setFont(QFont("Arial", 14))
        reset_btn.clicked.connect(self.reset_form)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6e7781;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5e6670;
            }
            QPushButton:pressed {
                background-color: #4e5560;
            }
        """)
        
        # Thêm nút Ủng hộ tôi (Đã ẩn)
        # donate_btn = QPushButton("Ủng hộ tôi")
        # donate_btn.setMinimumHeight(60)
        # donate_btn.setFont(QFont("Arial", 14))
        # donate_btn.clicked.connect(self.open_donate_page)
        # donate_btn.setStyleSheet("""
        #     QPushButton {
        #         background-color: #0969da;
        #         color: white;
        #         border: none;
        #         border-radius: 6px;
        #         padding: 10px 20px;
        #         font-weight: bold;
        #         font-size: 16px;
        #     }
        #     QPushButton:hover {
        #         background-color: #0452bc;
        #     }
        #     QPushButton:pressed {
        #         background-color: #0347a5;
        #     }
        # """)
        
        btn_container_layout.addWidget(self.filter_btn, 2)
        btn_container_layout.addWidget(reset_btn, 1)
        # btn_container_layout.addWidget(donate_btn, 1)  # Đã ẩn
        
        button_layout.addWidget(button_frame)
        main_layout.addLayout(button_layout)
        
    def toggle_input_method(self):
        """Hiển thị/ẩn các container nhập mã dựa trên radio button được chọn"""
        self.manual_input_container.setVisible(self.manual_input_radio.isChecked())
        self.file_input_container.setVisible(self.file_input_radio.isChecked())
            
    def browse_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục hình ảnh đầu vào")
        if folder:
            self.input_folder = folder
            self.input_path_edit.setText(folder)
            
    def browse_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục đầu ra")
        if folder:
            self.output_folder = folder
            self.output_path_edit.setText(folder)
            
    def browse_code_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file TXT chứa mã số", "", "Text Files (*.txt)")
        if file_path:
            self.code_file_edit.setText(file_path)
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    # Phân tách mã số bằng dấu phẩy, khoảng trắng, hoặc xuống dòng
                    import re
                    codes = re.split(r'[,\s]+', content)
                    self.codes = [code.strip() for code in codes if code.strip()]
                    self.codes_edit.setText("\n".join(self.codes))
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể đọc file: {str(e)}")
    
    def add_code(self):
        new_codes = self.code_edit.text().strip()
        if new_codes:
            # Phân tách mã bằng dấu phẩy, khoảng trắng hoặc xuống dòng
            import re
            codes_list = re.split(r'[,\s]+', new_codes)
            codes_list = [code.strip() for code in codes_list if code.strip()]
            
            self.codes.extend(codes_list)
            self.codes = list(set(self.codes))  # Loại bỏ trùng lặp
            self.codes_edit.setText("\n".join(self.codes))
            self.code_edit.clear()
    
    def clear_codes(self):
        """Xóa tất cả mã số đã nhập sau khi xác nhận"""
        reply = QMessageBox.question(self, 'Xác nhận', 
                                     'Bạn có chắc chắn muốn xóa tất cả mã số?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.codes = []
            self.codes_edit.clear()
            self.code_edit.clear()
    
    def start_filtering(self):
        # Kiểm tra các thông tin đầu vào
        if not self.input_folder:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn thư mục hình ảnh đầu vào!")
            return
            
        if not self.output_folder:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn thư mục đầu ra!")
            return
        
        # Nếu chọn phương thức file và chưa chọn file, hãy cập nhật danh sách mã
        if self.file_input_radio.isChecked() and self.code_file_edit.text():
            try:
                with open(self.code_file_edit.text(), 'r') as file:
                    content = file.read()
                    import re
                    codes = re.split(r'[,\s]+', content)
                    self.codes = [code.strip() for code in codes if code.strip()]
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể đọc file: {str(e)}")
                return
            
        if not self.codes:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập ít nhất một mã số để lọc!")
            return
        
        # Đổi trạng thái UI
        self.filter_btn.setEnabled(False)
        self.status_label.setText("Đang lọc hình ảnh...")
        self.progress_bar.setValue(0)
        
        # Bắt đầu tiến trình lọc trong một luồng riêng
        self.filter_thread = FilterThread(
            self.image_filter,
            self.input_folder,
            self.output_folder,
            self.codes
        )
        self.filter_thread.progress_update.connect(self.update_progress)
        self.filter_thread.finished_signal.connect(self.filtering_finished)
        self.filter_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def filtering_finished(self, result, results_dict):
        self.filter_btn.setEnabled(True)
        self.status_label.setText("Hoàn thành")
        
        # Tính toán tỷ lệ thành công
        total_codes = len(self.codes)
        successful_codes = sum(1 for success in results_dict.values() if success)
        
        # Tạo thông báo chi tiết
        detail_message = f"Kết quả chi tiết:\n"
        detail_message += f"- Tổng số mã cần tìm: {total_codes}\n"
        detail_message += f"- Số mã tìm thấy hình ảnh: {successful_codes}\n"
        detail_message += f"- Số mã không tìm thấy hình ảnh: {total_codes - successful_codes}\n\n"
        
        # Nếu có mã không thành công, liệt kê ra
        if successful_codes < total_codes:
            failed_codes = [code for code, success in results_dict.items() if not success]
            detail_message += "Các mã không tìm thấy hình ảnh:\n- " + "\n- ".join(failed_codes)
        
        # Hiển thị kết quả với thông tin chi tiết trong hộp thoại tùy chỉnh
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Kết quả lọc hình ảnh")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(result)
        msg_box.setDetailedText(detail_message)
        
        # Tạo nút "Xem chi tiết" và "Đóng"
        msg_box.setStandardButtons(QMessageBox.Open | QMessageBox.Close)
        msg_box.button(QMessageBox.Open).setText("Mở thư mục đầu ra")
        msg_box.button(QMessageBox.Close).setText("Đóng")
        
        # Hiển thị hộp thoại và xử lý kết quả
        choice = msg_box.exec_()
        
        # Nếu người dùng chọn "Mở thư mục đầu ra"
        if choice == QMessageBox.Open:
            os.startfile(self.output_folder)
    
    def reset_form(self):
        self.input_folder = ""
        self.output_folder = ""
        self.codes = []
        
        self.input_path_edit.clear()
        self.output_path_edit.clear()
        self.code_edit.clear()
        self.codes_edit.clear()
        self.code_file_edit.clear()
        
        self.progress_bar.setValue(0)
        self.status_label.setText("Sẵn sàng")
    
    def open_donate_page(self):
        """Mở trang ủng hộ trong trình duyệt web mặc định"""
        donate_url = "https://example.com/donate"  # Thay thế bằng URL thực tế của trang donate
        webbrowser.open(donate_url)
