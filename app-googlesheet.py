import streamlit as st
import graphviz
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐานของหน้าเว็บ ---
st.set_page_config(page_title="แนะนำสาขาวิชา", page_icon="🎓", layout="wide")

# --- 2. เชื่อมต่อกับ Google Sheets (วิธีใหม่ด้วย gspread) ---
try:
    # ดึงข้อมูล credentials จาก st.secrets
    creds = st.secrets["connections"]["gsheets"]
    # สร้างการเชื่อมต่อ
    gc = gspread.service_account_from_dict(creds)
    # เปิด Google Sheet ของเรา (ใช้ชื่อไฟล์ที่เราตั้งไว้)
    sh = gc.open("MajorAppData")
    # เลือก worksheet (แท็บ) ที่ต้องการ (ปกติคือ Sheet1)
    worksheet = sh.worksheet("Sheet1")
except Exception as e:
    st.error("เกิดข้อผิดพลาดในการเชื่อมต่อกับ Google Sheets:")
    st.error(e)
    st.stop()

# --- 3. สร้างเมนูหลักด้านซ้าย ---
st.sidebar.title("เมนูหลัก")
menu_choice = st.sidebar.selectbox(
    "เลือกเมนูที่ต้องการ:",
    ("Dashboard สรุปผล", "แบบทดสอบเลือกการตัดสินใจ", "ให้ความรู้แต่ละสาขา")
)

# --- 4. แสดงหน้าตามเมนูที่เลือก ---

# ==============================================================================
#  หน้า DASHBOARD
# ==============================================================================
if menu_choice == "Dashboard สรุปผล":
    st.title("📊 Dashboard สรุปผล (จากข้อมูลจริง)")
    st.write("ภาพรวมข้อมูลจากผู้ใช้งานทั้งหมดที่เข้ามาทำแบบทดสอบ")

    # --- อ่านข้อมูลจริงจาก Google Sheets ---
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("ยังไม่มีข้อมูลในระบบ กรุณาไปที่หน้า 'แบบทดสอบ' เพื่อเริ่มบันทึกข้อมูล")
    else:
        # --- แสดงผล Dashboard ---
        st.header("สรุปสาขาที่ได้รับการแนะนำมากที่สุด")
        major_counts = df['Recommended_Major'].value_counts().reset_index()
        major_counts.columns = ['สาขาวิชา', 'จำนวนผู้ใช้']
        
        fig_bar = px.bar(major_counts, x='สาขาวิชา', y='จำนวนผู้ใช้', title="จำนวนผู้ใช้ในแต่ละสาขา", color='สาขาวิชา', text_auto=True)
        st.plotly_chart(fig_bar, use_container_width=True)

        st.header("การกระจายตัวของผลการเรียน")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("เกรดเฉลี่ยรวม")
            fig_pie_total = px.pie(df, names='Total_Grade', title='สัดส่วนเกรดเฉลี่ยรวม')
            st.plotly_chart(fig_pie_total, use_container_width=True)
        with col2:
            st.subheader("เกรดวิชาเอก")
            fig_pie_major = px.pie(df, names='Major_Grade', title='สัดส่วนเกรดวิชาเอก')
            st.plotly_chart(fig_pie_major, use_container_width=True)
        with col3:
            st.subheader("เกรดวิชาธุรกิจ")
            fig_pie_business = px.pie(df, names='Business_Grade', title='สัดส่วนเกรดวิชาธุรกิจ')
            st.plotly_chart(fig_pie_business, use_container_width=True)

        st.header("ตารางข้อมูลล่าสุด")
        st.dataframe(df.sort_values(by="Timestamp", ascending=False))

# ==============================================================================
#  หน้า แบบทดสอบ
# ==============================================================================
elif menu_choice == "แบบทดสอบเลือกการตัดสินใจ":
    st.title("📝 แบบทดสอบเลือกการตัดสินใจ")
    st.write("เลือกผลการเรียนของคุณในแต่ละด้าน แล้วกดปุ่มเพื่อดูเส้นทางการตัดสินใจและผลลัพธ์")
    
    with st.sidebar.form(key='recommendation_form'):
        st.header("กรอกข้อมูลของคุณที่นี่")
        total_grade = st.radio("1. ผลการเรียนเฉลี่ยรวม", ["ดี", "ไม่ดี"], key="total")
        major_grade = st.radio("2. ผลการเรียนในวิชาเอก", ["ดี", "ไม่ดี"], key="major")
        business_grade = st.radio("3. ผลการเรียนในวิชาธุรกิจ", ["ดี", "ไม่ดี"], key="business")
        submit_button = st.form_submit_button(label='แสดงผลการแนะนำ')

    if submit_button:
        # --- ส่วนตรรกะการตัดสินใจ (Logic) ---
        result_text = ""
        if total_grade == "ไม่ดี":
            if major_grade == "ไม่ดี":
                if business_grade == "ไม่ดี": result_text = "การจัดการ"
                else: result_text = "คอมพิวเตอร์"
            else: result_text = "คอมพิวเตอร์"
        else:
            if major_grade == "ไม่ดี": result_text = "การโรงแรม"
            else:
                if business_grade == "ไม่ดี": result_text = "การโรงแรม"
                else: result_text = "การตลาด"
        
        # --- บันทึกข้อมูลลง Google Sheets (วิธีใหม่) ---
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # สร้างแถวข้อมูลใหม่ตามลำดับคอลัมน์ใน Sheet
            new_row = [timestamp, total_grade, major_grade, business_grade, result_text]
            # เพิ่มแถวใหม่ต่อท้ายข้อมูลเดิม
            worksheet.append_row(new_row, value_input_option='USER_ENTERED')
            st.sidebar.success("บันทึกข้อมูลของคุณเรียบร้อยแล้ว!")
        except Exception as e:
            st.sidebar.error(f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")

        st.header("เส้นทางการตัดสินใจของคุณ:")
        st.success(f"สาขาที่แนะนำสำหรับคุณคือ: **{result_text}**")

    else:
        st.info("กรุณาเลือกข้อมูลทางด้านซ้ายและกดปุ่ม 'แสดงผลการแนะนำ' เพื่อเริ่มต้น")

# ==============================================================================
#  หน้า ให้ความรู้
# ==============================================================================
elif menu_choice == "ให้ความรู้แต่ละสาขา":
    st.title("📚 ข้อมูลความรู้แต่ละสาขา")
    st.write("ทำความรู้จักกับสาขาวิชาต่างๆ เพื่อประกอบการตัดสินใจของคุณ")

    st.header("💻 สาขาคอมพิวเตอร์ (Computer)")
    st.write("...") # (เนื้อหาเดิม)
    st.header("🏨 สาขาการโรงแรม (Hotel)")
    st.write("...") # (เนื้อหาเดิม)
    st.header("📈 สาขาการตลาด (Marketing)")
    st.write("...") # (เนื้อหาเดิม)
    st.header("👔 สาขาการจัดการ (Management)")
    st.write("...") # (เนื้อหาเดิม)