#!/usr/bin/env python3

""""
Set parametro impressora zebra zd220~230

Script acessa a impressora pelo navegador, verifica os parametros, registra
e faz a troca para o definido

# python set_default-zebra.py ip larg.impr larg.max

$ python set_default-zebra.py 192.168.16.238 831 3048

"""

__version__ = "0.1.1"
__author__ = "Myke A. Bueno"
__license__ = "Unlicense"

import sys
import os
import logging
from logging import handlers
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
log = logging.Logger("set_default-zebra.py", log_level)
fh = handlers.RotatingFileHandler(
    "set_default-zebra-log.log",
    maxBytes=10**7, # tamanho = 10MB
    backupCount=10
)
fh.setLevel(log_level)
fmt = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s '
    'l:%(lineno)s f:%(filename)s: %(message)s'
)
fh.setFormatter(fmt)
log.addHandler(fh)

path = os.curdir
filepath = os.path.join(path, "set-default-zebra.txt")

arguments = sys.argv[1:]

info = {
    "ip": None,
    "larg.impr": None,
    "larg.max": None
    }

try:
    info = {
        "ip": arguments[0],
        "larg.impr": arguments[1],
        "larg.max": arguments[2]
    }
except IndexError as e:
    try:
        info = {
            line.split("=")[0]: line.split("=")[1].strip()
            for line in open(filepath, encoding="UTF-8")
            if "=" in line
        }
    except FileNotFoundError as e:
        for key in info:
            try:
                info[key] = str(input(f"Qual {key}: ").strip())
            except:
                log.error("[ERROR] -> %s")
                sys.exit(1)


with open(filepath, "w", encoding="UTF-8") as file_:
    for key, value in info.items():
        file_.write(f"{key}={value}\n")
    file_.close()


try:
    while True:
        # Config Selenium -------------------------------
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Comente essa linha para acompanhar
        navegador = webdriver.Chrome(options=options)
        # -----------------------------------------------

        # Limpar tela
        os.system('cls' if os.name == "nt" else 'clear')

        try:
            print(f"Acessando: {info['ip']}")
            navegador.get(f"http://{info['ip']}/setmed")
            sleep(2)
        except KeyboardInterrupt as e:
            log.error("ERROR: KeyboardInterrupt")
        except:
            log.error("PAGE NOT FOUNT: http://%s/setmed", info['ip'])
            sys.exit(1)

        try: 
            # Preencher o BOX senha
            navegador.find_element("xpath",
                                "/html/body/div/form/p[1]/input").send_keys("1234")
            sleep(1)

            # Clicar no box da senha
            navegador.find_element("xpath",
                                "//html/body/div/form/p[2]/input").click()
            sleep(1)

            # entro novamente no site
            navegador.get(f"http://{info['ip']}/setmed")
            sleep(1)
        except:
            pass
            

        try:
            # Limpar o BOX LARG.IMPRES.
            navegador.find_element("xpath",
                                "/html/body/div/form/p[5]/input").send_keys(Keys.BACKSPACE*3)
            sleep(1)

            # Preencher o BOX LARG.IMPRES.
            print(f"Alterando a larg.impr para: {info['larg.impr']}")
            navegador.find_element("xpath",
                                "/html/body/div/form/p[5]/input").send_keys(info['larg.impr'])
            sleep(1)

            # Limpar o BOX LARG.MAX.
            navegador.find_element("xpath",
                                "/html/body/div/form/p[6]/input").send_keys(Keys.BACKSPACE*4)
            sleep(1)

            # Preencher o BOX LARG.MAX.
            print(f"Alterando a larg.max para: {info['larg.max']}")
            navegador.find_element("xpath",
                                "/html/body/div/form/p[6]/input").send_keys(info['larg.max'])
            sleep(1)

            # Clicar no box de 'submeter alterações'
            navegador.find_element("xpath",
                                "/html/body/div/form/p[7]/input").click()
            print("Default realizado com sucesso!")
            print("Encerrando o Script!!!")
            sleep(2)
        except KeyboardInterrupt as e:
            print("Parando o script!")
            sys.exit(1)
        
        except:
            log.error("Error when modifying attributes", info['ip'])
        navegador.close()
        sleep(5)

except KeyboardInterrupt as e:
    print("Reiniciando o Script!")
    sys.exit(1)
