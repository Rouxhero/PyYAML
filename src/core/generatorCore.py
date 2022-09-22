# Main Class


import os
from core.state import State, TABYAML, Transition
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading

class Core:
    def __init__(self, window):
        self.path = ""
        self.window = window
        self.setting = {
            "name": "",
            "description": "",
            "preamble": "",
            "nameRoot": "",
            "initialState": "",
        }
        self.transitions = []
        self.state = []

    def addState(self, state):
        self.state.append(state)

    def setSetting(self, key, setting):
        if key in self.setting:
            self.setting[key] = setting

    def setPath(self, path):
        self.path = path

    def updateChart(self):
        self.setting["name"] = self.window.nameInput.text()
        self.setting["description"] = self.window.descriptionInput.text()
        self.setting["preamble"] = self.window.preambleInput.toPlainText()
        self.setting["nameRoot"] = self.window.RootNameInput.text()
        self.setting["initialState"] = self.window.InitialState.currentText()
        text = (
            """statechart:
"""
            + TABYAML
            + """name: """
            + self.setting["name"]
            + """
"""
            + TABYAML
            + """description: """
            + self.setting["description"]
            + """
"""
            + TABYAML
            + """preamble: |
"""
            + TABYAML
            + TABYAML
            + """"""
            + self.setting["preamble"]
            + """
"""
            + TABYAML
            + """root state:
"""
            + TABYAML
            + TABYAML
            + """name: """
            + self.setting["nameRoot"]
            + """
"""
            + TABYAML
            + TABYAML
            + """initial: """
            + self.setting["initialState"]
            + """
"""
            + TABYAML
            + TABYAML
            + """states:
"""
            + self._renderState()
            + """
"""
        )
        self.window.codeContent.setText(text)
        self.updateChartPreview()

    def addTransition(self):
        self.transitions.append(
            Transition(
                self.window.targetInput.currentText(),
                self.window.eventInput.currentText(),
            )
        )
        item = QListWidgetItem(
            self.window.targetInput.currentText()
            + "("
            + self.window.eventInput.currentText()
            + ")"
        )
        self.window.TransitionListContent.addItem(item)

    def addTransitionEdit(self):
        self.editTransition.append(
            Transition(
                self.window.targetInput_2.currentText(),
                self.window.eventInput_2.currentText(),
            )
        )
        self.window.transitionSelect.addItem(
            self.window.targetInput_2.currentText()
            + "("
            + self.window.eventInput_2.currentText()
            + ")"
        )

    def deleteState(self):
        name = self.window.SelectStateEditInput.currentText()
        for state in self.state:
            if state.name == name:
                index = self.state.index(state)
                self.state.pop(index)
                break
        self._updateComboBox()
        self.updateChart()

    def updateChartPreview(self):
        myCode = self.window.codeContent.toPlainText()
        with open("../libs/temp.yaml","w+") as f:
            f.write(myCode)
        self.window.imgReceiver.clear()
        # threading.Thread(target=self.runPreview,args=()).start()
        self.runPreview()
    def runPreview(self):
        if os.name == "posix":
            os.system("cd ../libs/&&run.sh")
        else :
            os.system("cd ../libs/&&run.bat")
        self.refreshPreview()

    def refreshPreview(self):
        try :
            print(open("../libs/temp.png","rb").read())
            pixmap = QPixmap('../libs/temp.png')
            self.window.imgReceiver.setPixmap(pixmap)
            self.window.imgReceiver.resize(pixmap.width(),pixmap.height())
        except Exception as e :
            print(e)
            text = """
<html><head/><body><p align="center"><span style=" font-size:24pt; font-weight:600; color:#c10000;">Error generating image</span></p><p align="center"><span style=" font-size:24pt; font-style:italic; color:#132624;">Please check code</span></p></body></html>"""
            self.window.imgReceiver.setText(text)
            self.window.imgReceiver.resize(self.window.widget.width(),self.window.widget.height())
        
    def addNewTrans(self):
        self.window.eventInput_2.clear()
        self.window.eventInput_2.addItems(["press", "release", "short", "long"])
        self.window.targetInput_2.clear()
        for state in self.state:
            self.window.targetInput_2.addItem(state.name)
        try:
            self.window.saveTrans.clicked.disconnect(self.SaveTransitionEdit)
        except TypeError:
            pass
        self.window.saveTrans.clicked.connect(self.addTransitionEdit)

    def editTrans(self):
        self.window.eventInput_2.clear()
        self.window.eventInput_2.addItems(["press", "release", "short", "long"])
        self.window.targetInput_2.clear()
        for state in self.state:
            self.window.targetInput_2.addItem(state.name)
        try:
            self.window.saveTrans.clicked.disconnect(self.SaveTransitionEdit)
        except TypeError:
            pass
        self.window.saveTrans.clicked.connect(self.addTransitionEdit)

    def SaveTransitionEdit(self):
        MyTrans = None
        for trans in self.editTransition:
            if (
                trans.target + "(" + trans.event + ")"
                == self.window.transitionSelect.currentText()
            ):
                MyTrans = trans
                break
        MyTrans.target = self.window.targetInput_2.currentText()
        MyTrans.event = self.window.eventInput_2.currentText()

    def saveeditState(self):
        name = self.window.SelectStateEditInput.currentText()
        MyState = None
        for state in self.state:
            if state.name == name:
                MyState = state
                break
        MyState.name = self.window.NameStateInput_2.text()
        MyState.entry = self.window.EntryInput_2.toPlainText()
        MyState.transition = self.editTransition
        self._updateComboBox()
        self.updateChart()

    def editState(self):
        name = self.window.SelectStateEditInput.currentText()
        MyState = None
        for state in self.state:
            if state.name == name:
                MyState = state
                break
        self.editTransition = MyState.transitions
        self.window.NameStateInput_2.setText(MyState.name)
        self.window.EntryInput_2.setText(MyState.entry)
        self.window.transitionSelect.clear()
        for trans in MyState.transitions:
            self.window.transitionSelect.addItem(trans.target)

    def addState(self):
        self.state.append(
            State(
                self.window.NameStateInput.text(),
                self.window.EntryInput.toPlainText(),
                self.transitions,
            )
        )
        self.window.TransitionListContent.clear()
        self.transitions = []
        self._updateComboBox()
        self.updateChart()

    def _updateComboBox(self):
        self.window.InitialState.clear()
        self.window.targetInput.clear()
        self.window.SelectStateEditInput.clear()
        for state in self.state:
            self.window.InitialState.addItem(state.name)
            self.window.targetInput.addItem(state.name)
            self.window.SelectStateEditInput.addItem(state.name)

    def _renderState(self):
        text = ""
        for state in self.state:
            text += state.render()
        return text

    def exportYAML(self):
        file2 = QFileDialog.getSaveFileName(
            self.window, "Save File", ".", "YAML File (*.yaml);;All File (*.*)"
        )
        f = QFile(file2[0])
        f.open(QIODevice.WriteOnly | QFile.Text)
        QTextStream(f) << self.window.codeContent.toPlainText()
        f.close()
