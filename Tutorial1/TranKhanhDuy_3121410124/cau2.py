class FibonacciGenerator:
    @staticmethod
    def generate_sequence(n):
        def fibonacci(n):
            if n <= 0:
                return []
            elif n == 1:
                return [0]
            elif n == 2:
                return [0, 1]
            else:
                sq = fibonacci(n - 1)
                sq.append(sq[-1] + sq[-2])
                return sq
        if n <= 0:
            return []
        else:
            return fibonacci(n)

def main():
    try:
        n = int(input("Nhập số phần tử của dãy Fibonacci cần tạo: "))
        fib_sq = FibonacciGenerator.generate_sequence(n)
        print("Dãy Fibonacci được tạo:")
        for i in fib_sq:
            print(i, end=" ")
    except ValueError:
        print("Đầu vào bị lỗi!.")

if __name__ == "__main__":
    main()
