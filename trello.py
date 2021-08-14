import sys 
import requests    
base_url = "https://api.trello.com/1/{}"

with open('.\Trello_Key.txt') as f:
    key = f.read()

with open('.\Trello_Token.txt') as f:
    token = f.read()

auth_params = {    
    'key': key,
    'token': token,}

with open('.\Доска1_trello.txt') as f:
    board_id = f.read()

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # print(column_data)      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name']) 

def create_card(name, column_name, column_data):
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна        
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            return True
    return False  
    
def create(name, column_name):  
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json() 
    # Создаём новую задачу (карточку)
    if create_card(name, column_name, column_data) == False:    
        # Если колонки column_name не существует, создаём новую колонку
        requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': column_data[0]['idBoard'], **auth_params})
        # Получим данные всех колонок на доске 
        column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
        # Создаём новую задачу (карточку) во вновь созданной колонке       
        create_card(name, column_name, column_data)

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                break    
        if task_id:    
            break    
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break    
    
if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])          