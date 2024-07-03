from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Meminta pengguna untuk memasukkan URL toko
url = input("Masukkan url toko : ")

if url:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    data = []

    # Definisikan fungsi untuk klik "Selengkapnya"
    def klik_selengkapnya():
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.css-89c2tx")
        for button in buttons:
            try:
                button.click()  # Klik tombol 'Selengkapnya'
                time.sleep(1)  # Tunggu 1 detik untuk memuat ulasan tambahan
            except Exception as e:
                print(f"Error saat mengklik 'Selengkapnya': {str(e)}")

    # Panggil fungsi untuk klik "Selengkapnya" setelah membuka halaman
    klik_selengkapnya()

    for i in range(0, 31):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs={'class': 'css-72zbc4'})

        for container in containers:
            try:
                review = container.find(
                    'span', attrs={'data-testid': 'lblItemUlasan'}).text.strip()
                data.append((review))
            except AttributeError:
                continue

        time.sleep(2)
        try:
            driver.find_element(
                By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
            time.sleep(3)
            klik_selengkapnya()  # Panggil fungsi untuk klik "Selengkapnya" di halaman berikutnya
        except Exception as e:
            print(f"Error saat mengklik halaman berikutnya: {str(e)}")
            break

    print(data)
    df = pd.DataFrame(data, columns=["Ulasan"])
    df.to_csv("Aerostreet4.csv", index=False)

    driver.quit()  # Menutup browser Selenium setelah selesai
