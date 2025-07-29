import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def show_clustering_page():
    """صفحة التجميع البسيطة"""
    
    st.markdown("""
    <style>
    .simple-title {
        font-size: 2rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 1rem;
    }
    
    .cluster-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #17a2b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="simple-title">🎯 تجميع المنتجات البسيط</h1>', unsafe_allow_html=True)
    
    try:
        # تحميل البيانات
        products_df = load_products_data()
        
        # عرض معلومات أساسية
        st.subheader("📊 معلومات البيانات")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("عدد المنتجات", len(products_df))
        with col2:
            st.metric("عدد الخصائص", len(products_df.columns))
        with col3:
            st.metric("عدد الفئات", products_df['Category'].nunique())
        
        # اختيار خصائص التجميع
        st.subheader("⚙️ اختيار خصائص التجميع")
        
        numeric_columns = ['Price', 'Rating', 'Stock', 'PowerWatt', 'WeightKg']
        available_columns = [col for col in numeric_columns if col in products_df.columns]
        
        selected_features = st.multiselect(
            "اختر الخصائص للتجميع:",
            available_columns,
            default=available_columns[:2] if len(available_columns) >= 2 else available_columns
        )
        
        if len(selected_features) >= 2:
            # عدد المجموعات
            n_clusters = st.slider("عدد المجموعات:", 2, 6, 3)
            
            # تنفيذ التجميع
            if st.button("🎯 تنفيذ التجميع"):
                clusters, cluster_centers = perform_clustering(products_df, selected_features, n_clusters)
                
                # إضافة نتائج التجميع للبيانات
                products_df['Cluster'] = clusters
                
                # عرض النتائج
                st.subheader("📈 نتائج التجميع")
                
                # رسم بياني للتجميع (إذا كان هناك خاصيتان)
                if len(selected_features) == 2:
                    fig = px.scatter(
                        products_df,
                        x=selected_features[0],
                        y=selected_features[1],
                        color='Cluster',
                        title=f'التجميع باستخدام {selected_features[0]} و {selected_features[1]}',
                        color_discrete_sequence=px.colors.qualitative.Set1
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # عرض تفاصيل كل مجموعة
                st.subheader("📋 تفاصيل المجموعات")
                
                for i in range(n_clusters):
                    cluster_products = products_df[products_df['Cluster'] == i]
                    
                    st.markdown(f"""
                    <div class="cluster-card">
                        <h4>🏷️ المجموعة {i + 1}</h4>
                        <p><strong>عدد المنتجات:</strong> {len(cluster_products)}</p>
                        <p><strong>أمثلة المنتجات:</strong> {', '.join(cluster_products['ProductName'].head(3).tolist())}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # إحصائيات المجموعة
                    if st.expander(f"إحصائيات المجموعة {i + 1}"):
                        cluster_stats = cluster_products[selected_features].describe()
                        st.dataframe(cluster_stats, use_container_width=True)
                
                # ملخص التجميع
                st.subheader("📊 ملخص التجميع")
                cluster_summary = products_df.groupby('Cluster').agg({
                    'ProductName': 'count',
                    'Price': 'mean',
                    'Rating': 'mean'
                }).round(2)
                cluster_summary.columns = ['عدد المنتجات', 'متوسط السعر', 'متوسط التقييم']
                st.dataframe(cluster_summary, use_container_width=True)
        
        else:
            st.warning("يرجى اختيار خاصيتين على الأقل للتجميع")
        
        # عرض عينة من البيانات
        st.subheader("👀 عينة من البيانات")
        st.dataframe(products_df[['ProductName', 'Category', 'Price', 'Rating']].head(10), use_container_width=True)
        
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {str(e)}")

def load_products_data():
    """تحميل بيانات المنتجات"""
    try:
        df = pd.read_csv("data/Extended_Products_Dataset__25_Products.csv")
        return df
    except:
        # إنشاء بيانات تجريبية
        data = {
            'ProductName': ['Bluetooth Headset', 'Portable SSD', 'Surge Protector', 'Wireless Mouse', '4K Monitor', 'External HDD', 'Flash Drive', 'Gaming Mouse', 'Conference Webcam', 'Ergonomic Chair', 'Desk Lamp'],
            'Category': ['Accessories', 'Storage', 'Accessories', 'Accessories', 'Electronics', 'Storage', 'Storage', 'Accessories', 'Electronics', 'Furniture', 'Accessories'],
            'Price': [55, 80, 30, 15.99, 300, 60, 12, 35, 90, 180, 18],
            'Rating': [4.2, 4.6, 4.5, 4.4, 5.0, 4.7, 4.3, 4.9, 4.6, 4.9, 4.2],
            'Stock': [190, 168, 216, 158, 38, 114, 76, 156, 66, 163, 156],
            'PowerWatt': [5, 2, 5, 2, 0, 5, 5, 0, 20, 30, 5],
            'WeightKg': [3.56, 1.13, 2.0, 5.26, 0.13, 0.96, 1.3, 2.86, 5.68, 4.14, 5.71]
        }
        return pd.DataFrame(data)

def perform_clustering(df, features, n_clusters):
    """تنفيذ التجميع باستخدام K-Means"""
    
    # تحضير البيانات
    X = df[features].copy()
    
    # معالجة القيم المفقودة
    X = X.fillna(X.mean())
    
    # تطبيع البيانات
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # تطبيق K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    return clusters, kmeans.cluster_centers_

if __name__ == "__main__":
    show_clustering_page()