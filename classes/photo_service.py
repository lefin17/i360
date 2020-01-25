import os.path # for fileexists options

import os # for remove file 

from time import sleep # for pause options

#import pymysql

from mysql_connect import *

# команды получаем из очереди при подключении к БД (i360_roadmap)
# команды p32, h32 - и тому подобное - p32 - фотография, смещение на 50 шагов со скоростью по дефолту
# статус кладем тудаже
 
# файлы с илюстрациями сохраняем на диск
# имена файлов могут быть по типу - тест, фото, хдр (хдр + фото), фон (BACK)
# имена файлов зависят от съемки - номер задания (разделенный по индексу), далее номер камеры cam+i если камер больше 1? опционально,
# далее при съемки hdr добавляем индекс последовательности для дальнейшей обраотки
# программа выполняет одну не отработанную команду из очереди в БД на локацию
# возможно игра в паузу (например через управляющий файл, или вспомогательные команды на локацию)

# 2019-12-04 
# s
# - product path: i/p/[product_id]/[issue_id]-[location_name]-[phototype](-[sequence])(-cams[cameras])(/cam[camera_index])/[product_id]_[issue_id](_cam[camera_id])(_sequence_index)(_[phototype_index]).jpg
# - test path i/t/[issue_id]-[photo_type](-[squence])
# - location: i/l/[issue_id]-[location_name]

# все снимается по заданию - основное - номер задания.
# на более высоком уровне идет объединение задания и цели съемки, это может быть пересъемка, к одному продукту может быть 
# множество различных съемок
# некоторые съемки могут быть объеденены для различных целей

# DB_NAME = "i360"
# DB_HOST = "localhost"
# DB_PASS = "nEvMqSM9"
# DB_USER = "user"

LIVE_TIMEOUT = 30

APP = "/home/lefin/work/i360";

LOG_PATH = "/log"

PAUSE_FILE = APP + "/tmp/pause.tmp"

PAUSE_REMOVE_FILE = APP + "/tmp/pause_remover.tmp"

RESET_FILE = APP + "/tmp/reset.tmp"

# словарь команд. Фото по кругу, просто фото, возможно просто поворот? или просто поворот убераем на файловое взаимодействие
commands_dict = {"p32" : {"sequence": 32, "hdr": 0, "speed": 10, "steps": 50},
                "h32" : {"sequence": 32, "hdr": 1, "speed": 10, "steps": 50},
                "photo": {"sequence": 1, "hdr": 0}}

settings = {}

timer = 0; # инструмент построения таймера 

# жив ли контроллер управления, получен ли от него ответ в течение LIVE_TIMEOUT
ctrl_alive = False;


# cameras = 1 # can be changed by load options to roadmap

# sequence_steps = 32 # количество шагов в последовательности по умолчанию (в следующей версии можно перенести в файл настроек)

# hdr = 1 # может принимать значение (0 || 1) если 0 то без цикла, если 1 - то добавляется индекс к файлам и цикл по брекетингу
	# можно заменить на кадров на позицию, но тогда немного смысл теряется.
	
roadmap_id = 0 # обязательно меняется загрузкой - если остается 0 после функции старта - уходим из программы

# название рабочего места на которое приходят команды управления
# после обработки происходит загрузка в библиотеку - при загрузке в библиотеку - возможно важно на каком рабочем месте выполнены работы, 
# на самом рабочем месте - данная информация не важна
 
WORKPLACE_NAME = "NOTE-1" # имя запущенного сервиса с подключенным оборудованием (месту даются задания)

# LOCATION_NAME = "WHITE" # имя рабочего стола (может быть черным, белым, может быть для зонтов, еще что-то (стол как и фон готовится фотографом)
# location - уехал в настройки съемки через sql

# если в заданный промежуток времени не пришло ответа от управляющего воздействия - ошибка

# con = None
# cur = None

# def connect_mysql():
#    global con, cur
#    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
#    with con:
#        cur = con.cursor()


def clear_tmp():
    #clear tmp folder from files witch can affect for executaiton of main program
    os.remove(PAUSE_FILE)
    os.remove(RESET_FILE)
    
    
def can_start():
#    global cur
    # print (cur.query)
    cur.execute("SELECT `i360_roadmap_id` FROM `i360_roadmap` WHERE `i360_roadmap_started` = 1 and `i360_roadmap_finished` = 0 and `i360_roadmap_workplace` = %s", (WORKPLACE_NAME)) #command not over
    i = cur.rowcount
    if (i > 0):
        res = False
    else:
        res = True
    return res 	  
	
		          
def read_options(options):    
    # some options can be read from json from options field in db
    # read more complex settings from json after command load default param
    json_options = json.loads(options)
    fields = ["steps", "sequence", "hdr", "cameras"]
    for =i in range(len(fields)):
        if fields[i] in json_options:
            key = fields[i]
            settings[key] = json_options[key] 


def start_issue():
    #    global cur
    # read from mysql command and fix that program in started
    cur.execute("SELECT `i360_roadmap_id`, `i360_roadmap_json_options`, `i360_roadmap_command` FROM `i360 roadmap` WHERE  `i360_roadmap_started` = 0 and `i360_roadmap_workplace` = %s", (WORKPLACE_NAME)) # command not started
    roadmap_id, options, cmd = cur.fetchone()
    print ("loaded issue from roadmap command %s, roadmap id: %d", (cmd, roadmap_id))
    read_command(cmd)
    read_options(options)
    cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_stated` = 1, `i360_roadmap_started_at` = NOW() WHERE `i360_roadmap_id` = %s", roadmap_id)
    con.commit()
	#end start_work file	       
	    

def read_command(cmd):
    # простая команда дает некоторые настройки по умолчанию
    settings = commands_dict.get(cmd, "photo") #default simple photo
    return settings                   


def update_work(message, progress):
    cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_updated_at` = NOW(), `i360_roadmap_message` = %s, `i360_roadmap_progress` = %d WHERE `i360_roadmap_id` = %d", (message, progress, roadmap_id))
    con.commit()
    print ("u", end='') # just update current state of work
	     
		
def finish_work():
    # put to database that work is finished
    cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_finished` = 1, `i360_roadmap_started_at` = NOW() WHERE `i360_roadmap_id` = %s", (roadmap_id))
    con.commit()
    print ("F") #finish this issue and waiting for next task from roadmap or file


def indexPath(number):
    # формируем путь из индекса согласно следованию по числу
    # так для индекса 123 путь будет /1/2/3 далее имя файла
    path = ''
    string = str(number)
    for i in range(len(string)):
        path += "/" + string[i]
    return path



def makePhoto(roadmap_id): 
    delay = settings.get("delay", 8) # нужно увести куда-то в модуль управления поворотом платформы
    steps = settings.get("steps", 50)
    com_port = settings.get("com_arduino", "/dev/COM") #need to test and change

    ctrl = initCTRL({"delay" : delay, #задержка между шагами в милисекундах, определяет скорость вращения платформы 
                     "steps" : steps, #число шагов шагового двигателя на один шаг поворота платформы
                  "com_port" : com_port}) # инициализация контроллера, по хорошему сюда скорость и настройки из БД
    if ctrl == False:
        print ("Can not initialize controller")
        return False
    # sequence = getOption(options, 'sequence') # вот это всё ерунда какая-то... 
    
    # cameras = getOption(options, 'cameras')
    # тут нужно деление по объекту съемки (тест, фон, продукт)
    # product = getOption(options, 'product')

    hdr = settings.get("hdr", 0)
    cameras = settings.get("cameras", 1)
    sequence = settings.get("sequence", 1) #can be 32, 
   
    if hdr == 1: 
        photos_by_step = 3
	else:
        photos_by_step = 1

    # photo_type = getOption(options, 'photo_type') # hdr or simply 
    # photos_by_step = getPhotosByStep(photo_type)
    # photo_object = getOption(options, 'object') # product, background (table), test 
    path = "/i/src" + indexPath(roadmap_id)
    for s in range(sequence): #each step need to make photo
        for c in range(cameras): #if few cameras in table //but here we must use the specific comport
            for t in range(photos_by_step): #photo for hdr
                fn = path + "/cam" + c + "-" + s
                if (photos_by_range > 0):
                    fn += "-" + t
                runPhoto(c, fn) # for photo we must to know witch camera is used    
                pause()
	
        if (sequence == 1):
            break

        makeStep(); 
        update_work("next step", s)
    finish_work()

def pause():
    # sleep one second while file exists
    while os.path.exists(PAUSE_FILE):
        sleep(1)
        if os.path.exists(PAUSE_REMOVE_FILE):
            os.remove(PAUSE_REMOVE_FILE)
            os.remove(PAUSE_FILE)
            break
        print('.', end='') #simulate, possible can be stopped some other way
    
        
# функция шага двигателя    
def makeStep():
    # передать контроллеру команду RUN
    pass


def run():
    # run once
    print('Программа для съемки вокруг объекта')
    print('Проект i360')
    print('https://github.com/lefin17/i360')
    print()
    # инициализация подключения к БД
    con, cur = connect_mysql()
    if can_start():
        print ('we can start')
    else:
        print ('there is no chance to start')
            
    # получение команды (здесь задается путь куда сохранять)
    # так это прям из БД получаем абсолютную или относительную локацию в составе команды

  
