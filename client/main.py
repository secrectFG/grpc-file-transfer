# import argparse
# import logging
from posixpath import join
import sys,os
from PyQt5.QtCore import Qt,pyqtSlot

from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QMainWindow, QApplication, QMessageBox,
 QProgressBar, QStyleFactory, QTextEdit, QVBoxLayout, QWidget,QPushButton,QLineEdit)

from client import FileClient
from myhelpers import foreachFile
from myhelpers import readFileAllText
from myhelpers import saveFileAllText
from threadutil import run_in_main_thread
from threading import Thread
import subprocess
import json
import math

Infrozen = False
if getattr(sys, 'frozen', False):
    Infrozen = True
    application_path = os.path.dirname(sys.executable)+'\\'
elif __file__:
    application_path = os.path.dirname(__file__)+'\\'

application_path_parent =  os.path.abspath(application_path+'..')+'\\'

try:
  config = json.loads(readFileAllText(application_path+'config.json'))
  
except:
  config={'ip':'','port':''}

PROGRESS_MAX = 10000

class MyQTextEdit(QTextEdit):
  def __init__(self, main):
      super().__init__()
      self.main=main

  def dragEnterEvent(self, event):
      if event.mimeData().hasUrls():
          event.accept()
      else:
          event.ignore()
  def dropEvent(self, event):
    self.main.dropEvent(event)

class MainWidget(QMainWindow):
    def __init__(self):
      super().__init__()
      self.setWindowTitle("服务器辅助工具")
      self.resize(720, 480)
      self.setAcceptDrops(True)
      self.ip_address = config['ip']
      self.port = config['port']
      

      self.client = None

      
      
      wid = QWidget(self)
      self.setCentralWidget(wid)
      # layout = QtGui.QVBoxLayout()
      # wid.setLayout(layout)
      self.textEdit = MyQTextEdit(self)
      self.textEdit.append("文件夹拖进来")
      # self.label = QLabel("文件夹拖进来")
      # self.label.setAlignment(Qt.AlignCenter)

      mainLayout = QVBoxLayout()
      self.progressBar = QProgressBar()
      self.progressBar.setRange(0, PROGRESS_MAX)
      # self.progressBar.setValue(1234)
      # self.progressBar.setFormat('123456')
      # self.progressBar.setFixedWidth(1000)
      # self.startServerButton = QPushButton('开启特定服务器')
      # self.startServerButton.clicked.connect(self.on_startServerButton_clicked)
      # mainLayout.addWidget(self.startServerButton)
      mainLayout.addWidget(self.textEdit)

      def savejson():
        s =json.dumps(config)
        saveFileAllText(application_path+'config.json',s)

      sublayout1 = QHBoxLayout()
      lineEditIP = QLineEdit()
      lineEditIP.setText(self.ip_address)
      def ontextChanged(text):
        self.ip_address = text
        config['ip'] = text
        savejson()
        print(text)

      lineEditIP.textChanged.connect(ontextChanged)
      lineEditPort = QLineEdit()
      lineEditPort.setText(str(self.port))
      def onport(text):
        self.port = int(text)
        config['port'] = self.port
        print(self.port)
        savejson()

      lineEditPort.textChanged.connect(onport)
      sublayout1.addWidget(lineEditIP)
      sublayout1.addWidget(lineEditPort)
      mainLayout.addLayout(sublayout1)
      mainLayout.addWidget(self.progressBar)

      self.progressBar.hide()
      
      # self.setLayout(mainLayout)
      wid.setLayout(mainLayout)
      # self.changeStyle('Fusion')

      self.setText = run_in_main_thread(self.setLabelText)
      self.text = ''
      self.setProgressFunc = run_in_main_thread(self.setProgress)
      self.thread=None
      self.fileList = []

      

    # @pyqtSlot()
    def on_startServerButton_clicked(self):
        # self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox2.value()))
        # print(value)
        print('11')

    def setProgress(self,total,cur):
      value = float(cur)/float(total)
      self.progressBar.setFormat(f'{math.floor(cur/1024)}/{math.floor(total/1024)}KB')
      self.progressBar.setValue(int(value*PROGRESS_MAX))
      if cur!=total:
        self.progressBar.show()
      else:
        self.progressBar.hide()

    def setLabelText(self,text:str):
      self.text += text
      # self.label.setText(self.text)
      self.textEdit.append(text)
      print(text)
        
    def changeStyle(self, styleName):
      QApplication.setStyle(QStyleFactory.create(styleName))

    
        
    def dragEnterEvent(self, event):
      if event.mimeData().hasUrls():
          event.accept()
      else:
          event.ignore()

    def dropEvent(self, event):
      
      files = [u.toLocalFile() for u in event.mimeData().urls()]
      for f in files:
          self.fileList.append(f)
          self.setText(f'添加到队列:{f}')
      if self.thread and self.thread.is_alive():
        return
      try:
        if self.client:
          self.client.close()
        self.client = FileClient(
          ip_address= config['ip'],
          port = config['port'],
          )
        self.setText(f'ip_address:{self.ip_address} port:{self.port}')
      except Exception as e:
        QMessageBox.critical(self,'',f'创建连接失败 {e}')
      self.thread = Thread(target=self.packThread,daemon=True)
      self.thread.start()

    def packThread(self):

      findOne = False
      # for f in files:
      while len(self.fileList)>0:
        f = self.fileList.pop(0)
        if os.path.isfile(f):
          fn = os.path.split(f)[1]
          self.client.uploadSetName(fn,f)
          rsp = self.client.upload(f,self.setProgressFunc)
          self.setText(f'结果 {rsp.result}')
          # continue
        
        # if os.path.isdir(f):
        #   def handler(dirpath,filepath,file_name):
        #     if file_name in ('打包.bat','打包exe.bat','打包独立exe.bat'):
        #       return dirpath
        #   dirpath = foreachFile(f,handler,['.bat'])
        #   if dirpath:
        #     print('找到',dirpath)
        #     findOne=True
        #     # self.setText(f'正在打包{dirpath}')
        #     # pro = subprocess.check_output(f'dotnet-warp.exe', cwd=dirpath)
        #     # print(pro.decode())
        #     # self.setText(pro.decode())

        #     gameName = os.path.split(dirpath)[1]+'.exe'
        #     fullpath = dirpath+'/'+gameName
        #     if os.path.isfile(fullpath):
        #       try:
        #         self.setText(f'正在上传到{self.ip_address} {self.port},路径:{fullpath}')
        #         self.client.uploadSetName(gameName,fullpath)
        #         rsp = self.client.upload(fullpath,self.setProgressFunc)
        #         self.setText(f'结果 {rsp.result}')
        #       except Exception as e:
        #         self.setText(f'发生了错误 {e}')
        #       self.setProgressFunc(1,1)
        #     else:
        #       self.setText(f'打包出错:\n{pro.decode()}\n5秒后继续运行')
            


        #   else:
        #     self.setText('没有找到文件“打包exe.bat”')
      if findOne==False:
        self.setText('没有找到文件“打包exe.bat”')
      else:
        self.setText('结束')
    # def handleFile(self,dirpath,filepath,file_name):

    #     pass
          # print(f)

def main():
  
  app = QApplication(sys.argv)
  
  ui = MainWidget()
  ui.show()
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
