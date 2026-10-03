
import streamlit as st
st.image("logo.jpg.jpg")
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
st.title("💰APP CÔNG CỤ TÍNH LÃI GỬI TIẾT KIỆM_PHẠM KIỀU TƯỜNG VI")
st.write("Nhập thông tin khoản tiền gửi để tính số tiền lãi.")

st.divider()

# ============================================================
# 2. CẤU HÌNH LÃI SUẤT THAM CHIẾU
# ============================================================
# Đơn vị: %/năm

LAI_SUAT_THAM_CHIEU = {
    1: 3.0,
    3: 3.5,
    6: 4.8,
    9: 5.0,
    12: 5.3,
    18: 5.5,
    24: 5.7,
    36: 6.0
}


# ============================================================
# 3. HÀM ĐỌC SỐ TIỀN BẰNG TIẾNG VIỆT
# ============================================================

SO = [
    "không", "một", "hai", "ba", "bốn",
    "năm", "sáu", "bảy", "tám", "chín"
]


def doc_hang_chuc(n):
    """Đọc số từ 0 đến 99."""

    if n < 10:
        return SO[n]

    chuc = n // 10
    don_vi = n % 10

    if chuc == 1:
        ket_qua = "mười"
    else:
        ket_qua = SO[chuc] + " mươi"

    if don_vi == 0:
        return ket_qua

    if don_vi == 1 and chuc >= 2:
        ket_qua += " mốt"
    elif don_vi == 5:
        ket_qua += " lăm"
    else:
        ket_qua += " " + SO[don_vi]

    return ket_qua


def doc_hang_tram(n, day_du=True):
    """Đọc số từ 0 đến 999."""

    tram = n // 100
    phan_du = n % 100

    if tram == 0:
        if not day_du:
            return doc_hang_chuc(phan_du)
        if phan_du == 0:
            return ""
        if phan_du < 10:
            return "lẻ " + SO[phan_du]
        return doc_hang_chuc(phan_du)

    ket_qua = SO[tram] + " trăm"

    if phan_du == 0:
        return ket_qua

    if phan_du < 10:
        ket_qua += " lẻ " + SO[phan_du]
    else:
        ket_qua += " " + doc_hang_chuc(phan_du)

    return ket_qua


def doc_so_tien(n):
    """Đọc số tiền VNĐ bằng chữ."""

    n = int(round(n))

    if n == 0:
        return "Không đồng"

    if n < 0:
        return "Âm " + doc_so_tien(abs(n))

    don_vi_nhom = [
        (1_000_000_000, "tỷ"),
        (1_000_000, "triệu"),
        (1_000, "nghìn"),
        (1, "")
    ]

    ket_qua = []

    for gia_tri, ten in don_vi_nhom:

        if n >= gia_tri:

            so_nhom = n // gia_tri
            n %= gia_tri

            # Nhóm tỷ/triệu/nghìn
            if gia_tri >= 1000:
                phan_doc = doc_hang_tram(
                    so_nhom,
                    day_du=False
                )
            else:
                phan_doc = doc_hang_tram(
                    so_nhom,
                    day_du=False
                )

            if ten:
                ket_qua.append(phan_doc + " " + ten)
            else:
                ket_qua.append(phan_doc)

    return " ".join(ket_qua).capitalize() + " đồng"


# ============================================================
# 4. HÀM FORMAT TIỀN
# ============================================================

def format_money(value):
    return f"{value:,.0f} VNĐ"


# ============================================================
# 5. HÀM TÍNH LÃI ĐƠN
# ============================================================

def tinh_lai_don(
    tien_goc,
    lai_suat_nam,
    so_thang,
    tien_gui_hang_thang=0
):
    """
    Tính lãi đơn.

    Tiền gửi ban đầu:
        Lãi = Gốc * lãi suất * thời gian

    Tiền DCA:
        Mỗi khoản nộp thêm được tính lãi theo số tháng
        còn lại.
    """

    lai_suat_thang = lai_suat_nam / 100 / 12

    tong_lai = 0
    tong_goc = tien_goc

    # Lãi của khoản tiền gửi ban đầu
    tong_lai += tien_goc * lai_suat_thang * so_thang

    # Lãi của các khoản DCA
    for thang in range(1, so_thang + 1):
        so_thang_con_lai = so_thang - thang + 1

        tong_lai += (
            tien_gui_hang_thang
            * lai_suat_thang
            * so_thang_con_lai
        )

        tong_goc += tien_gui_hang_thang

    return tong_goc, tong_lai


# ============================================================
# 6. HÀM TÍNH LÃI KÉP
# ============================================================

def tinh_lai_kep(
    tien_goc,
    lai_suat_nam,
    so_thang,
    tien_gui_hang_thang=0
):
    """
    Tính lãi kép với kỳ nhập lãi hàng tháng.

    Mỗi tháng:
        Gốc mới = Gốc cũ + tiền DCA + lãi tháng
    """

    lai_suat_thang = lai_suat_nam / 100 / 12

    so_du = tien_goc
    tong_goc = tien_goc

    lich = []

    for thang in range(1, so_thang + 1):

        goc_dau_ky = so_du

        # DCA vào đầu mỗi tháng
        so_du += tien_gui_hang_thang
        tong_goc += tien_gui_hang_thang

        lai_thang = so_du * lai_suat_thang

        so_du += lai_thang

        lich.append({
            "Kỳ": thang,
            "Gốc đầu kỳ": goc_dau_ky,
            "Tiền gửi thêm": tien_gui_hang_thang,
            "Tiền lãi kỳ này": lai_thang,
            "Tổng gốc đã gửi": tong_goc,
            "Tổng tài sản": so_du
        })

    tong_lai = so_du - tong_goc

    return tong_goc, tong_lai, so_du, lich


# ============================================================
# 7. TẠO LỊCH CHI TIẾT
# ============================================================

def tao_lich(
    tien_goc,
    lai_suat_nam,
    so_thang,
    tien_gui_hang_thang,
    ngay_bat_dau
):

    lai_suat_thang = lai_suat_nam / 100 / 12

    so_du_don = tien_goc
    so_du_kep = tien_goc

    tong_goc = tien_goc

    lich = []

    for thang in range(1, so_thang + 1):

        ngay_nhan = (
            ngay_bat_dau
            + relativedelta(months=thang)
        )

        # ========================
        # LÃI ĐƠN
        # ========================

        lai_don = (
            (tien_goc + tien_gui_hang_thang * (thang - 1))
            * lai_suat_thang
        )

        # ========================
        # LÃI KÉP
        # ========================

        goc_dau_ky = so_du_kep

        so_du_kep += tien_gui_hang_thang
        tong_goc += tien_gui_hang_thang

        lai_kep = so_du_kep * lai_suat_thang

        so_du_kep += lai_kep

        lich.append({
            "Kỳ": thang,
            "Ngày nhận": ngay_nhan.strftime("%d/%m/%Y"),
            "Tiền gửi thêm": tien_gui_hang_thang,
            "Lãi đơn kỳ này": lai_don,
            "Lãi kép kỳ này": lai_kep,
            "Tài sản - Lãi đơn": (
                tien_goc
                + tien_gui_hang_thang * thang
                + sum(
                    x["Lãi đơn kỳ này"]
                    for x in lich
                )
                + lai_don
            ),
            "Tài sản - Lãi kép": so_du_kep
        })

    return pd.DataFrame(lich)


# ============================================================
# 8. TÍNH GIÁ TRỊ THỰC SAU LẠM PHÁT
# ============================================================

def gia_tri_thuc(gia_tri_tuong_lai, lam_phat, so_nam):

    if lam_phat <= 0:
        return gia_tri_tuong_lai

    return gia_tri_tuong_lai / (
        (1 + lam_phat / 100) ** so_nam
    )


# ============================================================
# 9. GOAL-BASED
# ============================================================

def tinh_goc_muc_tieu(
    muc_tieu,
    lai_suat_nam,
    so_thang
):
    """
    Tính số tiền cần gửi ban đầu để đạt mục tiêu
    với lãi kép hàng tháng.
    """

    r = lai_suat_nam / 100 / 12

    return muc_tieu / ((1 + r) ** so_thang)


def tinh_dca_muc_tieu(
    muc_tieu,
    lai_suat_nam,
    so_thang
):
    """
    Tính số tiền cần gửi đều mỗi tháng để đạt mục tiêu.
    """

    r = lai_suat_nam / 100 / 12

    if r == 0:
        return muc_tieu / so_thang

    return muc_tieu * r / (
        (1 + r) ** so_thang - 1
    )


# ============================================================
# 10. SESSION STATE
# ============================================================

if "so_tien_gui" not in st.session_state:
    st.session_state.so_tien_gui = 100_000_000


def set_money(value):
    st.session_state.so_tien_gui = value


# ============================================================
# 11. HEADER
# ============================================================

st.title("💰 SMART SAVINGS")
st.subheader("Công cụ tính toán & mô phỏng tiền gửi tiết kiệm")

st.caption(
    "Tính lãi đơn • Lãi kép • DCA • Mục tiêu tài chính • "
    "Lạm phát • Lịch nhận lãi • Xuất báo cáo"
)


# ============================================================
# 12. LÃI SUẤT THAM CHIẾU
# ============================================================

st.info(
    "📌 Lãi suất dưới đây là mức tham chiếu cố định để "
    "phục vụ mục đích mô phỏng. Không đại diện cho lãi suất "
    "của một ngân hàng cụ thể."
)

rate_df = pd.DataFrame(
    [
        {
            "Kỳ hạn": f"{ky_han} tháng",
            "Lãi suất": f"{lai_suat:.1f}%/năm"
        }
        for ky_han, lai_suat in LAI_SUAT_THAM_CHIEU.items()
    ]
)

st.dataframe(
    rate_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 13. INPUT CHÍNH
# ============================================================

st.header("1️⃣ Khoản tiền gửi")

col1, col2 = st.columns([2, 1])

with col1:

    so_tien_gui = st.number_input(
        "Số tiền gửi ban đầu (VNĐ)",
        min_value=0,
        max_value=100_000_000_000,
        value=st.session_state.so_tien_gui,
        step=1_000_000,
        format="%d",
        key="money_input"
    )

    st.session_state.so_tien_gui = so_tien_gui

    if so_tien_gui > 0:
        st.caption(
            "🔤 "
            + doc_so_tien(so_tien_gui)
        )

with col2:

    ky_han = st.selectbox(
        "Kỳ hạn",
        options=list(LAI_SUAT_THAM_CHIEU.keys()),
        format_func=lambda x: f"{x} tháng"
    )

    lai_suat = LAI_SUAT_THAM_CHIEU[ky_han]

    st.metric(
        "Lãi suất áp dụng",
        f"{lai_suat:.1f}%/năm"
    )


# ============================================================
# NÚT CHỌN NHANH
# ============================================================

st.write("⚡ **Chọn nhanh số tiền:**")

quick_cols = st.columns(5)

quick_values = [
    (10_000_000, "10M"),
    (50_000_000, "50M"),
    (100_000_000, "100M"),
    (500_000_000, "500M"),
    (1_000_000_000, "1B")
]

for col, (value, label) in zip(
    quick_cols,
    quick_values
):
    with col:
        if st.button(
            label,
            use_container_width=True
        ):
            st.session_state.so_tien_gui = value
            st.rerun()


# ============================================================
# DCA
# ============================================================

st.header("2️⃣ Gửi tích lũy định kỳ — DCA")

dca = st.number_input(
    "Số tiền gửi thêm mỗi tháng (VNĐ)",
    min_value=0,
    max_value=10_000_000_000,
    value=0,
    step=500_000,
    format="%d"
)

if dca > 0:
    st.caption(
        "Mỗi tháng bạn sẽ bổ sung "
        f"{format_money(dca)} vào khoản tiết kiệm."
    )


# ============================================================
# LẠM PHÁT
# ============================================================

st.header("3️⃣ Lạm phát & sức mua")

lam_phat = st.number_input(
    "Lạm phát dự kiến (%/năm)",
    min_value=0.0,
    max_value=30.0,
    value=3.0,
    step=0.1
)

ngay_bat_dau = st.date_input(
    "Ngày bắt đầu gửi",
    value=date.today()
)


# ============================================================
# TAB
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Tổng quan",
    "⚖️ Lãi đơn vs Lãi kép",
    "🎯 Mục tiêu",
    "📅 Lịch nhận lãi",
    "📥 Xuất báo cáo",
    "☕ Quy đổi thực tế"
])


# ============================================================
# TAB 1 — TỔNG QUAN
# ============================================================

with tab1:

    st.header("📊 Tổng quan khoản tiết kiệm")

    tong_goc_don, tong_lai_don = tinh_lai_don(
        so_tien_gui,
        lai_suat,
        ky_han,
        dca
    )

    tong_goc_kep, tong_lai_kep, tong_tai_san_kep, _ = tinh_lai_kep(
        so_tien_gui,
        lai_suat,
        ky_han,
        dca
    )

    tong_tai_san_don = (
        tong_goc_don + tong_lai_don
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💵 Tổng gốc",
            format_money(tong_goc_kep)
        )

    with col2:
        st.metric(
            "📈 Lãi đơn",
            format_money(tong_lai_don)
        )

    with col3:
        st.metric(
            "🚀 Lãi kép",
            format_money(tong_lai_kep)
        )

    with col4:
        st.metric(
            "💰 Tài sản cuối kỳ",
            format_money(tong_tai_san_kep)
        )

    st.divider()

    # Lãi thực sau lạm phát
    so_nam = ky_han / 12

    gia_tri_thuc_te = gia_tri_thuc(
        tong_tai_san_kep,
        lam_phat,
        so_nam
    )

    st.subheader("🛒 Sức mua sau lạm phát")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Giá trị danh nghĩa",
            format_money(tong_tai_san_kep)
        )

    with c2:
        st.metric(
            "Giá trị thực ước tính",
            format_money(gia_tri_thuc_te)
        )

    st.caption(
        "Giá trị thực là ước tính sức mua quy đổi về hiện tại "
        "theo mức lạm phát bạn nhập."
    )


# ============================================================
# TAB 2 — LÃI ĐƠN VS LÃI KÉP
# ============================================================

with tab2:

    st.header("⚖️ So sánh Lãi đơn và Lãi kép")

    st.write(
        "Lãi kép giả định tiền lãi được tái đầu tư hàng tháng."
    )

    lich_df = tao_lich(
        so_tien_gui,
        lai_suat,
        ky_han,
        dca,
        ngay_bat_dau
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Lãi đơn")

        lai_don_cuoi = lich_df[
            "Tài sản - Lãi đơn"
        ].iloc[-1]

        st.metric(
            "Tài sản cuối kỳ",
            format_money(lai_don_cuoi)
        )

    with col2:

        st.subheader("Lãi kép")

        lai_kep_cuoi = lich_df[
            "Tài sản - Lãi kép"
        ].iloc[-1]

        st.metric(
            "Tài sản cuối kỳ",
            format_money(lai_kep_cuoi)
        )

    chenhlech = lai_kep_cuoi - lai_don_cuoi

    st.info(
        f"📈 Chênh lệch mô phỏng giữa hai phương pháp: "
        f"**{format_money(chenhlech)}**"
    )

    # =========================
    # BIỂU ĐỒ
    # =========================

    st.subheader("📈 Biểu đồ tăng trưởng tài sản")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=lich_df["Kỳ"],
            y=lich_df["Tài sản - Lãi đơn"],
            mode="lines+markers",
            name="Lãi đơn"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=lich_df["Kỳ"],
            y=lich_df["Tài sản - Lãi kép"],
            mode="lines+markers",
            name="Lãi kép"
        )
    )

    fig.update_layout(
        xaxis_title="Kỳ",
        yaxis_title="Tài sản (VNĐ)",
        hovermode="x unified",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================
    # BẢNG SO SÁNH
    # =========================

    comparison = pd.DataFrame({
        "Chỉ tiêu": [
            "Tổng tiền gốc",
            "Tổng tiền lãi",
            "Tổng tài sản"
        ],
        "Lãi đơn": [
            tong_goc_don,
            tong_lai_don,
            tong_tai_san_don
        ],
        "Lãi kép": [
            tong_goc_kep,
            tong_lai_kep,
            tong_tai_san_kep
        ]
    })

    for col in ["Lãi đơn", "Lãi kép"]:
        comparison[col] = comparison[col].map(
            format_money
        )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 3 — GOAL BASED
# ============================================================

with tab3:

    st.header("🎯 Tính ngược mục tiêu tài chính")

    st.write(
        "Nhập số tiền bạn muốn có trong tương lai. "
        "Ứng dụng sẽ ước tính số tiền cần chuẩn bị."
    )

    muc_tieu = st.number_input(
        "🎯 Số tiền mục tiêu (VNĐ)",
        min_value=1_000_000,
        value=500_000_000,
        step=10_000_000,
        format="%d"
    )

    thoi_gian_muc_tieu = st.number_input(
        "⏳ Thời gian đầu tư (tháng)",
        min_value=1,
        max_value=600,
        value=60,
        step=1
    )

    st.caption(
        "Mục tiêu: "
        + doc_so_tien(muc_tieu)
    )

    goc_can_gui = tinh_goc_muc_tieu(
        muc_tieu,
        lai_suat,
        thoi_gian_muc_tieu
    )

    dca_can_gui = tinh_dca_muc_tieu(
        muc_tieu,
        lai_suat,
        thoi_gian_muc_tieu
    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("💰 Gửi một lần")

        st.metric(
            "Gốc cần gửi ban đầu",
            format_money(goc_can_gui)
        )

        st.caption(
            "Giả định lãi được tái đầu tư hàng tháng."
        )

    with c2:

        st.subheader("📅 Gửi đều hàng tháng")

        st.metric(
            "Khoản cần gửi mỗi tháng",
            format_money(dca_can_gui)
        )

        st.caption(
            "Giả định gửi vào đầu mỗi tháng."
        )

    st.divider()

    st.subheader("📌 Tóm tắt")

    st.write(
        f"Để hướng tới **{format_money(muc_tieu)}** "
        f"sau **{thoi_gian_muc_tieu} tháng**, "
        f"với lãi suất tham chiếu **{lai_suat:.1f}%/năm**:"
    )

    st.write(
        f"• Gửi một lần: **{format_money(goc_can_gui)}**"
    )

    st.write(
        f"• Hoặc gửi đều: **{format_money(dca_can_gui)}/tháng**"
    )


# ============================================================
# TAB 4 — LỊCH NHẬN LÃI
# ============================================================

with tab4:

    st.header("📅 Lịch thu hoạch lãi")

    st.write(
        "Bảng dưới đây mô phỏng từng tháng trong thời gian gửi."
    )

    lich_df = tao_lich(
        so_tien_gui,
        lai_suat,
        ky_han,
        dca,
        ngay_bat_dau
    )

    display_df = lich_df.copy()

    money_columns = [
        "Tiền gửi thêm",
        "Lãi đơn kỳ này",
        "Lãi kép kỳ này",
        "Tài sản - Lãi đơn",
        "Tài sản - Lãi kép"
    ]

    for col in money_columns:
        display_df[col] = display_df[col].map(
            format_money
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.divider()

    st.subheader("📌 Kỳ cuối")

    last = lich_df.iloc[-1]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Lãi đơn",
            format_money(
                last["Lãi đơn kỳ này"]
            )
        )

    with c2:
        st.metric(
            "Lãi kép",
            format_money(
                last["Lãi kép kỳ này"]
            )
        )

    with c3:
        st.metric(
            "Tài sản cuối kỳ",
            format_money(
                last["Tài sản - Lãi kép"]
            )
        )


# ============================================================
# TAB 5 — XUẤT BÁO CÁO
# ============================================================

with tab5:

    st.header("📥 Xuất báo cáo")

    st.write(
        "Bạn có thể tải toàn bộ dữ liệu mô phỏng "
        "về máy dưới dạng CSV hoặc Excel."
    )

    lich_df = tao_lich(
        so_tien_gui,
        lai_suat,
        ky_han,
        dca,
        ngay_bat_dau
    )

    # =========================
    # CSV
    # =========================

    csv_data = lich_df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="📄 Tải lịch nhận lãi CSV",
        data=csv_data,
        file_name="lich_tiet_kiem.csv",
        mime="text/csv",
        use_container_width=True
    )

    # =========================
    # EXCEL
    # =========================

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        # Sheet tổng quan
        overview = pd.DataFrame({
            "Thông tin": [
                "Số tiền gửi ban đầu",
                "Kỳ hạn",
                "Lãi suất",
                "DCA mỗi tháng",
                "Lạm phát",
                "Ngày bắt đầu"
            ],
            "Giá trị": [
                format_money(so_tien_gui),
                f"{ky_han} tháng",
                f"{lai_suat:.1f}%/năm",
                format_money(dca),
                f"{lam_phat:.1f}%/năm",
                ngay_bat_dau.strftime("%d/%m/%Y")
            ]
        })

        overview.to_excel(
            writer,
            sheet_name="Tong quan",
            index=False
        )

        # Sheet lịch
        lich_df.to_excel(
            writer,
            sheet_name="Lich nhan lai",
            index=False
        )

        # Sheet so sánh
        comparison_excel = pd.DataFrame({
            "Chỉ tiêu": [
                "Tổng tiền gốc",
                "Tổng lãi đơn",
                "Tổng lãi kép",
                "Tài sản cuối kỳ - lãi đơn",
                "Tài sản cuối kỳ - lãi kép"
            ],
            "Giá trị": [
                tong_goc_kep,
                tong_lai_don,
                tong_lai_kep,
                tong_tai_san_don,
                tong_tai_san_kep
            ]
        })

        comparison_excel.to_excel(
            writer,
            sheet_name="So sanh",
            index=False
        )

    excel_data = excel_buffer.getvalue()

    st.download_button(
        label="📊 Tải báo cáo Excel",
        data=excel_data,
        file_name="bao_cao_tiet_kiem.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )


# ============================================================
# TAB 6 — QUY ĐỔI THỰC TẾ
# ============================================================

with tab6:

    st.header("☕ Tiền lãi của bạn tương đương với gì?")

    st.write(
        "Một cách vui để hình dung giá trị của khoản tiền lãi."
    )

    tien_lai = tong_lai_kep

    # Giá tham chiếu
    gia_ca_phe = 45_000
    gia_ve_phim = 120_000
    gia_bua_an = 80_000
    gia_du_lich = 5_000_000

    so_cafe = tien_lai / gia_ca_phe
    so_ve_phim = tien_lai / gia_ve_phim
    so_bua_an = tien_lai / gia_bua_an
    so_chuyen_du_lich = tien_lai / gia_du_lich

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("☕ Cà phê")

        st.metric(
            "Số ly tương đương",
            f"{so_cafe:,.0f} ly"
        )

        st.caption(
            "Giả định 45.000 VNĐ/ly."
        )

    with c2:

        st.subheader("🎬 Vé xem phim")

        st.metric(
            "Số vé tương đương",
            f"{so_ve_phim:,.0f} vé"
        )

        st.caption(
            "Giả định 120.000 VNĐ/vé."
        )

    c3, c4 = st.columns(2)

    with c3:

        st.subheader("🍜 Bữa ăn")

        st.metric(
            "Số bữa tương đương",
            f"{so_bua_an:,.0f} bữa"
        )

        st.caption(
            "Giả định 80.000 VNĐ/bữa."
        )

    with c4:

        st.subheader("✈️ Du lịch")

        st.metric(
            "Chuyến tương đương",
            f"{so_chuyen_du_lich:,.1f} chuyến"
        )

        st.caption(
            "Giả định 5 triệu VNĐ/chuyến."
        )

    st.divider()

    st.info(
        f"💡 Với khoản tiền gửi hiện tại, "
        f"tiền lãi kép mô phỏng của bạn là "
        f"**{format_money(tien_lai)}**."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "💰 Smart Savings Calculator | "
    "Công cụ mô phỏng tài chính cá nhân"
)

st.caption(
    "Lưu ý: Lãi suất là số liệu tham chiếu do ứng dụng "
    "thiết lập, không phải cam kết của ngân hàng. "
    "Kết quả thực tế có thể khác do cách tính lãi, "
    "ngày gửi, ngày đáo hạn, thuế và chính sách từng ngân hàng."
)

