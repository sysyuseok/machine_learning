import time
def my_sleep(seconds):
    time.sleep(seconds)
def main():
    my_sleep(1)
    my_sleep(2)
    my_sleep(3)
    my_sleep(4)
print(__name__)
if __name__=="__main__": #import할때는 동작하지 않도록 설정해준 부분
    start = time.time()
    main()
    end=time.time()
    print("걸린시간:",end-start,"초")
    
