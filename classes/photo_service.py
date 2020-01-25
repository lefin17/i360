import os.path # for fileexists options

import os # for remove file 

from time import sleep # for pause options

#import pymysql

from mysql_connect import *
from roadmap_class import *

# команды получаем из очереди при подключении к БД (i360_roadmap)
# команды p32, h32 - и тому подобное - p32 - фотография, смещение на 50 шагов со скоростью по дефолту
# статус кладем тудаже
 
# файлы с илюстрациями сохраняем на диск
# имена файлов зависят от съемки - номер задания (разделенный по индексу), далее номер камеры cam+i если камер больше 1? опционально,
# далее при съемки hdr добавляем индекс последовательности для дальнейшей обработки
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

LIVE_TIMEOUT = 30

APP = "/home/lefin/work/i360";

LOG_PATH = "/log"

PAUSE_LOOP_FILE = APP + "/tmp/pause.tmp"

PAUSE_REMOVE_FILE = APP + "/tmp/pause_remover.tmp"

RESET_LOOP_FILE = APP + "/tmp/reset_remover.tmp"

# словарь команд. Фото по кругу, просто фото, возможно просто поворот? или просто поворот убераем на файловое взаимодействие

settings = {} # возможно настройки можно будет читать не только из дорожной карты (оперативного плана)

timer = 0; # инструмент построения таймера 

# жив ли контроллер управления, получен ли от него ответ в течение LIVE_TIMEOUT
ctrl_alive = False;

# cameras = 1 # can be changed by load options to roadmap

# sequence_steps = 32 # количество шагов в последовательности по умолчанию (в следующей версии можно перенести в файл настроек)

# hdr = 1 # может принимать значение (0 || 1) если 0 то без цикла, если 1 - то добавляется индекс к файлам и цикл по брекетингу
	# можно заменить на кадров на позицию, но тогда немного смысл теряется.
	
# roadmap_id = 0 # обязательно меняется загрузкой - если остается 0 после функции старта - уходим из программы

# название рабочего места на которое приходят команды управления
# после обработки происходит загрузка в библиотеку - при загрузке в библиотеку - возможно важно на каком рабочем месте выполнены работы, 
# на самом рабочем месте - данная информация не важна
 
WORKPLACE = "NOTE-1" # имя запущенного сервиса с подключенным оборудованием (месту даются задания)

# если в заданный промежуток времени не пришло ответа от управляющего воздействия - ошибка


def clear_tmp():
    #clear tmp folder from files witch can affect for executaiton of main program
    os.remove(PAUSE_LOOP_FILE)
    os.remove(RESET_LOOP_FILE)


def indexPath(number):
    # формируем путь из индекса согласно следованию по числу
    # так для индекса 123 путь будет /1/2/3 далее имя файла
    path = ''
    string = str(number)
    for i in range(len(string)):
        path += "/" + string[i]
    return path


def initCtrl():
    delay = settings.get("delay", 8) # нужно увести куда-то в модуль управления поворотом платформы
    steps = settings.get("steps", 50)
    com_port = settings.get("com_arduino", "/dev/COM") #need to test and change

    ctrl = initCTRL({"delay" : delay, #задержка между шагами в милисекундах, определяет скорость вращения платформы 
                     "steps" : steps, #число шагов шагового двигателя на один шаг поворота платформы
                  "com_port" : com_port}) # инициализация контроллера, по хорошему сюда скорость и настройки из БД
    # вышестоящую функцию нужно бы заменить на соединение с контроллером и вывод этого результата
    if ctrl == False:
        print ("Can not initialize controller")

        return False
    return True


def run_loop(): 
    #roadmap_id global one?
    hdr = settings.get("hdr", 0)
    cameras = settings.get("cameras", 1)
    sequence = settings.get("sequence", 1) #can be 32, possible more, 1600 microstep by stepper motor for whole circle (loop), 
   
    if hdr == 1: 
        photos_by_step = 3
    else:
        photos_by_step = 1

    path = "/i/src" + indexPath(roadmap.roadmap_id)

    for s in range(sequence): #each step needs to make photo
        for c in range(cameras): #if few cameras in table //but here we must use the specific comport
            for t in range(photos_by_step): #photo for hdr ? can be differ from different cameras?
                fn = path + "/" + roadmap.roadmap_id + "-cam" + c + "-" + s
                if (photos_by_range > 1):
                    fn += "-" + t
                runPhoto(c, fn) # for photo we must to know which camera is used    
                loop_pause()
                if (loop_reset()):
                    return False
            #count progress, still with out photo by cameras count
            progress = round(s / sequence * 100)
            # make message for sql
            json_message = json.dumps({"fn" : fn, "step":  s, "camera": c, "photo_step": t})
            roadmap.update_issue(json_message, progress) #info to sql
            sleep(1) # в секундах
        if (sequence == 1):
            break

        makeStep(); #поворот платформы / platform rotation step
    return True #success with task - after it start finish function

def loop_reset():
    #reset loop by file exists
    if (os.path.exists(RESET_LOOP_FILE)):
        os.remove(RESET_LOOP_FILE)
        return True
    return False
  
          
def loop_pause():
    # sleep one second while file exists
    while os.path.exists(PAUSE_LOOP_FILE):
        sleep(1)
        if os.path.exists(PAUSE_REMOVE_FILE):
            os.remove(PAUSE_REMOVE_FILE)
            os.remove(PAUSE_LOOP_FILE)
            break
        print('.', end='') #simulate, possible can be stopped some other way
    

def runPhoto(camera, fn):
    #fn - file to save
    #camera - index of camera to work with
    #load camera settings
    print ("P", end='')
    pass

        
def makeStep():
    # функция шага двигателя    
    # передать контроллеру команду RUN
    print ("S", end='')
    pass


def run(): #разовый запуск одного из заданий помещенных в оперативный план
    # run once
    print('Программа для съемки вокруг объекта')
    print('Проект i360')
    print('https://github.com/lefin17/i360')
    print()
    # инициализация подключения к БД
    # con, cur = connect_mysql()
    roadmap = Roadmap(WORKPLACE)
    if roadmap.can_start() & initCtrl(): # если ничего другого не выполняется, далее проверка на подсоединение контроллера
        print ('we can start')
        roadmap.start_issue() # запуск команды
        settings = roadmap.settings # берем настройки из загруженного задания 
        run_loop() # цикл - у функции есть успех о выполенении
        roadmap.finish_issue() # финализация выполнения (можно давать информацию об успехе или отмене выполнения)
    else:
        print ('there is no chance to start')
  
