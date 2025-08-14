
import webbrowser
from dotenv import load_dotenv
load_dotenv()
import os
GOOGLE_GEMİNİ=os.getenv("GOOGLE_GEMİNİ")
key=os.getenv("key")
import yfinance as yf
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
from sklearn.linear_model import LinearRegression
import google.generativeai as genai
from google import genai
plt.style.use("seaborn-v0_8-darkgrid")
tarih=datetime.datetime.now()
def logla(mesaj):
    with open("hata_dosyam.txt","a+",encoding="utf-8") as file:
        file.write("\n" + " " + "Tarih" + " " + ":" + " " +  str(tarih) + " "  + "," + " " + "Hata Mesajı" + " " + ":" + " " + mesaj + " " + "\n")
class System:
    def __init__(self):
        try:
            self.df=pd.read_csv("C:/Users/emre_/Downloads/malitablo (1).csv")
        except Exception as e:
            raise RuntimeError(f"Dosya Okunamadı : {e}")
    def cari_oran(self,tarih="2025/6"):
        dönen_varlıklar=self.df[tarih][1]
        kısa_vadeli_yükümlülükler=self.df[tarih][31]
        cari_oran_değeri=dönen_varlıklar/kısa_vadeli_yükümlülükler
        print(f"Şirketin Cari Oran Değeri : {cari_oran_değeri}")
        return cari_oran_değeri
    def cari_oran_değerlendirme(self,cari_oran_değeri):
        if cari_oran_değeri<1:
            print("Yetersiz Cari Oran,Şirket Kısa Vadeli Borçlarını Ödeyemez")
        elif 1<=cari_oran_değeri<=1.5:
            print("Cari Oran Riskli, Dikkatli Kontrol Edilmeli!")
        else:
            print("Yüksek Cari Oran, Şirket Borçlarını Rahat Ödeyebilir!")
    def grafik_göster(self,cari_oran_değeri,ortalama_değer=1.5):
        labels=["Ortalama Değer","Cari Oran Değeri"]
        oran=[ortalama_değer,cari_oran_değeri]
        plt.bar(labels,oran,color="Red",linewidth=3)
        plt.title("CARİ ORAN ve SEKTÖR ORTALAMASI",color="Black",fontsize=20)
        plt.grid(True)
        plt.show()
    def cari_oran_tahmin(self,tahmin_edilecek_dönem=1):
        tarihler = ['2024/9', '2024/12', '2025/3', '2025/6']
        cari_oranlar = []
        for tarih in tarihler:
            try:
                oran = self.cari_oran(tarih)
                cari_oranlar.append(oran)
            except:
                continue
        X = np.arange(len(cari_oranlar)).reshape(-1, 1)
        y = np.array(cari_oranlar)
        model=LinearRegression()
        model.fit(X, y)
        tahmin_noktası=len(cari_oranlar) + tahmin_edilecek_dönem -1
        tahmin=model.predict([[tahmin_noktası]])[0]
        print(f"Tahmini Cari Oran Değeri : {tahmin}")
        return tahmin
    def likidite_oranı(self,tarih="2025/6"):
        dönen_varlıklar = self.df[tarih][1]
        kısa_vadeli_yükümlülükler = self.df[tarih][31]
        stoklar=self.df[tarih][8]
        likidite_oranı=(dönen_varlıklar-stoklar)/kısa_vadeli_yükümlülükler
        print(f"Şirketin Likidite Oranı : {likidite_oranı}")
        return likidite_oranı
    def likidite_oranı_değerlendirme(self,likidite_oranı):
        if likidite_oranı<1:
            print("Riskli, likidite problemi")
        elif 1<=likidite_oranı<=1.5:
            print("Kabul edilebilir, sağlıklı")
        elif 1.5<likidite_oranı<=2.0:
            print("	İyi, dengeli")
        else:
            print("Çok yüksek, sermaye verimsiz")
    def likidite_grafik(self,likidite_oranı):
        labels=["Sektör Ortalaması","Şirket"]
        oranlar=[1.2,likidite_oranı]
        plt.bar(labels,oranlar,linewidth=3,color="Black")
        plt.title("LİKİDİTE ORANI ve SEKTÖR ANALİZİ",fontsize=20)
        plt.grid(True)
        plt.show()
    def likidite_tahmin(self,tahmin_edilecek_dönem=1):
        tarihler = ['2024/9', '2024/12', '2025/3', '2025/6']
        likidite_oranları=[]
        for tarih in tarihler:
            try:
                l_oran=self.likidite_oranı(tarih)
                likidite_oranları.append(l_oran)
            except:
                continue
        X=np.arange(len(likidite_oranları)).reshape(-1,1)
        Y=np.array(likidite_oranları)
        model=LinearRegression()
        model.fit(X,Y)
        tahmin_noktası=len(likidite_oranları)+tahmin_edilecek_dönem-1
        tahmin=model.predict([[tahmin_noktası]])[0]
        print(f"Tahmin Edilen Likidite Oranı : {tahmin}")
        return tahmin
    def finansal_kaldıraç_oranı(self,tarih="2025/6"):
        toplam_borç=self.df[tarih][31]+self.df[tarih][45]
        özsermaye_oranı=self.df[tarih][58]
        finansal_kaldıraç=toplam_borç/özsermaye_oranı
        print(f"Şirketin Finansal Kaldıraç Oranı : {finansal_kaldıraç}")
        return finansal_kaldıraç
    def finansal_kaldıraç_sektör_analizi(self,finansal_kaldıraç_oranı):
        if finansal_kaldıraç_oranı<0.5:
            print("Şirket borç yükü düşük, finansal risk az, ama büyüme potansiyeli sınırlı olabilir.")
        elif 0.5<=finansal_kaldıraç_oranı<=1.5:
            print("Dengeli borç kullanımı. Hem büyüme için finansman sağlanıyor, hem risk yönetilebilir.")
        else:
            print(" Risk yüksek, borçlanma maliyeti ve iflas riski artar. Şirket gelirlerinde dalgalanma varsa tehlikeli olabilir.")
    def finansal_kaldıraç_grafik(self,finansal_kaldıraç):
        labels=["Sektör Ortalaması","Şirketin Değeri"]
        oranlar=[1.5,finansal_kaldıraç]
        plt.bar(labels,oranlar,color="Yellow",linewidth=3)
        plt.title("FİNANSAL KALDIRAÇ ORANININ İNCELENMESİ",color="Black",fontsize=20)
        plt.grid(True)
        plt.show()
    def finansal_kaldıraç_tahmin(self,tahmin_edilecek_dönem=1):
        tarihler=["2025/6","2025/3","2024/12","2024/9"]
        finansal_kaldıraçlar=[]
        for tarih in tarihler:
            try:
                f_oran=self.finansal_kaldıraç_oranı(tarih)
                finansal_kaldıraçlar.append(f_oran)
            except:
                continue
        X=np.arange(len(finansal_kaldıraçlar)).reshape(-1,1)
        Y=np.array(finansal_kaldıraçlar)
        model=LinearRegression()
        model.fit(X,Y)
        tahmin_noktası=len(finansal_kaldıraçlar)+tahmin_edilecek_dönem-1
        tahmin=model.predict([[tahmin_noktası]])[0]
        print(f"Bir Sonraki Dönem İçin Tahmin Edilen Finansal Kaldıraç Oranı : {tahmin}")
        return tahmin
    def roe_oranı(self,tarih="2025/6"):
        net_kar=self.df[tarih][67]
        özsermaye=self.df[tarih][58]
        roe_değeri=(net_kar/özsermaye)*1000
        print(f"Şirketin ROE değeri : %{roe_değeri}")
        return roe_değeri
    def roe_oranı_analiz(self,roe_değeri):
        if roe_değeri<10:
            print("Orta seviye, sektör bağımlı,Daha detaylı analiz gerekli")
        elif 10<=roe_değeri<=15:
            print("İyi performans,Genellikle yatırım için cazip")
        elif 15 < roe_değeri<=25:
            print("Çok iyi, güçlü kârlılık,Uyarı:Sektör ortalamasına göre kontrol")
        else:
            print("Aşırı yüksek, kaldıraç veya spekülatif olabilir,Detaylı finansal inceleme zorunlu")
    def roe_grafik(self,roe_değeri):
        labels=["Sektör Ortalaması","Şirket"]
        oranlar=[10,roe_değeri]
        plt.bar(labels,oranlar,color="Orange",linewidth=3)
        plt.grid(True)
        plt.title("ROE ORANININ İNCELENMESİ",color="Black",fontsize=20)
        plt.show()
    def roe_tahmin(self,tahmin_edilecek_dönem=1):
        tarihler=["2025/6","2025/3","2024/12","2024/9"]
        oranlar=[]
        for tarih in tarihler:
            try:
                roe_değeri=self.roe_oranı(tarih)
                oranlar.append(roe_değeri)
            except:
                continue
        X=np.arange(len(tarihler)).reshape(-1,1)
        Y=np.array(oranlar)
        model=LinearRegression()
        model.fit(X,Y)
        tahmin_noktası=len(oranlar)+tahmin_edilecek_dönem-1
        tahmin=model.predict([[tahmin_noktası]])[0]
        print(f"Bir Sonraki Çeyrek İçin ROE Tahminimiz : %{tahmin}")
        return tahmin
class YardımcıAraçlar:
    def yapay_zeka(self):
        mesaj = input("Bir Mesaj Gönderin : ")
        print("Gemini cevap hazırlıyor...")
        time.sleep(1)
        client = genai.Client(api_key=GOOGLE_GEMİNİ)
        cevap = client.models.generate_content(model="gemini-2.5-flash", contents=mesaj)
        print(f"Gemini Cevap : {cevap.text}")
        return cevap.text
    def dolar_tl(self):
        url = f"https://v6.exchangerate-api.com/v6/{key}/latest/USD"
        cevap = requests.get(url=url)
        if cevap.status_code == 200:
            data = cevap.json()
            print(f"1 Dolar : {data['conversion_rates']['TRY']} TL'dir")
        else:
            print("API servisine ulaşılamadı , Daha sonra tekrar deneyin ! ")
    def borsa_haber(self):
        url = "https://tr.investing.com/news/economy"
        print("Investing.com borsa haberleri sayfası açılıyor...")
        webbrowser.open(url)  # Varsayılan tarayıcıda aça
    def borsa_tahmin(self):
        sembol_al = input("Merak  Ettiğiniz Şirketin Hisse Kodunu Giriniz : ")
        df = yf.download(sembol_al, period="30d", interval="1d")
        kapanış = df["Close"].dropna().reset_index(drop=True)
        X = np.array(range(len(kapanış))).reshape(-1, 1)
        Y = kapanış.values.reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, Y)
        tahmin_noktası = len(kapanış) + 1
        tahmin = model.predict(([[tahmin_noktası]]))[0]
        print(f"{sembol_al} Şirketinin Yarınki Tahmini Değeri : {tahmin} TL'dir.")

sistem=System()
yardımcı_araç=YardımcıAraçlar()
def main():
    print("Bilanço Analiz Sistemine Hoşgeldiniz!")
    print("Yapabilecekleriniz:\n1=Cari Oran Analizi\n2=Likidite Oranı Analizi\n3=Finansal Kaldıraç Analizi\n4=ROE Oranı Analizi\n5=Yardımcı Araçlarımız\n6=Sistemden Çıkış".center(120,"*"))
    while True:
        try:
            seçim=int(input("Yapmak İstediğiniz İşlemin Numarasını Giriniz : "))
            if seçim==1:
                print("Cari Oran Analizi Bölümüne Hoşgeldiniz!")
                print("Yapılabilecekler:\n1=Cari Oran Hesapla\n2=Cari Oran Sektör Karşılaştırması\n3=Cari Oran Grafik\n4=Bir Sonraki Dönem için Cari Oran Tahminimiz")
                try:
                    decision=int(input("Yapmak İstediğiniz İşlemin Numarasını Giriniz : "))
                    if decision==1:
                        sistem.cari_oran()
                    elif decision==2:
                        cari_oran_değeri=sistem.cari_oran()
                        değerlendirme=sistem.cari_oran_değerlendirme(cari_oran_değeri)
                        print(değerlendirme)
                    elif decision==3:
                        cari_oran_değeri=sistem.cari_oran()
                        sistem.grafik_göster(cari_oran_değeri)
                    elif decision==4:
                        sistem.cari_oran_tahmin()
                except ValueError as v:
                    print(f"Hata Kodu : {v} , Lütfen Belirtilen İşlem Değerini Giriniz!")
                    logla("Kullanıcı Belirtilen İşlem Değerini Girmedi")
            elif seçim==2:
                print("Likidite Oranı Analizi Bölümüne Hoşgeldiniz!")
                print("Yapılabilecekler:\n1=Likidite Oran Hesapla\n2=Likidite Oran Sektör Karşılaştırması\n3=Likidite Oran Grafik\n4=Bir Sonraki Dönem için Likidite Oran Tahminimiz")
                try:
                    qwe=int(input("Yapmak İstediğiniz İşlemin Numarasını Giriniz : "))
                    if qwe==1:
                        sistem.likidite_oranı()
                    elif qwe==2:
                        likidite_oranı=sistem.likidite_oranı()
                        print(sistem.likidite_oranı_değerlendirme(likidite_oranı))
                    elif qwe==3:
                        likidite_oranı = sistem.likidite_oranı()
                        sistem.likidite_grafik(likidite_oranı)
                    elif qwe==4:
                        sistem.likidite_tahmin()
                except ValueError as q:
                    print(f"Hata Kodu : {q} , Lütfen Belirtilen İşlem Değerini Giriniz!")
                    logla("Kullanıcı Belirtilen İşlem Değerini Girmedi")
            elif seçim==3:
                print("Finansal Kaldıraç Analizi Bölümüne Hoşgeldiniz!")
                print("Yapabilecekleriniz:\n1=Finansal Kaldıraç Oranı Hesapla\n2=Finansal Kaldıraç Sektör Karşılaştırması\n3=Finansal Kaldıraç Grafik\n4=Bir Sonraki Dönem için Finansal Kaldıraç Oran Tahminimiz")
                try:
                    ert=int(input("Yapmak İstediğiniz İşlemin Numarasını Giriniz : "))
                    if ert==1:
                        sistem.finansal_kaldıraç_oranı()
                    elif ert==2:
                        finansal_kaldıraç=sistem.finansal_kaldıraç_oranı()
                        print(sistem.finansal_kaldıraç_sektör_analizi(finansal_kaldıraç))
                    elif ert==3:
                        finansal_kaldıraç=sistem.finansal_kaldıraç_oranı()
                        sistem.finansal_kaldıraç_grafik(finansal_kaldıraç)
                    elif ert==4:
                        sistem.finansal_kaldıraç_tahmin()
                except ValueError as e:
                    print(f"Hata Kodu : {e} , Lütfen Belirtilen İşlem Değerini Giriniz!")
                    logla("Kullanıcı Belirtilen İşlem Değerini Girmedi")
            elif seçim==4:
                print("ROE Oranı Analizi Bölümüne Hoşgeldiniz!")
                print("Yapabilecekleriniz:\n1=ROE Oranı\n2=ROE Sektör Analizi\n3=ROE Grafik\n4=Bir Sonraki Çeyrek için ROE Tahminimiz")
                try:
                    rty=int(input("Yapmak İstediğiniz İşlemin Numarasını Giriniz : "))
                    if rty==1:
                        sistem.roe_oranı()
                    elif rty==2:
                        roe_oranı=sistem.roe_oranı()
                        print(sistem.roe_oranı_analiz(roe_oranı))
                    elif rty==3:
                        roe_oranı=sistem.roe_oranı()
                        sistem.roe_grafik(roe_oranı)
                    elif rty==4:
                        sistem.roe_tahmin()
                except Exception as t:
                    print(f"Hata Kodu : {t} ,  Lütfen Belirtilen İşlem Numaralarını Giriniz!")
                    logla("Kullanıcı Belirtilen İşlem Değerini Girmedi")
            elif seçim==5:
                print("Yardımcı Araçlar Bölümüne Hoşgeldiniz")
                print("Yapabilecekleriniz:\n1=Gemini ile Sohbet\n2=Dolar/TL Fiyat Bilgisi\n3=Investing ile Ekonomi Haberleri\n4=Hisse Fiyat Tahmini")
                try:
                    yuı=int(input("Yapmak İstediğiniz İşlemin Numarasını Giriniz : "))
                    if yuı==1:
                        yardımcı_araç.yapay_zeka()
                    elif yuı==2:
                        yardımcı_araç.dolar_tl()
                    elif yuı==3:
                        yardımcı_araç.borsa_haber()
                    elif yuı==4:
                        yardımcı_araç.borsa_tahmin()
                except Exception as g:
                    print(f"Hata Kodu : {g} , Lütfen Belirtilen İşlem Değerlerini Giriniz!")
                    logla("Kullanıcı Belirtilen İşlem Değerini Girmedi")
            elif seçim==6:
                print("Sistemden Çıkılıyor...")
                time.sleep(2)
                print("Sistemden Başarıyla Çıkıldı!")
                quit()
        except ValueError as w:
            print(f"Hata Kodu : {w} , Lütfen Belirtilen İşlem Değerini Giriniz!")
            logla("Kullanıcı Belirtilen İşlem Değerini Girmedi")
if __name__ == "__main__":
    main()







































































































































































































































