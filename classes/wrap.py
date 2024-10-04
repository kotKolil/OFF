from .storage import *

def UserFormatWrapper(InputFunc):
    def wrapper(*args):
        TypeOfData = args[2]
        UserData = InputFunc(args)
        if TypeOfData == "obj":
            return UserStorage(UserData[0], UserData[1])
        elif TypeOfData == "json":
            return {
                "email":UserData[0][0],
                "UserId":UserData[0][1],
                "IsAdmin":UserData[0][2],
                "IsBanned":UserData[0][3],
                "LogoPath":UserData[0][4],
                "citate":UserData[0][5],
                "time":UserData[0][6],
                "token":UserData[0][7],
                "ActiveNum":UserData[0][8],
                "IsActivated":UserData[0][9]
            }
        else:
            raise TypeError("Uknwon format of output data")

    return wrapper

def MessageFormatWrapper(InputFunc):
    def wrapper(*args):
        TypeOfData = args[2]
        MsgData = InputFunc(args)
        if TypeOfData == "obj":
            return MessagesStorage(MsgData[0], MsgData[1])
        elif TypeOfData == "json":
            return {
                "TopicId":MsgData[0][0],
                "MesageId":MsgData[0][1],
                "author":MsgData[0][2],
                "text":MsgData[0][3],
                "time":MsgData[0][4]
            }
        else:
            raise TypeError("Uknwon format of output data")