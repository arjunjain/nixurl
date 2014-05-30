'''
Created on Oct 9, 2011

@author: arjunjain
'''

import sys
from PyQt4.QtGui import QMainWindow,QMenu,QSystemTrayIcon,QIcon,QMessageBox,QDialog,QApplication
from PyQt4.QtCore import SIGNAL
from uipy.ui_mainwindow import Ui_MainWindow
from uipy.ui_about import Ui_NixURL_about
from exlib import tinyurl,google,bitly

class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)         
        self.setupUi(self)
        self.textshorturl.setEnabled(False)
        self.convertprogress.hide()        
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(QIcon("/usr/share/pixmaps/nixiconsvg.svg"))
        trayIconMenu = QMenu()
        self.appabout = trayIconMenu.addAction("About")
        self.appexit = trayIconMenu.addAction("Exit")
        self.trayIcon.setContextMenu(trayIconMenu)       
        self.connect(self.trayIcon,SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),self.iconActivated)
        self.connect(self.buttonurlconvert,SIGNAL('clicked()'),self.converturl)
        self.connect(self.appexit,SIGNAL('triggered()'),self.close)
        self.connect(self.appabout,SIGNAL('triggered()'),self.showabout)
        self.connect(self.actionAbout,SIGNAL('triggered()'),self.showabout)
        self.connect(self.buttonreset,SIGNAL('clicked()'),self.resetall)
        self.connect(self.actionNew,SIGNAL('triggered()'),self.resetall)
        
    
    def iconActivated(self,dovod):
        if dovod == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                 
    def resetall(self):
        self.texturl.setText("")
        self.textshorturl.setText("")
        self.textshorturl.setEnabled(False)
        self.buttonurlconvert.setEnabled(True)
        self.comboservice.setCurrentIndex(0)
        self.convertprogress.hide()
        
    def converturl(self):
        url=str(self.texturl.text())
        url=url.strip()
        if url=="":
            QMessageBox.warning(self,"Error","Please Enter the valid URL")
        else:
            self.convertprogress.show()
            self.convertprogress.setValue(10)
            self.textshorturl.setEnabled(True)
            self.convertprogress.setValue(30)
            self.currentservice=self.comboservice.currentText()
            self.convertprogress.setValue(50)
            self.buttonurlconvert.setEnabled(False)
            if self.currentservice == "TinyURL":
                try:
                    self.textshorturl.setText(str(tinyurl.create_one(url)))
                    self.convertprogress.setValue(100)
                    self.buttonurlconvert.setEnabled(True)
                except:
                    QMessageBox.warning(self,"Error","Host can not be resolved")
                            
            elif self.currentservice == "google":
                try:
                    self.textshorturl.setText(str(google.shorten(url)))
                    self.convertprogress.setValue(100)
                    self.buttonurlconvert.setEnabled(True)
                    self.textshorturl.copy()
                except:
                    QMessageBox.warning(self,"Error","Host can not be resolved")
                    
            elif self.currentservice == "bit.ly":
                try:
                    a=bitly.Api()
                    self.textshorturl.setText(str(a.shorten(url)))
                    self.convertprogress.setValue(100)
                    self.buttonurlconvert.setEnabled(True)
                except:
                    QMessageBox.warning(self,"Error","Host can not be resolved")
    
    def showEvent(self,event):
        self.show()
        self.trayIcon.hide()
        event.ignore()
     
    def closeEvent(self,event):
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.trayIcon.hide()
            event.accept()
        else:
            self.hide()
            self.trayIcon.show()
            event.ignore()  

    def showabout(self):
        ab=About()
        ab.exec_()
        
              
class About(QDialog,Ui_NixURL_about):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
    def closeEvent(self,event):
        self.hide()
        event.ignore()
        
def run():  
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show() 
    sys.exit(app.exec_())    

if __name__=="__main__":
    run()
