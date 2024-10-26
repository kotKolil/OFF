from .storage import *

import os

def UserFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        TypeOfData = kwargs["format"]
        FuncData = InputFunc(*args, **kwargs)
        if len(FuncData[0]) > 1:

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
                            "ActiveNum":i[8],
                            "IsActivated":i[9],
                            "NumOfPosts":i[10]
                        }
                            for i in FuncData[0]
                ]

            else:
                raise TypeError("Uknwon format of output data")
            
        elif len(FuncData[0]) == 1:
            #if not iterable
            if TypeOfData == "obj":
                return UserStorage(FuncData[0], FuncData[1])
            elif TypeOfData == "json":
                return {
                            "email":FuncData[0][0][0],
                            "UserId":FuncData[0][0][1],
                            "IsAdmin":FuncData[0][0][2],
                            "IsBanned":FuncData[0][0][3],
                            "LogoPath":FuncData[0][0][4],
                            "citate":FuncData[0][0][5],
                            "time":FuncData[0][0][6],
                            "ActiveNum":FuncData[0][0][8],
                            "IsActivated":FuncData[0][0][9],
                            "NumOfPosts": FuncData[0][0][10]
                        }
            
        else:
            return 0

    return wrapper



def MessageFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        TypeOfData = kwargs["format"]
        FuncData = InputFunc(*args, **kwargs)

        try:

            if len(FuncData[0]) > 1:
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
            else:
                if TypeOfData == "obj":
                    return MessagesStorage(FuncData[0][0], FuncData[1])
                elif TypeOfData == "json":
                    return {
                        "TopicId":FuncData[0][0][0],
                        "MesageId":FuncData[0][0][1],
                        "author":FuncData[0][0][2],
                        "text":FuncData[0][0][3],
                        "time":FuncData[0][0][4]
                    }


        except:

            return []

            
    return wrapper

def TopicFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        TypeOfData = kwargs["format"]
        FuncData = InputFunc(*args, **kwargs)



        if len(FuncData[0]) == 0:
            return []
        elif len(FuncData[0]) > 1 :
                if TypeOfData == "obj":
                    return [
                        TopicStorage(i, FuncData[1])
                        for i in FuncData[0]
                    ]
                elif TypeOfData == "json":
                    return [
                        {
                            "time": i[0],
                            "theme": i[1],
                            "author": i[2],
                            "about": i[3],
                            "TopicId": i[4]
                        }
                        for i in FuncData[0]
                    ]

        else:
            if TypeOfData == "obj":
                return TopicStorage(FuncData[0], FuncData[1])
            elif TypeOfData == "json":
                return {
                    "time":FuncData[0][0][0],
                    "theme":FuncData[0][0][1],
                    "author":FuncData[0][0][2],
                    "about":FuncData[0][0][3],
                    "TopicId":FuncData[0][0][4],


                }

    return wrapper