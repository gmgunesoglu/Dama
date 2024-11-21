def selam_ver(isim):
    return f"Merhaba, {isim}!"

def fonksiyonu_cagir(fonksiyon, arg):
    return fonksiyon(arg)

# selam_ver fonksiyonunu, fonksiyonu_cagir fonksiyonuna gönderiyoruz
sonuc = fonksiyonu_cagir(selam_ver, "Ali")
print(sonuc)  # Çıktı: Merhaba, Ali!
