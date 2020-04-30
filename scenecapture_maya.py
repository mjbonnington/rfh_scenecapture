#!/usr/bin/python

# scenecapture.py
#
# Mike Bonnington <michael@recomfarmhouse.com>
# (c) 2020 Recom Farmhouse
#
# A tool for capturing object and camera layouts during angle sessions.
# Ported from existing VRED tool.

'''
Run with the following code, or add to shelf

from rfh_scenecapture import scenecapture_maya
scenecapture_maya.run_maya()

'''


import os
import re
import sys
#from pkg_resources import resource_filename

import maya.cmds as mc

from Qt import QtCompat, QtCore, QtGui, QtWidgets

# Import custom modules


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

__version__ = "0.3.1"

cfg = {}

# Set window title and object names
cfg['window_title'] = "RFH Scene Capture"
cfg['window_object'] = "sceneCaptureUI"

# Set the UI and the stylesheet
cfg['ui_file'] = os.path.join(os.path.dirname(__file__), 'scenecapture.ui')

# Other options
cfg['dockable'] = True

# ----------------------------------------------------------------------------
# Begin main dialog class
# ----------------------------------------------------------------------------
 
class SceneCaptureUI(QtWidgets.QDialog):
	""" Preview UI.
	"""
	def __init__(self, parent=None):
		super(SceneCaptureUI, self).__init__(parent)
		self.parent = parent

		# Load UI
		self.ui = QtCompat.loadUi(cfg['ui_file'], self)

		# Set object name and window title
		self.setObjectName(cfg['window_object'])
		self.setWindowTitle(cfg['window_title'])

		# Set window icon, flags and other Qt attributes
		self.setWindowFlags(QtCore.Qt.Tool)
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Set icons

		# Connect signals & slots
		self.ui.pick_root1.clicked.connect(lambda: self.pick_root(1))
		self.ui.pick_root2.clicked.connect(lambda: self.pick_root(2))
		self.ui.pick_root3.clicked.connect(lambda: self.pick_root(3))
		self.ui.pick_root4.clicked.connect(lambda: self.pick_root(4))
		self.ui.pick_root5.clicked.connect(lambda: self.pick_root(5))
		self.ui.pick_root6.clicked.connect(lambda: self.pick_root(6))
		self.ui.pick_root7.clicked.connect(lambda: self.pick_root(7))
		self.ui.pick_root8.clicked.connect(lambda: self.pick_root(8))
		self.ui.pick_root9.clicked.connect(lambda: self.pick_root(9))
		self.ui.pick_root10.clicked.connect(lambda: self.pick_root(10))

		self.ui.capture_action.clicked.connect(self.capture)

		self.ui.set1.clicked.connect(lambda: self.set_nodes(1))
		self.ui.set2.clicked.connect(lambda: self.set_nodes(2))
		self.ui.set3.clicked.connect(lambda: self.set_nodes(3))
		self.ui.set4.clicked.connect(lambda: self.set_nodes(4))
		self.ui.set5.clicked.connect(lambda: self.set_nodes(5))
		self.ui.set6.clicked.connect(lambda: self.set_nodes(6))
		self.ui.set7.clicked.connect(lambda: self.set_nodes(7))
		self.ui.set8.clicked.connect(lambda: self.set_nodes(8))
		self.ui.set9.clicked.connect(lambda: self.set_nodes(9))
		self.ui.set10.clicked.connect(lambda: self.set_nodes(10))
		self.ui.set11.clicked.connect(lambda: self.set_nodes(11))
		self.ui.set12.clicked.connect(lambda: self.set_nodes(12))
		self.ui.set13.clicked.connect(lambda: self.set_nodes(13))
		self.ui.set14.clicked.connect(lambda: self.set_nodes(14))
		self.ui.set15.clicked.connect(lambda: self.set_nodes(15))
		self.ui.set16.clicked.connect(lambda: self.set_nodes(16))
		self.ui.set17.clicked.connect(lambda: self.set_nodes(17))
		self.ui.set18.clicked.connect(lambda: self.set_nodes(18))
		self.ui.set19.clicked.connect(lambda: self.set_nodes(19))
		self.ui.set20.clicked.connect(lambda: self.set_nodes(20))

		self.ui.captured_name_1.returnPressed.connect(lambda: self.text_edit(1))
		self.ui.captured_name_2.returnPressed.connect(lambda: self.text_edit(2))
		self.ui.captured_name_3.returnPressed.connect(lambda: self.text_edit(3))
		self.ui.captured_name_4.returnPressed.connect(lambda: self.text_edit(4))
		self.ui.captured_name_5.returnPressed.connect(lambda: self.text_edit(5))
		self.ui.captured_name_6.returnPressed.connect(lambda: self.text_edit(6))
		self.ui.captured_name_7.returnPressed.connect(lambda: self.text_edit(7))
		self.ui.captured_name_8.returnPressed.connect(lambda: self.text_edit(8))
		self.ui.captured_name_9.returnPressed.connect(lambda: self.text_edit(9))
		self.ui.captured_name_10.returnPressed.connect(lambda: self.text_edit(10))
		self.ui.captured_name_11.returnPressed.connect(lambda: self.text_edit(11))
		self.ui.captured_name_12.returnPressed.connect(lambda: self.text_edit(12))
		self.ui.captured_name_13.returnPressed.connect(lambda: self.text_edit(13))
		self.ui.captured_name_14.returnPressed.connect(lambda: self.text_edit(14))
		self.ui.captured_name_15.returnPressed.connect(lambda: self.text_edit(15))
		self.ui.captured_name_16.returnPressed.connect(lambda: self.text_edit(16))
		self.ui.captured_name_17.returnPressed.connect(lambda: self.text_edit(17))
		self.ui.captured_name_18.returnPressed.connect(lambda: self.text_edit(18))
		self.ui.captured_name_19.returnPressed.connect(lambda: self.text_edit(19))
		self.ui.captured_name_20.returnPressed.connect(lambda: self.text_edit(20))

		self.ui.recap1.clicked.connect(lambda: self.recapture_nodes(1))
		self.ui.recap2.clicked.connect(lambda: self.recapture_nodes(2))
		self.ui.recap3.clicked.connect(lambda: self.recapture_nodes(3))
		self.ui.recap4.clicked.connect(lambda: self.recapture_nodes(4))
		self.ui.recap5.clicked.connect(lambda: self.recapture_nodes(5))
		self.ui.recap6.clicked.connect(lambda: self.recapture_nodes(6))
		self.ui.recap7.clicked.connect(lambda: self.recapture_nodes(7))
		self.ui.recap8.clicked.connect(lambda: self.recapture_nodes(8))
		self.ui.recap9.clicked.connect(lambda: self.recapture_nodes(9))
		self.ui.recap10.clicked.connect(lambda: self.recapture_nodes(10))
		self.ui.recap11.clicked.connect(lambda: self.recapture_nodes(11))
		self.ui.recap12.clicked.connect(lambda: self.recapture_nodes(12))
		self.ui.recap13.clicked.connect(lambda: self.recapture_nodes(13))
		self.ui.recap14.clicked.connect(lambda: self.recapture_nodes(14))
		self.ui.recap15.clicked.connect(lambda: self.recapture_nodes(15))
		self.ui.recap16.clicked.connect(lambda: self.recapture_nodes(16))
		self.ui.recap17.clicked.connect(lambda: self.recapture_nodes(17))
		self.ui.recap18.clicked.connect(lambda: self.recapture_nodes(18))
		self.ui.recap19.clicked.connect(lambda: self.recapture_nodes(19))
		self.ui.recap20.clicked.connect(lambda: self.recapture_nodes(20))

		self.ui.del1.clicked.connect(lambda: self.delete(1))
		self.ui.del2.clicked.connect(lambda: self.delete(2))
		self.ui.del3.clicked.connect(lambda: self.delete(3))
		self.ui.del4.clicked.connect(lambda: self.delete(4))
		self.ui.del5.clicked.connect(lambda: self.delete(5))
		self.ui.del6.clicked.connect(lambda: self.delete(6))
		self.ui.del7.clicked.connect(lambda: self.delete(7))
		self.ui.del8.clicked.connect(lambda: self.delete(8))
		self.ui.del9.clicked.connect(lambda: self.delete(9))
		self.ui.del10.clicked.connect(lambda: self.delete(10))
		self.ui.del11.clicked.connect(lambda: self.delete(11))
		self.ui.del12.clicked.connect(lambda: self.delete(12))
		self.ui.del13.clicked.connect(lambda: self.delete(13))
		self.ui.del14.clicked.connect(lambda: self.delete(14))
		self.ui.del15.clicked.connect(lambda: self.delete(15))
		self.ui.del16.clicked.connect(lambda: self.delete(16))
		self.ui.del17.clicked.connect(lambda: self.delete(17))
		self.ui.del18.clicked.connect(lambda: self.delete(18))
		self.ui.del19.clicked.connect(lambda: self.delete(19))
		self.ui.del20.clicked.connect(lambda: self.delete(20))

		self.ui.pick_swap1.clicked.connect(lambda: self.pick_swap(1))
		self.ui.pick_swap2.clicked.connect(lambda: self.pick_swap(2))
		self.ui.swap_nodes.clicked.connect(self.swap)

		self.ui.width_spinBox.valueChanged.connect(self.width_edit)
		self.ui.height_spinBox.valueChanged.connect(self.height_edit)
		self.ui.path.returnPressed.connect(self.path_edit)
		self.ui.render_button.clicked.connect(self.render)

		self.init_me()


	def display(self):
		""" Initialise and display UI.
		"""
		self.returnValue = False

		self.show()
		self.raise_()

		return self.returnValue


	def init_me(self):
		""" Set up scene capture nodes.
		"""
		if not mc.objExists("sceneCapture_DONT_DELETE"):
			root_set = mc.createNode('transform', name="sceneCapture_DONT_DELETE" )  # sort in system
			roots = mc.createNode('transform', name="root_nodes", parent=root_set)
			captures = mc.createNode('transform', name="capture_nodes", parent=root_set)
			settings = mc.createNode('transform', name="rendersettings", parent=root_set)
			width = mc.createNode('transform', name="renderwidth", parent=settings)
			# mc.createNode('transform', name="2000", parent=width)
			height = mc.createNode('transform', name="renderheight", parent=settings)
			# mc.createNode('transform', name="1500", parent=height)
			path = mc.createNode('transform', name="path", parent=settings)
			# mc.createNode('transform', name="c:/", parent=path)

		else:
			for i in range(1, 21):
				if mc.objExists("sceneCap_rootNode_%d" % i):
					name = mc.listRelatives("sceneCap_rootNode_%d" % i, type='transform')[0]
					name = name.replace("_GEOM", "")
					lineEdit = self.ui.root_box.findChild(QtWidgets.QLineEdit, "root%d" % i)
					lineEdit.setText(name)

				# untested ---------------------------------------------------
				if mc.objExists("sceneCap_Slot_%d" % i):
					name = mc.listRelatives("sceneCap_Slot_%d" % i, type='transform')[0]
					self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % i).setEnabled(True)
					lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % i)
					lineEdit.setEnabled(True)
					lineEdit.setText(name)
					self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "recap%d" % i).setEnabled(True)
					self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "del%d" % i).setEnabled(True)
				# ------------------------------------------------------------

			# if findNode("renderwidth").getChild(0).isValid():
			# 	width=findNode("renderwidth").getChild(0).getName()
			# 	lineEdit = findQObject(render_box, "width")
			# 	lineEdit.setProperty("text", width)

			# if findNode("renderheight").getChild(0).isValid():
			# 	height=findNode("renderheight").getChild(0).getName()
			# 	lineEdit = findQObject(render_box, "height")
			# 	lineEdit.setProperty("text", height)

			# if findNode("path").getChild(0).isValid():
			# 	path=findNode("path").getChild(0).getName()
			# 	lineEdit = findQObject(render_box, "path")
			# 	lineEdit.setProperty("text", path)

		if not mc.objExists("rendersettings"):
			print("add settings")
			root_set = "sceneCapture_DONT_DELETE"  # sort in system
			settings = createNode('transform', name="rendersettings", parent=root_set)
			width = createNode('transform', name="renderwidth", parent=settings)
			# createNode('transform', name="2000", parent=width)
			height = createNode('transform', name="renderheight", parent=settings)
			# createNode('transform', name="1500", parent=height)
			path = createNode('transform', name="path", parent=settings)
			# createNode('transform', name="c:/", parent=path)


	def pick_root(self, slot):
		""" Pick a root node and add it to the specified slot.
		"""
		try:
			node = mc.ls(selection=True, type='transform')[-1]

			root_slot = "sceneCap_rootNode_%d" % slot
			lineEdit = self.ui.root_box.findChild(QtWidgets.QLineEdit, "root%d" % slot)
			lineEdit.setText(node)
			if mc.objExists(root_slot):
				mc.delete(root_slot)
			root = mc.createNode('transform', name=root_slot, parent="root_nodes")
			mc.createNode('transform', name="%s_GEOM" % node, parent=root)

			# untested -------------------------------------------------------
			for i in range(1, 21):
				#print("slot: %d" % i)
				slot_to_change = "sceneCap_Slot_%d" % i
				if mc.objExists(slot_to_change):
					print("changing slot: %d" % i)
					for j in range(1, 11):
						root_to_change = mc.listRelatives(slot_to_change, type='transform')[j]
						if mc.objExists(root_to_change):
							print("rootname: %s" + root_to_change)
							if root_to_change == "root%d" % slot:
								child = mc.listRelatives(root_to_change, type='transform')[0]
								print(child)
								mc.rename(child, "GEOMNAME_"+node)
			# ----------------------------------------------------------------

			mc.select(node)

		except IndexError:
			mc.warning("Nothing selected.")


	def capture(self):
		""" Capture the scene state and add it to the next free slot.
			TODO: Some of this code is pretty janky and should be refactored
		"""
		name = self.ui.capture_name.text()
		print("capture set with name: " + name)

		enabled = 1
		i = 0

		# Exclude double name (?)
		captured_names = []
		for i in range(1, 21):
			if self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % i).isEnabled():
				captured_names.append(self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % i).text())

		i = 0
		while enabled == 1:
			i += 1
			print("search empty slot %d" % i)
			if not self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % i).isEnabled():
				print("slot %d inactive" % i)
				self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % i).setEnabled(True)
				self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % i).setEnabled(True)
				self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "recap%d" % i).setEnabled(True)
				self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "del%d" % i).setEnabled(True)
				if name == "":
					name = "unnamed%d" % i
				# elif "_" in name:
				# 	name = name + str(i)
				if name in captured_names:
					name += "_v%d" % i
				lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % i)
				lineEdit.setText(name)
				enabled = 0
				self.capture_nodes(i, name)
	
			if i == 20:
				enabled=0
				mc.warning("No free slots.")


	def capture_nodes(self, slot, name):
		""" Capture state and store data.
		"""
		roots = "capture_nodes"
		slot = mc.createNode('transform', name="sceneCap_Slot_%d" % slot, parent=roots)
		slotname = mc.createNode('transform', name=name, parent=slot)

		# addViewPoint("SceneCap_" + name)
		panel = mc.getPanel(withFocus=True)
		camera = mc.modelPanel(panel, cam=True, q=True)
		print(camera)
		snapcam = mc.duplicate(camera, name="SceneCap_"+name, rr=True)
		mc.parent(snapcam, slotname)

		for i in range(1, 11):
			current_node = self.ui.root_box.findChild(QtWidgets.QLineEdit, "root%d" % i).text()

			if len(current_node):
				print("hello")
				rootnode = mc.createNode('transform', name="root%d" % i, parent=slot)
				slotroot = mc.createNode('transform', name="GEOMNAME_"+current_node, parent=rootnode)

				mc.matchTransform(slotroot, current_node)
				mc.setAttr(slotroot+'.visibility', mc.getAttr(current_node+'.visibility'))

				if mc.objExists("WHEEL_FL_TURN"):
					wheelfl = mc.createNode('transform', name="GEOMNAME_WHEEL_FL_TURN", parent=rootnode)
					mc.matchTransform(wheelfl, "WHEEL_FL_TURN")
				if mc.objExists("WHEEL_FR_TURN"):
					wheelfl = mc.createNode('transform', name="GEOMNAME_WHEEL_FR_TURN", parent=rootnode)
					mc.matchTransform(wheelfl, "WHEEL_FR_TURN")


	def recapture_nodes(self, slot):
		""" TODO: Almost identical to capture_nodes - could be combined
		"""
		mc.select(clear=True)

		roots = "capture_nodes"

		name = mc.listRelatives("sceneCap_Slot_%d" % slot, type='transform')[0]
		mc.delete("sceneCap_Slot_%d" % slot)
		# removeViewPoint("SceneCap_" + name)

		slot = mc.createNode('transform', name="sceneCap_Slot_%d" % slot, parent=roots)
		slotname = mc.createNode('transform', name=name, parent=slot)

		# addViewPoint("SceneCap_" + name)
		panel = mc.getPanel(withFocus=True)
		camera = mc.modelPanel(panel, cam=True, q=True)
		print(camera)
		snapcam = mc.duplicate(camera, name="SceneCap_"+name, rr=True)
		mc.parent(snapcam, slotname)

		for i in range(1, 11):
			current_node = self.ui.root_box.findChild(QtWidgets.QLineEdit, "root%d" % i).text()

			if len(current_node):
				print("recapture %s" % current_node)
				rootnode = mc.createNode('transform', name="root%d" % i, parent=slot)
				slotroot = mc.createNode('transform', name="GEOMNAME_"+current_node, parent=rootnode)

				mc.matchTransform(slotroot, current_node)
				mc.setAttr(slotroot+'.visibility', mc.getAttr(current_node+'.visibility'))

				if mc.objExists("WHEEL_FL_TURN"):
					wheelfl = mc.createNode('transform', name="GEOMNAME_WHEEL_FL_TURN", parent=rootnode)
					mc.matchTransform(wheelfl, "WHEEL_FL_TURN")
				if mc.objExists("WHEEL_FR_TURN"):
					wheelfl = mc.createNode('transform', name="GEOMNAME_WHEEL_FR_TURN", parent=rootnode)
					mc.matchTransform(wheelfl, "WHEEL_FR_TURN")

				# mc.setAttr(rootnode+'.visibility', mc.getAttr(current_node+'.visibility'))


	def set_nodes(self, slot):
		""" Restore captured state.
			TODO: Make it work and refactor from this shit-show
		"""
		root = "sceneCap_Slot_%d" % slot
		rootroots = mc.listRelatives(root, type='transform', fullPath=True)
		num_roots = len(rootroots)
		print("SET Slot %d" % slot)

		# Restore camera bookmark
		name = "SceneCap_" + mc.listRelatives("sceneCap_Slot_%d" % slot, type='transform')[0]
		# jumpViewPoint(name)
		# print(name)
		snapcam = rootroots[0]+"|SceneCap_*"
		if mc.objExists(snapcam):
			freecam = "FreeCam_*"
			if mc.objExists(freecam):
				mc.delete(freecam)
			currentcam = mc.duplicate(snapcam, name="FreeCam_"+name, rr=True)
			mc.parent(currentcam, "sceneCapture_DONT_DELETE")
			panel = mc.getPanel(withFocus=True)
			mc.lookThru(panel, currentcam)

		for i in range(num_roots-1):
			rootnode = rootroots[i+1]
			geom_name = mc.listRelatives(rootnode, type='transform', fullPath=True)[0]
			node = geom_name.split("|")[-1].replace("GEOMNAME_", "")
			print("moveNode: %s" % node)

			if mc.objExists(node):
				mc.matchTransform(node, geom_name)
				mc.setAttr(node+'.visibility', mc.getAttr(geom_name+'.visibility'))

				if mc.objExists(rootnode+"|GEOMNAME_WHEEL_FL_TURN"):
					mc.matchTransform("WHEEL_FL_TURN", rootnode+"|GEOMNAME_WHEEL_FL_TURN")
				if mc.objExists(rootnode+"|GEOMNAME_WHEEL_FR_TURN"):
					mc.matchTransform("WHEEL_FR_TURN", rootnode+"|GEOMNAME_WHEEL_FR_TURN")


	def delete(self, slot):
		""" Delete a capture.
		"""
		print("delete %d" % slot)

		name_lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % slot)
		name_lineEdit.setEnabled(False)
		name_lineEdit.setText("")

		self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % slot).setEnabled(False)
		self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "recap%d" % slot).setEnabled(False)
		self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "del%d" % slot).setEnabled(False)

		mc.delete("sceneCap_Slot_%d" % slot)

		# name = findNode("sceneCap_Slot_%d" % slot).getChild(0).getName()
		# # viewpoints=getViewpoints()
		# # viewname="SceneCap_" + name
		# # if viewname in viewpoints:
		# removeViewPoint("SceneCap_" + name)


	def text_edit(self, slot):
		""" Change the name of a capture.
		"""
		print("text_edit %d" % slot)

		slot_to_change = "sceneCap_Slot_%d" % slot

		if mc.objExists(slot_to_change):
			name_to_change = mc.listRelatives(slot_to_change, type='transform')[0]

			if mc.objExists(name_to_change):
				print("slitti")  # ?
				# viewpoint_name = "SceneCap_" + slot_to_change.getChild(0).getName()
				# jumpViewPoint(viewpoint_name)
				# removeViewPoint(viewpoint_name)

				name = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % slot).text()
				print(name)
				if name == "":
					name = "unnamed%d" % slot
				mc.rename(name_to_change, name)
				# addViewPoint("SceneCap_" + name)


	def pick_swap(self, slot):
		""" Pick a transform to add to the swap box entry.
		"""
		print("pick_swap %d" % slot)

		node = mc.ls(selection=True, type='transform')[-1]

		if mc.objExists(node):
			lineEdit = self.ui.swap_box.findChild(QtWidgets.QLineEdit, "swap%d" % slot)
			lineEdit.setText(node)


	def swap(self):
		""" Swap the positions of two objects.
		"""
		node1 = self.ui.swap1.text()
		node2 = self.ui.swap2.text()
		print("swap %s and %s" % (node1, node2))

		if mc.objExists(node1) and mc.objExists(node2):
			xformtmp = mc.createNode('transform', name="TEMP_SWAP_BUFFER", skipSelect=True)
			mc.matchTransform(xformtmp, node1)
			mc.matchTransform(node1, node2)
			mc.matchTransform(node2, xformtmp)
			mc.delete(xformtmp)


	def width_edit(self):
		""" 
		"""
		print("width_edit")

		# name_to_change = findNode("renderwidth").getChild(0)
		# if name_to_change.isValid():
		# 	name = self.ui.width.text()  # TODO: change to QSpinBox
		# 	name_to_change.setName(name)


	def height_edit(self):
		""" 
		"""
		print("height_edit")

		# name_to_change = findNode("renderheight").getChild(0)
		# if name_to_change.isValid():
		# 	name = self.ui.height.text()  # TODO: change to QSpinBox
		# 	name_to_change.setName(name)


	def path_edit(self):
		""" 
		"""
		print("path_edit")

		# name_to_change = findNode("path").getChild(0)
		# if name_to_change.isValid():
		# 	name = self.ui.path.text()
		# 	name_to_change.setName(name)


	def render(self):
		""" Render the selected snapshots.
		"""
		print("render")

		width = self.ui.width_spinBox.value()
		height = self.ui.height_spinBox.value()
		path = self.ui.path.text()
		extension = "."+self.ui.filetype.currentText()

		for i in range(1, 21):
			render_checkBox = self.ui.captured_sets_box.findChild(QtWidgets.QCheckBox, "render_set%d" % i)
			set_toolButton = self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % i)

			if render_checkBox.checkState() == QtCore.Qt.Checked and set_toolButton.isEnabled():
				self.set_nodes(i)

				name_lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % i)
				filename = path+name_lineEdit.text()+extension
				if extension == ".jpg":
					print("createSnapshot(%s, %d, %d, 2, 0)" % (filename, width, height))
				else:
					print("createSnapshot(%s, %d, %d, 2, 1)" % (filename, width, height))

# ----------------------------------------------------------------------------
# End of main dialog class
# ============================================================================
# DCC helper / Run functions
# ----------------------------------------------------------------------------

def _maya_main_window():
	""" Return Maya's main window.
	"""
	for obj in QtWidgets.QApplication.topLevelWidgets():
		if obj.objectName() == 'MayaWindow':
			return obj
	raise RuntimeError("Could not find MayaWindow instance")


def _maya_delete_ui(window_object, window_title):
	""" Delete existing UI in Maya.
	"""
	if mc.window(window_object, query=True, exists=True):
		mc.deleteUI(window_object)  # Delete window
		print("Delete UI: " + window_object)

	dock_control = '%s|%s' % (_maya_main_window().objectName(), re.sub(r'\W', '_', window_title))
	if mc.dockControl(dock_control, query=True, exists=True):
		mc.deleteUI(dock_control)  # Delete docked window
		print("Delete Dock Control: " + dock_control)


def run_maya(session=None, dock=False, **kwargs):
	""" Run in Maya.
		'session' is a persistent object to bind to
		'dock' docks the window, value can be either 'left' or 'right'
	"""
	if session is None:
		# session = AppSession()
		_maya_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		sceneCaptureUI = SceneCaptureUI(parent=_maya_main_window())

		if dock and cfg['dockable']:
			allowed_areas = ['right', 'left']
			mc.dockControl(
				cfg['window_title'], 
				label=cfg['window_title'], 
				area=dock, 
				content=cfg['window_object'], 
				allowedArea=allowed_areas
			)
		else:
			sceneCaptureUI.display(**kwargs)  # Show the UI

	else:
		try:
			session.sceneCaptureUI.display(**kwargs)

		except:
			_maya_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
			session.sceneCaptureUI = SceneCaptureUI(parent=_maya_main_window())
			session.sceneCaptureUI.display(**kwargs)
