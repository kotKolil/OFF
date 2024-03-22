class IDataBase:

	def __init__(self, object):
		self.__object = object

	def execute_query(self, query):
		return self.__object.execute_query(query)


class  ILogger:

        def __init__(self, object):
                self.__object = object

        def log(self, message):
                return self.__object.log(message)
