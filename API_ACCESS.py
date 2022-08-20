from os import access
import jwt
import requests
from requests.structures import CaseInsensitiveDict
from tkinter import *
from tkinter import ttk
import ast


import datetime
import time
import tkinter.messagebox
import sqlite3




#####test connection#####
response = requests.get("https://flightlog-backend.herokuapp.com/")
print(response.status_code) 



class xyz(object):


    def __init__(self,root):

        self.root = root
        self.root.title('LOGIN SCREEN')

        Label(text = ' Username ',font='Times 15').grid(row=1,column=1,pady=20)
        self.username = Entry()
        self.username.grid(row=1,column=2,columnspan=10)

        Label(text = ' Password ',font='Times 15').grid(row=2,column=1,pady=10)
        self.password = Entry(show='*')
        self.password.grid(row=2,column=2,columnspan=10)

        
        button=ttk.Button(text='LOGIN',command=self.login_user).grid(row=3,column=2)
        


    def login_user(self):

        userdata = {
            'username' : str(self.username.get()),
            'password' : str(self.password.get()),
        }


        response = requests.post("https://flightlog-backend.herokuapp.com/user/authenticate",json=userdata)
        print(response.status_code)
        
        if response.status_code == 200:
            jsontoken=response.json()
            xyz.accesstoken=jsontoken['accessToken']
            print(xyz.accesstoken)
            root.destroy()
            
        else:
            
            self.message = Label(text = 'Username or Password incorrect. Try again!',fg = 'Red')
            self.message.grid(row=6,column=2)







if __name__ == '__main__':

    root = Tk()
    root.geometry('425x225')
    application = xyz(root)

    root.mainloop()







class flight_Portal(xyz):
    # response = requests.post("https://flightlog-backend.herokuapp.com/user/authenticate",json=userdata)
    # jsontoken=response.json()
    # accesstoken=jsontoken['accessToken']
    # header={'Authorization': 'Bearer ' + accesstoken}
    #print(response.json()) 
    
    # def retrieve(self):
    #     xyz.login_user.funxyz()


    def __init__(self, root):
        print(xyz.accesstoken)
        header={'Authorization': 'Bearer ' + xyz.accesstoken}
        print(header)

        self.root = root
        self.root.geometry('1200x525+600+200')
        self.root.title('Flight Data')

        '''Logo and Title'''

        self.photo = PhotoImage(file='staerologo.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0, column=0)

        self.label1 = Label(font=('arial', 15, 'bold'), text='Flight Portal System', fg='dark red')
        self.label1.grid(row=8, column=0)

        ''' New Records '''
        frame = LabelFrame(self.root, text='Add New Record:')
        frame.grid(row=0, column=1)

        Label(frame, text='Tail Number:').grid(row=1, column=1, sticky=W)
        self.tailnumber = Entry(frame)
        self.tailnumber.grid(row=1, column=2)

        Label(frame, text='Flight ID:').grid(row=2, column=1, sticky=W)
        self.flightid = Entry(frame)
        self.flightid.grid(row=2, column=2)

        Label(frame, text='Takeoff Time:').grid(row=3, column=1, sticky=W)
        self.takeofftime = Entry(frame)
        self.takeofftime.grid(row=3, column=2)

        Label(frame, text='Landing Time:').grid(row=4, column=1, sticky=W)
        self.landingtime = Entry(frame)
        self.landingtime.grid(row=4, column=2)

        Label(frame, text='Flight Duration:').grid(row=5, column=1, sticky=W)
        self.flightduration = Entry(frame)
        self.flightduration.grid(row=5, column=2)

        
        '''Add Button'''
        ttk.Button(frame, text='Add Record', command=self.add).grid(row=6, column=2)

        '''Message Display'''
        self.message = Label(text='', fg='Red')
        self.message.grid(row=11, column=0)

        '''Database Table display box '''
        self.tree = ttk.Treeview(height=8,columns=(0,1,2,3,4,5), show='headings')
        self.tree.grid(row=9, column=0, columnspan=2)

        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        vsb.place(x=1180, y=260, height=183)

        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.heading(0, text='ID')
        self.tree.heading(1, text='Tail Number')
        self.tree.heading(2, text='Flight ID')
        self.tree.heading(3, text='Takeoff Time')
        self.tree.heading(4, text='Landing Time')
        self.tree.heading(5, text='Flight Duration')


        '''Time and Date'''
        def tick():
            d = datetime.datetime.now()
            today = '{:%B %d,%Y}'.format(d)

            mytime = time.strftime('%I:%M:%S%p')
            self.lblInfo.config(text=(mytime + '\t' + today))
            self.lblInfo.after(200, tick)

        self.lblInfo = Label(font=('arial', 20, 'bold'), fg='Black')
        self.lblInfo.grid(row=10, column=0, columnspan=2)
        tick()

        ''' Menu Bar '''
        Chooser = Menu()
        itemone = Menu()

        itemone.add_command(label='Add Record', command=self.add)
        itemone.add_command(label='Edit Record', command=self.edit)
        itemone.add_command(label='Delete Record', command=self.delet)
        itemone.add_separator()
        itemone.add_command(label='Help', command=self.help)
        itemone.add_command(label='Exit', command=self.ex)

        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_command(label='Add', command=self.add)
        Chooser.add_command(label='Edit', command=self.edit)
        Chooser.add_command(label='Delete', command=self.delet)
        Chooser.add_command(label='Help', command=self.help)
        Chooser.add_command(label='Exit', command=self.ex)

        root.config(menu=Chooser)
        self.viewing_records()

    ''' View Database Table'''

    def run_query(self):
        flight_Portal.header={'Authorization': 'Bearer ' + xyz.accesstoken}
        response = requests.get("https://flightlog-backend.herokuapp.com/flightLog",headers=flight_Portal.header)
        flight_Portal.jsonlist=response.json()
        print(flight_Portal.jsonlist) 

    def viewing_records(self):
        self.run_query()
        for i in flight_Portal.jsonlist:
            data=[]
            data.append(i['_id'])
            data.append(i['tailNumber'])
            data.append(i['flightID'])
            data.append(i['takeoff'])
            data.append(i['landing'])
            data.append(i['duration'])
            datatuple=tuple(data)
            self.tree.insert("", 'end', iid=i, values=datatuple)
        #self.tree.insert()

    ''' Add New Record '''

    def validation(self):
        return len(self.tailnumber.get()) != 0 and len(self.flightid.get()) != 0 and len(self.takeofftime.get()) != 0 and \
               len(self.landingtime.get()) != 0 and len(self.flightduration.get()) != 0

    def add_record(self):
        if self.validation():
            ad = tkinter.messagebox.askquestion('Add Record', 'Do you want to add a New Record?')
            if ad == 'yes':
                flightdata = {
                    'tailNumber' : str(self.tailnumber.get()),
                    'flightID' : str(self.flightid.get()),
                    'takeoff' : str(self.takeofftime.get()),
                    'landing' : str(self.landingtime.get()),
                    'duration' : str(self.flightduration.get()),
                }
                response = requests.post("https://flightlog-backend.herokuapp.com/flightLog",headers=flight_Portal.header, json=flightdata)
                print(response.status_code) 
                self.tree.delete(*self.tree.get_children())

                #self.viewing_records()

                '''Empty the fields'''
                self.tailnumber.delete(0, END)
                self.flightid.delete(0, END)
                self.takeofftime.delete(0, END)
                self.landingtime.delete(0, END)
                self.flightduration.delete(0, END)



        else:
            tkinter.messagebox.showwarning(title='Important', message='Fields not completed! Complete all fields...')

        self.viewing_records()

    '''Function for using buttons'''

    def add(self):
        self.add_record()

    ''' Deleting a Record '''

    def delete_record(self):
        
        print(flight_Portal.selected)
        selecteddict=ast.literal_eval(flight_Portal.selected)
        flight_Portal.selectedid=selecteddict['_id']
        print(flight_Portal.selectedid)
        url="https://flightlog-backend.herokuapp.com/flightLog/"+flight_Portal.selectedid
        response = requests.delete(url,headers=flight_Portal.header)
        print(response.status_code) 
        if response.status_code==204:
            tkinter.messagebox.showinfo(title="Deletion Successful", message="Deleted")
        else:
            tkinter.messagebox.showerror(title="Error", message="Deletion Unsuccessful!")
        self.tree.delete(*self.tree.get_children())

        
        
        self.viewing_records()

    # Function to add functionality in buttons

    def delet(self):
        flight_Portal.selected=self.tree.focus()

        if flight_Portal.selected=="":
            tkinter.messagebox.showerror(title="Error", message="Please select a log!")
            print("NOTHING")

        else:
            de = tkinter.messagebox.askquestion('Delete Record', 'Are you sure you want to delete this Record?')
            if de == 'yes':
                self.delete_record()

    '''EDIT RECORD'''

    '''CREATING A POP UP WINDOW FOR EDIT'''

    def edit_box(self):
        print(flight_Portal.selected)
        selecteddict=ast.literal_eval(flight_Portal.selected)
        flight_Portal.selectedid=selecteddict['_id']
        flight_Portal.selectedtailnNmber=selecteddict['tailNumber']
        flight_Portal.selectedflightID=selecteddict['flightID']
        flight_Portal.selectedtakeoff=selecteddict['takeoff']
        flight_Portal.selectedlanding=selecteddict['landing']
        flight_Portal.selectedduration=selecteddict['duration']

        self.edit_root = Toplevel()
        self.edit_root.title('Edit Record')
        self.edit_root.geometry('305x355+800+200')
 
        Label(self.edit_root, text='New Tail Number').grid(row=1, column=1, sticky=W)
        flight_Portal.new_selectedtailnNmber = Entry(self.edit_root , textvariable=StringVar(self.edit_root, value=flight_Portal.selectedtailnNmber),width=25)
        flight_Portal.new_selectedtailnNmber.grid(row=1, column=2,padx=20, pady=20)

        Label(self.edit_root, text='New Flight ID').grid(row=3, column=1, sticky=W)
        flight_Portal.new_selectedflightID = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=flight_Portal.selectedflightID),width=25)
        flight_Portal.new_selectedflightID.grid(row=3, column=2,padx=20, pady=20)

        Label(self.edit_root, text='New Takeoff Time').grid(row=5, column=1, sticky=W)
        flight_Portal.new_selectedtakeoff = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=flight_Portal.selectedtakeoff),width=25)
        flight_Portal.new_selectedtakeoff.grid(row=5, column=2,padx=20, pady=20)

        Label(self.edit_root, text='New Landing Time').grid(row=7, column=1, sticky=W)
        flight_Portal.new_selectedlanding = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=flight_Portal.selectedlanding),width=25)
        flight_Portal.new_selectedlanding.grid(row=7, column=2,padx=20, pady=20)
        
        Label(self.edit_root, text='New Flight Duration').grid(row=9, column=1, sticky=W)
        flight_Portal.new_selectedduration = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=flight_Portal.selectedduration),width=25)
        flight_Portal.new_selectedduration.grid(row=9, column=2,padx=20, pady=20)

        Button(self.edit_root, text='Save Changes', command=self.edit_record).grid(row=12, column=2, sticky=W)

        self.edit_root.mainloop()

    def editvalidation(self):
        return len(flight_Portal.new_selectedtailnNmber.get()) != 0 and len(flight_Portal.new_selectedflightID.get()) != 0 and len(flight_Portal.new_selectedtakeoff.get()) != 0 and \
               len(flight_Portal.new_selectedlanding.get()) != 0 and len(flight_Portal.new_selectedduration.get()) != 0
    
    def edit_record(self):
        # query = 'UPDATE flightlist SET Firstname=?, Lastname=?, Username=?, Email=?, Subject=?, Age=? WHERE ' \
        #         'Firstname=? AND Lastname=? AND Username=? AND Email=? AND Subject=? AND Age=?'

        #parameters = (flight_Portal.selectedid,flight_Portal.new_selectedtailnNmber.get(), flight_Portal.new_selectedflightID.get(), flight_Portal.new_selectedtakeoff.get(), flight_Portal.new_selectedlanding.get(), flight_Portal.new_selectedduration.get())
        
        if self.editvalidation():
            de = tkinter.messagebox.askquestion('Amend Record', 'Are you sure you want to amend this Record?')
            if de == 'yes':
                flightdata = {
                    'tailNumber' : str(flight_Portal.new_selectedtailnNmber.get()),
                    'flightID' : str(flight_Portal.new_selectedflightID.get()),
                    'takeoff' : str(flight_Portal.new_selectedtakeoff.get()),
                    'landing' : str(flight_Portal.new_selectedlanding.get()),
                    'duration' : str(flight_Portal.new_selectedduration.get()),
                }
                dataid=flight_Portal.selectedid
                url="https://flightlog-backend.herokuapp.com/flightLog/"+dataid
                response = requests.put(url,headers=flight_Portal.header, json=flightdata)
                print(response.status_code) 
                if response.status_code==204:
                    tkinter.messagebox.showinfo(title="Edit Success", message="Edit Success")
                    self.edit_root.destroy()
                else:
                    tkinter.messagebox.showerror(title="Error", message="Unable to update data!")
                self.tree.delete(*self.tree.get_children())
                self.viewing_records()
        else:
            tkinter.messagebox.showerror(title="Error", message="Fields not completed! Complete all fields...")
        

    def edit(self):
        flight_Portal.selected=self.tree.focus()

        if flight_Portal.selected=="":
            tkinter.messagebox.showerror(title="Error", message="Please select a log!")
            print("NOTHING")

        else:
            self.edit_box()

    '''HELP'''
    def help(self):
        tkinter.messagebox.showinfo('Log','Report Sent!')

    '''EXIT'''
    def ex(self):
        exit = tkinter.messagebox.askquestion('Exit Application','Are you sure you want to close this application?')
        if exit == 'yes':
            self.root.destroy()


'''MAIN'''

if __name__ == '__main__':
    root = Tk()
    # root.geometry('585x515+500+200')
    application = flight_Portal(root)
    root.mainloop()