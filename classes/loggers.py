from abc import *


class abc_log(ABC):
    
    @abstractclassmethod
    def __init__(self, filename,p4th):
        self.__p4th = p4th
        self.__filename = filename



    @abstractmethod
    def log_message(text):
        pass


class txt_log(abc_log):
    
    def __init__(self, filename,p4th):
        super().__init__(filename,p4th)


    def log_message(self, text):
        try:
            with open(self.__p4th + self.__filename, "r") as file:
                file.write(text)
                file.close()

            return 1
        except Exception as e:
            return [str(e), 0]
        