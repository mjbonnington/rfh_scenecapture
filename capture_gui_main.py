
## v.02

def init_me():
	
	if findNode("sceneCapture_DONT_DELETE").isValid() == false:
		root_set=createNode("Group", "sceneCapture_DONT_DELETE") # einsortieren in system
		roots=createNode("Group", "root_nodes", root_set)
		captures=createNode("Group", "capture_nodes", root_set)
		settings=createNode("Group", "rendersettings", root_set)
		width=createNode("Group", "renderwidth", settings)
		createNode("Group", "2000", width)
		height=createNode("Group", "renderheight", settings)
		createNode("Group", "1500", height)
		path=createNode("Group", "path", settings)
		createNode("Group", "c:/", path)



	else:
		for i in range(20):
			if findNode("sceneCap_rootNode_"+str(i+1)).isValid():
				name=findNode("sceneCap_rootNode_"+str(i+1)).getChild(0).getName()
				name=name.replace("_GEOM", "")
				lineedit = findQObject(root_nodes, "root"+str(i+1))
				lineedit.setProperty("text", name)
			if findNode("sceneCap_Slot_"+str(i+1)).isValid():
				name=findNode("sceneCap_Slot_"+str(i+1)).getChild(0).getName()
				findQObject(captured_sets, "set"+str(i+1)).setProperty("enabled", "true")
				findQObject(captured_sets, "captured_name_"+str(i+1)).setProperty("enabled", "true")
				findQObject(captured_sets, "recap"+str(i+1)).setProperty("enabled", "true")
				findQObject(captured_sets, "del"+str(i+1)).setProperty("enabled", "true")
				lineedit = findQObject(captured_sets, "captured_name_"+str(i+1))
				lineedit.setProperty("text", name)
		
		if findNode("renderwidth").getChild(0).isValid():
			width=findNode("renderwidth").getChild(0).getName()
			lineedit = findQObject(render_box, "width")
			lineedit.setProperty("text", width)

		if findNode("renderheight").getChild(0).isValid():
			height=findNode("renderheight").getChild(0).getName()
			lineedit = findQObject(render_box, "height")
			lineedit.setProperty("text", height)

		if findNode("path").getChild(0).isValid():
			path=findNode("path").getChild(0).getName()
			lineedit = findQObject(render_box, "path")
			lineedit.setProperty("text", path)


	if findNode("rendersettings").isValid() == false:
		print "settings nachtragen"
		root_set=findNode("sceneCapture_DONT_DELETE") # einsortieren in system
		settings=createNode("Group", "rendersettings", root_set)
		width=createNode("Group", "renderwidth", settings)
		createNode("Group", "2000", width)
		height=createNode("Group", "renderheight", settings)
		createNode("Group", "1500", height)
		path=createNode("Group", "path", settings)
		createNode("Group", "c:/", path)
			
				
		

	
def pick_root(slot):

	node=getSelectedNode()
	

	if node.isValid():
		node=getSelectedNode().getName()
		
		lineedit = findQObject(root_nodes, "root"+str(slot))
		lineedit.setProperty("text", node)
		roots=findNode("root_nodes")
		deleteNodes(findNodes("sceneCap_rootNode_" +str(slot)), false)
		root=createNode("Group", "sceneCap_rootNode_" +str(slot), roots)
		createNode("Group", node+"_GEOM", root)

		for i in range(20):
			#print "slot: " + str(i+1)
			if findNode("sceneCap_Slot_" + str(i+1)).isValid():
				#print "changing slot: " + str(i+1)
				slot_to_change=findNode("sceneCap_Slot_" + str(i+1))
				for j in range(10):
					root_to_change=slot_to_change.getChild(j+1)
					if root_to_change.isValid():
						#print "rootname: " + root_to_change.getName()
						if root_to_change.getName()==("root" + str(slot)):
							#print root_to_change.getChild(0).getName()
							root_to_change.getChild(0).setName("GEOMNAME_"+node)

	else:

		print "ERROR: nothing selected"

	
	
def capture():
	name=findQObject(capture_name, "capture_name").getProperty("text")
	      
	print "capture set with name: " + name
	enabled=1
	i=0
	# double name ausschliessen:
	captured_names=[]
	for i in range(20):
		if findQObject(captured_sets, "set"+str(i)).getProperty("enabled") == "true":
			captured_names.append(findQObject(captured_sets, "captured_name_"+str(i)).getProperty("text"))

	

	i=0

	while enabled==1:
		i+=1
		print "suche leeren slot" + str(i)
		if findQObject(captured_sets, "set"+str(i)).getProperty("enabled") == "false":
			print "slot " + str(i) + "inaktiv"
			findQObject(captured_sets, "set"+str(i)).setProperty("enabled", "true")
			
			findQObject(captured_sets, "captured_name_"+str(i)).setProperty("enabled", "true")
			findQObject(captured_sets, "recap"+str(i)).setProperty("enabled", "true")
			findQObject(captured_sets, "del"+str(i)).setProperty("enabled", "true")
			if name=="":
				name="unnamed"+str(i)
			#elif "_" in name:
			#	name=name+str(i)
			if name in captured_names:
				name=name+"_v"+str(i)
			lineedit = findQObject(captured_sets, "captured_name_"+str(i))
			lineedit.setProperty("text", name)
			enabled=0
			capture_nodes(i, name)
		if i==20:
			enabled=0
			print "KEIN SLOT FREI"


def capture_nodes(slot, name):

	roots=findNode("capture_nodes")
	slot=createNode("Group", "sceneCap_Slot_" +str(slot), roots)
	slotname=createNode("Group", name, slot)
	addViewPoint("SceneCap_" + name)

	for i in range(10):
		current_node=findQObject(root_nodes, ("root"+str(i+1)) ).getProperty("text")

		if len(current_node) > 0:
			print "servus"
			rootnode=createNode("Group", "root"+str(i+1), slot)
			slotroot=createNode("Group","GEOMNAME_"+current_node, rootnode)
			isactive=findNode(current_node).getActive()
			if not isactive:
				createNode("Group","unvis",slotroot)

			coord=getTransformNodeTranslation(findNode(current_node),false)
			createNode("Group",str(coord.x()), rootnode)
			createNode("Group",str(coord.y()), rootnode)
			createNode("Group",str(coord.z()), rootnode)
			coord2=getTransformNodeRotation(findNode(current_node))
			createNode("Group",str(coord2.x()), rootnode)
			createNode("Group",str(coord2.y()), rootnode)
			createNode("Group",str(coord2.z()), rootnode)
			coord3=getTransformNodeScale(findNode(current_node))
			createNode("Group",str(coord3.x()), rootnode)
			createNode("Group",str(coord3.y()), rootnode)
			createNode("Group",str(coord3.z()), rootnode)
			
			if findNode(current_node).getChild(0).getChild(1).getChild(0).getName()=="WHEEL_FR_TURN":
				print "capture WHEEL_FR_TURN"
				tirerotation=getTransformNodeRotation(findNode(current_node).getChild(0).getChild(1).getChild(0))                                
				createNode("Group",str(tirerotation.x()), rootnode)
				createNode("Group",str(tirerotation.y()), rootnode)
				createNode("Group",str(tirerotation.z()), rootnode)
			if findNode(current_node).getChild(0).getChild(1).getChild(1).getName()=="WHEEL_FL_TURN":
				print "capture WHEEL_FL_TURN"
				tirerotation=getTransformNodeRotation(findNode(current_node).getChild(0).getChild(1).getChild(1))
				createNode("Group",str(tirerotation.x()), rootnode)
				createNode("Group",str(tirerotation.y()), rootnode)
				createNode("Group",str(tirerotation.z()), rootnode)
			

def recapture_nodes(slot):
	deselectAll()
	roots=findNode("capture_nodes")
	name=findNode("sceneCap_Slot_"+str(slot)).getChild(0).getName()
	
	deleteNodes(findNodes("sceneCap_Slot_" +str(slot)), false)
	removeViewPoint("SceneCap_" + name)
	
	slot=createNode("Group", "sceneCap_Slot_" +str(slot), roots)
	slotname=createNode("Group", name, slot)
	addViewPoint("SceneCap_" + name)
	

	for i in range(10):
		current_node=findQObject(root_nodes, ("root"+str(i+1)) ).getProperty("text")

		if len(current_node) > 0:
			print "recapture" + current_node
			rootnode=createNode("Group", "root"+str(i+1), slot)
			slotroot=createNode("Group","GEOMNAME_"+current_node, rootnode)
			isactive=findNode(current_node).getActive()
			if not isactive:
				createNode("Group","unvis",slotroot)
			coord=getTransformNodeTranslation(findNode(current_node),false)
			createNode("Group",str(coord.x()), rootnode)
			createNode("Group",str(coord.y()), rootnode)
			createNode("Group",str(coord.z()), rootnode)
			coord2=getTransformNodeRotation(findNode(current_node))
			createNode("Group",str(coord2.x()), rootnode)
			createNode("Group",str(coord2.y()), rootnode)
			createNode("Group",str(coord2.z()), rootnode)
			coord3=getTransformNodeScale(findNode(current_node))
			createNode("Group",str(coord3.x()), rootnode)
			createNode("Group",str(coord3.y()), rootnode)
			createNode("Group",str(coord3.z()), rootnode)
			
			if findNode(current_node).getChild(0).getChild(1).getChild(0).getName()=="WHEEL_FR_TURN":
				print "capture WHEEL_FR_TURN"
				tirerotation=getTransformNodeRotation(findNode(current_node).getChild(0).getChild(1).getChild(0))                                
				createNode("Group",str(tirerotation.x()), rootnode)
				createNode("Group",str(tirerotation.y()), rootnode)
				createNode("Group",str(tirerotation.z()), rootnode)
			if findNode(current_node).getChild(0).getChild(1).getChild(1).getName()=="WHEEL_FL_TURN":
				print "capture WHEEL_FL_TURN"
				tirerotation=getTransformNodeRotation(findNode(current_node).getChild(0).getChild(1).getChild(1))
				createNode("Group",str(tirerotation.x()), rootnode)
				createNode("Group",str(tirerotation.y()), rootnode)
				createNode("Group",str(tirerotation.z()), rootnode)
			isactive=findNode(current_node).getActive()
			if not isactive:
				createNode("Group","unvis",rootnode)

def set_nodes(slot):

	root=findNode("sceneCap_Slot_"+str(slot))
	num_roots=root.getNChildren()
	#print num_roots
	print "SET Slot" + str(slot)

	name="SceneCap_"+findNode("sceneCap_Slot_" +str(slot)).getChild(0).getName()
	jumpViewPoint(name)
	print name

	for i in range(num_roots-1):
		geom_name=root.getChild(i+1).getChild(0).getName()
		geom_name=geom_name.replace("GEOMNAME_", "")
		node=findNode(geom_name)
		print "moveNode: " + geom_name
		if node.isValid():
			if root.getChild(i+1).getChild(0).getChild(0).getName()=="unvis":
				node.setActive(0)
			else:
				node.setActive(1)

			node.setTranslation(float(root.getChild(i+1).getChild(1).getName()), float(root.getChild(i+1).getChild(2).getName()), float (root.getChild(i+1).getChild(3).getName()))
			node.setRotation(float(root.getChild(i+1).getChild(4).getName()), float(root.getChild(i+1).getChild(5).getName()), float (root.getChild(i+1).getChild(6).getName()))
			node.setScale(float(root.getChild(i+1).getChild(7).getName()), float(root.getChild(i+1).getChild(8).getName()), float (root.getChild(i+1).getChild(9).getName()))
			if node.getChild(0).getChild(1).getChild(0).getName()=="WHEEL_FR_TURN":
				print "set WHEEL_FR_TURN"
				tirenode=node.getChild(0).getChild(1).getChild(0)
				if root.getChild(i+1).getChild(10) and root.getChild(i+1).getChild(11) and root.getChild(i+1).getChild(12):
					print "daten vorhanden"
					tirenode.setRotation(float(root.getChild(i+1).getChild(10).getName()), float(root.getChild(i+1).getChild(11).getName()), float (root.getChild(i+1).getChild(12).getName()))
			if node.getChild(0).getChild(1).getChild(1).getName()=="WHEEL_FL_TURN":
				print "set WHEEL_FL_TURN"
				tirenode=node.getChild(0).getChild(1).getChild(1)
				if root.getChild(i+1).getChild(13) and root.getChild(i+1).getChild(14) and root.getChild(i+1).getChild(15):
					print "daten vorhanden"
					tirenode.setRotation(float(root.getChild(i+1).getChild(13).getName()), float(root.getChild(i+1).getChild(14).getName()), float (root.getChild(i+1).getChild(15).getName()))
				
				

       
			
def swap():

   
	print "Swap"
	
	node1=findNode(findQObject(swap_nodes, "swap1").getProperty("text"))
	node2=findNode(findQObject(swap_nodes, "swap2").getProperty("text"))

	if node1.isValid() and node2.isValid():
		
		coord1t=getTransformNodeTranslation(node1,true)
		coord1r=getTransformNodeRotation(node1)
		coord1s=getTransformNodeScale(node1)

		coord2t=getTransformNodeTranslation(node2,true)
		coord2r=getTransformNodeRotation(node2)
		coord2s=getTransformNodeScale(node2)

		node1.setTranslation(coord2t.x(),coord2t.y(),coord2t.z())
		node1.setRotation(coord2r.x(),coord2r.y(),coord2r.z())
		node1.setScale(coord2s.x(),coord2s.y(),coord2s.z())

		node2.setTranslation(coord1t.x(),coord1t.y(),coord1t.z())
		node2.setRotation(coord1r.x(),coord1r.y(),coord1r.z())
		node2.setScale(coord1s.x(),coord1s.y(),coord1s.z())

	
			
			
def pick_swap(slot):

	node=getSelectedNode()
	
	if node.isValid():
		node=getSelectedNode().getName()
		
		lineedit = findQObject(swap_nodes, "swap"+str(slot))
		lineedit.setProperty("text", node)
			
	
	

def delete(slot):
	print "delete"
	findQObject(captured_sets, "set"+str(slot)).setProperty("enabled", "false")
	findQObject(captured_sets, "captured_name_"+str(slot)).setProperty("enabled", "false")
	findQObject(captured_sets, "recap"+str(slot)).setProperty("enabled", "false")
	findQObject(captured_sets, "del"+str(slot)).setProperty("enabled", "false")
	lineedit = findQObject(captured_sets, "captured_name_"+str(slot))
	lineedit.setProperty("text", "")
	name=findNode("sceneCap_Slot_" +str(slot)).getChild(0).getName()

	deleteNodes(findNodes("sceneCap_Slot_" +str(slot)), false)
##        viewpoints=getViewpoints()
##        viewname="SceneCap_" + name
##        if viewname in viewpoints:
	removeViewPoint("SceneCap_" + name)




def text_edit(slot):
	
	
	slot_to_change=findNode("sceneCap_Slot_" + str(slot))
	
	
	if slot_to_change.isValid():

		
			
		name_to_change=slot_to_change.getChild(0)
		if name_to_change.isValid():
			print "slitti"
			viewpoint_name="SceneCap_" + slot_to_change.getChild(0).getName()
					       
			jumpViewPoint(viewpoint_name)
			removeViewPoint(viewpoint_name) 
			name=findQObject(captured_sets, "captured_name_"+str(slot)).getProperty("text")
			
			print name
			if name=="":
				name="unnamed"+str(slot)
			name_to_change.setName(name)
			addViewPoint("SceneCap_" + name)



def render():
	
	path=findQObject(render_box, "path").getProperty("text")
	width=int(findQObject(render_box, "width").getProperty("text"))
	height=int(findQObject(render_box, "height").getProperty("text"))

	if findQObject(render_box, "filetype").getProperty("currentIndex") == "0":
		extension=".jpg"
	else:
		extension=".exr"

	
	for i in range(20):
		
		if  findQObject(captured_sets, "render_set"+str(i+1)).getProperty("checked") == "true" and findQObject(captured_sets, "set"+str(i+1)).getProperty("enabled") == "true":
				set_nodes(i+1)
				
				file=path+findQObject(captured_sets, "captured_name_"+str(i+1)).getProperty("text")+extension
				if extension == ".jpg":
					createSnapshot(file,width,height,2,0)
				else:
					createSnapshot(file,width,height,2,1)
				

	

##        

## helper functions

def pick_root1():
    pick_root(1)
def pick_root2():
    pick_root(2)
def pick_root3():
    pick_root(3)
def pick_root4():
    pick_root(4)
def pick_root5():
    pick_root(5)
def pick_root6():
    pick_root(6)
def pick_root7():
    pick_root(7)
def pick_root8():
    pick_root(8)
def pick_root9():
    pick_root(9)
def pick_root10():
    pick_root(10)


def delete1():
	delete(1)
def delete2():
	delete(2)
def delete3():
	delete(3)
def delete4():
	delete(4)
def delete5():
	delete(5)
def delete6():
	delete(6)
def delete7():
	delete(7)
def delete8():
	delete(8)
def delete9():
	delete(9)
def delete10():
	delete(10)

def delete11():
	delete(11)
def delete12():
	delete(12)
def delete13():
	delete(13)
def delete14():
	delete(14)
def delete15():
	delete(15)
def delete16():
	delete(16)
def delete17():
	delete(17)
def delete18():
	delete(18)
def delete19():
	delete(19)
def delete20():
	delete(20)

def recap1():
	recapture_nodes(1)
def recap2():
	recapture_nodes(2)
def recap3():
	recapture_nodes(3)
def recap4():
	recapture_nodes(4)
def recap5():
	recapture_nodes(5)
def recap6():
	recapture_nodes(6)
def recap7():
	recapture_nodes(7)
def recap8():
	recapture_nodes(8)
def recap9():
	recapture_nodes(9)
def recap10():
	recapture_nodes(10)
def recap11():
	recapture_nodes(11)
def recap12():
	recapture_nodes(12)
def recap13():
	recapture_nodes(13)
def recap14():
	recapture_nodes(14)
def recap15():
	recapture_nodes(15)
def recap16():
	recapture_nodes(16)
def recap17():
	recapture_nodes(17)
def recap18():
	recapture_nodes(18)
def recap19():
	recapture_nodes(19)
def recap20():
	recapture_nodes(20)

def set1():
	set_nodes(1)
def set2():
	set_nodes(2)
def set3():
	set_nodes(3)
def set4():
	set_nodes(4)
def set5():
	set_nodes(5)
def set6():
	set_nodes(6)
def set7():
	set_nodes(7)
def set8():
	set_nodes(8)
def set9():
	set_nodes(9)
def set10():
	set_nodes(10)
def set11():
	set_nodes(11)
def set12():
	set_nodes(12)
def set13():
	set_nodes(13)
def set14():
	set_nodes(14)
def set15():
	set_nodes(15)
def set16():
	set_nodes(16)
def set17():
	set_nodes(17)
def set18():
	set_nodes(18)
def set19():
	set_nodes(19)
def set20():
	set_nodes(20)



def pick_swap1():
    pick_swap(1)
def pick_swap2():
    pick_swap(2)






def text_edit1():
	text_edit(1)

def text_edit2():
	text_edit(2)

def text_edit3():
	text_edit(3)

def text_edit4():
	text_edit(4)

def text_edit5():
	text_edit(5)

def text_edit6():
	text_edit(6)

def text_edit7():
	text_edit(7)

def text_edit8():
	text_edit(8)

def text_edit9():
	text_edit(9)

def text_edit10():
	text_edit(10)
def text_edit11():
	text_edit(11)

def text_edit12():
	text_edit(12)

def text_edit13():
	text_edit(13)

def text_edit14():
	text_edit(14)

def text_edit15():
	text_edit(15)

def text_edit16():
	text_edit(16)

def text_edit17():
	text_edit(17)

def text_edit18():
	text_edit(18)

def text_edit19():
	text_edit(19)

def text_edit20():
	text_edit(20)

 
## init widget

widget = vrWidget(script_path+"capture6slim.ui")
widget_root=widget.getQObject()
widget.setToolWindow(true)

capture_what=findQObject(widget_root, "capture_what_box")
captured_sets=findQObject(widget_root, "captured_sets_box")
capture_name=findQObject(widget_root, "name_box")
root_nodes=findQObject(widget_root, "root_box")
swap_nodes=findQObject(widget_root, "swap_box")
render_box=findQObject(widget_root, "render_box")                                


# connect buttons

widget.connect("capture_action", "clicked()", capture)



widget.connect("pick_root1", "clicked()", pick_root1)
widget.connect("pick_root2", "clicked()", pick_root2)
widget.connect("pick_root3", "clicked()", pick_root3)
widget.connect("pick_root4", "clicked()", pick_root4)
widget.connect("pick_root5", "clicked()", pick_root5)
widget.connect("pick_root6", "clicked()", pick_root6)
widget.connect("pick_root7", "clicked()", pick_root7)
widget.connect("pick_root8", "clicked()", pick_root8)
widget.connect("pick_root9", "clicked()", pick_root9)
widget.connect("pick_root10", "clicked()", pick_root10)


for i in range(1,21):
	command="widget.connect(\"del" +str(i)+ "\", \"clicked()\", delete" +str(i)+ ")"

	eval(command)
	command="widget.connect(\"recap" +str(i)+ "\", \"clicked()\", recap" +str(i)+ ")"

	eval(command)
	command="widget.connect(\"set" +str(i)+ "\", \"clicked()\", set" +str(i)+ ")"
	eval(command)
	command="widget.connect(\"captured_name_" +str(i)+ "\", \"returnPressed()\", text_edit" +str(i)+ ")"
	eval(command)




def width_edit():
	#widget_root=widget.getQObject()
	#render_box=findQObject(widget_root, "render_box") 
	
	name_to_change=findNode("renderwidth").getChild(0)
	if name_to_change.isValid():
	       
		name=findQObject(render_box, "width").getProperty("text")
		name_to_change.setName(name)

def height_edit():
	name_to_change=findNode("renderheight").getChild(0)
	if name_to_change.isValid():
		print "height change"
		name=findQObject(render_box, "height").getProperty("text")
		name_to_change.setName(name)
		
def path_edit():
	name_to_change=findNode("path").getChild(0)
	if name_to_change.isValid():
		name=findQObject(render_box, "path").getProperty("text")
		name_to_change.setName(name)


widget.connect("pick_swap1", "clicked()", pick_swap1)
widget.connect("pick_swap2", "clicked()", pick_swap2)
widget.connect("swap_nodes", "clicked()", swap)
widget.connect("render", "clicked()", render)

widget.connect("width" , "returnPressed()", width_edit)
widget.connect("height" , "returnPressed()", height_edit)
widget.connect("path" , "returnPressed()", path_edit)




print "sodele"
init_me()



