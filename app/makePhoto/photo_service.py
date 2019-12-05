import os.path # for fileexists options
from time import sleep # for pause options
# команды получаем из очереди при подключении к БД
# статус кладем тудаже 
# файлы с илюстрациями сохраняем на диск
# имена файлов могут быть по типу - тест, фото, хдр (хдр + фото), фон (BACK)
# программа выполняет одну не отработанную команду из очереди в БД на локацию
# возможно игра в паузу (например через управляющий файл, или вспомогательные команды на локацию)

# 2019-12-04 
# s
# - product path: i/p/[product_id]/[issue_id]-[location_name]-[phototype](-[sequence])(-cams[cameras])(/cam[camera_index])/[product_id]_[issue_id](_cam[camera_id])(_sequence_index)(_[phototype_index]).jpg
# - test path i/t/[issue_id]-[photo_type](-[squence])
# - location: i/l/[issue_id]-[location_name]

DB_NAME = "i360"
DB_HOST = "localhost"
DB_PASS = ""
DB_BASE = "i360"

CAMERAS = 1

# название рабочего места на которое приходят команды управления
# 
SERVICE_NAME = "NOTE-1" # имя запущенного сервиса с подключенным оборудованием (месту даются задания)

# LOCATION_NAME = "WHITE" # имя рабочего стола (может быть черным, белым, может быть для зонтов, еще что-то (стол как и фон готовится фотографом)
# location - уехал в настройки съемки через sql

# если в заданный промежуток времени не пришло ответа от управляющего воздействия - ошибка
LIVE_TIMEOUT = 30

LOG_PATH = "/log"

PAUSE_FILE = "/tmp/pause.tmp"

APP = "/home/lefin/work/i360"

#pathes = { "test" : "/test/[i]",
#	   "product" : "/p/[i]",
#	   "back" : "/b/[i]"
#	   }
#	   
#текущий номер последовательности для HDR из трех кадров (номер записи после вставки в БД)

timer = 0; # инструмент построения таймера 

# жив ли контроллер управления, получен ли от него ответ в течение LIVE_TIMEOUT
ctrl_alive = False;

def indexPath(number)
    # формируем путь из индекса согласно следованию по числу
    # так для индекса 123 путь будет /1/2/3 далее имя файла
    path = ''
    string = str(number)
    for i in range(len(string)):
	path += "/" + string[i]
    return path

def newPath(cmd)
    # получаем путь сохранения файла под каждый файл
    try:
	path = APP + pathes.get(cmd)
	path = path.replace('[i]', indexPath(current_photo))
    except: 
	path = APP + "/tmp"
	print('no path in dictionary for command {}'.format(cmd))
    return path 

def getOption(options, key)
    pass  # проверка рабочих параметров передаваемых переменных

def makePhoto(issue_id, options)
    initCTRL(["delay" => "8", "Steps" = 50]) # инициализация контроллера, по хорошему сюда скорость и настройки из БД
    sequence = getOption(options, 'sequence')
    cameras = getOption(options, 'cameras')
    # тут нужно деление по объекту съемки (тест, фон, продукт)
    product = getOption(options, 'product')
    photo_type = getOption(options, 'photo_type') # hdr or simply 
    photos_by_step = getPhotosByStep(photo_type)
    photo_object = getOption(options, 'object') # product, background (table), test 

    for s in range(sequence): #each step need to make photo
	for c in range(cameras): #if few cameras in table //but here we must use the specific comport
	    for t in range(photos_by_step): #photo for hdr
		if (photo_object == 'product')
		    path = "/i/" + photo_object + "/" + indexPath(product_id)
		else if (photo_object == 'background')
		    
		else # test one
		    path = "/i/test/" + issue_id + "_cam" + c + "_" + photo_type    
		runPhoto(c, path) # for photo we must to know witch camera is used    
	pause()
	if (sequence == 1) break
	makeStep(); 


def pause()
    # sleep one second while file exists
    while os.path.exists(PAUSE_FILE):
	sleep(1)
	print('.', end='')
    
        
# функция шага двигателя    
def makeStep()
    # передать контроллеру команду RUN
    pass


def start()
    # фиксация того, что процедура стартовала и остальные потоки блокировались к запуску
    pass     

    
def run()
    # run once
    print('Программа для съемки вокруг объекта')
    print('Проект i360')
    print('https://github.com/lefin17/i360')
    # инициализация подключения к БД
    start()
    # получение команды (здесь задается путь куда сохранять)
    # так это прям из БД получаем абсолютную или относительную локацию в составе команды

    
