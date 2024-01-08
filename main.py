# MAIN starts at line 886
#class
class Dir:
    def __init__(self, path:list, permission:list, user:str) -> None:
        self.path = path
        self.exist = True
        self.permission = permission
        self.user = user
        self.hidden = False

    def get_path(self) -> list:
        return self.path
    
    def set_permission(self, perm:str, loc:int) -> list:
        self.permission[loc] = perm
        return self.permission

    def get_permission(self) -> list:
        return self.permission

    def is_exist(self) -> bool:
        return self.exist

    def set_exist(self, exist:bool) -> None:
        self.exist = exist
    
    def get_user(self) -> str:
        return self.user
    
    def set_user(self, user2:str) -> None:
        self.user = user2

    def is_hidden(self) -> bool:
        if self.get_path()[-1][0] == '.':
            self.hidden = True
        return self.hidden

    def ls(self, flag) -> str:
        a = ''.join(self.get_permission())
        b = self.get_user()
        c = self.get_path()

        #refer to dir itself
        if flag == '-l-d':
            return f'{a} {b} .'
        if flag == '-d': 
            return '.'
        if flag == '-l':
            return f'{a} {b} {c[-1]}'
            
        #refer to dir as .. of child
        if flag == '-p': #parent of child
            return '..'
        if flag == '-l-p':
            return f'{a} {b} ..'

#Function convert every path to absolute path
def full_path(path:str, pwd:str) -> list:
    if path == pwd and pwd == '/':
        return [['/'], ['/']]
    if path == '/':
        return [['/'], ['/']]
    else:
        path = path.split('/') #1: if '/' at front then it -> ''

    if pwd == '/':             
        pwd = [pwd]
    else:
        pwd = pwd.split('/') #there no way pwd w/o '/' at front
        pwd[0] = '/'
    
    i = 0
    while i < len(path):
        if i == 0 or i == (len(path)-1): 
            if path[i] != '' and path[i] != '.': #solve 1
                pwd.append(path[i])
        else:
            if path[i] != '.':
                pwd.append(path[i])
        i += 1
    
    #prefix 
    prefix = []
    for i in pwd:
        if i == '..' or i == '.':
            break
        prefix.append(i)

    i = 0
    while i < len(pwd): 
        #if there's a .., del it and its parent, if its parent isnt / or ..
        if pwd[i] == '..':
            pwd.pop(i)
            if pwd[i-1] != '/' and pwd[i-1] != '..':
                pwd.pop(i-1)
                i -= 2
            else:
                i -= 1                                   
        i += 1

    return [pwd, prefix]           

#Function to check if path exist
def check_exist(path:list, dlevel:list) -> bool:
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            if dlevel[i].is_exist() == True:
                return True
        i += 1         
    return False
    
#Function to check path permission <path already exist>
def check_permission(path:list, dlevel:list) -> list:
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            return dlevel[i].get_permission()
        i += 1  

#Function to set permission <path already exist>
def set_permission(perm:str, loc:int, path:list, dlevel:list):
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            dlevel[i].set_permission(perm, loc)
        i += 1  

#Function to return path name
def check_path_name(path:list, dlevel:list) -> list:
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            return dlevel[i].get_path()[-1]
        i += 1  

#Function to return info of path for ls
def get_info(path:list, dlevel:list, flag:str):
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            return dlevel[i].ls(flag)
        i += 1  

#Function to check path user
def check_user(path:list, dlevel:list) -> str:
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            return dlevel[i].get_user()
        i += 1 

#Function to check if it's a hidden file
def check_hidden(path:list, dlevel:list) -> bool:
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            return dlevel[i].is_hidden()
        i += 1          

#Function to set path exist from True to False
def set_exist(path:list, dlevel:list):
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            dlevel[i].set_exist(False)
        i += 1 

#Function to change path user
def set_user(path:list, dlevel:list, username:str):
    i = 0
    while i < len(dlevel): #file object
        if path == dlevel[i].get_path():
            dlevel[i].set_user(username)
        i += 1 

#Function to check if dir is empty (dir already exists)
def check_empty_dir(path: list, lv:list, dlevel:list) -> bool:
    empty = True
    #the len -1 of absolute file <path> represent what lv they are on
    
    #there are no next lv of current <path>
    if len(path) == len(lv):
        return True

    #check if next lv contains file that belongs to <path>
    lv = lv[len(path)]

    for i in lv:
        if check_exist(i, dlevel) == True:
            if i[:len(path)] == path:
                empty = False
    return empty  

#Function to ls
def ls(flag: list, path: list, raw: str, parent:list, lv:list, dlevel:list, user:str, is_dir:bool, no_path:bool, is_empty:bool):
    #dir is empty
    if is_empty == True:
        child_path = []
    #dir not empty
    else:
        lv = lv[len(path)]
        child_path = []
        for i in lv:
            if check_exist(i, dlevel) == True:
                if i[:len(path)] == path:
                    child_path.append(i)

        child_path = sorted(child_path)

    #ls + flag only
    if no_path == True:
        #Include Hidden
        if '-a' in flag:
            #ls [-a] [-d] [-l] <nothing>
            if '-d' in flag and '-l' in flag:
                print(get_info(path, dlevel, '-l-d'))

            #ls [-a] [-d] <nothing>
            elif '-d' in flag:
                print(get_info(path, dlevel, '-d'))

            #ls [-a] [-l] <nothing>
            elif '-l' in flag:
                print(get_info(path, dlevel, '-l-d'))
                print(get_info(parent, dlevel, '-l-p'))
                
                for i in child_path:
                    print(get_info(i, dlevel, '-l'))
            
            #ls [-a] <nothing>
            else:
                print(get_info(path, dlevel, '-d'))
                print(get_info(parent, dlevel, '-p'))

                for i in child_path:
                    print(check_path_name(i, dlevel))

        #Ignore hidden
        if '-a' not in flag:
            #ls [-d] [-l] <nothing>
            if '-d' in flag and '-l' in flag:
                pass

            #ls [-d] <nothing>   >edpost #1019
            elif '-d' in flag:
                pass

            #ls [-l] <nothing>
            elif '-l' in flag:
                for i in child_path:
                    if check_hidden(i, dlevel) == False:
                        print(get_info(i, dlevel, '-l'))

            #ls <nothing>
            else:
                for i in child_path:
                    if check_hidden(i, dlevel) == False:
                        print(check_path_name(i, dlevel))

    #ls + flag + path
    if no_path == False:
        #Include Hidden
        if '-a' in flag:
            #ls [-a] [-d] [-l] <path>
            if '-d' in flag and '-l' in flag:
                a = ''.join(check_permission(path, dlevel))
                b = check_user(path, dlevel)
                print(f'{a} {b} {raw}')

            #ls [-a] [-d] <path>
            elif '-d' in flag:
                print(raw)

            #ls [-a] [-l] <path>
            elif '-l' in flag:
                #a file
                if is_dir == False:
                    a = ''.join(check_permission(path, dlevel))
                    b = check_user(path, dlevel)
                    print(f'{a} {b} {raw}')
                #a dir
                else:
                    print(get_info(path, dlevel, '-l-d'))
                    print(get_info(parent, dlevel, '-l-p'))

                    for i in child_path:
                        print(get_info(i, dlevel, '-l'))

            #ls [-a] <path>
            else:
                #a file
                if is_dir == False:
                    print(raw)
                #a dir
                else:
                    print(get_info(path, dlevel, '-d'))
                    print(get_info(parent, dlevel, '-p'))

                    for i in child_path:
                        print(check_path_name(i, dlevel))
                
        #Ignore hidden
        if '-a' not in flag:
            #ls [-l] [-d] <path>
            if '-d' in flag and '-l' in flag:
                if check_hidden(path, dlevel) == False and raw[0] != '.':
                    a = ''.join(check_permission(path, dlevel))
                    b = check_user(path, dlevel)
                    print(f'{a} {b} {raw}')

            #ls [-l] <path>
            elif '-d' in flag:
                if check_hidden(path, dlevel) == False and raw[0] != '.':
                    print(raw)
                 
            #ls [-d] <path>
            elif '-l' in flag:
                #a file
                if is_dir == False:
                    if check_hidden(path, dlevel) == False and raw[0] != '.':
                        a = ''.join(check_permission(path, dlevel))
                        b = check_user(path, dlevel)
                        print(f'{a} {b} {raw}')
            
                #a dir
                else:
                    for i in child_path:
                        if check_hidden(i, dlevel) == False:
                            print(get_info(i, dlevel, '-l'))
            #ls <path>
            else:
                #a file
                if is_dir == False:
                    if check_hidden(path, dlevel) == False and raw[0] != '.':
                        print(raw)
                #a dir
                else:
                    for i in child_path:
                        if check_hidden(i, dlevel) == False:
                            print(check_path_name(i, dlevel))    
                            

#Function to chmod recursively
def chmod_r(user:list, sign:list, perm:list, path: list, lv:list, dlevel:list, user2:str, error:list):
    lv = lv[len(path):]
    
    child_path = []

    for i in lv:
        for p in i:
            if check_exist(p, dlevel) == True:
                if p[:len(path)] == path:
                    child_path.append(p)
    #recursion top_down
    #children of same parent are tied
    #edpost #997
    child_path = sorted(child_path)

    for baby in child_path:
        if baby != ['/']:
            p = '/'.join(baby[0])[1:]
        else:
            p = '/'.join(baby[0])
                
        dad = full_path(p+'/..', '/')

        cannot = False
        #current user is not path owner nor root
        if check_user(baby, dlevel) == user2 or user2 == 'root':
            pass
        else:
            error.append('chmod: Operation not permitted')
            cannot = True
        
        if cannot == False:
            chmod(user, sign, perm, baby, dlevel)

    for i in error:
        print(i)

#Function to chown recursively
def chown_r(path: list, lv:list, dlevel, username:str):
    lv = lv[len(path):]
    child_path = []
    
    for i in lv:
        for p in i:
            if check_exist(p, dlevel) == True:
                if p[:len(path)] == path:
                    child_path.append(p)

    for baby in child_path:
        set_user(baby, dlevel, username)

#Function to check ancestor permission <path already exists>
def ancestor_permission(path:list, dlevel:list, bit: str, user:str) -> bool:
    for i in range(0, len(path)):
        #base of current user then decide read from 'u' or 'o'
        if bit == 'x':
            if check_user(path, dlevel) == user:
                loc = 3
            else:
                loc = -1
        elif bit == 'w':
            if check_user(path, dlevel) == user:
                loc = 2
            else:
                loc = -2
        elif bit == 'r':
            if check_user(path, dlevel) == user:
                loc = 1
            else:
                loc = -3

        if check_permission(path, dlevel)[loc] != bit:
            return False

        path = path[: -1]

    return True

#Function to check if name is valid <single str>
def valid_name(name:str) -> bool:
    name = list(name)
    ls = []

    for i in name:
        if i.isalpha() == True or i == '-' or i == '.' or i == '_' or i == ' ':
            ls.append('x')
        elif i.isdigit() == True:
            ls.append('x')
        else:
            ls.append(i)

    ls2 = []
    for i in ls:
        if i != 'x':
            ls2.append(i)

    if ls2 == []:
        return True
    else:
        return False

    
#Function to check if smode of 'chmod' is valid <additional char> <+ - =>
def valid_name_chmod(name:str) -> bool:
    name = list(name)
    ls = []

    for i in name:
        if i.isalpha() == True or i == '-' or i == '.' or i == '_' or i == ' ':
            ls.append('x')
        elif i == '+' or i == '-' or i == '=':
            ls.append('x')
        elif i.isdigit() == True:
            ls.append('x')
        else:
            ls.append(i)

    ls2 = []
    for i in ls:
        if i != 'x':
            ls2.append(i)

    if ls2 == []:
        return True
    else:
        return False

#Function to check invalid syntax of absolute path 
#ie : ['/', 'a', 'b']
def check_invalid_cmd(path:list) -> bool:
    #ignore root
    for i in path[1:]:
        if valid_name(i) == False:
            return False

    return True

#Function to check if name of path already existed
def name_existed(name:str, existed_name:list) -> bool:
    if name not in existed_name:
        return False
    else:
        return True

#Function to check if user (ie adduser) already existed
def user_existed(user:str, existed_user:list) -> bool:
    if user not in existed_user:
        return False
    else:
        return True

#Function to remove path name (ie when remove file)
def rm_name(name:str, existed_name:list) -> list:
    if name in existed_name:
        index = existed_name.index(name)
        existed_name.pop(index)
    return existed_name

#Function to remove username (ie deluser)
def rm_user(user:str, existed_user:list) -> list:
    if user in existed_user:
        index = existed_user.index(user)
        existed_user.pop(index)
    return existed_user

#Function to parse name (with space) if its valid (cmd with 1 path only)
def valid_space_name(name:list,cmd:str, flag:str, with_flag:bool) -> list:
    #drop cmd off list
    name = name[len(cmd):]
    
    if with_flag == True:
        #drop until flag
        while True:
            if name[0] == ' ' or name[0] == '-':
                name = name[1:]
            elif name[0] == flag: #delete flag only occurs 1
                name = name[1:]
                break       

    #(from flag) drop ' ' until we reach smt
    while True:
        if name[0] == ' ':
            name = name[1:]
        else:
            break

    #(from end) drop ' ' until we reach smt
    while True:
        if name[-1] == ' ':
            name = name[:-1]
        else:
            break

    #too much arguments
    if name[0] != '"' or name[-1] != '"':
        return [name, False]
    #parsing argument
    else:
        name = name[1:-1]
        path = ''.join(name)
        return [path, True]

#Function to parse name (with space) if its valid (cmd with 2 paths only)
def valid_space_two_paths(name:list, cmd:str, flag:str, with_flag:bool) -> list:
    #drop cmd off list
    name = name[len(cmd):]
    
    #count number of quote
    count = 0
    for i in name:
        if i == '"':
            count += 1

    #quote number must be 2 or 4
    if count == 2 or count == 4:
        pass
    else:
        return [name, name, False] 
    
    if with_flag == True:
        #drop until flag
        while True:
            if name[0] == ' ' or name[0] == '-':
                name = name[1:]
            elif name[0] == flag: #delete flag only occurs 1
                name = name[1:]
                break       

    #(from flag) drop ' ' until we reach smt
    while True:
        if name[0] == ' ':
            name = name[1:]
        else:
            break

    #(from end) drop ' ' until we reach smt
    while True:
        if name[-1] == ' ':
            name = name[:-1]
        else:
            break

    #too much arguments
    if count == 4: #both 2 paths contain space
        if name[0] != '"' or name[-1] != '"':
            return [name, name, False]

    #remember: name now contains both path
    #too less arguments
    if count == 2: #only 1 path contains space
        if name[0] == '"' and name[-1] == '"':
            return [name, name, False]

    #determine index of "
    i = 0
    index = []
    while i < len(name):
        if name[i] == '"':
            index.append(i)
        i += 1

    #only 1 path contains space
    if count == 2:
        #first path contains space
        if name[0] == '"':
            path1 = name[index[0]+1:index[1]]
            path2 = name[index[1]+1:]
            if path2[0] != ' ':
                return [name, name, False]
            #from path1 drop ' ' until we reach smt
            while True:
                if path2[0] == ' ':
                    path2 = path2[1:]
                else:
                    break

            jpath1 = ''.join(path1)
            jpath2 = ''.join(path2)

            return [jpath1, jpath2, True]

        #second path contains space
        elif name[-1] == '"':
            path1 = name[index[0]+1:index[1]]
            path2 = name[:index[0]]
            if path2[-1] != ' ':
                return [name, name, False]
            #from path2 drop ' ' until we reach smt
            while True:
                if path2[-1] == ' ':
                    path2 = path2[:-1]
                else:
                    break

            jpath1 = ''.join(path1)
            jpath2 = ''.join(path2)
            return [jpath2, jpath1, True]

        else:
            return [name, name, False]

    #both paths contain space
    if count == 4:
        #if theres no space between 2 paths -> 1 argument
        #too less argument
        if index[1] + 1 == index[2]:
            return [name, name, False]
            
        #check if  between 2 paths is just space
        space = name[index[1]+1:index[2]]
        for i in space:
            if i != ' ':
                return [name, name, False]

        path1 = name[index[0]+1:index[1]]
        path2 = name[index[2]+1:index[3]]
        jpath1 = ''.join(path1)
        jpath2 = ''.join(path2)
    
        return [jpath1, jpath2, True]


#Function to mkdir with flag -p
def mkdir(path:list, existed_name:list, dlevel: list, user:str, count:int, lv2:list):
    copy = []
    blank = []
    #copy of path
    for i in path:
        if i != '/':
            copy.append(i)

    #check in path whether there is a name that has been created by touch or mkdir
    not_found = True
    while len(copy) != 0:
        if copy[-1] in existed_name:
            dst = path.index(copy[-1]) + 1
            not_found = False
            break
        copy = copy[:-1]
    
    #name(s) of path have existed 
    if not_found == False:
        path2 = path[:dst]
        
        #name existed but path not exists
        #cut path until we reach smt exists
        while True:
            if check_exist(path2, dlevel) == False:
                dst -= 1
                path2 = path[:dst]
            else:
                break
        

        #check user
        if check_user(path2, dlevel) == user:
            bit_w = 2
        else:
            bit_w = -2

        #check permission 'w' on <parent>
        if check_permission(path2, dlevel)[bit_w] != 'w':
            if user != 'root':
                return [count, lv2] #permission denied create nothing
                    
        #check permission 'x' on <ancestors>
        if ancestor_permission(path2, dlevel, 'x', user) == False:
            if user != 'root':
                return [count, lv2] #permission denied create nothing

        #continue make dir from existed dir
        i = 1
        while i < len(path[dst:]) + 1:
            dlevel.append([])
            dlevel[count] = Dir(path[:dst+i], ['d', 'r', 'w', 'x', 'r', '-', 'x'], user)
            existed_name.append(dlevel[count].get_path()[-1])
            lv2 = full_level(lv2, dlevel[count].get_path())
            count += 1
            i += 1

    #name(s) of path not exist and surely start from root
    #root face no permission denied
    if not_found == True:
        if path == ['/']:
            return [count, lv2]

        #make dir  
        i = 1
        while i < len(path):
            dlevel.append([])
            dlevel[count] = Dir(path[:1+i],['d', 'r', 'w', 'x', 'r', '-', 'x'], user)
            existed_name.append(dlevel[count].get_path()[-1])
            lv2 = full_level(lv2, dlevel[count].get_path())
            count += 1
            i += 1
        
    return [count, lv2]

#Function to change permission <chmod>
def chmod(user:list, sign:list, perm:list, path:list, dlevel:list):
    if 'a' in user:
        if sign[0] == '+':
            if 'r' in perm:
                set_permission('r', 1, path, dlevel)
                set_permission('r', -3, path, dlevel)
            if 'w' in perm:
                set_permission('w', 2, path, dlevel)
                set_permission('w', -2, path, dlevel)
            if 'x' in perm:
                set_permission('x', 3, path, dlevel)
                set_permission('x', -1, path, dlevel)

        elif sign[0] == '=':
            set_permission('r', 1, path, dlevel)
            set_permission('r', -3, path, dlevel)
            set_permission('w', 2, path, dlevel)
            set_permission('w', -2, path, dlevel)
            set_permission('x', 3, path, dlevel)
            set_permission('x', -1, path, dlevel)
            if 'r' not in perm:
                set_permission('-', 1, path, dlevel)
                set_permission('-', -3, path, dlevel)
            if 'w' not in perm:
                set_permission('-', 2, path, dlevel)
                set_permission('-', -2, path, dlevel)
            if 'x' not in perm:
                set_permission('-', 3, path, dlevel)
                set_permission('-', -1, path, dlevel)

            
        elif sign[0] == '-':
            if 'r' in perm:
                set_permission('-', 1, path, dlevel)
                set_permission('-', -3, path, dlevel)
            if 'w' in perm:
                set_permission('-', 2, path, dlevel)
                set_permission('-', -2, path, dlevel)
            if 'x' in perm:
                set_permission('-', 3, path, dlevel)
                set_permission('-', -1, path, dlevel)

        #perm empty, clear all per bits for <?> candidates edpost #632

        if perm == [] or 0 in perm:
            if sign[0] == '=':
                set_permission('-', 1, path, dlevel)
                set_permission('-', 2, path, dlevel)
                set_permission('-', 3, path, dlevel)
                set_permission('-', -3, path, dlevel)
                set_permission('-',-2, path, dlevel)                
                set_permission('-', -1, path, dlevel)

        return

    if 'u' in user:
        if sign[0] == '+':
            if 'r' in perm:
                set_permission('r', 1, path, dlevel) 
            if 'w' in perm:
                set_permission('w', 2, path, dlevel)          
            if 'x' in perm:
                set_permission('x', 3, path, dlevel)

        elif sign[0] == '=':
            set_permission('r', 1, path, dlevel)
            set_permission('w', 2, path, dlevel)
            set_permission('x', 3, path, dlevel)
            if 'r' not in perm:
                set_permission('-', 1, path, dlevel)
            if 'w' not in perm:
                set_permission('-', 2, path, dlevel)
            if 'x' not in perm:
                set_permission('-', 3, path, dlevel)
     
        elif sign[0] == '-':
            if 'r' in perm:
                set_permission('-', 1, path, dlevel)  
            if 'w' in perm:
                set_permission('-', 2, path, dlevel)
            if 'x' in perm:
                set_permission('-', 3, path, dlevel)

        if perm == [] or 0 in perm:
            if sign[0] == '=':
                set_permission('-', 1, path, dlevel)
                set_permission('-', 2, path, dlevel)
                set_permission('-', 3, path, dlevel)

    if 'o' in user:
        if sign[0] == '+':
            if 'r' in perm:
                set_permission('r', -3, path, dlevel)
            if 'w' in perm:
                set_permission('w', -2, path, dlevel)
            if 'x' in perm:
                set_permission('x', -1, path, dlevel)

        elif sign[0] == '=':
            set_permission('r', -3, path, dlevel)
            set_permission('w', -2, path, dlevel)
            set_permission('x', -1, path, dlevel)
            if 'r' not in perm:
                set_permission('-', -3, path, dlevel)
            if 'w' not in perm:
                set_permission('-', -2, path, dlevel)
            if 'x' not in perm:
                set_permission('-', -1, path, dlevel)
            
        elif sign[0] == '-':
            if 'r' in perm:
                set_permission('-', -3, path, dlevel)
            if 'w' in perm:
                set_permission('-', -2, path, dlevel)
            if 'x' in perm:
                set_permission('-', -1, path, dlevel)

        #perm empty, clear all per bits for <?> candidates edpost #632

        if perm == [] or 0 in perm:
            if sign[0] == '=':
                set_permission('-', -3, path, dlevel)
                set_permission('-',-2, path, dlevel)
                set_permission('-', -1, path, dlevel)

#Function to update lv (full path)
#ie current = [['/']] <lv 0>
#add ['/','a'] <lv 1>
# lv = [['/'], [['/','a']]]
def full_level(lv, path):
    #ensure that current lv contains enough lv to contains path
    while True:
        if len(path) > len(lv):
            lv.append([])
        else:
            break

    a = len(path)
    lv[a-1].append(path)
    return lv

#MAIN
def main():
    #default
    user = 'root'
    pwd = '/'

    #contains every dir (absolute form)
    #refer as lv
    lv2 = [['/']]

    #Initialize list of name/user
    existed_name = []
    existed_user = ['root']

    #Initialize Dir class
    count = 1
    dlevel = [[]]

    #root #every permission
    dlevel[0] = Dir(['/'], ['d', 'r', 'w', 'x', 'r', '-', 'x'],user) 

    #Start while
    while True:
        a = input(user+':'+pwd+'$ ')
        b = a.split()

        if len(b) == 0:
            continue

        #exit
        elif b[0] == 'exit':
            if len(b) == 1:
                print(f'bye, {user}')
                break
            #too many arguments
            else:
                print(f'{b[0]}: Invalid syntax')
                continue

        #pwd
        elif b[0] == 'pwd':
            if len(b) == 1:
                print(f'{pwd}')
                continue
            #too many arguments
            else:
                print(f'{b[0]}: Invalid syntax')
                continue
    
        #cd <dir>
        elif b[0] == 'cd':
            #too few arguments
            if len(b) == 1: 
                print(f'{b[0]}: Invalid syntax')
                continue

            #cd and path (surely no space)
            if len(b) == 2: 
                path = b[1]
                if path[0] == '"' and path[-1] == '"':
                    path = path[1:-1]

            #argument > 2
            elif len(b) > 2:
                name = list(a)
                #too many arguments
                if valid_space_name(name,b[0],'x', False)[1] == False:
                    print(f'{b[0]}: Invalid syntax')
                    continue

                #name with space
                else:
                    path = valid_space_name(name,b[0],'x', False)[0]
           
            if path == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #is a relative path
            if path[0] != '/':
                #convert to absolute path
                pathc = full_path(path, pwd)
            #already an absolute path
            else:
                #is root
                if path == '/':
                    pathc = full_path(path, '/')
                #not root
                else:
                    pathc = full_path(path+'/.', '/')

            #check if file path valid
            if check_invalid_cmd(pathc[0]) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            #Path/prefix not exists
            if check_exist(pathc[0], dlevel) == False or check_exist(pathc[1], dlevel) == False:
                print('cd: No such file or directory')
                continue

            #Path exists
            else:
                #check user
                if check_user(pathc[0], dlevel) == user:
                    bit_x = 3
                else:
                    bit_x = -1

                #check path is a file
                if check_permission(pathc[0], dlevel)[0] == '-':
                    print('cd: Destination is a file')
                    continue
                
                #check permission 'x' on <dir>
                if check_permission(pathc[0], dlevel)[bit_x] != 'x':
                    if user != 'root':
                        print(f'{b[0]}: Permission denied') 
                        continue

                #Path satified, change pwd to path
                if pathc[0] != ['/']:
                    pwd = '/'.join(pathc[0])[1:]
                else:
                    pwd = '/'.join(pathc[0])
                  
            
        #mkdir [-p] <dir>      
        elif b[0] == 'mkdir':

            #too few arguments
            if len(b) == 1:
                print(f'{b[0]}: Invalid syntax')
                continue

            #with flag -p
            elif (len(b) > 2 and b[1] == '-p') or (len(b) > 2 and b[1] == '"-p"'):
                with_p = True
                #mkdir, 1 flag and path (surely no space)
                if len(b) == 3:
                    path = b[2]
                    if path[0] == '"' and path[-1] == '"':
                        path = path[1:-1]

                #argument > 2 and -p is specified
                else:
                    if b[1] == '"-p"':
                        a = a.replace('"-p"', '-p', 1)

                    name = list(a)
                    #too many arguments
                    if valid_space_name(name,b[0],'p', True)[1] == False:
                        print(f'{b[0]}: Invalid syntax')
                        continue
                    #name with space
                    else:
                        path = valid_space_name(name,b[0],'p', True)[0]

            #with no flag -p
            else:
                with_p = False
                #mkdir and path (no_space)
                if len(b) ==  2:
                    path = b[1]
                    if path[0] == '"' and path[-1] == '"':
                        path = path[1:-1]

                #argument > 2 and -p not specified
                else:
                    name = list(a)

                    #too many arguments
                    if valid_space_name(name,b[0],'x', False)[1] == False:
                        print(f'{b[0]}: Invalid syntax')
                        continue
                    #name with space
                    else:
                        path = valid_space_name(name,b[0],'x', False)[0]   

            if path == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #is a relative path
            if path[0] != '/':
                #convert to absolute path
                pathc = full_path(path, pwd)
            #already an absolute path
            else:
                #is root
                if path == '/':
                    pathc = full_path(path, '/')
                #not root
                else:
                    pathc = full_path(path+'/.', '/')

            #check if file path valid
            if check_invalid_cmd(pathc[0]) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if pathc[0] != ['/']:
                p = '/'.join(pathc[0])[1:]
            else:
                p = '/'.join(pathc[0])
                
            #parent dir
            prepathc = full_path(p+'/..', '/')

            #if -p not specified
            if with_p == False:

                #parent dir exist -> ancestor dir also exist
                if check_exist(prepathc[0], dlevel) == True:
                    
                    #check user
                    if check_user(prepathc[0], dlevel) == user:
                        bit_w = 2
                    else:
                        bit_w = -2

                    #A file cannot mkdir
                    if check_permission(prepathc[0], dlevel)[0] == '-':
                        continue

                    #check permission 'w' on <parent>
                    if check_permission(prepathc[0], dlevel)[bit_w] != 'w':
                        if user != 'root':
                            print(f'{b[0]}: Permission denied')
                            continue
                    
                    #check permission 'x' on <ancestors>
                    if ancestor_permission(prepathc[0], dlevel, 'x', user) == False:
                        if user != 'root':
                            print(f'{b[0]}: Permission denied')
                            continue

                    #dir intended to create already exist:
                    if check_exist(pathc[0], dlevel) == True:
                        print('mkdir: File exists')
                        continue
        
                    #create dir
                    else:
                        dlevel.append([])
                        dlevel[count] = Dir(pathc[0], ['d', 'r', 'w', 'x', 'r', '-', 'x'], user)
                        existed_name.append(dlevel[count].get_path()[-1])
                        lv2 = full_level(lv2, dlevel[count].get_path())
                        count += 1
                        
                #parent dir not exists and so the ancestor dir
                else:
                    print('mkdir: Ancestor directory does not exist')
                    continue

            if with_p == True:
                finished = mkdir(pathc[0], existed_name, dlevel, user, count, lv2)
                count = finished[0]
                lv2 = finished[1]

        #touch <file>
        elif b[0] == 'touch':
            #too few arguments
            if len(b) == 1:
                print(f'{b[0]}: Invalid syntax')
                continue

            #only touch and file name (w/o space)
            if len(b) == 2: 
                path = b[1]
                if path[0] == '"' and path[-1] == '"':
                    path = path[1:-1]

            #argument > 2
            elif len(b) > 2:
                name = list(a)
                #too many arguments
                if valid_space_name(name,b[0],'x', False)[1] == False:
                    print(f'{b[0]}: Invalid syntax')
                    continue
                #name with space
                else:
                    path = valid_space_name(name,b[0],'x', False)[0]

            if path == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #is a relative path
            if path[0] != '/':
                #convert to absolute path
                pathc = full_path(path, pwd)
            #already an absolute path
            else:
                #is root
                if path == '/':
                    pathc = full_path(path, '/')
                #not root
                else:
                    pathc = full_path(path+'/.', '/')

            #check if file path valid
            if check_invalid_cmd(pathc[0]) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if pathc[0] != ['/']:
                p = '/'.join(pathc[0])[1:]
            else:
                p = '/'.join(pathc[0])
                
            #parent dir
            prepathc = full_path(p+'/..', '/')

            #parent dir exist and so ancestor dir
            if check_exist(prepathc[0], dlevel) == True:

                #check user
                if check_user(prepathc[0], dlevel) == user:
                    bit_w = 2
                else:
                    bit_w = -2

                #A file cannot touch
                if check_permission(prepathc[0], dlevel)[0] == '-':
                    print('touch: Ancestor directory does not exist')
                    continue

                #check permission 'w' <parent>
                if check_permission(prepathc[0], dlevel)[bit_w] != 'w':
                    if user != 'root':
                        print(f'{b[0]}: Permission denied')
                        continue

                #check permission 'x' <ancestors>
                if ancestor_permission(prepathc[0], dlevel, 'x', user) == False:
                    if user != 'root':
                        print(f'{b[0]}: Permission denied')
                        continue

                #file already exist:
                if check_exist(pathc[0], dlevel) == True:
                    continue
                #file not exist, create file
                else:
                    dlevel.append([])
                    dlevel[count] = Dir(pathc[0], ['-', 'r', 'w', '-', 'r', '-', '-'], user)
                    existed_name.append(dlevel[count].get_path()[-1])
                    lv2 = full_level(lv2, dlevel[count].get_path())
                    count += 1
                    
            #parent dir not exist and so ancestor dir
            else:
                print('touch: Ancestor directory does not exist')
                continue

        #cp <src> <dst>
        elif b[0] == 'cp':
            #too few arguments
            if len(b) == 1 or len(b) == 2:
                print(f'{b[0]}: Invalid syntax')
                continue

            #only cp and 2 file paths (w/o space)
            elif len(b) == 3:
                src = b[1]
                dst = b[2]
                if src[0] == '"' and src[-1] == '"':
                    src = src[1:-1]
                if dst[0] == '"' and dst[-1] == '"':
                    dst = dst[1:-1]
            
            elif len(b) > 3:
                name = list(a)
                if valid_space_two_paths(name, 'cp', 'x', False)[2] == False:
                    #too many/few arguments
                    print(f'{b[0]}: Invalid syntax')
                    continue
                else:
                    src = valid_space_two_paths(name, 'cp', 'x', False)[0]
                    dst = valid_space_two_paths(name, 'cp', 'x', False)[1]

            if src == '' or dst == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #<src> is a relative path
            if src[0] != '/':
                #convert to absolute path
                copy = full_path(src, pwd)
            #<src> already an absolute path
            else:
                #is root
                if src == '/':
                    copy = full_path(src, '/')
                #not root
                else:
                    copy = full_path(src+'/.', '/')

            #<dst> is a relative path
            if dst[0] != '/':
                #convert to absolute path
                paste = full_path(dst, pwd)
            #<dst> already an absolute path
            else:
                #is root
                if dst == '/':
                    paste = full_path(dst, '/')
                #not root
                else:
                    paste = full_path(dst+'/.', '/')

            #check if file path valid
            if check_invalid_cmd(copy[0]) == False or check_invalid_cmd(paste[0]) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if copy[0] != ['/']:
                c = '/'.join(copy[0])[1:]
            else:
                c = '/'.join(copy[0])

            if paste[0] != ['/']:
                p = '/'.join(paste[0])[1:]
            else:
                p = '/'.join(paste[0])

            #parent dir
            c_parent = full_path(c+'/..', '/')
            p_parent = full_path(p+'/..', '/')

            #Path/prefix not exists <src>
            if check_exist(copy[0], dlevel) == False or check_exist(copy[1], dlevel) == False:
                print('cp: No such file')
                continue

            #dst already exists 
            if check_exist(paste[0], dlevel) == True:
                #dst is dir
                if check_permission(paste[0], dlevel)[0] != '-':
                    print('cp: Destination is a directory')
                    continue
                else:
                    print('cp: File exists')
                    continue
            
            #same file name
            if copy[0][-1] == paste[0][-1]:
                print('cp: File exists')
                continue

            #src is dir
            if check_permission(copy[0], dlevel)[0] != '-':
                print('cp: Source is a directory')
                continue

            #Parent <dst> not exist 
            if check_exist(p_parent[0], dlevel) == False:
                print('cp: No such file or directory')
                continue

            #parent <dst> must be dir
            if check_permission(p_parent[0], dlevel)[0] != 'd':
                print('cp: No such file or directory')
                continue

            #check user <src>
            if check_user(copy[0], dlevel) == user:
                cbit_r = 1
            else:
                cbit_r = -3

            #check user parent <dst>
            if check_user(p_parent[0], dlevel) == user:
                pbit_w = 2
            else:
                pbit_w = -2

            #check permission 'r' on <src>
            if check_permission(copy[0], dlevel)[cbit_r] != 'r':
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #check permission 'x' on <ancestors> <src>
            if ancestor_permission(c_parent[0], dlevel, 'x', user) == False:
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #check permission 'x' on <ancestors> <dst>
            if ancestor_permission(p_parent[0], dlevel, 'x', user) == False:
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue
            
            #check permission 'w' on <parent> <dst>
            if check_permission(p_parent[0], dlevel)[pbit_w] != 'w':
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #create file
            dlevel.append([])
            dlevel[count] = Dir(paste[0], ['-', 'r', 'w', '-', 'r', '-', '-'], user)
            existed_name.append(dlevel[count].get_path()[-1])
            lv2 = full_level(lv2, dlevel[count].get_path())
            count += 1

        #mv <src> <dst>
        elif b[0] == 'mv':
            #too few arguments
            if len(b) == 1 or len(b) == 2:
                print(f'{b[0]}: Invalid syntax')
                continue

            #only mv and 2 file paths (w/o space)
            elif len(b) == 3:
                src = b[1]
                dst = b[2]
                if src[0] == '"' and src[-1] == '"':
                    src = src[1:-1]
                if dst[0] == '"' and dst[-1] == '"':
                    dst = dst[1:-1]
            
            elif len(b) > 3:
                name = list(a)
                if valid_space_two_paths(name, 'mv', 'x', False)[2] == False:
                    #too many/few arguments
                    print(f'{b[0]}: Invalid syntax')
                    continue
                else:
                    src = valid_space_two_paths(name, 'mv', 'x', False)[0]
                    dst = valid_space_two_paths(name, 'mv', 'x', False)[1]

            if src == '' or dst == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #<src> is a relative path
            if src[0] != '/':
                #convert to absolute path
                copy = full_path(src, pwd)
            #<src> already an absolute path
            else:
                #is root
                if src == '/':
                    copy = full_path(src, '/')
                #not root
                else:
                    copy = full_path(src+'/.', '/')

            #<dst> is a relative path
            if dst[0] != '/':
                #convert to absolute path
                paste = full_path(dst, pwd)
            #<dst> already an absolute path
            else:
                #is root
                if dst == '/':
                    paste = full_path(dst, '/')
                #not root
                else:
                    paste = full_path(dst+'/.', '/')

            #check if file path valid
            if check_invalid_cmd(copy[0]) == False or check_invalid_cmd(paste[0]) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if copy[0] != ['/']:
                c = '/'.join(copy[0])[1:]
            else:
                c = '/'.join(copy[0])

            if paste[0] != ['/']:
                p = '/'.join(paste[0])[1:]
            else:
                p = '/'.join(paste[0])

            #parent dir
            c_parent = full_path(c+'/..', '/')
            p_parent = full_path(p+'/..', '/')


            #dst already exists 
            if check_exist(paste[0], dlevel) == True:
                #dst is dir
                if check_permission(paste[0], dlevel)[0] != '-':
                    print('mv: Destination is a directory')
                    continue
                else:
                    print('mv: File exists')
                    continue
            
            #dst not exist but same file name
            if copy[0][-1] == paste[0][-1]:
                print('mv: File exists')
                continue

            #Path/prefix not exists <src>
            if check_exist(copy[0], dlevel) == False or check_exist(copy[1], dlevel) == False:
                print('mv: No such file')
                continue

            #src is dir
            if check_permission(copy[0], dlevel)[0] != '-':
                print('mv: Source is a directory')
                continue

            #Parent <dst> not exist 
            if check_exist(p_parent[0], dlevel) == False:
                print('mv: No such file or directory')
                continue

            #parent <dst> must be dir
            if check_permission(p_parent[0], dlevel)[0] != 'd':
                print('mv: No such file or directory')
                continue

            #check user <src>
            if check_user(c_parent[0], dlevel) == user:
                cbit_w = 2
            else:
                cbit_w = -2

            #check user <dst>
            if check_user(p_parent[0], dlevel) == user:
                pbit_w = 2
            else:
                pbit_w = -2

            #check permission 'x' on <ancestors> <src>
            if ancestor_permission(c_parent[0], dlevel, 'x', user) == False:
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #check permission 'w' on <parent> <src>
            if check_permission(c_parent[0], dlevel)[cbit_w] != 'w':
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #check permission 'x' on <ancestors> <dst>
            if ancestor_permission(p_parent[0], dlevel, 'x', user) == False:
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #check permission 'w' on <parent> <dst>
            if check_permission(p_parent[0], dlevel)[pbit_w] != 'w':
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #delete <src> existence/ name
            set_exist(copy[0], dlevel)
            existed_name = rm_name(copy[0][-1], existed_name)

            #create file
            dlevel.append([])
            dlevel[count] = Dir(paste[0], ['-', 'r', 'w', '-', 'r', '-', '-'], user)
            existed_name.append(dlevel[count].get_path()[-1])
            lv2 = full_level(lv2, dlevel[count].get_path())
            count += 1

        elif b[0] == 'rm':
            #too few arguments
            if len(b) == 1:
                print(f'{b[0]}: Invalid syntax')
                continue

            #only rm and path (w/o space)
            elif len(b) == 2:
                path = b[1]
                if path[0] == '"' and path[-1] == '"':
                    path = path[1:-1]

            elif len(b) > 2:
                name = list(a)
                #too many arguments
                if valid_space_name(name,b[0],'x', False)[1] == False:
                    print(f'{b[0]}: Invalid syntax')
                    continue
                #name with space
                else:
                    path = valid_space_name(name,b[0],'x', False)[0]

            if path == '':
                print(f'{b[0]}: Invalid syntax')
                continue
            
            #is a relative path
            if path[0] != '/':
                #convert to absolute path
                pathc = full_path(path, pwd)
            #already an absolute path
            else:
                #is root
                if path == '/':
                    pathc = full_path(path, '/')
                #not root
                else:
                    pathc = full_path(path+'/.', '/')

            #check if file path valid
            if check_invalid_cmd(pathc[0]) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if pathc[0] != ['/']:
                p = '/'.join(pathc[0])[1:]
            else:
                p = '/'.join(pathc[0])
                
            #parent dir
            prepathc = full_path(p+'/..', '/')

            #if path not exist
            if check_exist(pathc[0], dlevel) == False or check_exist(pathc[1], dlevel) == False:
                print('rm: No such file')
                continue
                
            #if path is dir
            if check_permission(pathc[0], dlevel)[0] != '-':
                print('rm: Is a directory')
                continue

            #check user 
            if check_user(pathc[0], dlevel) == user:
                bit_w = 2
            else:
                bit_w = -2

            #check user <parent>
            if check_user(prepathc[0], dlevel) == user:
                dbit_w = 2
            else:
                dbit_w = -2

            #check permission 'w' on <path>
            if check_permission(pathc[0], dlevel)[bit_w] != 'w':
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #check permission 'x' on <ancestors>
            if ancestor_permission(prepathc[0], dlevel, 'x', user) == False:
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #check permission 'w' on <parent>
            if check_permission(prepathc[0], dlevel)[dbit_w] != 'w':
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #delete <path> existence/ name
            set_exist(pathc[0], dlevel)
            existed_name = rm_name(pathc[0][-1], existed_name)

        elif b[0] == 'rmdir':
            #too few arguments
            if len(b) == 1:
                print(f'{b[0]}: Invalid syntax')
                continue

            #only rmdir and path (w/o space)
            elif len(b) == 2:
                path = b[1]
                if path[0] == '"' and path[-1] == '"':
                    path = path[1:-1]

            elif len(b) > 2:
                name = list(a)
                #too many arguments
                if valid_space_name(name,b[0],'x', False)[1] == False:
                    print(f'{b[0]}: Invalid syntax')
                    continue
                #name with space
                else:
                    path = valid_space_name(name,b[0],'x', False)[0]

            if path == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #is a relative path
            if path[0] != '/':
                #convert to absolute path
                pathc = full_path(path, pwd)
            #already an absolute path
            else:
                #is root
                if path == '/':
                    pathc = full_path(path, '/')
                #not root
                else:
                    pathc = full_path(path+'/.', '/')

            #check if file path valid
            if check_invalid_cmd(pathc[0]) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if pathc[0] != ['/']:
                p = '/'.join(pathc[0])[1:]
            else:
                p = '/'.join(pathc[0])
                
            #parent dir
            prepathc = full_path(p+'/..', '/')

            #Prefix/dir not exists
            if check_exist(pathc[0], dlevel) == False or check_exist(pathc[1], dlevel) == False:
                print('rmdir: No such file or directory')
                continue
            
            if pwd == pathc[0]:
                print('rmdir: Cannot remove pwd')
                continue
            
            #Is root or is a file (not a dir)
            if check_permission(pathc[0], dlevel)[0] == '-':
                print('rmdir: Not a directory')
                continue

            #dir is not empty
            if check_empty_dir(pathc[0], lv2, dlevel) == False:
                print('rmdir: Directory not empty')
                continue

            #dir is current pwd
            cpwd = full_path('.', pwd)

            if pathc[0] == cpwd[0]:
                print('rmdir: Cannot remove pwd')
                continue

            #check user 
            if check_user(prepathc[0], dlevel) == user:
                bit_w = 2
            else:
                bit_w = -2

            #check permission 'x' on <ancestors>
            if ancestor_permission(prepathc[0], dlevel, 'x', user) == False:
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #check permission 'w' on <parent>
            if check_permission(prepathc[0], dlevel)[bit_w] != 'w':
                if user != 'root':
                    print(f'{b[0]}: Permission denied')
                    continue

            #remove dir
            set_exist(pathc[0], dlevel)
            existed_name = rm_name(pathc[0][-1], existed_name)
        
        #chmod [-r] <s> <path>
        elif b[0] == 'chmod':
            #too few arguments
            if len(b) < 3:
                print(f'{b[0]}: Invalid syntax')
                continue

            #with no flag -r
            if b[1] != '-r' and b[1] != '"-r"':
                with_r = False
                
                #chmod <s> <no_space path> 
                if len(b) == 3:
                    perm = b[1]
                    path = b[2]
                    if perm[0] == '"' and perm[-1] == '"':
                        perm = perm[1:-1]
                    if path[0] == '"' and path[-1] == '"':
                        path = path[1:-1]

                #chmod <s> <path with_space>
                elif len(b) > 3:
                    name = list(a)

                    if valid_space_two_paths(name, b[0], 'x', False)[2] == False:
                        #too many/few arguments
                        print(f'{b[0]}: Invalid syntax')
                        continue
                    else:
                        perm = valid_space_two_paths(name, b[0], 'x', False)[0]
                        path = valid_space_two_paths(name, b[0], 'x', False)[1]  

            #with flag -r
            elif b[1] == '-r' or b[1] == '"-r"':
                with_r = True

                if len(b) < 4:
                    #too few arguments
                    print(f'{b[0]}: Invalid syntax')
                    continue

                #chmod [-r] <s> <no_space path>
                if len(b) == 4:
                    perm = b[2]
                    path = b[3]
                    if perm[0] == '"' and perm[-1] == '"':
                        perm = perm[1:-1]
                    if path[0] == '"' and path[-1] == '"':
                        path = path[1:-1]

                #chmod [-r] <s> <path with_space>
                elif len(b) > 4:
                    if b[1] == '"-r"':
                        a = a.replace('"-r"', '-r', 1)
                    name = list(a)

                    if valid_space_two_paths(name, b[0], 'r', True)[2] == False:
                        #too many/few arguments
                        print(f'{b[0]}: Invalid syntax')
                        continue
                    else:
                        perm = valid_space_two_paths(name, b[0], 'r', True)[0]
                        path = valid_space_two_paths(name, b[0], 'r', True)[1] 

            if path == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #is a relative path
            if path[0] != '/':
                #convert to absolute path
                fpath = full_path(path, pwd)
            #already an absolute path
            else:
                #is root
                if path == '/':
                    fpath = full_path(path, '/')
                #not root
                else:
                    fpath = full_path(path+'/.', '/')
          
            #check if cmd valid
            if check_invalid_cmd(fpath[0]) == False or valid_name_chmod(perm) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if fpath[0] != ['/']:
                p = '/'.join(fpath[0])[1:]
            else:
                p = '/'.join(fpath[0])
                
            #parent dir
            prepathf = full_path(p+'/..', '/')

            #error file to print out alphabetically
            chmod_error = []

            #check if path exists
            if check_exist(fpath[0], dlevel) == True:

                #current user is not path owner nor root
                if check_user(fpath[0], dlevel) == user or user == 'root':
                    pass
                else:
                    if with_r == False:
                        print(f'{b[0]}: Operation not permitted')
                        continue
                    else:
                        chmod_error.append('chmod: Operation not permitted')

                #check permission 'x' on <ancestors>
                if ancestor_permission(prepathf[0], dlevel, 'x', user) == False:
                    if with_r == False:
                        if user != 'root':
                            print(f'{b[0]}: Permission denied')
                            continue
                    else:
                        if user != 'root':
                            chmod_error.append('chmod: Permission denied')

            #path not exist
            else:
                print(f'{b[0]}: No such file or directory')
                continue

            #extract <s> [uoa...][-+=][perms...]
            full_perm = list(perm)

            all_perm = [] #[perms...]
            all_user = [] #[uoa...]
            sign = [] #[-+=]
            perm_zero = []
            other = []

            for i in full_perm: 
                #user
                if i == 'a' or i == 'o' or i == 'u':
                    if i not in all_user:
                        all_user.append(i)
                    if i in all_user:
                        if len(sign) != 0:
                            other.append(i)
                #sign
                elif i == '+' or i == '-' or i == '=':
                    sign.append(i)
                #permission
                elif i == 'r' or i == 'w' or i == 'x':
                    if i not in all_perm:
                        all_perm.append(i)
                elif i == '0':
                    perm_zero.append(0)
                else:
                    other.append(i)
         
            #mode string <s> is invalid
            #1: more than 1 sign [+ - =]
            if len(sign) != 1:
                print(f'{b[0]}: Invalid mode')
                continue

            #2: both 0 and r-w-x co-exist
            if len(perm_zero) != 0 and len(all_perm) != 0:
                print(f'{b[0]}: Invalid mode')
                continue

            #4: exist non-related command 
            if len(other) != 0:
                print(f'{b[0]}: Invalid mode')
                continue

            #5: no change to any user
            if len(all_user) == 0: 
                print(f'{b[0]}: Invalid mode')
                continue
            
            fuser = sorted(all_user) #['a','o','u']
            fperm = sorted(all_perm) #['r','w','x ] or [0] or []

            #add zero if exist
            if len(perm_zero) != 0:
                fperm.append(0)

            #without flag -r
            if with_r == False:
                chmod(fuser, sign, fperm, fpath[0], dlevel)
            
            #with flag -r
            if with_r == True:
                if check_user(fpath[0], dlevel) == user or user == 'root':
                    chmod(fuser, sign, fperm, fpath[0], dlevel)
                chmod_r(fuser, sign, fperm, fpath[0], lv2, dlevel, user, sorted(chmod_error))
                
        #chown [-r] <s> <path>
        elif b[0] == 'chown':
            #current user isn't root
            if user != 'root':
                print('chown: Operation not permitted')
                continue

            #too few arguments
            if len(b) < 3:
                print(f'{b[0]}: Invalid syntax')
                continue

            #with no flag -r
            if b[1] != '-r' and b[1] != '"-r"':
                with_r = False
                
                #chown <s> <no_space path> 
                if len(b) == 3:
                    username = b[1]
                    path = b[2]
                    if username[0] == '"' and username[-1] == '"':
                        username = username[1:-1]
                    if path[0] == '"' and path[-1] == '"':
                        path = path[1:-1]

                #chown <s> <path with_space>
                elif len(b) > 3:
                    name = list(a)

                    if valid_space_two_paths(name, b[0], 'x', False)[2] == False:
                        #too many/few arguments
                        print(f'{b[0]}: Invalid syntax')
                        continue
                    else:
                        username = valid_space_two_paths(name, b[0], 'x', False)[0]
                        path = valid_space_two_paths(name, b[0], 'x', False)[1]  

            #with flag -r
            elif b[1] == '-r' or b[1] == '"-r"':
                with_r = True

                if len(b) < 4:
                    #too few arguments
                    print(f'{b[0]}: Invalid syntax')
                    continue

                #chown [-r] <s> <no_space path>
                if len(b) == 4:
                    username = b[2]
                    path = b[3]
                    if username[0] == '"' and username[-1] == '"':
                        username = username[1:-1]
                    if path[0] == '"' and path[-1] == '"':
                        path = path[1:-1]

                #chown [-r] <s> <path with_space>
                elif len(b) > 4:
                    if b[1] == '"-r"':
                        a = a.replace('"-r"', '-r', 1)
                    name = list(a)

                    if valid_space_two_paths(name, b[0], 'r', True)[2] == False:
                        #too many/few arguments
                        print(f'{b[0]}: Invalid syntax')
                        continue
                    else:
                        username = valid_space_two_paths(name, b[0], 'r', True)[0]
                        path = valid_space_two_paths(name, b[0], 'r', True)[1] 

            if path == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #is a relative path
            if path[0] != '/':
                #convert to absolute path
                fpath = full_path(path, pwd)
            #already an absolute path
            else:
                #is root
                if path == '/':
                    fpath = full_path(path, '/')
                #not root
                else:
                    fpath = full_path(path+'/.', '/')
          
            #check if cmd valid
            if check_invalid_cmd(fpath[0]) == False or valid_name(username) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            #user does not exist
            if user_existed(username, existed_user) == False:
                print(f'chown: Invalid user')
                continue

            #check if path exists
            if check_exist(fpath[0], dlevel) == False:
                print(f'{b[0]}: No such file or directory')
                continue

            #without flag -r
            if with_r == False: 
                set_user(fpath[0], dlevel, username)

            #with flag -r
            if with_r == True:
                set_user(fpath[0], dlevel, username)
                chown_r(fpath[0], lv2, dlevel, username)
                

        #adduser <user>
        elif b[0] == 'adduser':
            if len(b) == 1:
                print(f'{b[0]}: Invalid syntax')
                continue

            #adduser and <no_space username>
            elif len(b) == 2:
                username = b[1]
                if username[0] == '"' and username[-1] == '"':
                    username = username[1:-1]
            
            #adduser and <username with_space>
            elif len(b) > 2:
                name = list(a)
                #too many arguments
                if valid_space_name(name,b[0],'x', False)[1] == False:
                    print(f'{b[0]}: Invalid syntax')
                    continue
                #name with space
                else:
                    username = valid_space_name(name,b[0],'x', False)[0]

            if username == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #check if user name valid
            if valid_name(username) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if user_existed(username, existed_user) == True:
                print(f'{b[0]}: The user already exists')
                continue

            if user != 'root':
                print(f'{b[0]}: Operation not permitted')
                continue

            existed_user.append(username)


        #deluser <user>
        elif b[0] == 'deluser':
            if len(b) == 1:
                print(f'{b[0]}: Invalid syntax')
                continue

            #deluser and <no_space username>
            elif len(b) == 2:
                username = b[1]
                if username[0] == '"' and username[-1] == '"':
                    username = username[1:-1]
            
            #deluser and <username with_space>
            elif len(b) > 2:
                name = list(a)
                #too many arguments
                if valid_space_name(name,b[0],'x', False)[1] == False:
                    print(f'{b[0]}: Invalid syntax')
                    continue
                #name with space
                else:
                    username = valid_space_name(name,b[0],'x', False)[0]

            if username == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #check if user name valid
            if valid_name(username) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if user_existed(username, existed_user) == False:
                print(f'{b[0]}: The user does not exist')
                continue

            if user != 'root':
                print(f'{b[0]}: Operation not permitted')
                continue

            if username == 'root':
                print('WARNING: You are just about to delete the root account')
                print('Usually this is never required as it may render the whole system unusable')
                print('If you really want this, call deluser with parameter --force')
                print('(but this `deluser` does not allow `--force`, haha)')
                print('Stopping now without having performed any action')
                continue
           
            existed_user = rm_user(username, existed_user)

        
        #su <user>
        elif b[0] == 'su':
            #only su
            if len(b) == 1:
                user = 'root'
                continue

            #su and <no_space username>
            elif len(b) == 2:
                username = b[1]
                if username[0] == '"' and username[-1] == '"':
                    username = username[1:-1]
            
            #su and <username with_space>
            elif len(b) > 2:
                name = list(a)
                #too many arguments
                if valid_space_name(name,b[0],'x', False)[1] == False:
                    print(f'{b[0]}: Invalid syntax')
                    continue
                #name with space
                else:
                    username = valid_space_name(name,b[0],'x', False)[0]

            if username == '':
                print(f'{b[0]}: Invalid syntax')
                continue

            #check if user name valid
            if valid_name(username) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            if user_existed(username, existed_user) == False:
                print(f'{b[0]}: Invalid user')
                continue
           
            user = username

        elif b[0] == 'ls':
            flag = []
            index = [] #index of every flag 
            #add all flag -<smt> in 1 list
            for i in b:
                if len(i) == 2 or len(i) == 4:
                    if i[0] == '-' or i[:2] == '"-':
                        if i not in flag:
                            index.append(b.index(i))
                            if i == '-a' and '-a' not in flag:
                                flag.append('-a')
                            if i == '-d' and '-d' not in flag:
                                flag.append('-d')
                            if i == '-l' and '-l' not in flag:
                                flag.append('-l')
                            if i == '"-a"' and '-a' not in flag:
                                flag.append('-a')
                            if i == '"-d"' and '-d' not in flag:
                                flag.append('-d')
                            if i == '"-l"' and '-l' not in flag:
                                flag.append('-l')
            
            #check if any flag -<smt> is invalid 
            #ie: ls -e
            no_invalid_flag = True
            for i in flag:
                if i == '-a' or i == '-d' or i == '-l':
                    pass
                elif i == '"-a"' or i == '"-d"' or i == '"-l"':
                    pass
                else:
                    #too many arguments <invalid flag>
                    no_invalid_flag = False
            
            if no_invalid_flag == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            #there exist a non flag beteen flags
            #ie: ls -a e -f
            if len(flag) > 0:
                extras = []
                for i in b:
                    if i in flag or i == 'ls':
                        pass
                    else:
                        extras.append(i)
            
                #the last flag index
                flag_end = max(index)

                #check if everything beside ls and flag <sit outside flag range>
                invalid_char = False
                for i in extras:
                    if b.index(i) < flag_end:
                        invalid_char = True

                if invalid_char == True:
                    print(f'{b[0]}: Invalid syntax')
                    continue
            

            #1: NO PATH
            #path is pwd (flag or no flag)
            if len(b) == 1 or len(b) == len(flag) + 1:
                #path existed
                path = pwd
                
                #already an existed/ valid/ absolute path
                #is root
                if path == '/':
                    pathf = full_path(path, '/')
                    parentf = full_path(path, '/')
                #not root
                else:
                    pathf = full_path(path+'/.', '/')
                    parentf = full_path(path+'/..', '/')

                #pwd always a dir
                is_dir = True
                is_empty = check_empty_dir(pathf[0], lv2, dlevel)
                
                #ls <nopath = True>
                ls(flag, pathf[0], pathf[0], parentf[0], lv2, dlevel, user, is_dir, True, is_empty)
                

            #2: INCL PATH
            #ls + flag and path
            elif len(b) >= len(flag) + 2:
               
                #path <no_space>
                if len(b) == len(flag) + 2:
                    path = b[-1]
                    if path[0] == '"' and path[-1] == '"':
                         path = path[1:-1]

                #path <with_space>
                else:
                    name = list(a)
                    #contains flags
                    if len(flag) > 0:
                        last_flag = b[max(index)]        
                
                        if valid_space_name(name, 'ls', last_flag[-1], True)[1] == False:
                            print(f'{b[0]}: Invalid syntax')
                            continue
                        else:
                            path = valid_space_name(name,'ls', last_flag[-1], True)[0]
                    #0 flag
                    else:
                        if valid_space_name(name, 'ls', 'x', False)[1] == False:
                            print(f'{b[0]}: Invalid syntax')
                            continue
                        else:
                            path = valid_space_name(name,'ls', 'x', False)[0]

                if path == '':
                    print(f'{b[0]}: Invalid syntax')
                    continue

                #is a relative path
                if path[0] != '/':
                    #convert to absolute path
                    pathf = full_path(path, pwd)
                #already an absolute path
                else:
                    #is root
                    if path == '/':
                        pathf = full_path(path, '/')
                    #not root
                    else:
                        pathf = full_path(path+'/.', '/')

                #check if file path valid
                if check_invalid_cmd(pathf[0]) == False and pathf[0] != ['/']:
                    print(f'{b[0]}: Invalid syntax')
                    continue
                
                if pathf[0] != ['/']:
                    p = '/'.join(pathf[0])[1:]
                else:
                    p = '/'.join(pathf[0])
                
                #parent dir
                parent = full_path(p+'/..', '/')

                #path exists
                if check_exist(pathf[0], dlevel) == True:
                    #check user <path>
                    if check_user(pathf[0], dlevel) == user:
                        bit_r = 1
                    else:
                        bit_r = -3

                    #check user <parent>
                    if check_user(parent[0], dlevel) == user:
                        pbit_r = 1
                    else:
                        pbit_r = -3
       
                    #valid dir
                    if check_permission(pathf[0], dlevel)[0] == 'd':
                        is_dir = True
                        #check permission 'r' of <path>
                        if check_permission(pathf[0], dlevel)[bit_r] != 'r':
                            if user != 'root':
                                print(f'{b[0]}: Permission denied')
                                continue

                        #check permission 'r' of <parent>, only when '-d'
                        if '-d' in flag:
                            if check_permission(parent[0], dlevel)[pbit_r] != 'r':
                                if user != 'root':
                                    print(f'{b[0]}: Permission denied')
                                    continue
                    
                    #valid file
                    if check_permission(pathf[0], dlevel)[0] == '-':
                        is_dir = False
                        #check permission 'r' of <parent>
                        if check_permission(parent[0], dlevel)[pbit_r] != 'r':
                            if user != 'root':
                                print(f'{b[0]}: Permission denied')
                                continue
                    
                    #check permission 'x' on user bit of ancestors
                    if ancestor_permission(parent[0], dlevel, 'x', user) == False:
                        if user != 'root':
                            print(f'{b[0]}: Permission denied')
                            continue

                #path not exists
                else:
                    print('ls: No such file or directory')
                    continue

                is_empty = check_empty_dir(pathf[0], lv2, dlevel)
                
                #ls <nopath = False>
                ls(flag, pathf[0], path, parent[0], lv2, dlevel, user, is_dir, False, is_empty)
            
            
        else:
            if valid_name(b[0]) == False:
                print(f'{b[0]}: Invalid syntax')
                continue

            print(f'{b[0]}: Command not found')
            continue
            
if __name__ == '__main__':
    main()   