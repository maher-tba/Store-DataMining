import streamlit as st
import pandas as pd
import numpy as np

def show_data_analysis_page():
    """صفحة تحليل البيانات البسيطة - القيم المفقودة فقط"""
    
    st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 1rem;
    }
    
    .simple-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        text-align: center;
    }
    
    .success-card {
        background: #d4edda;
        border-left: 5px solid #28a745;
        color: #155724;
    }
    
    .warning-card {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        color: #856404;
    }
    
    .arabic-text {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', sans-serif;
    }
    
    .big-number {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 0;
    }
    
    .table-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">📊 فحص القيم المفقودة</h1>', unsafe_allow_html=True)
    
    # تحميل البيانات
    try:
        products_df = load_data()
        
        # عدد القيم المفقودة الإجمالي
        total_missing = products_df.isnull().sum().sum()
        total_cells = products_df.shape[0] * products_df.shape[1]
        
        # عرض النتيجة الرئيسية
        if total_missing == 0:
            st.markdown(f"""
            <div class="simple-card success-card">
                <h2>✅ ممتاز!</h2>
                <p class="big-number">0</p>
                <h3>قيمة مفقودة</h3>
                <p>جميع البيانات مكتملة ولا توجد قيم مفقودة</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            missing_percentage = (total_missing / total_cells) * 100
            st.markdown(f"""
            <div class="simple-card warning-card">
                <h2>⚠️ تنبيه!</h2>
                <p class="big-number">{total_missing}</p>
                <h3>قيمة مفقودة</h3>
                <p>نسبة القيم المفقودة: {missing_percentage:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        # معلومات إضافية بسيطة
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="simple-card">
                <h3 style="color: #1f77b4;">📦 عدد المنتجات</h3>
                <p class="big-number" style="font-size: 2rem;">{len(products_df)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="simple-card">
                <h3 style="color: #28a745;">📋 عدد الأعمدة</h3>
                <p class="big-number" style="font-size: 2rem;">{len(products_df.columns)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="simple-card">
                <h3 style="color: #dc3545;">📊 إجمالي الخلايا</h3>
                <p class="big-number" style="font-size: 2rem;">{total_cells}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # جدول القيم المفقودة (فقط إذا وجدت)
        if total_missing > 0:
            st.markdown("---")
            st.subheader("📋 تفاصيل القيم المفقودة لكل عمود")
            
            missing_data = products_df.isnull().sum()
            missing_data = missing_data[missing_data > 0]  # عرض الأعمدة التي بها قيم مفقودة فقط
            
            if len(missing_data) > 0:
                missing_df = pd.DataFrame({
                    'اسم العمود': missing_data.index,
                    'عدد القيم المفقودة': missing_data.values,
                    'النسبة المئوية': ((missing_data.values / len(products_df)) * 100).round(1)
                })
                
                st.markdown('<div class="table-container">', unsafe_allow_html=True)
                st.dataframe(missing_df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # عرض عينة من البيانات
        st.markdown("---")
        st.subheader("👀 نظرة سريعة على البيانات")
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(products_df.head(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # رسالة بسيطة للمبتدئين
        st.markdown(f"""
        <div class="simple-card" style="margin-top: 2rem;">
            <h3>💡 ما هي القيم المفقودة؟</h3>
            <p class="arabic-text">
            القيم المفقودة هي البيانات التي لم يتم إدخالها أو فُقدت من قاعدة البيانات.
            <br>
            مثلاً: إذا كان هناك منتج بدون سعر أو تقييم، فهذه تُعتبر قيم مفقودة.
            <br>
            <strong>لماذا مهمة؟</strong> لأنها تؤثر على دقة التحليل والتوصيات.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {str(e)}")
        st.info("يرجى التأكد من وجود ملف البيانات في المجلد الصحيح")

def load_data():
    """تحميل البيانات"""
    # محاولة تحميل من ملف CSV
    df = pd.read_csv("data/Extended_Products_Dataset__25_Products.csv")
    return df


if __name__ == "__main__":
    show_data_analysis_page()