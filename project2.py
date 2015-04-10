import bsddb3 as bsddb
import random, os, sys, time 

#create this directory in tmp before running this program
DB_FILE = "/tmp/nsd_db/my_db"

#ten thousand for now but needs to be one hundred thousand to hand in
DB_SIZE = 1000
SEED = 10000000
db_1 = None 


# FLAGS
BTREE =  bsddb.db.DB_BTREE # BTree
HASH = bsddb.db.DB_HASH
DB_FLAG = BTREE

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

def main(argv):
    if len(argv) > 1:
        print("Error: too many args. Please enter one of these (btree, hash, indexfile)")
        time.sleep(2)
        sys.exit()
    elif argv[0] == "btree":
        DB_FLAG = BTREE
        print("btree selected")
        time.sleep(1)
    elif argv[0] == "hash":
        DB_FLAG = HASH
        print("hash selected")
        time.sleep(1)
    elif argv[0] == "indexfile":
        DB_FLAG = "INDEX_FILE"
        print("indexfile selected")
        time.sleep(1)
    else:
        print("Error: incorrect argument. Please enter one of these (btree, hash, indexfile)")
        time.sleep(2)
        sys.exit()        
    
    deleteContent("answers")    
    
    main_menu()

def main_menu():
    while True:
        
        os.system('clear')
        print ("Welcome!")
        print ("Please choose the menu you want to start:")
        print ("1. Create and populate a database")
        print ("2. Retrieve records with a given key")
        print ("3. Retrieve records with a given data")
        print ("4. Retrieve records with a given range key values")
        print ("5. Destroy the database")
        print ("\n0. Exit")
        choice = input(" >>  ")
        exec_menu(choice)
 
def Create():
    #Where database is created and populated
    os.system('clear')
    print("Creating & Populating Database ...")
    try:
        if DB_FLAG == "INDEX_FILE":
            db_1 = bsddb.db.DB()
            db_1.open(DB_FILE,BTREE)
            db_2 = bsddb.db.DB()
            db_2.open(DB_FILE,BTREE)
        else:
            db_1 = bsddb.db.DB()
            db_1.open(DB_FILE,DB_FLAG)
    except:
        print("Error: Database does not exist. Creating a new one.")
        time.sleep(2)
        if DB_FLAG == "INDEX_FILE":
            db_1 = bsddb.db.DB()
            db_1.open(DB_FILE,BTREE,bsddb.db.DB_CREATE)
            db_2 = bsddb.db.DB()
            db_2.open(DB_FILE,BTREE,bsddb.db.DB_CREATE)
        else:
            db_1 = bsddb.db.DB()
            db_1.open(DB_FILE,DB_FLAG,bsddb.db.DB_CREATE)
    random.seed(SEED)
    
    records = 0
    start_time = time.time()
    
    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        for i in range(krng):
            key += str(get_random_char())
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        print("key: " + key)
        print("value: "+ value) 
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        if DB_FLAG == "INDEX_FILE":
            if db_1.has_key(key) == False:
                db_1.put(key, value)
                db_2.put(value,key)
        else:
            if db_1.has_key(key) == False:
                db_1.put(key, value)
        
    end_time = time.time()
    performance(records, (end_time-start_time))
    time.sleep(3)   
    db_1.close()


def Key():
    #Search with given key  
    os.system('clear')  
    try:
        db_1 = bsddb.db.DB()
        db_1.open(DB_FILE)
    except:
        print("Error: no database found. please create database first")
        return

    print("Please enter the Key: ")
    stdin = input(">>")
    
    records = 0
    start_time = time.time()    

    if db_1.has_key(stdin.encode(encoding='UTF-8')):
        records += 1
        results(stdin,db_1.get(stdin.encode(encoding='UTF-8')).decode(encoding='UTF-8'))        
        
    end_time = time.time()
    performance(records, (end_time-start_time))
    time.sleep(2)
    
    db_1.close()    
    
def Data():
    #search with given data
    os.system('clear')    
    print("Please enter the Data: ")
    stdin = input(">>")

    if(DB_FLAG == HASH):
        db_1 = bsddb.hashopen(DB_FILE, "r")
    elif(DB_FLAG == BTREE):
        db_1 = bsddb.btopen(DB_FILE, "r")
    
    records = 0
    start_time = time.time()  
    
    for key, value in db_1.iteritems():
        if (value == stdin.encode(encoding='UTF-8')):
            results(key.decode(encoding='UTF-8'),stdin)
            records += 1

    end_time = time.time()
    performance(records, (end_time-start_time))
    time.sleep(2)
    
    db_1.close() 

def Range():
    #Search with range of keys
    db_1 = bsddb.db.DB()
    db_1.open(DB_FILE)
    os.system('clear') 
    cursor = db_1.cursor()
    print("Please enter lower limit key for the range: ")
    low = input(">> ")
    print("Please enter upper limit key for the range: ")
    high = input(">> ")
     
    list =[]
    i = 0
    
    records = 0
    start_time = time.time()     
    
    # Hash 
    if (DB_FLAG == HASH):
        while (cursor.next()):
            if (cursor.current()[0].decode(encoding='UTF-8') >= low) and (cursor.current()[0].decode(encoding='UTF-8') <= high):
                list.append(cursor.current()[0])
                records += 1 
    
    # B-Tree & IndexedFile    
    else:
        list.append(cursor.set(low.encode(encoding='UTF-8'))[0])
        while cursor.current()[0].decode(encoding='UTF-8') != high:
            cursor.next()
            list.append(cursor.current()[0])
            records += 1 
            
    end_time = time.time()
    performance(records, (end_time-start_time))
    time.sleep(2)
    
    db_1.close() 
    
    print(list)
    time.sleep(1)
 
def Destroy():
    #Destroy the database
    os.system('clear')
    
    print("Destroying Database ...")
    time.sleep(1) 
   # try:
       # db_1.close()
       # db_1.remove()
       # db_1.dbremove()
    if os.path.isfile(DB_FILE):
        print("Removing file")
        os.remove(DB_FILE)
        time.sleep(1)
    #except Exception as e:
      #  print (e)    

# Exit program
def exitProgram():
    Destroy()
    sys.exit()

# Execute menu
def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            time.sleep(1)
            menu_actions['main_menu']()
    return

def performance(records,time):
    print("Number of records retrieved: %d"%records)
    print("Total execution time: %f ms"%(1000000*time))

def results(key,value):
    output = open("answers", 'a')    
    output.write(key)
    output.write("\n"+value)
    output.write("\n")
    output.write("\n")
    output.close()    
 
def deleteContent(fName):
    with open(fName, "w"):
        pass
    
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': Create,
    '2': Key,
    '3': Data,
    '4': Range,
    '5': Destroy,
    '0': exitProgram,
}

if __name__ == "__main__":
    main(sys.argv[1:])
