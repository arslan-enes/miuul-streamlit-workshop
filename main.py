import streamlit as st
import plotly.express as px
import joblib
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data
def get_data():
    df = px.data.gapminder()
    return df

def get_model():
    model = joblib.load("gapminder_model.joblib")
    return model


st.header("👨🏻‍⚕️ :red[Yaşam] Beklentisi :red[Tahmini] 👩🏻‍⚕️")
tab_home, tab_vis, tab_model = st.tabs(["Ana Sayfa", "Grafikler", "Model"])

# TAB HOME

column_hans, column_dataset = tab_home.columns(2, gap="large")

column_hans.subheader("Hans Rosling Kimdir?")

column_hans.markdown("1948'de Uppsala/İsveç'te dünyaya gelen Hans Rosling, sadece hekim ve uluslararası sağlık profesörü olmakla kalmayıp aynı zamanda Halka açık konferanslar veren ünlü bir konuşmacıydı. Rosling, Dünya Sağlık Örgütü ve UNICEF’e danışmanlık yapmanın yanı sıra, İsviçre’de Sınır Tanımayan Doktorlar ve Gapminder Vakfı’nın kurucu ortağı olarak da önemli bir rol oynamıştı. TED konuşmaları, otuz beş milyondan fazla izlenen Rosling, Time dergisinin yayımladığı dünyanın en etkili yüz insanı listesine girmişti. Hans, ömrünün son on yılını Factfulness kitabını yazmaya adamış ve 2017 yılında hayata gözlerini kapamıştır, ancak mirası ve etkisi dünya genelinde hala canlılığını korumaktadır.")
column_hans.image("media/hans_rosling.png")

column_dataset.subheader("Veri Seti Hakkında")
column_dataset.markdown("Geçmişte demografik değişkenleri, gelir bileşimini ve ölüm oranlarını dikkate alan birçok çalışma yapılmış olmasına rağmen, bağışıklama ve İnsani Gelişme Endeksi'nin etkisi göz önüne alınmamıştır. Bu çalışma, bağışıklama faktörleri, mortalite faktörleri, ekonomik faktörler, sosyal faktörler ve diğer sağlıkla ilgili faktörlere çalışmalara dahil edilmelidir. Bu veri setindeki gözlemler farklı ülkeler temelinde olduğu için bir ülkenin nüfusunun yaşam beklentisine katkıda bulunan tahmin edici faktörü belirlemesi daha kolay olacaktır. Bu, bir ülkeye nüfusunun yaşam beklentisini etkili bir şekilde artırmak için hangi alanın önemli olduğunu önermede yardımcı olacaktır.")

df = get_data()
column_dataset.dataframe(df, width=900)

# TAB VIS

## grafik 1

tab_vis.subheader("Seçilen Ülkelerin Yıllara Göre Yaşam Beklentisi Karşılaştırması")

selected_countries = tab_vis.multiselect(label="Ülke Seçiniz", options=df.country.unique(), default=["Turkey", "Syria", "Greece"])
filtered_df = df[df.country.isin(selected_countries)]

fig = px.line(
    filtered_df,
    x="year",
    y="lifeExp",
    color="country"
)

tab_vis.plotly_chart(fig, use_container_width=True)

## grafik 2

tab_vis.subheader("Ülkelerin Yıllar İçerisinde Yaşam Beklentisi Değişikliğinin Harita Üzerinde Gösterilmesi")
year_select_for_map = tab_vis.slider("Yıllar ", min_value=int(df.year.min()), max_value=int(df.year.max()),
                                     step=5)

fig2 = px.choropleth(df[df.year == year_select_for_map], locations="iso_alpha",
                     color="lifeExp",
                     range_color=(df.lifeExp.min(), df.lifeExp.max()),
                     hover_name="country",
                     color_continuous_scale=px.colors.sequential.Plasma)

tab_vis.plotly_chart(fig2, use_container_width=True)

## grafik 3


tab_vis.subheader("Ülkelerin Yıllar İçerisindeki Nüfus, GSMH ve Yaşam Beklentisi Değişimleri")
fig3 = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                  animation_group='country', animation_frame="year",
                  hover_name="country", range_x=[100, 100000], range_y=[25, 90], log_x=True, size_max=60)
fig3.add_hline(y=50, line_dash="dash", line_color="black")
tab_vis.plotly_chart(fig3, use_container_width=True)

# TAB MODEL

model = get_model()

year = tab_model.number_input("Yıl Giriniz", min_value=1952, max_value=2027, step=1, value=2000)
pop = tab_model.number_input("Nüfus Giriniz", min_value=10000, max_value=1000000000,  step=100000, value=1000000)
gdpPercap = tab_model.number_input("GDP Giriniz", min_value=1, step=1, value=5000)

user_input = pd.DataFrame({'year':year, 'pop':pop, 'gdpPercap': gdpPercap}, index=[0])

if tab_model.button("Tahmin et!"):
    prediction = model.predict(user_input)
    tab_model.success(f"Tahmin edilen yaşam süresi: {prediction[0]}")
    st.balloons()
