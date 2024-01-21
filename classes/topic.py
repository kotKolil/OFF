from abcd_classes import *
from tools import *

#place, where user write message

class topic(sub_disscussion):
    
    def __init__(self, time_of_creation, theme,author,about, sb_id):
        super.__init__(time_of_creation, theme,author,about, sb_id)


    # structure of table topic time_of_creation|theme|author|about|sb_id

    def get(self, mess_id):
        return self.db.execute_query(f"SELECT FROM messages WHERE id_thd = '{mess_id} ORDER BY time_sending' ")
    
    def delete(self, mess_id):
        return self.db.execute_query(F"DELETE FROM messages WHERE id_thd = '{mess_id}'")

    def update(self,id_thd,text):

        # structure of table messages: id_thread, message_id, author, text, time_of_publication
        return self.db.excute_query(f"UPDATE messages SET text='{text}' , 
                                    time_of_publication='{get_current_time()}'  WHERE id_thread='{id_thd}'")