import maya.cmds as mc

t_dict = {
	'translation': [0.0, 0.0, 0.0], 
	'rotation': [0.0, 0.0, 0.0], 
	'scale': [1.0, 1.0, 1.0]
	}

def copy_transform():
	last_selection = mc.ls(selection=True, transforms=True)[-1]
	t_dict['translation'] = mc.xform(last_selection, query=True, translation=True)
	t_dict['rotation'] = mc.xform(last_selection, query=True, rotation=True)
	t_dict['scale'] = mc.xform(last_selection, query=True, scale=True, relative=True)

def paste_transform():
	selection = mc.ls(selection=True, transforms=True)
	for item in selection:
		mc.xform(
			item, 
			translation=t_dict['translation'], 
			rotation=t_dict['rotation'], 
			scale=t_dict['scale'])

def print_transform():
	for key in ['translation', 'rotation', 'scale']:
		print("%s : %s" % (key, t_dict[key]))

def swap_transforms():
	""" Swap the positions of two objects.
	"""
	selection = mc.ls(selection=True, transforms=True)
	if len(selection) == 2:
		node1 = selection[0]
		node2 = selection[1]

		xformtmp = mc.createNode('transform', name="TEMP_SWAP_BUFFER", skipSelect=True)
		mc.matchTransform(xformtmp, node1)
		mc.matchTransform(node1, node2)
		mc.matchTransform(node2, xformtmp)
		mc.delete(xformtmp)

	else:
		mc.warning("Please select two transforms.")


shelfCommandMEL = '''
	shelfButton
		-enableCommandRepeat 1
		-flexibleWidthType 3
		-flexibleWidthValue 32
		-enable 1
		-width 41
		-height 34
		-manage 1
		-visible 1
		-preventOverride 0
		-annotation "Copy and paste transforms" 
		-enableBackground 0
		-backgroundColor 0 0 0 
		-highlightColor 0.321569 0.521569 0.65098 
		-align "center" 
		-label "Copy Transforms" 
		-labelOffset 0
		-rotation 0
		-flipX 0
		-flipY 0
		-useAlpha 1
		-font "plainLabelFont" 
		-imageOverlayLabel "xform" 
		-overlayLabelColor 0.8 0.8 0.8 
		-overlayLabelBackColor 0 0 0 0.5 
		-image "transformation.png" 
		-image1 "transformation.png" 
		-style "iconOnly" 
		-marginWidth 1
		-marginHeight 1
		-command "import mjbCopyTransform\nmjbCopyTransform.print_transform()\n" 
		-sourceType "python" 
		-doubleClickCommand "import mjbCopyTransform\nreload(mjbCopyTransform)\n" 
		-commandRepeatable 1
		-flat 1
		-mi "Copy transform from last selected object" ( "import mjbCopyTransform\nmjbCopyTransform.copy_transform()\n" )
		-mip 1
		-mi "Paste transform to selected object(s)" ( "import mjbCopyTransform\nmjbCopyTransform.paste_transform()\n" )
		-mip 1
		-mi "Swap positions of two objects" ( "import mjbCopyTransform\nmjbCopyTransform.swap_transforms()\n" )
		-mip 1
	;
'''