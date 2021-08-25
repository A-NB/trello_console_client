"""
Консольное приложение для управления доской на сайте trello.com при помощи API Trello.
Основные возможности:
- получение информации обо всех карточках во всех колонках доски;
- создание новой колонки;
- создание новой карточки;
- перемещение карточки из одной колонки в другую;
- удаление карточки из колонки;
- удаление колонки (на самом деле колонка перемещается в архив из-за ограничений на сайте trello.com).

Для работы приложения необходимо иметь валидные ключ и токен. Для получения токена нужно зарегистрироваться на сайте trello.com.
После регистрации будет создана доска, для работы с которой предназначено это консольное приложение. Сохраните её id в файл
"Доска1_trello.txt" (id доски можно увидеть в адресной строке браузера, например: https://trello.com/b/HDns2wVz/доска1. Здесь HDns2wVz
и есть нужный id доски). После этого нужно перейти на trello.com/app-key, согласиться с условиями пользования и нажать "Показать API ключ".
Сохраните ключ, который указан в поле "Ключ", в файл "Trello_Key.txt". Кроме этого, необходимо сгенерировать токен на основе этого ключа.
Для этого нужно перейти по ссылке на слове "токен", потом нажать внизу на кнопку "Разрешаю". Сохраните сгенерированный токен в файл
"Trello_Token.txt". Если все три файла сохранены в той же директории, где и этот файл trello.py, то в путях к файлам уберите символы
../ (их можно оставить, если файлы находятся в родительской по отношению к файлу trello.py директории).

~~~ Автор: A-NB (https://github.com/A-NB) 2021 год ~~~

"""
import sys 
import requests 

base_url = "https://api.trello.com/1/{}"

""" Считываем ключ доступа к API Trello из файла (если он в той же директории, уберите ../) """
with open('../Trello_Key.txt') as f:
    key = f.read()

""" Считываем токен для работы с API Trello из файла (если он в той же директории, уберите ../) """
with open('../Trello_Token.txt') as f:
    token = f.read()

""" Параметры авторизации """
auth_params = {    
    'key': key,
    'token': token,}

""" Считываем id доски на сайте trello.com, с которой мы будем работать, из файла (если он в той же директории, уберите ../) """
with open('../Доска1_trello.txt') as f:
    board_id = f.read()

""" Получение информации о колонках. """
def get_column_data():  
    # Получим данные всех колонок на доске:
    return requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json() 

""" Чтение и вывод информации обо всех имеющихся на доске колонках и карточках в них. """
def read():      
    # Получим данные всех колонок на доске:      
    column_data = get_column_data()
    # Получим название доски:
    board_name = requests.get(base_url.format('boards')+ '/' + board_id, headers = {"Accept": "application/json"}, params=auth_params).json()['name']
    s = f"На доске '{board_name}' найдено {len(column_data)} колонок:"
    print(f"{s}\n{'-' * len(s)}")
    # Для каждой колонки ... 
    for i in range(len(column_data)):      
        # ... получим данные всех карточек в колонке, ...
        card_data = requests.get(base_url.format('lists') + '/' + column_data[i]['id'] + '/cards', params=auth_params).json() 
        # ... выведем в консоль для каждой колонки её название и количество карточек в ней:
        print(f"{i + 1}) В колонке '{column_data[i]['name']}' количество карточек = {str(len(card_data))}:")
        # Если в колонке нет карточек, ...
        if not card_data: 
            # ... выведем соответствующее сообщение:     
            print(f"{' ' * len(str(i + 1) + ' )')}Нет карточек!")
            continue
        # Для непустых колонок выводим названия всех имеющихся в них карточек:      
        for j in range(len(card_data)): 
            print(f"{' ' * len(str(i + 1) + ' )')}{j + 1}. {card_data[j]['name']}")        

""" Поиск колонки по имени. Функция возвращает список из двух значений: id колонки и её названия. """            
def find_column(column_name, action = 'использовать'):
    column_data = get_column_data()
    columns_list = [] # Список списков для хранения данных о найденных колонках в формате:
                      # [id колонки, имя колонки, её порядковый номер на доске]
    for i in range(len(column_data)):
        if column_data[i]['name'].lower() == column_name.lower():
            columns_list.append(
                                 [
                                  column_data[i]['id'], 
                                  column_data[i]['name'],
                                  i + 1
                                 ]
                                )
    if len(columns_list) > 1: # Если найдено более одной колонки с именем column_name, ...
        # ... выводим в консоль информацию о количестве всех найденных колонок ...
        s = f"Найдено колонок с именем '{column_name}': {str(len(columns_list))}"
        print(f"{s}\n{'-' * len(s)}")
        for i in range(len(columns_list)):
            # ... и перечисляем их в виде нумерованного списка:
            print(f"{str(i + 1)}: '{columns_list[i][1]}' (позиция на доске: {columns_list[i][2]} из {len(column_data)})")
        # Предлагаем пользователю выбрать номер нужной колонки или "передумать":
        s = f"Введите с клавиатуры номер той колонки, которую Вы хотите {action}"
        print(f"{'-' * len(s)}\n{s}\n(для отмены введите латиницей символ 'q'):")
        # Предотвращаем ввод неправильных данных:
        while True:
            try: # Пробуем получить от пользователя с клавиатуры номер колонки и выбрать в списке нужный id:
                enter = input()
                if int(enter) in range(1, len(columns_list)+1):
                    column_id, column_name = columns_list[int(enter) - 1][:2]
                else:
                    raise ValueError # Несуществующий номер
            except: # При неправильном вводе - несуществующий номер или не число (кроме 'q') - выводим в консоль сообщение об ошибке:
                if enter in ['q', 'Q', 'й', 'Й']: # При вводе 'q' выходим из программы:
                    return [None, None]
                else:
                    print("Необходимо ввести номер колонки из списка. Попробуйте снова\n(для отмены введите латиницей символ 'q'):")
            else: # При правильном вводе идём дальше.
                break
    elif len(columns_list) == 1: # Если найдена только одна колонка с именем column_name, ...
        # ... запоминаем её id и название:
        column_id, column_name = columns_list[0][:2]
    else: # Если не найдено ни одной колонки с именем column_name, ...
        print(f"Колонка с именем '{column_name}' не обнаружена :(")
        return [None, None] # ... выходим из программы.
    return [column_id, column_name]

""" Создание колонки (она становится последней). Для выбора другой позиции измените параметр 'pos' (см. документацию Trello API). """
def create_column(column_name):
    requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': get_column_data()[0]['idBoard'], 'pos': 'bottom', **auth_params})
    print(f"Новая колонка '{column_name}' успешно создана!") 

""" Перемещение колонки внутри доски (в API Trello нет такой функции) """
def move_column(name): # position): # ???
    pass 

""" Удаление колонки (функция реализует только архивирование, поскольку в API Trello возможность удаления не предусмотрена). """
def remove_column(par_colunm_name):
    column_id, column_name = find_column(par_colunm_name, 'переместить в архив')
    if column_id:
        requests.put(base_url.format('lists') + '/' + column_id + '/closed', data={'value': 'true', **auth_params})
        print(f"Колонка '{column_name}' успешно перемещена в архив.")
    else:
        print("Удаление отменено.")

""" Подпрограмма для функций create_card и move_card по созданию карточки. """
def new_card(name, column_name):
    # Ищем нужную колонку:        
    column_id, column_name = find_column(column_name)
    # Если нужнуая колонка найдена:
    if column_id:
        # Ищем карточки с похожими названиями:
        card_data = requests.get(base_url.format('lists') + '/' + column_id + '/cards', params=auth_params).json()
        card_data = [card_data[i]['name'] for i in range(len(card_data))]
        # Если похожие карточки найдены:
        if name.lower() in map(lambda s: s.lower(), card_data):
            print(f"В выбранной Вами колонке '{column_name}' найдено карточек с именем '{name}': {len(card_data)}")
            print("Вы всё равно хотите продолжить?\nДля подтверждения введите латиницей символ 'y' (для отмены нажмите 'Enter')")
            if not input() in ['y', 'Y', 'н', 'Н']: # Если ничего не введено или введено
                                                    # не ['y', 'Y', 'н', 'Н'] и нажат Enter, ...
                print(f"Создание карточки '{name}' в колонке '{column_name}' отменено.") 
                return True # ... выходим из программы.
        # Создадим карточку с именем name в найденной колонке:      
        requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})
        print(f"Карточка '{name}' успешно создана в колонке '{column_name}'!") 
        return True
    # Если нужнуая колонка не найдена:
    return False  

""" Создание карточки в указанной колонке. Если колонки не существует, она будет создана. """    
def create_card(name, column_name):
    # Создаём новую задачу (карточку):
    if new_card(name, column_name) == False: # Если колонки column_name не существует, ...
        print(f"Колонка с именем '{column_name}' не найдена! Вы хотите её создать?")
        print(f"Для подтверждения введите латиницей символ 'y' (для отмены нажмите 'Enter')")
        if input() in ['y', 'Y', 'н', 'Н']:
            # ... создаём новую колонку:
            create_column(column_name)
            # Создаём новую задачу (карточку) во вновь созданной колонке:       
            new_card(name, column_name)
        else: # Если ничего не введено или введено не ['y', 'Y', 'н', 'Н'] и нажат Enter:
            print("Создание карточки в несуществующей колонке отменено пользователем.")

""" Поиск карточки по имени. Функция возвращает список из трёх значений: id катрочки, название карточки и название колонки. """
def find_card(name, action):
    # Получим данные всех колонок на доске:    
    column_data = get_column_data()    
    card_ids = [] # Список списков для хранения найденных карточек в формате:
                  # [id карточки, название карточки, название колонки, позиция колонки на доске,
                  # цвет меток, цвет фона, наличие картинки, дата и время последней активности]
                  # Список признаков можно изменить по своему желанию (см. документацию Trello API).
    # Для каждой колонки ...
    for i in range(len(column_data)): 
        # ... получим данные всех карточек в колонке:   
        column_cards = requests.get(base_url.format('lists') + '/' + column_data[i]['id'] + '/cards', params=auth_params).json()
        # Для каждой карточки в колонке ...    
        for card in column_cards:
            # ... если искомая карточка найдена, ...    
            if card['name'].lower() == name.lower(): 
                # ... добавляем в список её id и остальные параметры:
                card_ids.append(
                                [
                                 card['id'],
                                 card['name'],
                                 column_data[i]['name'],
                                 i + 1,
                                 [card['labels'][j]['color'] for j in range(len(card['labels']))],
                                 card['cover']['color'],
                                 card['cover']['idUploadedBackground'],
                                 card['dateLastActivity']
                                ]
                               )    
    if len(card_ids) > 1: # Если найдено более одной карточки с именем name, ...
        # ... выводим в консоль информацию о количестве всех найденных карточек ...
        s = f"Найдено карточек с именем '{name}': {str(len(card_ids))}"
        print(f"{s}\n{'-' * len(s)}")
        for i in range(len(card_ids)):
            # ... и перечисляем их в виде нумерованного списка:
            print(f"{str(i + 1)}: '{card_ids[i][1]}' в колонке {card_ids[i][3]} из {len(column_data)} '{card_ids[i][2]}' (метки: {card_ids[i][4]}, цвет фона: {card_ids[i][5]}, фоновое изображение: {'есть' * bool(card_ids[i][6]) + 'нет' * (not card_ids[i][6])}, последняя активность: {card_ids[i][7]})")            
        # Предлагаем пользователю выбрать номер нужной карточки или "передумать":
        s = f"Введите с клавиатуры номер той карточки, которую Вы хотите {action}"
        print(f"{'-' * len(s)}\n{s}\n(для отмены введите латиницей символ 'q'):")
        # Предотвращаем ввод неправильных данных:
        while True:
            try: # Пробуем получить от пользователя с клавиатуры номер карточки и выбрать в списке нужный id:
                enter = input()
                if int(enter) in range(1, len(card_ids)+1): # Если введён номер из напечатанного списка, ...
                    card_id, card_name, column_name = card_ids[int(enter) - 1][:3] # ... запоминаем id, название карточки и название колонки.
                    # Если в колонке, куда планируется перемещение, уже есть карточка с таким же именем:
                    if action[:12] == 'Переместить' and card_ids[int(enter) - 1][1] == column_name:
                        print(f"Карточка с именем '{name}' уже существует в выбранной Вами колонке '{column_name}'")
                        print("Вы всё равно хотите продолжить?\nДля подтверждения введите латиницей символ 'y' (для отмены нажмите 'Enter')")
                        if not input() in ['y', 'Y', 'н', 'Н']: # Если ничего не введено или введено
                                                                # не ['y', 'Y', 'н', 'Н'] и нажат Enter, ...
                            print(f"Перемещение отменено.") 
                            return [None, None, None] # ... выходим из программы.
                else:
                    raise ValueError # Несуществующий номер
            except: # При неправильном вводе - несуществующий номер или не число (кроме 'q') - выводим в консоль сообщение об ошибке:
                if enter in ['q', 'Q', 'й', 'Й']: # При вводе 'q' выходим из программы.
                    print("Действие отменено пользователем.")
                    return [None, None, None]
                else:
                    print("Необходимо ввести номер карточки из списка. Попробуйте снова\n(для отмены введите латиницей символ 'q'):")
            else: # При правильном вводе идём дальше.
                break
    elif len(card_ids) == 1: # Если найдена только одна карточка с именем name, ...
        # ... запоминаем её id, название и название колонки:
        card_id, card_name, column_name = card_ids[0][:3]
    else: # Если не найдено ни одной карточки с именем name, ...
        print(f"Карточка с именем '{name}' не обнаружена :(")
        return [None, None, None] # ... выходим из программы.
    return [card_id, card_name, column_name]

""" Перемещение карточки в указанную колонку """
def move_card(name, par_column_name): 
    # Ищем нужную карточку:   
    card_id, card_name = find_card(name, f"переместить в колонку '{par_column_name}'")[:2]
    if card_id:
        # Теперь, когда у нас есть id карточки, которую мы хотим переместить, ищем нужную колонку:   
        column_id, column_name = find_column(par_column_name)
        if column_id:
            # Если колонка найдена, выполним запрос к API для перемещения карточки в нужную колонку: 
            requests.put(base_url.format('cards') + '/' + card_id + '/idList', data={'value': column_id, **auth_params}) 
            print(f"Карточка '{card_name}' успешно перемещена в колонку '{column_name}'!")
        else: # Если колонка не найдена, ...
            print(f"Колонка с именем '{par_column_name}' не найдена! Вы хотите её создать?")
            print(f"Для подтверждения введите латиницей символ 'y' (для отмены нажмите 'Enter')")
            if input() in ['y', 'Y', 'н', 'Н']:
                # ... после подтверждения создаём новую колонку и перемещаем в неё нашу карточку:
                create_column(par_column_name)
                column_id, column_name = find_column(par_column_name)
                requests.put(base_url.format('cards') + '/' + card_id + '/idList', data={'value': column_id, **auth_params}) 
                print(f"Карточка '{card_name}' успешно перемещена во вновь созданную колонку '{column_name}'!")                
            else: # Если ничего не введено или введено не ['y', 'Y', 'н', 'Н'] и нажат Enter:
                print("Перемещение отменено пользователем.")

""" Удаление карточки """
def remove_card(name):
    # Ищем карточку:    
    card_id,  card_name, column_name = find_card(name, 'удалить')
    if card_id:
        # Если карточка найдена, выполним запрос к API для удаления карточки по её id:
        requests.delete(base_url.format('cards') + '/' + card_id, params=auth_params)
        print(f"Карточка '{card_name}' успешно удалена из колонки '{column_name}'!")


"""
++++++++++++++++++++++++++++++++++++++++  Основная программа.  ++++++++++++++++++++++++++++++++++++++

Для её запуска откройте командную строку в директории, где расположен этот файл trello.py и введите:

    python trello.py и через пробел параметры запуска как на примерах ↓↓↓

Пример ввода команды с параметрами запуска функции для создания новой колонки:

    python trello.py create column new_column

В зависимости от конфигурации вашей системы возможно вместо python необходимо будет вводить python3

"""  

if __name__ == "__main__":    
    if len(sys.argv) <= 2:
        read()                                              # read
    elif str(sys.argv[1]) == 'create':
        if sys.argv[2] == 'card':
            create_card(str(sys.argv[3]), str(sys.argv[4])) # Например: create card new_card Готово или create card new_card 'new column'
                                                            # (названия из одного слова можно вводить без кавычек).
        elif sys.argv[2] == 'column':
            create_column(str(sys.argv[3]))                 # Например: create column new_column
                                                            # (названия из одного слова можно вводить без кавычек).
    elif sys.argv[1] == 'move':
        move_card(str(sys.argv[2]), str(sys.argv[3]))       # Например: move new_card 'В процессе'
                                                            # (названия из одного слова можно вводить без кавычек).  
    elif sys.argv[1] == 'remove':
        if sys.argv[2] == 'card':
            remove_card(str(sys.argv[3]))                   # Например: remove card new_card (названия из одного слова можно вводить без кавычек.
        elif sys.argv[2] == 'column':
            remove_column(str(sys.argv[3]))                 # Например: remove column 'new column'
                                                            # (названия из одного слова можно вводить без кавычек).          


"""
Эти ↓↓↓ строки помогут в некотором роде протестировать возможности программы и её баги (надеюсь, их нет :) ).
Если вдруг очень сильно захочется выполнить эти ↓↓↓ строки кода, можно закомментировать блок ↑↑↑ 'Основная программа',
раскомментировать эти ↓↓↓ строки и запустить программу из редактора обычным способом.

"""

# s = '* Now run read() *'
# print(f"{'*' * len(s)}\n{s}\n")
# read()
# s = '* End of the read() *'
# print(f"\n{s}\n{'*' * len(s)}\n")

# s = '* Now run create_card("simple_card", "new_column") *'
# print(f"{'*' * len(s)}\n{s}\n")
# create_card("simple_card", "new_column")
# s = '* End of the create_card("simple_card", "new_column") *'
# print(f"\n{s}\n{'*' * len(s)}\n")

# s = '* Now run create_column("next_column") *'
# print(f"{'*' * len(s)}\n{s}\n")
# create_column("next_column")
# s = '* End of the create_column("next_column") *'
# print(f"\n{s}\n{'*' * len(s)}\n")

# s = '* Now run move_card("simple_card", "next_column") *'
# print(f"{'*' * len(s)}\n{s}\n")
# move_card("simple_card", "next_column")
# s = '* End of the move_card("simple_card", "next_column") *'
# print(f"\n{s}\n{'*' * len(s)}\n")

# s = '* Now run create_card("simple_card", "next_column") *'
# print(f"{'*' * len(s)}\n{s}\n")
# create_card("simple_card", "next_column")
# s = '* End of the create_card("simple_card", "next_column") *'
# print(f"\n{s}\n{'*' * len(s)}\n")

# s = '* Now run remove_card("simple_card") *'
# print(f"{'*' * len(s)}\n{s}\n")
# remove_card("simple_card")
# s = '* End of the remove_card("simple_card") *'
# print(f"\n{s}\n{'*' * len(s)}\n")

# s = '* Now run remove_column("new_column") *'
# print(f"{'*' * len(s)}\n{s}\n")
# remove_column("new_column")
# s = '* End of the remove_column("new_column") *'
# print(f"\n{s}\n{'*' * len(s)}\n")
