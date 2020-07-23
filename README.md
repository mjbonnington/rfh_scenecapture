# RFH Scene Capture

A tool for capturing object and camera layouts for stills.
Adapted from existing VRED tool.

## Setup

Copy the 'rfh_scenecapture' folder (or clone the Git repository) into a 
location from which Maya can run scripts, 
e.g. C:\Users\<USERNAME>\Documents\maya\scripts (Windows)

Run in Maya with the following code, or add to a shelf:

	from rfh_scenecapture import scenecapture_maya
	scenecapture_maya.run_maya()

The UI can also be docked, with either:

	scenecapture_maya.run_maya(dock='left')

	scenecapture_maya.run_maya(dock='right')

## Usage

This tool captures snapshots which store the state of certain nodes in the 
scene.

On the first run, a set named 'sceneCapture_set1' will be created containing 
the current selection. Choose what to capture by adding or removing objects 
from this set. All keyable attributes of any transform or shape nodes will be 
captured.

A thumbnail image preview of the capture will be stored in the 
'playblasts/sceneCapture/<Scene>' subfolder of the current Maya project. If 
there is a camera in the set, this will be used for snaphots. If there is 
more than one camera, it can be selected from the options on the Setup tab. 
If the set contains no cameras, the snapshot cam will default to 'persp'. The 
image dimensions set in the Render Globals will be used.
