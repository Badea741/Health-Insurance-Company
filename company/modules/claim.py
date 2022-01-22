from company import db
class Claim:
    def __init__(self):
        self.claimIds = []
        self.customerSsn = []
        self.planIds =[]
        self.beneficiaryIds = []
        self.hospitalNames =[]
        self.hospitalAddresss = []
        self.expensesAmounts = []
        self.expensesDetails = []

    def insert(self, customerSsn, beneficiarySsn, hospitalName, expenseAmount, expenseDetails,planId):
        if len(customerSsn) > 20:
            return 'Too long customer ssn'
        if len(beneficiarySsn) > 20:
            return 'Too long beneficiary ssn'
        if len(hospitalName) > 30:
            return 'Too long hospital name'
        if expenseAmount > 99999:
            return 'Too much expense amount'
        if len(expenseDetails) > 1024:
            return 'Too long details ,please type at most 1024 characters'
        
        db(f"INSERT INTO claim VALUES(0,'{customerSsn}','{planId}','{beneficiarySsn}','{hospitalName}','{expenseAmount}','{expenseDetails}','pending')")

    def delete(self, claimId):
        checkExist = db(
            f"SELECT claim_id FROM claim WHERE claim_id='{claimId}'")
        if checkExist == []:
            'The claim you are trying to send does already exist'
        db(f"DELETE FROM claim WHERE claim_id={claimId}")
        
    def update(self, key, value, predicate):
        db(f"UPDATE claim SET {key}='{value}' WHERE {predicate}")

    def refresh(self):
        self.__init__()

    # TODO: implement relational algebra functions
    def getAll(self,customerSsn):
        return db(f"SELECT * FROM claim WHERE customer_ssn='{customerSsn}'")
    def get(self,claimId):
        return db(f"SELECT * FROM claim WHERE claim_id={claimId}")[0]
    def getUnresolved(self,customerSsn):
        return db(f"SELECT * FROM claim WHERE customer_ssn='{customerSsn}' AND isResolved='pending'")
        
    def checkResolved(self,claimId):
        return db(f"SELECT * FROM claim WHERE claim_id={claimId} AND isResolved<>'pending'")
