#!/usr/bin/python

# scenecapture.py
#
# Mike Bonnington <michael@recomfarmhouse.com>
# (c) 2020 Recom Farmhouse
#
# A tool for capturing object and camera layouts for stills.
# Ported from existing VRED tool.

'''
Run with the following code, or add to shelf

from rfh_scenecapture import scenecapture_maya
scenecapture_maya.run_maya()

'''


import json
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

__version__ = "0.4.0"

CAPTURE_SET = "sceneCapture_set1"
CAPTURE_ATTR_PREFIX = "captureData_"

cfg = {}

# Set window title and object names
cfg['window_title'] = "RFH Scene Capture v" + __version__
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
		# self.ui.pick_root1.clicked.connect(lambda: self.pick_root(1))
		# self.ui.pick_root2.clicked.connect(lambda: self.pick_root(2))
		# self.ui.pick_root3.clicked.connect(lambda: self.pick_root(3))
		# self.ui.pick_root4.clicked.connect(lambda: self.pick_root(4))
		# self.ui.pick_root5.clicked.connect(lambda: self.pick_root(5))
		# self.ui.pick_root6.clicked.connect(lambda: self.pick_root(6))
		# self.ui.pick_root7.clicked.connect(lambda: self.pick_root(7))
		# self.ui.pick_root8.clicked.connect(lambda: self.pick_root(8))
		# self.ui.pick_root9.clicked.connect(lambda: self.pick_root(9))
		# self.ui.pick_root10.clicked.connect(lambda: self.pick_root(10))

		self.ui.capture_action.clicked.connect(self.capture)

		self.ui.set1.clicked.connect(lambda: self.restore(1))
		self.ui.set2.clicked.connect(lambda: self.restore(2))
		self.ui.set3.clicked.connect(lambda: self.restore(3))
		self.ui.set4.clicked.connect(lambda: self.restore(4))
		self.ui.set5.clicked.connect(lambda: self.restore(5))
		self.ui.set6.clicked.connect(lambda: self.restore(6))
		self.ui.set7.clicked.connect(lambda: self.restore(7))
		self.ui.set8.clicked.connect(lambda: self.restore(8))
		self.ui.set9.clicked.connect(lambda: self.restore(9))
		self.ui.set10.clicked.connect(lambda: self.restore(10))
		self.ui.set11.clicked.connect(lambda: self.restore(11))
		self.ui.set12.clicked.connect(lambda: self.restore(12))
		self.ui.set13.clicked.connect(lambda: self.restore(13))
		self.ui.set14.clicked.connect(lambda: self.restore(14))
		self.ui.set15.clicked.connect(lambda: self.restore(15))
		self.ui.set16.clicked.connect(lambda: self.restore(16))
		self.ui.set17.clicked.connect(lambda: self.restore(17))
		self.ui.set18.clicked.connect(lambda: self.restore(18))
		self.ui.set19.clicked.connect(lambda: self.restore(19))
		self.ui.set20.clicked.connect(lambda: self.restore(20))

		# self.ui.captured_name_1.returnPressed.connect(lambda: self.rename(1))
		# self.ui.captured_name_2.returnPressed.connect(lambda: self.rename(2))
		# self.ui.captured_name_3.returnPressed.connect(lambda: self.rename(3))
		# self.ui.captured_name_4.returnPressed.connect(lambda: self.rename(4))
		# self.ui.captured_name_5.returnPressed.connect(lambda: self.rename(5))
		# self.ui.captured_name_6.returnPressed.connect(lambda: self.rename(6))
		# self.ui.captured_name_7.returnPressed.connect(lambda: self.rename(7))
		# self.ui.captured_name_8.returnPressed.connect(lambda: self.rename(8))
		# self.ui.captured_name_9.returnPressed.connect(lambda: self.rename(9))
		# self.ui.captured_name_10.returnPressed.connect(lambda: self.rename(10))
		# self.ui.captured_name_11.returnPressed.connect(lambda: self.rename(11))
		# self.ui.captured_name_12.returnPressed.connect(lambda: self.rename(12))
		# self.ui.captured_name_13.returnPressed.connect(lambda: self.rename(13))
		# self.ui.captured_name_14.returnPressed.connect(lambda: self.rename(14))
		# self.ui.captured_name_15.returnPressed.connect(lambda: self.rename(15))
		# self.ui.captured_name_16.returnPressed.connect(lambda: self.rename(16))
		# self.ui.captured_name_17.returnPressed.connect(lambda: self.rename(17))
		# self.ui.captured_name_18.returnPressed.connect(lambda: self.rename(18))
		# self.ui.captured_name_19.returnPressed.connect(lambda: self.rename(19))
		# self.ui.captured_name_20.returnPressed.connect(lambda: self.rename(20))

		self.ui.recap1.clicked.connect(lambda: self.recapture(1))
		self.ui.recap2.clicked.connect(lambda: self.recapture(2))
		self.ui.recap3.clicked.connect(lambda: self.recapture(3))
		self.ui.recap4.clicked.connect(lambda: self.recapture(4))
		self.ui.recap5.clicked.connect(lambda: self.recapture(5))
		self.ui.recap6.clicked.connect(lambda: self.recapture(6))
		self.ui.recap7.clicked.connect(lambda: self.recapture(7))
		self.ui.recap8.clicked.connect(lambda: self.recapture(8))
		self.ui.recap9.clicked.connect(lambda: self.recapture(9))
		self.ui.recap10.clicked.connect(lambda: self.recapture(10))
		self.ui.recap11.clicked.connect(lambda: self.recapture(11))
		self.ui.recap12.clicked.connect(lambda: self.recapture(12))
		self.ui.recap13.clicked.connect(lambda: self.recapture(13))
		self.ui.recap14.clicked.connect(lambda: self.recapture(14))
		self.ui.recap15.clicked.connect(lambda: self.recapture(15))
		self.ui.recap16.clicked.connect(lambda: self.recapture(16))
		self.ui.recap17.clicked.connect(lambda: self.recapture(17))
		self.ui.recap18.clicked.connect(lambda: self.recapture(18))
		self.ui.recap19.clicked.connect(lambda: self.recapture(19))
		self.ui.recap20.clicked.connect(lambda: self.recapture(20))

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
		# Check for existing capture data and populate list in UI
		self.root_set = CAPTURE_SET
		if mc.objExists(self.root_set):
			capture_list = mc.listAttr(self.root_set, userDefined=True)
			i = 1
			if capture_list:
				for attr_name in capture_list:
					if attr_name.startswith(CAPTURE_ATTR_PREFIX):
						capture_id = attr_name.replace(CAPTURE_ATTR_PREFIX, "")
						self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % i).setEnabled(True)
						lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % i)
						lineEdit.setEnabled(True)
						lineEdit.setText(capture_id)
						self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "recap%d" % i).setEnabled(True)
						self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "del%d" % i).setEnabled(True)
						i += 1 # will break after 20

		# Create set to hold capture data
		else:
			self.root_set = mc.sets(n=self.root_set)


	# def pick_root(self, slot):
	# 	""" Pick a root node and add it to the specified slot.
	# 	"""
	# 	try:
	# 		node = mc.ls(selection=True, type='transform')[-1]

	# 		root_slot = "sceneCap_rootNode_%d" % slot
	# 		lineEdit = self.ui.root_box.findChild(QtWidgets.QLineEdit, "root%d" % slot)
	# 		lineEdit.setText(node)
	# 		if mc.objExists(root_slot):
	# 			mc.delete(root_slot)
	# 		root = mc.createNode('transform', name=root_slot, parent="root_nodes")
	# 		mc.createNode('transform', name="%s_GEOM" % node, parent=root)

	# 		# untested -------------------------------------------------------
	# 		for i in range(1, 21):
	# 			#print("slot: %d" % i)
	# 			slot_to_change = "sceneCap_Slot_%d" % i
	# 			if mc.objExists(slot_to_change):
	# 				print("changing slot: %d" % i)
	# 				for j in range(1, 11):
	# 					root_to_change = mc.listRelatives(slot_to_change, type='transform')[j]
	# 					if mc.objExists(root_to_change):
	# 						print("rootname: %s" + root_to_change)
	# 						if root_to_change == "root%d" % slot:
	# 							child = mc.listRelatives(root_to_change, type='transform')[0]
	# 							print(child)
	# 							mc.rename(child, "GEOMNAME_"+node)
	# 		# ----------------------------------------------------------------

	# 		mc.select(node)

	# 	except IndexError:
	# 		mc.warning("Nothing selected.")


	def capture(self):
		""" Capture a snapshot of the current state and add it to the next
			free slot.
			TODO: Some of this code is pretty janky and should be refactored
		"""
		capture_id = self.ui.capture_name.text()
		print("capture set with name: " + capture_id)

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
				if capture_id == "":
					capture_id = "unnamed%d" % i
				# elif "_" in capture_id:
				# 	capture_id = capture_id + str(i)
				if capture_id in captured_names:
					capture_id += "_v%d" % i
				lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % i)
				lineEdit.setText(capture_id)
				enabled = 0
				self.store(i, capture_id)
	
			if i == 20:
				enabled=0
				mc.warning("No free slots.")


	def recapture(self, slot):
		""" Re-capture an existing snapshot.
		"""
		lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % slot)
		capture_id = lineEdit.text()

		self.store(slot, capture_id)


	def store(self, slot, capture_id):
		""" Store data for a captured state.
		"""
		capture_data = {}
		set_members = []

		for node in mc.sets(self.root_set, q=True):
			set_members.append(node)

			shapes = mc.listRelatives(node, shapes=True, fullPath=True)
			if shapes:
				for shape in shapes:
					set_members.append(shape)

		for node in set_members:
			capture_data[node] = {}

			keyable_attrs = mc.listAttr(node, keyable=True)
			if keyable_attrs:
				for attr in keyable_attrs:
					try:
						capture_data[node][attr] = mc.getAttr(node+"."+attr)
					except KeyError:
						capture_data[node] = {attr: mc.getAttr(node+"."+attr)}
					except RuntimeError as e:
						mc.warning(str(e))

		serialized_data = json.dumps(capture_data, indent=4, sort_keys=True)
		attr_name = CAPTURE_ATTR_PREFIX + capture_id
		if not mc.attributeQuery(attr_name, node=self.root_set, exists=True):
			mc.addAttr(self.root_set, ln=attr_name, dt="string")
		mc.setAttr(self.root_set+"."+attr_name, serialized_data, type="string")


	def restore(self, slot):
		""" Restore from a captured state.
		"""
		lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % slot)
		capture_id = lineEdit.text()

		attr_name = CAPTURE_ATTR_PREFIX + capture_id
		capture_data = json.loads(mc.getAttr(self.root_set+"."+attr_name))

		for node, attributes in capture_data.items():
			for attr, value in attributes.items():
				# print(node, attr, value)
				try:
					mc.setAttr(node+"."+attr, value)
				except RuntimeError as e:
					mc.warning(str(e))


	def delete(self, slot):
		""" Delete a saved capture.
		"""
		lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % slot)
		capture_id = lineEdit.text()
		attr_name = CAPTURE_ATTR_PREFIX + capture_id

		try:
			mc.deleteAttr(self.root_set+"."+attr_name)
		except ValueError as e:
			mc.warning(str(e))

		lineEdit.setEnabled(False)
		lineEdit.setText("")
		self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % slot).setEnabled(False)
		self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "recap%d" % slot).setEnabled(False)
		self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "del%d" % slot).setEnabled(False)


	# def rename(self, slot):
	# 	""" Change the name of a capture.
	# 	"""
	# 	slot_to_change = "sceneCap_Slot_%d" % slot

	# 	if mc.objExists(slot_to_change):
	# 		name_to_change = mc.listRelatives(slot_to_change, type='transform')[0]

	# 		if mc.objExists(name_to_change):
	# 			print("slitti")  # ?
	# 			# viewpoint_name = "SceneCap_" + slot_to_change.getChild(0).getName()
	# 			# jumpViewPoint(viewpoint_name)
	# 			# removeViewPoint(viewpoint_name)

	# 			name = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % slot).text()
	# 			print(name)
	# 			if name == "":
	# 				name = "unnamed%d" % slot
	# 			mc.rename(name_to_change, name)
	# 			# addViewPoint("SceneCap_" + name)


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
				self.restore(i)

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
