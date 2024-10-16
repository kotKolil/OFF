class UserStorage:

    def __init__(self, Data, DBWorker):
        self.DBWorker = DBWorker

        self.email = Data[0][0]
        self.UserId = Data[0][1]
        self.IsAdmin = Data[0][2]
        self.IsBanned = Data[0][3]
        self.LogoPath = Data[0][4]
        self.citate = Data[0][5]
        self.time = Data[0][6]
        self.IsActivated = Data[0][9]
        self.ActiveNum = Data[0][-2]

    def save(self):
        self.DBWorker(query = """UPDATE user SET email = ?, UserId = ?, IsAdmin = ?, IsBanned = ?, LogoPath = ?, citate = ?, time = ?, ActiveNum = ?, IsActivated = ? WHERE UserId = ?""", param = (self.email, self.UserId, self.IsAdmin,
                       self.IsBanned, self.LogoPath, self.citate, self.time, self.ActiveNum, self.IsActivated, self.UserId))
        
class TopicStorage:

    def __init__(self, Data, DBWorker):
        self.DBWorker = DBWorker

        self.time = Data[0][0]
        self.theme = Data[0][1]
        self.author = Data[0][2]
        self.about = Data[0][3]
        self.TopicId = Data[0][4]
    
    def save(self):
        self.DBWorker(query = "UPDATE topic SET time = ?, theme = ?, author = ?, about = ?, TopicId = ? WHERE TopicId = ? ", param = (self.time,  self.theme, 
                      self.author,  self.about, self.TopicId, self.TopicId ))
        
class MessagesStorage:

    def __init__(self, Data, DBWorker):
        self.DBWorker = DBWorker

        self.TopicId = Data[0][0]
        self.MessageId = Data[0][1]
        self.author = Data[0][2]
        self.text = Data[0][3]
        self.time = Data[0][4]

    def save(self):
        self.DBWorker(query = "UPDATE messages SET TopicId = ?, MessageId = ?, author = ?, text = ?, time = ?", param =  (self.TopicId, self.MessageId, self.author,
                                                                                                                           self.text, self.time) )
