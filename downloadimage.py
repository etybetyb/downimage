#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys,os,requests,urllib
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5 import QtCore
import downui
       
class DLThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super(DLThread, self).__init__(parent)

    def download_(self,save_path,webn,filename):
        data=[save_path,webn,filename]
        self.trigger.emit(data)

class Main(QMainWindow, downui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.click_button)
        self.pushButton_2.clicked.connect(self.click_button_download)

        self.DLthreads = DLThread(self)
        self.DLthreads.trigger.connect(self.downdate)
    
    def click_button(self):
        self.zeron = self.filenum3.text()
        self.nup = self.filenum1.text()
        self.ndown = self.filenum2.text()
        self.webn = self.webname.text()
        self.fnameup = self.fileup.text()
        self.fnamedown = self.filedown.text()
        self.sfname = self.savefilename.text()
        if self.sfname == "":
            self.sfname='下載資料夾'
        self.k = self.create_f_name(self.nup,self.ndown,self.zeron)
        self.textnn="下載網址為:\n%s\n檔案從 %s%s%s 到 %s%s%s\n儲存到'%s'\n--------------------"         % (self.webn,self.fnameup,self.k[0],self.fnamedown,self.fnameup,self.k[-1],self.fnamedown,self.sfname)
        self.textview.setText(self.textnn)
        
    def click_button_download(self):
        dataname = []
        if not os.path.exists('./' + self.sfname):
            os.mkdir(self.sfname)
        for h in self.k:
            dataname.append(self.fnameup+str(h)+self.fnamedown)
        for j in dataname:
            self.textview.append('正在下載..%s'% j)
            QApplication.processEvents()
            try:
                if self.webn[-1]!="/":
                    self.webn = self.webn + "/"
                save_path = './%s/' % self.sfname +j
                self.DLthreads.download_(save_path,self.webn,j)
                

            except:
                self.textview.append('無法下載%s' % j)

        self.textview.append('--------------------\n已下載完成')
    
    def downdate(self,data):
        with open(data[0],'wb') as f:
                    req = urllib.request.Request(url=data[1]+data[2], headers=headers)
                    pic = urllib.request.urlopen(req).read()
                    f.write(pic)
                    QApplication.processEvents()
                    
    def create_f_name(self,nup,ndown,in_n):
        k=[]
        try:
            n=int(in_n)
        except:
            n=0
        try:
            for i in range(int(nup),int(ndown)+1):
                p=n-len(str(i))
                if p >0:
                    k.append('0'*p+str(i))
                else:
                    k.append(str(i))
            return k
        except:
            k=[""]
            return k

if __name__ == "__main__":
    headers = {'user-agent': '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    app = QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())

