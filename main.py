import selenium
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import os

#make non-clickable items clickable
def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class popUpMainFunction(QWidget):
    def __init__(self):
        super(popUpMainFunction, self).__init__()
        self.popUpMainFunctionUi()

    # MAIN FUNCTION
    def import_events(self):

        names_text = []
        class_name = []
        task_day = []
        task_month = []
        names_text_del = []
        class_name_del = []
        task_day_del = []
        task_month_del = []

        global subjects
        global browser
        browser.get("https://uwcim.managebac.com/student/calendar")
        sleep(1)
        year = browser.find_element_by_xpath("/html/body/main/div[2]/div/div[2]/div[1]/div[1]/h2").text[-4:]
        firstStageLabel = QLabel("Going through individual events...\n\n")
        self.popUpMainFunctionLayout.addWidget(firstStageLabel)
        qApp.processEvents()
        names = browser.find_elements_by_class_name("fc-title")
        event_number = len(names)
        eventsLabelText = ""
        eventsLabelCounterText = ""
        eventsLabelHorizontal = QHBoxLayout()
        eventsLabel = QLabel(eventsLabelText)
        eventsLabelCounter = QLabel(eventsLabelCounterText)
        eventsLabelCounter.setFont(QFont("Arial",weight=QFont.Bold))
        self.popUpMainFunctionLayout.addLayout(eventsLabelHorizontal)
        eventsLabelHorizontal.addWidget(eventsLabel)
        eventsLabelHorizontal.addStretch()
        eventsLabelHorizontal.addWidget(eventsLabelCounter)
        for i in range(0,event_number):
                names = browser.find_elements_by_class_name("fc-title")
                name_temp = names[i].text
                names_text.append(names[i].text)
                names[i].click()
                sleep(1)

                class_name.append(str(browser.find_element_by_tag_name("h3").text))
                task_day.append(str(browser.find_element_by_class_name("day").text))
                task_month.append(str(browser.find_element_by_class_name("month").text))

                # Convert subject name to shorter name
                if (class_name[i] == subjects[0]):
                    class_name[i] = subjects[0].split()[2]
                elif (class_name[i] == subjects[1]):
                    class_name[i] = subjects[1].split()[2]
                elif (class_name[i] == subjects[2]):
                    class_name[i] = subjects[2].split()[2]
                elif (class_name[i] == subjects[3]):
                    class_name[i] = subjects[3].split()[2]
                elif (class_name[i] == subjects[4]):
                    class_name[i] = subjects[4].split()[2]
                elif (class_name[i] == subjects[5]):
                    class_name[i] = subjects[5].split()[2]
                eventsLabelText = "Found Task: {} [{}]".format(name_temp, class_name[i])
                eventsLabelCounterText = "[{}/{}]".format(i+1, event_number)
                eventsLabel.setText(eventsLabelText)
                eventsLabelCounter.setText(eventsLabelCounterText)
                eventsLabel.adjustSize()
                self.adjustSize()
                perc_complete = 100/(event_number) * (i+1)
                self.eventProgressBar.setValue(perc_complete/2)
                qApp.processEvents()

                browser.get("https://uwcim.managebac.com/student/calendar")
                sleep(1)

        event_number = len(names_text)
        eventsLabel.hide()
        eventsLabelCounter.hide()
        eventsLabelCounter.setText("")
        eventsLabel.setText("")
        firstStageLabel.hide()
        # CHECK IF ANY TASK IS ALREADY CREATED
        secondStageLabel = QLabel("Removing duplicate tasks...\n\n")
        self.popUpMainFunctionLayout.addWidget(secondStageLabel)
        eventsRemovingText = ""
        eventsRemovingLabel = QLabel(eventsRemovingText)
        self.popUpMainFunctionLayout.addWidget(eventsRemovingLabel)
        if os.path.isfile('created_tasks.txt'):
            f = open("created_tasks.txt")
            for i in range(0, event_number):
                checkFileString = names_text[i]
                if (checkFileString in f.read()):
                    eventsRemovingText += ("Removing task: \n", names_text[i])
                    eventsRemovingLabel.setText(eventsRemovingText)
                    qApp.processEvents()
                    sleep(0.75)
                    names_text_del.append(names_text[i])
                    class_name_del.append(class_name[i])
                    task_day_del.append(task_day[i])
                    task_month_del.append(task_month[i])
                else:
                    names_text_del.append("0")
                    class_name_del.append("0")
                    task_day_del.append("0")
                    task_month_del.append("0")
            f.close()
            for i in range(0, event_number):
                if not names_text_del[i] == "0":
                    del names_text[i]
                    del task_day[i]
                    del task_month[i]
                    del class_name[i]
            event_number = len(names_text)
            if event_number == 0:
                popUpMainFunctionLayout.addWidget(QLabel("No new tasks need to be added. Returning to main menu in 3 seconds..."))
                sleep(3)
                global windowMain
                windowMain = mainWindow()
                self.close()
        else:
            pass
        sleep(2)
        secondStageLabel.hide()

        # MYSTUDYLIFE
        self.loadingLabel1.setText("Importing events into MyStudyLife")
        qApp.processEvents()
        global msl_email
        global msl_pw

        browser.get("https://app.mystudylife.com/?utm_source=mystudylife&utm_medium=sign-in&utm_campaign=mystudylife.com")
        browser.find_element_by_link_text('Sign in with email').click()
        browser.find_element_by_name("email").send_keys(msl_email)
        browser.find_element_by_name("password").send_keys(msl_pw)
        browser.find_element_by_name("password").submit()
        sleep(3)
        eventsLabel.show()
        eventsLabelCounter.show()
        qApp.processEvents()
        for i in range(0, event_number):
            browser.find_element_by_xpath("/html/body/ui-view/div/div[1]/div/div/div/header/div[2]/div[1]/a").click()
            sleep(1.5)
            for option in browser.find_element_by_name("subject").find_elements_by_tag_name('option'):
                if option.text == class_name[i]:
                    option.click()
                    break
            browser.find_element_by_xpath("/html/body/div[5]/div/form/msl-antiscroll/div[1]/div/div[3]/div[1]/div/input").send_keys(Keys.COMMAND, "a")
            browser.find_element_by_xpath("/html/body/div[5]/div/form/msl-antiscroll/div[1]/div/div[3]/div[1]/div/input").send_keys(task_month[i], " ", task_day[i], " ", year)
            browser.find_element_by_xpath("/html/body/div[5]/div/form/msl-antiscroll/div[1]/div/div[3]/div[1]/div/input").send_keys(Keys.RETURN)
            browser.find_element_by_xpath("/html/body/div[5]/div/form/msl-antiscroll/div[1]/div/div[4]/input").send_keys(names_text[i])
            browser.find_element_by_xpath("/html/body/div[5]/div/form/div/button[1]/span").click()
            perc_complete = 100/(event_number) * (i+1)
            self.eventProgressBar.setValue(perc_complete/2 + 50)
            eventsLabelText = "Imported Task: {} [{}]".format(names_text[i], class_name[i])
            eventsLabelCounterText = "[{}/{}]".format(i+1, event_number)
            eventsLabel.setText(eventsLabelText)
            eventsLabelCounter.setText(eventsLabelCounterText)
            eventsLabel.adjustSize()
            qApp.processEvents()
            sleep(1)

        #write tasks into file
        if os.path.isfile('created_tasks.txt'):
            f = open("created_tasks.txt","a")
            for i in range(0, event_number):
                f.write("\n{}".format(names_text[i]))
            f.close()
        else:
            f = open("created_tasks.txt","w")
            for i in range(0, event_number):
                f.write("\n{}".format(names_text[i]))
            f.close()


    def popUpMainFunctionUi(self):
            qApp.processEvents()
            self.popUpMainFunctionLayout = QVBoxLayout()
            self.setLayout(self.popUpMainFunctionLayout)
            self.loadingLabel1 = QLabel("Getting events from ManageBac...")
            self.popUpMainFunctionLayout.addWidget(self.loadingLabel1)
            loadingLabel2 = QLabel("Importing events into MyStudyLife...")
            self.popUpMainFunctionLayout.addWidget(loadingLabel2)
            loadingLabel2.hide()
            self.eventProgressBar = QProgressBar()
            self.popUpMainFunctionLayout.addWidget(self.eventProgressBar)
            self.show()
            qApp.processEvents()
            self.import_events()
            doneLabel = QLabel("Imported all events.\nYou can now exit the app.")
            doneLabel.setFont(QFont("Arial", 16, QFont.Bold))
            self.popUpMainFunctionLayout.addWidget(doneLabel)
            exitButton = QPushButton("Exit")
            exitButtonHorizontal = QHBoxLayout()
            self.popUpMainFunctionLayout.addLayout(exitButtonHorizontal)
            exitButtonHorizontal.addStretch()
            exitButtonHorizontal.addWidget(exitButton)
            exitButton.clicked.connect(lambda: exitApp())
class popUpSubjectSetup(QWidget):
    def __init__(self):
        super(popUpSubjectSetup, self).__init__()
        self.popUpSubjectSetupUi()

    def hide_popUpSubjects(self):
        global windowMain
        windowMain = mainWindow()
        self.close()

    def popUpSubjectSetupUi(self):
            qApp.processEvents()
            popUpSubjectSetupLayout = QVBoxLayout()
            self.setLayout(popUpSubjectSetupLayout)
            popUpSubjectSetupLayout.addWidget(QLabel("Loading subjects from ManageBac. Please wait..."))
            subjectProgressBar = QProgressBar()
            popUpSubjectSetupLayout.addWidget(subjectProgressBar)
            self.show()
            qApp.processEvents()
            global subjects
            subjects = []
            subjectSetupListLabelText = "Found subjects:\n"
            for i in range(1,7):
                browser.get(browser.find_element_by_xpath("/html/body/div[1]/ul/li[9]/ul/li[{}]/a".format(i)).get_attribute("href"))
                subjects.append(browser.find_element_by_xpath("/html/body/main/div[2]/div[2]/div[1]/h3").text)
                browser.get("https://uwcim.managebac.com/student")
                subjectSetupListLabelText += subjects[i-1] + "\n"
                perc_complete = 100/6 * i
                subjectProgressBar.setValue(perc_complete)
                qApp.processEvents()
            f = open("subjects.txt","w")
            f.write("{}".format(subjects[0]))
            for i in range(1,6):
                f.write("\n{}".format(subjects[i]))
            f.close()
            subjectSetupListLabel = QLabel("{}\n\nPress Ok to continue.".format(subjectSetupListLabelText))
            popUpSubjectSetupLayout.addWidget(subjectSetupListLabel)
            okButton = QPushButton("Ok")
            okButtonHorizontal = QHBoxLayout()
            popUpSubjectSetupLayout.addLayout(okButtonHorizontal)
            okButtonHorizontal.addStretch()
            okButtonHorizontal.addWidget(okButton)
            okButton.clicked.connect(lambda: self.hide_popUpSubjects())

class mainWindow(QWidget):
    def __init__(self):
        super(mainWindow, self).__init__()
        try:
            global loginWindow
            loginWindow.close()
        except:
            pass
        self.mainUi()

    def setupSubjects(self):
        if os.path.isfile('subjects.txt'):
            subjectsFile = open("subjects.txt","r")
            global subjects
            subjects = subjectsFile.readlines()
            subjects = [x.strip() for x in subjects]
            return True
        else:
            return False

    def popUpMainFunctionFunction(self):
        self.close()
        qApp.processEvents()
        global popUpMainFunction
        popUpMainFunction = popUpMainFunction()
        popUpMainFunction.show()

    def mainUi(self):
        qApp.processEvents()
        self.setWindowTitle("ManageBac Tools")
        mainLayoutV = QVBoxLayout()
        self.setLayout(mainLayoutV)
        self.show()
        if self.setupSubjects() == True:
            mainLayoutV.addWidget(QLabel("Found ManageBac subjects:"))
            subjectListLabelText = subjects[0]
            for i in range(1,len(subjects)):
                subjectListLabelText += "\n{}".format(subjects[i])
            subjectListLabel = QLabel(subjectListLabelText)
            mainLayoutV.addWidget(subjectListLabel)
            mainLayoutV.addWidget(QLabel("To start importing events into MyStudyLife, press 'Start'."))
            goButton = QPushButton("Start")
            mainLayoutV.addWidget(goButton)
            goButton.clicked.connect(lambda:self.popUpMainFunctionFunction())
        else:
            self.close()
            popUpSubjectSetup().show()

class loginWindow(QWidget):
    def __init__(self):
        super(loginWindow, self).__init__()
        self.loginUi()

    def login_mb(self, email_mb, password_mb):
        global msl_pw
        global msl_email
        if self.mslCheckBox.checkState()!=Qt.Checked:
            msl_email = self.loginEmailMsl.text()
            msl_pw = self.loginPasswordMsl.text()
        else:
            msl_email = email_mb
            msl_pw = password_mb

        browser.find_element_by_id("session_login").send_keys(email_mb)
        browser.find_element_by_id("session_password").send_keys(password_mb)
        browser.find_element_by_name("commit").click()
        if (browser.current_url == "https://uwcim.managebac.com/student") or (browser.current_url == "http://uwcim.managebac.com/student"):
            global windowMain
            # open main window
            windowMain = mainWindow()
        else:
            self.loggedIn = False

    def showMslLogin(self, state):
        if state != Qt.Checked:
            self.mslLoginWidget.show()
        else:
            self.mslLoginWidget.hide()
            self.adjustSize()

    def loginUi(self):
        loginLayoutV = QVBoxLayout()
        self.setLayout(loginLayoutV)
        # load browser
        loadingLabel = QLabel('Loading ManageBac...')
        loginLayoutV.addWidget(loadingLabel)
        self.show()
        qApp.processEvents()
        opts = Options()
        opts.add_argument('-headless')
        global browser
        browser = Firefox(options=opts)
        browser.get('https://uwcim.managebac.com/')
        loadingLabel.hide()
        # ------------------------------------------
        # login menu
        self.setWindowTitle('Log In')
        loginLayoutH1 = QHBoxLayout()
        titleLoginMb = QLabel('ManageBac Login')
        titleLoginMb.setFont(QFont("Arial", 16, QFont.Bold))

        loginLayoutH2 = QHBoxLayout()
        loginEmailMb = QLineEdit()
        loginEmailMb.setPlaceholderText("Email")
        loginEmailMb.setFixedWidth(150)

        loginLayoutH3 = QHBoxLayout()
        loginPasswordMb = QLineEdit()
        loginPasswordMb.setEchoMode(2)
        loginPasswordMb.setPlaceholderText("Password")
        loginPasswordMb.setFixedWidth(150)

        checkBoxH = QHBoxLayout()
        self.mslCheckBox = QCheckBox()
        checkBoxLabel = QLabel("Same details for MyStudyLife")

        self.mslLoginWidget = QWidget()
        mslLoginVLayout = QVBoxLayout()

        loginLayoutH1Msl = QHBoxLayout()
        self.titleLoginMsl = QLabel('MyStudyLife Login')
        self.titleLoginMsl.setFont(QFont("Arial", 16, QFont.Bold))

        loginLayoutH2msl = QHBoxLayout()
        self.loginEmailMsl = QLineEdit()
        self.loginEmailMsl.setPlaceholderText("Email")
        self.loginEmailMsl.setFixedWidth(150)

        loginLayoutH3msl = QHBoxLayout()
        self.loginPasswordMsl = QLineEdit()
        self.loginPasswordMsl.setEchoMode(2)
        self.loginPasswordMsl.setPlaceholderText("Password")
        self.loginPasswordMsl.setFixedWidth(150)

        loginLayoutH4 = QHBoxLayout()
        loginButtonMb = QPushButton('Log in')
        exitButtonMb = QPushButton('Exit')
        loginLayoutV.addStretch()
        loginLayoutV.addLayout(loginLayoutH1)
        loginLayoutH1.addStretch()
        loginLayoutH1.addWidget(titleLoginMb)
        loginLayoutH1.addStretch()

        loginLayoutV.addLayout(loginLayoutH2)
        loginLayoutH2.addStretch()
        loginLayoutH2.addWidget(loginEmailMb)
        loginLayoutH2.addStretch()

        loginLayoutV.addLayout(loginLayoutH3)
        loginLayoutH3.addStretch()
        loginLayoutH3.addWidget(loginPasswordMb)
        loginLayoutH3.addStretch()

        loginLayoutV.addStretch()
        loginLayoutV.addLayout(checkBoxH)
        checkBoxH.addStretch()
        checkBoxH.addWidget(self.mslCheckBox)
        self.mslCheckBox.toggle()
        checkBoxH.addStretch()
        checkBoxH.addWidget(checkBoxLabel)

        loginLayoutV.addWidget(self.mslLoginWidget)
        self.mslLoginWidget.hide()
        self.mslLoginWidget.setLayout(mslLoginVLayout)

        mslLoginVLayout.addLayout(loginLayoutH1Msl)
        loginLayoutH1Msl.addStretch()
        loginLayoutH1Msl.addWidget(self.titleLoginMsl)
        loginLayoutH1Msl.addStretch()

        mslLoginVLayout.addLayout(loginLayoutH2msl)
        loginLayoutH2msl.addStretch()
        loginLayoutH2msl.addWidget(self.loginEmailMsl)
        loginLayoutH2msl.addStretch()

        mslLoginVLayout.addLayout(loginLayoutH3msl)
        loginLayoutH3msl.addStretch()
        loginLayoutH3msl.addWidget(self.loginPasswordMsl)
        loginLayoutH3msl.addStretch()

        loginLayoutV.addLayout(loginLayoutH4)
        loginLayoutH4.addStretch()
        loginLayoutH4.addWidget(exitButtonMb)
        loginLayoutH4.addStretch()
        loginLayoutH4.addWidget(loginButtonMb)
        loginLayoutH4.addStretch()

        loginLayoutV.addStretch()
        self.show()
        self.mslCheckBox.stateChanged.connect(self.showMslLogin)
        clickable(checkBoxLabel).connect(lambda: self.mslCheckBox.toggle())
        exitButtonMb.clicked.connect(lambda: exitApp())
        loginButtonMb.clicked.connect(lambda: self.login_mb(loginEmailMb.text(), loginPasswordMb.text()))

def exitApp():
    global browser
    browser.close()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        loginWindow = loginWindow()
        sys.exit(app.exec())
    except Exception as e:
        print("Error: ", e)
        global browser
        browser.close()
