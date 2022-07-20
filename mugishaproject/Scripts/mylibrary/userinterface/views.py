
class userinterface:
    first_name=input('firstname')
    last_name=input('lastname')
    def display(self):
        print('Hello %s,%s,you are welcome'%(self.firstname,self.lastname))

class bookrequest(userinterface):
    def __init__(self,request):
        self.request=request

    bookavailable=0
    while bookavailable>0:
        if bookavailable==1:
            print('The book is available')
            
        else:
            print('The book is not available. We are sorry')


        






    





