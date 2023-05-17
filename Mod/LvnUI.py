import maya.cmds as cmds
import IndivPy.grpMaker as grpMaker
import IndivPy.connAttr as connAttr
import IndivPy.renamer as renamer
import IndivPy.snapper as snapper
import IndivPy.transAttr as transAttr
import IndivPy.cleaner as cleaner
import IndivPy.skinWeight as skinWeight
import IndivPy.paintMidVertWeight as paintMidVertWeight
import IndivPy.copyMirSDK as copyMirSDK
import IndivPy.attribute as attribute
import IndivPy.surfaceMaker as surfaceMaker
import IndivPy.ctrlMaker as ctrlMaker
import IndivPy.bindPreMatrix as bindPreMatrix
import IndivPy.constraints as constraints
import IndivPy.ctrlReadWrite as ctrlReadWrite
import IndivPy.joint as joint
import IndivPy.blendshape as blendshape
import IndivPy.ctrlSetup as ctrlSetup
import IndivPy.convKeyToSDK as convKeyToSDK
import IndivPy.detAttSDK as detAttSDK
import IndivPy.retrace as retrace
import IndivPy.eyelidSetup as eyelidSetup
import IndivPy.mayaSetting as mayaSetting
import Mod.reloadUI as reloadUI
import Mod.helpBox as helpBox
import Logs.allLogs as allLogs


class LvnUI(object):
    def __init__(self, *args):
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):    
        try:
            cmds.deleteUI("LvnDock")
        except:
            pass       
        try:
            cmds.deleteUI("Lvn")
        except:
            pass         
        LvnWin= cmds.window("Lvn", mb=1)
        cmds.columnLayout()
        self.m1= cmds.menu(l="Tools", to=1)
        cmds.menuItem(l="Blendshape", c=blendshape.Blendshape) 
        cmds.menuItem(l="Constraints", c=constraints.Constraints)  
        cmds.menuItem(l="Group Maker", c=grpMaker.GrpMaker) 
        cmds.menuItem(l="Snapper", c=snapper.Snapper) 
        cmds.menuItem(l="Surface Maker", c=surfaceMaker.SurfaceMaker)                  
        cmds.menuItem(l="Renamer", c=renamer.Renamer)     
        cmds.menuItem(d=1)
        cmds.menuItem(l="Cleaner", c=cleaner.Cleaner)
        self.m2= cmds.menu(l="ChannelBox", to=1)
        cmds.menuItem(l="Attributes", c=attribute.Attribute) 
        cmds.menuItem(l="Connect Attribute", c=connAttr.ConnAttr) 
        cmds.menuItem(l="Retrace", c=retrace.Retrace)    
        cmds.menuItem(l="Transfer Attribute", c=transAttr.TransAttr) 
        self.m3= cmds.menu(l="Shapes", to=1)    
        cmds.menuItem(l="Ctrl Maker", c=ctrlMaker.CtrlMaker)
        cmds.menuItem(l="Ctrl Read Write", c=ctrlReadWrite.CtrlReadWrite)  
        self.m4= cmds.menu(l="Set Driven", to=1)
        cmds.menuItem(l="Convert Key To SDK", c=convKeyToSDK.ConvKeyToSDK) 
        cmds.menuItem(l="Copy Mirror SDK", c=copyMirSDK.CopyMirSDK) 
        cmds.menuItem(l="Detach Attach SDK", c=detAttSDK.DetAttSDK)           
        self.m5= cmds.menu(l="Skinning", to=1)
        cmds.menuItem(l="Bind Pre Matrix", c=bindPreMatrix.BindPreMatrix)     
        cmds.menuItem(l="Skin Weight", c=skinWeight.SkinWeight ) 
        cmds.menuItem(l="Paint Middle Vertex Weight", c=paintMidVertWeight.PaintMidVertWeight)
        cmds.menuItem(l="Joint", c=joint.Joint)                  
        self.m6= cmds.menu(l="Rig", to=1)   
        cmds.menuItem(l="Ctrl Setup", c=ctrlSetup.CtrlSetup)  
        cmds.menuItem(l="Eyelid Setup", c=eyelidSetup.EyelidSetup)  
        self.m7= cmds.menu(l="Setting", to=1)
        cmds.menuItem(l="Maya Setting", c=mayaSetting.MayaSetting)  
        cmds.setParent("..", m=1)
        self.m8= cmds.menu(l="Help", to=1) 
        cmds.menuItem(l="Kill All", c=lambda x:self.killAll())
        cmds.menuItem(l="About", c=lambda x:self.about()) 
        cmds.menuItem(l="Logs", c=lambda x:self.logs())
        cmds.menuItem(l="Reload", c=reloadUI.reloadUI)   
        cmds.dockControl("LvnDock", l="LvnTools  v1.06", a="top", s=1, con=LvnWin, fcc=lambda:self.docking1())
        #cmds.showWindow(LvnWin)

        self.preSetting()

    def docking1(self):
        notDock= cmds.dockControl("LvnDock", q=1, fl=1)
        if notDock:
            cmds.dockControl("LvnDock", e=1, w=420)

    def preSetting(self):
        ver= cmds.about(v=1)
        if "matrixNodes" not in cmds.pluginInfo(q=1, ls=1):
            try:
                cmds.loadPlugin("C:/Program Files/Autodesk/Maya%s/bin/plug-ins/matrixNodes.mll"%ver)
            except:
                cmds.warning("Matrix plugin missing from <C:/Program Files/Autodesk/Maya%s/bin/plug-ins/matrixNodes.mll>"%ver)
        #turn on "track selection order" in pref        
        if cmds.selectPref(q=1, tso=1)==0:        
            cmds.selectPref(tso=1)

    def about(self):
        name="About"
        helpTxt="""
    DESCRIPTION
    ==============
        LvnTools contains multiple tools. Mainly for rigging task
        
        01. Group Maker
        02. Connect Attribute
        03. Renamer
        04. Snapper
        05. Transfer Attribute
        06. Cleaner
        07. Skin Weight
        08. Paint Middle Vertex Weight
        09. Copy Mirror Set Driven Key
        10. Attributes
        11. Surface Maker
        12. Ctrl Maker
        13. BindPreMatrix
        14. Constraints
        15. Shape Read Write
        16. Joint
        17. Blendshape
        18. Ctrl Setup
        19. Convert Key to Set Driven Key
        20. Detach Attach Set Driven Key
        21. Retrace
        22. Eyelid Setup
        23. Maya Setting

        (*According creation date)



    LICENSE
    ===========
        Copyright (c) 2018, Lih Haur Tan
        
        The BSD 2-clause license 
            - Free to use the script for any purposes
            - Allow to modify & distribute

        """
        self.helpBoxClass.helpBox1(name, helpTxt)

    def logs(self):
        name="Logs"
        helpTxt= allLogs.allLogs()
        self.helpBoxClass.helpBox1(name, helpTxt)
     
    def killAll(self):
        allUI=("grpM",
             "connA", 
             "ren", 
             "snp", 
             "un", 
             "ta", 
             "clean", 
             "sw", 
             "paintMVW", 
             "cmSDK", 
             "attrs", 
             "surfM", 
             "ctrlM", 
             "bpm", 
             "const",
             "ctrlRW",
             "jnts",
             "bs",
             "ctrlSet",
             "cktSDK",
             "daSDK",
             "retr",
             "eyelidSet",
             "mSet")  
        for item in allUI:
            try:
                cmds.deleteUI(item)
            except:
                pass       
     
        
if __name__=='__main__':
    LvnUI()

