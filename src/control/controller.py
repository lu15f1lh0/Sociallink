import view
import model

class Controller():
	def start(self):
		self.view.menu()
		opt = self.view.userOption()
		print(opt)
		while (opt != 4):
			if opt == 1:
				self.model.syncdata()
			elif opt == 2:
				lo = self.view.getLongitude()
				la = self.view.getLatitude()
				print(lo)
				print(la)        
				unitHealth = self.model.searchNearUnitHealth(lo, la)
				print(unitHealth)
				self.view.show(unitHealth)
			elif opt == 3:
				listOfUnitHealth = self.model.searchAllUnitHealth()
				self.view.showAll(listOfUnitHealth)
			elif opt == 5:
				self.model.generateLog()

			self.view.menu()
			opt = self.view.userOption()
			
	def __init__(self):
		self.view = view.View()
		self.model = model.NetDataModel()
