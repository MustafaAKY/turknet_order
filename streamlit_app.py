import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide")
tab11, tab22, tab33 = st.tabs(["Yeni İŞ GİR", "Yapılan İşler", "Listeyi Sil"])

with tab11:
    # Load the data from the provided file
    tarih = datetime.now()
    tarih = tarih.strftime("%d.%m.%Y")

    url = "https://docs.google.com/spreadsheets/d/1F9_pYcSh2ct_LamzK0jhIHqBJY_STvUbXPdaLdc25xs/edit?gid=0#gid="

    conn = st.connection("gsheets", type=GSheetsConnection)
    
    paket1liste = conn.read(worksheet="Sayfa1", usecols=list(range(13)), ttl=500)
    paket1liste = paket1liste.dropna(how="all")

    st.title("İş Kaydetme Ekranı")
    data = st.text_area("İş bilgisini gir", placeholder="İş taslağını yapıştır. Sıralamanın doğru olduğundan emin ol.")
    bolge = st.selectbox("Çalıştığın Bölge", ["Gaziosmanpaşa", "Zeytinburnu"])
    malzemeler = st.multiselect("Kullandığın Malzemeleri Seç", ["MOBİLİZASYON", "Bina Sonlandırma Kutusu Kurulumu", "Bina İç Kutusu", "1/4 SPLİTTER", "1/8 SPLİTTER", "İlave Bina Splitter Kutusu (BSK) Kurulumu/Değişimi/Arıza-Onarım İşçiliği"], placeholder="Malzeme Seç")



    dugme = st.button("Kaydet")
    if dugme:
        if not data:
            st.write("Bilgiler eksik")
            st.stop()
        else:
            for line in data.split('\n'):
                parts = line.split("#")
                no = parts[1]
                address = parts[2]

                # Extract address components
                try:
                    mahalle = address.split(" NO: ")[0].replace("MAH.", "").strip()
                    sokak = mahalle.split()[-2] + " " + mahalle.split()[-1].replace("SK.", "").replace("CAD.", "").strip()
                    mahalle = " ".join(mahalle.split()[:-2]).strip()
                    kapi_no = address.split(" NO: ")[1].strip() if "NO: " in address else ""
                except IndexError:
                    st.write("Adres bilgileri doğru formatta değil.")
                    st.stop()

                description = parts[3]

                malzeme1 = 1 if "MOBİLİZASYON" in malzemeler else ""
                malzeme2 = 1 if "Bina Sonlandırma Kutusu Kurulumu" in malzemeler else ""
                malzeme3 = 1 if "Bina İç Kutusu" in malzemeler else ""
                malzeme4 = 1 if "1/4 SPLİTTER" in malzemeler else ""
                malzeme5 = 1 if "1/8 SPLİTTER" in malzemeler else ""
                malzeme6 = 1 if "İlave Bina Splitter Kutusu (BSK) Kurulumu/Değişimi/Arıza-Onarım İşçiliği" in malzemeler else ""


                processed_data = pd.DataFrame({
                    "NO": no,
                    "Müdahale Açıklaması": description,
                    "TARİH": tarih,
                    "İLÇE": bolge,
                    "MAHALLE veya SİTE ADI": mahalle,
                    "SOKAK/CADDE": sokak,
                    "DIŞ KAPI NO": kapi_no,
                    "SS.6.1.MOBİLİZASYON": malzeme1,
                    "SS.1.1.Bina Bağlantısı ve Aktivasyonu": "",
                    "SS.1.3.Bina Sonlandırma Kutusu Kurulumu": malzeme2,
                    "MM.3.1.Bina İç Kutusu": malzeme3,
                    "MM.2.1.1/4 SPLİTTER": malzeme4,
                    "MM.2.3.1/8 SPLİTTER": malzeme5,
                    "SS.3.4.İlave Bina Splitter Kutusu (BSK) Kurulumu/Değişimi/Arıza-Onarım İşçiliği": malzeme6
                })

                df = st.dataframe(processed_data)

                # Update Google Sheets
                updated_df = pd.concat([paket1liste, df], ignore_index=True)
                
                conn.update(worksheet="Sayfa1", data=updated_df)
                st.success("İş kaydedildi.")

with tab22:
    veri = pd.DataFrame(paket1liste)
    st.dataframe(veri)

with tab33:
    st.title("Sipariş Silme Ekranı")
    st.text("DİKKAT: SİPARİŞLERİ YAZDIRDIĞINDAN EMİN OL")
    if st.button("Hepsini Sil"):
        paket1liste.drop(paket1liste.index, inplace=True)
        conn.update(worksheet="Sayfa1", data=paket1liste)
        st.success("Tüm veri silindi!")
