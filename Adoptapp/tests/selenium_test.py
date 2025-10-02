from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Ruta al ejecutable de Opera
opera_path = r"C:\Users\lENOVO\Desktop\chrome-win64\chrome.exe"  # Cambia esto a la ruta correcta

# Ruta al ChromeDriver (el que bajaste)
driver_path = r"C:\Users\lENOVO\Desktop\chromedriver.exe"

# Configuración para Opera
options = webdriver.ChromeOptions()
options.binary_location = opera_path   # 👈 le decimos que use Opera

# Servicio apuntando a chromedriver.exe
service = Service(driver_path)

# Creamos el navegador
driver = webdriver.Chrome(service=service, options=options)

try:
    # Abre la página de login de tu app
    driver.get("http://127.0.0.1:8000/login/")
    print("Título de la página:", driver.title)

    # Buscar campos y rellenar
    email_input = driver.find_element(By.NAME, "username")  # si tu form usa "email", cámbialo
    password_input = driver.find_element(By.NAME, "password")

    email_input.send_keys("valerialucia1998@gmail.com")
    password_input.send_keys("123456")A
    password_input.send_keys(Keys.RETURN)

    email_input = driver.find_element(By.NAME, "username")  # o el campo correcto
    print("✔ Campo de usuario encontrado")
    
    password_input = driver.find_element(By.NAME, "password")
    print("✔ Campo de contraseña encontrado")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    print("✔ Botón de login encontrado")

except Exception as e:
    print("❌ Error:", e)


finally:
    driver.quit()
