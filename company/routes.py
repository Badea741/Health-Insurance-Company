from flask.helpers import url_for
from company import app
from flask import render_template, redirect, request
from company.modules.hospital import Hospital
from company.modules.coverRelation import Cover
from company.modules.customer import Customer
from company.modules.claim import Claim
from company.modules.dependent import Dependent
from company.modules.plan import Plan

def getSsn():
    return str(request.args.get('ssn'))

@app.route("/")
@app.route("/home")
def homePage():
    return render_template('home.html')


@app.route('/admin')
def adminPage():
    return render_template('admin.html')

@app.route('/showcustomers')
def showCustomers():
    customer=Customer()
    customer.getInfo()
    return render_template('show_customer.html',ssn=customer.ssn,names=customer.names)
    
@app.route('/claimoptions')
def claimOptions():
    return render_template('claim_option.html')

@app.route('/allclaims',methods=['GET'])
def allClaims():
    claim = Claim()
    customerSsn=getSsn()
    claims= claim.getAll(customerSsn)
    return render_template('all_claim.html',claims=claims)    
    
@app.route('/unresolvedclaims',methods=['GET'])
def unResolvedClaims():
    claim = Claim()
    customerSsn=getSsn()
    claims= claim.getUnresolved(customerSsn)
    return render_template('unresolved_claims.html',claims=claims)

@app.route('/claimdetails',methods=['GET'])
def claimDetails():
    claim=Claim()
    customer=Customer()
    dependent=Dependent()
    hospital=Hospital()
    cover=Cover()
    claimId=request.args.get('claimId')
    claimDetails=claim.get(claimId)
    customerSsn=claimDetails[1]
    beneficiarySsn=claimDetails[3]
    hospitalAddress=hospital.get(claimDetails[4])
    availablePlans=cover.getPlanType(claimDetails[4])#plan types of claim hospital
    availableTypes=[]
    
    for plan in availablePlans:
        availableTypes.append(plan[0])
    if customerSsn==beneficiarySsn:
        currentPlan=customer.getUsedPlan(beneficiarySsn)
    else:
        currentPlan=dependent.getUsedPlan(beneficiarySsn)
    
    if currentPlan in availableTypes:
        isCover='Yes'
    else:
        isCover='No'
    if customerSsn==beneficiarySsn:
        name=customer.get(beneficiarySsn)
    else:
        name=dependent.get(beneficiarySsn)
    checkResolved=claim.checkResolved(claimId)!=[]
    return render_template('show_claim.html'
                           ,claimDetails=claimDetails
                           ,beneficiaryName=name
                           ,hospitalAddress=hospitalAddress
                           ,isCover=isCover
                           ,checkResolved=checkResolved)
    
@app.route('/updateresolved',methods=['GET'])
def updateResolved():
    claim=Claim()
    response=request.args.get('response')
    claimId=request.args.get('claimId')
    claim.update('isResolved',response,f"claim_id={claimId}")
    return redirect(url_for('showCustomers'))

@app.route('/customersignup')
def customerPage():
    return render_template('customer_sign_up.html')


@app.route('/addhospital')
def addHospital():
    return render_template('addhospital.html')


@app.route('/addnewhospital', methods=['GET', 'POST'])
def addHospital_db():
    hospital = Hospital()
    cover = Cover()
    hospitalName = request.form.get('namehospital')
    hospitalAddress = request.form.get('addresshospital')
    hospitalPlanTypes=request.form.getlist('mycheck')
    response = hospital.insert(name=hospitalName, address=hospitalAddress)
    if response == None:
        for plan in hospitalPlanTypes:
            cover.insert(hospitalName=hospitalName, planType=plan)
        return redirect(url_for('adminPage'))
    return redirect(url_for('addHospital',response=response))


@app.route('/addnewcustomer', methods=['GET', 'POST'])
def addCustomer_db():
    customer = Customer()
    ssn = request.form.get('ssncustomer')
    name = request.form.get('namecustomer')
    address = request.form.get('adresscustomer')
    age = request.form.get('agecustomer')
    gender = request.form.get('gendercustomer')
    response = customer.insert(
        ssn=ssn, name=name, address=address, age=int(age), gender=gender)
    if response != None:
        return redirect(url_for('customerPage',response=response))
    return redirect(url_for('purchasePlan',customerName=name,ssn=ssn))
    
@app.route("/customersignin")
def customerSignIn():
    return render_template('customer_sign_in.html')
    
@app.route("/checkcustomer",methods=['GET','POST'])
def customerSignIn_db():    
    customer=Customer()
    ssn=request.form.get('ssncustomer')
    response = customer.checkExist(ssn)
    customerName=customer.get(ssn)
    if response:
        return redirect(url_for('customerHome',customerName=customerName,ssn=ssn))
    response='Customer not found'
    return redirect(url_for('customerSignIn',response=response))
    
@app.route('/customerhome')
def customerHome():
    return render_template('customer_home.html')
    
@app.route('/addbeneficiary')
def addBeneficiary():
    customer=Customer()
    plan=Plan()
    dependent=Dependent()
    customerSsn=getSsn()
    customerName=customer.get(customerSsn)
    availablePlans=customer.getPlans(customerSsn)
    dependentsList=customer.getDependents(customerSsn)
    customerBeneficiaryPlanId=customer.getBeneficiaryPlan(customerSsn)
    customerBeneficiaryPlan=plan.getType(customerBeneficiaryPlanId)
    formattedAvailablePlans=[]
    formattedDependentsNames=[]
    formattedDependentSsn=[]
    formattedDependentPlans=[]
    for plan in availablePlans:
        formattedAvailablePlans.append(plan[0])
    for dependent0 in dependentsList:
        formattedDependentSsn.append(dependent0[0])
        formattedDependentsNames.append(dependent0[1])
    for dependentSsn in formattedDependentSsn:
        dependentPlan=dependent.getUsedPlan(dependentSsn)
        formattedDependentPlans.append(dependentPlan)
    return render_template('assign_plan.html'
                           ,ssn=customerSsn
                           ,plans=formattedAvailablePlans
                           ,dependentSsn=formattedDependentSsn
                           ,dependentNames=formattedDependentsNames
                           ,customerName=customerName
                           ,customerPlan=customerBeneficiaryPlan
                           ,dependentPlans=formattedDependentPlans)

@app.route('/adddependent')
def addDependent():
    ssn=getSsn()
    return render_template('add_dependent.html',ssn=ssn)
    
@app.route('/purchaseplan')
def purchasePlan():
    ssn=getSsn()
    return render_template('purchase_plan.html',ssn=ssn)
    
@app.route('/availablehospitals')
def availableHospitals():
    customer=Customer()
    hospital=Hospital()
    plan=Plan()
    ssn=getSsn()
    beneficiaryPlan=customer.getBeneficiaryPlan(ssn)
    planType=plan.getType(beneficiaryPlan)
    hospitalNames=customer.showHospitals(ssn=ssn,planType=planType)
    
    formattedHospitalAddresses=[]
    formatedHospitalNames=[]
    for name in hospitalNames:
        formattedHospitalAddresses.append(hospital.get(name[0]))
        formatedHospitalNames.append(name[0])
    return render_template('available_hospitals.html'
                           ,hospitalNames=formatedHospitalNames
                           ,hospitalAddresses=formattedHospitalAddresses)

@app.route('/fileclaim',methods=['GET'])
def fileClaim():
    customer=Customer()
    customerSsn=getSsn()
    dependentList=customer.getDependents(customerSsn)
    formattedDependentSsn=[]
    formattedDependentNames=[]
    for dependent in dependentList:
        formattedDependentSsn.append(dependent[0])
        formattedDependentNames.append(dependent[1])
    return render_template('file_claim.html'
                           ,ssn=customerSsn
                           ,dependentSsn=formattedDependentSsn
                           ,dependentNames=formattedDependentNames)

@app.route('/addnewdependentdb',methods=['GET','POST'])
def addDependent_db():
    customer=Customer()
    customerSsn=request.form.get('ssncustomer')
    customerName=customer.get(customerSsn)
    dependentSsn=request.form.get('ssndependant')
    dependentName=request.form.get('namedependant')
    dependentAddress=request.form.get('addressdependant')
    dependentAge=int(request.form.get('agedependant'))
    dependentGender=request.form.get('genderdependant')
    response=customer.addDependent(ssn=dependentSsn,customerSsn=customerSsn,name=dependentName,
    address=dependentAddress,age=dependentAge,gender=dependentGender)
    if response != None:
        return redirect(url_for('addDependent',response=response,ssn=customerSsn))
    return redirect(url_for('customerHome',customerName=customerName,ssn=customerSsn))

@app.route('/buynewplan',methods=['GET','POST'])
def buyPlan_db():
    customer=Customer()
    customerSsn=getSsn()
    customerName=customer.get(customerSsn)
    choosenPlan=request.form.get('plan')
    response=customer.buyPlan(ssn=customerSsn,planType=choosenPlan)
    customer.updateBeneficiary(customerSsn=customerSsn,beneficiarySsn=customerSsn,planType=choosenPlan)
    if response != None:
        return redirect(url_for('purchasePlan',response=response,ssn=customerSsn))
    return redirect(url_for('customerHome',ssn=customerSsn,customerName=customerName))

@app.route('/filenewclaim',methods=['GET','POST'])
def fileClaim_db():
    customer=Customer()
    customerSsn=request.form.get('ssncustomer')
    customerName=customer.get(customerSsn)
    beneficiarySsn=request.form.get('ssnbeneficiary')
    hospitalName=request.form.get('namehospital')
    expenseAmount=int(request.form.get('amountexpense'))
    expenseDetails=request.form.get('detailsexpense')
    response=customer.fileInsuranceClaim(customerSsn=customerSsn
                                ,beneficiarySsn=beneficiarySsn
                                ,hospitalName=hospitalName
                                ,expenseAmount=expenseAmount
                                ,expenseDetails=expenseDetails)
    if response != None:
        return redirect(url_for('fileClaim',response=response,ssn=customerSsn))
    return redirect(url_for('customerHome',ssn=customerSsn,customerName=customerName))


@app.route('/updatebeneficiary',methods=['GET','POST'])
def addBeneficiary_db():
    customer=Customer()
    customerSsn=getSsn()
    customerName=customer.get(customerSsn)
    dependentSsn=request.args.getlist('dependentssn')
    customerPlanType=request.form.get('plantypecustomer')
    customer.updateBeneficiary(customerSsn=customerSsn
                               ,beneficiarySsn=customerSsn
                               ,planType=customerPlanType)
    dependentplantypes=[]
    for i in range(len(dependentSsn)):
        dependentplantypes.append(request.form.get(f"plantypedependent{i}"))
    for i in range(len(dependentSsn)):
        customer.updateBeneficiary(customerSsn=customerSsn
                                   ,beneficiarySsn=dependentSsn[i]
                                   ,planType=dependentplantypes[i])
    return redirect(url_for('customerHome',ssn=customerSsn,customerName=customerName))