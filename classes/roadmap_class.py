class Roadmap:
#class which get info from mysql and get some settings for future work
#connect_mysql class required for mysql connection
    roadmap_id = 0
    commands_dict = {"p32"  : {"sequence": 32, "hdr": 0, "speed": 10, "steps": 50},
                     "h32"  : {"sequence": 32, "hdr": 1, "speed": 10, "steps": 50},
                     "photo": {"sequence": 1, "hdr": 0}}
    settings = {}
    workplace = 'NOTE-1'    
    fields = ["steps", "sequence", "hdr", "cameras"]

    def __init__(self, workplace)
        self.workplace = workplace

     
    def can_start(self):
    #    global cur
    # print (cur.query)
        con, cur = connect_mysql()
        cur.execute("SELECT `i360_roadmap_id` FROM `i360_roadmap` WHERE `i360_roadmap_started` = 1 and `i360_roadmap_finished` = 0 and `i360_roadmap_workplace` = %s", (self.WORKPLACE_NAME)) #command not over
        i = cur.rowcount
        if (i > 0):
            res = False
        else:
            res = True
        cur.close()
        con.close()
        return res 	  
    

    def finish_issue(self):
        # put to database that work is finished
        con, cur = connect_mysql()
        cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_finished` = 1, `i360_roadmap_started_at` = NOW() WHERE `i360_roadmap_id` = %s", (self.roadmap_id))
        con.commit()
        print ("F") #finish this issue and waiting for next task from roadmap or file
        cur.close()
        con.close()

    def read_options(self, options):    
    # some options can be read from json from options field in db
    # read more complex settings from json after command load default param
        json_options = json.loads(options)
        
        for i in range(len(self.fields)):
            if fields[i] in json_options:
                key = fields[i]
                self.settings[key] = json_options[key] 

    
    def start_issue(self):
    #    global cur
    # read from mysql command and fix that program in started
        con, cur = connect_mysql()
        cur.execute("SELECT `i360_roadmap_id`, `i360_roadmap_json_options`, `i360_roadmap_command` FROM `i360 roadmap` WHERE  `i360_roadmap_started` = 0 and `i360_roadmap_workplace` = %s", (self.WORKPLACE_NAME)) # command not started
        self.roadmap_id, options, cmd = cur.fetchone()
        print ("loaded issue from roadmap command %s, roadmap id: %d", (cmd, self.roadmap_id))
        self.read_command(cmd)
        self.read_options(options)
        cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_stated` = 1, `i360_roadmap_started_at` = NOW() WHERE `i360_roadmap_id` = %s", self.roadmap_id)
        con.commit()
        cur.close()
        con.close()
	    #end start_work file	       
    

    def read_command(self, cmd):
    # простая команда дает некоторые настройки по умолчанию
        self.settings = self.commands_dict.get(cmd, "photo") #default simple photo
        return self.settings                   


    def update_issue(json_message, progress):
        con, cur = connect_mysql()
        cur.execute("UPDATE `i360_roadmap` SET `i360_roadmap_updated_at` = NOW(), `i360_roadmap_json_message` = %s, `i360_roadmap_progress` = %d WHERE `i360_roadmap_id` = %d", (json_message, progress, self.roadmap_id))
        con.commit()
        print ("u", end='') # just update current state of work
        cur.close()
        con.close()

 
