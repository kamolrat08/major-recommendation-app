import streamlit as st
import graphviz
import pandas as pd
import numpy as np
import plotly.express as px

# --- ตั้งค่าพื้นฐานของหน้าเว็บ ---
st.set_page_config(page_title="แนะนำสาขาวิชา", page_icon="🎓", layout="wide")

# --- เมนูหลักด้านซ้าย ---
st.sidebar.title("เมนูหลัก")
menu_choice = st.sidebar.selectbox(
    "เลือกเมนูที่ต้องการ:",
    ("Dashboard สรุปผล", "ให้ความรู้แต่ละสาขา", "แบบทดสอบเลือกการตัดสินใจ")
)

# --- แสดงหน้าตามเมนูที่เลือก ---

# 1. ถ้าผู้ใช้เลือกเมนู "Dashboard สรุปผล"
if menu_choice == "Dashboard สรุปผล":
    st.title("📊 Dashboard สรุปผล")
    st.write("ภาพรวมข้อมูลจากการจำลองนักเรียน 200 คนที่เข้ามาทำแบบทดสอบ")

    # --- สร้างข้อมูลจำลอง (Simulated Data) ---
    @st.cache_data # ใช้ Cache เพื่อให้ไม่ต้องสร้างข้อมูลใหม่ทุกครั้งที่รีเฟรช
    def create_mock_data():
        num_students = 200
        grades = ["ดี", "ไม่ดี"]
        data = {
            'Total_Grade': np.random.choice(grades, num_students, p=[0.6, 0.4]),
            'Major_Grade': np.random.choice(grades, num_students, p=[0.5, 0.5]),
            'Business_Grade': np.random.choice(grades, num_students, p=[0.7, 0.3])
        }
        df = pd.DataFrame(data)
        
        recommendations = []
        for index, row in df.iterrows():
            result = ""
            if row['Total_Grade'] == "ไม่ดี":
                if row['Major_Grade'] == "ไม่ดี":
                    if row['Business_Grade'] == "ไม่ดี": result = "การจัดการ"
                    else: result = "คอมพิวเตอร์"
                else: result = "คอมพิวเตอร์"
            else: # Total_Grade == "ดี"
                if row['Major_Grade'] == "ไม่ดี": result = "การโรงแรม"
                else:
                    if row['Business_Grade'] == "ไม่ดี": result = "การโรงแรม"
                    else: result = "การตลาด"
            recommendations.append(result)
        
        df['Recommended_Major'] = recommendations
        return df

    df = create_mock_data()

    # --- แสดงผล Dashboard ---
    st.header("สรุปสาขาที่ได้รับการแนะนำมากที่สุด")
    
    # กราฟแท่งแสดงจำนวนนักเรียนในแต่ละสาขา
    major_counts = df['Recommended_Major'].value_counts().reset_index()
    major_counts.columns = ['สาขาวิชา', 'จำนวนนักเรียน']
    
    fig_bar = px.bar(major_counts, 
                     x='สาขาวิชา', 
                     y='จำนวนนักเรียน', 
                     title="จำนวนนักเรียนที่ได้รับการแนะนำในแต่ละสาขา",
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

    st.header("ตารางข้อมูลดิบ")
    st.dataframe(df)


# 2. ถ้าผู้ใช้เลือกเมนู "ให้ความรู้แต่ละสาขา"
elif menu_choice == "ให้ความรู้แต่ละสาขา":
    # (โค้ดส่วนนี้เหมือนเดิม ไม่ต้องแก้ไข)
    st.title("📚 ข้อมูลความรู้แต่ละสาขา")
    st.write("ทำความรู้จักกับสาขาวิชาต่างๆ เพื่อประกอบการตัดสินใจของคุณ")
    st.header("💻 สาขาคอมพิวเตอร์ (Computer)")
    st.write("...") # ใส่เนื้อหาเดิม
    st.header("🏨 สาขาการโรงแรม (Hotel)")
    st.write("...") # ใส่เนื้อหาเดิม
    st.header("📈 สาขาการตลาด (Marketing)")
    st.write("...") # ใส่เนื้อหาเดิม
    st.header("👔 สาขาการจัดการ (Management)")
    st.write("...") # ใส่เนื้อหาเดิม


# 3. ถ้าผู้ใช้เลือกเมนู "แบบทดสอบเลือกการตัดสินใจ"
elif menu_choice == "แบบทดสอบเลือกการตัดสินใจ":
    # (โค้ดส่วนนี้เหมือนเดิม ไม่ต้องแก้ไข)
    st.title("📝 แบบทดสอบเลือกการตัดสินใจ")
    st.write("เลือกผลการเรียนของคุณในแต่ละด้าน แล้วกดปุ่มเพื่อดูเส้นทางการตัดสินใจและผลลัพธ์")
    st.sidebar.header("กรอกข้อมูลของคุณที่นี่")
    total_grade = st.sidebar.radio("1. ผลการเรียนเฉลี่ยรวม", ["ดี", "ไม่ดี"], key="total")
    major_grade = st.sidebar.radio("2. ผลการเรียนในวิชาเอก", ["ดี", "ไม่ดี"], key="major")
    business_grade = st.sidebar.radio("3. ผลการเรียนในวิชาธุรกิจ", ["ดี", "ไม่ดี"], key="business")
    if st.sidebar.button("แสดงผลการแนะนำ"):
        # (โค้ด Logic และ Graphviz ทั้งหมดเหมือนเดิม)
        path_nodes = ["total"]
        path_edges = []
        result = ""
        if total_grade == "ไม่ดี":
            # ... โค้ด Logic เดิมทั้งหมด ...
            result = "การจัดการ (Management)"
        else:
            # ... โค้ด Logic เดิมทั้งหมด ...
            result = "การตลาด (Marketing)"
        
        dot = graphviz.Digraph()
        # ... โค้ดสร้าง Graphviz เดิมทั้งหมด ...
        st.header("เส้นทางการตัดสินใจของคุณ:")
        st.graphviz_chart(dot)
        st.success(f"สาขาที่แนะนำสำหรับคุณคือ: **{result}**")
    else:
        st.info("กรุณาเลือกข้อมูลทางด้านซ้ายและกดปุ่ม 'แสดงผลการแนะนำ' เพื่อเริ่มต้น")