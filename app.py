import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="ប្រព័ន្ធគ្រប់គ្រងស្តុកទំនិញ E.D.CON", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        .stButton>button {
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        h1, h2, h3 { color: #007acc; font-family: 'Khmer OS Battambang', sans-serif; }
    </style>
""", unsafe_allow_html=True)

logo_path = "EDCon-removebg.jpg"
if os.path.exists(logo_path):
    img = Image.open(logo_path)
    st.sidebar.image(img, width=160)
else:
    st.sidebar.warning("⚠️ រកមិនឃើញ File រូបភាព: EDCon-removebg.jpg")

st.sidebar.markdown("<h2 style='text-align: center;'>🗂️ MENU CONTROL</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

if 'users' not in st.session_state:
    st.session_state.users = {
        "admin1": {"password": "123", "role": "Admin", "permissions": ["មើល", "អាន", "កែ", "Import", "Export"]},
        "admin2": {"password": "456", "role": "Admin", "permissions": ["មើល", "អាន", "កែ", "Import", "Export"]}
    }

if 'stock_data' not in st.session_state:
    st.session_state.stock_data = pd.DataFrame(columns=["កូដទំនិញ", "ឈ្មោះទំនិញ", "ចំនួនចូល", "ចំនួនចេញ", "ស្តុកនៅសល់"])


if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

if st.session_state.logged_in_user is None:
    st.sidebar.subheader("🔐 ចូលប្រើប្រាស់ប្រព័ន្ធ")
    username = st.sidebar.text_input("ឈ្មោះអ្នកប្រើប្រាស់ (Username)")
    password = st.sidebar.text_input("លេខកូដសម្ងាត់ (Password)", type="password")
    
    if st.sidebar.button("👉 ចូលប្រព័ន្ធ (Login)", use_container_width=True, type="primary"):
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.logged_in_user = username
            st.rerun()
        else:
            st.sidebar.error("❌ ឈ្មោះ ឬលេខកូដសម្ងាត់មិនត្រឹមត្រូវទេ!")
            
    st.title("🏢 ប្រព័ន្ធគ្រប់គ្រងស្តុកទំនិញ E.D.CON")
    st.info("💡 សូមធ្វើការ Login នៅរបារខាងឆ្វេង ដើម្បីចូលប្រើប្រាស់ប្រព័ន្ធទៅតាមតួនាទីរបស់អ្នក។")

else:
    current_user = st.session_state.logged_in_user
    user_info = st.session_state.users[current_user]
    
    st.sidebar.markdown(f"<div style='background-color:#e1f5fe; padding:10px; border-radius:8px; border-left:5px solid #0288d1; color:#01579b;'>👤 <b>គណនី៖</b> {current_user}<br>🔰 <b>តួនាទី៖</b> {user_info['role']}</div>", unsafe_allow_html=True)
    st.sidebar.write("")
    if st.sidebar.button("🚪 ចាកចេញ (Logout)", use_container_width=True):
        st.session_state.logged_in_user = None
        st.rerun()
        
    perms = user_info["permissions"]

    st.markdown("<h1 style='text-align: center; color: #0288d1;'>🏢 ប្រព័ន្ធគ្រប់គ្រងស្តុកទំនិញក្រុមហ៊ុន E.D.CON</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>គ្រប់គ្រងការ នាំចូល-នាំចេញ ទិន្នន័យស្តុកទំនិញទូទៅប្រចាំក្រុមហ៊ុន</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    df_stock = st.session_state.stock_data
    total_items = len(df_stock)
    total_in = df_stock["ចំនួនចូល"].sum() if total_items > 0 else 0
    total_out = df_stock["ចំនួនចេញ"].sum() if total_items > 0 else 0
    total_remain = df_stock["ស្តុកនៅសល់"].sum() if total_items > 0 else 0
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("📦 មុខទំនិញសរុប", f"{total_items} មុខ")
    m_col2.metric("📥 គ្រឿងចូលសរុប", f"{total_in} គ្រឿង")
    m_col3.metric("📤 គ្រឿងចេញសរុប", f"{total_out} គ្រឿង")
    m_col4.metric("⚖️ ស្តុកនៅសល់សរុប", f"{total_remain} គ្រឿង")
    st.markdown("---")

    if user_info['role'] == "Admin":
        with st.expander("👥 ផ្ទាំងគ្រប់គ្រងសមាជិក និងបុគ្គលិក (សម្រាប់តែ Admin)", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("➕ បង្កើតសមាជិកថ្មី")
                new_user = st.text_input("ឈ្មោះសមាជិកថ្មី")
                new_pass = st.text_input("លេខកូដសមាជិកថ្មី", type="password")
                
                st.write("📋 កំណត់សិទ្ធិសម្រាប់សមាជិកនេះ៖")
                p_edit = st.checkbox("កែប្រែទិន្នន័យស្តុក (Edit)", value=True)
                p_import = st.checkbox("នាំចូលឯកសារ Excel (Import)", value=True)
                
                if st.button("💾 រក្សាទុកសមាជិក", type="primary"):
                    if new_user and new_pass:
                        if new_user in st.session_state.users:
                            st.error("❌ ឈ្មោះសមាជិកនេះមានរួចហើយ!")
                        else:
                            user_perms = ["មើល", "អាន", "Export"]
                            if p_edit: user_perms.append("កែ")
                            if p_import: user_perms.append("Import")
                            
                            st.session_state.users[new_user] = {"password": new_pass, "role": "សមាជិក", "permissions": user_perms}
                            st.success(f"🎉 បានបង្កើតសមាជិក [{new_user}] រួចរាល់!")
                            st.rerun()
                    else:
                        st.error("❌ សូមបំពេញឈ្មោះ និងលេខកូដសម្ងាត់ឱ្យបានគ្រប់គ្រាន់!")
                        
            with col2:
                st.subheader("❌ លុបសមាជិកដែលឈប់ប្រើ")
                delete_list = [u for u in st.session_state.users.keys() if u not in ["admin1", "admin2"]]
                user_to_delete = st.selectbox("ជ្រើសរើសឈ្មោះដើម្បីលុប", ["--- ជ្រើសរើស ---"] + delete_list)
                
                if st.button("🗑️ លុបទិន្នន័យសមាជិកនេះ", type="secondary"):
                    if user_to_delete != "--- ជ្រើសរើស ---":
                        del st.session_state.users[user_to_delete]
                        st.warning(f"🗑️ បានលុបសមាជិក [{user_to_delete}] ចេញពីប្រព័ន្ធ!")
                        st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    col_input, col_file = st.columns([2, 1])
    
    with col_input:
        if "កែ" in perms:
            st.subheader("✏️ បញ្ចូល ឬកែប្រែទិន្នន័យស្តុក")
            with st.form("stock_form", clear_on_submit=True):
                col_a, col_b = st.columns(2)
                with col_a: p_code = st.text_input("កូដទំនិញ (Product Code)")
                with col_b: p_name = st.text_input("ឈ្មោះទំនិញ (Product Name)")
                
                col_c, col_d = st.columns(2)
                with col_c: p_in = st.number_input("ចំនួនចូល", min_value=0, step=1)
                with col_d: p_out = st.number_input("ចំនួនចេញ", min_value=0, step=1)
                
                submit_btn = st.form_submit_button("💾 រក្សាទុកទិន្នន័យស្តុក", type="primary")
                if submit_btn:
                    if p_code and p_name:
                        df = st.session_state.stock_data
                        remain = p_in - p_out
                        
                        if p_code in df["កូដទំនិញ"].values:
                            df.loc[df["កូដទំនិញ"] == p_code, ["ឈ្មោះទំនិញ", "ចំនួនចូល", "ចំនួនចេញ", "ស្តុកនៅសល់"]] = [p_name, p_in, p_out, remain]
                        else:
                            new_row = pd.DataFrame([[p_code, p_name, p_in, p_out, remain]], columns=df.columns)
                            st.session_state.stock_data = pd.concat([df, new_row], ignore_index=True)
                        st.success("✅ បានរក្សាទុកទិន្នន័យទំនិញរួចរាល់!")
                        st.rerun()
                    else:
                        st.error("❌ សូមបំពេញកូដទំនិញ និងឈ្មោះទំនិញ!")

    with col_file:
        if "Import" in perms:
            st.subheader("📥 នាំចូល Excel (Import)")
            uploaded_file = st.file_uploader("ជ្រើសរើស File Excel (.xlsx)", type=["xlsx"])
            if uploaded_file is not None:
                try:
                    df_excel = pd.read_excel(uploaded_file)
                    required_cols = ["កូដទំនិញ", "ឈ្មោះទំនិញ", "ចំនួនចូល", "ចំនួនចេញ", "ស្តុកនៅសល់"]
                    if all(col in df_excel.columns for col in required_cols):
                        st.session_state.stock_data = df_excel
                        st.success("✅ បាននាំចូលទិន្នន័យជោគជ័យ!")
                        st.rerun()
                    else:
                        st.error("❌ ទម្រង់ File ត្រូវតែមានជួរឈរ៖ កូដទំនិញ, ឈ្មោះទំនិញ, ចំនួនចូល, ចំនួនចេញ, ស្តុកនៅសល់")
                except Exception as e:
                    st.error(f"❌ មានបញ្ហា៖ {e}")

    st.markdown("---")

    if "មើល" in perms or "អាន" in perms:
        st.subheader("📊 តារាងបង្ហាញស្តុកទំនិញបច្ចុប្បន្ន")
        if not st.session_state.stock_data.empty:
            st.dataframe(st.session_state.stock_data.style.background_gradient(cmap="Blues", subset=["ស្តុកនៅសល់"]), use_container_width=True)
        else:
            st.info("ℹ️ មិនទាន់មានទិន្នន័យក្នុងស្តុកនៅឡើយទេ។")
        
    if "Export" in perms and not st.session_state.stock_data.empty:
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.stock_data.to_excel(writer, index=False, sheet_name='Stock_Report')
        excel_data = output.getvalue()
        
        st.write("")
        st.download_button(
            label="📤 ទាញយករបាយការណ៍ជាឯកសារ Excel (Export)",
            data=excel_data,
            file_name='របាយការណ៍ស្តុកទំនិញ_EDCON.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            use_container_width=True
        )