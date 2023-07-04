from flask_app.config.mysqlconnection import connectToMySQL

class Message():
    def __init__(self,data):
        self.id = data['id']
        self.message = data['message']
        self.created_at = data['cerated_at']
        self.updated_at = data['updated_at']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.receiver_id = data['receiver_id']
        self.receiver = data['receiver']
    
    @classmethod
    def save(cls,data):
        query ='insert into messages(message,sender_id,sender,receiver_id,receiver) values(%(message)s,%(sender_id)s,%(sender)s,%(receiver_id)s,%(receiver)s);'
        return connectToMySQL('walls_schema').query_db(query,data)
    
    @classmethod
    def show_messages(cls,data):
        query ='SELECT * from messages where receiver_id = %(id)s'
        result = connectToMySQL('walls_schema').query_db(query,data)    
        return result
    
    @classmethod
    def delete(cls,data):
        query='DELETE FROM messages WHERE i d = %(id)s'
        return connectToMySQL('walls_schema').query_db(query,data)