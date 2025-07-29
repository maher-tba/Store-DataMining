import streamlit as st
import pandas as pd
from itertools import combinations

def show_association_rules_page():
    """صفحة قواعد الارتباط البسيطة"""
    
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
    
    .rule-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="simple-title">🔗 قواعد الارتباط البسيطة</h1>', unsafe_allow_html=True)
    
    try:
        # تحميل البيانات
        invoices_df = load_invoice_data()
        
        # عرض معلومات أساسية
        st.subheader("📊 معلومات البيانات")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("عدد الفواتير", invoices_df['InvoiceID'].nunique())
        with col2:
            st.metric("عدد المنتجات", invoices_df['ProductID'].nunique())
        with col3:
            st.metric("إجمالي المعاملات", len(invoices_df))
        
        # تحليل بسيط للفواتير
        st.subheader("🛒 تحليل سلة التسوق")
        
        # إنشاء قاعدة بيانات الفواتير
        basket_data = create_basket_data(invoices_df)
        
        # عرض أشهر المنتجات
        st.subheader("⭐ أشهر المنتجات")
        product_counts = invoices_df['ProductID'].value_counts().head(5)
        
        for product_id, count in product_counts.items():
            st.markdown(f"""
            <div class="rule-card">
                <strong>منتج رقم {product_id}</strong> - تم شراؤه {count} مرة
            </div>
            """, unsafe_allow_html=True)
        
        # قواعد ارتباط بسيطة
        st.subheader("🔗 قواعد الارتباط البسيطة")
        
        rules = find_simple_rules(basket_data)
        
        if rules:
            for rule in rules[:5]:  # عرض أول 5 قواعد
                st.markdown(f"""
                <div class="rule-card">
                    <strong>إذا اشترى العميل:</strong> {rule['antecedent']} <br>
                    <strong>فمن المحتمل أن يشتري:</strong> {rule['consequent']} <br>
                    <strong>نسبة الثقة:</strong> {rule['confidence']:.1%}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لم يتم العثور على قواعد ارتباط قوية في البيانات الحالية")
        
        # عرض عينة من البيانات
        st.subheader("👀 عينة من بيانات الفواتير")
        st.dataframe(invoices_df.head(10), use_container_width=True)
        
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {str(e)}")

def load_invoice_data():
    """تحميل بيانات الفواتير"""
    try:
        df = pd.read_csv("data/Invoices_Dataset_for_Association_Rules.csv")
        return df
    except:
        # إنشاء بيانات تجريبية
        data = {
            'InvoiceID': [2001, 2001, 2001, 2001, 2002, 2002, 2002, 2002, 2002, 2003, 2003, 2004],
            'ProductID': [17, 9, 25, 1, 13, 8, 19, 11, 25, 16, 22, 23],
            'Quantity': [1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 2]
        }
        return pd.DataFrame(data)

def create_basket_data(invoices_df):
    """إنشاء بيانات سلة التسوق"""
    basket = invoices_df.groupby('InvoiceID')['ProductID'].apply(list).to_dict()
    return basket

def find_simple_rules(basket_data, min_support=0.1, min_confidence=0.5):
    """البحث عن قواعد ارتباط بسيطة"""
    # حساب تكرار المنتجات الفردية
    all_items = []
    for items in basket_data.values():
        all_items.extend(items)
    
    item_counts = {}
    for item in all_items:
        item_counts[item] = item_counts.get(item, 0) + 1
    
    total_transactions = len(basket_data)
    
    # العثور على العناصر المتكررة
    frequent_items = {item: count for item, count in item_counts.items() 
                     if count / total_transactions >= min_support}
    
    rules = []
    
    # البحث عن قواعد بسيطة (عنصر واحد -> عنصر واحد)
    for item1 in frequent_items:
        for item2 in frequent_items:
            if item1 != item2:
                # حساب الثقة
                both_count = 0
                item1_count = 0
                
                for items in basket_data.values():
                    if item1 in items:
                        item1_count += 1
                        if item2 in items:
                            both_count += 1
                
                if item1_count > 0:
                    confidence = both_count / item1_count
                    if confidence >= min_confidence:
                        rules.append({
                            'antecedent': f'منتج {item1}',
                            'consequent': f'منتج {item2}',
                            'confidence': confidence
                        })
    
    # ترتيب حسب الثقة
    rules.sort(key=lambda x: x['confidence'], reverse=True)
    return rules

if __name__ == "__main__":
    show_association_rules_page()