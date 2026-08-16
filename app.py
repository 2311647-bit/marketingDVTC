import streamlit as st
import pandas as pd
st.image("IMG_5515.jpeg")
# 1. Cấu hình trang
st.set_page_config(
    page_title="Quản lý Thông tin Khách hàng",
    page_icon="👤",
    layout="wide"
)

# 2. Khởi tạo session state để lưu trữ dữ liệu tạm thời
if "customer_data" not in st.session_state:
    st.session_state.customer_data = pd.DataFrame(
        columns=["Tên khách hàng", "Số điện thoại", "Khu vực", "Ghi chú"]
    )

st.title("📋 Quản lý Thông tin Khách hàng")

# 3. Form nhập thông tin
with st.form(key="customer_form", clear_on_submit=True):
    st.subheader("Thêm khách hàng mới")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Tên khách hàng *", placeholder="Nhập họ và tên")
        phone = st.text_input("Số điện thoại *", placeholder="Nhập số điện thoại")
        
    with col2:
        region = st.selectbox(
            "Khu vực",
            ["Miền Bắc", "Miền Trung", "Miền Nam", "Nước ngoài", "Khác"]
        )
        note = st.text_area("Ghi chú", placeholder="Nhập ghi chú thêm (nếu có)")
        
    submit_button = st.form_submit_button(label="➕ Thêm khách hàng")

# 4. Xử lý khi bấm nút Thêm
if submit_button:
    if not name.strip() or not phone.strip():
        st.error("Vui lòng điền đầy đủ Tên khách hàng và Số điện thoại!")
    else:
        # Tạo bản ghi mới
        new_entry = {
            "Tên khách hàng": name.strip(),
            "Số điện thoại": phone.strip(),
            "Khu vực": region,
            "Ghi chú": note.strip()
        }
        
        # Thêm vào DataFrame trong session_state
        st.session_state.customer_data = pd.concat(
            [st.session_state.customer_data, pd.DataFrame([new_entry])],
            ignore_index=True
        )
        st.success(f"Đã thêm thành công khách hàng: {name}")

st.divider()

# 5. Hiển thị danh sách khách hàng & Xuất dữ liệu
st.subheader("📊 Danh sách khách hàng đã nhập")

if not st.session_state.customer_data.empty:
    st.dataframe(
        st.session_state.customer_data,
        use_container_width=True,
        hide_index=True
    )
    
    col_download1, col_download2 = st.columns([1, 4])
    
    # Tải file CSV
    csv_data = st.session_state.customer_data.to_csv(index=False).encode("utf-8-sig")
    with col_download1:
        st.download_button(
            label="📥 Tải về file CSV",
            data=csv_data,
            file_name="danh_sach_khach_hang.csv",
            mime="text/csv"
        )
else:
    st.info("Chưa có dữ liệu khách hàng nào được nhập.")
