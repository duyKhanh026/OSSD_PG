from tkinter import *
from PIL import  ImageTk, Image
import tkinter.messagebox
import KetNoiCSDL
import SignUp
from main import Main


def TaoCuaSo(win: Tk):
    win.title("Log In")
   # win.attributes("-topmost", True)
    win.resizable(False, False)
    win.configure(background='black')
    window_width = 1000
    window_height = 600
    '''
        Lay ra kich thuoc kich thuoc cua man hinh
    '''
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    '''
        Toa do dat cua so
    '''

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    win.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    



win = Tk()
TaoCuaSo(win)

#Them hinh anh
import_img = (Image.open("GUI/image.png"))
resize = import_img.resize((500,600), Image.LANCZOS)
img = ImageTk.PhotoImage(resize)

hinh_anh = Label(win, text= "aaaa", font= ("Times New Roman",11 ), image = img)
# relwidth and relheight la dat vi tri tuong doi tuong ung voi cua so
hinh_anh.place(x=0, y = 0 , relwidth = 0.5 , relheight = 1)


Frame_LogIn = Frame(win, bg = "white")
Frame_LogIn.place(x = 500, y = 0 , relwidth= 0.5, width = 500, height = 600)

#Title and Subtitle

Title = Label(Frame_LogIn, text = "Login Here", font = ("Impact", 35, "bold"), fg = "#7B68EE", bg = "white")
Title.place (x = 90, y = 100)

Subtitle = Label(Frame_LogIn, text = "Members login area", font = ("Times New Roman", 15), fg = "black", bg = "white")
Subtitle.place(x =90, y = 160)

# Nhap thong tin

lbl_UserName = Label(Frame_LogIn, text = "User name", font = ("Times New Roman",15), fg = "gray", bg = "white")
lbl_UserName.place(x = 90 , y = 230)

entry_UserName = Entry(Frame_LogIn, font= ("Times New Roman", 14), bg = "#D3D3D3" ,width = 40)
entry_UserName.place(x = 90 , y = 270)
entry_UserName.focus()

lbl_Password = Label(Frame_LogIn, text = "Password" , font= ("Times New Roman",15), fg = "gray" , bg = "white")
lbl_Password.place(x = 90 , y = 330)

entry_Passwd = Entry(Frame_LogIn, font= ("Times New Roman", 14), bg = "#D3D3D3" ,width = 40, show = "*")
entry_Passwd.place(x = 90 , y = 370)




# Chuc nang dang nhap

ListTaiKhoan = KetNoiCSDL.get_account_list()

def check_List(name, password):
    for account in ListTaiKhoan:
        print(account[0])
        if(account[1] == name and account[2] == password): 
            return True
    
    return False

def LogIn():
    userName = entry_UserName.get()
    passwd = entry_Passwd.get()
    print(ListTaiKhoan)
    if(userName == "" or passwd == ""):
        tkinter.messagebox.showerror(title= "Error", message= "Khong duoc de trong thong tin")
    elif(check_List(userName, passwd) == False):
        tkinter.messagebox.showerror(title= "Error", message= "Sai thong tin dang nhap hoac tai khoan dang bi khoa")
    else:
        tkinter.messagebox.showinfo(title= "Welcome", message = "Welcome " + userName)
        main_app = Main()  # Tạo đối tượng Main
        main_app.run()
        
# Tao nut an de dang nhap

btn_Submit = Button(Frame_LogIn, text = "Log In", font = ("Times New Roman", 15) , bg = "#7B68EE", fg = "white" , bd = 0, width = 20, command = LogIn)
btn_Submit.place(x = 90 , y = 470)

# Thêm nút và chức năng để chuyển sang đăng ký
def open_register_window():
    win.destroy()  # Đóng cửa sổ đăng nhập
    # Mở cửa sổ đăng ký
    SignUp.main()

btn_Register = Button(Frame_LogIn, text="Register", font=("Times New Roman", 15), bg="green", fg="white", bd=0, width=10, command=open_register_window)
btn_Register.place(x=300, y=470)


win.mainloop()

