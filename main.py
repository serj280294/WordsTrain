
# add the following 2 lines to solve OpenGL 2.0 bug
from kivy import Config
Config.set('graphics', 'multisamples', '0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

#Config.set('graphics', 'resizable', '0')
#Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'width', '360')

from kivy.lang import Builder

from kivy.clock import Clock
import datetime

from kivy.storage.jsonstore import JsonStore
from kivy.factory import Factory

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BooleanProperty, DictProperty

class NewWordPopup(Popup):
	def saveWord(self):
		if self.checkForm():
			wordForm = {"word": self.ids.wordTextInp.text, 
						"translate": self.ids.translateTextInp.text,
						"weight": 0,
						"trainings": []}
			
			wordsTrainApp.addWord(wordsTrainApp, wordForm)
			self.clearForm()

	def checkForm(self):
		return True if self.ids.wordTextInp.text and self.ids.translateTextInp.text else False

	def clearForm(self):
		self.ids.wordTextInp.text = ""
		self.ids.translateTextInp.text = ""

class DictListItem(BoxLayout):
	word = StringProperty()
	translate = StringProperty()
	weight = StringProperty()
	number = StringProperty()

class DictionaryScreen(Screen):
	def on_enter(self):
		self.updateWordsList()
	
	def updateWordsList(self):
		self.ids.dict_rv.data = self.getWordsRecycleData()

	def getWordsRecycleData(self):
		recycleData = []

		for wordNumber, wordData in wordsTrainApp.getWords(wordsTrainApp).items():
			recycleData.append({"viewclass": "DictListItem", 
								"word":		 wordData['word'],
								"translate": wordData['translate'],
								"weight":	 str(wordData['weight']),
								"number": 	 wordNumber})

		if not recycleData:
			return [{"viewclass": "Label", "text":"Dictionary is empty"}]

		return recycleData

class MainScreen(Screen):
	pass

class wordsTrainApp(App):

	storeData = JsonStore("data.json")

	def build(self):
		self.screen = Factory.AppScreens()
		return self.screen

	def getWords(self):
		return {key: self.storeData.get(key) for key in [number for number in self.storeData.keys()]}

	def addWord(self, wordForm):
		nextNumber = self.getLastEntryNumber(self) + 1
		self.storeData.put(str(nextNumber), **wordForm)

	def deleteWord(self, wordNumber):
		self.storeData.delete(wordNumber)

	def getLastEntryNumber(self):
		if (self.storeData):
			return max([int(number) for number in self.storeData.keys()])
		else:
			return 0

if __name__ == "__main__":
    wordsTrainApp().run()
