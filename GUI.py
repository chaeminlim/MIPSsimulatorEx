import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,\
    QVBoxLayout,QGroupBox, QMainWindow, QLineEdit,QMessageBox, QTextEdit,\
    QHBoxLayout, QBoxLayout, QScrollArea, QPushButton, QAction, qApp, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from dataPath import dataPath
from readbinary import *

global prev_PC, isAssem

prev_PC = 0
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.run_inst = dataPath()
        self.run_inst.setup()
        #self.set_registers()
        self.makeWidget()
        self.show()

    def makeWidget(self):
        QWidget.__init__(self, flags=Qt.Widget)

        self.label_R = QLabel()
        self.label_I = QLabel()
        #임시로 정보를 받아옵니다.
        self.label_R.setStyleSheet('QLabel { font-family: "Lucida Console", Monospace ;margin: 0; font-weight: normal;}')

        self.R_list = self.run_inst.Registers
        regis_len = len(self.run_inst.Registers_log)
        self.inst_len = len(self.run_inst.inst_log)

        ############################################



        # 레이아웃 선언 및 Form Widget에 설정
        self.layout_main = QVBoxLayout()
        self.layout_Register = QVBoxLayout()
        self.layout_Instruction = QVBoxLayout()
        self.layout_total = QHBoxLayout()
        self.layout_buttons = QHBoxLayout()
        # making scroll
        self.scrollArea1 = QScrollArea()
        self.scrollArea2 = QScrollArea()


        # 부모 레이아웃에 자식 레이아웃을 추가
        self.layout_total.addLayout(self.layout_Register)
        self.layout_total.addLayout(self.layout_Instruction)
        self.layout_main.addLayout(self.layout_buttons)
        self.layout_main.addLayout(self.layout_total)
        self.setLayout(self.layout_main)

        self.init_widget()
        self.init_button()

    def init_button(self):

        btn_step = QPushButton("step")
        btn_file = QPushButton("load BinaryFile")
        btn_fileA = QPushButton('load AssemblyFile')
        btn_step.setStyleSheet('QPushButton {background-color: #A3C1DA; color: white;}')
        btn_file.setStyleSheet('QPushButton {background-color: #A3C1DA; color: white;}')
        btn_fileA.setStyleSheet('QPushButton {background-color: #A3C1DA; color: white;}')

        self.layout_buttons.addWidget(btn_file)
        self.layout_buttons.addWidget(btn_step)
        self.layout_buttons.addWidget(btn_fileA)
        btn_step.clicked.connect(self.btn_step_clicked)
        btn_file.clicked.connect(self.btn_file_clicked)
        btn_fileA.clicked.connect(self.btn_fileA_clicked)
        # toolbars

    def init_widget(self, isAssembly=None):

        self.setWindowTitle("Layout Basic")
        self.setGeometry(800, 200, 600, 800)
        #
        self.label_R.setText("PC: 0x%08X\nR0: 0x%08X\nR1: 0x%08X\nR2: 0x%08X\nR3: 0x%08X\n"
                             "R4: 0x%08X\nR5: 0x%08X\nR6: 0x%08X\nR7: 0x%08X\n"
                             "R8: 0x%08X\nR9: 0x%08X\nR10: 0x%08X\nR11: 0x%08X\n"
                             "R12: 0x%08X\nR13: 0x%08X\nR14: 0x%08X\nR15: 0x%08X\n"
                             "R16: 0x%08X\nR17: 0x%08X\nR18: 0x%08X\nR19: 0x%08X\n"
                             "R20: 0x%08X\nR21: 0x%08X\nR22: 0x%08X\nR23: 0x%08X\n"
                             "R24: 0x%08X\nR25: 0x%08X\nR26: 0x%08X\nR27: 0x%08X\n"
                             "R28: 0x%08X\nR29: 0x%08X\nR30: 0x%08X\nR31: 0x%08X\n"
                             %(0x0000, self.R_list[0],self.R_list[1],self.R_list[2],self.R_list[3],
                               self.R_list[4],self.R_list[5],self.R_list[6],self.R_list[7],
                               self.R_list[8],self.R_list[9],self.R_list[10],self.R_list[11],
                               self.R_list[12],self.R_list[13],self.R_list[14],self.R_list[15],
                               self.R_list[16],self.R_list[17],self.R_list[18],self.R_list[19],
                               self.R_list[20],self.R_list[21],self.R_list[22],self.R_list[23],
                               self.R_list[24],self.R_list[25],self.R_list[26],self.R_list[27],
                               self.R_list[28],self.R_list[29],self.R_list[30],self.R_list[31],)
                             )
        #
        self.scrollArea1.setWidget(self.label_R)
        self.layout_Register.addWidget(self.scrollArea1)
####################################################################
        sgruopbox = QGroupBox()
        layout_groupbox = QVBoxLayout(sgruopbox)

        if isAssembly == None:
            self.decodedList = self.run_inst.decodeInstr()
            length = len(self.run_inst.readBin.codeList) + 9
            self.instr = [0]*(length)
            self.decoded = [0]*(length)
            Memstart = 0x00400000
            for i in range(length):
                layout_Horiz = QHBoxLayout()
                self.instr[i] = QLabel("[%08X] 0x%08X"
                               % (Memstart, self.run_inst.Mem.MEM(Memstart, "", 0, 2)))
                self.decoded[i] = QLabel("%s" % self.decodedList[i])
                self.instr[i].setStyleSheet(
                    'QLabel { font-family: "Lucida Console", Monospace ;margin: 0; font-weight: normal;}')
                self.decoded[i].setStyleSheet(
                    'QLabel { font-family: "Lucida Console", Monospace ;margin: 0; font-weight: bold;}')


                layout_Horiz.addWidget(self.instr[i])
                layout_Horiz.addWidget(self.decoded[i])
                layout_groupbox.addLayout(layout_Horiz)
                Memstart += 0x4

        elif isAssembly == 1:
            self.decodedList = self.run_inst.decodeInstr(1)
            length = len(self.run_inst.instList) + 9
            self.instr = [0] * length
            self.decoded = [0] * length
            Memstart = 0x00400000
            instval = []
            for i in range(length):
                layout_Horiz = QHBoxLayout()
                self.instr[i] = QLabel("[%08X] 0x%08X"
                                % (Memstart, self.run_inst.Mem.MEM(Memstart, "", 0, 2)))
                self.decoded[i] = QLabel("%s" % self.decodedList[i])
                self.instr[i].setStyleSheet(
                    'QLabel { font-family: "Lucida Console", Monospace ;margin: 0; font-weight: normal;}')
                self.decoded[i].setStyleSheet(
                    'QLabel { font-family: "Lucida Console", Monospace ;margin: 0; font-weight: bold;}')

                instval.append(self.run_inst.Mem.MEM(Memstart, "", 0, 2))
                layout_Horiz.addWidget(self.instr[i])
                layout_Horiz.addWidget(self.decoded[i])
                layout_groupbox.addLayout(layout_Horiz)
                Memstart += 0x4


        self.scrollArea2.setWidget(sgruopbox)
        self.layout_Instruction.addWidget(self.scrollArea2)

    def btn_step_clicked(self):
        global prev_PC, isAssem
        prev_PC = self.run_inst.ProgramCounter

        self.run_inst.step(isAssem)
        self.label_R.setText("PC: 0x%08X\nR0: 0x%08X\nR1: 0x%08X\nR2: 0x%08X\nR3: 0x%08X\n"
                             "R4: 0x%08X\nR5: 0x%08X\nR6: 0x%08X\nR7: 0x%08X\n"
                             "R8: 0x%08X\nR9: 0x%08X\nR10: 0x%08X\nR11: 0x%08X\n"
                             "R12: 0x%08X\nR13: 0x%08X\nR14: 0x%08X\nR15: 0x%08X\n"
                             "R16: 0x%08X\nR17: 0x%08X\nR18: 0x%08X\nR19: 0x%08X\n"
                             "R20: 0x%08X\nR21: 0x%08X\nR22: 0x%08X\nR23: 0x%08X\n"
                             "R24: 0x%08X\nR25: 0x%08X\nR26: 0x%08X\nR27: 0x%08X\n"
                             "R28: 0x%08X\nR29: 0x%08X\nR30: 0x%08X\nR31: 0x%08X\n"
                             % (0x0000, self.R_list[0], self.R_list[1], self.R_list[2], self.R_list[3],
                                self.R_list[4], self.R_list[5], self.R_list[6], self.R_list[7],
                                self.R_list[8], self.R_list[9], self.R_list[10], self.R_list[11],
                                self.R_list[12], self.R_list[13], self.R_list[14], self.R_list[15],
                                self.R_list[16], self.R_list[17], self.R_list[18], self.R_list[19],
                                self.R_list[20], self.R_list[21], self.R_list[22], self.R_list[23],
                                self.R_list[24], self.R_list[25], self.R_list[26], self.R_list[27],
                                self.R_list[28], self.R_list[29], self.R_list[30], self.R_list[31],)
                             )

        print("%08x" % self.run_inst.ProgramCounter)
        index = (self.run_inst.ProgramCounter - 0x00400000)/4
        index = int(index)
        prev_index = (prev_PC -0x00400000)/4
        prev_index = int(prev_index)
        #print("%08x" % (self.run_inst.ProgramCounter - 0x00400000)/4 - 1)
        #print("%08x" % (self.run_inst.ProgramCounter - 0x00400000)/4)

        self.instr[prev_index].setStyleSheet("background-color: None")
        self.instr[index].setStyleSheet("background-color: red")

        if self.decodedList[index] == "syscall":
            if self.R_list[2] == 10:
                QMessageBox.about(self, "알림", "syscall %d 호출로 종료되었습니다." %(self.R_list[2]))
            if self.R_list[2] == 1:
                QMessageBox.about(self, "알림", "syscall 1 :\n %d" %(self.R_list[4] - 0x100000000))


    def btn_file_clicked(self):
        global isAssem
        isAssem= None
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "바이너리 파일을 열어주세요", "",
                                                  "All Files (*);;Binary Files (*.bin)", options=options)
        if fileName:
            self.run_inst.run(fileName)
            self.init_widget()

    def btn_fileA_clicked(self):
        global isAssem
        isAssem = 1
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "어셈블리 파일을 열어주세요", "",
                                                  "All Files (*);;Assembly Files (*.s)", options=options)
        if fileName:
            self.run_inst.run(fileName, 1)
            self.init_widget(1)


if __name__ == "__main__":
    app = QApplication(sys.argv) #sys.argv는 디렉토리를 나타낸다.
    myWindow = MyWindow()
    try:
        app.exec_() # 이벤트 루프에 진입
    except Exception as e:
        print(e)

