from company import db
from company.modules.dependent import Dependent
from company.modules.hospital import Hospital
from company.modules.plan import Plan
from company.modules.claim import Claim


class Customer:
    def __init__(self):
        self.ssn = []
        self.names = []
        self.planIds = []
        self.addresses = []
        self.ages = []
        self.genders = []

    def insert(self, ssn, name, address, age, gender):
        if len(ssn) > 20:
            return 'Too long ssn number'
        if len(name) > 30:
            return 'Too long name'
        if len(address) > 60:
            return 'Too long address'
        if age < 18 or age > 200:
            return 'Invalid age'
        if gender not in ['Male', 'Female']:
            return 'Invalid gender'
        checkExist = db(
            f"SELECT customer_ssn FROM customer WHERE customer_ssn='{ssn}'")
        if checkExist != []:
            return 'The customer you are trying to insert does already exist'

        db(f"INSERT INTO customer VALUES('{ssn}','{name}',null,'{address}',{age},'{gender}')")

    def delete(self, ssn):
        if not self.checkExist(ssn):
            return 'The customer you are trying to delete doesn\'t exist'
        db(f"DELETE FROM customer WHERE customer_ssn='{ssn}'")

    def update(self, key, value, predicate):
        db(f"UPDATE customer SET {key}='{value}' WHERE {predicate}")

    def buyPlan(self, ssn, planType):
        if not self.checkExist(ssn):
            return 'Customer not found'
        if self.checkPlan(ssn,planType):
            return 'You have already bought this plan'
        plan = Plan()
        return plan.insert(ssn, planType)
    def getInfo(self):
        data=db('SELECT * FROM customer')
        for tuple in data:
            self.ssn.append(tuple[0])
            self.names.append(tuple[1])
            self.planIds.append(tuple[2])
            self.addresses.append(tuple[3])
            self.ages.append(tuple[4])
            self.genders.append(tuple[5])

    def checkExist(self, ssn):
        checkExist = db(
            f"SELECT customer_ssn FROM customer WHERE customer_ssn='{ssn}'")
        return checkExist != []

    def get(self, ssn):
        if not self.checkExist(ssn):
            return 'Customer you are trying to get not found'
        return db(f"SELECT name FROM customer WHERE customer_ssn='{ssn}'")[0][0]
        
    def getPlans(self,ssn):
        if not self.checkExist(ssn):
            return 'Customer not found'
        return db(f"SELECT type FROM plan WHERE customer_ssn='{ssn}'")
        
    def getUsedPlan(self,ssn):
        planId=db(f"SELECT plan_id FROM customer WHERE customer_ssn='{ssn}'")
        if planId == [] or planId[0][0] ==None :
            return 'Please add yourself as benficiary first'
        planType=db(f"SELECT type FROM plan p WHERE p.plan_id={planId[0][0]}")
        return planType[0][0]
        
    def checkPlan(self,ssn,planType):
        plan= db(f"SELECT type FROM plan WHERE customer_ssn='{ssn}' AND type='{planType}'")
        return plan != [] and plan[0][0]!=None
        
    def showHospitals(self,ssn,planType):
        if not self.checkPlan(ssn,planType):
            return 'Please choose a plan you own'
        hospital=Hospital()
        return hospital.getByPlanType(planType)
        
    def showAvailablePlans(self,ssn):
        plans=self.getPlans(ssn)
        availablePlans=['Basic', 'Premium', 'Golden']
        temp=[]
        for plan in plans:
            temp.append(plan[0])
        for i in plans:
            for j in availablePlans:
                if i==j:
                    availablePlans.remove(i)
        return availablePlans   
    def getDependents(self, ssn):
        if not self.checkExist(ssn):
            return 'Customer not found'
        return db(f"SELECT d.dependent_ssn,d.name FROM dependent d\
                    JOIN customer c \
                    ON d.customer_ssn = c.customer_ssn \
                    WHERE c.customer_ssn='{ssn}'")
                    
    def getBeneficiaryPlan(self,ssn):
        if not self.checkExist(ssn):
            return 'Customer not found'
        usedPlan=db(f"SELECT plan_id FROM customer WHERE customer_ssn ='{ssn}'")
        if usedPlan==[] or usedPlan[0][0]==None:
            return None
        return usedPlan[0][0]
    def addDependent(self, ssn, customerSsn, name, address, age, gender):
        if not self.checkExist(customerSsn):
            return 'Customer not found'
        dependent = Dependent()
        return dependent.insert(ssn, customerSsn, name, address, age, gender)
    
    def updateBeneficiary(self,customerSsn,beneficiarySsn,planType):
        if not self.checkExist(customerSsn):
            return 'Customer not found'
        planId=db(f"SELECT plan_id FROM plan WHERE customer_ssn='{customerSsn}' AND type='{planType}'")
        if customerSsn==beneficiarySsn:
            return self.update('plan_id',planId[0][0],f"customer_ssn='{beneficiarySsn}'")
        dependent=Dependent()
        return dependent.update('plan_id',planId[0][0],f"dependent_ssn='{beneficiarySsn}'")
    
    def fileInsuranceClaim(self,customerSsn,beneficiarySsn,hospitalName,expenseAmount,expenseDetails):
        if not self.checkExist(customerSsn):
            return 'customer not found'
        hospital=Hospital()
        if not hospital.checkExist(hospitalName):
            return 'Hospital not found'
        if customerSsn==beneficiarySsn:
            planId=db(f"SELECT plan_id FROM customer WHERE customer_ssn='{beneficiarySsn}'")
        else:
            #check if beneficiary has no plan_id in his table
            planId=db(f"SELECT plan_id FROM dependent WHERE dependent_ssn='{beneficiarySsn}'")
        claim=Claim()
        return claim.insert(customerSsn,beneficiarySsn,hospitalName,expenseAmount
                            ,expenseDetails,planId[0][0])
    def refresh(self):
        self.__init__()


# customer = Customer()
# customer.fileInsuranceClaim('9','8','good hospital',2511,'leg cut')



# customer.getUsedPlan('4')
# customer.insert(ssn='1', name='Hossam', plantype='Golden',
#                 address='asdkl;fj', age=23, gender='Male')
# customer.refresh()
# customer.names[0][0]
# customer.addDependent(name='Muhammad', ssn='10', customerSsn='1',
#                       planType='Golden', address='as;dkljf', age=22, gender='Male')
# customer.getDependents('1')
# plan=Plan()
# plan.refresh()
# plan.ids
