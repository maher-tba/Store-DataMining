import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
from pages.Data_Analysis import show_data_analysis_page
from pages.association_rules import show_association_rules_page
# إعداد الصفحة
st.set_page_config(
    page_title="نظام توصية المنتجات",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص للتنسيق
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 1rem;
        font-family: 'Arial', sans-serif;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Arial', sans-serif;
    }
    
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        font-family: 'Arial', sans-serif;
    }
    
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
        font-family: 'Arial', sans-serif;
    }
    
    .arabic-text {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # شريط التنقل الجانبي
    st.sidebar.title("🛍️ التنقل")
    st.sidebar.markdown("---")
    
    # فحص وجود ملفات البيانات
    data_files_exist = check_data_files()
    
    if not data_files_exist:
        st.sidebar.warning("⚠️ ملفات البيانات غير موجودة!")
        st.sidebar.info("يرجى رفع ملفات البيانات المطلوبة:")
        st.sidebar.markdown("- Extended_Products_Dataset__25_Products.csv")
        st.sidebar.markdown("- Invoices_Dataset_for_Association_Rules.csv")
    
    # اختيار الصفحة
    pages = {
        "🏠 الرئيسية": "home",
        "📊 تحليل البيانات": "data_analysis",
        "🔗 قواعد الارتباط": "association_rules", 
        "🎯 تحليل التجميع": "clustering",
        "💰 دراسة تأثير السعر": "price_impact",
        "🤖 نظام التوصية": "recommendation"
    }
    
    selected_page = st.sidebar.selectbox("اختر الصفحة", list(pages.keys()))
    
    # معلومات المشروع في الشريط الجانبي
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 معلومات المشروع")
    st.sidebar.markdown("""
    **التقنيات المستخدمة:**
    - قواعد الارتباط (Apriori)
    - التجميع بخوارزمية K-Means
    - تحليل تأثير السعر
    
    **أهداف تنقيب البيانات:**
    - توصية المنتجات
    - تحليل سلوك العملاء
    - دراسة تأثير الخصائص
    """)
    
    # المحتوى الرئيسي حسب الصفحة المختارة
    if selected_page == "🏠 الرئيسية":
        show_home_page()
    elif selected_page == "📊 تحليل البيانات":
        show_data_analysis_page() 
    elif selected_page == "🔗 قواعد الارتباط":
        show_association_rules_page()
    elif selected_page == "🎯 تحليل التجميع":
        show_clustering_page()
    elif selected_page == "💰 دراسة تأثير السعر":
        show_price_impact_page()
    elif selected_page == "🤖 نظام التوصية":
        show_recommendation_page()

def check_data_files():
    """فحص وجود ملفات البيانات المطلوبة"""
    required_files = [
        "data/Extended_Products_Dataset__25_Products.csv",
        "data/Invoices_Dataset_for_Association_Rules.csv"
    ]
    
    return all(os.path.exists(file) for file in required_files)

def show_home_page():
    """عرض محتوى الصفحة الرئيسية"""
    
    st.markdown('<h1 class="main-header">🛍️ نظام توصية المنتجات</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">مشروع تنقيب البيانات باستخدام قواعد الارتباط والتجميع</p>', unsafe_allow_html=True)
    
    # رسالة الترحيب
    st.markdown("""
    <div class="info-box arabic-text">
        <h3>🎯 مرحباً بك في نظام توصية المنتجات!</h3>
        <p>يحلل هذا النظام أنماط شراء العملاء وخصائص المنتجات لتقديم توصيات ذكية للمنتجات باستخدام تقنيات تنقيب البيانات المتقدمة.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # نظرة عامة على المشروع في أعمدة
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-container arabic-text">
            <h4>🔗 قواعد الارتباط</h4>
            <p>اكتشف المنتجات التي يتم شراؤها معاً بكثرة باستخدام خوارزمية Apriori</p>
            <ul>
                <li>تحليل سلة التسوق</li>
                <li>فرص البيع المتقاطع</li>
                <li>أنماط سلوك العملاء</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container arabic-text">
            <h4>🎯 تحليل التجميع</h4>
            <p>تجميع المنتجات المتشابهة بناءً على خصائصها باستخدام خوارزمية K-Means</p>
            <ul>
                <li>تقسيم المنتجات</li>
                <li>كشف التشابه</li>
                <li>التجميع المبني على الخصائص</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container arabic-text">
            <h4>💰 دراسة تأثير السعر</h4>
            <p>تحليل كيفية تأثير التسعير على جودة التجميع والتوصيات</p>
            <ul>
                <li>تحليل تأثير الخصائص</li>
                <li>تقييم الجودة</li>
                <li>رؤى التحسين</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # إحصائيات سريعة إذا كانت البيانات متوفرة
    if check_data_files():
        st.markdown("---")
        st.subheader("📈 نظرة سريعة على البيانات")
        
        try:
            products_df = pd.read_csv("data/Extended_Products_Dataset__25_Products.csv")
            invoices_df = pd.read_csv("data/Invoices_Dataset_for_Association_Rules.csv") 
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("إجمالي المنتجات", len(products_df))
            
            with col2:
                st.metric("العلامات التجارية الفريدة", products_df['Brand'].nunique())
            
            with col3:
                st.metric("فئات المنتجات", products_df['Category'].nunique())
            
            with col4:
                st.metric("سجلات الفواتير", len(invoices_df))
                
        except Exception as e:
            st.error(f"خطأ في تحميل البيانات: {e}")
    
    # دليل التنقل
    st.markdown("---")
    st.subheader("🗺️ كيفية استخدام هذا النظام")
    
    steps = [
        ("📊 تحليل البيانات", "ابدأ بالاستكشاف هيكل البيانات والتوزيعات"),
        ("🔗 قواعد الارتباط", "استخراج الأنماط المتكررة وقواعد الارتباط"),
        ("🎯 تحليل التجميع", "تجميع المنتجات بناءً على التشابه"),
        ("💰 دراسة تأثير السعر", "تحليل تأثير السعر على جودة التجميع"),
        ("🤖 نظام التوصية", "احصل على التوصيات النهائية بناءً على جميع التحليلات")
    ]
    
    for i, (title, description) in enumerate(steps, 1):
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 1rem 0;" class="arabic-text">
            <div style="background-color: #1f77b4; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-left: 1rem; font-weight: bold;">
                {i}
            </div>
            <div>
                <strong>{title}</strong><br>
                <small style="color: #666;">{description}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)






def show_clustering_page():
    """صفحة تحليل التجميع"""
    st.title("🎯 تحليل التجميع")
    st.info("ستقوم هذه الصفحة بتنفيذ تجميع K-Means على خصائص المنتجات.")
    st.markdown("**الميزات ستشمل:**")
    st.markdown("- تحديد العدد الأمثل للمجموعات")
    st.markdown("- نتائج تجميع K-Means")
    st.markdown("- تصور المجموعات")
    st.markdown("- تحليل تجميع المنتجات")

def show_price_impact_page():
    """صفحة دراسة تأثير السعر"""
    st.title("💰 دراسة تأثير السعر")
    st.info("ستحلل هذه الصفحة كيفية تأثير إدراج السعر على جودة التجميع.")
    st.markdown("**الميزات ستشمل:**")
    st.markdown("- مقارنة التجميع مع/بدون السعر")
    st.markdown("- حساب مقاييس الجودة")
    st.markdown("- تحليل أهمية الخصائص")
    st.markdown("- تقييم جودة التوصيات")

def show_recommendation_page():
    """صفحة نظام التوصية"""
    st.title("🤖 نظام التوصية")
    st.info("ستوفر هذه الصفحة واجهة توصية المنتجات النهائية.")
    st.markdown("**الميزات ستشمل:**")
    st.markdown("- البحث واختيار المنتجات")
    st.markdown("- التوصيات المبنية على الارتباط")
    st.markdown("- التوصيات المبنية على التجميع")
    st.markdown("- نقاط التوصية المدمجة")

if __name__ == "__main__":
    main()