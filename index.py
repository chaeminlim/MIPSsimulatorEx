import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMainWindow, QLineEdit, QHBoxLayout, QBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from dataPath import dataPath

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.run_inst = dataPath(4)
        #self.set_registers()
        self.makeWidget()
        self.show()

    """def set_registers(self):
        
        labels = []

        for i in range(32):
            labels.append("label" + str(i))

        for i in range(32):
            labels[i] = QLabel('Helloworld' + str(i), self)
            labels[i].setAlignment(Qt.AlignHCenter)

        layout = QHBoxLayout()
        for i in range(32):
            layout.addWidget(labels[i])


        self.setWindowTitle('QLabel')
        self.setGeometry(500, 500, 500, 500)
"""
    def makeWidget(self):
        QWidget.__init__(self, flags=Qt.Widget)

        self.labels_R = []
        self.labels_I = []
        self.run_inst.run()
        regis_len = len(self.run_inst.Registers_log)
        self.inst_len = len(self.run_inst.inst_log)
        ############################################
        for i in range(32):
            self.labels_R.append("label" + str(i))
            self.labels_R[i] = QLabel()

        for i in range(self.inst_len):
            self.labels_I.append("label" + str(i))
            self.labels_I[i] = QLabel()

        # 레이아웃 선언 및 Form Widget에 설정
        self.layout_Register = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.layout_Instruction = QBoxLayout(QBoxLayout.TopToBottom)

        # 부모 레이아웃에 자식 레이아웃을 추가
        self.layout_Register.addLayout(self.layout_Instruction)

        self.setLayout(self.layout_Register)
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("Layout Basic")
        self.resize(500, 500)

        for i in range(32):
            self.labels_R[i].setText("Registers")
            self.labels_R[i].setStyleSheet("background-color: grey")
            self.layout_Register.addWidget(self.labels_R[i])


        for i in range(self.inst_len):
            self.labels_I[i].setText("Registers")
            self.labels_I[i].setStyleSheet("background-color: grey")
            self.layout_Instruction.addWidget(self.labels_I[i])

'''         
        self.lb_1.setStyleSheet("background-color: yellow")
        self.lb_2.setStyleSheet("background-color: red")
        self.lb_3.setStyleSheet("background-color: blue")
        self.lb_4.setStyleSheet("background-color: pink")
        self.lb_5.setStyleSheet("background-color: grey")

        self.layout_2.addWidget(self.lb_1)
        self.layout_2.addWidget(self.lb_2)
        self.layout_3.addWidget(self.lb_3)
        self.layout_3.addWidget(self.lb_4)
        self.layout_3.addWidget(self.lb_5)'''

if __name__ == "__main__":
    app = QApplication(sys.argv) #sys.argv는 디렉토리를 나타낸다.
    myWindow = MyWindow()
    app.exec_() # 이벤트 루프에 진입


