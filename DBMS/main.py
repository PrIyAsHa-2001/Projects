import mysql.connector
database=mysql.connector.connect(host='localhost',user='root',password ='Priyasha@123',database='Bank_management')

def OpenAcc():
    name=input("Enter your name : ")
    accountno=input("Enter the Account number : ")
    dob=input("Enter Yur date of birth :")
    add=input("Enter your Address : ")
    cn=input("Enter your contact number: ")
    ob=input("Enter your Opening balance : ")

    data1=(name,accountno,dob,add,cn,ob)
    data2=(name,accountno,ob)

    sql1=('insert into ACCOUNT values (%s,%s,%s,%s,%s,%s)')
    sql2=('insert into AMOUNT value (%s,%s,%s)')
    x=database.cursor(buffered = True)
    x.execute(sql1,data1)
    x.execute(sql2,data2)
    database.commit()

    print("Data entry succesful")
    main()

def DepoAcc():
    ac=input("Enter the account number : ")
    amount=int(input("Enter the amount you want to deposit : "))
    
    a='select Balance from AMOUNT where Accno=%s'
    data=(ac,)
    x=database.cursor(buffered = True)
    x.execute(a,data)
    result=x.fetchone()
    t=result[-1]+amount
    sql='update AMOUNT set Balance=%s where Accno=%s'
    d=(t,ac)
    
    x.execute(sql,d)
    
    database.commit()
    main()

def Withdraw():
    amount=int(input("How much money you want to withdraw : "))
    ac=input("Enter the account number : ")
    a='select balance from AMOUNT where Accno=%s'
    data=(ac,)
    x=database.cursor(buffered = True)
    x.execute(a,data)
    result=x.fetchone()
    t=result[-1]-amount
    sql='update AMOUNT set Balance=%s where Accno=%s'
    d=(t,ac)
    x.execute(sql,d)
    result=x.fetchone()
    database.commit()
    main()

def Balenq():
    ac=input("Enter the Account number : ")
    a='select Balance from AMOUNT where Accno=%s'
    data=(ac,)
    x=database.cursor(buffered = True)
    x.execute(a,data)
    result=x.fetchone()
    print("Balance in your account: ",ac,"is",result[-1])
    main()

def Custdetails():
    ac=input("Enter the Account number : ")
    a='select * from ACCOUNT where Accno=%s'
    data=(ac,)
    x=database.cursor(buffered = True)
    x.execute(a,data)
    result=x.fetchone()
    for i in result :
        print(i)
    main()

def CloseAcc():
    ac=input("Enter the Account number : ")
    sql1='delete from ACCOUNT where Accno=%s'
    sql2='delete from AMOUNT where Accno=%s'
    data=(ac,)
    x=database.cursor(buffered = True)
    x.execute(sql1,data)
    x.execute(sql2,data)
    database.commit()
    print("Account closed succesfully")
    main()


def main():
    print(
    '''
        1.OPEN NEW ACCOUNT 
        2.DEPOSIT AMOUNT
        3.WITHDRAW AMOUNT
        4.BALANCE ENQUIRY 
        5.DISPLAY CUSTOMER DETAILS
        6.CLOSE AN ACCOUNT
    '''
    )

    option =input("Enter the task you want to perform: ")
    if(option=='1'):
        OpenAcc()
    elif(option=='2'):
        DepoAcc()
    elif(option=='3'):
        Withdraw()
    elif(option=='4'):
        Balenq()
    elif(option=='5'):
        Custdetails()
    elif(option=='6'):
        CloseAcc()

    else:
        print("Invalid option ")
        main()
main()