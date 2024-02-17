import zope.interface

class IModelMethod(zope.interface.Interface):
    #they represented http methods for classes 

    def all():
        pass
    def create():
        pass
    def get():
        pass
    def delete():
        pass
    def update():
        pass
    
