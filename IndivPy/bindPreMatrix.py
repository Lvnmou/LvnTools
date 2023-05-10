import maya.cmds as cmds
import maya.mel as mel
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox
import re
from functools import partial

class BindPreMatrix(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()


    def win(self):
        try: 
            cmds.deleteUI("bpm") 
        except:
            pass    
        cmds.window("bpm", mb=1)              
        cmds.window("bpm", t="BindPreMatrix", s=1, e=1, wh=(390,415))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on BindPreMatrix", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload BindPreMatrix", c=lambda x:self.reloadSub())    
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("BPM")
        form1= cmds.formLayout(nd=100, p=column1) 
        self.drop1= cmds.optionMenuGrp(l="Method 1 :", cw2=(60,10), cc=lambda x:self.om1())
        cmds.menuItem(l="Parent Inverse Matrix")
        cmds.menuItem(l="Search and Replace")   
        self.drop2= cmds.optionMenuGrp(l="Method 2 :", cw2=(60,10), cc=lambda x:self.om2())
        cmds.menuItem(l="Except")
        cmds.menuItem(l="Affect")   
        sep1= cmds.separator(h=20, st="in")
        self.txtSear= cmds.textFieldGrp(l="Search :", tx="", cw2=(50,10), adj=2, en=0) 
        self.txtRepl= cmds.textFieldGrp(l="Replace :", tx="", cw2=(50,10), adj=2, en=0)
        sep2= cmds.separator(h=20, st="in")   
        self.txtSkin= cmds.textFieldButtonGrp(l="Skin :", tx="", pht="<Can skip, just to enable popUp menu>", cw3=(50,10,10), adj=2, bl="  Grab  ", bc= lambda :self.grabSkin())  
        self.txtExc= cmds.textFieldGrp(l="Except :", tx="", pht="<Can be left blank> <Right click>", cw2=(50,10), adj=2)  
        self.jntExc= cmds.popupMenu(p=self.txtExc)
        self.txtAff= cmds.textFieldGrp(l="Affect :", tx="", en=0, pht="<Can be left blank>  <Right click>", cw2=(50,10), adj=2)  
        self.jntAff= cmds.popupMenu(p=self.txtAff)
        txt1= cmds.text(l="Select SKINNED MESH", fn="smallObliqueLabelFont", en=0)
        b1= cmds.button(l="Setup BindPreMatrix", c=lambda x:self.setupBpm())   
        b2= cmds.button(l="Setup for Cluster", c=lambda x:self.setupCluster())
        b3= cmds.button(l="Break BindPreMatrix", c=lambda x:self.breakBpm())
        txt2= cmds.text(l="*Set to default pose before breakBpm", fn="smallObliqueLabelFont", en=0)
        cmds.formLayout(form1, e=1,
                              af=[(self.drop1, "top", 0),
                                  (self.drop2, "top", 0),
                                  (sep1, "top", 25),
                                  (self.txtSear, "top", 50),
                                  (self.txtRepl, "top", 50),
                                  (sep2, "top", 75),
                                  (self.txtSkin, "top", 100),
                                  (self.txtExc, "top", 130),
                                  (self.txtAff, "top", 156),
                                  (txt1, "top", 200),
                                  (b1, "top", 216),
                                  (b2, "top", 216),
                                  (b3, "top", 242),
                                  (txt2, "top", 270)],
                              ap=[(self.drop1, "left", 0, 0),
                                  (self.drop2, "right", 0, 100),
                                  (sep1, "left", 0, 0),
                                  (sep1, "right", 0, 100),
                                  (self.txtSear, "left", 0, 0),
                                  (self.txtSear, "right", 0, 50),
                                  (self.txtRepl, "left", 0, 51),
                                  (self.txtRepl, "right", 0, 100),
                                  (sep2, "left", 0, 0),
                                  (sep2, "right", 0, 100),
                                  (self.txtSkin, "left", 0, 0),
                                  (self.txtSkin, "right", 0, 100),
                                  (self.txtExc, "left", 0, 0),
                                  (self.txtExc, "right", 0, 100),
                                  (self.txtAff, "left", 0, 0),
                                  (self.txtAff, "right", 0, 100),
                                  (txt1, "left", 0, 0),
                                  (txt1, "right", 0, 100),
                                  (b1, "left", 0, 0),
                                  (b1, "right", 0, 50),
                                  (b2, "left", 0, 51),
                                  (b2, "right", 0, 100),
                                  (b3, "left", 0, 0),
                                  (b3, "right", 0, 100),
                                  (txt2, "left", 0, 0),
                                  (txt2, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l= ""))
        cmds.showWindow("bpm")

    def om1(self):
        if cmds.optionMenuGrp(self.drop1, q=1, sl=1)==1:
            cmds.textFieldGrp(self.txtSear, e=1, en=0) 
            cmds.textFieldGrp(self.txtRepl, e=1, en=0)         
        else:
            cmds.textFieldGrp(self.txtSear, e=1, en=1) 
            cmds.textFieldGrp(self.txtRepl, e=1, en=1) 

    def om2(self):
        if cmds.optionMenuGrp(self.drop2, q=1, sl=1)==1:
            cmds.textFieldGrp(self.txtExc, e=1, en=1) 
            cmds.textFieldGrp(self.txtAff, e=1, en=0)         
        else:
            cmds.textFieldGrp(self.txtExc, e=1, en=0) 
            cmds.textFieldGrp(self.txtAff, e=1, en=1)  

    def defi(self):
        self.obj= cmds.ls(sl=1)  
        self.sear= cmds.textFieldGrp(self.txtSear, q=1, tx=1) 
        self.repl= cmds.textFieldGrp(self.txtRepl, q=1, tx=1) 
        self.exc= cmds.textFieldGrp(self.txtExc, q=1, tx=1) 
        self.aff= cmds.textFieldGrp(self.txtAff, q=1, tx=1) 

    def grabSkin(self):
        self.defi()
        if self.obj:
            if len(self.obj)==1:
                skinCluster= mel.eval("findRelatedSkinCluster %s"%self.obj[0])
                if skinCluster:
                    allJnt= cmds.skinCluster(self.obj, inf=1, q=1)
                    cmds.popupMenu(self.jntExc, e=1, dai=1)
                    cmds.popupMenu(self.jntAff, e=1, dai=1)
                    for item in sorted(allJnt):   
                        cmds.menuItem("%s"%item, c=partial(self.subPop, self.txtExc, item), p=self.jntExc)   
                        cmds.menuItem("%s"%item, c=partial(self.subPop, self.txtAff, item), p=self.jntAff)  
                    cmds.textFieldButtonGrp(self.txtSkin, e=1, tx="%s"%skinCluster) 
                else:
                    cmds.warning("Object does not have a skincluster")
            else:
                cmds.warning("Please select only 1 object")
        else:
            cmds.warning("Please select 1 object")

    def subPop(self, txt, jntName, *args):
        txtF= cmds.textFieldGrp(txt, q=1, tx=1)   
        if txtF:  
            cmds.textFieldGrp(txt, e=1, tx="%s, %s"%(txtF, jntName))            
        else:
            cmds.textFieldGrp(txt, e=1, tx="%s"%(jntName))           

    def setupBpm(self):
        self.defi()
        testSkin = 1 

        if self.obj:
            allJnt= []
            for item in self.obj:
                skin= mel.eval("findRelatedSkinCluster %s"%item) 
                if skin:
                    jnt= cmds.skinCluster(skin, inf=1, q=1)
                    for subJnt in jnt:
                        #to filter off appropriate joint
                        if cmds.optionMenuGrp(self.drop2, q=1, sl=1)==1: 
                            if subJnt in self.exc:
                                continue
                        else:
                            if subJnt not in self.aff:
                                continue
                        if subJnt not in allJnt:
                            allJnt.append(subJnt)
                else:
                    testSkin=[]
                    break
            if testSkin:
                if cmds.optionMenuGrp(self.drop1, q=1, sl=1)==1:
                    #This is to auto detect see if user setup have bpmJnt but forget bpm as search replace
                    non, finalTar= self.dialogClass.sameNameOrNoExistDialog(allJnt, "jnt", "bpmJnt", noPop=1) 
                    if finalTar:
                        conti1= self.dialogClass.continueDialog([], "Located bpmJnt for skinned joint, you sure you want to continue?")
                    else:
                        conti1= 1
                else:
                    conti1, tar= self.dialogClass.sameNameOrNoExistDialog(allJnt, self.sear, self.repl)
                if conti1:
                    self.uiStuffClass.loadingBar(1, len(self.obj))
                    for item in self.obj:
                        skin= mel.eval("findRelatedSkinCluster %s"%item) 
                        jnts=cmds.listConnections("%s.matrix"%skin, s=1, d=0, c=1)
                        for x in range(0,len(jnts),2):
                            if cmds.optionMenuGrp(self.drop2, q=1, sl=1)==1: 
                                if jnts[x+1] in self.exc:
                                    continue
                            else:
                                if jnts[x+1] not in self.aff:
                                    continue
                            matInd=re.findall("\[\d*\]", jnts[x])[0]            
                            try:
                                if cmds.optionMenuGrp(self.drop1, q=1, sl=1)==1: 
                                    cmds.connectAttr("%s.parentInverseMatrix"%jnts[x+1], "%s.bindPreMatrix%s"%(skin,matInd), f=1)   
                                else:
                                    cmds.connectAttr("%s.worldInverseMatrix"%jnts[x+1].replace(self.sear, self.repl), "%s.bindPreMatrix%s"%(skin, matInd), f=1)                          
                            except:
                                pass   
                        self.uiStuffClass.loadingBar(2)       
                    self.uiStuffClass.loadingBar(3) 
            else:
                cmds.warning("One of the Selected object does not have skinCluster")
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def setupCluster(self):
        self.defi()               
        if len(self.obj)==1: 
            allClus= cmds.ls(cmds.listHistory(self.obj[0], f=0), typ="cluster")
            if allClus:
                self.uiStuffClass.loadingBar(1, len(allClus))
                for clus in allClus:
                    cmds.setAttr("%s.relative"%clus, 1)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("Selected object does not have any cluster deformer")
        else:
            cmds.warning("Please select 1 OBJECT")

    def breakBpm(self): 
        self.defi()
        test1= 1
        if self.obj:        
            for item in self.obj:
                skin= mel.eval("findRelatedSkinCluster %s"%item)    
                if skin=="":
                    test1= []
            if test1:
                self.uiStuffClass.loadingBar(1, len(self.obj))
                for item in self.obj:
                    skin= mel.eval("findRelatedSkinCluster %s"%item)
                    num= cmds.getAttr("%s.matrix"%(skin), s=1) 
                    jnts=cmds.listConnections("%s.matrix"%skin, s=1, d=0, c=1)    
                    for x in range(0,len(jnts),2):
                        matInd=re.findall("\[\d*\]", jnts[x])[0]            
                        try:
                            conn= cmds.listConnections("%s.matrix%s"%(skin,matInd), s=1, d=0)[0]    
                            try:             
                                cmds.connectAttr("%s.worldInverseMatrix"%conn, "%s.bindPreMatrix%s"%(skin,matInd), f=1) 
                            except:
                                pass
                            bpm= ( cmds.getAttr("%s.bindPreMatrix%s"%(skin,matInd)))
                            cmds.disconnectAttr("%s.worldInverseMatrix"%conn, "%s.bindPreMatrix%s"%(skin,matInd))
                            cmds.setAttr("%s.bindPreMatrix%s"%(skin,matInd), bpm, typ="matrix")
                        except:
                            print jnts[x+1] 
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("Selected object does not have skinCluster")
        else:
            cmds.warning("Please select at least 1 SKINNED OBJECT")    
                    
    def helps(self):
        name="Help On BindPreMatrix"
        helpTxt="""
        - Setup bindPreMatrix for skincluster
        (* Usually connect the skin joint's parentInverseMatrix to appropriate bindPreMatrix)
        (* Resulting joint will deform the object but the joint's parent won't. This is for some tweak layer effects)



        A) Setup
        =========
            1) Skin
            ------------
                1. Method 1 
                    - Skinned joint's Parent Inverse Matrix
                    - Search & Replace (Manually search bindPreMatrix joint target)

                2. Method 2
                    - Except
                        - Usually use this
                        - Usually have the "static_jnt" to flush all other joint. Should not bindPrematrix this
                    - Affect 
                        - Maybe object in the skin have different BPM target name
                        (* Because setup BPM will reset for every other joint, so it just wanna affect specific target, needa specify)
                        (*eg. joint1,2,3 BPM target is A1,2,3 where joint4,5,6 is B4,5,6)

                - <Grab> skin textfield mainly to activate popup menu for <Except>, <Affect> textfield, can choose to skip.
                (* Meaning after grab skin can right click on textfield to choose joint)  

            2) Cluster
                (* its actually just tick the relative)

        
        B) Break
        =============
            - Delete BindPreMatrix link + return the mesh to original shape
            (* Must set to default pose before use <Break BPM>!)
            (* Manually delete link will messed up object shape. Have to note the matrix of it and after breaking it, need to re-apply)

        """
        self.helpBoxClass.helpBox1(name, helpTxt)    

    def reloadSub(self):
        BindPreMatrix()   
            

if __name__=='__main__':
    BindPreMatrix() 
                   