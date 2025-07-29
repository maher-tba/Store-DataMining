import streamlit as st
import pandas as pd
import numpy as np

def show_recommendation_page():
    """صفحة نظام التوصية البسيط"""
    
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
    
    .recommendation-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #dc3545;
    }
    
    .selected-product {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="simple-title">🤖 نظام التوصية البسيط</h1>', unsafe_allow_html=True)
    
    try:
        # تحميل البيانات
        products_df = load_products_data()
        
        # عرض معلومات أساسية
        st.subheader("📊 معلومات النظام")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("عدد المنتجات", len(products_df))
        with col2:
            st.metric("عدد الفئات", products_df['Category'].nunique())
        with col3:
            st.metric("عدد العلامات التجارية", products_df['Brand'].nunique())
        
        # اختيار منتج للحصول على توصيات
        st.subheader("🔍 اختر منتج للحصول على توصيات")
        
        # عرض قائمة المنتجات
        product_options = {}
        for idx, row in products_df.iterrows():
            product_options[f"{row['ProductName']} - {row['Brand']} (${row['Price']})"] = idx
        
        selected_product_display = st.selectbox(
            "اختر المنتج:",
            list(product_options.keys())
        )
        
        if selected_product_display:
            selected_idx = product_options[selected_product_display]
            selected_product = products_df.iloc[selected_idx]
            
            # عرض المنتج المختار
            st.markdown(f"""
            <div class="selected-product">
                <h4>🛍️ المنتج المختار</h4>
                <p><strong>الاسم:</strong> {selected_product['ProductName']}</p>
                <p><strong>العلامة التجارية:</strong> {selected_product['Brand']}</p>
                <p><strong>الفئة:</strong> {selected_product['Category']}</p>
                <p><strong>السعر:</strong> ${selected_product['Price']}</p>
                <p><strong>التقييم:</strong> {selected_product['Rating']} ⭐</p>
            </div>
            """, unsafe_allow_html=True)
            
            # نوع التوصية
            recommendation_type = st.selectbox(
                "نوع التوصية:",
                ["حسب الفئة", "حسب السعر المشابه", "حسب التقييم العالي"]
            )
            
            # عدد التوصيات
            num_recommendations = st.slider("عدد التوصيات:", 1, 5, 3)
            
            # الحصول على التوصيات
            if st.button("🎯 احصل على التوصيات"):
                recommendations = get_recommendations(
                    products_df, 
                    selected_idx, 
                    recommendation_type, 
                    num_recommendations
                )
                
                st.subheader("💡 التوصيات المقترحة")
                
                if recommendations is not None and len(recommendations) > 0:
                    for i, (idx, product) in enumerate(recommendations.iterrows(), 1):
                        similarity_score = calculate_similarity_score(selected_product, product)
                        
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>🏷️ توصية #{i}</h4>
                            <p><strong>الاسم:</strong> {product['ProductName']}</p>
                            <p><strong>العلامة التجارية:</strong> {product['Brand']}</p>
                            <p><strong>السعر:</strong> ${product['Price']}</p>
                            <p><strong>التقييم:</strong> {product['Rating']} ⭐</p>
                            <p><strong>نقاط التشابه:</strong> {similarity_score:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("لم يتم العثور على توصيات مناسبة")
        
        # إحصائيات سريعة
        st.subheader("📈 إحصائيات سريعة")
        
        # أعلى المنتجات تقييماً
        top_rated = products_df.nlargest(3, 'Rating')[['ProductName', 'Brand', 'Rating', 'Price']]
        st.markdown("**⭐ أعلى المنتجات تقييماً:**")
        st.dataframe(top_rated, use_container_width=True, hide_index=True)
        
        # أرخص المنتجات
        cheapest = products_df.nsmallest(3, 'Price')[['ProductName', 'Brand', 'Rating', 'Price']]
        st.markdown("**💰 أرخص المنتجات:**")
        st.dataframe(cheapest, use_container_width=True, hide_index=True)
        
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
            'ProductName': ['Bluetooth Headset', 'Portable SSD', 'Surge Protector', 'Wireless Mouse', '4K Monitor', 'External HDD', 'Flash Drive', 'Gaming Mouse', 'Conference Webcam', 'Ergonomic Chair', 'Desk Lamp', 'USB Cable'],
            'Brand': ['Sony', 'Samsung', 'Belkin', 'Logitech', 'LG', 'WD', 'SanDisk', 'Razer', 'Logitech', 'IKEA', 'Philips', 'Anker'],
            'Category': ['Accessories', 'Storage', 'Accessories', 'Accessories', 'Electronics', 'Storage', 'Storage', 'Accessories', 'Electronics', 'Furniture', 'Accessories', 'Accessories'],
            'Price': [55, 80, 30, 15.99, 300, 60, 12, 35, 90, 180, 18, 8],
            'Rating': [4.2, 4.6, 4.5, 4.4, 5.0, 4.7, 4.3, 4.9, 4.6, 4.9, 4.2, 4.1],
            'Stock': [190, 168, 216, 158, 38, 114, 76, 156, 66, 163, 156, 200]
        }
        return pd.DataFrame(data)

def get_recommendations(df, selected_idx, recommendation_type, num_recommendations):
    """الحصول على التوصيات"""
    
    selected_product = df.iloc[selected_idx]
    
    # استبعاد المنتج المختار
    candidates = df.drop(selected_idx)
    
    if recommendation_type == "حسب الفئة":
        # البحث في نفس الفئة
        recommendations = candidates[
            candidates['Category'] == selected_product['Category']
        ].head(num_recommendations)
        
    elif recommendation_type == "حسب السعر المشابه":
        # البحث حسب السعر المشابه (±30%)
        price_range = selected_product['Price'] * 0.3
        min_price = selected_product['Price'] - price_range
        max_price = selected_product['Price'] + price_range
        
        recommendations = candidates[
            (candidates['Price'] >= min_price) & 
            (candidates['Price'] <= max_price)
        ].head(num_recommendations)
        
    elif recommendation_type == "حسب التقييم العالي":
        # أعلى التقييمات
        recommendations = candidates.nlargest(num_recommendations, 'Rating')
    
    else:
        recommendations = candidates.head(num_recommendations)
    
    return recommendations

def calculate_similarity_score(product1, product2):
    """حساب نقاط التشابه بين منتجين"""
    
    score = 0
    total_factors = 0
    
    # التشابه في الفئة
    if product1['Category'] == product2['Category']:
        score += 30
    total_factors += 30
    
    # التشابه في السعر
    price_diff = abs(product1['Price'] - product2['Price'])
    max_price = max(product1['Price'], product2['Price'])
    if max_price > 0:
        price_similarity = max(0, (1 - price_diff / max_price)) * 25
        score += price_similarity
    total_factors += 25
    
    # التشابه في التقييم
    rating_diff = abs(product1['Rating'] - product2['Rating'])
    rating_similarity = max(0, (1 - rating_diff / 5)) * 25
    score += rating_similarity
    total_factors += 25
    
    # التشابه في العلامة التجارية
    if product1['Brand'] == product2['Brand']:
        score += 20
    total_factors += 20
    
    return (score / total_factors) * 100 if total_factors > 0 else 0

if __name__ == "__main__":
    show_recommendation_page()