# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QComboBox
from s_des import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.input_type = QComboBox()
        self.input_type.addItem("二进制")
        self.input_type.addItem("ASCII")

        self.encrypt_text = QLineEdit()
        self.encrypt_key = QLineEdit()
        self.decrypt_text = QLineEdit()
        self.decrypt_key = QLineEdit()
        self.result_box = QTextEdit()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("输入类型:"))
        layout.addWidget(self.input_type)

        layout.addWidget(QLabel("加密信息:"))
        layout.addWidget(self.encrypt_text)
        layout.addWidget(QLabel("密钥:"))
        layout.addWidget(self.encrypt_key)
        encrypt_button = QPushButton("加密")
        encrypt_button.clicked.connect(self.encrypt_clicked)
        layout.addWidget(encrypt_button)

        layout.addWidget(QLabel("解密信息:"))
        layout.addWidget(self.decrypt_text)
        layout.addWidget(QLabel("密钥:"))
        layout.addWidget(self.decrypt_key)
        decrypt_button = QPushButton('解密')
        decrypt_button.clicked.connect(self.decrypt_clicked)
        layout.addWidget(decrypt_button)

        layout.addWidget(QLabel("结果:"))
        layout.addWidget(self.result_box)

        self.setLayout(layout)
        self.setWindowTitle('S-DES Encryptor/Decryptor')
        self.show()

    def encrypt_clicked(self):
        pt = self.encrypt_text.text()
        key = self.encrypt_key.text()

        if not key or len(key) != 10 or not all(c in '01' for c in key):
            self.result_box.setPlainText('错误: 密钥必须是10位0或1组成的字符串')
            return

        keys = keygen([int(i) for i in key])

        if self.input_type.currentText() == "二进制":
            if not pt or len(pt) != 8 or not all(c in '01' for c in pt):
                self.result_box.setPlainText('错误: 明文必须是8位0或1组成的字符串')
                return
            pt = [int(i) for i in pt]
            cipher = encrypt(pt, keys)
            self.result_box.setPlainText('加密结果: ' + ''.join([str(i) for i in cipher]))
        else:
            cipher_text = ""
            for char in pt:
                bin_char = [int(i) for i in format(ord(char), '08b')]
                cipher = encrypt(bin_char, keys)
                cipher_text += chr(int(''.join([str(i) for i in cipher]), 2))
            self.result_box.setPlainText('加密结果: ' + cipher_text)

    def decrypt_clicked(self):
        ct = self.decrypt_text.text()
        key = self.decrypt_key.text()

        if not key or len(key) != 10 or not all(c in '01' for c in key):
            self.result_box.setPlainText('错误: 密钥必须是10位0或1组成的字符串')
            return

        keys = keygen([int(i) for i in key])

        if self.input_type.currentText() == "二进制":
            if not ct or len(ct) != 8 or not all(c in '01' for c in ct):
                self.result_box.setPlainText('错误: 密文必须是8位0或1组成的字符串')
                return
            ct = [int(i) for i in ct]
            plain = decrypt(ct, keys)
            self.result_box.setPlainText('解密结果: ' + ''.join([str(i) for i in plain]))
        else:
            plain_text = ""
            for char in ct:
                bin_char = [int(i) for i in format(ord(char), '08b')]
                plain = decrypt(bin_char, keys)
                plain_text += chr(int(''.join([str(i) for i in plain]), 2))
            self.result_box.setPlainText('解密结果: ' + plain_text)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())