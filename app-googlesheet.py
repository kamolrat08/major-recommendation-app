import streamlit as st
import graphviz
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐานของหน้าเว็บ ---
st.set_page_config(page_title="แนะนำสาขาวิชา", page_icon="🎓", layout="wide")

# --- 2. เชื่อมต่อกับ Google Sheets ---
# Streamlit จะดึงข้อมูลการเชื่อมต่อจาก "Secrets" ที่เราตั้งค่าไว้โดยอัตโนมัติ
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("ไม่สามารถเชื่อมต่อกับฐานข้อมูล Google Sheets ได้")
    st.error("กรุณาตรวจสอบการตั้งค่า Secrets ใน Streamlit Community Cloud")
    st.stop() # หยุดการทำงานของแอปถ้าเชื่อมต่อไม่ได้

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
    # ttl=5 หมายความว่าให้ดึงข้อมูลใหม่ทุก 5 วินาที (เพื่อให้ข้อมูลสดใหม่เสมอ)
    df = conn.read(worksheet="MajorAppData", usecols=list(range(5)), ttl=5)
    df = df.dropna(how="all") # ลบแถวที่ว่างเปล่า (อาจเกิดขึ้นได้)

    if df.empty:
        st.warning("ยังไม่มีข้อมูลในระบบ กรุณาไปที่หน้า 'แบบทดสอบ' เพื่อเริ่มบันทึกข้อมูล")
    else:
        # --- แสดงผล Dashboard ---
        st.header("สรุปสาขาที่ได้รับการแนะนำมากที่สุด")
        major_counts = df['Recommended_Major'].value_counts().reset_index()
        major_counts.columns = ['สาขาวิชา', 'จำนวนผู้ใช้']
        
        fig_bar = px.bar(major_counts, 
                         x='สาขาวิชา', 
                         y='จำนวนผู้ใช้', 
                         title="จำนวนผู้ใช้ที่ได้รับการแนะนำในแต่ละสาขา",
                         color='สาขาวิชา',
                         text_auto=True)
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
    
    # ใช้ st.form เพื่อให้ผู้ใช้กรอกข้อมูลให้ครบก่อนแล้วค่อยกดส่งทีเดียว
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
        
        # --- บันทึกข้อมูลลง Google Sheets ---
        try:
            # อ่านข้อมูลเก่ามาก่อน
            existing_data = conn.read(worksheet="MajorAppData", usecols=list(range(5)), ttl=5)
            existing_data = existing_data.dropna(how="all")

            # เตรียมข้อมูลแถวใหม่
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Total_Grade": total_grade,
                "Major_Grade": major_grade,
                "Business_Grade": business_grade,
                "Recommended_Major": result_text
            }])
            
            # รวมข้อมูลเก่ากับใหม่
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            
            # เขียนข้อมูลที่รวมแล้วกลับไปที่ Sheet
            conn.update(worksheet="MajorAppData", data=updated_df)
            
            st.sidebar.success("บันทึกข้อมูลของคุณเรียบร้อยแล้ว!")
        except Exception as e:
            st.sidebar.error(f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")

        # --- ส่วนแสดงผล Graphviz (เหมือนเดิม) ---
        st.header("เส้นทางการตัดสินใจของคุณ:")
        st.success(f"สาขาที่แนะนำสำหรับคุณคือ: **{result_text}**")
        # (คุณสามารถนำโค้ดสร้าง Graphviz เดิมมาใส่ตรงนี้ได้ถ้าต้องการ)

    else:
        st.info("กรุณาเลือกข้อมูลทางด้านซ้ายและกดปุ่ม 'แสดงผลการแนะนำ' เพื่อเริ่มต้น")

# ==============================================================================
#  หน้า ให้ความรู้
# ==============================================================================
elif menu_choice == "ให้ความรู้แต่ละสาขา":
    st.title("📚 ข้อมูลความรู้แต่ละสาขา")
    st.write("ทำความรู้จักกับสาขาวิชาต่างๆ เพื่อประกอบการตัดสินใจของคุณ")

    st.header("💻 สาขาคอมพิวเตอร์ (Computer)")
    st.write(
        """
        สาขาที่เกี่ยวข้องกับการสร้างสรรค์เทคโนโลยี ซอฟต์แวร์ และนวัตกรรมดิจิทัล
        - **เรียนเกี่ยวกับ:** การเขียนโปรแกรม, โครงสร้างข้อมูล, อัลกอริทึม, ระบบเครือข่าย, ปัญญาประดิษฐ์ (AI)
        - **อาชีพในอนาคต:** นักพัฒนาซอฟต์แวร์ (Software Developer), วิศวกรข้อมูล (Data Engineer), ผู้เชี่ยวชาญด้านความปลอดภัยไซเบอร์ (Cybersecurity Specialist)
        """
    )

    st.header("🏨 สาขาการโรงแรม (Hotel)")
    st.write(
        """
        ศาสตร์แห่งการบริการและการบริหารจัดการธุรกิจที่พักและบริการที่เกี่ยวข้อง เพื่อสร้างความพึงพอใจสูงสุดให้แก่ลูกค้า
        - **เรียนเกี่ยวกับ:** การจัดการส่วนหน้า, การบริหารงานแม่บ้าน, การจัดการอาหารและเครื่องดื่ม, การตลาดสำหรับธุรกิจบริการ
        - **อาชีพในอนาคต:** ผู้จัดการโรงแรม, ผู้จัดการฝ่ายต้อนรับ, ผู้จัดงานอีเวนต์และประชุม
        """
    )
    
    st.header("📈 สาขาการตลาด (Marketing)")
    st.write(
        """
        สาขาที่เรียนรู้เกี่ยวกับการวางแผนและกลยุทธ์เพื่อนำเสนอสินค้าหรือบริการให้เข้าถึงและตอบสนองความต้องการของลูกค้า
        - **เรียนเกี่ยวกับ:** การวิเคราะห์พฤติกรรมผู้บริโภค, การตลาดดิจิทัล, การสร้างแบรนด์, การสื่อสารการตลาด
        - **อาชีพในอนาคต:** นักการตลาดดิจิทัล (Digital Marketer), ผู้จัดการแบรนด์ (Brand Manager), ผู้เชี่ยวชาญด้าน SEO/SEM
        """
    )

    st.header("👔 สาขาการจัดการ (Management)")
    st.write(
        """
        เรียนรู้หลักการบริหารองค์กรและทรัพยากรบุคคลเพื่อให้องค์กรดำเนินงานได้อย่างมีประสิทธิภาพและบรรลุเป้าหมาย
        - **เรียนเกี่ยวกับ:** การวางแผนกลยุทธ์, การจัดการทรัพยากรมนุษย์, การบริหารการเงิน, การเป็นผู้นำ
        - **อาชีพในอนาคต:** ผู้จัดการฝ่ายต่างๆ, นักวิเคราะห์ธุรกิจ (Business Analyst), เจ้าของกิจการ
        """
    )