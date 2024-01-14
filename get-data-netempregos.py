import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import subprocess
import sys

def buscar_e_comparar_strings(url, string_alvo_texto):
    # Realiza requisição HTTP para pegar o conteúdo da página
    response = requests.get(url)

    # Realiza a verificação da requisição (código de status 200)
    if response.status_code == 200:
        # Parseia o HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Converte a string alvo de texto para minúsculas (Para que a busca não seja sensitiva)
        string_alvo_texto_lower = string_alvo_texto.lower()

        # Encontra o elemento que contém a string alvo de texto
        elemento_com_string_alvo = soup.find(text=re.compile(rf'\b{re.escape(string_alvo_texto_lower)}\b', re.I))

        # Se o elemento for encontrado, exibe a mensagem correspondente
        if elemento_com_string_alvo:
            print('Que ótimo!')
            print(f'Encontramos um anúncio da "{string_alvo_texto}" no site!')

            # Procura por strings que correspondam a variações de nn-n-nnnn dentro da mesma <ul>
            padrao_data = re.compile(r'\b\d{1,2}-\d{1,2}-\d{2,4}\b')
            ul_pai = elemento_com_string_alvo.find_parent('ul')
            elementos_data = ul_pai.find_all(text=padrao_data)

            if elementos_data:
                for elemento_data in elementos_data:
                    # Extrai a data do texto dentro do elemento
                    data_texto = elemento_data.strip()

                    try:
                        # Converte a string de data para um objeto datetime
                        data_elemento = datetime.strptime(data_texto, '%d-%m-%Y')

                        # Obtém a data atual (apenas ano, mês e dia)
                        data_atual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

                        # Compara as datas
                        if data_elemento == data_atual:
                            print(f'E a vaga foi anunciada hoje!')
                            
                            # Executa o script send-mail.py se a data for igual à data atual
                            subprocess.run([sys.executable, '/home/felipe/python-scripts/send-mail.py'])
                            
                        elif data_elemento < data_atual:
                            print(f'Mas a vaga foi anunciada em {data_texto}.')

                    except ValueError:
                        print(f'Formato de data inválido para o elemento: "{data_texto}"')

            else:
                print('Nenhum elemento encontrado com o formato nn-n-nnnn dentro desta <ul>.')

        else:
            print(f'Infelizmente não encontramos nenhum anúncio de "{string_alvo_texto}"no site.')

    else:
        print(f'Falha ao obter a página. Código de status: {response.status_code}')




# Exemplo de uso
url_da_pagina = 'https://www.net-empregos.com/empregos-leiria-informatica-redes.asp?categoria=37&zona=11'
string_alvo_texto = 'apolonia'
resultado = buscar_e_comparar_strings(url_da_pagina, string_alvo_texto)



# Verifica se o resultado é 'Vaga anunciada hoje!' antes de executar o segundo script
if resultado == 'Vaga anunciada hoje!':
    subprocess.run([sys.executable, '/usr/local/python-scripts/send-mail.py'])
