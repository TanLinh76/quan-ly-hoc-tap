import json
import os
import pandas as pd
import streamlit as st

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Hệ Thống Quản Lý Học Tập", page_icon="📚", layout="wide"
)

DATA_FILE = "learning_data.json"


# 2. CÁC HÀM XỬ LÝ DỮ LIỆU JSON
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "student_name": "Lê Tấn Linh",
        "student_id": "SV001",
        "courses": [],
        "goals": [],
        "tasks": [],
        "timetable": {},
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Khởi tạo dữ liệu trong Session State
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# 3. GIAO DIỆN TIÊU ĐỀ & SIDEBAR
st.title("📚 TRANG QUẢN LÝ HỌC TẬP CÁ NHÂN")
st.caption(
    f"Sinh viên: **{data['student_name']}** | MSSV: **{data['student_id']}**"
)

st.sidebar.header("⚙️ Cấu hình thông tin")
data["student_name"] = st.sidebar.text_input(
    "Họ và tên sinh viên", data["student_name"]
)
data["student_id"] = st.sidebar.text_input(
    "Mã số sinh viên (MSSV)", data["student_id"]
)
if st.sidebar.button("💾 Lưu thông tin cá nhân"):
    save_data(data)
    st.sidebar.success("Đã lưu thành công!")

# 4. TÍNH TOÁN GPA TỰ ĐỘNG
total_credits = sum(
    [c["credits"] for c in data["courses"] if c.get("grade") is not None]
)
total_points = sum(
    [
        c["grade"] * c["credits"]
        for c in data["courses"]
        if c.get("grade") is not None
    ]
)
gpa = (total_points / total_credits) if total_credits > 0 else 0.0

# Hiển thị các chỉ số tổng quan (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("🎯 GPA Tích Lũy", f"{gpa:.2f} / 10.0")
col2.metric("📖 Tổng Số Môn Học", len(data["courses"]))
pending_tasks = len(
    [t for t in data["tasks"] if t.get("status") != "Hoàn thành"]
)
col3.metric("📝 Bài Tập Cần Làm", pending_tasks)

st.divider()

# 5. CÁC TAB CHỨC NĂNG
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📚 Môn Học & Điểm Số",
        "📝 Bài Tập & Deadline",
        "🎯 Mục Tiêu Học Tập",
        "📅 Thời Khóa Biểu",
    ]
)

# --- TAB 1: QUẢN LÝ MÔN HỌC & ĐIỂM SỐ ---
with tab1:
    st.subheader("Danh sách môn học")
    col_a, col_b = st.columns([2, 1])

    with col_a:
        if data["courses"]:
            df_courses = pd.DataFrame(data["courses"])
            df_courses.columns = [
                "Mã Môn",
                "Tên Môn Học",
                "Số Tín Chỉ",
                "Điểm Số",
            ]
            st.dataframe(df_courses, use_container_width=True)
        else:
            st.info("Chưa có môn học nào. Bạn hãy thêm ở khung bên phải.")

    with col_b:
        st.write("**Thêm hoặc Cập nhật môn học**")
        c_code = st.text_input("Mã môn (Ví dụ: CS101)").strip()
        c_name = st.text_input("Tên môn học").strip()
        c_credits = st.number_input(
            "Số tín chỉ", min_value=1, max_value=10, value=3
        )
        c_grade = st.number_input(
            "Điểm số (Thang 10)", min_value=0.0, max_value=10.0, value=8.0
        )

        if st.button("➕ Thêm / Lưu Môn Học"):
            if c_code and c_name:
                # Kiểm tra nếu môn đã tồn tại thì cập nhật, chưa thì thêm mới
                existing = [
                    c
                    for c in data["courses"]
                    if c["code"].upper() == c_code.upper()
                ]
                if existing:
                    existing[0]["name"] = c_name
                    existing[0]["credits"] = c_credits
                    existing[0]["grade"] = c_grade
                else:
                    data["courses"].append(
                        {
                            "code": c_code,
                            "name": c_name,
                            "credits": c_credits,
                            "grade": c_grade,
                        }
                    )
                save_data(data)
                st.success(f"Đã lưu môn {c_name}!")
                st.rerun()
            else:
                st.warning("Vui lòng nhập đầy đủ Mã môn và Tên môn!")

# --- TAB 2: NHIỆM VỤ & DEADLINE ---
with tab2:
    st.subheader("Danh sách Nhiệm vụ / Bài tập")
    col_t1, col_t2 = st.columns([2, 1])

    with col_t1:
        if data["tasks"]:
            for idx, task in enumerate(data["tasks"]):
                status = task.get("status", "Chưa xong")
                color = (
                    "🟢"
                    if status == "Hoàn thành"
                    else ("🟡" if status == "Đang làm" else "🔴")
                )
                st.write(
                    f"{color} **{task['title']}** | Môn: `{task['course_code']}` | Hạn nộp: *{task['deadline']}* | Trạng thái: **{status}**"
                )
        else:
            st.info("Chưa có bài tập hay deadline nào.")

    with col_t2:
        st.write("**Thêm nhiệm vụ mới**")
        t_title = st.text_input("Tên bài tập/nhiệm vụ").strip()
        t_code = st.text_input("Mã môn liên quan").strip()
        t_deadline = st.date_input("Hạn nộp").strftime("%d/%m/%Y")
        t_status = st.selectbox(
            "Trạng thái", ["Chưa xong", "Đang làm", "Hoàn thành"]
        )

        if st.button("➕ Thêm Bài Tập"):
            if t_title:
                data["tasks"].append(
                    {
                        "title": t_title,
                        "course_code": t_code,
                        "deadline": t_deadline,
                        "status": t_status,
                    }
                )
                save_data(data)
                st.success("Đã thêm bài tập mới!")
                st.rerun()
            else:
                st.warning("Vui lòng nhập tên bài tập!")

# --- TAB 3: MỤC TIÊU HỌC TẬP ---
with tab3:
    st.subheader("Mục tiêu học tập")
    if data["goals"]:
        for idx, g in enumerate(data["goals"]):
            checked = st.checkbox(
                f"{g['title']} (Hạn hoàn thành: {g['target_date']})",
                value=g.get("completed", False),
                key=f"goal_{idx}",
            )
            if checked != g.get("completed"):
                g["completed"] = checked
                save_data(data)
                st.rerun()
    else:
        st.info("Chưa có mục tiêu nào được thiết lập.")

    st.divider()
    st.write("**Thêm mục tiêu mới**")
    g_title = st.text_input("Nội dung mục tiêu").strip()
    g_date = st.date_input("Hạn hoàn thành mục tiêu").strftime("%d/%m/%Y")
    if st.button("➕ Thêm Mục Tiêu"):
        if g_title:
            data["goals"].append(
                {"title": g_title, "target_date": g_date, "completed": False}
            )
            save_data(data)
            st.success("Đã thêm mục tiêu!")
            st.rerun()
        else:
            st.warning("Vui lòng nhập nội dung mục tiêu!")

# --- TAB 4: THỜI KHÓA BIỂU ---
with tab4:
    st.subheader("Thời khóa biểu tuần")
    selected_day = st.selectbox(
        "Chọn ngày trong tuần",
        [
            "Thứ 2",
            "Thứ 3",
            "Thứ 4",
            "Thứ 5",
            "Thứ 6",
            "Thứ 7",
            "Chủ Nhật",
        ],
    )

    current_schedule = "\n".join(data["timetable"].get(selected_day, []))
    new_schedule = st.text_area(
        f"Lịch học ngày {selected_day} (Nhập mỗi môn/tiết trên 1 dòng):",
        value=current_schedule,
        height=150,
    )

    if st.button("💾 Lưu Thời Khóa Biểu"):
        lines = [line.strip() for line in new_schedule.split("\n") if line.strip()]
        data["timetable"][selected_day] = lines
        save_data(data)
        st.success(f"Đã cập nhật lịch học cho {selected_day}!")

    st.divider()
    st.write("**Xem nhanh thời khóa biểu tuần:**")
    if data["timetable"]:
        for day, items in data["timetable"].items():
            if items:
                st.write(f"📌 **{day}:** {', '.join(items)}")