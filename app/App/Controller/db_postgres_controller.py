from App import config
import psycopg2

database = config.configs['DB_NAME']
host = config.configs['DB_HOST']
user = config.configs['DB_USER']
port = config.configs['DB_PORT']
password = config.configs['DB_PASSWORD']

class PostgreSQL:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, database, user, password, port):
        if not hasattr(self, 'connection'):
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.port = port
            self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
    def execute_query(self, query, args=()):        
        cur = self.connection.cursor()
        cur.execute(query,args)
        self.connection.commit()  
        return cur
    
    
    def signupUser(self, username, user_id):
        query = "INSERT INTO users (id,username) VALUES (%s , %s)"
        args =(user_id,username)
        self.execute_query(query, args)
        return 'true' 
        
    
    # Add request to database
    def addReqToDb(self , user_id, type, j_params, time, uuid):
        query = "INSERT INTO request (user_id,type,params,time,status,uuid) VALUES (%s , %s , %s , %s , 'in queue' , %s) RETURNING uuid"
        args =(user_id, type, j_params, time, uuid)
        req_uuid = self.execute_query(query, args).fetchall()[0][0]
        return req_uuid 
    
    def updateInRequest(self, req_id, api_req_id, status):
        query = "UPDATE request set status=%s, api_req_id=%s WHERE uuid=%s"
        args = (status, api_req_id, req_id)
        res = self.execute_query(query,args)        
        return res        
    
    # Retrieve request info
    def getReqInfo(self, req_id):
        query = "SELECT * FROM request WHERE uuid=%s"
        args = (req_id,)
        res = self.execute_query(query,args).fetchall()
        return res
    
    # Retrieve process result
    def getReqRes(self, req_uuid,user_id):
        query = "SELECT result,status,type,api_req_id FROM request WHERE uuid=%s AND user_id=%s"
        args = (req_uuid,user_id)
        res = self.execute_query(query,args).fetchall()
        return res
      
    def updateResFromApi(self, status, result, req_uuid):
        query = 'UPDATE request SET status=%s , result=%s where uuid=%s'
        args = (status, result, req_uuid)
        self.execute_query(query,args)

    def changeParams(self, params, uuid):
        query = 'UPDATE request SET params=%s where uuid=%s'
        args = (params, uuid)
        self.execute_query(query,args)

    # Checks whether it is already registered or not
    def check_duplicate_id(self, id):
        query = "SELECT id FROM users WHERE id=%s"
        args = (id,)
        res = self.execute_query(query,args).fetchone()
        return res

    def addUserLocation(self, user_id, location):
        query = "UPDATE users set location=%s WHERE id=%s"
        args = (location, user_id )
        res = self.execute_query(query,args)        
        return res      
    
    def changeUserTextMessage(self, text_msg, user_id):
        query = "UPDATE users set text_msg=%s WHERE id=%s RETURNING text_msg, step"
        args = (text_msg, user_id )
        text = self.execute_query(query, args).fetchall()[0]
        return text
        
    def changeUserSecretMsg(self, value, user_id):
        query = "UPDATE users set value=%s WHERE id=%s"
        args = (value, user_id )
        text = self.execute_query(query, args)
        return text

    def getUserSecretMsg(self, user_id):
        query = "SELECT value FROM users WHERE id=%s"
        args = (user_id,)
        res = self.execute_query(query,args).fetchone()[0]
        return res

    def changeUserSTEP(self, new_step, user_id):
        query = "UPDATE users set step=%s WHERE id=%s"
        args = (new_step, user_id )
        self.execute_query(query, args)
        return 'true'


# Admin
    def admin_getUsersRequestsStatus(self):
        query = "SELECT status, COUNT(*) AS count FROM request GROUP BY status;"
        args = ()
        res = self.execute_query(query,args).fetchall()
        return res

    def admin_getAllReq(self, type1, type2):
        query = "SELECT COUNT(*) AS count FROM request WHERE type=%s OR type=%s ;"
        args = (type1, type2)
        res = self.execute_query(query,args).fetchall()
        return res

    
    def admin_userResDone(self, type, user_id):
        query = "SELECT user_id, id, status, params, result, uuid FROM request WHERE status='done' AND type=%s AND user_id=%s"
        args = (type,user_id)
        res = self.execute_query(query,args).fetchall()
        return res    

    def admin_userResQueue(self, type, user_id):
        query = "SELECT user_id, id, status, params, result, uuid FROM request WHERE status='in queue' AND type=%s AND user_id=%s"
        args = (type,user_id)
        res = self.execute_query(query,args).fetchall()
        return res    

    def admin_userResProcessing(self, type, user_id):
        query = "SELECT user_id, id, status, params, result, uuid FROM request WHERE status='processing' AND type=%s AND user_id=%s"
        args = (type,user_id)
        res = self.execute_query(query,args).fetchall()
        return res    

    
    def admin_resDone(self, type):
        query = "SELECT user_id, id, status, params, result, uuid FROM request WHERE status='done' AND type=%s"
        args = (type,)
        res = self.execute_query(query,args).fetchall()
        return res

    def admin_resProcessing(self, type):
        query = "SELECT user_id, id, status, params, result, uuid FROM request WHERE status='processing' AND type=%s"
        args = (type,)
        res = self.execute_query(query,args).fetchall()
        return res
    
    def admin_resQueue(self, type):
        query = "SELECT user_id, id, status, params, uuid FROM request WHERE request.status='in queue' AND request.type=%s"
        args = (type,)
        res = self.execute_query(query,args).fetchall()
        return res
    

    # Users info
    def admin_get_users_info(self):
        query = "SELECT id, username FROM users"
        args = ()
        res = self.execute_query(query,args).fetchall()
        return res
    # End users info
# End admin


db = PostgreSQL(host=host, database=database, user=user, password=password, port=port)
db.connect()