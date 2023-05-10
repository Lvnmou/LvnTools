import maya.cmds as cmds
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox


class Constraints(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):
        try: 
            cmds.deleteUI("const") 
        except:
            pass    
        cmds.window("const", mb=1)              
        cmds.window("const", t="Constraints", s=1, e=1, wh=(280,500))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Constraints", c=lambda x:self.helps())        
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Constraints", c=lambda x:self.reloadSub())       
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Create")
        form1= cmds.formLayout(nd=100, p=column1)
        self.omType= cmds.optionMenuGrp(l="Type :", cw2=(50,10))
        cmds.menuItem(l="Normal")
        cmds.menuItem(l="Matrix")              
        self.omMeth= cmds.optionMenuGrp(l="Method :", cw2=(50,10))
        cmds.menuItem(l="One Parent to Multiple")
        cmds.menuItem(l="Multiple Parent to One")         
        sep11= cmds.separator(h=5, st="in")       
        self.cbMo= cmds.checkBoxGrp(l="Maintain Offset :", cw=(1,90), v1=1) 
        self.cbTran= cmds.checkBoxGrp(l="Translate :", la3=["X","Y","Z"], cw4=(90,50,50,50), ncb=3, va3=(1,1,1))   
        self.cbRot= cmds.checkBoxGrp(l="Rotate :", la3=["X","Y","Z"], cw4=(90,50,50,50), ncb=3, va3=(1,1,1)) 
        self.cbScal= cmds.checkBoxGrp(l="Scale :", la3=["X","Y","Z"], cw4=(90,50,50,50), ncb=3, va3=(1,1,1))   
        sep12= cmds.separator(h=5, st="in")
        self.cbTar= cmds.checkBoxGrp(l="", cw=(1,10), cc=lambda x:self.targ())  
        self.txtTar= cmds.textFieldButtonGrp(l="Targets :", tx="", en=0, cw3=(50,10,10), adj=2, bl="  Grab  ", bc=lambda :self.grab11())
        sep13= cmds.separator(h=5, st="in")      
        self.cbSR= cmds.checkBoxGrp(l="", cw=(1,10), cc=lambda x:self.sr())  
        self.txtSear= cmds.textFieldGrp(l="Search :", tx="", en=0, cw2=(50,10), adj=2)
        self.txtRepl= cmds.textFieldGrp(l="Replace :", tx="", en=0, cw2=(50,10), adj=2)
        sep14= cmds.separator(h=5, st="in") 
        txt11= cmds.text(l="Select SOURCES the TARGET", fn="smallObliqueLabelFont", en=0)  
        b11= cmds.button(l="Parent Constraint", c=lambda x:self.preAllCon(1))
        b12= cmds.button(l="Scale Constraint", c=lambda x:self.preAllCon(2))   
        b13= cmds.button(l="Point Constraint", c=lambda x:self.preAllCon(3))  
        b14= cmds.button(l="Orient Constraint", c=lambda x:self.preAllCon(4)) 
        cmds.formLayout(form1, e=1,
                                af=[(self.omType, "top", 0),
                                    (self.omMeth, "top", 26),
                                    (sep11, "top", 56),
                                    (self.cbMo, "top", 71),
                                    (self.cbTran, "top", 96),
                                    (self.cbRot, "top", 116),
                                    (self.cbScal, "top", 136),
                                    (sep12, "top", 161),
                                    (self.cbTar, "top", 181),
                                    (self.txtTar, "top", 175),
                                    (sep13, "top", 211),
                                    (self.cbSR, "top", 236),
                                    (self.txtSear, "top", 226),
                                    (self.txtRepl, "top", 249),
                                    (sep14, "top", 283),
                                    (txt11, "top", 301),
                                    (b11, "top", 317),
                                    (b12, "top", 317),
                                    (b13, "top", 343),
                                    (b14, "top", 343)],
                                ap=[(sep11, "left", 0, 0),
                                    (sep11, "right", 0, 100),
                                    (sep12, "left", 0, 0),
                                    (sep12, "right", 0, 100),
                                    (self.txtTar, "left", 40, 0),
                                    (self.txtTar, "right", 0, 100),
                                    (sep13, "left", 0, 0),
                                    (sep13, "right", 0, 100),
                                    (self.txtSear, "left", 40, 0),
                                    (self.txtSear, "right", 0, 100),
                                    (self.txtRepl, "left", 40, 0),
                                    (self.txtRepl, "right", 0, 100),
                                    (sep14, "left", 0, 0),
                                    (sep14, "right", 0, 100),
                                    (txt11, "left", 0, 0),
                                    (txt11, "right", 0, 100),
                                    (b11, "left", 0, 0),
                                    (b11, "right", 0, 50),
                                    (b12, "left", 0, 51),
                                    (b12, "right", 0, 100),
                                    (b13, "left", 0, 0),
                                    (b13, "right", 0, 50),
                                    (b14, "left", 0, 51),
                                    (b14, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column21= self.uiStuffClass.sepBoxSub("Edit")
        form21= cmds.formLayout(nd=100, p=column21)
        txt21= cmds.text(l="Select Constraint Parent", fn="smallObliqueLabelFont", en=0)
        b21= cmds.button(l="Find Constraint Child", c=lambda x:self.conChd()) 
        txt22= cmds.text(l="Select Connected Child", fn="smallObliqueLabelFont", en=0)
        b22= cmds.button(l="Delete Any Connected Constraints", c=lambda x:self.delCon()) 
        cmds.formLayout(form21, e=1,
                                af=[(txt21, "top", 0),
                                    (b21, "top", 16),
                                    (txt22, "top", 52),
                                    (b22, "top", 68)],
                                ap=[(txt21, "left", 0, 0),
                                    (txt21, "right", 0, 100),
                                    (txt22, "left", 0, 0),
                                    (txt22, "right", 0, 100),
                                    (b21, "left", 0, 0),
                                    (b21, "right", 0, 100),
                                    (b22, "left", 0, 0),
                                    (b22, "right", 0, 100)])          
        cmds.setFocus(cmds.text(l= ""))
        cmds.showWindow("const")


    def defi(self):
        self.obj= cmds.ls(sl=1)   
        self.mo= cmds.checkBoxGrp(self.cbMo, v1=1, q=1) 
        self.type= cmds.optionMenuGrp(self.omType, q=1, sl=1)         
        self.skipT, self.skipR, self.skipS= [],[],[]
        for skip,cbx in zip((self.skipT,self.skipR,self.skipS),(self.cbTran,self.cbRot,self.cbScal)):
            if cmds.checkBoxGrp(cbx, v1=1, q=1)==0:
                skip.append("x")
            if cmds.checkBoxGrp(cbx, v2=1, q=1)==0:
                skip.append("y")  
            if cmds.checkBoxGrp(cbx, v3=1, q=1)==0:
                skip.append("z")   
            if skip==[]:
                skip.append("none")
        self.tar= cmds.textFieldButtonGrp(self.txtTar, tx=1, q=1)   
        self.sear= cmds.textFieldGrp(self.txtSear, tx=1, q=1)
        self.repl= cmds.textFieldGrp(self.txtRepl, tx=1, q=1)        
        
    def grab11(self):
        obj= cmds.ls(sl=1)           
        if obj:      
            cmds.textFieldButtonGrp(self.txtTar, e=1, tx=", ".join(obj))                           
        else:
            cmds.warning("Select at least 1 TARGET")

    def targ(self):
        if cmds.checkBoxGrp(self.cbTar, q=1, v1=1):
            cmds.textFieldButtonGrp(self.txtTar, e=1, en=1)
            cmds.checkBoxGrp(self.cbSR, e=1, v1=0)
            cmds.textFieldGrp(self.txtSear, e=1, en=0)
            cmds.textFieldGrp(self.txtRepl, e=1, en=0)
            cmds.optionMenuGrp(self.omMeth, e=1, en=0)                 
        else:
            cmds.textFieldButtonGrp(self.txtTar, e=1, en=0)
            cmds.optionMenuGrp(self.omMeth, e=1, en=1)
                              
    def sr(self):
        if cmds.checkBoxGrp(self.cbSR, q=1, v1=1):
            cmds.textFieldGrp(self.txtSear, e=1, en=1)
            cmds.textFieldGrp(self.txtRepl, e=1, en=1)
            cmds.checkBoxGrp(self.cbTar, e=1, v1=0)
            cmds.textFieldButtonGrp(self.txtTar, e=1, en=0)   
            cmds.optionMenuGrp(self.omMeth, e=1, en=0) 
        else:
            cmds.textFieldGrp(self.txtSear, e=1, en=0)
            cmds.textFieldGrp(self.txtRepl, e=1, en=0)
            cmds.optionMenuGrp(self.omMeth, e=1, en=1)     
    
    def preAllCon(self, meth):
        self.defi()
        if cmds.checkBoxGrp(self.cbSR, q=1, v1=1):
            if self.obj:
                conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(self.obj, self.sear, self.repl)
                if conti:
                    self.allCon(self.obj, self.obj, meth, 1)
                    cmds.select(self.obj)
            else:
                cmds.warning("Please select at least 1 SOURCE")
        elif cmds.checkBoxGrp(self.cbTar, q=1, v1=1): 
            if self.tar:
                if self.obj:
                    self.allCon(self.obj, self.tar.split(", "), meth, 0)
                    cmds.select(self.obj)
                else:
                    cmds.warning("Please select at least 1 OBJECT")
            else:
                cmds.warning("<TARGET> textfield is empty!")  
        else:
            if len(self.obj)>=2:
                if cmds.optionMenuGrp(self.omMeth, q=1, sl=1)==1: 
                    self.allCon([self.obj[0]], self.obj[1:], meth, 0)
                else:
                    self.allCon(self.obj[:-1], [self.obj[-1]], meth, 0)
                cmds.select(self.obj)
            else:
                cmds.warning("Please select at least 1 SOURCE and 1 TARGET")

    def allCon(self, allObj, allTar, meth, sr):
        if self.type==2:
            tranRotScal= []
            if meth==1:
                tranRotScal.append("Translate")
                tranRotScal.append("Rotate")
            elif meth==2:
                tranRotScal.append("Scale")
            elif meth==3:
                tranRotScal.append("Translate")
            elif meth==4:
                tranRotScal.append("Rotate")
            wam, dcmF, allDcmF= [],[],[]
            if sr==1:
                for item in allObj:
                    self.matrixCon(item, item.replace(self.sear,self.repl), allObj, meth, tranRotScal, wam)
            else:
                for stuff in allTar:
                    if len(allObj)>1:
                        wam= cmds.createNode("wtAddMatrix", n="%s_wam"%("_").join(allObj))
                        dcmF= cmds.createNode("decomposeMatrix", n="%s_testC_dcm"%("_").join(allObj))  
                        cmds.addAttr(stuff, ln="matrixConstraint", at="bool")
                        cmds.setAttr("%s.matrixConstraint"%stuff, k=1, l=1)
                    for item in allObj:    
                        self.matrixCon(item, stuff, allObj, meth, tranRotScal, wam)
                    if len(allObj)>1:
                        cmds.connectAttr("%s.matrixSum"%wam,"%s.inputMatrix"%dcmF)
                        for trs in tranRotScal:
                            for attr in ("X","Y","Z"):
                                test1= 1
                                if trs=="Translate":
                                    if str.lower(attr) in self.skipT:
                                        test1=[]
                                elif trs=="Rotate":
                                    if str.lower(attr) in self.skipR:
                                        test1=[]
                                elif trs=="Scale":
                                    if str.lower(attr) in self.skipS:
                                        test1=[]
                                if test1:
                                    cmds.connectAttr("%s.output%s%s"%(dcmF,trs,attr),"%s.%s%s"%(stuff,str.lower(trs),attr)) 
        else:
            if sr==1:
                self.uiStuffClass.loadingBar(1, len(allObj))
                for item in allObj:
                    self.normCon(item, item.replace(self.sear, self.repl), meth)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
            else:
                self.uiStuffClass.loadingBar(1, len(allObj)*len(allTar))
                for item in allObj:
                    for stuff in allTar:
                        self.normCon(item, stuff, meth)
                        self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)

    def matrixCon(self, sour, tar, allObj, meth, tranRotScal, wam):
        mm= cmds.createNode("multMatrix", n="%s_mm"%sour)
        if meth==1:
            dcm4= cmds.createNode("decomposeMatrix", n="%s_parentC_dcm"%sour)        
        if meth==2:
            dcm4= cmds.createNode("decomposeMatrix", n="%s_scaleC_dcm"%sour)
        elif meth==3:
            dcm4= cmds.createNode("decomposeMatrix", n="%s_pointC_dcm"%sour)
        elif meth==4:
            dcm4= cmds.createNode("decomposeMatrix", n="%s_orientC_dcm"%sour)           
        if cmds.checkBoxGrp(self.cbMo, q=1, v1=1)==1: 
            dcm1= cmds.createNode("decomposeMatrix", n="%s_wm_dcm"%tar)
            dcm2= cmds.createNode("decomposeMatrix", n="%s_wim_dcm"%sour)
            dcm1Val= cmds.getAttr("%s.worldMatrix"%tar)
            dcm2Val= cmds.getAttr("%s.worldInverseMatrix"%sour)
            cmds.setAttr("%s.inputMatrix"%dcm1, dcm1Val, typ="matrix")
            cmds.setAttr("%s.inputMatrix"%dcm2, dcm2Val, typ="matrix")
            if meth==3:
                #Im not sure is there any other better way...
                dcmTran= cmds.getAttr("%s.outputTranslate"%dcm1)
                dcmScal= cmds.getAttr("%s.outputScale"%dcm1)
                cmTemp= cmds.createNode("composeMatrix", n="%s_wm_cm"%tar)
                cmds.setAttr("%s.inputTranslate"%cmTemp, dcmTran[0][0], dcmTran[0][1], dcmTran[0][2])
                cmds.setAttr("%s.inputScale"%cmTemp, dcmScal[0][0], dcmScal[0][1], dcmScal[0][2])
                dcmNoOrient= cmds.createNode("decomposeMatrix", n="%s_wm_noOrient_dcm"%tar)
                cmVal= cmds.getAttr("%s.outputMatrix"%cmTemp)
                cmds.setAttr("%s.inputMatrix"%dcmNoOrient, cmVal, typ="matrix")
                cmds.connectAttr("%s.worldMatrix"%sour,"%s.matrixIn[0]"%mm)
                cmds.connectAttr("%s.inputMatrix"%dcm2,"%s.matrixIn[1]"%mm)  
                cmds.connectAttr("%s.inputMatrix"%dcmNoOrient,"%s.matrixIn[2]"%mm)
                cmds.delete(cmTemp, dcm1)
            else:
                cmds.connectAttr("%s.inputMatrix"%dcm1,"%s.matrixIn[0]"%mm)
                cmds.connectAttr("%s.inputMatrix"%dcm2,"%s.matrixIn[1]"%mm) 
                cmds.connectAttr("%s.worldMatrix"%sour,"%s.matrixIn[2]"%mm)
        dcm3= cmds.createNode("decomposeMatrix", n="%s_pim_dcm"%tar)
        dcm3Val= cmds.getAttr("%s.parentInverseMatrix"%tar)
        cmds.setAttr("%s.inputMatrix"%dcm3, dcm3Val, typ="matrix")  
        if cmds.checkBoxGrp(self.cbMo, q=1, v1=1)==1:
            cmds.connectAttr("%s.inputMatrix"%dcm3,"%s.matrixIn[3]"%mm) 
        else:
            cmds.connectAttr("%s.worldMatrix"%sour,"%s.matrixIn[0]"%mm)
            cmds.connectAttr("%s.inputMatrix"%dcm3,"%s.matrixIn[1]"%mm)  
        if wam:
            cmds.connectAttr("%s.matrixSum"%mm,"%s.wtMatrix[%s].matrixIn"%(wam,allObj.index(sour)))
            cmds.addAttr(tar, ln="%sW%s"%(sour.split("|")[-1],allObj.index(sour)), at="float")
            cmds.setAttr("%s.%sW%s"%(tar,sour.split("|")[-1],allObj.index(sour)), 1.0/len(allObj), k=1)
            cmds.connectAttr("%s.%sW%s"%(tar,sour.split("|")[-1],allObj.index(sour)),"%s.wtMatrix[%s].weightIn"%(wam,allObj.index(sour)))
        else:
            cmds.connectAttr("%s.matrixSum"%mm,"%s.inputMatrix"%dcm4)
            if cmds.objectType(tar)!="joint":
                for trs in tranRotScal:
                    for attr in ("X","Y","Z"):
                        test1= 1
                        if trs=="Translate":
                            if str.lower(attr) in self.skipT:
                                test1=[]
                        elif trs=="Rotate":
                            if str.lower(attr) in self.skipR:
                                test1=[]
                        elif trs=="Scale":
                            if str.lower(attr) in self.skipS:
                                test1=[]
                        if test1:
                            cmds.connectAttr("%s.output%s%s"%(dcm4,trs,attr),"%s.%s%s"%(tar,str.lower(trs),attr))
            else:
                if "Rotate" not in tranRotScal:
                    for trs in tranRotScal:
                        for attr in ("X","Y","Z"):
                            test1= 1
                            if trs=="Translate":
                                if str.lower(attr) in self.skipT:
                                    test1=[]
                            elif trs=="Scale":
                                if str.lower(attr) in self.skipS:
                                    test1=[]
                            if test1:                            
                                cmds.connectAttr("%s.output%s%s"%(dcm4,trs,attr),"%s.%s%s"%(tar,str.lower(trs),attr))
                else:
                    etq= cmds.createNode("eulerToQuat", n="%s_etq"%tar)
                    qin= cmds.createNode("quatInvert", n="%s_qin"%tar)
                    qprod= cmds.createNode("quatProd", n="%s_qprod"%tar)
                    qte= cmds.createNode("quatToEuler", n="%s_qte"%tar)
                    cmds.connectAttr("%s.jointOrient"%tar,"%s.inputRotate"%etq)
                    cmds.connectAttr("%s.outputQuat"%etq,"%s.inputQuat"%qin)
                    cmds.connectAttr("%s.outputQuat"%dcm4,"%s.input1Quat"%qprod)
                    cmds.connectAttr("%s.outputQuat"%qin,"%s.input2Quat"%qprod)
                    cmds.connectAttr("%s.outputQuat"%qprod,"%s.inputQuat"%qte)
                    for attr in ("X","Y","Z"):
                        test1= 1
                        if str.lower(attr) in self.skipR:
                            test1=[]
                        if test1:
                            cmds.connectAttr("%s.outputRotate%s"%(qte,attr),"%s.rotate%s"%(tar,attr))     
                    for trs in tranRotScal:
                        if trs is not "Rotate":
                            for attr in ("X","Y","Z"):
                                test1= 1
                                if trs=="Translate":
                                    if str.lower(attr) in self.skipT:
                                        test1=[]
                                elif trs=="Scale":
                                    if str.lower(attr) in self.skipS:
                                        test1=[]
                                if test1:
                                    cmds.connectAttr("%s.output%s%s"%(dcm4,trs,attr),"%s.%s%s"%(tar,str.lower(trs),attr))       


    def normCon(self, sour, tar, meth):
        if meth==1:
            cmds.parentConstraint(sour, tar, mo=self.mo, w=1, st=self.skipT, sr=self.skipR) 
        elif meth==2:
            cmds.scaleConstraint(sour, tar, mo=self.mo, w=1, sk=self.skipS)
        elif meth==3:
            cmds.pointConstraint(sour, tar, mo=self.mo, w=1, sk=self.skipT)
        else:
            cmds.orientConstraint(sour, tar, mo=self.mo, w=1, sk=self.skipR)

    def conChd(self):
        self.defi()
        finalTar= []
        if self.obj:
            for item in self.obj:
                allCon= []
                con= cmds.listConnections("%s.parentMatrix"%item)
                if con:
                    for thing in con:
                        if thing not in allCon:
                            allCon.append(thing)
                    if allCon:
                        for subCon in allCon:
                            if subCon not in finalTar:
                                allTar= cmds.listConnections("%s.constraintParentInverseMatrix"%subCon)
                                finalTar.append(allTar[0])
        if finalTar:
            cmds.select(finalTar)
        else:
            cmds.warning("Selected object does not have a CONSTRAINT CHILD") 

    def delCon(self):
        self.defi()
        allCon=[]
        for item in self.obj:
            con= cmds.listConnections("%s.parentInverseMatrix"%item)
            if con:
                for thing in con:
                    if thing not in allCon:
                        allCon.append(thing)
        if allCon:
            cmds.delete(allCon)
        else:
            cmds.warning("There is no constraint to delete")        

    def helps(self):
        name="Help On Constraints"
        helpTxt=""" 
        - Parent / Point / Orient / Scale Constraint (with share tickbox) (Doesn't have Aim Constraint)
        - Able to constraint using matrix



        < Create >
        ===========
            1) Type
            --------
                - Matrix (Good for customize)
                - Normal (Maya Constraint)   

            2) Method
            ------------
                - Mainly to clarify which is parent / child without using "target textfield"

                1. One Parent to Multi
                    - 1st will be "SOURCE"
                    - 2nd onwards are "TARGETS"

                2. Multiple Parent to One
                    - 1st to 2nd last is "SOURCES"
                    - Last is "TARGET"


        < Edit >
        ==========
            1) Find Constraint Child
                - Select Constraint Parent to find constrained object (without going to Node Editor)

            2) Delete Connected Constraints
                - Delete every connected constraints


        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)
             
    def reloadSub(self):
        Constraints()  
                         

if __name__=='__main__':
    Constraints() 