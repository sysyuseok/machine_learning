# %%writefile 파일 경로 -> cell의 내용을 파일로 저장.

def plus(num1,num2):
    return num1+ num2
def minus(num1,num2):
    return num1-num2
def multiply(num1,num2):
    return num1 * num2
def divide(num1,num2):
    if num2 != 0:
        return num1 / num2
    else :
        print("not available")
