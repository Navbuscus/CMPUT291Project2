import bsddb3 as bsddb
import random, os, sys, time 

#create this directory in tmp before running this program
DA_FILE = "/tmp/nsd_db/my_db"

#ten thousand for now but needs to be one hundred thousand to hand in
DB_SIZE = 10000
SEED = 10000000
db = None 

# FLAGS
DB_FLAG = 0 # BTree
#DB_FLAG = 1 # HashTable
#DB_FLAG = 2 # Indexed File

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))


def main():
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
    print("HERE DATABASE IS CREATED AND POPULATED")
    
    if (DB_FLAG == 0):
        try:
            db = bsddb.btopen(DA_FILE, "w")
        except:
            print("DB doesn't exist, creating a new one")
            db = bsddb.btopen(DA_FILE, "c")
        random.seed(SEED)
    
        for index in range(DB_SIZE):
            krng = 64 + get_random()
            key = ""
            for i in range(krng):
                key += str(get_random_char())
            vrng = 64 + get_random()
            value = ""
            for i in range(vrng):
                value += str(get_random_char())
            print("\n" + key)            
            key = key.encode(encoding='UTF-8')
            value = value.encode(encoding='UTF-8')
            if db.has_key(key) == False:
                db[key] = value

    if (DB_FLAG == 1):
        try:
            db = bsddb.hashopen(DA_FILE, "w")
        except:
            print("DB doesn't exist, creating a new one")
            db = bsddb.hashopen(DA_FILE, "c")
        random.seed(SEED)
    
        for index in range(DB_SIZE):
            krng = 64 + get_random()
            key = ""
            for i in range(krng):
                key += str(get_random_char())
            vrng = 64 + get_random()
            value = ""
            for i in range(vrng):
                value += str(get_random_char())
            key = key.encode(encoding='UTF-8')
            value = value.encode(encoding='UTF-8')
            if db.has_key(key) == False:
                db[key] = value
    
def Key():
    #Search with given key  
    os.system('clear')    
    print("Please enter the Key: ")
    db = bsddb.btopen(DA_FILE, "r")
    stdin = input(">>")
    
    if db.has_key(stdin.encode(encoding='UTF-8')):
        print("Exists!")
    else:
        print("%s doesn't exist." %stdin)
            
    time.sleep(2)
    
def Data():
    #search with given data
    os.system('clear')    
    print("Please enter the Key: ")
    db = bsddb.btopen(DA_FILE, "r")
    stdin = input(">>")
    
    time.sleep(2)

def Range():
    #Search with range of keys
    os.system('clear')    
    print("HERE PROGRAM SEARCHES A GIVEN RANGE OF KEYS")
    time.sleep(2)
 
def Destroy():
    #Destroy the database
    time.sleep(1)
    
    try:
        db.close()
    except Exception as e:
        print (e)    

# Back to main menu
def back():
    main()
 
# Exit program
def exitProgram():
    Destroy()
    sys.exit()

# Execute menu
def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            time.sleep(1)
            menu_actions['main']()
    return
 
# Menu definition
menu_actions = {
    'main_menu': main,
    '1': Create,
    '2': Key,
    '3': Data,
    '4': Range,
    '5': Destroy,
    '0': exitProgram,
}

if __name__ == "__main__":
    main()
