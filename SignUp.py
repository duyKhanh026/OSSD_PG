from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox
import KetNoiCSDL
import SignIn

def TaoCuaSo(win: Tk):
    win.title("Register")
    # win.attributes("-topmost", True)
    win.resizable(False, False)
    win.configure(background='black')
    window_width = 1000
    window_height = 600
    '''
        Lấy ra kích thước cửa sổ
    '''
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    '''
        Tọa độ đặt cửa sổ
    '''

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    win.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

win = Tk()
TaoCuaSo(win)

# Kết nối đến cơ sở dữ liệu SQLite
conn = KetNoiCSDL.connect_to_database()
c = conn.cursor()



# Thêm hình ảnh
import_img = Image.open("GUI/image.png")
resize = import_img.resize((500,600), Image.LANCZOS)
img = ImageTk.PhotoImage(resize)

hinh_anh = Label(win, text="aaaa", font=("Times New Roman", 11), image=img)
hinh_anh.place(x=0, y=0, relwidth=0.5, relheight=1)

Frame_Register = Frame(win, bg="white")
Frame_Register.place(x=500, y=0, relwidth=0.5, width=500, height=600)

# Tiêu đề và phụ đề
Title = Label(Frame_Register, text="Register Here", font=("Impact", 35, "bold"), fg="#7B68EE", bg="white")
Title.place(x=90, y=100)

Subtitle = Label(Frame_Register, text="Create new account", font=("Times New Roman", 15), fg="black", bg="white")
Subtitle.place(x=90, y=160)

# Nhập thông tin
lbl_UserName = Label(Frame_Register, text="User name", font=("Times New Roman", 15), fg="gray", bg="white")
lbl_UserName.place(x=90, y=230)

entry_UserName = Entry(Frame_Register, font=("Times New Roman", 14), bg="#D3D3D3", width=40)
entry_UserName.place(x=90, y=270)
entry_UserName.focus()

lbl_Password = Label(Frame_Register, text="Password", font=("Times New Roman", 15), fg="gray", bg="white")
lbl_Password.place(x=90, y=330)

entry_Passwd = Entry(Frame_Register, font=("Times New Roman", 14), bg="#D3D3D3", width=40, show="*")
entry_Passwd.place(x=90, y=370)

# Nhập thông tin
lbl_NameCharacter = Label(Frame_Register, text="Name Character", font=("Times New Roman", 15), fg="gray", bg="white")
lbl_NameCharacter.place(x=90, y=430)

entry_NameCharacter = Entry(Frame_Register, font=("Times New Roman", 14), bg="#D3D3D3", width=40)
entry_NameCharacter.place(x=90, y=470)

# Chức năng đăng ký
def Register():
    userName = entry_UserName.get()
    passwd = entry_Passwd.get()
    namecharacter = entry_NameCharacter.get()

    if userName == "" or passwd == "" or namecharacter == "":
        tkinter.messagebox.showerror(title="Error", message="Không được để trống thông tin")
    else:
        # Kiểm tra xem tên đăng nhập đã tồn tại chưa
        c.execute("SELECT * FROM account WHERE Username=%s", (userName,))
        if c.fetchone():
            tkinter.messagebox.showerror(title="Error", message="Tên đăng nhập đã tồn tại")
        else:
            # Thêm người dùng mới vào cơ sở dữ liệu
            c.execute("INSERT INTO account (Username, Password, NameCharacter) VALUES (%s, %s, %s)",
                        (userName, passwd, namecharacter))
            conn.commit()
            # Hiển thị thông báo đăng ký thành công
            tkinter.messagebox.showinfo(title="Success", message="Đã đăng ký tài khoản thành công")

# Tạo nút đăng ký
btn_Register = Button(Frame_Register, text="Register", font=("Times New Roman", 15), bg="#7B68EE", fg="white", bd=0, width=20, command=Register)
btn_Register.place(x=90, y=530)

# Chuyển đổi sang giao diện đăng nhập
def open_login_window():
    win.destroy()  # Đóng cửa sổ đăng ký
    # Mở cửa sổ đăng nhập
    SignIn.main()

btn_Login = Button(Frame_Register, text="Log In", font=("Times New Roman", 15), bg="green", fg="white", bd=0, width=10, command=open_login_window)
btn_Login.place(x=300, y=530)

win.mainloop()

