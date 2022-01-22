from company import db


class Hospital:
    def __init__(self):
        self.names = []
        self.addresses = []

    def insert(self, name, address):
        if len(name) > 30:
            return 'Too long hospital name'
        if len(address) > 60:
            return 'Too long hospital address'
        checkExist = db(
            f"SELECT hospital_name FROM hospital WHERE hospital_name='{name}'")
        if checkExist != []:
            return 'The hospital you are trying to insert does already exist'

        db(f"INSERT INTO hospital VALUES('{name}','{address}')")

    def delete(self, name):
        checkExist = db(
            f"SELECT hospital_name FROM hospital WHERE hospital_name='{name}'")
        if checkExist == []:
            return 'The hospital you are trying to delete doesn\'t exist'

        db(f"DELETE FROM hospital WHERE hospital_name='{name}'")

    def update(self, key, value, predicate):
        db(f"UPDATE hospital SET {key}='{value}' WHERE {predicate}")
        
    def getByPlanType(self,planType):
        if planType not in ['Golden','Premium','Basic']:
            return 'Invalid plan type'
        return db(f"SELECT hospital_name FROM cover WHERE plan_type='{planType}'")

    def refresh(self):
        self.getInfo()
        
    def checkExist(self,hospitalName):
        hospital=db(f"SELECT hospital_name FROM hospital WHERE hospital_name='{hospitalName}'")
        return hospital != []
    def getInfo(self):
        data=db('SELECT * FROM hospital')
        for tuple in data:
            self.names.append(tuple[0])
            self.addresses.append(tuple[1])
            
    def get(self, hospitalName):
        if not self.checkExist(hospitalName):
            return 'hospital not found'
        return db(f"SELECT address FROM hospital WHERE hospital_name='{hospitalName}'")[0][0]

# hospital.insert(name='Tanta central',address='tanta',planType='Basic')
# hospital.delete('Tanta central')
# hospital.refresh()
# hospital.names