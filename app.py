from __future__ import annotations

from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# AgriAI Cloud Demo: public, read-only showcase.
# This app intentionally contains NO database, upload form, or write operation.
# All numbers below are synthetic examples and are prominently labelled as such.
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="AgriAI | Bản demo nghiên cứu",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
:root { color-scheme: light; }
[data-testid="stAppViewContainer"] { background: #f4f8f4; color: #203529; }
[data-testid="stHeader"] { background: rgba(244,248,244,.92); }
[data-testid="stSidebar"] { background: #eaf2eb; border-right: 1px solid #d9e5da; }
[data-testid="stSidebar"] * { color: #203529; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1450px; }
.hero { background: linear-gradient(115deg,#174a2d 0%,#2d8050 62%,#83a85e 100%); padding: 1.5rem 1.7rem; border-radius: 18px; color: white; margin-bottom: 1.15rem; box-shadow: 0 8px 26px rgba(20,70,40,.12); }
.hero h1 { color: #fff !important; margin: 0 0 .3rem 0; font-size: 2.05rem; }
.hero p { color: #e7f4e8 !important; margin: 0; font-size: 1rem; }
.demo-banner { background: #fff3d8; border: 1px solid #efd69b; color: #704d12; padding: .8rem 1rem; border-radius: 12px; font-weight: 650; margin: .8rem 0 1.1rem 0; }
.section-sub { color: #66786c; margin-top: -.4rem; font-size: .92rem; }
div[data-testid="stMetric"] { background: white; border: 1px solid #e1eae2; padding: 14px 16px; border-radius: 14px; box-shadow: 0 2px 8px rgba(25,60,35,.035); }
div[data-testid="stMetricLabel"] p { color: #627567; }
div[data-testid="stMetricValue"] { color: #205d36; }
div[data-testid="stDataFrame"] { border: 1px solid #e1eae2; border-radius: 12px; overflow: hidden; }
.card { background: white; border: 1px solid #e1eae2; padding: 1rem 1.1rem; border-radius: 14px; height: 100%; }
.small-muted { color: #687b6d; font-size: .83rem; }
hr { border-color: #dfe8e0; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Synthetic, deterministic demonstration data: 5 groups x 5 time points x 3 repeats.
TIMES = [0, 6, 12, 24, 48]
FORMULAS = {
    "CT-A": {"ratio": "Tỷ lệ minh họa A", "dead": [0, 5, 12, 22, 32], "damage": [1.0, 1.4, 1.8, 2.4, 3.0]},
    "CT-B": {"ratio": "Tỷ lệ minh họa B", "dead": [0, 10, 20, 34, 42], "damage": [1.0, 1.8, 2.4, 3.8, 5.0]},
    "CT-C": {"ratio": "Tỷ lệ minh họa C", "dead": [0, 15, 27, 40, 46], "damage": [1.0, 3.0, 7.0, 14.0, 22.0]},
    "CT-D": {"ratio": "Tỷ lệ minh họa D", "dead": [0, 7, 16, 29, 38], "damage": [1.0, 1.2, 1.4, 1.7, 2.0]},
    "Đối chứng": {"ratio": "Không xử lý", "dead": [0, 2, 4, 6, 8], "damage": [1.0, 1.1, 1.2, 1.4, 1.5]},
}


def build_demo_data() -> pd.DataFrame:
    rows = []
    for formula, cfg in FORMULAS.items():
        group = "Đối chứng" if formula == "Đối chứng" else "Xử lý"
        for idx, hour in enumerate(TIMES):
            for rep in (1, 2, 3):
                dead = max(0, min(50, cfg["dead"][idx] + (rep - 2)))
                alive = 50 - dead
                damage_after = max(0.0, min(100.0, cfg["damage"][idx] + (rep - 2) * 0.15))
                rows.append({
                    "Công thức": formula,
                    "Tỷ lệ ghi chú": cfg["ratio"],
                    "Nhóm": group,
                    "Lần lặp": rep,
                    "Thời điểm (giờ)": hour,
                    "Rệp sống (đã xác minh)": alive,
                    "Rệp chết (đã xác minh)": dead,
                    "Tổn thương lá trước (%)": 1.0,
                    "Tổn thương lá tại thời điểm (%)": round(damage_after, 2),
                })
    return pd.DataFrame(rows)


def calculate_summary(raw: pd.DataFrame) -> pd.DataFrame:
    data = raw.copy()
    total = data["Rệp sống (đã xác minh)"] + data["Rệp chết (đã xác minh)"]
    data["Tỷ lệ chết quan sát (%)"] = data["Rệp chết (đã xác minh)"] / total * 100
    data["Mức thay đổi tổn thương (điểm %) "] = (
        data["Tổn thương lá tại thời điểm (%)"] - data["Tổn thương lá trước (%)"]
    )
    grouped = data.groupby(["Công thức", "Tỷ lệ ghi chú", "Nhóm", "Thời điểm (giờ)"], as_index=False).agg(
        **{
            "Tỷ lệ chết quan sát (%)": ("Tỷ lệ chết quan sát (%)", "mean"),
            "Mức thay đổi tổn thương (điểm %) ": ("Mức thay đổi tổn thương (điểm %) ", "mean"),
            "Tổn thương lá trung bình (%)": ("Tổn thương lá tại thời điểm (%)", "mean"),
            "Số lần lặp": ("Lần lặp", "count"),
        }
    )
    controls = grouped[grouped["Nhóm"] == "Đối chứng"][
        ["Thời điểm (giờ)", "Tỷ lệ chết quan sát (%)", "Mức thay đổi tổn thương (điểm %) "]
    ].rename(columns={
        "Tỷ lệ chết quan sát (%)": "Chết đối chứng (%)",
        "Mức thay đổi tổn thương (điểm %) ": "Tăng tổn thương đối chứng (điểm %)"
    })
    treated = grouped[grouped["Nhóm"] == "Xử lý"].merge(controls, on="Thời điểm (giờ)", how="left")
    denominator = 100 - treated["Chết đối chứng (%)"]
    treated["Tỷ lệ chết hiệu chỉnh Abbott (%)"] = (
        (treated["Tỷ lệ chết quan sát (%)"] - treated["Chết đối chứng (%)"])
        / denominator * 100
    )
    treated["Tăng tổn thương lá đã hiệu chỉnh (điểm %) "] = (
        treated["Mức thay đổi tổn thương (điểm %) "]
        - treated["Tăng tổn thương đối chứng (điểm %)"]
    )
    return treated.sort_values(["Thời điểm (giờ)", "Công thức"])


raw = build_demo_data()
summary = calculate_summary(raw)

with st.sidebar:
    st.markdown("## 🌿 AgriAI")
    st.caption("Bản trình diễn nghiên cứu")
    st.divider()
    page = st.radio(
        "ĐIỀU HƯỚNG",
        ["Tổng quan", "So sánh công thức", "Dữ liệu minh họa", "Kiến trúc AI", "Thông tin & giới hạn"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Chế độ truy cập**")
    st.success("Chỉ xem · Không ghi dữ liệu")
    st.caption("Bản demo công khai không nhận ảnh tải lên và không lưu thông tin người xem.")

st.markdown(
    """<div class="hero"><h1>🌿 AgriAI</h1>
    <p>Hệ thống nghiên cứu · Phân tích hình ảnh · Đánh giá chế phẩm sinh học</p></div>""",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="demo-banner">BẢN DEMO CHỈ XEM — TOÀN BỘ SỐ LIỆU LÀ GIẢ LẬP ĐỂ MINH HỌA GIAO DIỆN, KHÔNG PHẢI KẾT QUẢ THỰC NGHIỆM.</div>',
    unsafe_allow_html=True,
)

if page == "Tổng quan":
    st.header("Tổng quan nghiên cứu")
    st.markdown('<p class="section-sub">Minh họa cách AgriAI tổ chức dữ liệu và trình bày kết quả nghiên cứu.</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bản ghi minh họa", f"{len(raw)}")
    c2.metric("Công thức xử lý", "4")
    c3.metric("Mốc theo dõi", "5")
    c4.metric("Số lần lặp / nhóm / mốc", "3")

    a, b = st.columns(2)
    with a:
        st.subheader("Tình trạng mô hình AI")
        st.info("YOLO nhận diện rệp: chưa tích hợp trọng số đã huấn luyện.")
    with b:
        st.subheader("Phân tích tổn thương lá")
        st.info("Mô hình phân vùng lá: chưa tích hợp trọng số đã huấn luyện.")

    st.subheader("Diễn biến minh họa theo thời gian")
    selected_metric = st.selectbox(
        "Chỉ số hiển thị",
        ["Tỷ lệ chết hiệu chỉnh Abbott (%)", "Tăng tổn thương lá đã hiệu chỉnh (điểm %) "],
    )
    line = summary.pivot(index="Thời điểm (giờ)", columns="Công thức", values=selected_metric)
    fig = px.line(line.reset_index(), x="Thời điểm (giờ)", y=line.columns, markers=True,
                  title="Số liệu mô phỏng – không dùng làm kết luận nghiên cứu")
    fig.update_layout(legend_title_text="Công thức", plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig, use_container_width=True)

elif page == "So sánh công thức":
    st.header("So sánh các công thức nghiên cứu")
    hour = st.select_slider("Chọn mốc thời gian", options=TIMES, value=48, format_func=lambda x: f"{x} giờ" if x else "0 giờ")
    view = summary[summary["Thời điểm (giờ)"] == hour].copy()
    st.caption(f"Số liệu giả lập tại mốc {hour} giờ. Mỗi công thức minh họa có 3 lần lặp.")
    show = view[[
        "Công thức", "Tỷ lệ ghi chú", "Số lần lặp", "Tỷ lệ chết quan sát (%)",
        "Tỷ lệ chết hiệu chỉnh Abbott (%)", "Tổn thương lá trung bình (%)",
        "Tăng tổn thương lá đã hiệu chỉnh (điểm %) "
    ]].round(2)
    st.dataframe(show, hide_index=True, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Hiệu quả đối với rệp")
        fig1 = px.bar(view, x="Công thức", y="Tỷ lệ chết hiệu chỉnh Abbott (%)", color="Công thức", text_auto=".1f")
        fig1.update_layout(showlegend=False, yaxis_title="Tỷ lệ chết hiệu chỉnh (%)", xaxis_title="", plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig1, use_container_width=True)
    with right:
        st.subheader("Tổn thương lá")
        fig2 = px.bar(view, x="Công thức", y="Tăng tổn thương lá đã hiệu chỉnh (điểm %) ", color="Công thức", text_auto=".1f")
        fig2.update_layout(showlegend=False, yaxis_title="Điểm phần trăm", xaxis_title="", plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)
    st.warning("Demo không tự kết luận công thức tối ưu. Kết luận thực tế cần dữ liệu thật, đối chứng, lặp độc lập và kiểm định thống kê.")

elif page == "Dữ liệu minh họa":
    st.header("Bảng dữ liệu minh họa")
    st.caption("Mỗi dòng là một lần lặp của một công thức tại một mốc thời gian. Dữ liệu được tạo sẵn trong mã, không có thao tác ghi hoặc sửa dữ liệu.")
    formula_filter = st.selectbox("Lọc công thức", ["Tất cả"] + list(FORMULAS.keys()))
    view = raw if formula_filter == "Tất cả" else raw[raw["Công thức"] == formula_filter]
    st.dataframe(view, use_container_width=True, hide_index=True)

elif page == "Kiến trúc AI":
    st.header("Các thành phần AI dự kiến")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 1. Nhận diện rệp")
        st.write("Mục tiêu: phát hiện vị trí và đếm cá thể rệp trên ảnh đã chuẩn hóa.")
        st.code("Input: ảnh lá\nOutput: bounding boxes + số lượng\nModel: YOLO (sẽ tích hợp sau khi huấn luyện)", language="text")
        st.info("Trạng thái: chưa có trọng số mô hình trong bản demo công khai.")
    with col2:
        st.markdown("### 2. Phân tích tổn thương lá")
        st.write("Mục tiêu: phân vùng lá và vùng có dấu hiệu tổn thương để tính tỷ lệ diện tích.")
        st.code("Input: ảnh lá chuẩn hóa\nOutput: mask vùng lá + mask tổn thương\nModel: segmentation (cần dataset gán nhãn)", language="text")
        st.info("Trạng thái: chưa có trọng số mô hình trong bản demo công khai.")
    st.markdown("### Kiểm chứng mô hình")
    st.write("Các chỉ số dự kiến: Precision, Recall, F1-score, MAE và RMSE; phải đối chiếu với bộ ảnh chuẩn được gán nhãn độc lập.")

else:
    st.header("Thông tin và giới hạn sử dụng")
    st.markdown("""
**Mục đích bản demo**

- Minh họa giao diện AgriAI và cách trình bày dữ liệu nghiên cứu.
- Minh họa quy trình so sánh song song hiệu quả đối với rệp và tổn thương lá.
- Cho phép người xem chuyển trang, lọc bảng và đổi mốc thời gian.

**Giới hạn**

- Tất cả số liệu trong bản demo là giả lập.
- Chưa tích hợp mô hình AI đã huấn luyện.
- Không nhận ảnh tải lên, không ghi dữ liệu và không lưu thông tin người xem.
- Không dùng biểu đồ này để kết luận hiệu lực hoặc độ an toàn của chế phẩm.

**Bản nghiên cứu cục bộ**

Dữ liệu thật tiếp tục được quản lý riêng trên máy tính của nhóm nghiên cứu. Không tải cơ sở dữ liệu, ảnh gốc hoặc trọng số mô hình riêng tư lên kho công khai.
""")
    st.caption(f"Phiên bản demo · cập nhật {datetime.now().strftime('%d/%m/%Y')}")

st.divider()
st.caption("AgriAI · Bản demo công khai chỉ xem · Số liệu minh họa, không phải kết quả nghiên cứu thực tế.")
