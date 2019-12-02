# команды получаем из очереди при подключении к БД
# статус кладем тудаже 
# файлы с илюстрациями сохраняем на диск
# имена файлов могут быть по типу - тест, фото, хдр (хдр + фото), фон (BACK)
# программа выполняет одну не отработанную команду из очереди в БД на локацию
# возможно игра в паузу (например через управляющий файл, или вспомогательные команды на локацию)

DB_NAME = "i360"
DB_HOST = "localhost"
DB_PASS = ""
DB_BASE = "i360"

# название рабочего места на которое приходят команды управления
LOCATION_NAME = "White"

# если в заданный промежуток времени не пришло ответа от управляющего воздействия - ошибка
LIVE_TIMEOUT = 30

LOG_PATH = "/log"

PAUSE_FILE = "/tmp/pause.tmp"

APP = "/home/lefin/work/i360"

pathes = { "testPhoto" : "/test/[i]",
	   "photo" : "/p/[i]",
	   "back" : "/b/[i]",
	   "hdr" : "/h" }
	   
commands = { "ringPhoto32" : ringPhoto32(),
	     "ringHDR32" : ringHDR32(),
	     "testPhoto" : testPhoto(),
	     "testHDR" : testHDR(),
	     "backPhoto" : backPhoto(),
	     "backHDR" : backHDR() }
	         

#текущий номер последовательности для HDR из трех кадров (номер записи после вставки в БД)

timer = 0; // инструмент построения таймера 

// жив ли контроллер управления, получен ли от него ответ в течение LIVE_TIMEOUT
ctrl_alive = False;

current_hdr = 1 
 
current_photo = 1

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

def getHDR_ID()
    # получить индекс HDR (просто так последовательно присваивать нельзя из-за паралельных съемок)
    pass 

    
def getPhoto_ID()
    # получить индекс фото, далее 


def makePhoto()
    Photo_id = getPhotoId()
    pass

    
def makeHDR()
    # фотоаппарат должен быть выставлен в режим брекетеринга, и три кадра и на диск и в базу    
    HDR_id = getHDRid()
    for i in range(3)
	makePhoto(["HDR" => HDR_id])
	pause()
	    

# функция шага двигателя    
def makeStep()
    # передать контроллеру команду RUN
    pass


def ringHDR32()
    initCTRL(["delay" => "8", "Steps" = 50])
    for i in range(32):
	path 
	pause()
	makeHRD()
	pause()
	makeStep()
	

def pause()
    # если есть файл - остановись... если нет - продолжи
    
	
def ringPhoto32()
    initCTRL(["delay" => "8", "Steps" = 50])
    for i in range(32):
	pause()
	makePhoto()
	pause()
	makeStep()
	

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

    
