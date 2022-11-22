# ббібліотека для GUI
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

# бібліотеки для роботи із системою
import os
import sys

# створюємо головне вікно

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
	
		
		self.qp = QPalette()
		self.qp.setColor(QPalette.Window, Qt.white)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.setCentralWidget(self.tabs)
		
		
		#статус
		self.status = QStatusBar()
		self.setStatusBar(self.status)

		#тулбар
		navtb = QToolBar("Navigation")
		navtb.setIconSize(QSize(16, 16))
		self.addToolBar(navtb)

		#кнопка назад
		back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
		back_btn.setStatusTip("Back to previous page")
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		navtb.addAction(back_btn)

		#кнопка вперед
		forward_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "forward", self)
		forward_btn.setStatusTip("forward to previous page")
		forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(forward_btn)

		#кнопка перезагрузити
		reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "reload", self)
		reload_btn.setStatusTip("reload")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		#кнопка додому
		home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "home", self)
		home_btn.setStatusTip("go to home page")
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)

		#Сепаратор
		navtb.addSeparator()

		#SSL ключ
		self.httpsicon = QLabel()
		self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))
		navtb.addWidget(self.httpsicon)
		#провірка пустої силки
	def add_new_tab(self, qurl=None, label="Blank"):
		if qurl is None:
			qurl = QUrl('')
		#запуск браузера
		browser = QWebEnigeView()
		#підставляє силку
		browser.setUrl(qurl)
		#додає нову вкладку
		i = self.tabs.addTab(browser, label)
		
		self.tabs.setCurrentIndex(i)
		#оновлює сторінку
		browser.urlChanged.connect(lambda qurl, browser=browser:
																self.update_urlbar(qurl, browser))
		#заголовок вікна вкладки
		browser.loadFinished.connect(lambda _, i=i, browser=browser:
																	self.tabs.setTabText(i, browser.page().title()))

	def tab_open_doubleclick(self, i):
		if i == -1: #додаємо вкладку в кінець списку
			self.add_new_tab()
	
	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		self.update_urlbar(qurl, self.tabs.currentWidget())
		self.update_title(self.tabs.currentWidget())
		#закриття вкладки
	def close_current_tab(self, i):
		if self.tabs.count() < 2:
			retrun
		
		self .tabs.removeTab(i)
	
	def update_title(self, browser):
		if browser != self.tabs.currentWidget():
			return
			
		title = self.tabs.currentWidget().page().title()
		self.seWindowTitle("%s - 1nbrowser" % title)
		
	def navigate_home(self):
		self.tabs.currentWidget().setUrl(QUrl ("http://www.google.com"))
	
	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
			
		self.tabs.currentWidget().setUrl(q)
		
	def update_urlbar(self, q, browser=None):
		if browser != self.tabs.currentWidget():
			return
		if q.scheme() == 'https':
			self.https.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))
		else:
			self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
		
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)
	
	

app = QApplication(sys.argv)
app.setApplicationName("1nbrowser")
window = MainWindow()
app.setPalette(window.qp)

app.exec_()
