from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def get_weather():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.foreca.com/ru/100619066/Zaslawye-Belarus"
    driver.get(url)

    # Ждём пока появится температура
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.value.temp.temp_c.cold"))
        )
    except:
        print("⚠️ Элемент температуры не найден")

    # Температура
    temps = driver.find_elements(By.CSS_SELECTOR,
        "span.value.temp.temp_c.cold"
    )
    temperature_value = temps[0].text if temps else "нет данных"

    # Влажность
    vlag = driver.find_elements(By.CSS_SELECTOR,
        "div.rhum.center > p > em"
    )
    vlaghnost_value = vlag[0].text if vlag else "нет данных"

    # Температура по ощущениям
    po = driver.find_elements(By.CSS_SELECTOR,
        "div.temp > p:nth-child(2) > span.value.temp.temp_c.cold > em"    
    )
    pojoe_value = po[0].text if po else "нет данных"

    # Восход
    vh = driver.find_elements(By.CSS_SELECTOR,
        "div.row.sun.details > div:nth-child(1) > em > span.value.time.time_24h"
    )
    voshod_value = vh[0].text if vh else "нет данных"

    # Закат
    zah = driver.find_elements(By.CSS_SELECTOR,
        "div.row.sun.details > div.sunset.right > em > span.value.time.time_24h"
    )
    zahod_value = zah[0].text if zah else "нет данных"

    # Длина дня
    sun = driver.find_elements(By.CSS_SELECTOR,
        "div.row.sun.details > div.daylen.center > em"
    )
    sunny_value = sun[0].text if sun else "нет данных"

    driver.quit()
    return temperature_value, vlaghnost_value, pojoe_value, voshod_value, zahod_value, sunny_value


def generate_html(temp, hum, joe, vos, zah, sun):
    html_code = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Сайт с фоном</title>
  <link rel="stylesheet" href="css/gminsk.css">
</head>
<body>
  <img src="images/fonminsk.png" alt="Фон" class="background">
  <div class="content">
    <div class="column">
      <h1 class="centered">ПОГОДА</h1>
      <h1 class="centered">МИНСКАЯ ОБЛАСТЬ</h1>
      <h1>Заславль</h1>
      <ul class="Minsk1">
        <li>Температура: {temp}</li>
        <li>По ощущениям: {joe}</li>
        <li>Влажность: {hum}%</li>
        <li>восход -> {vos} = {sun} = {zah} <- закат</li>
      </ul>
    </div>
  </div>
</body>
</html>
"""

    # Проверка пути
    full_path = os.path.abspath("obl city/Minsk/Zaslavl.html")
    print("📂 Текущая рабочая директория:", os.getcwd())
    print("📄 HTML будет создан по пути:", full_path)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html_code)
    print("✅ HTML обновлён:", full_path)


# Запускаем цикл каждые 60 минут
while True:
    temperature, humidity, pojoe, voshod, zahod, sunny = get_weather()
    generate_html(temperature, humidity, pojoe, voshod, zahod, sunny)
    time.sleep(3600)  # ждать 60 минут
