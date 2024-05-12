import threading


def thread1():
    count = 0
    for x in range(10):
        count += 1
        print('thread 1: ', count)


def thread2():
    count = 0
    for x in range(10):
        count += 1
        print('thread 2: ', count)


try:
    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)
    t1.start()
    t2.start()
except Exception as e:
    print(e)