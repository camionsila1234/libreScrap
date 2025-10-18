import random, time, pandas, openpyxl
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scrape_products(url):
    chrome_driver_path = "chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.minimize_window()

    product_set = set()
    product_list = []

    driver.get(url)
    time.sleep(random.uniform(1, 3))

    products = driver.find_elements(By.CLASS_NAME, "poly-card")

    for product in products:
        try:
            image = product.find_element(By.CLASS_NAME ,"poly-component__picture").get_attribute("data-src") or product.find_element(By.CLASS_NAME, "poly-component__picture").get_attribute("srcset") or product.find_element(By.CLASS_NAME, "poly-component__picture").get_attribute("src")
            title = product.find_element(By.CLASS_NAME, "poly-component__title").text
            price = product.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text.replace(".", "")
            stars = product.find_element(By.CLASS_NAME, "poly-reviews__rating").text
        except:
            continue
        print(Fore.GREEN + "[+] ",image)
        print(Fore.GREEN + "[+] ",title)
        print(Fore.GREEN + "[+] ",price)
        print(Fore.GREEN + "[+] ",stars)
        print("")
        product_set.add(title)
        product_list.append(
            {
                "image": image,
                "title": title,
                "price": price,
                "stars": stars
            }
        )

    write = pandas.DataFrame(product_list)
    write.to_excel("resultados/productos.xlsx", index=False)

    read = pandas.read_excel("resultados/productos.xlsx")
    read["price"] = read["price"].astype(int)

    print(Fore.GREEN + "[+]", Fore.RESET + f"Se han encontrado {len(product_set)} productos y guardados en resultados/productos.xlsx")

    expensive = read["price"].max()
    cheap = read["price"].min()
    total = int(read["price"].mean())

    expensive_fmt = f"{expensive:,}".replace(",", ".")
    cheap_fmt = f"{cheap:,}".replace(",", ".")
    total_fmt = f"{total:,}".replace(",", ".")

    print("")
    print(Fore.GREEN + "[+]",  Fore.RESET + f"El promedio de precios es de {total_fmt}")
    print(Fore.GREEN + "[+]",  Fore.RESET + f"El producto más caro vale: {expensive_fmt}")
    print(Fore.GREEN + "[+]",  Fore.RESET + f"El producto más barato vale: {cheap_fmt}")

    driver.quit()

if 1 == 2:
    scrape_products("https://listado.mercadolibre.com.co/consolas?sb=all_mercadolibre#D[A:consolas]")