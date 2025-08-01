# نظام توصية للمنتجات باستخدام قواعد الارتباط والعنقدة

## وصف المشروع

يهدف المشروع إلى تطوير نظام توصية يعرض للمستخدم منتجات مشابهة عند فتح أي منتج، بالاعتماد على تقنيتين أساسيتين من تقنيات تنقيب البيانات:

### 1. قواعد الارتباط (Association Rules)
لاقتراح المنتجات التي غالبًا ما تُشترى مع المنتج الحالي ("من يشتري هذا المنتج، يشتري معه ذاك").

### 2. العنقدة (Clustering)
لتجميع المنتجات المتشابهة في عنقود واحد (بناءً على خصائصها)، واقتراح منتجات من نفس العنقود.

## أهداف المشروع

- تطبيق خوارزمية Apriori لاستخراج قواعد الشراء المشترك
- تطبيق خوارزمية K-Means لتجميع المنتجات في عناقيد
- تخزين رقم العنقود الخاص بكل منتج في قاعدة البيانات بعد تنفيذ العنقدة
- عرض منتجات مقترحة بناءً على:
  - قواعد الشراء المشترك
  - المنتجات من نفس العنقود
- إجراء دراسة تجريبية لتحديد أفضل الخصائص التي ساهمت في تشكيل العناقيد

## الدراسة التجريبية

تحليل العناقيد الناتجة بهدف تقييم أثر كل خاصية (مثل السعر، النوع، الشركة) على جودة التجميع من خلال:

1. اختيار عينات من المنتجات ضمن عنقود معين
2. عرض المنتجات المشابهة لها
3. تقييم جودة التشابه بدرجة من 100
4. حساب المتوسط الحسابي للتقييمات
5. مقارنة بين:
   - عنقدة مع تضمين السعر
   - عنقدة بدون تضمين السعر
6. اتخاذ قرار حول تأثير السعر على جودة العنقدة

## المتطلبات

### Python Libraries:
```
pandas>=1.5.0
mlxtend>=0.21.0
scikit-learn>=1.1.0
matplotlib>=3.5.0
seaborn>=0.11.0
numpy>=1.21.0
jupyter>=1.0.0
```

## هيكل المشروع

```

product-recommendation-system/
│
├── streamlit_app.py              # Main Streamlit application
├── pages/
│   ├── 01_data_exploration.ipynb       # Data exploration page
│   ├── 02_association_rules.ipynb   # Association rules analysis
│   ├── 03_Clustering_Analysis.ipynb # Clustering analysis
│   ├── 04_Price_Impact_Study.py  # Price impact study
│   └── 05_Recommendation_System.py # Final recommendation system
│
├── data/
│   ├── Extended_Products_Dataset__25_Products.csv
│   ├── Invoices_Dataset_for_Association_Rules.csv
│   ├── processed/
│   └── results/
│
├── src/
│   ├── data_preprocessing.py
│   ├── association_rules.py
│   ├── clustering.py
│   └── recommendation_system.py
│
├── requirements.txt
├── README.md
└── .gitignore
## كيفية التشغيل

1. **تثبيت المتطلبات:**
   ```bash
   pip install -r requirements.txt
   ```

2. **تشغيل Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

3. **اتباع التسلسل:**
   - ابدأ بـ `01_data_exploration.ipynb`
   - ثم `02_association_rules.ipynb`
   - ثم `03_clustering_analysis.ipynb`
   - ثم `04_price_impact_study.ipynb`
   - وأخيراً `05_final_recommendation_system.ipynb`

## النتائج المتوقعة

- نظام توصية فعال يجمع بين قواعد الارتباط والعنقدة
- تحليل مفصل لتأثير السعر على جودة التوصيات
- توصيات محسنة للمنتجات بناءً على سلوك الشراء والخصائص المتشابهة

## المساهمة

نرحب بالمساهمات! يرجى فتح issue أو إرسال pull request.

## الترخيص

هذا المشروع مرخص تحت رخصة IUSR