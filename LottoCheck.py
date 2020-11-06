#!/usr/bin/python3
#-*- coding:utf-8 -*-
#from __future__ import print_function
import os
import random
from bs4 import BeautifulSoup as bsoup
import requests
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtWidgets import (QMainWindow , QWidget, QApplication, QTableView, QPushButton, QVBoxLayout, QHBoxLayout, 
                            QLabel, QAbstractScrollArea, QInputDialog, QAction, QMessageBox, 
                            QPlainTextEdit, QFileDialog)
from PyQt5.QtCore import Qt, QSettings, QItemSelectionModel

class Editor(QMainWindow):
    def __init__(self):
        super(Editor, self).__init__()
        self.setWindowFlags(Qt.Popup)
        self.isModified = False
        dir = os.path.dirname(sys.argv[0])
        self.tliste = []
        self.zahlen = "%s/%s" % (dir,"zahlen.txt")
        self.tipp_editor = QPlainTextEdit(self)
        self.tipp_editor.textChanged.connect(self.setModified)
        self.close_btn = QPushButton("Close", self)
        self.close_btn.setFixedWidth(100)
        self.close_btn.setIcon(QIcon.fromTheme("window-close"))
        self.close_btn.clicked.connect(self.closeWin)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tipp_editor)
        self.layout.addWidget(self.close_btn)
        self.wid = QWidget()
        self.wid.setLayout(self.layout)
        self.setCentralWidget(self.wid)
        self.setGeometry(50, 50, 400, 400)
        self.show()

    def closeWin(self):
        if self.isModified == True:
            with open(self.zahlen, 'w') as f:
                f.write(self.tipp_editor.toPlainText())
                f.close()
                os.execv(sys.argv[0], sys.argv)
        else:
            print("closing editor")
        self.close()

    def closeEvent(self, event):
        print("close event")

    def setModified(self):
        self.isModified = True

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.lz = []
        self.ts = 0
        self.zahlenListe = []
        dir = os.path.dirname(sys.argv[0])
        self.settingsfile = "%s/%s" % (dir,"Lotto.conf")
        self.zahlen = "%s/%s" % (dir,"zahlen.txt")
        print(self.settingsfile)
        self. settings = QSettings(self.settingsfile,QSettings.IniFormat)
        self.setStyleSheet(stylesheet(self))
        self.lottolink = 'https://www.dielottozahlende.net/lotto-6-aus-49'
        self.mysuper = 5
        self.model =  QStandardItemModel(self)
        self.model.setRowCount(7)
        self.tableview = QTableView(self)
        self.tableview.setSortingEnabled(False)
        self.tableview.setGridStyle(1)
        if int(sys.version[0]) > 2:
            self.tableview.setFixedHeight(149)
        else:
            self.tableview.setFixedHeight(171)
        self.tableview.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableview.horizontalHeader().setStretchLastSection(True)
        self.tableview.verticalHeader().setStretchLastSection(False)
        self.tableview.setCornerButtonEnabled(True)
        self.tableview.setShowGrid(True)
        self.tableview.setModel(self.model)
        self.tableview.hideRow(6)
        self.tableview.hideColumn(13)
        self.pushButtonLoad = QPushButton()
        self.pushButtonLoad.setText("Zahlen holen")
        self.pushButtonLoad.setIcon(QIcon.fromTheme("view-refresh"))
        self.pushButtonLoad.clicked.connect(self.getLotto)
        self.pushButtonLoad.setFixedWidth(110)
        self.pushButtonLoad.setFixedHeight(24)

        self.btnGenerator = QPushButton()
        self.btnGenerator.setText("Zufallszahlen")
        self.btnGenerator.clicked.connect(self.generateNumbers)
        self.btnGenerator.setFixedWidth(110)
        self.btnGenerator.setFixedHeight(24)

        self.btnSave = QPushButton()
        self.btnSave.setText("Speichern")
        self.btnSave.clicked.connect(self.saveNumbers)
        self.btnSave.setFixedWidth(110)
        self.btnSave.setFixedHeight(24)

        self.zahlenAction = QAction(QIcon.fromTheme("edit"), "Editor", self, 
                                    triggered = self.edit_Tipps, shortcut = "F5")
        self.addAction(self.zahlenAction)

        self.superAction = QAction(QIcon.fromTheme("edit"), "Superzahl", self, 
                                    triggered = self.setMySuper, shortcut = "F6")
        self.addAction(self.superAction)

        self.infoAction = QAction(QIcon.fromTheme("help-info"), "Information", self, 
                                    triggered = self.showInfo, shortcut = "F1")
        self.addAction(self.infoAction)

        self.generatorAction = QAction(QIcon.fromTheme("help-info"), "Generator", self, 
                                        triggered = self.generateNumbers, shortcut = "F7")
        self.addAction(self.generatorAction)

        self.lbl = QLabel()

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.pushButtonLoad)
        self.hbox.addWidget(self.btnGenerator)
        self.hbox.addWidget(self.btnSave)

        grid = QVBoxLayout()
        grid.setSpacing(10)
        grid.addLayout(self.hbox)
        grid.addWidget(self.tableview)
        grid.addWidget(self.lbl)

        mywidget = QWidget()
        mywidget.setLayout(grid)
        self.setCentralWidget(mywidget)

        self.readSettings()
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()
        self.setHeaders()

        print("Wilkommen bei Lotto")
        self.statusBar().showMessage("%s %s" % ("Willkommen bei LottoCheck"
                                    , " *** F5 Lottozahlen ändern *** F6 Superzahl ändern"), 0)
                                    
    def findTableItems(self):
        model = self.tableview.model()
        print(self.zahlenListe)
        for column in range(11):
            start = model.index(0, column)
            for zahl in self.zahlenListe:      

                matches = model.match(
                    start, Qt.DisplayRole,
                    str(zahl), 1, Qt.MatchExactly)
                if matches:
                    index = matches[0]
                    # index.row(), index.column()
                    self.tableview.selectionModel().select(
                        index, QItemSelectionModel.Select)

    def saveNumbers(self):
        print(self.model.columnCount(), "Columns")
        textData = ""
        fileName, _ = QFileDialog.getSaveFileName(self, "Open File", "~/lottozahlen.csv","CSV Files (*.csv)")
        if fileName:
            print("%s %s" % (fileName, "saved"))
            f = open(fileName, 'w')
            for col in range(self.model.columnCount()):
                textData += str(self.model.horizontalHeaderItem(col).text())
                textData += "\t" 
            textData += "\n"
            for row in range(self.model.rowCount()-1):
                for col in range(self.model.columnCount()):
                    textData += str(self.model.data(self.model.index(row,col)))
                    textData += "\t" 
                textData += "\n"
            f.write(textData)
            f.close()

    def generateNumbers(self):
        tippliste = []
        self.tliste = []
        for x in range(self.model.columnCount() - 1):
            t = sorted(random.sample(range(1, 50), 6))
            tippliste.append(str(t).strip('[]'))
        for tips in tippliste:
            self.tliste.append(tips.split(","))
        for i in range(self.model.columnCount() - 1):
            tipp = tippliste[i].split(",")
            for row in range(len(tipp)):
                self.model.setData(self.model.index(row, i), tipp[row])
                self.model.item(row, i).setTextAlignment(Qt.AlignCenter)
        self.getLotto()

    def edit_Tipps(self):
        self.edWin = Editor()
        with open(self.zahlen, 'r') as f:
            text = f.read()
            self.edWin.tipp_editor.setPlainText(text)
            f.close()
        self.edWin.isModified = False

    def showInfo(self):
        link = "<p><a title='Axel Schneider' href='http://goodoldsongs.jimdo.com' target='_blank'> \
                Axel Schneider</a></p>"
        message = "<h2>LottoCheck 1.0</h2><h4>6 aus 49</h4>created by " + link + " with PyQt5<br>©September 2019<br>" \
                            + "<br>Copyright © 2017 The Qt Company Ltd and other contributors." \
                            + "<br>Qt and the Qt logo are trademarks of The Qt Company Ltd."  \
                            + "<br><br>F5 = Tipps ändern" \
                            + "<br>F6 = Superzahl ändern"
        self.msgbox(message)

    def msgbox(self, message):
        msg = QMessageBox(1, "Information", message, QMessageBox.Ok)
        msg.exec_()

    def getLotto(self):
        if not self.lz == []:
            print("values already here", self.lz)
            self.compare()
        else:
            print("getting Values")
            source = requests.get(self.lottolink).text
            soup = bsoup(source, 'lxml')
            result = (soup.find('div', class_='row sixaus49-numbers').text
                        .partition("\n")[2].partition("Ziehungsreihenfolge")[0])
            lotto = result.split()
    
            print("Gewinnzahlen:")
            result =lotto[:6]
            self.lz = result
            result = list(map(int, result))
            result.sort()
            self.zahlenListe = result
            theSuper = lotto[6]
            self.ts = theSuper
            print("theSuper", self.ts)
            for i in range(6):
                self.model.setData(self.model.index(i, 12), result[i])
                self.model.item(i, 12).setTextAlignment(Qt.AlignCenter)
            self.compare()


    def getSpiel77(self):
        source = requests.get(self.lottolink).text
        soup = bsoup(source, 'lxml')
        result = soup.find('div', class_="col-12 h6").text #.partition("    <strong>")[0]
        
#        print("Spiel77:")
        self.lbl.setText(self.lbl.text() + result.replace(" ", ""))

    def compare(self):
        ### compare all tipps
        self.lz = [ int(x) for x in self.lz]
        print(self.mysuper, self.lz)
        self.lbl.clear()
        tipp = []
        for x in range(len(self.tliste)):
            t = []
            tipp = [ int(x) for x in self.tliste[x]]
#            print(tipp)
            for a in self.lz:
                if int(a) in tipp:
                    print(a, "in tipp", str(x+1))
                    t.append(a)

            rtext = ""
            print("len(t) ", len(t) )
            if len(t) == 2 and self.mysuper == self.ts:
                rtext += self.lbl.text()
                rtext += '\ngewonnen in Tipp '
                rtext += str(int(x)+1)
                rtext += " : "
                rtext += str(t)
                rtext += " *** "
                rtext += str(len(t))
                rtext += "er ***"
                rtext += ' + Superzahl'
                self.lbl.setText(rtext) 
            elif len(t) > 2:
                if self.mysuper == self.ts:
                    rtext += self.lbl.text()
                    rtext += '\ngewonnen in Tipp '
                    rtext += str(int(x)+1)
                    rtext += " : "
                    rtext += str(t)
                    rtext += " *** "
                    rtext += str(len(t))
                    rtext += "er ***"
                    rtext += ' + Superzahl'
                    self.lbl.setText(rtext) 
                else:
                    rtext += self.lbl.text()
                    rtext += '\ngewonnen in Tipp '
                    rtext +=str(int(x)+1)
                    rtext += " : "
                    rtext += str(t)
                    rtext += " *** "
                    rtext += str(len(t))
                    rtext += "er ***"
                    self.lbl.setText(rtext)      

        if self.lbl.text() == "":
            self.lbl.setText("leider nichts gewonnen ...")
        self.statusBar().showMessage("%s %s %s %s" % ("Gewinnzahlen: "
                                    , (', '.join(str(x) for x in self.lz)), " *** Superzahl: ", str(self.ts)), 0)
        self.getSpiel77()
        self.findTableItems()

    def setHeaders(self):
        self.tableview.horizontalHeader().setVisible(True)
        self.tableview.verticalHeader().setVisible(False)
        for x in range(self.model.columnCount() - 1):
            self.model.setHeaderData(x, Qt.Horizontal, "%s %s" % ("Tipp", (x+1)))
        self.model.setHeaderData(self.model.columnCount() - 1, Qt.Horizontal, "Gewinnzahlen")
        self.tableview.setAlternatingRowColors(True)
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()


    def closeEvent(self, event):
        print("Goodbye ...")
        self.writeSettings()

    def setMySuper(self):
        s = int(self.mysuper)
        dlg = QInputDialog()
        ms, ok = dlg.getInt(self, 'Superzahl:', "",  s, 0, 9, 1, Qt.Dialog)
        if ok:
            self.mysuper = ms
            print("Superzahl =", self.mysuper)

    def readSettings(self):
        if self.settings.contains("mysuper"):  
            self.mysuper = self.settings.value("mysuper") 
        else:
            self.setMySuper()
        print("Superzahl:", self.mysuper)
        self.tliste = []
        with open(self.zahlen, 'r') as f:
            text = f.read()
            f.close()
            for line in text.splitlines():
                self.tliste.append(line.split(","))
            self.model.setColumnCount( len(self.tliste) + 1)
            for x in range(0, len(self.tliste)):
                tipp = self.tliste[x]
                for i in range(len(tipp)):
                    self.model.setData(self.model.index(i, x), tipp[i])
                    self.model.item(i, x).setTextAlignment(Qt.AlignCenter)

    def writeSettings(self):
        self.settings.setValue("mysuper", self.mysuper)  

def stylesheet(self):
        return """
    QTableView
     {
        font-family: Helvetica;
        border: 1px outset #d3d7cf;
        background: transparent;
        selection-color: #ffffff;
        gridline-color: #888a85;
        }
        
    QTableView::item:selected {
        color: #F4F4F4;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                            stop:0 #6169e1, stop:1 #3465a4);
        border: 0px;
        } 
    QPushButton
        {
        background: #d3d7cf;
        } 
    QMainWindow
        {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    }
    QHeaderView::section
    {
         background: qlineargradient( y1: 0,  y2: 1,
                                 stop: 0 #1f3c5d, stop: 1.0 #204a87);
        color: #f3f3f3;
        padding-left: 2px;
        border: 0px;
        font-weight: bold;
        gridline-color: #eeeeec;
    }
    QLabel
    {
        font-family: Helvetica;
        font-size: 9pt;
    }
    QStatusBar
    {
        font-family: Helvetica;
        font-size: 8pt;
    }
    """


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    main = MyWindow()
    main.setMinimumSize(649, 460)
    main.setGeometry(0,0,649,460)
    main.setWindowTitle("Lottozahlen 6 aus 49")
    main.setWindowIcon(QIcon.fromTheme("browser"))
    main.show()

sys.exit(app.exec_())
