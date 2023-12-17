import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Veri setlerini yükleyin
buy_box_unq = pd.read_csv('Int4_1_Cleaned_Buy_Box_Unqualified.csv')
image_data = pd.read_excel('merged.xlsx')

# Streamlit arayüzünü oluşturma
st.markdown(
    """
    <style>
    .stApp {
        background-color: orange;  /* Arka plan rengi */
    }
    .custom-text {
        font-size: 24px; /* Yazı boyutu */
        color: red;      /* Yazı rengi */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("Amazon.png", use_column_width=True)
# Kenar çubuğu için ASIN seçici ekle
unique_asins = buy_box_unq['ASIN'].unique()  # Veri setinden benzersiz ASIN'leri al
selected_asin = st.sidebar.selectbox("ASIN Seçiniz", unique_asins)
# Seçilen ASIN'i bir metin olarak gösterin ve kopyalanabilir yapın
st.sidebar.text(f"Seçilen ASIN: {selected_asin}")


def find_related_products(asin, df):
    related_products = [asin]  # Verilen ASIN ile başla
    index = 0
    while index < len(related_products):
        current_asin = related_products[index]
        filtered_df = df[df['ASIN'] == current_asin]
        if not filtered_df.empty:
            freq_bought_together = filtered_df.iloc[0]['Freq. Bought Together']
            if pd.notna(freq_bought_together) and freq_bought_together != 'nan':
                for product in freq_bought_together.split(', '):
                    if product not in related_products:
                        related_products.append(product)
        index += 1
    related_products.remove(asin)  # İlk eklenen ASIN'i kaldır
    return related_products

st.title('Ürün Tavsiye Sistemi')

asin_input = st.text_input('Beraber satılan ürünleri bulmak için bir ASIN girin:', '')

if asin_input:
    product_row = buy_box_unq[buy_box_unq['ASIN'] == asin_input]
    if not product_row.empty:
        product_details = product_row.iloc[0]
        st.write(f"**Ürün Adı:** {product_details['ASIN']}")
        st.write(f"**Kategori:** {product_details['Categories: Root']} > {product_details['Categories: Sub']}")
        st.write(f"**Son Aydaki Satış:** {product_details['Bought in past month']}")
        st.write(f"**Rating:** {product_details['Reviews: Rating']}")

        # ASIN'e ait resmi göster
        link_series = image_data[image_data['ASIN'] == asin_input]['Image']
        if not link_series.empty and pd.notna(link_series.iloc[0]):
            link = link_series.iloc[0]
            st.image(link, width=300, use_column_width=False, caption=f'ASIN: {asin_input}')

        related_products = find_related_products(asin_input, buy_box_unq)
        if related_products:
            st.subheader('Beraber Satın Alınan Ürünler:')
            st.write(related_products)
            for rp_asin in related_products:
                rp_row = buy_box_unq[buy_box_unq['ASIN'] == rp_asin]
                if not rp_row.empty:
                    rp_details = rp_row.iloc[0]
                    st.write(f"**Ürün Adı:** {rp_details['ASIN']} - **Kategori:** {rp_details['Categories: Root']} > {rp_details['Categories: Sub']} - **Son Aydaki Satışlar:** {rp_details['Bought in past month']} - **Rating:** {rp_details['Reviews: Rating']}")
            # Web sitesini bir iframe içinde göster
            st.markdown("### Amazon ASIN Arama")
            components.iframe("https://amazon-asin.com/", height=500, scrolling=True)
        else:
            st.write('Bu ASIN ile beraber satın alınan başka bir ürün bulunamadı.')
    else:
        st.error(f"{asin_input} ASIN'ine ait bilgi bulunamadı.")
