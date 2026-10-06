# 📚 Hệ Thống Quản Lý Học Tập Cá Nhân

Ứng dụng quản lý học tập cá nhân được xây dựng bằng **Python + Streamlit**.

Chương trình giúp sinh viên quản lý môn học, điểm số, bài tập/deadline, mục tiêu học tập và thời khóa biểu trên một giao diện web đơn giản.

## ✨ Chức năng

* 👤 Quản lý thông tin sinh viên: họ tên và mã số sinh viên.
* 📚 Quản lý môn học:

  * Mã môn
  * Tên môn học
  * Số tín chỉ
  * Điểm số
  * Thêm mới hoặc cập nhật môn học
* 🎯 Tính **GPA tích lũy tự động** theo số tín chỉ.
* 📝 Quản lý bài tập và deadline:

  * Tên bài tập
  * Mã môn
  * Hạn nộp
  * Trạng thái: Chưa xong / Đang làm / Hoàn thành
* 🎯 Quản lý mục tiêu học tập và đánh dấu hoàn thành.
* 📅 Quản lý thời khóa biểu theo từng ngày trong tuần.
* 💾 Lưu dữ liệu vào file `learning_data.json`.

## 🛠️ Công nghệ sử dụng

* **Python 3**
* **Streamlit** – xây dựng giao diện web
* **Pandas** – hiển thị dữ liệu môn học dạng bảng
* **JSON** – lưu trữ dữ liệu

## 📁 Cấu trúc dự án

```text
project/
├── hoctap.py
├── learning_data.json
└── README.md
```

### Mô tả file

| File                 | Chức năng                                                             |
| -------------------- | --------------------------------------------------------------------- |
| `hoctap.py`          | File chương trình chính của ứng dụng                                  |
| `learning_data.json` | Lưu thông tin sinh viên, môn học, mục tiêu, bài tập và thời khóa biểu |
| `README.md`          | Tài liệu hướng dẫn sử dụng dự án                                      |

## ⚙️ Cài đặt

### 1. Cài Python

Cài **Python 3** nếu máy chưa có Python.

Kiểm tra bằng:

```bash
python --version
```

hoặc:

```bash
python3 --version
```

### 2. Cài thư viện

Mở Terminal/CMD tại thư mục dự án và chạy:

```bash
pip install streamlit pandas
```

Nếu máy sử dụng `pip3`:

```bash
pip3 install streamlit pandas
```

## ▶️ Chạy chương trình

Trong thư mục chứa `hoctap.py`, chạy:

```bash
streamlit run hoctap.py
```

Sau khi chạy, Streamlit sẽ cung
