import streamlit as st
import graphviz

# --- ตั้งค่าพื้นฐานของหน้าเว็บ ---
st.set_page_config(page_title="แนะนำสาขาวิชา", page_icon="🎓", layout="wide")

# --- เมนูหลักด้านซ้าย ---
st.sidebar.title("เมนูหลัก")
menu_choice = st.sidebar.selectbox(
    "เลือกเมนูที่ต้องการ:",
    ("ให้ความรู้แต่ละสาขา", "แบบทดสอบเลือกการตัดสินใจ")
)

# --- แสดงหน้าตามเมนูที่เลือก ---

# 1. ถ้าผู้ใช้เลือกเมนู "ให้ความรู้แต่ละสาขา"
if menu_choice == "ให้ความรู้แต่ละสาขา":
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


# 2. ถ้าผู้ใช้เลือกเมนู "แบบทดสอบเลือกการตัดสินใจ"
elif menu_choice == "แบบทดสอบเลือกการตัดสินใจ":
    st.title("📝 แบบทดสอบเลือกการตัดสินใจ")
    st.write("เลือกผลการเรียนของคุณในแต่ละด้าน แล้วกดปุ่มเพื่อดูเส้นทางการตัดสินใจและผลลัพธ์")

    # --- ส่วนรับข้อมูลจากผู้ใช้ (ย้ายมาอยู่ใต้ title ของหน้านี้) ---
    st.sidebar.header("กรอกข้อมูลของคุณที่นี่")
    total_grade = st.sidebar.radio("1. ผลการเรียนเฉลี่ยรวม", ["ดี", "ไม่ดี"], key="total")
    major_grade = st.sidebar.radio("2. ผลการเรียนในวิชาเอก", ["ดี", "ไม่ดี"], key="major")
    business_grade = st.sidebar.radio("3. ผลการเรียนในวิชาธุรกิจ", ["ดี", "ไม่ดี"], key="business")

    # --- ปุ่มสำหรับเริ่มประมวลผล ---
    if st.sidebar.button("แสดงผลการแนะนำ"):

        # --- ส่วนตรรกะการตัดสินใจ (Logic) ---
        path_nodes = ["total"]
        path_edges = []
        result = ""

        if total_grade == "ไม่ดี":
            path_nodes.append("major1")
            path_edges.append(("total", "major1"))
            if major_grade == "ไม่ดี":
                path_nodes.append("biz1")
                path_edges.append(("major1", "biz1"))
                if business_grade == "ไม่ดี":
                    path_nodes.append("mgmt")
                    path_edges.append(("biz1", "mgmt"))
                    result = "การจัดการ (Management)"
                else:
                    path_nodes.append("comp2")
                    path_edges.append(("biz1", "comp2"))
                    result = "คอมพิวเตอร์ (Computer)"
            else:
                path_nodes.append("comp1")
                path_edges.append(("major1", "comp1"))
                result = "คอมพิวเตอร์ (Computer)"
        else:
            path_nodes.append("major2")
            path_edges.append(("total", "major2"))
            if major_grade == "ไม่ดี":
                path_nodes.append("hotel1")
                path_edges.append(("major2", "hotel1"))
                result = "การโรงแรม (Hotel)"
            else:
                path_nodes.append("biz2")
                path_edges.append(("major2", "biz2"))
                if business_grade == "ไม่ดี":
                    path_nodes.append("hotel2")
                    path_edges.append(("biz2", "hotel2"))
                    result = "การโรงแรม (Hotel)"
                else:
                    path_nodes.append("mktg")
                    path_edges.append(("biz2", "mktg"))
                    result = "การตลาด (Marketing)"

        # --- ส่วนสร้างภาพกราฟ (Visual) ---
        dot = graphviz.Digraph(comment='Decision Tree')
        dot.attr('node', shape='box', style='rounded, filled', fontname='Tahoma')
        dot.attr('edge', fontname='Tahoma')
        dot.attr(rankdir='TB')

        nodes = {
            "total": "Rank_grade_total", "major1": "Rank_grade_major", "major2": "Rank_grade_major",
            "biz1": "Rank_grade_business", "biz2": "Rank_grade_business", "comp1": "computer",
            "hotel1": "hotel", "mgmt": "management", "comp2": "computer", "hotel2": "hotel", "mktg": "marketing"
        }
        
        edges = [
            ("total", "major1", "Bad"), ("total", "major2", "Good"),
            ("major1", "biz1", "Bad"), ("major1", "comp1", "Good"),
            ("major2", "hotel1", "Bad"), ("major2", "biz2", "Good"),
            ("biz1", "mgmt", "Bad"), ("biz1", "comp2", "Good"),
            ("biz2", "hotel2", "Bad"), ("biz2", "mktg", "Good")
        ]

        for node_id, label in nodes.items():
            if node_id in path_nodes:
                dot.node(node_id, label, color="#28a745", fillcolor="#d4edda")
            else:
                dot.node(node_id, label, color="#adb5bd", fillcolor="#f8f9fa")

        for u, v, label in edges:
            if (u, v) in path_edges:
                dot.edge(u, v, label, color="#28a745", penwidth="2.5", fontcolor="#28a745")
            else:
                dot.edge(u, v, label, color="#adb5bd")
                
        # --- ส่วนแสดงผลลัพธ์ ---
        st.header("เส้นทางการตัดสินใจของคุณ:")
        st.graphviz_chart(dot)
        st.success(f"สาขาที่แนะนำสำหรับคุณคือ: **{result}**")

    else:
        st.info("กรุณาเลือกข้อมูลทางด้านซ้ายและกดปุ่ม 'แสดงผลการแนะนำ' เพื่อเริ่มต้น")