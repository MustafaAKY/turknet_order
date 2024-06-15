import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
# Load the data from the provided file

tarih = datetime.now()
tarih = tarih.strftime("%d.%m.%Y")

url = "https://docs.google.com/spreadsheets/d/1F9_pYcSh2ct_LamzK0jhIHqBJY_STvUbXPdaLdc25xs/edit?gid=0#gid="

conn = st.connection("gsheets", type=GSheetsConnection)         
  
paket1liste = conn.read(spreadsheet=url,worksheet="Sayfa1" ,usecols=list(range(13)),ttl=500)
paket1liste = paket1liste.dropna(how="all")

# Process the data
veri = pd.DataFrame(paket1liste)
st.dataframe(veri)

st.title("iş kaydetme Ekranı")    
data = st.text_area("İş bilgisini gir",placeholder="iş taslağını Yapıştır Sıralamanın Dorğu Olduğundan Emin Ol")
bolge = st.selectbox("Çalıştığın Bölge",["Gaziosmanpaşa","Zeytinburnu"])
malzemeler = st.multiselect("Kullandığın Malzemeleri Seç",["MOBİLİZASYON","Bina Sonlandırma Kutusu Kurulumu","Bina İç Kutusu","1/4 SPLİTTER","1/8 SPLİTTER","İlave Bina Splitter Kutusu (BSK) Kurulumu/Değişimi/Arıza-Onarım İşçiliği"],placeholder="Bölge Seç")

processed_data = []

if st.button("Kaydet"):
    for line in data.split('\n'):
        parts = line.split("#")
        no = parts[1]
        address = parts[2]
        
        # Extract address components
        mahalle = address.split(" NO: ")[0].replace("MAH.","")

        sokak = mahalle.split()[-2] + " " + mahalle.split()[-1].replace("SK.","").replace("CAD.","")
     
        mahalle = " ".join(mahalle.split()[:-2])
        kapi_no = address.split(" NO: ")[1] if "NO: " in address else ""
        
        description = parts[3]
        
        if "MOBİLİZASYON" in malzemeler:
            malzeme1 = 1
        else:
            malzeme1 = ""    
        if "Bina Sonlandırma Kutusu Kurulumu" in malzemeler:
            malzeme2 = 1
        else:
            malzeme2 = "" 

        if "Bina İç Kutusu" in malzemeler:
            malzeme3 = 1
        else:
            malzeme3 = "" 
        if "1/4 SPLİTTER" in malzemeler:
            malzeme4 = 1
        else:
            malzeme4 = ""
        if "1/8 SPLİTTER" in malzemeler:
            malzeme5 = 1
        else:
            malzeme5 = ""
        if "İlave Bina Splitter Kutusu (BSK) Kurulumu/Değişimi/Arıza-Onarım İşçiliği" in malzemeler:
            malzeme6 = 1
        else:
            malzeme6 = ""


        processed_data.append({"NO":no,"Müdahale Açıklaması": description,"TARİH": tarih,"İLÇE": bolge,"MAHALLE veya SİTE ADI": mahalle, "SOKAK/CADDE":sokak,"DIŞ KAPI NO": kapi_no,"SS.6.1.MOBİLİZASYON":malzeme1,"SS.1.1.Bina Bağlantısı ve Aktivasyonu":"","SS.1.3.Bina Sonlandırma Kutusu Kurulumu":malzeme2,"MM.3.1.Bina İç Kutusu":malzeme3,"MM.2.1.1/4 SPLİTTER":malzeme4,"MM.2.3.1/8 SPLİTTER":malzeme5,"SS.3.4.İlave Bina Splitter Kutusu (BSK) Kurulumu/Değişimi/Arıza-Onarım İşçiliği":malzeme6})

    # Create DataFrame

    df = pd.DataFrame(processed_data)

    st.dataframe(df)

    veri_Giris = pd.DataFrame(
                            [{"NO":no,
                              "Müdahale Açıklaması": description,
                              "TARİH": tarih,
                              "İLÇE": bolge,
                              "MAHALLE veya SİTE ADI": mahalle, 
                              "SOKAK/CADDE":sokak,
                              "DIŞ KAPI NO": kapi_no,
                              "SS.6.1.MOBİLİZASYON":malzeme1,
                              "SS.1.1.Bina Bağlantısı ve Aktivasyonu":"",
                              "SS.1.3.Bina Sonlandırma Kutusu Kurulumu":malzeme2,
                              "MM.3.1.Bina İç Kutusu":malzeme3,
                              "MM.2.1.1/4 SPLİTTER":malzeme4,
                              "MM.2.3.1/8 SPLİTTER":malzeme5,
                              "SS.3.4.İlave Bina Splitter Kutusu (BSK) Kurulumu/Değişimi/Arıza-Onarım İşçiliği":malzeme6}])

    updated_df = pd.concat([paket1liste, veri_Giris], ignore_index=True)
    conn.update(worksheet="Sayfa1", data=updated_df)
