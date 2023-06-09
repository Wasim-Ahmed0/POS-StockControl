# Form implementation generated from reading ui file 'frmSuppliers.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_frmSuppliers(object):
    def setupUi(self, frmSuppliers):
        frmSuppliers.setObjectName("frmSuppliers")
        frmSuppliers.resize(980, 500)
        frmSuppliers.setStyleSheet("background-color: rgb(10, 16, 30);")
        self.centralwidget = QtWidgets.QWidget(parent=frmSuppliers)
        self.centralwidget.setObjectName("centralwidget")
        self.lblUsername = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblUsername.setGeometry(QtCore.QRect(0, 0, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lblUsername.setFont(font)
        self.lblUsername.setStyleSheet("color: rgb(230, 230, 230);")
        self.lblUsername.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblUsername.setObjectName("lblUsername")
        self.lblLogo = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblLogo.setGeometry(QtCore.QRect(850, 0, 121, 81))
        self.lblLogo.setText("")
        self.lblLogo.setPixmap(QtGui.QPixmap("../Images/AlaturkaPlain.png"))
        self.lblLogo.setScaledContents(True)
        self.lblLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblLogo.setObjectName("lblLogo")
        self.txtName = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txtName.setGeometry(QtCore.QRect(340, 120, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txtName.setFont(font)
        self.txtName.setStyleSheet("color: rgb(255, 255, 255);")
        self.txtName.setObjectName("txtName")
        self.btnBack = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnBack.setGeometry(QtCore.QRect(10, 440, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.btnBack.setFont(font)
        self.btnBack.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(132, 116, 77);")
        self.btnBack.setObjectName("btnBack")
        self.btnSave = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnSave.setGeometry(QtCore.QRect(800, 290, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.btnSave.setFont(font)
        self.btnSave.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(132, 116, 77);")
        self.btnSave.setObjectName("btnSave")
        self.lblSName = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblSName.setGeometry(QtCore.QRect(100, 120, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblSName.setFont(font)
        self.lblSName.setStyleSheet("color: rgb(255, 255, 255);")
        self.lblSName.setObjectName("lblSName")
        self.lblSAddress = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblSAddress.setGeometry(QtCore.QRect(100, 190, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblSAddress.setFont(font)
        self.lblSAddress.setStyleSheet("color: rgb(255, 255, 255);")
        self.lblSAddress.setObjectName("lblSAddress")
        self.txtAddress = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txtAddress.setGeometry(QtCore.QRect(340, 190, 261, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txtAddress.setFont(font)
        self.txtAddress.setStyleSheet("color: rgb(255, 255, 255);")
        self.txtAddress.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.txtAddress.setObjectName("txtAddress")
        self.lblSTelephone = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblSTelephone.setGeometry(QtCore.QRect(100, 300, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblSTelephone.setFont(font)
        self.lblSTelephone.setStyleSheet("color: rgb(255, 255, 255);")
        self.lblSTelephone.setObjectName("lblSTelephone")
        self.txtPhone = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txtPhone.setGeometry(QtCore.QRect(380, 300, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txtPhone.setFont(font)
        self.txtPhone.setStyleSheet("color: rgb(255, 255, 255);")
        self.txtPhone.setObjectName("txtPhone")
        self.txtFindName = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txtFindName.setGeometry(QtCore.QRect(770, 120, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txtFindName.setFont(font)
        self.txtFindName.setStyleSheet("color: rgb(255, 255, 255);")
        self.txtFindName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.txtFindName.setObjectName("txtFindName")
        self.btnFind = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnFind.setGeometry(QtCore.QRect(800, 170, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.btnFind.setFont(font)
        self.btnFind.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(132, 116, 77);")
        self.btnFind.setObjectName("btnFind")
        self.btnEdit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnEdit.setGeometry(QtCore.QRect(800, 230, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.btnEdit.setFont(font)
        self.btnEdit.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(132, 116, 77);")
        self.btnEdit.setObjectName("btnEdit")
        self.btnDelete = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnDelete.setGeometry(QtCore.QRect(800, 350, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.btnDelete.setFont(font)
        self.btnDelete.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(132, 116, 77);")
        self.btnDelete.setObjectName("btnDelete")
        frmSuppliers.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=frmSuppliers)
        self.statusbar.setObjectName("statusbar")
        frmSuppliers.setStatusBar(self.statusbar)

        self.retranslateUi(frmSuppliers)
        QtCore.QMetaObject.connectSlotsByName(frmSuppliers)

    def retranslateUi(self, frmSuppliers):
        _translate = QtCore.QCoreApplication.translate
        frmSuppliers.setWindowTitle(_translate("frmSuppliers", "Suppliers"))
        self.lblUsername.setText(_translate("frmSuppliers", "username"))
        self.txtName.setPlaceholderText(_translate("frmSuppliers", "Full Name of Supplier"))
        self.btnBack.setText(_translate("frmSuppliers", "BACK"))
        self.btnSave.setText(_translate("frmSuppliers", "SAVE"))
        self.lblSName.setText(_translate("frmSuppliers", "Supplier Name"))
        self.lblSAddress.setText(_translate("frmSuppliers", "Supplier Address"))
        self.txtAddress.setPlaceholderText(_translate("frmSuppliers", "Full Address of Supplier"))
        self.lblSTelephone.setText(_translate("frmSuppliers", "Supplier Telephone Number"))
        self.txtPhone.setPlaceholderText(_translate("frmSuppliers", "Telephone num"))
        self.txtFindName.setPlaceholderText(_translate("frmSuppliers", "Find by Name"))
        self.btnFind.setText(_translate("frmSuppliers", "FIND"))
        self.btnEdit.setText(_translate("frmSuppliers", "EDIT"))
        self.btnDelete.setText(_translate("frmSuppliers", "DELETE"))
