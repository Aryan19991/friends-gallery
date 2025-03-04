
from tkinter import * #imports symbols from the Tkinter module
from tkinter import ttk  
from PIL import Image, ImageTk 
from tkinter import messagebox, filedialog 
import os 
import shutil 
import time 

# Global variables section - add variables that are required
path = 'images/' 
stateList=[] 



def resizeImage (image_path,width,height): 
    img=Image.open(image_path) 
    img=img.resize((width,height)) 
    return ImageTk.PhotoImage(img) 

def showFriends():
    btnShowFriends['state']="disabled" 
    btnClearAll['state']="enabled" #
    if os.path.exists(path): 
        count=0
        global Frame_Image  
        Frame_Image=LabelFrame(myApp, text="My friends- Tap a friend's profile to view their connections", bg="brown",
                               width=1100) #This line creates a new LabelFrame widget to display the images of friends.

        Frame_Image.grid(row=1,column=0,columnspan=len(os.listdir(path)),padx=5,pady=5,sticky=W) 
        for file in os.listdir(path): 
            (head,tail)=os.path.splitext(file) 
            if tail.lower() not in [".png",".jpg",".jpeg"]: # checks if the lower case extension of the file is not in the list
                                                            
                continue 
            else:
                resized_image=resizeImage(path+file,120,120) # it calls the resizeimage() function to resize the image file found at path+file to 120x120 pixels
                Button_friendImage=Button(Frame_Image,text=f"{head.title()}sfriends", 
                                          command=lambda head=head, count=count : friendButton_clicked(head,count)) 
                Button_friendImage.grid(row=1,column=count,padx=5)
                Label_Image=Label(Frame_Image,image=resized_image)#
                Label_Image.grid(row=0,column=count) 
                stateList.append(False) 
                Button_friendImage.image=resized_image #
                count+=1 #keeep track of column index for placing subsequent widgets.
    else:
        print("Path does not exists")

def del_Friend(head):
    fileType=[("Image files","*.png;*.jpg;*.jpeg"), ("All files","*.*")] #defines the type of the file that user can select
    selectedFile=filedialog.askopenfilename(initialdir=path+head,title="select a file",filetype=fileType)
    if selectedFile:
        check=messagebox.askquestion("Delete File","Are you absolutely certain you want to remove this file??")#Ask the 
        if check=="yes":
            fileName=os.path.basename(selectedFile)#get the name of the file from its path
            os.remove(selectedFile)#deletes the file
            messagebox.showinfo("delete friend's friend,"f"{fileName} deleted") 
            Frame_Image.grid_remove() 
            showFriends()
        else:
            messagebox.showinfo("delete.friend's friend","The intended deletion failed")  

def friendButton_clicked(head,count): 
    friends_folder=path+head 
    row_count=2 
    if os.path.exists(friends_folder):
        if not os.listdir(friends_folder): 
            messagebox.showinfo("Information",f"{head.title()}'s friend folder exist, but it doesn't contain any images.")
            
            for file in os.listdir(friends_folder): 
                (head_2,tail_2)=os.path.splitext(file) #splits the file name into head and tail
                if tail_2.lower() not in [".png",".jpg",".jpeg"]:
                    continue
                else:
                    resized_image=resizeImage(f"{friends_folder}/{file}",90,90) #resizes the image file to dimensions 90x30using resizeImage() function
                    Label_friend=Label(Frame_Image,text=f"{head_2}",compound="top",image=resized_image)
                    Label_friend.grid(row=row_count,column=count) 
                    Label_friend.image=resized_image # resized image is displayed
                    row_count+=1
            if stateList[count]==True:
                messagebox.showinfo("Information", f"Friends are already being displayed")
            else:
                stateList[count]=True #
            delFriendsFriend=Button(Frame_Image,text=f"Delete\n {head.title()}'s\nfriend",bg="red",command= lambda head=head :del_Friend(head))   
            delFriendsFriend.grid(row=row_count,column=count,pady=5) 
    else:
        messagebox.showinfo("Information",f"Friend's folder doesnot exist for {head}")     

def clearAll(): #this function controls the action of clearing all the displayed content in the GUI
    check=messagebox.askquestion("yes no","Could you please confirm?") 
    if check=="yes": 
        Frame_Image.grid_remove() 
        btnShowFriends['state']="enabled" 
        btnClearAll['state']="disabled" 
        stateList.clear() 
def delFriend(): # this function controls the deletion process of a friend
    fileType=(("Image files","*.png;*.jpg;*.jpeg"),("All files","*.*"))
    removeFriend=filedialog.askopenfilename(initialdir=path,title="Which friend's photo do you want to delete?",
                                            filetype=fileType)
    if removeFriend: 
        check=messagebox.askyesno("Delete file","Are you absolutely certain you want to remove this file??") 
        if check==True: 
            fileName=os.path.basename(removeFriend)
            os.remove(removeFriend)#remove the chosen file name 
            messagebox.showinfo("delete file",f"{fileName} removed")
            if btnClearAll.state()==("disabled",):#
                showFriends() 
            else:
                Frame_Image.grid_remove()
                stateList.clear()#
                showFriends()
        else:
            messagebox.showinfo("remove file","The intended deletion failed") #if the useer selects not to delete a file a message is shown           

def addFriend(): # this function controls the addition process of a friend
    fileType=(("Image files","*.png;*.jpg;*.jpeg"),("All files","*.*")) 
    newFriend=filedialog.askopenfilename(initialdir=path,title="Choose a friend's picture to add them.",filetype=fileType)
    if newFriend: 
        check=messagebox.askquestion("Add a new file","Just confirming, you want to add someone new to your friends list?")
        if check=="yes": 
            (head_3,tail_3)=os.path.splitext(newFriend) 
            if tail_3.lower() not in [".png",".jpg",".jpeg"]:
                messagebox.showwarning("Error","It's not an Image file")
            else:
                shutil.copy(newFriend,path) 
                if btnClearAll.state()==("disabled",):
                    showFriends() 
                else: 
                    Frame_Image.grid_remove() 
                    stateList.clear() 
                    showFriends() 
        else:
            messagebox.showinfo("Add a new file","Couldn't add the new file")

def quitApp(): # a function which is made for quitting the app
    if messagebox.askyesno("Quit","Are you sure you want to close this application?"): 
        myApp.destroy() 


#Basic Window for your app
myApp = Tk()
myApp.title("Image display app by: Aryan Paudel") 
myApp.geometry("1200x800") 
myApp.configure(background='Khaki') 

#code to configure styles for your ttk widget

style=ttk.Style() 
style.theme_use('alt')
style.configure("TButton",fg="yellow",width=20,height=50,pady=5,font=("Times New Roman",17),borderwidth=3)
style.map('TButton',background=[('active','violet')])

#Create a frame(mainMenu) that will hold buttons to manage the app.
buttonFrame=LabelFrame(myApp,text="App Menu",background="grey",width=1200,height=75,font=("Times New Roman",12))
buttonFrame.grid(columnspan=9) 


# This creates a button that lets users see their friends list..
btnShowFriends=ttk.Button(buttonFrame,text="showFriends",style="TButton",command=showFriends)
btnShowFriends.grid(row=0,column=0) 0

# These lines of code instruct the program to build a button. Clicking this button (which is currently disabled and cannot be clicked) would remove all your friends from the list. You can also change how the button looks.
btnClearAll=ttk.Button(buttonFrame,text="Clear All",style="TButton", command=clearAll)
btnClearAll['state']='disabled'
btnClearAll.grid(row=0,column=1)

#Define a button for deleting a friend, set its text and style, and bind it to the delFriend function
btnDeleteFriend=ttk.Button(buttonFrame, text="Delete Friend",style="TButton", command=delFriend)
btnDeleteFriend.grid(row=0, column=2)


#This code creates a button for adding new friends. You can customize how it looks and what happens when it's clicked.
btnAddFriend=ttk.Button(buttonFrame,text="AddFriend", style="TButton", command=addFriend)
btnAddFriend.grid(row=0,column=3)


#This code creates a button that lets users close the application. You can also change how it looks
btnQuit=ttk.Button(buttonFrame,text="Quit", style="TButton", command=quitApp)
btnQuit.grid(row=0,column=4) 


#Adding a clock which shows timr in hour, min , sec and time zone.
def clock():
    # To get current time components
    hour = time.strftime("%I")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    day = time.strftime("%A")
    am_pm = time.strftime("%p")
    time_zone = time.strftime("%Z")

    # to update the label with the current time
    my_label.config(text=hour + ":" + minute + ":" + second + " " + am_pm)
    # Call the clock function again after 1000 milliseconds (1 second)
    my_label.after(1000, clock)
    # Update the second label with the time zone and day
    my_label2.config(text=time_zone + " , " + day)
# Function to update the label text
def update():
    my_label.config(text="New Text")
# Create a label for displaying the time
my_label = Label(myApp, text="", font=("Times New Roman", 15), fg='grey', bg='white')
my_label.grid(row=3,column=8)  
# Create a label for displaying the time zone and day
my_label2 = Label(myApp, text="", font=("Times New Roman", 15), fg='grey')
my_label2.grid(row=4,column=8) 

# Start the clock function to update time continuously
clock() 


 


myApp.mainloop()











                                                                                                 
