import sys
if __name__ == '__main__':
    try:
        config = open("config.txt", 'r')
    except:
        print("config파일이 존재하지 않습니다.")
        print("파일이 있는지 확인해주세요.")
        exit()
    
    try:
        for string in config.readlines():
            exec(string)
        IsDiscord = IsDiscord
        digit = int(digit)
        diff = int(diff)
        token = token
    except:
        print("config파일의 변수 정보가 맞지 않습니다.")
        print("config파일 내의 변수가 맞는지 확인해주세요.")
        exit()
    
    if IsDiscord == True:
        from DiscordUI import *
    else:
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import *
        from PyQtUI import *
        app = QApplication(sys.argv)
        gameUI = PyQtUI(digit, diff)
        gameUI.show()
        sys.exit(app.exec_())
