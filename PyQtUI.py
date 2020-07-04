from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from NumBall import *

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 30)
        size.setWidth(max(size.width(), size.height()) + 35)
        return size
        
class PyQtUI(QWidget):
    def __init__(self, digit, diff):
        super().__init__(None)
        
        #message
        self.message = QLabel()
        self.message.setText('-> 을 눌러 게임을 시작하세요')        

        #display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(50)
        
        #button
        buttonLayout = QGridLayout()
        buttonGrid = [
            '1', '2', '3', 
            '4', '5', '6', 
            '7', '8', '9', 
            None, 'C', '->'
        ]
        rc = 0
        col = 3
        for btnText in buttonGrid:
            if btnText == None:
                rc += 1
                continue
            button = Button(btnText, self.buttonClicked)
            buttonLayout.addWidget(button, rc // col, rc % col)
            rc += 1
        
        #log
        self.log = QTextEdit()
        self.log.setDisabled(True)
        
        #mainLayout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addWidget(self.message, 0, 0, 1, 2)
        mainLayout.addWidget(self.display, 1, 0, 1, 2)
        mainLayout.addLayout(buttonLayout, 2, 0)
        mainLayout.addWidget(self.log, 3, 0, 1, 2)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("NumBall Game")
        
        self.game = Computer(digit, diff)
        
    def buttonClicked(self):
        sender = self.sender().text()
        game = self.game
        state = game.getState()
        
        if sender == 'C':
            self.display.clear()
        
        elif sender == '->':
            if state == 'start':
                self.message.setText('게임을 시작합니다')
                game.setState('setplayernum')
                
            elif state == 'setplayernum':
                self.message.setText('당신의 숫자를 입력하세요')
                game.setState('setplayernum_wait')
            elif state == 'setplayernum_wait' and game.isRight(self.display.text()):
                game.setPlayerNum(self.display.text())
                self.display.clear()
                self.message.setText('숫자를 정했습니다')
                game.setState('setcomputernum')
            elif state == 'setcomputernum':
                game.setComputerNum()
                self.message.setText('컴퓨터가 숫자를 정하였습니다')
                game.setState('playerattack')
                
            elif state == 'playerattack':
                self.message.setText('당신의 공격차례입니다 공격할 수를 입력해주세요')
                game.setState('playerattack_wait')
            elif state == 'playerattack_wait' and game.isRight(self.display.text()):
                attackNum, s, b = game.Attack(self.display.text())
                self.display.clear()
                self.message.setText('%s로 공격한 결과 strike: %d, ball: %d' % (attackNum, s, b))
                game.setState('computerattack')
                if not game.getWinner() == None: game.setState('end')
                
            elif state == 'computerattack':
                self.message.setText('컴퓨터가 공격할 차례입니다')
                game.setState('computerattack_wait')
            elif state == 'computerattack_wait':
                attackNum, s, b = game.Defend()
                self.message.setText('컴퓨터가 %s로 공격한 결과 strike: %d, ball: %d' % (attackNum, s, b)) 
                if not game.getWinner() == None: game.setState('end')
                else: game.setState('playerattack')
                
            elif state[-4:] == 'wait':
                self.message.setText('조건에 맞지 않는 숫자를 입력하였습니다 다시 입력해주세요')
                
            elif state == 'end':
                self.message.setText('게임이 끝났습니다 승자는 %s입니다 / 컴퓨터의 숫자) %s' % (game.getWinner(), game.getComputerNum()))
              
            self.log.append(self.message.text())
                
        else:
            self.display.setText(self.display.text() + sender)
              
