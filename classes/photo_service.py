import os.path # for fileexists options

import os # for remove file 

from time import sleep # for pause options

import pymysql

# команды получаем из очереди при подключении к БД (i360_roadmap)
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

DB_NAME = "i360"
DB_HOST = "localhost"
DB_PASS = "nEvMqSM9"
DB_USER = "user"

LIVE_TIMEOUT = 30

APP = "/home/lefin/work/i360";

LOG_PATH = "/log"

PAUSE_FILE = APP + "/tmp/pause.tmp"

PAUSE_REMOVE_FILE = APP + "/tmp/pause_remover.tmp"

RESET_FILE = APP + "/tmp/reset.tmp"

cameras = 1 # can be changed by load options to roadmap

sequence_steps = 32 # количество шагов в последовательности по умолчанию (в следующей версии можно перенести в файл настроек)

hdr = 1 # может принимать значение (0 || 1) если 0 то без цикла, если 1 - то добавляется индекс к файлам и цикл по брекетингу
	# можно заменить на кадров на позицию, но тогда немного смысл теряется.
	
roadmap_id = 0 # обязательно меняется загрузкой - если остается 0 после функции старта - уходим из программы

# название рабочего места на которое приходят команды управления
# после обработки происходит загрузка в библиотеку - при загрузке в библиотеку - возможно важно на каком рабочем месте выполнены работы, 
# на самом рабочем месте - данная информация не важна
 
WORKPLACE_NAME = "NOTE-1" # имя запущенного сервиса с подключенным оборудованием (месту даются задания)

# LOCATION_NAME = "WHITE" # имя рабочего стола (может быть черным, белым, может быть для зонтов, еще что-то (стол как и фон готовится фотографом)
# location - уехал в настройки съемки через sql

# если в заданный промежуток времени не пришло ответа от управляющего воздействия - ошибка

con = None
cur = None

def connect_mysql():
    global con, cur
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    with con:
        cur = con.cursor()
    print (con)    


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
	
		          
def start_work():
#    global cur
    # read from mysql command and fix that program in started
    cur.execute("SELECT `i360_roadmap_id` FROM `i360 roadmap` WHERE  `i360_roadmap_started` = 0 and `i360_roadmap_workplace` = %s", (WORKPLACE_NAME)) # command not started
    roadmap_id = cur.fetchone()[0]
    print (roadmap_id)
	
    cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_stated` = 1, `i360_roadmap_started_at` = NOW() WHERE `i360_roadmap_id` = '%s'", roadmap_id)
	#end start_work file	       
	    

def update_work(message, progress):
    cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_updated_at` = NOW(), `i360_roadmap_message` = '%s', `i360_roadmap_progress` = '%s' WHERE `i360_roadmap_id` = '%s'", (message, progress, roadmap_id))
    print ("Update work")     
	     
		
def finish_work():
    # put to database that work is finished
    cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_finished` = 1, `i360_roadmap_started_at` = NOW() WHERE `i360_roadmap_id` = '%s'", (roadmap_id))
    print ("Finish work")


def read_options():    
    # some options can be read from json from options field in db
    pass    
    

timer = 0; # инструмент построения таймера 

# жив ли контроллер управления, получен ли от него ответ в течение LIVE_TIMEOUT
ctrl_alive = False;

def indexPath(number):
    # формируем путь из индекса согласно следованию по числу
    # так для индекса 123 путь будет /1/2/3 далее имя файла
    path = ''
    string = str(number)
    for i in range(len(string)):
        path += "/" + string[i]
    return path

def newPath(cmd):
    # получаем путь сохранения файла под каждый файл
    try:
        path = APP + pathes.get(cmd)
        path = path.replace('[i]', indexPath(current_photo))
    except: 
        path = APP + "/tmp"
    print('no path in dictionary for command {}'.format(cmd))
    return path 


def getOption(options, key):
    pass  # проверка рабочих параметров передаваемых переменных


def makePhoto(roadmap_id):
    initCTRL({"delay" : "8", "Steps" : 50}) # инициализация контроллера, по хорошему сюда скорость и настройки из БД
    # sequence = getOption(options, 'sequence') # вот это всё ерунда какая-то... 
    
    # cameras = getOption(options, 'cameras')
    # тут нужно деление по объекту съемки (тест, фон, продукт)
    # product = getOption(options, 'product')
    if hdr == 1: 
        photos_by_step = 3
	
    # photo_type = getOption(options, 'photo_type') # hdr or simply 
    # photos_by_step = getPhotosByStep(photo_type)
    # photo_object = getOption(options, 'object') # product, background (table), test 

    for s in range(sequence): #each step need to make photo
        for c in range(cameras): #if few cameras in table //but here we must use the specific comport
            for t in range(photos_by_step): #photo for hdr
                path = "/i/" + photo_object + "/" + indexPath(product_id)
                runPhoto(c, path) # for photo we must to know witch camera is used    
                pause()
	
        if (sequence == 1):
            break
    makeStep(); 


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
    # инициализация подключения к БД
    connect_mysql()
    if can_start():
        print ('we can start')
    else:
        print ('there is no chance to start')
            
    # получение команды (здесь задается путь куда сохранять)
    # так это прям из БД получаем абсолютную или относительную локацию в составе команды

  