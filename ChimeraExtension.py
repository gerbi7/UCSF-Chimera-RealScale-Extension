import chimera.extension

# -----------------------------------------------------------------------------
#
class Real_Scale_EMO(chimera.extension.EMO):

	def name(self):
		return 'Real-Life Scaling Utility'
	def description(self):
		return 'Utility for managing scaling, useful for applications such as 3D printing.'
	def categories(self):
		return ['Utilities']
# 	def icon(self):
# 		return self.path('scalebar.gif')
	def activate(self):
 		self.module().show_dialog()
		return None

# -----------------------------------------------------------------------------
#
chimera.extension.manager.registerExtension(Real_Scale_EMO(__file__))
