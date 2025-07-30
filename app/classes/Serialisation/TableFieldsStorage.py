import os


class UserStorage:

    def __init__(self, Data, DBWorker):
        self.DBWorker = DBWorker

        self.__OldUserId = Data[0][1]

        self.email = Data[0][0]
        self.UserId = Data[0][1]
        self.IsAdmin = Data[0][2]
        self.IsBanned = Data[0][3]
        self.LogoPath = Data[0][4]
        self.citate = Data[0][5]
        self.time = Data[0][6]
        self.token = Data[0][7]
        self.ActiveNum = Data[0][8]
        self.IsActivated = Data[0][9]
        self.NumOfPosts = Data[0][10]

    def save(self):
        print(self.UserId)
        self.DBWorker(
            query="""UPDATE user SET email = ?, UserId = ?, IsAdmin = ?, IsBanned = ?, LogoPath = ?, citate = ?, 
            time = ?, ActiveNum = ?, IsActivated = ?, NumOfPosts = ?, token = ? WHERE UserId = ?""",
            param=[self.email, self.UserId, self.IsAdmin,
                   self.IsBanned, self.LogoPath, self.citate, self.time, self.ActiveNum, self.IsActivated,
                   self.NumOfPosts, self.token, self.__OldUserId])

        self.__OldUserId = self.UserId


class TopicStorage:

    def __init__(self, Data, DBWorker):
        self.DBWorker = DBWorker

        self.time = Data[0][0]
        self.theme = Data[0][1]
        self.author = Data[0][2]
        self.about = Data[0][3]
        self.TopicId = Data[0][4]
        self.protected = Data[0][5]
        self.image = Data[0][6]

    def save(self):
        self.DBWorker(query="UPDATE topic SET theme = ?, about = ?, Protected = ? WHERE TopicId = ? ",
                      param=[self.theme, self.about, self.protected, self.TopicId])


class MessagesStorage:

    def __init__(self, Data, DBWorker):
        self.DBWorker = DBWorker

        self.TopicId = Data[0]
        self.MessageId = Data[1]
        self.author = Data[2]
        self.text = Data[3]
        self.time = Data[4]
        self.image = Data[5]

    def save(self):
        self.DBWorker(query="UPDATE messages SET TopicId = ?, author = ?, text = ?, time = ? WHERE MessageId = ? ",
                      param=(self.TopicId, self.author, self.text, self.time, self.MessageId))
