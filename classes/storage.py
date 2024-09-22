class UserStorage:

    def __init__(self, Data):

        self.email = Data[0][0]
        self.UserId = Data[0][1]
        self.IsAdmin = Data[0][2]
        self.IsBanned = Data[0][3]
        self.LogoPath = Data[0][4]
        self.citate = Data[0][5]
        self.time = Data[0][6]
        self.token = Data[0][7]
        
class TopicStorage:

    def __init__(self, Data):

        self.time = Data[0][0]
        self.theme = Data[0][1]
        self.author = Data[0][2]
        self.about = Data[0][3]
        self.TopicId = Data[0][4]
        
class MessagesStorage:

    def __init__(self, Data):

        self.TopicId = Data[0][0]
        self.MessageId = Data[0][1]
        self.author = Data[0][2]
        self.text = Data[0][3]
        self.time = Data[0][4]

