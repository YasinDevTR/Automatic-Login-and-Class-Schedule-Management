import sqlite3
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def veritabani_baglanti_kur():
    return sqlite3.connect('kullanici_verileri.db')

def veritabani_olustur():
    try:
        conn = veritabani_baglanti_kur()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                okul_numarasi TEXT NOT NULL,
                sifre TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dersler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                okul_numarasi TEXT NOT NULL,
                gun TEXT NOT NULL,
                baslangic_saati TEXT NOT NULL,
                bitis_saati TEXT NOT NULL,
                FOREIGN KEY (okul_numarasi) REFERENCES kullanicilar (okul_numarasi)
            )
        ''')
        
        conn.commit()
    finally:
        conn.close()

def kullanici_girdisi_al():
    ad = input("İsim: ")
    okul_numarasi = input("Lütfen giriş için kullandığınız okul numaranızı giriniz: ")
    sifre = input("Şifrenizi giriniz: ")
    return (ad, okul_numarasi, sifre)

def kullanici_ekle(kullanici_verileri):
    try:
        conn = veritabani_baglanti_kur()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO kullanicilar (ad, okul_numarasi, sifre)
            VALUES (?, ?, ?)
        ''', kullanici_verileri)
        
        conn.commit()
    finally:
        conn.close()

def kullanici_dogrula(okul_numarasi, sifre):
    try:
        conn = veritabani_baglanti_kur()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM kullanicilar WHERE okul_numarasi = ? AND sifre = ?', (okul_numarasi, sifre))
        satir = cursor.fetchone()
        
        return satir
    finally:
        conn.close()

def rastgele_giris_saati(baslangic_saati):
    delta = timedelta(minutes=random.randint(-5, 5))
    baslangic_zamani = datetime.strptime(baslangic_saati, "%H:%M:%S")
    rastgele_zaman = baslangic_zamani + delta
    return rastgele_zaman.strftime("%H:%M:%S")

def ders_programi_ekle_guncelle(kullanici_verileri):
    try:
        conn = veritabani_baglanti_kur()
        cursor = conn.cursor()
        
        gun = input("Lütfen tarihi GG/AA/YYYY formatında giriniz: ")
        baslangic_saati = input("Ders Başlangıç Saati (HH:MM:SS formatında): ")
        bitis_saati = input("Ders Bitiş Saati (HH:MM:SS formatında): ")
        
        cursor.execute('''
            INSERT INTO dersler (okul_numarasi, gun, baslangic_saati, bitis_saati)
            VALUES (?, ?, ?, ?)
        ''', (kullanici_verileri[1], gun, baslangic_saati, bitis_saati))
        
        conn.commit()
        print("Ders programı başarıyla eklendi.")
    finally:
        conn.close()

def programi_baslat_takvim(okul_numarasi, sifre):
    try:
        conn = veritabani_baglanti_kur()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT gun, baslangic_saati FROM dersler WHERE okul_numarasi = ?
        ''', (okul_numarasi,))
        ders_verileri = cursor.fetchone()
        
        if not ders_verileri:
            print("Ders programı bulunamadı.")
            return
        
        gun, baslangic_saati = ders_verileri
        rastgele_saati = rastgele_giris_saati(baslangic_saati)
        
        hedef_tarih = datetime.strptime(gun + " " + rastgele_saati, "%d/%m/%Y %H:%M:%S")
        
        while datetime.now() < hedef_tarih:
            time.sleep(30)  # bilgisayarı yormamak için 30sn yede bir çalışıyor
        
        print(f"Program şimdi başlatıldı. Giriş Zamanı: {rastgele_saati}")

        tarayici = webdriver.Chrome()
        tarayici.get('https://ubys.omu.edu.tr/')
        
        WebDriverWait(tarayici, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))).send_keys(okul_numarasi)
        tarayici.find_element(By.XPATH, '//*[@id="password"]').send_keys(sifre)
        tarayici.find_element(By.XPATH, '//*[@id="loginForm"]/div[3]/div[1]/button').click()
        
        time.sleep(15)
        
        tarayici.quit()
    finally:
        conn.close()

def programi_baslat_test(okul_numarasi, sifre):
    print("Program şimdi başlatıldı.")
    
    tarayici = webdriver.Chrome()
   
    tarayici.get('https://ubys.omu.edu.tr/')
    
    WebDriverWait(tarayici, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))).send_keys(okul_numarasi)
    tarayici.find_element(By.XPATH, '//*[@id="password"]').send_keys(sifre)
    tarayici.find_element(By.XPATH, '//*[@id="loginForm"]/div[3]/div[1]/button').click()
    
    time.sleep(15)
    
    tarayici.quit()


def oturumu_kapat():
    print("Oturum kapatıldı.")
    ana_ekran()

def kullanici_paneli(kullanici_verileri):
    while True:
        print("1. Ders Programı Ekle/Güncelle")
        print("2. Programı Takvime Göre Başlat")
        print("3. Programı şimdi başlat (test için)")
        print("4. Oturumu Kapat")
        secim = input("Bir seçenek girin: ")

        if secim == '1':
            ders_programi_ekle_guncelle(kullanici_verileri)
        elif secim == '2':
            programi_baslat_takvim(kullanici_verileri[2], kullanici_verileri[3])
        elif secim == '3':
            programi_baslat_test(kullanici_verileri[2], kullanici_verileri[3])
        elif secim == '4':
            oturumu_kapat()
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

def ana_ekran():
    while True:
        print("1. Giriş Yap")
        print("2. Kayıt Ol")
        secim = input("Bir seçenek girin: ")

        if secim == '1':
            okul_numarasi = input("Okul numaranızı giriniz: ")
            sifre = input("Şifrenizi giriniz: ")
            kullanici_verileri = kullanici_dogrula(okul_numarasi, sifre)
            if kullanici_verileri:
                kullanici_paneli(kullanici_verileri)
            else:
                print("Giriş bilgileri hatalı veya sisteme kayıtlı değilsiniz.")
        elif secim == '2':
            kullanici_verileri = kullanici_girdisi_al()
            kullanici_ekle(kullanici_verileri)
            print("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    veritabani_olustur()
    ana_ekran()

