from abcd_classes import *

#groupes of themes for discushions
class topic(sub_disscussion):
    
    def __init__(self, time_of_creation, theme,author,about, sb_id, db:object):
        super.__init__(time_of_creation, theme,author,about, sb_id , db)
        db.excute("")


    def get(self,id_thd):
        return self.db.execute_query(f'SELECT * FROM topics WHERE id={id_thd}')
    
    def delete(self, id_thd):
        return self.db.excute_query(f"DELETE FROM topics WHERE id={id_thd}")
    
    def update(self,id_thd,name, decrpt):
        return self.db.excute_query("UPDATE topic SET name='{name}', decrpt='{decrpt}' WHERE id_thd='{id_thd}'")