
import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Nhập thông tin khoản tiền gửi để tính số tiền lãi.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

# Số tiền gửi
so_tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

# Kỳ hạn
ky_han = st.selectbox(
    "📅 Kỳ hạn",
    options=[1, 2, 3, 6, 9, 12, 18, 24, 36],
    format_func=lambda x: f"{x} tháng"
)

# Lãi suất
lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

# Hình thức nhận lãi
hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    options=[
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

st.divider()

# =========================
# TÍNH TOÁN
# =========================

# Lãi suất dạng thập phân
lai_suat_nam = lai_suat / 100

# Tổng tiền lãi theo công thức lãi đơn
tong_tien_lai = so_tien_gui * lai_suat_nam * ky_han / 12

# Xác định số kỳ nhận lãi
if hinh_thuc == "Cuối kỳ":
    so_ky_nhan_lai = 1
    tien_lai_dinh_ky = tong_tien_lai

elif hinh_thuc == "Hàng tháng":
    so_ky_nhan_lai = ky_han
    tien_lai_dinh_ky = tong_tien_lai / ky_han

else:  # Hàng quý
    so_ky_nhan_lai = ky_han / 3

    # Nếu kỳ hạn không chia hết cho 3,
    # vẫn tính tiền lãi trung bình mỗi quý
    tien_lai_dinh_ky = tong_tien_lai / so_ky_nhan_lai

tong_tien_nhan = so_tien_gui + tong_tien_lai

# =========================
# HIỂN THỊ KẾT QUẢ
# =========================

st.subheader("📊 KẾT QUẢ")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="💰 Tiền lãi định kỳ",
        value=f"{tien_lai_dinh_ky:,.0f} VNĐ"
    )

with col2:
    st.metric(
        label="📈 Tổng tiền lãi",
        value=f"{tong_tien_lai:,.0f} VNĐ"
    )

st.metric(
    label="💵 Tổng tiền nhận",
    value=f"{tong_tien_nhan:,.0f} VNĐ"
)

# =========================
# CHI TIẾT KHOẢN TIỀN
# =========================

st.divider()

st.subheader("📋 Chi tiết")

st.write(f"**Số tiền gốc:** {so_tien_gui:,.0f} VNĐ")
st.write(f"**Kỳ hạn:** {ky_han} tháng")
st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

if hinh_thuc == "Cuối kỳ":
    st.info(
        f"Bạn nhận toàn bộ tiền lãi {tong_tien_lai:,.0f} VNĐ "
        f"một lần khi kết thúc kỳ hạn."
    )

elif hinh_thuc == "Hàng tháng":
    st.info(
        f"Mỗi tháng bạn nhận khoảng "
        f"{tien_lai_dinh_ky:,.0f} VNĐ tiền lãi."
    )

else:
    st.info(
        f"Mỗi quý bạn nhận khoảng "
        f"{tien_lai_dinh_ky:,.0f} VNĐ tiền lãi."
    )

# =========================
# CÔNG THỨC
# =========================

with st.expander("📚 Xem công thức tính"):
    st.write("**Tổng tiền lãi:**")
    st.latex(
        r"Lãi = Tiền\ gốc \times Lãi\ suất\ năm \times "
        r"\frac{Số\ tháng}{12}"
    )

    st.write("**Tổng số tiền nhận:**")
    st.latex(
        r"Tổng\ tiền = Tiền\ gốc + Tổng\ tiền\ lãi"
    )

st.caption(
    "Lưu ý: Đây là công cụ tính theo phương pháp lãi đơn, "
    "chưa xét thuế, phí hoặc các quy định riêng của từng ngân hàng."
)

