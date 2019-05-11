import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QGroupBox, QMainWindow, QLineEdit, QHBoxLayout, QBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from dataPath import dataPath

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.run_inst = dataPath(4)
        #self.set_registers()
        self.makeWidget()
        self.show()

    def makeWidget(self):
        QWidget.__init__(self, flags=Qt.Widget)

        self.label_R = QLabel()
        self.label_I = QLabel()
        self.run_inst.run()
        #임시로 정보를 받아옵니다.
        self.R_list = self.run_inst.Registers
        regis_len = len(self.run_inst.Registers_log)
        self.inst_len = len(self.run_inst.inst_log)

        ############################################



        # 레이아웃 선언 및 Form Widget에 설정
        self.layout_Register = QVBoxLayout()
        self.layout_Instruction = QVBoxLayout()
        self.layout_total = QHBoxLayout()
        # making scroll
        self.scrollArea1 = QScrollArea()
        self.scrollArea2 = QScrollArea()

        # 부모 레이아웃에 자식 레이아웃을 추가
        self.layout_total.addLayout(self.layout_Register)
        self.layout_total.addLayout(self.layout_Instruction)

        self.setLayout(self.layout_total)
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("Layout Basic")
        self.setGeometry(800, 200, 500, 300)


        self.label_R.setText("R0: %s\nR1: %s\nR2: %s\nR3: %s\n"
                             "R4: %s\nR5: %s\nR6: %s\nR7: %s\n"
                             "R8: %s\nR9: %s\nR10: %s\nR11: %s\n"
                             "R12: %s\nR13: %s\nR14: %s\nR15: %s\n"
                             "R16: %s\nR17: %s\nR18: %s\nR19: %s\n"
                             "R20: %s\nR21: %s\nR22: %s\nR23: %s\n"
                             "R24: %s\nR25: %s\nR26: %s\nR27: %s\n"
                             "R28: %s\nR29: %s\nR30: %s\nR31: %s\n"
                             %(self.R_list[0],self.R_list[1],self.R_list[2],self.R_list[3],
                               self.R_list[4],self.R_list[5],self.R_list[6],self.R_list[7],
                               self.R_list[8],self.R_list[9],self.R_list[10],self.R_list[11],
                               self.R_list[12],self.R_list[13],self.R_list[14],self.R_list[15],
                               self.R_list[16],self.R_list[17],self.R_list[18],self.R_list[19],
                               self.R_list[20],self.R_list[21],self.R_list[22],self.R_list[23],
                               self.R_list[24],self.R_list[25],self.R_list[26],self.R_list[27],
                               self.R_list[28],self.R_list[29],self.R_list[30],self.R_list[31],)
                             )
        #

        #
        self.scrollArea1.setWidget(self.label_R)
        self.layout_Register.addWidget(self.scrollArea1)
####################################################################

        sgruopbox = QGroupBox("Group")
        layout_groupbox = QVBoxLayout(sgruopbox)
        for i in range(self.inst_len):
            hello = QLabel("inst %d: %d" % (i, self.run_inst.inst_log[i]))
            layout_groupbox.addWidget(hello)


        self.scrollArea2.setWidget(sgruopbox)


        self.layout_Instruction.addWidget(self.scrollArea2)
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


