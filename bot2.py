import requests
import time


api_url : str = 'https://api.telegram.org/bot'
bot_token : str = '6351251112:AAEchaYBDiGbrz0UDicVQP9N_T1ezhB5lqc'
api_cats: str = 'https://api.thecatapi.com/v1/images/search'
text : str = 'Апдейт'
max_counter : int = 100


offset: int = 49193058
counter: int = 0
count : int = 0
chat_id: int
of1 : int = 0

api_cats : str = 'https://dog.ceo/api/breed/pug/images/random'
cat_up = requests.get(api_cats).json()
cat_link = cat_up['message']
print(cat_link)


while counter < max_counter:
    #print('atempt = ', counter)
    updates = requests.get(f'{api_url}{bot_token}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        for result in updates['result']:
            #offset = result['update_id']
            of1 = result['update_id']
            if of1 <= offset:
                text.sleep(2)
            else:
                print('atempt = ', count)
                offset = result['update_id']
                chat_id = result['message']['from']['id']
                tt = updates
                cat_up = requests.get(api_cats)
                if cat_up.status_code == 200:
                    cat_link = cat_up.json()['message']
                    requests.get(f'{api_url}{bot_token}/sendPhoto?chat_id={chat_id}&photo={cat_link}&caption=Влад ПИДОР \U0001F970')
                    first_name = result["message"]["from"]["first_name"]
                    username = result["message"]["from"]["username"]
                    text = result["message"]["text"]
                    date = result["message"]["date"]
                    print(f'Имя - {first_name} \nНикнейм = {username}\nТекст сообщения - {text}\nДата отправки в UNIX - {date}')
                    #print(f'Имя - {first_name} /n ')
                counter += 1
                count += 1
                offset = of1
                print(of1)
    time.sleep(1)
    #counter += 1
