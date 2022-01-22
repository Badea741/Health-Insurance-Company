from company import db

class Cover:
    def __init__(self):
        self.hospitalNames = []
        self.planTypes =[]

    def insert(self, hospitalName, planType):
        hospitalExist = db(
            f"SELECT hospital_name FROM hospital WHERE hospital_name='{hospitalName}'")
        if hospitalExist == []:
            return 'hospital not found'
        if planType not in ['Basic', 'Premium', 'Golden']:
            return 'Invalid plan type'
        db(f"INSERT INTO cover VALUES('{hospitalName}','{planType}')")
    def getInfo(self):
        data=db('SELECT * FROM cover')
        for tuple in data:
            self.hospitalNames.append(tuple[0])
            self.planTypes.append(tuple[1])
    def update(self, key, value, predicate):
        if key not in ['hospital_name', 'plan_type']:
            return 'Not a valid update ,please check your inputs'
        db(f"UPDATE cover SET {key}='{value}' WHERE {predicate} ")
        
    def getPlanType(self,hospitalName):
        return db(f"SELECT plan_type FROM cover WHERE hospital_name='{hospitalName}'")
    
    def refresh(self):
        self.getInfo()