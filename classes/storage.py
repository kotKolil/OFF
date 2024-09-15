class UserStorage:

    def __init__(self, Data):

        self.email = Data[0]
        self.UserId = Data[1]
        self.IsAdmin = Data[2]
        self.IsBanned = Data[3]
        self.LogoPath = Data[4]
        self.citate = Data[4]
        self.time = Data[5]
        self.token = Data[6]
        
class TopicStorage:

    def __init__(self, Data):

        self.time = Data[0]
        self.theme = Data[1]
        self.author = Data[2]
        self.about = Data[3]
        self.TopicId = Data[4]
        
class MessagesStorage:

    def __init__(self, Data):

        self.TopicId = Data[0]
        self.MessageId = Data[1]
        self.author = Data[2]
        self.text = Data[3]
        self.time = Data[4]

