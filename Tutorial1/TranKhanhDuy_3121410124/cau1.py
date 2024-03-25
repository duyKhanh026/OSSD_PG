import json

# Hàm để tải dữ liệu từ tệp JSON
def load_data():
    try:
        with open('students.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

# Hàm để lưu dữ liệu vào tệp JSON
def save_data(data):
    with open('students.json', 'w') as file:
        json.dump(data, file, indent=4)

# Hàm để thêm sinh viên mới vào danh sách
def add_student(data):
    student_id = input("Nhập mã sinh viên: ")
    name = input("Nhập tên: ")
    age = input("Nhập tuổi: ")
    address = input("Nhập địa chỉ: ")
    new_student = {"mã sinh viên": student_id, "tên": name, "tuổi": age, "địa chỉ": address}
    data.append(new_student)
    save_data(data)
    print("Đã thêm sinh viên thành công!")

# Hàm để xóa sinh viên khỏi danh sách bằng mã sinh viên
def delete_student(data):
    student_id = input("Nhập mã sinh viên của sinh viên cần xóa: ")
    for student in data:
        if student["mã sinh viên"] == student_id:
            data.remove(student)
            save_data(data)
            print("Đã xóa sinh viên thành công!")
            return
    print("Không tìm thấy sinh viên có mã số này.")

# Hàm để cập nhật thông tin của sinh viên
def update_student(data):
    student_id = input("Nhập mã sinh viên của sinh viên cần cập nhật: ")
    for student in data:
        if student["mã sinh viên"] == student_id:
            print("Chọn thông tin cần cập nhật:")
            print("1. Tên")
            print("2. Tuổi")
            print("3. Địa chỉ")
            choice = input("Nhập lựa chọn: ")
            if choice == "1":
                student["tên"] = input("Nhập tên mới: ")
            elif choice == "2":
                student["tuổi"] = input("Nhập tuổi mới: ")
            elif choice == "3":
                student["địa chỉ"] = input("Nhập địa chỉ mới: ")
            else:
                print("Lựa chọn không hợp lệ.")
            save_data(data)
            print("Đã cập nhật thông tin sinh viên thành công!")
            return
    print("Không tìm thấy sinh viên có mã số này.")

# Hàm để hiển thị thông tin của tất cả sinh viên trong danh sách
def display_students(data):
    if not data:
        print("Danh sách sinh viên rỗng.")
    else:
        print("+-------------------------------------------------------------------------------+")
        print("| {:<15} {:<20} {:<10} {:<30}|".format("Mã sinh viên", "Tên", "Tuổi", "Địa chỉ"))
        print("|" + "-" * 79 + "|")
        for student in data:
            print("| {:<15} {:<20} {:<10} {:<30}|".format(student["mã sinh viên"], student["tên"], student["tuổi"], student["địa chỉ"]))
        print("+" + "-" * 79 + "+")


# Hàm main
def main():
    data = load_data()
    while True:
        print("\nCHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN")
        print("1. Thêm sinh viên")
        print("2. Xóa sinh viên")
        print("3. Cập nhật thông tin sinh viên")
        print("4. Hiển thị danh sách sinh viên")
        print("5. Thoát chương trình")
        choice = input("Nhập lựa chọn của bạn: ")
        if choice == "1":
            add_student(data)
        elif choice == "2":
            delete_student(data)
        elif choice == "3":
            update_student(data)
        elif choice == "4":
            display_students(data)
        elif choice == "5":
            print("Đã thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    main()
