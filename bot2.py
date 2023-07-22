import requests
import time


"""Бот присылает картинки с мопсами при отправке любого сообщения и выводит в консоль данные о пользователе"""

api_url : str = 'https://api.telegram.org/bot'
bot_token : str = '6351251112:AAEchaYBDiGbrz0UDicVQP9N_T1ezhB5lqc'
api_pugs: str = 'https://api.thecatapi.com/v1/images/search'
text : str = 'Апдейт'
max_counter : int = 100
timeout : int = 60 # задаю таймаут ожидания обновления для запроса &timeout={timeout}


offset: int = 49193058
counter: int = 0
count : int = 0
chat_id: int
of1 : int = 0

api_pugs : str = 'https://dog.ceo/api/breed/pug/images/random'
pug_up = requests.get(api_pugs).json()
pug_link = pug_up['message']


while counter < max_counter:
    updates = requests.get(f'{api_url}{bot_token}/getUpdates?offset={offset + 1}&timeout={timeout}').json()
    if updates['result']:
        for result in updates['result']:
            #offset = result['update_id']
            of1 = result['update_id']
            if of1 <= offset:
                time.sleep(0)
            else:
                print('atempt = ', count)
                offset = result['update_id']
                chat_id = result['message']['from']['id']
                tt = updates
                pug_up = requests.get(api_pugs)
                if pug_up.status_code == 200:
                    pug_link = pug_up.json()['message']
                    text = result["message"]["text"]
                    requests.get(f'{api_url}{bot_token}/sendPhoto?chat_id={chat_id}&photo={pug_link}&caption=Твое сообщение: {text}\nА еще Влад ПИДОР \U0001F970')
                    first_name = result["message"]["from"]["first_name"]
                    username = result["message"]["from"]["username"]
                    idch = result["message"]["from"]["id"]
                    date = result["message"]["date"]
                    print(f'Имя - {first_name} \nНикнейм = {username}\nID чата = {idch}\nТекст сообщения - {text}\nДата отправки в UNIX - {date}')
                counter += 1
                count += 1
                offset = of1
                print(f'id обновления {of1}')

