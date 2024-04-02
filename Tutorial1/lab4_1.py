import mysql.connector
import datetime

def connect_mysql():
    connection = mysql.connector.connect(host='localhost', user='root', password="")
    return connection

def create_database(db):
    con = connect_mysql()
    cursor = con.cursor()
    cursor.execute('create database if not exists ' + db)
    cursor.execute('use ' + db)
    print("Cơ sở dữ liệu là ", db)
    cursor.execute("create table if not exists employee (employeeid varchar(10) primary key, fullname varchar(100), birthday date, phone varchar(100))")
    return con

def insert(id, name, birthday, phone, con):
    cursor = con.cursor()
    cursor.execute("insert into employee values(%s, %s, %s, %s)", (id, name, birthday, phone))
    con.commit()
    cursor.close()

def delete_employee(id, con):
    cursor = con.cursor()
    count = cursor.execute("delete from employee where employeeid=%s", (id,))
    con.commit()
    cursor.close()
    if count is not None and count > 0:
        print("Xóa thành công")
    else:
        print("Mã không tồn tại")

def show_all(con):
    cursor = con.cursor()
    cursor.execute("select employeeid, fullname, birthday, phone from employee")
    records = cursor.fetchall()
    print("------------------------------DANH SÁCH NHÂN VIÊN ------------------------------------")
    for r in records:
        print(r[0], "\t", r[1], "\t", r[2], "\t", r[3])
    cursor.close()

def input_employee(con):
    print("------------------------------DANH SÁCH NHÂN VIÊN ------------------------------------")
    while True:
        id = input("Ma NV:")
        name = input("Tên NV:")
        birthday = datetime.datetime.strptime(input("Ngày sinh dd/mm/yyyy:"), "%d/%m/%Y")
        phone = input("Điện thoại:")
        insert(id, name, birthday, phone, con)
        choose = input("Bạn có muốn nhập tiếp không? y/n:")
        if choose == "n":
            break
    print("--------------------------------------------------------------------------------------")

def search_by_name(name, con):
    cursor = con.cursor()
    cursor.execute("select employeeid, fullname, birthday, phone from employee where fullname like %s", ('%' + name + '%',))
    records = cursor.fetchall()
    if not records:
        print("Không tìm thấy nhân viên có tên", name)
    else:
        print("------------------------------KẾT QUẢ TÌM KIẾM ------------------------------------")
        for r in records:
            print(r[0], "\t", r[1], "\t", r[2], "\t", r[3])
    cursor.close()

def update_employee(id, con):
    cursor = con.cursor()

    # Kiểm tra xem mã nhân viên có tồn tại không
    cursor.execute("SELECT * FROM employee WHERE employeeid = %s", (id,))
    employee = cursor.fetchone()
    if employee is None:
        print("Mã nhân viên không tồn tại")
        cursor.close()
        return

    # Nhập các thông tin mới từ người dùng
    new_name = input("Nhập tên mới cho nhân viên: ")
    new_birthday = datetime.datetime.strptime(input("Nhập ngày sinh mới (dd/mm/yyyy): "), "%d/%m/%Y")
    new_phone = input("Nhập số điện thoại mới cho nhân viên: ")

    # Thực hiện cập nhật thông tin của nhân viên trong cơ sở dữ liệu
    cursor.execute("UPDATE employee SET fullname = %s, birthday = %s, phone = %s WHERE employeeid = %s", (new_name, new_birthday, new_phone, id))
    con.commit()

    print("Cập nhật thông tin nhân viên thành công")

    cursor.close()


con = create_database('lab4_1')

while True:
    print("1. Nhập nhân viên")
    print("2. Hiển thị tất cả nhân viên")
    print("3. Xóa nhân viên")
    print("4. Tìm kiếm nhân viên theo tên")
    print("5. Sửa số điện thoại của nhân viên")
    print("6. Thoát")
    choose = input("Chọn một chức năng:")
    if choose == "1":
        input_employee(con)
    elif choose == "2":
        show_all(con)
    elif choose == "3":
        id = input("Nhập mã cần xóa:")
        delete_employee(id, con)
    elif choose == "4":
        name = input("Nhập tên nhân viên cần tìm kiếm:")
        search_by_name(name, con)
    elif choose == "5":
        id = input("Nhập mã nhân viên cần sửa:")
        update_employee(id, con)
        print("Sửa số điện thoại thành công!")
    elif choose == "6":
        break
    else:
        print("Bạn chọn sai rồi")
print("KẾT THÚC CHƯƠNG TRÌNH")
