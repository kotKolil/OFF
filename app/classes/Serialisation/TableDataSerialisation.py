from app.classes.Serialisation.TableFieldsStorage import *

def UserFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        type_of_data = kwargs["format"]
        func_data = InputFunc(*args, **kwargs)
        if len(func_data[0]) > 1:

            if type_of_data == "obj":
                return [UserStorage([i], func_data[1]) for i in func_data[0]]
            elif type_of_data == "json":
                return [
                    {
                        "email": i[0],
                        "UserId": i[1],
                        "IsAdmin": i[2],
                        "IsBanned": i[3],
                        "LogoPath": i[4],
                        "citate": i[5],
                        "time": i[6],
                        "IsActivated": i[9],
                        "NumOfPosts": i[10]
                    }
                    for i in func_data[0]
                ]

            else:
                raise TypeError("Invalid format of output data")

        elif len(func_data[0]) == 1:
            # if not iterable
            if type_of_data == "obj":
                return UserStorage(func_data[0], func_data[1])
            elif type_of_data == "json":
                return {
                    "email": func_data[0][0][0],
                    "UserId": func_data[0][0][1],
                    "IsAdmin": func_data[0][0][2],
                    "IsBanned": func_data[0][0][3],
                    "LogoPath": func_data[0][0][4],
                    "citate": func_data[0][0][5],
                    "time": func_data[0][0][6],
                    "ActiveNum": func_data[0][0][8],
                    "IsActivated": func_data[0][0][9],
                    "NumOfPosts": func_data[0][0][10]
                }

        else:
            return 0

    return wrapper


def MessageFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        type_of_data = kwargs["format"]
        func_data = InputFunc(*args, **kwargs)

        try:

            if len(func_data[0]) > 1:
                if type_of_data == "obj":
                    return [MessagesStorage(i, func_data[1]) for i in func_data[0]]
                elif type_of_data == "json":
                    return [
                        {
                            "TopicId": i[0],
                            "MessageId": i[1],
                            "author": i[2],
                            "text": i[3],
                            "time": i[4]
                        }
                        for i in func_data[0]
                    ]
                else:
                    raise TypeError("Uknwon format of output data")
            else:
                if type_of_data == "obj":
                    return MessagesStorage(func_data[0][0], func_data[1])
                elif type_of_data == "json":
                    return {
                        "TopicId": func_data[0][0][0],
                        "MessageId": func_data[0][0][1],
                        "author": func_data[0][0][2],
                        "text": func_data[0][0][3],
                        "time": func_data[0][0][4]
                    }

        except Exception:

            return []

    return wrapper


def TopicFormatWrapper(InputFunc):
    def wrapper(*args, **kwargs):
        type_of_data = kwargs["format"]
        func_data = InputFunc(*args, **kwargs)

        if len(func_data[0]) == 0:
            return []
        elif len(func_data[0]) > 1:
            if type_of_data == "obj":
                return [
                    TopicStorage([i], func_data[1])
                    for i in func_data[0]
                ]
            elif type_of_data == "json":
                return [
                    {
                        "time": i[0],
                        "theme": i[1],
                        "author": i[2],
                        "about": i[3],
                        "TopicId": i[4],
                        "protected": i[5],
                    }
                    for i in func_data[0]
                ]

        else:
            if type_of_data == "obj":
                return TopicStorage(func_data[0], func_data[1])
            elif type_of_data == "json":
                return {
                    "time": func_data[0][0][0],
                    "theme": func_data[0][0][1],
                    "author": func_data[0][0][2],
                    "about": func_data[0][0][3],
                    "TopicId": func_data[0][0][4],
                    "protected": func_data[0][0][5],
                }
            else:
                raise TypeError("Unknown format of output data")

    return wrapper
