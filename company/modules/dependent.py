from company import db

class Dependent:
    def __init__(self):
        self.ssn = []
        self.customerSsn = []
        self.names = []
        self.planIds = []
        self.addresses = []
        self.ages = []
        self.genders = []

    def insert(self, ssn, customer_ssn, name, address, age, gender):
        if len(ssn) > 20:
            return 'Too long ssn number'
        if len(name) > 30:
            return 'Too long name'
        if len(address) > 60:
            return 'Too long address'
        if age < 0 or age > 200:
            return 'Invalid age'
        if gender not in ['Male', 'Female', 'male', 'female']:
            return 'Invalid gender'
        checkExist = db(
            f"SELECT dependent_ssn FROM dependent WHERE dependent_ssn='{ssn}'")
        if checkExist != []:
            return 'The dependent you are trying to insert does already exist'
        db(f"INSERT INTO dependent VALUES('{ssn}','{customer_ssn}',null,'{name}','{address}',{age},'{gender}')")

    def delete(self, ssn):
        checkExist = db(
            f"SELECT dependent_ssn FROM dependent WHERE dependent_ssn='{ssn}'")
        if checkExist == []:
            return 'The dependent you are trying to delete doesn\'t exist'
        db(f"DELETE FROM dependent WHERE dependent_ssn='{ssn}'")

    def update(self, key, value, predicate):
        db(f"UPDATE dependent SET {key}='{value}' WHERE {predicate}")

    def checkExist(self, ssn):
        checkExist = db(
            f"SELECT dependent_ssn FROM dependent WHERE dependent_ssn='{ssn}'")
        return checkExist != []
        
    def getUsedPlan(self,ssn):
        planId=db(f"SELECT plan_id FROM dependent WHERE dependent_ssn='{ssn}'")
        if planId == [] or planId[0][0]==None:
            return None
        planType=db(f"SELECT type FROM plan WHERE plan_id='{planId[0][0]}'")
        return planType[0][0]
    def getInfo(self):
        data=db('SELECT * FROM dependent')
        for tuple in data:
            self.ssn.append(tuple[0])
            self.customerSsn.append(tuple[1])
            self.names.append(tuple[2])
            self.planIds.append(tuple[3])
            self.addresses.append(tuple[4])
            self.ages.append(tuple[5])
            self.genders.append(tuple[6])
            
            
    def get(self, ssn):
        if not self.checkExist(ssn):
            return 'Dependent you are trying to get not found'
        return db(f"SELECT name FROM dependent WHERE dependent_ssn={ssn}")[0][0]

    def refresh(self):
        self.getInfo()
