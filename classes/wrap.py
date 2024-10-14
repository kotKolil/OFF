from .storage import *

import os

def UserFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        TypeOfData = kwargs["format"]
        FuncData = InputFunc(*args, **kwargs)
        if len(FuncData[0]) == 0:
            return 0
        elif len(FuncData[0]) > 1:

            if TypeOfData == "obj":
                return [ UserStorage(i[0], FuncData[1])  for i in FuncData[0]  ]
            elif TypeOfData == "json":
                return [
                            {
                            "email":i[0],
                            "UserId":i[1],
                            "IsAdmin":i[2],
                            "IsBanned":i[3],
                            "LogoPath":i[4],
                            "citate":i[5],
                            "time":i[6],
                            "token":i[7],
                            "ActiveNum":i[8],
                            "IsActivated":i[9],
                        }
                            for i in FuncData[0]
                ]

            else:
                raise TypeError("Uknwon format of output data")
            
        else:
            #if not iterable

            if TypeOfData == "obj":
                return UserStorage(FuncData[0], FuncData[1])
            elif TypeOfData == "json":
                os.system("cls")
                print(FuncData[0])
                return                             {
                            "email":FuncData[0][0][0],
                            "UserId":FuncData[0][0][1],
                            "IsAdmin":FuncData[0][0][2],
                            "IsBanned":FuncData[0][0][3],
                            "LogoPath":FuncData[0][0][4],
                            "citate":FuncData[0][0][5],
                            "time":FuncData[0][0][6],
                            "token":FuncData[0][0][7],
                            "ActiveNum":FuncData[0][0][8],
                            "IsActivated":FuncData[0][0][9]
                        }

    return wrapper

def MessageFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        TypeOfData = args[1]
        FuncData = InputFunc(*args, **args)
        try:
            iter(FuncData)
            if TypeOfData == "obj":
                return [ MessagesStorage(i[0], FuncData[1]) for i in FuncData[0] ]
            elif TypeOfData == "json":
                return [
                        {
                        "TopicId":i[0],
                        "MesageId":i[1],
                        "author":i[2],
                        "text":i[3],
                        "time":i[4]
                    }
                for i in FuncData[0]
            ]
            else:
                raise TypeError("Uknwon format of output data")
        except TypeError:
            if TypeOfData == "obj":
                return MessagesStorage(FuncData[0], FuncData[1])
            elif TypeOfData == "json":
                return {
                    "TopicId":FuncData[0][0],
                    "MesageId":FuncData[0][1],
                    "author":FuncData[0][2],
                    "text":FuncData[0][3],
                    "time":FuncData[0][4]
                }
            
    return wrapper

def TopicFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        TypeOfData = args[1]
        FuncData = InputFunc(*args, **args)
        
        try:
            iter(FuncData[0])
            
            if TypeOfData == "obj":
                return [
                    MessagesStorage(i, FuncData[1]) 
                    for i in FuncData[0]
                ]
            elif TypeOfData == "json":
                return [
                    {
                        # TopicId, MessageId, author, text, time_of_publication
                        "TopicId": i[0],
                        "MessageId": i[1],
                        "author": i[2],
                        "text": i[3],
                        "time_of_publication": i[4]
                    }
                    for i in FuncData[0]
                ]
        
        except TypeError:
            if TypeOfData == "obj":
                return MessagesStorage(FuncData[0], FuncData[1])
            elif TypeOfData == "json":
                return {
                    "TopicId":FuncData[0][0],
                    "MessageId":FuncData[0][1],
                    "author":FuncData[0][2],
                    "text":FuncData[0][3],
                    "time_of_publication":FuncData[0][4]
                }

    return wrapper
