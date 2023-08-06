import sys, time
def check():
    t = time.strftime("%H")
    print(t)
    if int(t) == 23 or int(t) == 0 or int(t) == 1 or int(t) == 2 or int(t) == 3 or int(t) == 4:
        print("程序访问被禁止！您可以注释此段代码……")
        sys.exit()