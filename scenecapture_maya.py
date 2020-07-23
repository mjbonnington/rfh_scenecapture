#!/usr/bin/python

'''
scenecapture_maya.py

Mike Bonnington <michael@recomfarmhouse.com>
(c) 2020 Recom Farmhouse

A tool for capturing object and camera layouts for stills.
Adapted from existing VRED tool.

Run with the following code, or add to shelf:

from rfh_scenecapture import scenecapture_maya
scenecapture_maya.run_maya()

'''

import json
import math
import os
import re
import shutil
import sys
import time

import maya.cmds as mc
import maya.mel as mel

from Qt import QtCompat, QtCore, QtGui, QtWidgets

# Import custom modules
# from . import icons_rc
from . import mjb_transform_ops
from . import preview_maya


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

__version__ = "0.4.7"

CAPTURE_SET = "sceneCapture_set1"
CAPTURE_ATTR_PREFIX = "captureData_"
SNAPSHOT_MAX_RES = [1024, 1024]

cfg = {}

# Set window title and object names
cfg['window_title'] = "RFH Scene Capture v" + __version__
cfg['window_object'] = "sceneCaptureUI"

# Set the UI and the stylesheet
cfg['ui_file'] = os.path.join(os.path.dirname(__file__), 'ui', 'scenecapture.ui')

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

		# Makes Maya perform magic which makes the window stay on top in
		# OS X and Linux. As an added bonus, it'll make Maya remember the
		# window position.
		self.setProperty("saveWindowPref", True)

		# Set icons
		self.ui.capture_toolButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'capture.png')))
		self.ui.xformCopy_pushButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'copy.png')))
		self.ui.xformPaste_pushButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'paste.png')))
		self.ui.xformSwap_pushButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'swap.png')))
		self.ui.import_pushButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'import.png')))
		self.ui.export_pushButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'export.png')))
		self.ui.delData_pushButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'delete.png')))

		# Connect signals & slots
		self.ui.capture_toolButton.clicked.connect(lambda: self.store(self.ui.captureName_lineEdit.text(), force=False))
		self.ui.captureName_lineEdit.returnPressed.connect(lambda: self.store(self.ui.captureName_lineEdit.text(), force=False))
		self.ui.setEditor_pushButton.clicked.connect(lambda: mel.eval("SetEditor;"))
		self.ui.xformCopy_pushButton.clicked.connect(mjb_transform_ops.copy_transform)
		self.ui.xformPaste_pushButton.clicked.connect(mjb_transform_ops.paste_transform)
		self.ui.xformSwap_pushButton.clicked.connect(mjb_transform_ops.swap_transforms)
		self.ui.import_pushButton.clicked.connect(self.import_json)
		self.ui.export_pushButton.clicked.connect(self.export_json)
		self.ui.delData_pushButton.clicked.connect(self.delete_data)

		# self.ui.width_spinBox.valueChanged.connect(self.width_edit)
		# self.ui.height_spinBox.valueChanged.connect(self.height_edit)
		# self.ui.path_lineEdit.returnPressed.connect(self.path_edit)
		# self.ui.render_button.clicked.connect(self.render)

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[a-zA-Z_][a-zA-Z0-9_]*'), self.ui.captureName_lineEdit)
		self.ui.captureName_lineEdit.setValidator(alphanumeric_validator)

		# General initialisation
		self.root_set = CAPTURE_SET  # currently hard-coded
		if not mc.objExists(self.root_set):
			self.root_set = mc.sets(n=self.root_set)
		self.ui.set_comboBox.addItem(self.root_set)
		self.ui.tabWidget.removeTab(2)  # temp: remove render tab until implemented
		#self.ui.data_groupBox.setEnabled(False)  # temp: disable until implemented
		self.ui.snapCam_comboBox.addItems(self.get_snapshot_cam())

		self.refresh_capture_ui()


	def display(self):
		""" Initialise and display UI.
		"""
		self.returnValue = False

		self.show()
		self.raise_()

		return self.returnValue


	def refresh_capture_ui(self):
		""" Rebuild UI to show list of captures.
		"""
		# Delete existing items
		layout = self.ui.captures_verticalLayout
		for i in reversed(range(layout.count())):
			item = layout.itemAt(i).widget()
			if item:
				item.deleteLater()

		# Check for existing capture data and populate list in UI
		self.root_set = self.ui.set_comboBox.currentText() #CAPTURE_SET
		if mc.objExists(self.root_set):
			capture_list = mc.listAttr(self.root_set, userDefined=True)
			if capture_list:
				for attr_name in capture_list:
					if attr_name.startswith(CAPTURE_ATTR_PREFIX):
						self.add_snapshot_ui(attr_name, layout)
			# else:
			# 	self.ui.tabWidget.setCurrentTab(0)  # If no captures, go to setup tab


			# layout.insertStretch(-1, 1)  # Add spacer to bottom of layout

		# Create set to hold capture data
		else:
			self.root_set = mc.sets(n=self.root_set)


	def add_snapshot_ui(self, attr_name, layout):
		""" Add a capture item to the list by loading the template UI and
			populating its fields.
		"""
		capture_data = json.loads(mc.getAttr(self.root_set+"."+attr_name))
		capture_id = attr_name.replace(CAPTURE_ATTR_PREFIX, "")

		ui_file = os.path.join(os.path.dirname(__file__), 'ui', 'capture_item.ui')
		ui = QtCompat.loadUi(ui_file)

		ui.name_lineEdit.setText(capture_id)

		# Set icons
		ui.recap_toolButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'capture.png')))
		ui.delete_toolButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'delete.png')))
		ui.render_toolButton.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'ui', 'render.png')))
		ui.render_toolButton.setEnabled(False)  # temp until implemented

		default_thumb = os.path.join(os.path.dirname(__file__), 'ui', 'placeholder_thumb.png')
		thumb = capture_data.get('snapshot', default_thumb)
		if os.path.isfile(thumb):
			pixmap = QtGui.QPixmap(thumb)
		else:
			pixmap = QtGui.QPixmap(default_thumb)
		timestamp = capture_data.get('time', 'unknown')
		ui.capture_toolButton.setIcon(pixmap)
		ui.capture_toolButton.setText(timestamp)

		# Add capture UI instance to layout
		layout.addWidget(ui)

		# Connect signals & slots
		ui.capture_toolButton.clicked.connect(lambda: self.restore(attr_name))
		ui.name_lineEdit.returnPressed.connect(lambda: self.rename(attr_name, ui.name_lineEdit.text()))
		# ui.name_lineEdit.textEdited.connect(lambda text: self.rename(attr_name, text))
		ui.recap_toolButton.clicked.connect(lambda: self.store(capture_id, force=True))
		ui.delete_toolButton.clicked.connect(lambda: self.delete(attr_name))


	def store(self, capture_id, force=False):
		""" Store data for a captured state.
		"""
		if capture_id == "":
			mc.warning("Please give the capture a valid name.")
			return

		if (capture_id in self.capture_list()) and (not force):
			if self.confirm_overwite(capture_id) == 'No':
				return

		set_members = []
		capture_data = {}

		# Get capture set members
		set_contents = mc.sets(self.root_set, q=True)
		if set_contents:
			for node in set_contents:
				set_members.append(node)

				shapes = mc.listRelatives(node, shapes=True, fullPath=True)
				if shapes:
					for shape in shapes:
						set_members.append(shape)

		else:
			mc.warning("Set '%s' has no contents to capture." % self.root_set)
			return

		# Get current time
		capture_data['time'] = time.strftime("%d/%m/%Y %H:%M")

		# Take snapshot
		snapshot_img = self.snapshot(capture_id)
		if snapshot_img:
			capture_data['snapshot'] = snapshot_img

		# Store all keyable attributes of set members
		for node in set_members:
			capture_data[node] = {}

			keyable_attrs = mc.listAttr(node, keyable=True)
			if keyable_attrs:
				for attr in keyable_attrs:
					try:
						capture_data[node][attr] = mc.getAttr(node+"."+attr)
					except KeyError:
						capture_data[node] = {attr: mc.getAttr(node+"."+attr)}
					except (RuntimeError, ValueError) as e:
						if not self.suppress_warnings():
							mc.warning(str(e))

		self.store_attr(capture_id, capture_data)
		self.refresh_capture_ui()


	def store_attr(self, capture_id, capture_data):
		""" Serialize capture data dictionary as JSON and store in custom
			attribute.
		"""
		serialized_data = json.dumps(capture_data)
		attr_name = CAPTURE_ATTR_PREFIX + capture_id
		if not mc.attributeQuery(attr_name, node=self.root_set, exists=True):
			mc.addAttr(self.root_set, ln=attr_name, dt="string")
		mc.setAttr(self.root_set+"."+attr_name, serialized_data, type="string")


	def restore(self, attr_name):
		""" Restore from a captured state.
			TODO: Deal elegantly with the following errors when setting attributes:
			setAttr: '<attr>' is not a simple numeric attribute.  Its values must be set with a -type flag.
			setAttr: The attribute '<attr>' is a multi. Its values must be set individually.
		"""
		capture_data = json.loads(mc.getAttr(self.root_set+"."+attr_name))

		for node, attributes in capture_data.items():
			# print(type(attributes) == dict)
			if type(attributes) == dict:
				for attr, value in attributes.items():
					# print(node, attr, value)
					try:
						mc.setAttr(node+"."+attr, value)
					except RuntimeError as e:
						if not self.suppress_warnings():
							mc.warning(str(e))


	def rename(self, attr_name, new_name):
		""" Change the name of a capture.
			TODO: rename snapshot image file also
		"""
		# new_name = self.sender().text()

		if new_name == "":
			mc.warning("Please give the capture a valid name.")
			self.refresh_capture_ui()
			return

		new_attr_name = CAPTURE_ATTR_PREFIX + new_name
		# print(self.root_set+"."+attr_name, new_attr_name)
		try:
			mc.renameAttr(self.root_set+"."+attr_name, new_attr_name)
		except RuntimeError as e:
			mc.warning(str(e))

		self.refresh_capture_ui()


	def delete(self, attr_name):
		""" Delete a saved capture.
		"""
		try:
			capture_data = json.loads(mc.getAttr(self.root_set+"."+attr_name))
			mc.deleteAttr(self.root_set+"."+attr_name)
			if os.path.isfile(capture_data['snapshot']):
				os.remove(capture_data['snapshot'])

		except KeyError:
			pass

		except ValueError as e:
			mc.warning(str(e))

		self.refresh_capture_ui()


	def suppress_warnings(self):
		""" Get the value the 'Suppress warnings' checkbox and return a
			Boolean value.
		"""
		if self.ui.noWarnings_checkBox.checkState() == QtCore.Qt.Checked:
			return True
		else:
			return False


	def capture_list(self):
		""" Return a list with the names of existing captures.
		"""
		id_list = []

		capture_list = mc.listAttr(self.root_set, userDefined=True)
		if capture_list:
			for attr_name in capture_list:
				if attr_name.startswith(CAPTURE_ATTR_PREFIX):
					id_list.append(attr_name.replace(CAPTURE_ATTR_PREFIX, ""))

		# print(id_list)
		return id_list


	def get_snapshot_cam(self):
		""" Return a camera to snapshot from. This will be the first camera
			found in the capture set. If the set contains no cameras, return
			'persp'.
		"""
		cameras = []

		set_contents = mc.sets(self.root_set, q=True)
		if set_contents:
			for node in set_contents:
				shapes = mc.listRelatives(node, shapes=True)
				if shapes:
					for shape in shapes:
						if mc.nodeType(shape) == 'camera':
							cameras.append(node)

		if not cameras:
			cameras.append('persp')

		cameras.sort()
		# print(cameras)
		return cameras


	def get_snapshot_res(
		self, 
		max_w=SNAPSHOT_MAX_RES[0], 
		max_h=SNAPSHOT_MAX_RES[1]):
		""" Return the max resolution for snapshots, as a 2 element list.
		"""
		w = mc.getAttr("defaultResolution.w")
		h = mc.getAttr("defaultResolution.h")
		ratio = float(w)/float(h)

		if w > max_w:
			w = max_w
			h = int(math.ceil(w/ratio))

		if h > max_h:
			h = max_h
			w = int(math.ceil(h*ratio))

		# print(w, h)
		return [w, h]


	def get_output_dir(self):
		""" Return the output directory for capture snapshots and data.
		"""
		playblasts_dir = os.getenv('IC_MAYA_PLAYBLASTS_DIR', os.path.join(mc.workspace(q=True, active=True), 'playblasts'))
		scene_name =  os.path.splitext(mc.file(q=True, sceneName=True, shortName=True))[0]
		if not scene_name:
			scene_name = 'untitled'
		output_dir = os.path.normpath(os.path.join(playblasts_dir, 'sceneCapture', scene_name))

		# Create dir to store shapshots if it doesn't exist
		if not os.path.isdir(output_dir):
			os.makedirs(output_dir)

		# print(output_dir)
		return(output_dir)


	def snapshot(self, name):
		""" Take a snapshot of the current viewport panel.
			Uses preview_maya.py module, shared with Preview.
		"""
		pb_args = {}
		pb_args['outputDir'] = self.get_output_dir()
		pb_args['outputFile'] = name
		pb_args['outputFormat'] = "JPEG sequence"
		pb_args['activeView'] = "modelPanel4"  # FIX
		pb_args['camera'] = self.ui.snapCam_comboBox.currentText() #self.get_snapshot_cam()
		pb_args['res'] = self.get_snapshot_res()
		pb_args['frRange'] = [mc.currentTime(q=1), mc.currentTime(q=1)]
		pb_args['offscreen'] = True
		pb_args['noSelect'] = True
		pb_args['guides'] = False
		pb_args['burnin'] = False
		pb_args['interruptible'] = False

		snapshot = preview_maya.Preview(**pb_args)
		result = snapshot.playblast_()
		# print(result)

		if result[0] == "Completed":
			return result[1]
		else:
			return None


	def import_json(self):
		""" Import capture data from JSON file.
		"""
		startingDir = self.get_output_dir()
		fileFilter = "JSON Files (*.json)"
		fileName = QtWidgets.QFileDialog.getOpenFileName(
			self, self.tr("Import JSON"), startingDir, fileFilter)

		try:
			result = fileName[0]
		except IndexError:
			result = None

		if result:
			with open(result, 'r') as f:
				import_data = json.load(f)

			for capture_id in import_data.keys():
				if capture_id not in self.capture_list():
					self.store_attr(capture_id, import_data[capture_id])
				else:
					if self.confirm_overwite(capture_id) == 'Yes':
						self.store_attr(capture_id, import_data[capture_id])

			self.refresh_capture_ui()


	def export_json(self):
		""" Export capture data to JSON file.
		"""
		startingDir = self.get_output_dir()
		fileFilter = "JSON Files (*.json)"
		fileName = QtWidgets.QFileDialog.getSaveFileName(
			self, self.tr("Export JSON"), startingDir, fileFilter)

		try:
			result = fileName[0]
		except IndexError:
			result = None

		if result:
			export_data = {}
			for capture_id in self.capture_list():
				attr_name = CAPTURE_ATTR_PREFIX + capture_id
				export_data[capture_id] = json.loads(mc.getAttr(self.root_set+"."+attr_name))

			with open(result, 'w') as f:
				json.dump(export_data, f, indent=4, sort_keys=True)


	def delete_data(self):
		""" Delete external save data (snapshots, exported JSON data, etc.)
		"""
		data_dir = self.get_output_dir()
		if 'Yes' == mc.confirmDialog(
			title='Delete Data', 
			message='The following folder and its contents will be deleted:\n%s\nAre you sure?' % data_dir, 
			button=['Yes', 'No'], 
			defaultButton='Yes', 
			cancelButton='No'):
			shutil.rmtree(data_dir)
			self.refresh_capture_ui()


	def confirm_overwite(self, capture_id):
		""" Confirm overwite of existing capture.
		"""
		return mc.confirmDialog(
			title='Capture Exists', 
			message='A capture named %s already exists. Do you want to overwrite it?' % capture_id, 
			button=['Yes', 'No'], 
			defaultButton='Yes', 
			cancelButton='No')


	# def width_edit(self):
	# 	""" 
	# 	"""
	# 	print("width_edit")

	# 	# name_to_change = findNode("renderwidth").getChild(0)
	# 	# if name_to_change.isValid():
	# 	# 	name = self.ui.width.text()  # TODO: change to QSpinBox
	# 	# 	name_to_change.setName(name)


	# def height_edit(self):
	# 	""" 
	# 	"""
	# 	print("height_edit")

	# 	# name_to_change = findNode("renderheight").getChild(0)
	# 	# if name_to_change.isValid():
	# 	# 	name = self.ui.height.text()  # TODO: change to QSpinBox
	# 	# 	name_to_change.setName(name)


	# def path_edit(self):
	# 	""" 
	# 	"""
	# 	print("path_edit")

	# 	# name_to_change = findNode("path").getChild(0)
	# 	# if name_to_change.isValid():
	# 	# 	name = self.ui.path_lineEdit.text()
	# 	# 	name_to_change.setName(name)


	# def render(self):
	# 	""" Render the selected snapshots.
	# 	"""
	# 	print("render")

	# 	width = self.ui.width_spinBox.value()
	# 	height = self.ui.height_spinBox.value()
	# 	path = self.ui.path_lineEdit.text()
	# 	extension = "."+self.ui.filetype_comboBox.currentText()

	# 	for i in range(1, 21):
	# 		render_checkBox = self.ui.captured_sets_box.findChild(QtWidgets.QCheckBox, "render_set%d" % i)
	# 		set_toolButton = self.ui.captured_sets_box.findChild(QtWidgets.QToolButton, "set%d" % i)

	# 		if render_checkBox.checkState() == QtCore.Qt.Checked and set_toolButton.isEnabled():
	# 			self.restore(i)

	# 			name_lineEdit = self.ui.captured_sets_box.findChild(QtWidgets.QLineEdit, "captured_name_%d" % i)
	# 			filename = path+name_lineEdit.text()+extension
	# 			if extension == ".jpg":
	# 				print("createSnapshot(%s, %d, %d, 2, 0)" % (filename, width, height))
	# 			else:
	# 				print("createSnapshot(%s, %d, %d, 2, 1)" % (filename, width, height))

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
				allowedArea=allowed_areas)
		else:
			sceneCaptureUI.display(**kwargs)  # Show the UI

	else:
		try:
			session.sceneCaptureUI.display(**kwargs)

		except:
			_maya_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
			session.sceneCaptureUI = SceneCaptureUI(parent=_maya_main_window())
			session.sceneCaptureUI.display(**kwargs)
