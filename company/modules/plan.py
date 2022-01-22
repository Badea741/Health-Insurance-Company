from company import db


class Plan:
    def __init__(self):
        self.ids = []
        self.types = []
        self.customers = []

    def insert(self, customerSsn, type):
        if type not in ['Basic', 'Premium', 'Golden']:
            return 'Invalid plan type'
        if customerSsn == None:
            db(f"INSERT INTO plan VALUES(0,null,'{type}')")
            return
        checkExist = db(
            f"SELECT customer_ssn FROM customer WHERE customer_ssn={customerSsn}")
        if checkExist == []:
            return 'Customer not found'
        db(f"INSERT INTO plan VALUES(0,'{customerSsn}','{type}')")
    
    def delete(self, plan_id):
        checkExist = db(f"SELECT plan_id FROM plan WHERE plan_id={plan_id}")
        if checkExist == []:
            return 'The plan you are trying to delete doesn\'t exist'
        db(f"DELETE FROM plan WHERE plan_id={plan_id}")
    
    def update(self, key, value, predicate):
        db(f"UPDATE plan SET {key}='{value}' WHERE {predicate}")
        
    def checkExist(self,planId):
        planIds=db(f"SELECT plan_id FROM plan WHERE plan_id={planId}")
        return planIds != []
        
    def getType(self,planId):
        return db(f"SELECT type FROM plan WHERE plan_id={planId}")[0][0]
    
    def getInfo(self):
        data=db('SELECT * FROM plan')
        for tuple in data:
            self.ids.append(tuple[0])
            self.customers.append(tuple[1])
            self.types.append(tuple[2])
            
    def refresh(self):
        self.getInfo()
