**Simulator Features**

**Scenes.** Infinite random playroom configuration, depends on the import asset classes. 

**Objects.** 500+ custom annotated household objects and kids playing toys across 50 different object classes. 

**Agent Types.** Support teacher and baby learning agent. 

**Actions.** 20+ actions that facilitate research in a wide range of interaction and navigation based embodied AI tasks.

**Images.** Render RGBD, Depth and Instance segmentation. We also provide a selection of different camera angles for rendering.

**Metadata.** After each step in the environment, there is a large amount of sensory and visual data will be available and saved.  

**Installation**


**With pip (Windows)**

-pip install XenosPlayRoomEnv==0.0.1

**Once you've installed download the simulator via:**

-from room import download

**Test via GUI controller:**

-from room import GUI

-GUI.exec_full(./filepath/demo.py)

**Run via command lines:**

-from room import Run

-Run.init(Stack.exe Path) #Initialize Simulator

-Run.addcharacter(str(character)) # "baby" or "teacher"

-Run.setcam(camnum) # 0 to 4

-Run.action(character,action,object) # In string 

-Run.close() #Close simulator


