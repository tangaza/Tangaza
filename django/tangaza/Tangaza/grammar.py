
#Rudimentary parser

#Parse Rules
#***********

#0: split raw text into tokens

#Group commands
#**************
#2: if token[0] is a group command then 
#3: token[1] should be group name and token[2..n] = extras
#4: if token[0] begins with '@' (e.g. @xyz) then xyz is groupname, token[1] is group command, token[2..n] = extras
#5: if token[0] is not a group command check if its a group name and resolve. if not error
#6: if token[1] begins with @ (@xyz), drop '@' and use xyz as group name
#7: if token[0] is a group command and token[1] = the word 'group' drop token[1]
#8: if token[1] contains '@' assume token[1] = user@group [invite 0711@nrc, 0722@life, delete x@y, remove x@y]

#User commands?
#*************
#1: if token[0] is not a group command
#2: if token[0] contains @ then assume its a user command split it (abc@xyz)

def parse(tokens, language):
    '''
    Loops through the set of tokens and returns a dictionary of 
    group, command, member and extra text contained in the supplied text
    '''
    command = ''
    group = ''
    member = ''
    extras = []
    
    cmd = Commands(language)
    
    if len(tokens) <= 1:
        return [command, group, extras]
    
    if cmd.is_group_command(tokens[0]):
        command = tokens[0]    
        
        if tokens[1] == 'group':
            #e.g create group xyz
            #err: cant create a group called 'group'
            del tokens[1]
        if tokens[1].startswith('@'):
            #e.g create @xyz
            group = tokens[1].lstrip('@')
        elif tokens[1].__contains__('@'):
            #e.g delete user@xyz
            member, group = tokens[1].split('@')
        else:
            #e.g. create xyz
            group = tokens[1]
        
        extras = tokens[2:]
    elif cmd.is_user_command(tokens[0]):
        command = tokens[0]
        
        if tokens[1] == 'group':
            #e.g remove group xyz member
            #err: no group called 'group'
            del tokens[1]
        if len(tokens) > 2:
            if tokens[1].startswith('@'):
                #e.g remove @xyz member
                group = tokens[1].lstrip('@')
                member = tokens[2]
                extras = tokens[3:]
            elif tokens[-2] == 'from' or tokens[-2] == 'to':
                #e.g. invite abc to xyz
                #e.g. remove abc from xyz
                member = tokens[1]
                group = tokens[-1]
                #e.g. invite abc, abcd, abcde to xyz
                extras = tokens[2:-2]
                    
            elif tokens[2].startswith('@'):
                #e.g. remove member @xyz
                group = tokens[2].lstrip('@')
                member = tokens[1]
                extras = tokens[2:-1]
            else:
                #e.g. remove xyz member
                group = tokens[1]
                member = tokens[2]
                extras = tokens[3:]
        else:
            if tokens[1].__contains__('@'):
                #e.g remove member@xyz
                member, group = tokens[1].split('@')
            extras = tokens[2:]
    else:
        #e.g @xyz create, @xyz invite
        if tokens[0].startswith('@'):
            group = tokens[0].lstrip('@')
            
            if tokens[1] == 'group':
                del tokens[1]

            if cmd.is_group_command(tokens[1]):
                command = tokens[1]
                extras = tokens[2:]
            elif cmd.is_user_command(tokens[1]):
                #e.g. @xyz remove user
                if len(tokens) > 2:
                    command = tokens[1]
                    member = tokens[2]
                    extras = tokens[3:]
        else:
            #e.g. xyz create
            group = tokens[0]
            if tokens[1] == 'group':
                del tokens[1]
            
            if cmd.is_group_command(tokens[1]):
                command = tokens[1]
                extras = tokens[2:]
            elif cmd.is_user_command(tokens[1]):
                #e.g. xyz remove user
                if len(tokens) > 2:
                    command = tokens[1]
                    member = tokens[2]
                    extras = tokens[3:]
    
    #remove any punctuation in group name
    import string
    for p in string.punctuation:
        if p in group:
            group = group.replace(p, "")
    #TODO
    #loop through extras e.g. delete user1@xyz, user2@abc
    
    return {"command":command, 'group':group, 'member':member, 'extras':' '.join(extras)}

class Commands(object):
    
    def __init__(self, lang):
        self.GROUP_COMMANDS = [lang.CREATE, lang.JOIN, lang.LEAVE, lang.DELETE]
        self.USER_COMMANDS = [lang.REMOVE, lang.INVITE]
    
    def is_command(self, command):
        return is_group_command(command) or is_user_command(command)
    
    def is_group_command(self, command):
        return self.GROUP_COMMANDS.__contains__(command)
    
    def is_user_command(self, command):
        return self.USER_COMMANDS.__contains__(command)
