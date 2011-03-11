
#Rudimentary parser

def decompose(tokens, language):
    command = None
    group = None
    member = None
    extras = []
    
    cmd = Commands(language)
    
    if len(tokens) < 1:
        return [command, group, extras]
    
    if len(tokens) > 1:
        command = tokens[0]
        group = tokens[1]
        
    if cmd.is_group_command(tokens[0]):
        command = tokens[0]
        #e.g create group xyz
        if tokens[1] == 'group':
            tokens.remove('group')
            #err: cant create a group called 'group'
        #e.g create @xyz
        if tokens[1].startswith('@'):
            group = token[0].lstrip('@')
        elif:
            #e.g delete user@xyz
            tokens[1].__contains__('@')
            member, group = tokens[1].split('@')
        else:
            #e.g. create xyz
            group = tokens[1]
            
        extras = tokens[2:]
    else:
        #e.g @xyz create, @xyz invite
        if token[0].startswith('@'):
            group = token[0].lstrip('@')
            
            if cmd.is_group_command(token[1]):
                command = token[1]
                extras = tokens[2:]
        else:
            #e.g. xyz create
            group = tokens[0]
            if cmd.is_group_command(token[1]):
                command = token[1]
                extras = tokens[2:]
    else:
        #hopefully we get here
        pass
    
    #TODO
    #loop through extras e.g. delete user1@xyz, user2@abc
    
    return {"command":command, 'group':group, 'member':member, 'extras':extras}

class Commands(object):
    
    def __init__(self, lang):
        self.GROUP_COMMANDS = [lang.CREATE, lang.INVITE, lang.JOIN, lang.LEAVE]
        self.USER_COMMANDS = []
        
    def is_command(command):
        return is_group_command(command) or is_user_command(command)
    
    def is_group_command(command):
        return self.GROUP_COMMANDS.__contains__(command)
    
    def is_user_command(command):
        return self.USER_COMMANDS.__contains__(command)
