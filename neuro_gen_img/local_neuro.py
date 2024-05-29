import time
import base64
import requests
from random import randint
# Данный код модернизирован циклом который не дает терминалу завершать работу
# И генерировать картинки с новым именем каждый раз увеличивая счётчик, чтобы исходное изображение сохранялось
# с новым именем не перезаписывая постоянно один и тот же файл
# А также записывать картинки в папку pictures лежашей в одном каталоге с исполняемым файлом
# Инициализация счетчика
image_counter = 1

while True:
    message = input('\n\nПривет!\n\nЧто рисуем сегодня?\n\nВведите запрос:\t')

    prompt = {
        "modelUri": "art://b1g3f13cj7d6d3ss2md9/yandex-art/latest",
        "generationOptions": {
            "seed": randint(20000, 40000000)
        },
        "messages": [
            {
                "weight": 1,
                "text": message
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN1cZPDuaKqCCvn2KuJJ51xXP_QOv_Cm0_YFu8"
    }

    response = requests.post(url=url, headers=headers, json=prompt)
    result = response.json()
    print(result)

    operation_id = result['id']
    operation_url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"

    while True:
        operation_response = requests.get(url=operation_url, headers=headers)
        operation_result = operation_response.json()
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)

            # Формирование уникального имени файла
            image_filename = f"neuro_gen_img/pictures/image{image_counter}.jpeg"

            # Сохранение картинки
            with open(image_filename, 'wb') as image_file:
                image_file.write(image_data)


            # Увеличение счетчика
            image_counter += 1
            break
        else:
            print('\nОжидайте картинку, скоро будет!')
            time.sleep(5)

    print(f'\nИзображение сохранено как {image_filename} в корневой директории')
