import maya.cmds as cmds
import maya.mel as mel
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox
from functools import partial


class PaintMidVertWeight(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()


    def win(self):
        try:
            cmds.deleteUI("paintMVW")
        except:
            pass
        cmds.window("paintMVW", mb=1)        
        cmds.window("paintMVW", e=1, t="Paint Middle Vertex Weight", s=1, wh=(380,330))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on PaintMiddleVertexWeight", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload PaintMiddleVertexWeight", c=lambda x:self.reloadSub())   
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Paint")
        form1= cmds.formLayout(nd=100, p=column1)
        self.om= cmds.optionMenuGrp(l="Method :", cw2=(50,10), cc=lambda x:self.om1())    
        cmds.menuItem(label="Mirror")
        cmds.menuItem(label="Split")
        self.txtSear= cmds.textFieldGrp(l="Search :", tx="L", cw2=(40,40))
        self.txtRepl= cmds.textFieldGrp(l="Replace :", tx="R", cw2=(50,40))    
        sep1= cmds.separator(h=5, st="in") 
        self.txtVer= cmds.textFieldButtonGrp(l="Vertex :", adj=2, cw3=(45,10,100), bl="  Grab  ", bc=lambda :self.grabVert())     
        self.txtJnt= cmds.textFieldButtonGrp(l="Joint :", adj=2, cw3=(45,10,100),  pht="<Right click>", bl="  Set All Joint  ", bc=lambda :self.setAllJoint(1))     
        self.popJnt= cmds.popupMenu(p=self.txtJnt)
        sep2= cmds.separator(h=5, st="in")
        self.txtUnlock= cmds.textFieldButtonGrp(l="Unlock :", adj=2, cw3=(45,10,100),  pht="<Right click>", bl="  Set All Joint  ", bc=lambda :self.setAllJoint(2))     
        self.popUnlockJnt= cmds.popupMenu(p=self.txtUnlock)
        b1= cmds.button(l="Mirror/Split Weight", c=lambda x:self.msWeight())
        b2= cmds.button(l="Select Vertex", c=lambda x:self.selectVertex())
        cmds.formLayout(form1, e=1,
                                af=[(self.om, "top", 0),
                                    (self.txtSear, "top", 0),
                                    (self.txtRepl, "top", 0),
                                    (sep1, "top", 28),
                                    (self.txtVer, "top", 45),
                                    (self.txtJnt, "top", 91),
                                    (sep2, "top", 76),
                                    (self.txtUnlock, "top", 117),
                                    (b1, "top", 150),
                                    (b2, "top", 176)],
                                ap=[(self.om, "left", 0, 0),
                                    (self.om, "right", 0, 100),
                                    (self.txtSear, "right", 100, 100),
                                    (self.txtRepl, "right", 0, 100),
                                    (sep1, "left", 0, 0),
                                    (sep1, "right", 0, 100),
                                    (self.txtVer, "left", 0, 0),
                                    (self.txtVer, "right", 0, 100),
                                    (self.txtJnt, "left", 0, 0),
                                    (self.txtJnt, "right", 0, 100),
                                    (sep2, "left", 0, 0),
                                    (sep2, "right", 0, 100),                                    
                                    (self.txtUnlock, "left", 0, 0),
                                    (self.txtUnlock, "right", 0, 100),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 100),
                                    (b2, "left", 0, 0),
                                    (b2, "right", 0, 100)]) 
        cmds.setFocus(cmds.text(l=""))  
        cmds.showWindow("paintMVW")       
    
    def defi(self):   
        self.sear= cmds.textFieldGrp(self.txtSear, tx=1, q=1)   
        self.repl= cmds.textFieldGrp(self.txtRepl, tx=1, q=1)
        self.vert= cmds.textFieldButtonGrp(self.txtVer, tx=1, q=1)
        self.obj = self.vert.split(".")[0]
        self.skinClusterName= mel.eval("findRelatedSkinCluster %s"%self.obj)  
        self.allJnt= ", ".join(cmds.skinCluster(self.obj, inf=1, q=1))
        self.jnt= cmds.textFieldGrp(self.txtJnt, tx=1, q=1)
        self.unlock= cmds.textFieldGrp(self.txtUnlock, tx=1, q=1)

    def om1(self):
        if cmds.optionMenuGrp(self.om, q=1, sl=1)==1: 
            cmds.textFieldGrp(self.txtUnlock, e=1, en=1)
        else:
            cmds.textFieldGrp(self.txtUnlock, e=1, en=0)

    def grabVert(self):
        obj= cmds.ls(sl=1, fl=1)
        testVertExist, testJntExist, testJntNotInInf= 1,1,1
        tempObj= []
        if obj:
            for item in obj:
                if ".vtx" not in item:
                    testVertExist= []  
                else:
                    if tempObj:
                        if tempObj!= item.split(".")[0]:
                            testJntExist=[]
                    else:
                        tempObj= item.split(".")[0]
        else:
            testVertExist= []
        if testVertExist:
            if testJntExist:
                if mel.eval("findRelatedSkinCluster %s"%tempObj)=="":
                    testJntNotInInf=[]    
                if testJntNotInInf:
                    cmds.textFieldButtonGrp(self.txtVer, e=1, tx=", ".join(obj))       
                    self.defi()
                    self.popMain()
                    #cmds.textFieldGrp(self.txtJnt, e=1, tx="")
                else:
                    cmds.warning("Please select a VERTEX from a SKINNED object")
            else:
                cmds.warning("Please select VERTEX from the SAME object")
        else:
            cmds.warning("Please select at least 1 VERTEX")  

    def setAllJoint(self, meth):
        if cmds.textFieldButtonGrp(self.txtVer, tx=1, q=1):
            try:
                if self.vertJnt:
                    if meth==1:
                        cmds.textFieldButtonGrp(self.txtJnt, e=1, tx=", ".join(self.vertJnt))  
                    elif meth==2:
                        cmds.textFieldButtonGrp(self.txtUnlock, e=1, tx=", ".join(self.vertJnt)) 
            except:
                cmds.warning("<Vertex> textfield contain non skinned vertex, please redo")
        else:
            cmds.warning("<Vertex> textfield is empty!")

    def popMain(self):
        self.defi()
        self.vertJnt= cmds.skinPercent(self.skinClusterName, self.vert.split(", "), q=1, t=None, ib=0.001)
        cmds.popupMenu(self.popJnt, e=1, dai=1)
        cmds.popupMenu(self.popUnlockJnt, e=1, dai=1)        
        #using partial because lambda doesnt really work under loop
        for item in sorted(self.vertJnt):   
            cmds.menuItem("%s"%item, c=partial(self.subPop, item, 1, self.txtJnt), p=self.popJnt)   
            cmds.menuItem("%s"%item, c=partial(self.subPop, item, 2, self.txtUnlock), p=self.popUnlockJnt)  

    def subPop(self, newJnt, meth, txtJnt, *args):   
        #Doesnt really need "empty" arguement but partial somehow need it under class? 
        if meth==1:
            allJnt= cmds.textFieldGrp(self.txtJnt, tx=1, q=1)
            txtJnt= self.txtJnt 
        elif meth==2:
            allJnt= cmds.textFieldGrp(self.txtUnlock, tx=1, q=1)
            txtJnt= self.txtUnlock
        if allJnt:  
            if newJnt not in allJnt:
                cmds.textFieldGrp(txtJnt, e=1,tx="%s, %s"%(allJnt,newJnt))            
        else:
            cmds.textFieldGrp(txtJnt, e=1,tx="%s"%(newJnt)) 

    def msWeight(self):
        self.defi() 
        testVertExist, testJntExist, testJntNotInInf, testUnlockJntExist, conti1= 1,1,1,1,1
        if cmds.optionMenuGrp(self.om, q=1, sl=1)==1 and self.unlock=="":
            cmds.warning("Please input the <Unlock> textfield")
        else:
            for item in self.vert.split(", "):
                if cmds.objExists(item)==0:
                    testVertExist= []
            for thing in self.allJnt.split(", "):
                if cmds.objExists(thing)==0:
                    testJntExist= []                
            if testVertExist:
                if testJntExist:
                    conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(self.jnt.split(", "), self.sear, self.repl)
                    if conti:
                        mirJnt= []
                        for jnt in self.jnt.split(", "):
                            if jnt.replace(self.sear, self.repl) not in self.allJnt.split(", "):
                                testJntNotInInf=[]
                                mirJnt.append(jnt.replace(self.sear, self.repl))
                        if testJntNotInInf==[]:
                            conti1= self.dialogClass.printingDialog(mirJnt, "< %s > Joints are not the influence for this object"%len(mirJnt))
                        if conti1:

                            #Mirror Weight
                            if cmds.optionMenuGrp(self.om, q=1, sl=1)==1: 
                                for unlo in self.unlock.split(", "):
                                    if cmds.objExists(unlo)==False:
                                        testUnlockJntExist= []
                                if testUnlockJntExist:
                                    self.uiStuffClass.loadingBar(1, len(self.vert.split(", ")))
                                    for jnt in self.allJnt.split(", "): 
                                        if jnt not in self.unlock.split(", "):
                                            cmds.setAttr("%s.liw"%jnt, 1)
                                        else:         
                                            cmds.setAttr("%s.liw"%jnt, 0)
                                    for item in self.vert.split(", "): 
                                        for stuff in self.jnt.split(", "):
                                            try:
                                                val= cmds.skinPercent(self.skinClusterName, item, t=stuff, q=1 )
                                                cmds.skinPercent(self.skinClusterName, item, tv=((stuff.replace(self.sear, self.repl), val)))
                                            except:
                                                pass
                                        self.uiStuffClass.loadingBar(2)
                                    self.uiStuffClass.loadingBar(3)
                                else:
                                    cmds.warning("One of the object in UNLOCK texfield does not exist")
                            
                            #Split Weight
                            else:
                                self.uiStuffClass.loadingBar(1, len(self.vert.split(", ")))
                                for jnt in self.allJnt.split(", "):
                                    if jnt not in self.jnt.split(", "):
                                        cmds.setAttr("%s.liw"%jnt, 1)
                                    else:
                                        cmds.setAttr("%s.liw"%jnt, 0)    
                                for item in self.vert.split(", "):
                                    for stuff in self.jnt.split(", "):
                                        try:
                                            val1= cmds.skinPercent(self.skinClusterName, item, t=stuff, q=1)
                                            val2= cmds.skinPercent(self.skinClusterName, item, t=stuff.replace(self.sear,self.repl), q=1)
                                            cmds.skinPercent(self.skinClusterName, item, tv=((stuff.replace(self.sear,self.repl), (val1+val2)/2)))
                                        except:
                                            pass
                                    self.uiStuffClass.loadingBar(2)
                                self.uiStuffClass.loadingBar(3)
                else:
                    cmds.warning("One of the joint in JOINT texfield does not exist")
            else:
                cmds.warning("One of the vertex in VERTEX texfield does not exist")

    def selectVertex(self):
        vert= cmds.textFieldButtonGrp(self.txtVer, tx=1, q=1)
        testVertExist= 1
        if vert:
            for item in vert.split(", "):
                if cmds.objExists(item)==False:
                    testVertExist= []
            if testVertExist:
                self.uiStuffClass.loadingBar(1, 2)
                self.uiStuffClass.loadingBar(2)
                cmds.select(vert.split(", "), r=1)
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("One of the vertex in VERTEX texfield does not exist")
        else:
            cmds.warning("VERTEX textField is empty")

    def helps(self):
        name="Help On PaintMiddleVertexWeight"
        helpTxt="""
        - To fix paintweight for the middle vertex of the object (along the center grid) that are not properly mirror to the other side
        (* Eg. clav_L moving middle vertex but clav_R are not)



        1. Mirror
        ===========
            - Mirror whatever weight from one side to another
            (*eg. Left side originally 0.4... now both side 0.4, 0.4)

        2. Split
        ==========
            - Average whatever weight from both side
            (*eg. Left side originally 0.4... now both side 0.2,0.2 
                  but if left side 0.4, right side 0.2..... then both side = (0.4+0.2)/2 = 0.3,0.3)
        """
        self.helpBoxClass.helpBox1(name, helpTxt)    

    def reloadSub(self):
        PaintMidVertWeight()  
        

if __name__=='__main__':
    PaintMidVertWeight() 
                   