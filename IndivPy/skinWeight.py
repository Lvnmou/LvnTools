import maya.cmds as cmds
import maya.mel as mel
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox


class SkinWeight(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()


    def win(self):
        try:
            cmds.deleteUI("sw")
        except:
            pass          
        cmds.window("sw", mb=1)
        cmds.window("sw",t="Skin Weight", e=1, s=1, wh=(450,440))   
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on SkinWeight", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload SkinWeight", c=lambda x:self.reloadSub()) 
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Skinning")
        form11= cmds.formLayout(nd=100, p=column1)
        txt101= cmds.text(l="Select OBJECT", fn="smallObliqueLabelFont", en=0)
        b101= cmds.button(l="Joint Type Children", c=lambda x:self.selJointChild(1)) 
        b102= cmds.button(l="Joint Type Children (without last)", c=lambda x:self.selJointChild(2))
        b103= cmds.button(l="Skinned Joint", c=lambda x:self.selSkinJoint()) 
        cmds.formLayout(form11, e=1,
                                af=[(txt101, "top", 0),
                                    (b101, "top", 16),
                                    (b102, "top", 16),
                                    (b103, "top", 42)],
                                ap=[(txt101, "left", 0, 0),
                                    (txt101, "right", 0, 100),
                                    (b101, "left", 0, 0),
                                    (b101, "right", 0, 50),
                                    (b102, "left", 0, 51),
                                    (b102, "right", 0, 100),
                                    (b103, "left", 0, 0),
                                    (b103, "right", 0, 100)])  
        self.uiStuffClass.multiSetParent(3)
        column12= self.uiStuffClass.sepBoxSub()
        form12= cmds.formLayout(nd=100, p=column12)
        self.drop11= cmds.optionMenuGrp(l="Skin Method : ", cw2=(83,10))
        cmds.menuItem(l="Classic Linear")
        cmds.menuItem(l="Dual Quaternion") 
        cmds.menuItem(l="Weight Blended")   
        self.slider11= cmds.intSliderGrp(f=1, l="Max Influence :", cw3=(80,30,20), min=1, max=5, v=5, fmx=30)    
        self.cbMaxInf= cmds.checkBoxGrp(l="", l1="Maintain Max", cw2=(5,0))
        self.pt= cmds.radioButtonGrp(l="Paint Type :", cw4=(80,80,100,120), la3=["Normal", "Joint Chain", "Separate"], nrb=3, sl=1)
        txt111= cmds.text(l="Select JOINT then OBJECT", fn="smallObliqueLabelFont", en=0)
        b111= cmds.button(l="Normal Bind", c=lambda x:self.bindSkin(1)) 
        b112= cmds.button(l="Heat Map", c=lambda x:self.bindSkin(2))  
        txt112= cmds.text(l="Select OBJECT", fn="smallObliqueLabelFont", en=0)
        b113= cmds.button(l="Unbind", c=lambda x:self.unbindSkin(1, cmds.ls(sl=1))) 
        b114= cmds.button(l="Unbind (Keep History)", c=lambda x:self.unbindSkin(2, cmds.ls(sl=1))) 
        b115= cmds.button(l="Bind Back", c=lambda x:self.bindBack(cmds.ls(sl=1)))
        cmds.formLayout(form12, e=1,
                                af=[(self.drop11, "top", 0),
                                    (self.slider11, "top", 26),
                                    (self.cbMaxInf, "top", 26),
                                    (self.pt, "top", 52),
                                    (txt111, "top", 82),
                                    (b111, "top", 98),
                                    (b112, "top", 98),
                                    (txt112, "top", 134),
                                    (b113, "top", 150),
                                    (b114, "top", 176),
                                    (b115, "top", 176)],
                                ap=[(self.drop11, "left", 0, 0),
                                    (self.drop11, "right", 0, 100),
                                    (self.slider11, "left", 0, 0),
                                    (self.slider11, "right", 0, 70),
                                    (self.cbMaxInf, "left", 0, 71),
                                    (self.cbMaxInf, "right", 0, 100),
                                    (self.pt, "left", 0, 0),
                                    (self.pt, "right", 0, 100),
                                    (txt111, "left", 0, 0),
                                    (txt111, "right", 0, 100),
                                    (b111, "left", 0, 0),
                                    (b111, "right", 0, 50),
                                    (b112, "left", 0, 51),
                                    (b112, "right", 0, 100),
                                    (txt112, "left", 0, 0),
                                    (txt112, "right", 0, 100),
                                    (b113, "left", 0, 0),
                                    (b113, "right", 0, 100),
                                    (b114, "left", 0, 0),
                                    (b114, "right", 0, 50),
                                    (b115, "left", 0, 51),
                                    (b115, "right", 0, 100)])   
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column21= self.uiStuffClass.sepBoxSub("Influence")
        form21= cmds.formLayout(nd=100, p=column21)
        self.txtFInfSear= cmds.textFieldGrp(l="Search :", tx="L", cw2=(55,50), adj=2) 
        self.txtFInfRepl= cmds.textFieldGrp(l="Replace :", tx="R", cw2=(55,50), adj=2) 
        txt201= cmds.text(l="Select TARGETS", fn="smallObliqueLabelFont", en=0)
        txt202= cmds.text(l="Select SOURCE then TARGETS", fn="smallObliqueLabelFont", en=0)        
        b201= cmds.button(l="Add Search Replace Influence",c=lambda x:self.addSRInfluence())
        b202= cmds.button(l="Add Object's Influence",c=lambda x:self.addObjInfluence()) 
        cmds.formLayout(form21, e=1,
                                af=[(self.txtFInfSear, "top", 0),
                                    (self.txtFInfRepl, "top", 23),
                                    (txt201, "top", 60),
                                    (txt202, "top", 60),
                                    (b201, "top", 76),
                                    (b202, "top", 76)],
                                ap=[(self.txtFInfSear, "left", 0, 0),
                                    (self.txtFInfSear, "right", 0, 100),
                                    (self.txtFInfRepl, "left", 0, 0),
                                    (self.txtFInfRepl, "right", 0, 100),
                                    (txt201, "left", 0, 0),
                                    (txt201, "right", 0, 50),
                                    (txt202, "left", 0, 51),
                                    (txt202, "right", 0, 100),
                                    (b201, "left", 0, 0),
                                    (b201, "right", 0, 50),
                                    (b202, "left", 0, 51),
                                    (b202, "right", 0, 100)])   
        self.uiStuffClass.multiSetParent(3)
        column22= self.uiStuffClass.sepBoxSub()
        form22= cmds.formLayout(nd=100, p=column22)
        self.cbTar= cmds.checkBoxGrp(l="", cw2=(10,10), cc=lambda x:self.cbxTar())    
        self.txtInf= cmds.textFieldButtonGrp(l="Influence :", cw3=(60,10,10), en=0, adj=2, bl="  Grab  ", bc= lambda :self.grab1())  
        self.txt204= cmds.text(l="Select INFLUENCES then OBJECTS", fn="smallObliqueLabelFont", en=0)
        b203= cmds.button(l="Add Influence", c=lambda x:self.addRemoveInfluence(1, "ADDED"))
        b204= cmds.button(l="Remove Influence",c=lambda x:self.addRemoveInfluence(2, "REMOVED")) 
        cmds.formLayout(form22, e=1,
                                af=[(self.cbTar, "top", 6),
                                    (self.txtInf, "top", 0),
                                    (self.txt204, "top", 40),    
                                    (b203, "top", 56),
                                    (b204, "top", 56)],
                                ap=[(self.txtInf, "left", 40, 0),
                                    (self.txtInf, "right", 0, 100),
                                    (self.txt204, "left", 0, 0),
                                    (self.txt204, "right", 0, 100),
                                    (b203, "left", 0, 0),
                                    (b203, "right", 0, 50),
                                    (b204, "left", 0, 51),
                                    (b204, "right", 0, 100)])         
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column31= self.uiStuffClass.sepBoxSub("Weight")
        form31= cmds.formLayout(nd=100, p=column31)
        self.cbMeshSR= cmds.checkBoxGrp(l="", cw=(1,10), cc= lambda x:self.cbxMeshSR())
        self.txtMeshSear= cmds.textFieldGrp(l="Mesh Search :", tx="L", cw2=(80,50), adj=2, en=0) 
        self.txtMeshRepl= cmds.textFieldGrp(l="Mesh Replace :", tx="R", cw2=(80,50), adj=2, en=0) 
        sep301= cmds.separator(h=5, st="in")
        self.cbJntSR= cmds.checkBoxGrp(l="", cw=(1,10), cc= lambda x:self.cbxJntSR())
        self.txtJntSear= cmds.textFieldGrp(l="Joint Search :", tx="L", cw2=(80,50), adj=2, en=0) 
        self.txtJntRepl= cmds.textFieldGrp(l="Joint Replace :", tx="R", cw2=(80,50), adj=2, en=0)  
        sep302= cmds.separator(h=5, st="in")
        self.txt301= cmds.text(l="Select SOURCE then TARGETS", fn="smallObliqueLabelFont", en=0)
        eg301= cmds.text(l="   obj_A > obj_B", fn="smallObliqueLabelFont", en=0)  
        eg302= cmds.text(l="   old_JNT > new_JNT", fn="smallObliqueLabelFont", en=0)
        eg303= cmds.text(l="   L_Gloves > R_Gloves", fn="smallObliqueLabelFont", en=0)        
        b301= cmds.button(l="Copy Weight", c=lambda x:self.copyWeight())
        self.b302= cmds.button(l="Replace Joint", c=lambda x:self.replaceJoint(1), en=0)      
        self.b303= cmds.button(l="Replace Joint + Mirror (remove unused)",c=lambda x:self.replaceJoint(2), en=0)  
        self.rbMir1= cmds.radioButtonGrp(l="", cw4=(85,70,70,70), la3=["XY","YZ","XZ"], nrb=3 , sl=2)  
        cmds.formLayout(form31, e=1,
                                af=[(self.cbMeshSR, "top", 15),   
                                    (self.txtMeshSear, "top", 0),
                                    (self.txtMeshRepl, "top", 26),
                                    (sep301, "top", 62), 
                                    (self.cbJntSR, "top", 90), 
                                    (self.txtJntSear, "top", 78),
                                    (self.txtJntRepl, "top", 104),
                                    (sep302, "top", 140),
                                    (self.txt301, "top", 156),
                                    (b301, "top", 172),
                                    (eg301, "top", 177),
                                    (self.b302, "top", 198),
                                    (eg302, "top", 203),
                                    (self.b303, "top", 224),
                                    (eg303, "top", 229),
                                    (self.rbMir1, "top", 255)],
                                ap=[(self.txtMeshSear, "left", 40, 0),
                                    (self.txtMeshSear, "right", 0, 100),
                                    (self.txtMeshRepl, "left", 40, 0),
                                    (self.txtMeshRepl, "right", 0, 100),
                                    (sep301, "left", 0, 0),
                                    (sep301, "right", 0, 100),
                                    (self.txtJntSear, "left", 40, 0),
                                    (self.txtJntSear, "right", 0, 100),
                                    (self.txtJntRepl, "left", 40, 0),
                                    (self.txtJntRepl, "right", 0, 100),
                                    (sep302, "left", 0, 0),
                                    (sep302, "right", 0, 100),
                                    (self.txt301, "left", 50, 0),
                                    (self.txt301, "right", 0, 100),
                                    (b301, "left", 120, 0),
                                    (b301, "right", 0, 100),
                                    (self.b302, "left", 120, 0),
                                    (self.b302, "right", 0, 100),
                                    (self.b303, "left", 120, 0),
                                    (self.b303, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column41= self.uiStuffClass.sepBoxSub("Vertex Weight")
        form41= cmds.formLayout(nd=100, p=column41)
        self.txtCopySour= cmds.textFieldButtonGrp(l="Source Mesh :", cw3=(80,10,10), adj=2, bl="  Grab  ", bc= lambda :self.grab2())  
        self.txtCopyTar= cmds.textFieldButtonGrp(l="Target Vertex :", cw3=(80,10,10), adj=2, bl="  Grab  ", bc= lambda :self.grab3())  
        b401= cmds.button(l="Reselect Target Vertex",c=lambda x:self.selTarVert())
        b402= cmds.button(l="Copy Vertex Weight",c=lambda x:self.copyVertWeight())
        txt401= cmds.text(l="Select MESH", fn="smallObliqueLabelFont", en=0)
        b403= cmds.button(l="Convert Target Vertex To Selected Mesh's Vertex",c=lambda x:self.convertVert())
        cmds.formLayout(form41, e=1,
                                af=[(self.txtCopySour, "top", 0),   
                                    (self.txtCopyTar, "top", 26),
                                    (b401, "top", 62),
                                    (b402, "top", 88),
                                    (txt401, "top", 123),
                                    (b403, "top", 138)],
                                ap=[(self.txtCopySour, "left", 0, 0),
                                    (self.txtCopySour, "right", 0, 100),
                                    (self.txtCopyTar, "left", 0, 0),
                                    (self.txtCopyTar, "right", 0, 100),
                                    (b401, "left", 0, 0),
                                    (b401, "right", 0, 100),
                                    (b402, "left", 0, 0),
                                    (b402, "right", 0, 100),
                                    (txt401, "left", 0, 0),
                                    (txt401, "right", 0, 100),
                                    (b403, "left", 0, 0),
                                    (b403, "right", 0, 100)]) 
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column51= self.uiStuffClass.sepBoxSub("Cleanup")  
        form51= cmds.formLayout(nd=100, p=column51)
        txt501= cmds.text(l="Select Vertex", fn="smallObliqueLabelFont", en=0)
        b501= cmds.button(l="Hammer Weight",c=lambda x:self.hamWeight())                       
        txt502= cmds.text(l="Select OBJECT", fn="smallObliqueLabelFont", en=0)
        b502= cmds.button(l="Remove Unused Influence",c=lambda x:self.removeUnusedInfluence()) 
        b503= cmds.button(l="Prune Weight Below",c=lambda x:self.pruneWeight()) 
        self.slider51= cmds.floatSliderGrp(f=1, cw2=(50,20), min=0.001, max=1, v=0.001, pre=4)  
        sep501= cmds.separator(h=5, st="in")
        b504= cmds.button(l="Skin Back Fix Weight (Same Mesh)",c=lambda x:self.skinBack(1)) 
        b505= cmds.button(l="Skin Back Fix History (New Mesh)",c=lambda x:self.skinBack(2))        
        sep502= cmds.separator(h=5, st="in")        
        self.rbMir2= cmds.radioButtonGrp(l="", cw4=(85,70,70,70), la3=["XY","YZ","XZ"], nrb=3 , sl=2)  
        b506= cmds.button(l="Mirror Weight - to +",c=lambda x:self.mirWeight(1))
        b507= cmds.button(l="Mirror Weight + to -",c=lambda x:self.mirWeight(2))
        cmds.formLayout(form51, e=1,
                                af=[(txt501, "top", 0),
                                    (b501, "top", 16),
                                    (txt502, "top", 52),
                                    (b502, "top", 68),
                                    (b503, "top", 94),
                                    (self.slider51, "top", 94),
                                    (sep501, "top", 130),
                                    (b504, "top", 150),
                                    (b505, "top", 176),
                                    (sep502, "top", 212),
                                    (self.rbMir2, "top", 232),  
                                    (b506, "top", 253),
                                    (b507, "top", 253)],
                                ap=[(txt501, "left", 0, 0),
                                    (txt501, "right", 0, 100),
                                    (b501, "left", 0, 0),
                                    (b501, "right", 0, 100),
                                    (txt502, "left", 0, 0),
                                    (txt502, "right", 0, 100),
                                    (b502, "left", 0, 0),
                                    (b502, "right", 0, 100),
                                    (b503, "left", 0, 0),
                                    (b503, "right", 0, 40),
                                    (self.slider51, "left", 0, 41),
                                    (self.slider51, "right", 0, 100),
                                    (sep501, "left", 0, 0),
                                    (sep501, "right", 0, 100),
                                    (b504, "left", 0, 0),
                                    (b504, "right", 0, 100),
                                    (b505, "left", 0, 0),
                                    (b505, "right", 0, 100),
                                    (sep502, "left", 0, 0),
                                    (sep502, "right", 0, 100),
                                    (self.rbMir2, "left", 0, 0),
                                    (self.rbMir2, "right", 0, 100),
                                    (b506, "left", 0, 0),
                                    (b506, "right", 0, 50),
                                    (b507, "left", 0, 51),
                                    (b507, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column52= self.uiStuffClass.sepBoxSub("Extra")         
        form52= cmds.formLayout(nd=100, p=column52)
        txt511= cmds.text(l="Select FACES", fn="smallObliqueLabelFont", en=0)
        b511= cmds.button(l="Create Dummy Mesh Set",c=lambda x:self.createDummySet())
        txt512= cmds.text(l="Check <Help> for details instruction", fn="smallObliqueLabelFont", en=0)   
        cmds.formLayout(form52, e=1,
                              af=[(txt511, "top", 0),
                                  (b511, "top", 16),
                                  (txt512, "top", 42)], 
                              ap=[(txt511, "left", 0, 0),
                                  (txt511, "right", 0, 100),
                                  (b511, "left", 0, 0),
                                  (b511, "right", 0, 100),
                                  (txt512, "left", 0, 0),
                                  (txt512, "right", 0, 100)])     
        cmds.setFocus(cmds.text(l="")) 
        cmds.showWindow("sw")

    def defi1(self):
        self.obj= cmds.ls(sl=1)
        self.skinMeth= cmds.optionMenuGrp(self.drop11, q=1, sl=1)
        self.maxInf= cmds.intSliderGrp(self.slider11, q=1, v=1)  

    def defi2(self): 
        self.obj= cmds.ls(sl=1)   
        self.infSear= cmds.textFieldGrp(self.txtFInfSear, q=1, tx=1) 
        self.infRepl= cmds.textFieldGrp(self.txtFInfRepl, q=1, tx=1)
        self.infTar= cmds.textFieldGrp(self.txtInf, q=1, tx=1)  

    def defi3(self):  
        self.obj= cmds.ls(sl=1)   
        self.jntSear= cmds.textFieldGrp(self.txtJntSear, q=1, tx=1) 
        self.jntRepl= cmds.textFieldGrp(self.txtJntRepl, q=1, tx=1)   
        self.meshSear= cmds.textFieldGrp(self.txtMeshSear, q=1, tx=1) 
        self.meshRepl= cmds.textFieldGrp(self.txtMeshRepl, q=1, tx=1)   

    def defi4(self):        
        self.copyMesh= cmds.textFieldButtonGrp(self.txtCopySour, q=1, tx=1)
        self.copyTar= cmds.textFieldButtonGrp(self.txtCopyTar, q=1, tx=1)

    def grab1(self):
        obj= cmds.ls(sl=1, typ="joint")
        if obj:      
            cmds.textFieldButtonGrp(self.txtInf, e=1, tx=", ".join(obj))                           
        else:
            cmds.warning("Please select at least 1 JOINT")  
     
    def grab2(self):
        obj= cmds.ls(sl=1, tr=1)
        testShp=[]
        if obj:  
            if len(obj)==1:
                if cmds.listRelatives(obj, s=1):
                    if cmds.objectType(cmds.listRelatives(obj, s=1)[0])=="mesh":    
                        cmds.textFieldButtonGrp(self.txtCopySour, e=1, tx=obj[0]) 
                        testShp=1
                if testShp==[]:
                    cmds.warning("Selected object is not a MESH")    
            else:
                cmds.warning("Please select only 1 MESH")                      
        else:
            cmds.warning("Please select 1 MESH") 

    def grab3(self):
        obj= cmds.ls(sl=1, fl=1)
        testVert=1
        if obj:  
            for item in obj:
                if ".v" not in item:
                    testVert=[]
            if testVert:
                cmds.textFieldButtonGrp(self.txtCopyTar, e=1, tx=", ".join(obj)) 
            else:
                cmds.warning("Selected object is not a VERTEX")                        
        else:
            cmds.warning("Please select at least 1 SUBSELECTION") 

    def cbxMeshSR(self):
        if cmds.checkBoxGrp(self.cbMeshSR, q=1, v1=1):
            cmds.textFieldGrp(self.txtMeshSear, e=1, en=1) 
            cmds.textFieldGrp(self.txtMeshRepl, e=1, en=1) 
            cmds.text(self.txt301, e=1, l="Select SOURCES")
        else:
            cmds.textFieldGrp(self.txtMeshSear, e=1, en=0) 
            cmds.textFieldGrp(self.txtMeshRepl, e=1, en=0)   
            cmds.text(self.txt301, e=1, l="Select SOURCE then TARGETS")

    def cbxJntSR(self):
        if cmds.checkBoxGrp(self.cbJntSR, q=1, v1=1):
            cmds.textFieldGrp(self.txtJntSear, e=1, en=1) 
            cmds.textFieldGrp(self.txtJntRepl, e=1, en=1)  
            cmds.button(self.b302, e=1, en=1)
            cmds.button(self.b303, e=1, en=1)
        else:
            cmds.textFieldGrp(self.txtJntSear, e=1, en=0) 
            cmds.textFieldGrp(self.txtJntRepl, e=1, en=0)    
            cmds.button(self.b302, e=1, en=0)
            cmds.button(self.b303, e=1, en=0)

    def cbxTar(self):
        if cmds.checkBoxGrp(self.cbTar, q=1, v1=1):
            cmds.textFieldGrp(self.txtInf, e=1, en=1) 
            cmds.text(self.txt204, e=1, l="Select OBJECTS")
        else:
            cmds.textFieldGrp(self.txtInf, e=1, en=0) 
            cmds.text(self.txt204, e=1, l="Select INFLUENCES then OBJECTS")

    def selJointChild(self, meth):
        obj= cmds.ls(sl=1)
        if obj:
            jntChd= []
            self.uiStuffClass.loadingBar(1, 2)
            self.uiStuffClass.loadingBar(2)
            for item in obj:
                if cmds.objectType(item)=="joint":
                    jntChd.append(item)
                chd= cmds.listRelatives(item, ad=1, pa=1, typ="joint")
                if chd:
                    if meth==1:
                        for stuff in reversed(chd):
                            jntChd.append(stuff)
                    elif meth==2:
                        for stuff in reversed(chd):
                            subChd= cmds.listRelatives(stuff, c=1, pa=1)
                            if subChd:
                                jntChd.append(stuff) 
            self.uiStuffClass.loadingBar(2)   
            self.uiStuffClass.loadingBar(3)                        
            if jntChd:
                cmds.select(jntChd)
            else:
                cmds.warning("Selected object does not have a JOINT type children")
        else:
            cmds.warning("Please select an object have have a JOINT type children")  

    def selSkinJoint(self):
        obj= cmds.ls(sl=1)
        if obj:
            allJnt= []
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                skin= mel.eval("findRelatedSkinCluster %s"%item)
                if skin:
                    jnts= cmds.skinCluster(skin, inf=1, q=1) 
                    for subJnt in jnts:
                        if subJnt not in allJnt:
                            allJnt.append(subJnt)
                self.uiStuffClass.loadingBar(2)   
            self.uiStuffClass.loadingBar(3) 
            if allJnt:
                cmds.select(allJnt)       
            else:
                cmds.warning("Select object is no SKINNED")
        else:
            cmds.warning("Please select at least 1 skinned OBJECT") 

    def testPostSkinCluster(self, tar):
        skinObj= []
        for item in tar:
            if mel.eval("findRelatedSkinCluster %s"%item):
                skinObj.append(item)    
        conti1= self.dialogClass.printingDialog(skinObj, "< %s > successful \n< %s > SKINCLUSTER is found, replace skincluster?"%(len(tar)-len(skinObj),len(skinObj)))
        return conti1                   

    def testPreSkinCluster(self, obj):
        test1= 1
        for item in obj:
            if mel.eval("findRelatedSkinCluster %s"%item)=="":   
                test1= []  
        if test1==[]:   
            self.dialogClass.warningDialog("One of the SOURCE is not skinned") 
        return test1     

    def testScale(self, obj, msg):
        scalJnt= []
        conti= 1
        for item in obj:
            scal= cmds.xform(item, q=1, s=1, ws=1)
            if [abs(round(scal[0], 1)),abs(round(scal[1], 1)),abs(round(scal[2], 1))]!=[1.0,1.0,1.0]:
                scalJnt.append(item)
        if scalJnt:
            conti= self.dialogClass.printingDialog(scalJnt, "< %s > %s that have scale, if continue might have problem"%(len(scalJnt),msg))
        return conti        

    def testJointOrTransform(self, obj):
        allJnt, allObj= [],[]
        for item in obj:
            if cmds.objectType(item)=="joint":
                allJnt.append(item)
            elif cmds.objectType(item)=="transform":
                allObj.append(item)    
        return allJnt, allObj    

    def dupBecomeChain(self, obj):
        tar= []
        if len(obj)>1:
            conti= self.testScale(obj, "Joints")
            if conti:
                for item in obj: 
                    #Duplicate dummy and cleanup    
                    dup= cmds.duplicate(item, n="%s_newJC"%item.split("|")[-1])
                    dupChd= cmds.listRelatives(dup[0], c=1, pa=1)
                    if dupChd:
                        cmds.delete(dupChd)    
                    tar.append(dup[0])

                    #Unparent if got parent
                    if cmds.listRelatives(item, p=1, pa=1):
                        cmds.parent(dup[0], w=1)

                #Reparent in order
                for x in range((len(tar)-1),0, -1):
                    cmds.parent(tar[x], tar[x-1])
                return tar    
        else:
            cmds.warning("Please select at least 2 OBJECT")

    def bindSkin(self, meth):
        self.defi1()
        conti3, conti4= 1,1
        pType= cmds.radioButtonGrp(self.pt, q=1, sl=1) 
        if cmds.checkBoxGrp(self.cbMaxInf, q=1, v1=1):
            omi= 1
        else:
            omi= 0   
        allJnt, allObj= self.testJointOrTransform(self.obj)
        if allJnt and allObj:
            conti1= self.testScale(allJnt, "Joints")
            if conti1:
                conti2= self.testScale(allObj, "Meshes")
                if conti2:
                    conti3= self.testPostSkinCluster(allObj)
                    if conti3:
                        self.uiStuffClass.loadingBar(1, len(allObj)+1)
                        self.uiStuffClass.loadingBar(2)
                        #To recreate types of joints
                        if pType==2:
                            if len(allJnt)>1:
                                newAllJnt= self.dupBecomeChain(allJnt)
                            else:
                                newAllJnt= cmds.duplicate(allJnt)
                        elif pType==3:
                            newAllJnt= []
                            for thing in allJnt:
                                newJnt= cmds.duplicate(thing, n="%s_tempBind"%thing, po=1)[0]
                                par= cmds.listRelatives(newJnt, p=1, pa=1)
                                if par:    
                                    newJnt= cmds.parent(newJnt, w=1)[0]
                                newAllJnt.append(newJnt) 
                        for stuff in allObj:
                            #Unbind first if there is existing skinCluster
                            if mel.eval("findRelatedSkinCluster %s"%stuff):
                                cmds.skinCluster(stuff, e=1, ub=1)

                            #Normal Paint
                            if pType==1:
                                if meth==1:
                                    cmds.skinCluster(allJnt, stuff, tsb=1, bm=0, sm=self.skinMeth-1, nw=1, wd=0, omi=omi, mi=self.maxInf, dr=4) 
                                elif meth==2:
                                    cmds.skinCluster(allJnt, stuff, tsb=1, bm=2, sm=self.skinMeth-1, nw=1, wd=0, omi=omi, mi=self.maxInf, hmf=0.68)                                       
                            
                            #Special paint need to bind to a dummy
                            else:
                                dupObj= cmds.duplicate(stuff, n="%s_tempBindMesh"%stuff) 
                                if meth==1:    
                                    tempSkin= cmds.skinCluster(newAllJnt, dupObj[0], tsb=1, bm=0, sm=self.skinMeth-1, nw=1, wd=0, omi=omi, mi=self.maxInf, dr=4) 
                                    tarSkin= cmds.skinCluster(allJnt, stuff, tsb=1, bm=0, sm=self.skinMeth-1, nw=1, wd=0, omi=omi, mi=self.maxInf, dr=4) 
                                elif meth==2:
                                    tempSkin= cmds.skinCluster(newAllJnt, dupObj[0], tsb=1, bm=2, sm=self.skinMeth-1, nw=1, wd=0, omi=omi, mi=self.maxInf, hmf=0.68) 
                                    tarSkin= cmds.skinCluster(allJnt, stuff, tsb=1, bm=2, sm=self.skinMeth-1, nw=1, wd=0, omi=omi, mi=self.maxInf, hmf=0.68)   
                                cmds.copySkinWeights(nm=1, sa="closestPoint", ia=("name", "closestJoint"), ss=tempSkin[0], ds=tarSkin[0])
                                cmds.delete(dupObj)
                            self.uiStuffClass.loadingBar(2)
                        self.uiStuffClass.loadingBar(3, sel=self.obj)
                        if pType!=1:
                            cmds.delete(newAllJnt)
        else:
            if allJnt==[]:
                cmds.warning("Please select at least 1 JOINT")
            else:
                cmds.warning("Please select at least 1 OBJECT")

    def unbindSkin(self, meth, obj, loading=1):
        if obj:
            noSkin, allJnt= [],[]
            conti1= 1
            if meth==2:
                conti1= []
            for item in obj:
                skin= mel.eval("findRelatedSkinCluster %s"%item)
                if skin:
                    jnt= cmds.skinCluster(skin, inf=1, q=1)  
                    for subJnt in jnt:
                        if subJnt not in allJnt:
                            allJnt.append(subJnt)

                    #Check if skin is unbind but keep history
                    if cmds.getAttr("%s.nodeState"%skin)==0:
                        conti1= 1                    
                else:
                    noSkin.append(item)
            if conti1:               
                conti2= self.dialogClass.printingDialog(noSkin, "< %s > successful\n< %s > does not have skinCluster"%(len(obj)-len(noSkin), len(noSkin)))
                if conti2:
                    if loading:
                        conti3= self.testScale(allJnt, "Joints")
                    else:
                        conti3=1
                    if conti3:
                        if loading:
                            self.uiStuffClass.loadingBar(1, len(obj))
                        for item in obj:
                            try:
                                skin= mel.eval("findRelatedSkinCluster %s"%item)
                                if meth==1:
                                    cmds.skinCluster(skin, e=1, ub=1)
                                elif meth==2:
                                    cmds.skinCluster(skin, e=1, ubk=1)
                            except:
                                pass
                            if loading:    
                                self.uiStuffClass.loadingBar(2)
                        if loading:
                            self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("All of the selected object already UNBIND with keep history")
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def bindBack(self, obj, loading=1):
        noSkin, allObj, normalSkin= [],[],[]
        conti1, conti2= 1,1
        for item in obj:
            if cmds.objectType(item)=="transform":
                allObj.append(item)
        if allObj:         
            for item in allObj:
                skin= mel.eval("findRelatedSkinCluster %s"%item)
                if skin:
                    #Check if skin is unbind but keep history
                    if cmds.getAttr("%s.nodeState"%skin)==0:
                        conti2= []
                else:
                    noSkin.append(item)
            conti1= self.dialogClass.printingDialog(noSkin, "< %s > successful\n< %s > does not have old skinCluster"%(len(allObj)-len(noSkin), len(noSkin)))
            if conti1:
                if conti2:
                    if loading:
                        self.uiStuffClass.loadingBar(1, len(allObj)) 
                    jnt= cmds.createNode("joint")               
                    for item in allObj:
                        cmds.skinCluster(jnt, item, tsb=1) 
                        if loading:
                            self.uiStuffClass.loadingBar(2)
                    cmds.delete(jnt)
                    if loading:
                        self.uiStuffClass.loadingBar(3, sel= allObj)
                else:
                    cmds.warning("One of the select object have not unbind with keep history")
        else:
            cmds.warning("Please select at least 1 OBJECT")         

    def addSRInfluence(self):  
        self.defi2()
        testSkin= 1
        allJnt, newInf= [],[]
        sameName, noExist, success, dupName= [],[],[],[]
        if self.obj:
            self.uiStuffClass.loadingBar(1, len(self.obj))
            for item in self.obj:   
                skin= mel.eval("findRelatedSkinCluster %s"%item)
                if skin== "":
                    testSkin=[]
                else:
                    #Check all the Joints for same name or exist
                    preJnt= cmds.skinCluster(skin, inf=1, q=1) 
                    #Special case because need to stack up the success influence
                    conti,finalTar,sameName1,noExist1,success1,dupName1 = self.dialogClass.sameNameOrNoExistSrDialog(preJnt, self.infSear, self.infRepl, noPop=1)
                    sameName= list(set(sameName).union(sameName1))
                    noExist= list(set(noExist).union(noExist1))
                    success= list(set(success).union(success1))
                    dupName= list(set(dupName).union(dupName1))    
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)                           
            if testSkin:
                conti1,non,non,non,non,non = self.dialogClass.sameNameOrNoExistSrDialog([], self.infSear, self.infRepl,[],sameName,noExist,success,dupName)
                if conti1:  
                    self.uiStuffClass.loadingBar(1, len(self.obj))
                    for item in self.obj:   
                        skin= mel.eval("findRelatedSkinCluster %s"%item) 
                        jnt= cmds.skinCluster(skin, inf=1, q=1)      
                        non, finalTar= self.dialogClass.sameNameOrNoExistDialog(jnt, self.infSear, self.infRepl, noPop=1) 
                        cmds.skinCluster(skin, e=1, lw=1, tsb=1, ai=list(set(finalTar).difference(jnt)), wt=0)
                        if list(set(finalTar).difference(jnt)):
                            newInf= 1    
                        self.uiStuffClass.loadingBar(2)         
                    self.uiStuffClass.loadingBar(3, sel=self.obj)
                    if newInf==[]:
                        cmds.warning("No new influence is added") 
            else:
                cmds.warning("One of the TARGET does not have skinCluster")    
        else:
            cmds.warning("Please select at least 1 TARGET")

    def addObjInfluence(self):
        self.defi2()
        if len(self.obj)>=2:
            testSkin= 1
            newInf= []
            tar= self.obj[1:]
            sourSkin= mel.eval("findRelatedSkinCluster %s"%self.obj[0])  
            if sourSkin:
                for item in tar:
                    tarSkin= mel.eval("findRelatedSkinCluster %s"%item)
                    if tarSkin== "":
                        testSkin= []
                if testSkin:
                    self.uiStuffClass.loadingBar(1, len(tar))
                    sourJnt= cmds.skinCluster(sourSkin, q=1, inf=1)
                    for item in tar:
                        tarSkin= mel.eval("findRelatedSkinCluster %s"%item)
                        tarJnt= cmds.skinCluster(tarSkin, q=1, inf=1)
                        cmds.skinCluster(tarSkin, e=1, lw=1, tsb=1, ai=list(set(sourJnt).difference(tarJnt)), wt=0)
                        if list(set(sourJnt).difference(tarJnt)):
                            newInf= 1
                        self.uiStuffClass.loadingBar(2)
                    self.uiStuffClass.loadingBar(3, sel= self.obj)
                    if newInf==[]:
                        cmds.warning("No new influence is added")
                else:
                    cmds.warning("One of the TARGET does not have skinCluster")    
            else:
                cmds.warning("SOURCE does not have skinCluster")         
        else:
            cmds.warning("Please select 1 SOURCE and at least 1 TARGET")

    def addRemoveInfluence(self, meth, msg):
        self.defi2()
        testObjSkin, unusedJnt= [],[]
        if cmds.checkBoxGrp(self.cbTar, q=1, v1=1):
            if self.infTar:
                allJnt, non= self.testJointOrTransform(self.infTar.split(", "))
                #seems like no need this step since I already fix the grab
                if allJnt:
                    if self.obj:
                        non, allObj= self.testJointOrTransform(self.obj)
                        if allObj:
                            testObjSkin= self.testPreSkinCluster(allObj)
                        else:
                            cmds.warning("There is no MESH in the selected OBJECT")
                    else:
                        cmds.warning("Please select at least 1 MESH")
                else:
                    cmds.warning("There are no joint inside <INFLUENCE> textfield")
            else:
                cmds.warning("<INFLUENCE> textfield is empty!")           
        else:            
            if len(self.obj)>=2:
                allJnt, allObj= self.testJointOrTransform(self.obj)          
                if allJnt and allObj:
                    testObjSkin= self.testPreSkinCluster(allObj)   
                else:
                    cmds.warning("Please select at least 1 JOINT and 1 SKINNED OBJECT")    
            else:
                cmds.warning("Please select at least 1 JOINT and 1 SKINNED OBJECT")   
        if testObjSkin: 
            for item in allObj:
                skin= mel.eval("findRelatedSkinCluster %s"%item)
                oriJnt= cmds.skinCluster(skin, inf=1, q=1)
                if meth==1:
                    tar= list(set(allJnt).difference(oriJnt))    
                elif meth==2:
                    tar= list(set(allJnt).intersection(oriJnt))
                for stuff in tar:
                    unusedJnt.append(stuff)
            if unusedJnt:
                self.uiStuffClass.loadingBar(1, len(allObj))
                for item in allObj:
                    skin= mel.eval("findRelatedSkinCluster %s"%item)
                    oriJnt= cmds.skinCluster(skin, inf=1, q=1)
                    if meth==1:
                        cmds.skinCluster(skin, e=1, lw=1, tsb=1, ai=list(set(allJnt).difference(oriJnt)), wt=0)    
                    elif meth==2:
                        cmds.skinCluster(skin, e=1, ri=list(set(allJnt).intersection(oriJnt)))
                        for stuff in allJnt:        
                            #remove influence color   
                            allCol= cmds.listConnections("%s.objectColorRGB"%stuff, p=1)
                            if allCol:
                                for col in allCol:
                                    if skin in col:
                                        cmds.disconnectAttr("%s.objectColorRGB"%stuff, col)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=self.obj)
            else:
                cmds.warning("NO new influence is %s"%msg)

    def copyWeight(self):
        self.defi3() 
        if cmds.checkBoxGrp(self.cbMeshSR, q=1, v1=1):   
            if self.obj:
                conti1= self.testPreSkinCluster(self.obj) 
                if conti1:  
                    conti2, finalTar= self.dialogClass.sameNameOrNoExistDialog(self.obj, self.meshSear, self.meshRepl) 
                    if conti2:    
                        conti3= self.testPostSkinCluster(finalTar)
                        if conti3:
                            #Test joint is it scale (sometimes rig global is scaled, then copy weight might have issue)
                            allJnt= []
                            for item in self.obj:        
                                oldSkin= mel.eval("findRelatedSkinCluster %s"%item)
                                skinMethod= cmds.skinCluster(oldSkin, sm=1, q=1)
                                jnts= cmds.skinCluster(oldSkin, inf=1, q=1)
                                for subJnt in jnts:
                                    if subJnt not in allJnt:
                                        allJnt.append(subJnt)
                            conti4= self.testScale(allJnt, "Joints")
                            if conti4:
                                meshNoExist, meshExistTest= [],[]
                                self.uiStuffClass.loadingBar(1, len(self.obj))
                                for item in self.obj:        
                                    oldSkin= mel.eval("findRelatedSkinCluster %s"%item)
                                    skinMethod= cmds.skinCluster(oldSkin, sm=1, q=1)
                                    jnts= cmds.skinCluster(oldSkin, inf=1, q=1)   
                                    tar= item.replace(self.meshSear, self.meshRepl)
                                    if cmds.objExists(tar):
                                        if tar!=item:
                                            meshExistTest= 1
                                    if meshExistTest:
                                        if mel.eval("findRelatedSkinCluster %s"%tar):
                                            cmds.skinCluster(tar, e=1, ub=1)
                                        newSkin= cmds.skinCluster(jnts, tar, tsb=1, sm=skinMethod)      
                                        cmds.copySkinWeights(nm=1, sa="closestPoint", ia=("name", "closestJoint"), ss=oldSkin, ds=newSkin[0])     
                                    else:
                                        meshNoExist.append(item)
                                    self.uiStuffClass.loadingBar(2)
                                self.uiStuffClass.loadingBar(3, sel=finalTar)
                                if meshNoExist:
                                    cmds.warning("Successful but skipped for target mesh that don't exist. This is the source <%s>"%(", ".join(meshNoExist)))
            else:
                cmds.warning("Please select at least 1 object")
        else:
            if len(self.obj)>=2:
                conti1= self.testPreSkinCluster([self.obj[0]]) 
                if conti1:    
                    conti2= self.testPostSkinCluster(self.obj[1:])
                    if conti2:
                        oldSkin= mel.eval("findRelatedSkinCluster %s"%self.obj[0])
                        skinMethod= cmds.skinCluster(oldSkin, sm=1, q=1)
                        jnts= cmds.skinCluster(oldSkin, inf=1, q=1)  

                        #Test joint is it scale (sometimes rig global is scaled, then copy weight might have issue)
                        allJnt= []
                        conti4= self.testScale(jnts, "Joints")
                        if conti4:
                            self.uiStuffClass.loadingBar(1, len(self.obj[1:]))
                            for item in self.obj[1:]:    
                                if mel.eval("findRelatedSkinCluster %s"%item):
                                    cmds.skinCluster(item, e=1, ub=1)
                                newSkin= cmds.skinCluster(jnts, item, tsb=1, sm=skinMethod)                                 
                                cmds.copySkinWeights(nm=1, sa="closestPoint", ia=("name", "closestJoint"), ss=oldSkin, ds=newSkin[0])
                                self.uiStuffClass.loadingBar(2)
                            self.uiStuffClass.loadingBar(3, sel=self.obj[1:])
            else:
                cmds.warning("Please select 1 SOURCE and 1 TARGET")

    def replaceJoint(self, meth):
        self.defi3()
        if cmds.radioButtonGrp(self.rbMir1, sl=1, q=1)==1:
            mir="XY"
        elif cmds.radioButtonGrp(self.rbMir1, sl=1, q=1)==2:
            mir="YZ"
        else:
            mir="XZ"    
        if cmds.checkBoxGrp(self.cbMeshSR, q=1, v1=1): 
            if self.obj:
                conti1= self.testPreSkinCluster(self.obj) 
                if conti1:  
                    conti2, finalTar= self.dialogClass.sameNameOrNoExistDialog(self.obj, self.meshSear, self.meshRepl) 
                    if conti2:    
                        conti3= self.testPostSkinCluster((", ".join(self.obj)).replace(self.meshSear, self.meshRepl).split(", "))
                        if conti3:
                            allJnt= []
                            #Check all the Joints
                            for item in self.obj:        
                                oldSkin= mel.eval("findRelatedSkinCluster %s"%item)
                                preJnt= cmds.skinCluster(oldSkin, inf=1, q=1) 
                                allJnt= list(set(allJnt).union(preJnt))
                            conti4, finalTar= self.dialogClass.sameNameOrNoExistDialog(allJnt, self.jntSear, self.jntRepl)
                            if conti4: 
                                meshNoExist, meshExistTest= [],[]
                                self.uiStuffClass.loadingBar(1, len(self.obj))
                                for item in self.obj:        
                                    oldSkin= mel.eval("findRelatedSkinCluster %s"%item)
                                    skinMethod= cmds.skinCluster(oldSkin, sm=1, q=1)
                                    oldJnt= cmds.skinCluster(oldSkin, inf=1, q=1) 
                                    newJnt=[]  
                                    tar= item.replace(self.meshSear, self.meshRepl)
                                    if cmds.objExists(tar):
                                        if tar!=item:
                                            meshExistTest = 1
                                    if meshExistTest:
                                        for jnt in oldJnt:
                                            if cmds.objExists(jnt.replace(self.jntSear, self.jntRepl)):
                                                newJnt.append(jnt.replace(self.jntSear, self.jntRepl))
                                            else:
                                                newJnt.append(jnt)
                                        if mel.eval("findRelatedSkinCluster %s"%tar):
                                            cmds.skinCluster(tar, e=1, ub=1)
                                        if meth==1:          
                                            newSkin= cmds.skinCluster(newJnt, tar, tsb=1, sm=skinMethod)            
                                            cmds.copySkinWeights(nm=1, sa="closestPoint", ia=("name", "closestJoint"), ss=oldSkin, ds=newSkin[0])
                                        else:
                                            newSkin= cmds.skinCluster((oldJnt+newJnt), tar, tsb=1, sm=skinMethod)            
                                            cmds.copySkinWeights(mm=mir, sa="closestPoint", ia="closestJoint", ss=oldSkin, ds=newSkin[0])
                                            self.removeUnusedInfluence([tar], 1)     
                                    else:
                                        meshNoExist.append(item)
                                    self.uiStuffClass.loadingBar(2)    
                                self.uiStuffClass.loadingBar(3, sel=(", ".join(self.obj).replace(self.meshSear, self.meshRepl).split(", ")))
                                if meshNoExist:
                                    cmds.warning("Successful but skipped for target mesh that don't exist. This is the source <%s>"%(", ".join(meshNoExist)))
            else:
                cmds.warning("Please select at least 1 OBJECT")
        else:
            if len(self.obj)==2:
                conti1= self.testPreSkinCluster([self.obj[0]]) 
                if conti1:    
                    conti2= self.testPostSkinCluster([self.obj[1]])
                    if conti2:   
                        oldSkin= mel.eval("findRelatedSkinCluster %s"%self.obj[0])
                        skinMethod= cmds.skinCluster(oldSkin, sm=1, q=1)
                        oldJnt= cmds.skinCluster(oldSkin, inf=1, q=1) 
                        newJnt=[]
                        conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(oldJnt, self.jntSear, self.jntRepl)
                        if conti:
                            self.uiStuffClass.loadingBar(1, 2)
                            self.uiStuffClass.loadingBar(2)
                            for jnt in oldJnt:
                                if cmds.objExists(jnt.replace(self.jntSear, self.jntRepl)):
                                    newJnt.append(jnt.replace(self.jntSear, self.jntRepl))
                                else:
                                    newJnt.append(jnt)
                            if mel.eval("findRelatedSkinCluster %s"%self.obj[1]):
                                cmds.skinCluster(self.obj[1], e=1, ub=1)
                            if meth==1:          
                                newSkin= cmds.skinCluster(newJnt, self.obj[1], tsb=1, sm=skinMethod)            
                                cmds.copySkinWeights(nm=1, sa="closestPoint", ia=("name", "closestJoint"), ss=oldSkin, ds=newSkin[0])
                            else:
                                newSkin= cmds.skinCluster((oldJnt+newJnt), self.obj[1], tsb=1, sm=skinMethod)            
                                cmds.copySkinWeights(mm=mir, sa="closestPoint", ia="closestJoint", ss=oldSkin, ds=newSkin[0])
                                self.removeUnusedInfluence([self.obj[1]], 1) 
                            self.uiStuffClass.loadingBar(2)    
                            self.uiStuffClass.loadingBar(3, sel=self.obj[1])                
            else:
                cmds.warning("Please choose only 1 SOURCE and 1 TARGET") 

    def selTarVert(self):
        self.defi4()
        if self.copyTar:
            cmds.select(self.copyTar.split(", ")[0].split(".")[0])
            cmds.selectMode(co=1)
            cmds.select(self.copyTar.split(", "))
        else:
            cmds.warning("<Target Vertex> field is empty!")

    def copyVertWeight(self):
        self.uiStuffClass.loadingBar(1,2)
        self.defi4()
        obj= cmds.ls(sl=1)
        self.uiStuffClass.loadingBar(2)  
        conti= self.testMeshVertex()
        if conti:
            cmds.select(self.copyMesh, r=1)
            cmds.select(self.copyTar.split(", "), add=1)
            cmds.copySkinWeights(nm=1, sa="closestPoint", ia="closestJoint")
            self.uiStuffClass.loadingBar(2)    
        self.uiStuffClass.loadingBar(3, sel=obj)

    def testMeshVertex(self):
        self.defi4()
        testMeshExist, testShp, testSkin= [],[],[]
        testVertExist, testSameObj, testVert, conti= 1,1,1,1
        if self.copyMesh and self.copyTar:
            #Test mesh exist
            if cmds.objExists(self.copyMesh):
                testMeshExist= 1
                if cmds.objectType(self.copyMesh)=="transform":
                    if cmds.objectType(cmds.listRelatives(self.copyMesh, s=1)[0])=="mesh":
                        testShp= 1 
                        skin= mel.eval("findRelatedSkinCluster %s"%self.copyMesh)
                        if skin:
                            testSkin= 1    
            if testShp:   
                #Test vertex exist
                vertObj= self.copyTar.split(", ")[0].split(".")[0]
                if vertObj== self.copyMesh:
                    testSameObj= []
                if testSameObj:
                    if cmds.objExists(vertObj):
                        for vert in self.copyTar.split(", "):
                            if cmds.objExists(self.copyTar)==0:
                                testVertExist= []
                            if ".vtx" not in vert:
                                testVert= []
                    else:
                        testVertExist= [] 
            #Final
            if testMeshExist==[] or testVertExist==[] or testShp==[]  or testSkin==[] or testSameObj==[] or testVert==[]:
                if testMeshExist==[]:
                    cmds.warning("Object in <Source Mesh> does not EXIST")
                elif testShp==[]:
                    cmds.warning("Object in <Source Mesh> is not a MESH")  
                elif testSkin==[]:
                    cmds.warning("Object in <Source Mesh> is not a SKINNED MESH")                    
                elif testSameObj==[]:
                    cmds.warning("Object in <Source Mesh> is the SAME as <Target>")   
                elif testVert==[]:
                    cmds.warning("One of the selection in <Target Vertex> is not a VERTEX")    
                elif testVertExist==[]:
                    cmds.warning("One of the Vertex in <Target Vertex> does no EXIST")
                conti= []
        else:
            if self.copyMesh=="":
                cmds.warning("<Source Mesh> textfield is empty!") 
            elif self.copyTar=="":
                cmds.warning("<Target Vertex> textfield is empty!") 
            conti= [] 
        return conti

    def convertVert(self):
        self.defi4()
        obj= cmds.ls(sl=1, typ="transform")
        testShp, finalTar, prevObj= [],[],[]
        testVert, testSel= 1,1
        if self.copyTar:
            if obj:
                if len(obj)==1:
                    if cmds.objectType(obj)=="transform":
                        if cmds.objectType(cmds.listRelatives(obj, s=1)[0])=="mesh":
                            testShp= 1
                    if testShp:
                        self.uiStuffClass.loadingBar(1, 1)
                        vertObj= self.copyTar.split(", ")[0].split(".")[0]
                        tar= self.copyTar.replace(vertObj, obj[0])
                        cmds.select(obj[0])
                        cmds.selectMode(co=1)
                        self.uiStuffClass.loadingBar(2)
                        self.uiStuffClass.loadingBar(3, sel=tar.split(", "))  
                    else:
                        cmds.warning("Selection is not a MESH")
                else:
                    cmds.warning("Please select only 1 MESH")
            else:
                cmds.warning("Please select 1 MESH")
        else:
            cmds.warning("<Target Vertex> textfield is empty!")

    def hamWeight(self):
        obj= cmds.ls(sl=1, fl=1)
        subSelTest= 1
        if obj:
            for item in obj:
                if "." not in item:
                    subSelTest= []
            if subSelTest:
                par= []
                for item in obj:
                    if item.split(".")[0] not in par:
                        par.append(item.split(".")[0])
                if len(par)==1:
                    skin= mel.eval("findRelatedSkinCluster %s"%par[0])
                    if skin:
                        self.uiStuffClass.loadingBar(1, 1)
                        mel.eval('weightHammerVerts;')
                        self.uiStuffClass.loadingBar(2)
                        self.uiStuffClass.loadingBar(3)
                    else:
                        cmds.warning("The selected object is not skinned")
                else:
                    cmds.warning("Please select the SUBSELECTIONS from only 1 OBJECT")
            else:
                cmds.warning("One of the selection is not a subSelection (Vertex/Edge/Face)")
        else:
            cmds.warning("Please select subSelection (Vertex/Edge/Face)")
        
    def removeUnusedInfluence(self, tar=[], unpause=[]):
        if tar==[]:
            tar= cmds.ls(sl=1)
        noSkin=[]
        for item in tar:
            skinClusterName= mel.eval("findRelatedSkinCluster %s"%item)
            if skinClusterName =="":
                noSkin.append(item)
        if unpause:
            conti1= 1    
        else:
            conti1= self.dialogClass.printingDialog(noSkin, "< %s > successful\n< %s > does not have skinCluster"%(len(tar)-len(noSkin), len(noSkin)))                       
        if conti1:
            if tar:
                self.uiStuffClass.loadingBar(1, len(tar)*2)
                self.uiStuffClass.loadingBar(2)
                for item in tar:
                    #remove unused influence
                    try:
                        skinClusterName= mel.eval("findRelatedSkinCluster %s"%item)
                        if skinClusterName:
                            cmds.select(item)
                            mel.eval("removeUnusedInfluences")
                    except:
                        pass
                    #remove influence color
                    try:
                        skinClusterName= mel.eval("findRelatedSkinCluster %s"%item)
                        if skinClusterName:
                            inf= cmds.listConnections("%s.influenceColor"%skinClusterName, c=1, p=1)
                            for x in range(0, len(inf)-1, 2):
                                if skinClusterName not in cmds.listConnections("%s.worldMatrix[0]"%inf[x+1].split(".")[0]):    
                                    cmds.disconnectAttr(inf[x+1], inf[x])    
                    except:
                        pass   
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=tar)   
            else:
                cmds.warning("Please select at least 1 OBJECT")

    def copyWeightSkinBack(self, sour, tar):
        oldSkin= mel.eval("findRelatedSkinCluster %s"%sour)
        skinMethod= cmds.skinCluster(oldSkin, sm=1, q=1)
        jnts= cmds.skinCluster(oldSkin, inf=1, q=1) 
        if mel.eval("findRelatedSkinCluster %s"%tar):
            cmds.skinCluster(tar, e=1, ub=1)          
        newSkin= cmds.skinCluster(jnts, tar, tsb=1, sm=skinMethod)                                 
        cmds.copySkinWeights(nm=1, sa="closestPoint", ia=("name", "closestJoint"), ss=oldSkin, ds=newSkin[0])
        return oldSkin, newSkin

    def skinBack(self, meth):
        obj= cmds.ls(sl=1)
        testNotSame, allCompare= 1,[]
        conti1= self.testPreSkinCluster(obj)
        if conti1:
            self.uiStuffClass.loadingBar(1, len(obj)+1)
            self.uiStuffClass.loadingBar(2)
            #Test is it back to bindPose
            for item in obj:           
                dup= cmds.duplicate(item)
                self.unbindSkin(2, [item], [])
                #Use cmds.dagpose will be faster but have issue (eg. shirt mesh  get this warning even if ankle is not inf and somehow got value but its not moved)
                #polyCompare wont detect if just mesh translate/rotate but if joint move is considered as shape change
                #but skinBack is about skinning object so should be ok
                compare= cmds.polyCompare(item, dup[0])
                self.bindBack([item], [])
                cmds.delete(dup)
                if compare==1:
                    allCompare= 1 
                    break
            #Final
            if allCompare==[]:
                for item in obj:
                    dup= cmds.duplicate(item)
                    if meth==1:
                        oldSkin, newSkin1= self.copyWeightSkinBack(item, dup[0])
                        oldSkin1, newSkin=self.copyWeightSkinBack(dup[0], item)
                        cmds.delete(dup[0])
                    elif meth==2:
                        oldSkin, newSkin= self.copyWeightSkinBack(item, dup[0])
                        cmds.delete(item)
                        newTar= cmds.rename(dup[0], item)
                    cmds.rename(newSkin, oldSkin)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=obj)
            else:
                self.uiStuffClass.loadingBar(3, sel=obj)
                cmds.warning("Please go back to bindPose before doing this")

    def pruneWeight(self):
        obj= cmds.ls(sl=1)
        prune= cmds.floatSliderGrp(self.slider51, q=1, v=1) 
        if obj:
            conti1= self.testPreSkinCluster(obj) 
            if conti1:   
                self.uiStuffClass.loadingBar(1, len(obj))
                lockJnt= []
                for item in obj:
                    skin= mel.eval("findRelatedSkinCluster %s"%item)
                    jnt= cmds.skinCluster(skin, inf=1, q=1)  

                    #Prune weight cant work with locked joint      
                    for subJnt in jnt:
                        if cmds.getAttr("%s.liw"%subJnt)==1:
                            cmds.setAttr("%s.liw"%subJnt, 0)
                            if subJnt not in lockJnt:
                                lockJnt.append(subJnt)
                    cmds.skinPercent(skin, prw=prune)
                    self.uiStuffClass.loadingBar(2)
                
                #Lock back jnt    
                if lockJnt:
                    for subJnt in lockJnt: 
                        cmds.setAttr("%s.liw"%subJnt, 1)   
                self.uiStuffClass.loadingBar(3)        
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def mirWeight(self, meth):
        obj= cmds.ls(sl=1)
        if cmds.radioButtonGrp(self.rbMir2, sl=1, q=1)==1:
            mir="XY"
        elif cmds.radioButtonGrp(self.rbMir2, sl=1, q=1)==2:
            mir="YZ"
        else:
            mir="XZ"        
        if len(obj)>=1:
            test1=1 
            for item in obj:
                skinClusterName= mel.eval("findRelatedSkinCluster %s"%item)
                if skinClusterName=="":
                    test1=[]
            if test1:
                self.uiStuffClass.loadingBar(1, len(obj))
                for item in obj:
                    skinClusterName= mel.eval("findRelatedSkinCluster %s"%item)
                    if meth==1:
                        cmds.copySkinWeights(mm=mir, mi=1, sa="closestPoint", ia="closestJoint", ss=skinClusterName, ds=skinClusterName)
                    else:
                        cmds.copySkinWeights(mm=mir, sa="closestPoint", ia="closestJoint", ss=skinClusterName, ds=skinClusterName)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("One of the selected object does not have skinCluster") 
        else:
            cmds.warning("Please select 1 skinned object")

    def createDummySet(self):
        subSelect= cmds.ls(sl=1, fl=1)
        shp= cmds.ls(sl=1, o=1)
        test=1
        if subSelect:
            for item in subSelect:
                if ".f" not in item:
                    test=[]
            if test:
                if len(shp)==1:
                    self.uiStuffClass.loadingBar(1, 2)
                    self.uiStuffClass.loadingBar(2)
                    obj= subSelect[0].split(".")[0]
                    dup= cmds.duplicate(obj)
                    cmds.select((", ".join(subSelect). replace("%s"%(subSelect[0].split(".")[0]), "%s"%dup[0])).split(", "))
                    cmds.InvertSelection()
                    cmds.delete()
                    vert= cmds.polyListComponentConversion(subSelect, tv=1)    
                    cmds.sets(vert, n="SkinWeightVertex")
                    cmds.sets(dup[0], n="SkinWeightMesh")
                    cmds.xform(dup[0], cp=1)
                    if cmds.listRelatives(dup[0], p=1):
                        cmds.parent(dup[0], w=1)
                    attr= "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"
                    for item in attr:
                        cmds.setAttr("%s.%s"%(dup[0], item), k=1, l=0)
                    self.uiStuffClass.loadingBar(2)
                    self.uiStuffClass.loadingBar(3, sel=dup[0])
                else:
                    cmds.warning("Please select FACES from 1 object only")
            else:
                cmds.warning("Please select FACES only")
        else:
            cmds.warning("Please select FACES")

    def helps(self):
        name="Help On SkinWeight"
        helpTxt=""" 
        - Skinning functions



        < Skinning >
        =============
            1) Select Joint
            ------------------
                1. Select Joint Type Children
                    - Select all children that is joint type 

                2. Select Joint Type Children (Without Last)    
                    - Select all children that is joint type EXCEPT last joint (for heat map / mocap)  

                3. Skinned Joint
                    - Select joint that is skinned to object


            2) Binding  
            ------------
                1. Paint Type
                    Normal      : Paint according to joint hierarchy
                    Joint Chain : Paint as if it's joint chain according to selection order
                    Separate    : Paint as if it's individual separate joint  

                2. Normal Bind 
                    - Bind Method : Closest Distance
                    - Bind To : Selected joint   
                    - Drop off : 4

                3. Heat Map
                    - Bind To : Selected joint 
                    - Heat Map Falloff : 0.68

                4. Unbind / Unbind (Keep History)
                    - Unbind Delete History
                    - Unbind Keep History

                5. Bind Back
                    - Bind those skin that kept the history 
                    (*Cannot use <Normal Bind> because it will detect its existing skincluster and remove it)


        < Influence >
        =============
            1. Add Search Replace Influence
                - Add search replace influence base on the skinned influences
                (* Already have "Hand_L_jnt" so add "Hand_R_jnt")

            2. Add Object Influence
                - Add another's object skinned influence

            3. Add Influence
                - Locked weight

            4. Remove Influence
                - Also remove influence color
            

        < Weight >
        =============
            1. Copy Weight 
                - Bind with same joints + copy weight

            2. Replace Joint
                - Bind with search replace joint + copy Weight

            3. Replace Joint + Mirror
                - Bind with search replace joint + mirror weight + delete unused influence
                (* Mesh, joint is at opposite position)  

            (* Everything that have copy skin weight function will use "Name" then "Closest Joint" as influence association (Maya setting),
               this is so that even there's 2 different joint at same place, will still copy the weight correctly)
            (* Mirror weight, use back "Closest Joint")


        < Vertex Weight >
        ==================
            1. Copy Vertex weight
                - Similar to copy maya copy weight on vertex selection

            2. Convert
                - Convert vertex in textfield to another object's


        < Cleanup >
        =============
            1) Hammer Weight

            2) Remove Unused Influence
                - Also remove influence color

            3) Prune Weight Below

            4) Skin Back 
                - Same Mesh = copy weight to dummy then back
                - New Mesh = duplicate mesh, copy weight to new duplicate
                *To refresh weight, or fix history (like uv tweak or others)

            5) Mirror Weight 


        < Extra >
        =============
            - Create Dummy Mesh Set
                - Will create a dummy mesh base of selected face
                - Will create 2 sets:
                    - 1 is just now that dummy mesh
                    - 2 is the vertex selection on the original mesh
                (* This is to ease skinning by skin to a partial dummy mesh then copy weight using set selection)
                (* After select the vertex set MUST go to component mode and re-select one of the vertex 
                   or else maya wont register the vertex and copy weight wont work)

                (*eg. Hair got many joint Chain hairA1,A2.... hairB1,b12.. 
                     Select a part, A1 and re-create a mesh just to bind 
                     then in the end only copy weight back to original mesh)

        """
        self.helpBoxClass.helpBox1(name, helpTxt)    

    def reloadSub(self):
        SkinWeight()   
        

if __name__=='__main__':
    SkinWeight() 
                   
