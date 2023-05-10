import maya.cmds as cmds
import Mod.sepBox as sepBox
import Mod.helpBox as helpBox


class CtrlSetup(object):
    def __init__(self, *args):
        self.sepBoxClass= sepBox.SepBox()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):       
        try: 
            cmds.deleteUI("ctrlSet") 
        except:
            pass    
        cmds.window("ctrlSet", mb=1)              
        cmds.window("ctrlSet", t="Ctrl Setup", s=1, e=1, wh=(200,79))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on CtrlSetup", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload CtrlSetup", c=lambda x:self.reloadSub())    
        column1 = self.sepBoxClass.sepBoxMain() 
        form1= cmds.formLayout(nd=100, p=column1) 
        self.txtAssN= cmds.textFieldGrp(l="Asset Name :", tx="", pht="<xxx_setup", cw2=(70,100), adj=2)  
        self.txtSear= cmds.textFieldGrp(l="Search :", tx="_L", cw2=(45,50), adj=2) 
        self.txtRepl= cmds.textFieldGrp(l="Replace :", tx="_R", cw2=(55,50), adj=2) 
        self.txtSfx= cmds.textFieldGrp(l="Suffix :", tx="jnt", cw2=(50,50), adj=2) 
        sep1= cmds.separator(h=5, st="in")
        self.cb= cmds.checkBoxGrp(ncb=1, l="", cw2=(3,100), v1=0, cc=lambda x:self.cbx2())    
        self.txtNoFlip= cmds.textFieldButtonGrp(l="No Flip :", tx="", en=0, pht="<Can be left blank>", cw3=(42,100,100), adj=2, bl="  Grab  ", bc=lambda :self.grab())  
        sep2= cmds.separator(h=5, st="in")
        txt1= cmds.text(l="Select JOINTS including NO FLIP", fn="smallObliqueLabelFont", en=0) 
        txt2= cmds.text(l="Select PARENT JOINT", fn="smallObliqueLabelFont", en=0) 
        b1= cmds.button(l="Normal", c=lambda x:self.normal())
        b2= cmds.button(l="Parent", c=lambda x:self.withParent())
        sep3= cmds.separator(h=5, st="in")
        b3= cmds.button(l="Example", c=lambda x:self.example(1))
        b4= cmds.button(l="Example", c=lambda x:self.example(2))
        cmds.formLayout(form1, e=1,
                                af=[(self.txtAssN, "top", 0),
                                    (self.txtSear, "top", 30),
                                    (self.txtRepl, "top", 30),
                                    (self.txtSfx, "top", 30),
                                    (sep1, "top", 60),
                                    (self.cb, "top", 80),
                                    (self.txtNoFlip, "top", 75),
                                    (sep2, "top", 110),
                                    (txt1, "top", 130),
                                    (txt2, "top", 130),
                                    (b1, "top", 145),
                                    (b2, "top", 145),
                                    (sep3, "top", 175),
                                    (b3, "top", 180),
                                    (b4, "top", 180)],
                                ap=[(self.txtAssN, "left", 0, 0),
                                    (self.txtAssN, "right", 0, 100),
                                    (self.txtSear, "left", 0, 0),
                                    (self.txtSear, "right", 0, 33),
                                    (self.txtRepl, "left", 0, 34),
                                    (self.txtRepl, "right", 0, 66),
                                    (self.txtSfx, "left", 0, 67),
                                    (self.txtSfx, "right", 0, 100),
                                    (sep1, "left", 0, 0),
                                    (sep1, "right", 0, 100),
                                    (self.txtNoFlip, "left", 30, 0),
                                    (self.txtNoFlip, "right", 0, 100),
                                    (sep2, "left", 0, 0),
                                    (sep2, "right", 0, 100),
                                    (txt1, "left", 0, 0),
                                    (txt1, "right", 0, 50),
                                    (txt2, "left", 0, 51),
                                    (txt2, "right", 0, 100),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 50),
                                    (b2, "left", 0, 51),
                                    (b2, "right", 0, 100),
                                    (sep3, "left", 0, 0),
                                    (sep3, "right", 0, 100),
                                    (b3, "left", 0, 0),
                                    (b3, "right", 0, 50),
                                    (b4, "left", 0, 51),
                                    (b4, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        cmds.showWindow("ctrlSet")

    def cbx2(self):
        if cmds.checkBoxGrp(self.cb, q=1, v1=1):    
            cmds.textFieldButtonGrp(self.txtNoFlip, e=1, en=1)
        else:
            cmds.textFieldButtonGrp(self.txtNoFlip, e=1, en=0)   

    def defi(self):
        self.obj= cmds.ls(sl=1)
        self.sear= cmds.textFieldGrp(self.txtSear, q=1, tx=1) 
        self.repl= cmds.textFieldGrp(self.txtRepl, q=1, tx=1) 
        self.jnt= cmds.textFieldGrp(self.txtSfx, q=1, tx=1)  
        self.assN= cmds.textFieldGrp(self.txtAssN, q=1, tx=1) 
        self.noFlip= cmds.textFieldGrp(self.txtNoFlip, q=1, tx=1) 
        self.flipObj= self.obj + ", ".join(self.obj).replace(self.sear, self.repl).split(", ")
        self.child= cmds.listRelatives(self.obj, pa=1, c=1)
        if self.child:
            self.flipChild= (", ".join(self.child) + ", " + ", ".join(self.child).replace(self.sear, self.repl)).split(", ") 
            self.flipObjPar= (", ".join(self.obj + ", ".join(self.obj).replace(self.sear, self.repl).split(", "))).split(", ") + self.flipChild
        else:
            self.flipChild, self.flipObjPar= [], []    
        if cmds.checkBoxGrp(self.cb, q=1, v1=1):    
            if self.noFlip:
                for stuff in self.noFlip.split(", "):
                    try:
                        self.flipObj.remove(stuff.replace(self.sear, self.repl))  
                    except:
                        pass
                    if self.child:
                        try:
                            self.flipObjPar.remove(stuff.replace(self.sear, self.repl))
                            self.flipChild.remove(stuff.replace(self.sear, self.repl))
                        except:
                            pass   

    def grab(self):
        obj= cmds.ls(sl=1)           
        if obj:      
            cmds.textFieldButtonGrp(self.txtNoFlip, e=1, tx=", ".join(obj))                           
        else:
            cmds.warning("Select at least one target")  

    def preTest(self, tar):
        allGood, test1, test2, test3, test4, test5, test6= 1,1,1,1,1,1,1
        if self.sear and self.jnt:
            if cmds.objExists("%s_setup"%self.assN)==0:
                if cmds.checkBoxGrp(self.cb, q=1, v1=1):
                    if self.noFlip:
                        for item in self.noFlip.split(", "):
                            if item not in tar:
                                test1=[]               
                #self.noFlip cannot test "L" "R" but can test "self.jnt"
                for item in tar:
                    if self.noFlip:
                        if item not in self.noFlip.split(", "):
                            if item.replace(self.sear, self.repl)==item:
                                test2=[]
                            else:
                                if cmds.objExists(item.replace(self.sear, self.repl))==1:
                                    test3=[]      
                    else:
                        if item.replace(self.sear, self.repl)==item:
                            test2=[]
                        else:
                            if cmds.objExists(item.replace(self.sear, self.repl))==1:
                                test3=[] 
                    if "|" in item:
                        test6= []                
                for item in self.flipObj:           
                    if item.replace(self.jnt, "")==item:
                        test4=[]
                    else:
                        if item.split(self.jnt)[1]:
                            test5=[]       
                if test1==[] or test2==[] or test3==[] or test4 ==[]or test5==[] or test6==[]:
                    allGood=[]
                if test1==[]:  
                    cmds.warning("One of the <Noflip> is not selected (Or not under the parent joint *for parent function*)")    
                if test2==[]:  
                    cmds.warning("There is no '%s' in one of the the selected object"%self.sear)
                if test3==[]:  
                    cmds.warning("There are object with same name after <Search & Replace>")
                if test4==[]:
                    if self.jnt:  
                        cmds.warning("There is no '%s' as <joint suffix> in the selected object"%self.jnt)
                    else:
                        cmds.warning("There is no <joint suffix>")
                if test5==[]:  
                    cmds.warning("There are alphabets after <joint suffix> '%s'"%self.jnt)
                if test6==[]:
                    cmds.warning("There is same name object in the scene with one of the selected object, please rename")    
            else:
                cmds.warning("<%s_setup> already exist in the scene, please type another Asset Name"%self.assN)
                allGood=[]
        else:
            allGood=[]
            cmds.warning("Search textfield is empty!")    
        return allGood

    def jointSetup(self, tar):
        attr=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
        par= cmds.group(n="%s%s_%s_grp"%(self.assN, self.sear, self.jnt), em=1)
        mainPar= cmds.group(n="%s_setup"%self.assN, em=1)
        noScaleGrp= cmds.group(n="%s_noScaleGrp"%self.assN, em=1, p=mainPar)
        scaleGrp= cmds.group(n="%s_scaleGrp"%self.assN, em=1, p=mainPar)
        self.jntPar= cmds.group(n="%s_jntGrp"%self.assN, em=1, p=scaleGrp)
        self.ctrlPar= cmds.group(n="%s_ctrlGrp"%self.assN, em=1, p=scaleGrp)
        self.surfPar= cmds.group(n="%s_srfGrp"%self.assN, em=1, p=noScaleGrp) 
        #jnt         
        for item in tar:
            cmds.makeIdentity(item, a=1, t=1, r=1, s=1, n=0, pn=1)      
            grp1= cmds.group(n="%s"%item.replace(self.jnt, "%s_grp1"%self.jnt), em=1, p=item)
            cmds.parent(grp1, w=1)
            grp2= cmds.duplicate(grp1, n="%s"%grp1.replace("grp1","grp2")) 
            offset= cmds.duplicate(grp1, n="%s"%grp1.replace("grp1","offset")) 
            cmds.parent(item, grp1)
            cmds.parent(grp1, grp2)
            cmds.parent(grp2, offset)
            cmds.parent(offset, par)
        #ctrl
        dupCtrl= cmds.duplicate(par, n="%s"%par.replace(self.jnt, "ctrl"))
        for item in tar:
            cmds.delete("%s|%s_offset|%s_grp2|%s_grp1|%s"%(dupCtrl[0], item, item, item, item))
            ctrlGrp1= cmds.rename("%s|%s_offset|%s_grp2|%s_grp1"%(dupCtrl[0], item, item, item), item.replace(self.jnt,"ctrl_grp1"))
            cmds.rename("%s|%s_offset|%s_grp2"%(dupCtrl[0], item, item), item.replace(self.jnt,"ctrl_grp2"))
            cmds.rename("%s|%s_offset"%(dupCtrl[0], item), item.replace(self.jnt,"ctrl_offset"))
            sh= cmds.curve(d=1, n="%s"%item.replace(self.jnt, "ctrl"), p=[(-0.25,0.25,0.25), (-0.25,0.25,-0.25), (0.25,0.25,-0.25), (0.25,0.25,0.25), (-0.25,0.25,0.25), (-0.25,-0.25,0.25), (0.25,-0.25,0.25), (0.25,0.25,0.25), (0.25,-0.25,0.25), (0.25,-0.25,-0.25), (0.25,0.25,-0.25), (0.25,-0.25,-0.25), (-0.25,-0.25,-0.25), (-0.25,0.25,-0.25), (-0.25,-0.25,-0.25), (-0.25,-0.25,0.25)])
            shName= cmds.listRelatives(sh, pa=1, c=1, typ="nurbsCurve")
            cmds.setAttr("%s.overrideEnabled"%shName[0], 1)   
            cmds.setAttr("%s.overrideColor"%shName[0], 18)
            cmds.rename(shName, "%sShape"%item.replace(self.jnt, "ctrl"))
            cmds.parent(sh, ctrlGrp1)  
            cmds.setAttr("%s.t"%sh, 0,0,0) 
            cmds.setAttr("%s.r"%sh, 0,0,0) 
        #No Flip  
        if cmds.checkBoxGrp(self.cb, q=1, v1=1):
            if self.noFlip:
                nfJntPar= cmds.group(n="%s_noFlip_%s_grp"%(self.assN, self.jnt), em=1, p=self.jntPar)
                nfCtrlPar= cmds.group(n="%s_noFlip_ctrl_grp"%self.assN, em=1, p=self.ctrlPar)      
                for stuff in self.noFlip.split(", "):
                    cmds.parent("%s_offset"%stuff, nfJntPar)
                    cmds.parent("%s_offset"%stuff.replace(self.jnt, "ctrl"), nfCtrlPar)       
        #Duplicate R  
        opp= par, dupCtrl[0]
        test=1
        for thing in opp:
            dup2= cmds.duplicate(thing, n=thing.replace(self.sear, self.repl))
            dups= cmds.listRelatives(dup2[0], ad=1, pa=1)
            if dups:
                for old in dups:
                    new= cmds.rename(old, (old.split("|")[-1]).replace(self.sear, self.repl))            
                cmds.setAttr("%s.sx"%dup2[0], -1)
            else:
                cmds.delete(dup2)
                cmds.delete(thing)
                test=[]
        if test:        
            cmds.parent(par, self.jntPar)
            cmds.parent(par.replace(self.sear, self.repl), self.jntPar)
            cmds.parent(dupCtrl[0], self.ctrlPar)
            cmds.parent(dupCtrl[0].replace(self.sear, self.repl), self.ctrlPar)
        else:
            ch1= cmds.listRelatives("%s_noFlip_%s_grp"%(self.assN, self.jnt), c=1, pa=1)
            ch2= cmds.listRelatives("%s_noFlip_ctrl_grp"%self.assN, c=1, pa=1)
            for chd1 in ch1:
                cmds.parent(chd1, self.jntPar)
            for chd2 in ch2:
                cmds.parent(chd2, self.ctrlPar)
            cmds.delete("%s_noFlip_%s_grp"%(self.assN, self.jnt), "%s_noFlip_ctrl_grp"%self.assN)          
        #Connect to joint
        for item in tar:
            ctrl= item.replace(self.jnt, "ctrl")
            for thing in attr:
                cmds.connectAttr("%s.%s"%(ctrl, thing), "%s.%s"%(item, thing))
                cmds.connectAttr("%s_grp1.%s"%(ctrl, thing), "%s_grp1.%s"%(item, thing))
                cmds.connectAttr("%s_grp2.%s"%(ctrl, thing), "%s_grp2.%s"%(item, thing)) 
                cmds.connectAttr("%s_offset.%s"%(ctrl, thing), "%s_offset.%s"%(item, thing))
                if cmds.checkBoxGrp(self.cb, q=1, v1=1):
                    if self.noFlip: 
                        if item not in self.noFlip.split(", "):
                            cmds.connectAttr("%s.%s"%(ctrl.replace(self.sear, self.repl), thing), "%s.%s"%(item.replace(self.sear, self.repl), thing))
                            cmds.connectAttr("%s_grp1.%s"%(ctrl.replace(self.sear, self.repl), thing), "%s_grp1.%s"%(item.replace(self.sear, self.repl), thing))
                            cmds.connectAttr("%s_grp2.%s"%(ctrl.replace(self.sear, self.repl), thing), "%s_grp2.%s"%(item.replace(self.sear, self.repl), thing))
                            cmds.connectAttr("%s_offset.%s"%(ctrl.replace(self.sear, self.repl), thing), "%s_offset.%s"%(item.replace(self.sear, self.repl), thing))
                else:
                    cmds.connectAttr("%s.%s"%(ctrl.replace(self.sear, self.repl), thing), "%s.%s"%(item.replace(self.sear, self.repl), thing))
                    cmds.connectAttr("%s_grp1.%s"%(ctrl.replace(self.sear, self.repl), thing), "%s_grp1.%s"%(item.replace(self.sear, self.repl), thing))
                    cmds.connectAttr("%s_grp2.%s"%(ctrl.replace(self.sear, self.repl), thing), "%s_grp2.%s"%(item.replace(self.sear, self.repl), thing))
                    cmds.connectAttr("%s_offset.%s"%(ctrl.replace(self.sear, self.repl), thing), "%s_offset.%s"%(item.replace(self.sear, self.repl), thing))

    def surfaceC(self, source, tar):
        for item in source:
            surf=cmds.nurbsPlane(n="%s"%item.replace(self.jnt, "srf"), ax=[0,1,0], d=1, ch=0, lr=1, w=(0.1))[0]
            tran= cmds.xform(item, q=1, rp=1, ws=1)
            rot= cmds.xform(item, q=1, ro=1, ws=1)
            cmds.move(tran[0], tran[1], tran[2], surf, r=1)
            cmds.rotate(rot[0], rot[1], rot[2], surf, os=1,  r=1)  
            cmds.makeIdentity(surf, a=1, t=1, r=1, s=1, n=0, pn=1)
            #Surface Constraint
            space= item.replace(self.jnt, tar)
            pos= cmds.xform(item, q=1, rp=1, ws=1)
            cmds.move(pos[0], pos[1], pos[2], space)
            posi= cmds.createNode("pointOnSurfaceInfo", n="%s_posi"%surf.split("|")[-1]) 
            fbfm= cmds.createNode("fourByFourMatrix", n="%s_fbfm"%surf.split("|")[-1]) 
            dcm= cmds.createNode("decomposeMatrix", n="%s_dcm"%surf.split("|")[-1])
            mm= cmds.createNode("multMatrix", n="%s_mm"%surf.split("|")[-1])  
            for stuff in posi, fbfm, dcm, mm:
                cmds.setAttr("%s.ihi"%stuff, 0)
            cmds.connectAttr("%s.local"%surf, "%s.inputSurface"%posi)
            cmds.setAttr("%s.parameterU"%posi, 0.5)
            cmds.setAttr("%s.parameterV"%posi, 0.5)         
            attr=["X", "Y", "Z"]
            for thing, stuff in enumerate(attr):
                cmds.connectAttr("%s.normalizedTangentU%s"%(posi,stuff), "%s.in0%s"%(fbfm, thing))        
                cmds.connectAttr("%s.normalizedNormal%s"%(posi,stuff), "%s.in1%s"%(fbfm, thing))        
                cmds.connectAttr("%s.normalizedTangentV%s"%(posi,stuff), "%s.in2%s"%(fbfm, thing))        
                cmds.connectAttr("%s.position%s"%(posi,stuff), "%s.in3%s"%(fbfm, thing))
                cmds.connectAttr("%s.outputTranslate%s"%(dcm,stuff), "%s.translate%s"%(space,stuff))         
                cmds.connectAttr("%s.outputRotate%s"%(dcm,stuff), "%s.rotate%s"%(space,stuff))   
            cmds.connectAttr("%s.output"%fbfm, "%s.matrixIn[0]"%mm) 
            cmds.connectAttr("%s.parentInverseMatrix"%space, "%s.matrixIn[1]"%mm)                
            cmds.connectAttr("%s.matrixSum"%mm, "%s.inputMatrix"%dcm) 
            cmds.parent(surf, self.surfPar)   
            
    def normal(self):
        self.defi()
        if self.obj:
            testType=1
            for check in self.obj:
                if cmds.objectType(check)!="joint":
                    testType=[]
            if testType:
                allGood= self.preTest(self.obj)
                if allGood:
                    self.jointSetup(self.obj)
                    #Create Surface
                    self.surfaceC(self.flipObj, "ctrl_offset")
                    cmds.select(cl=1)
                    for item in self.flipObj:
                        cmds.select(item.replace(self.jnt, "ctrl"), add=1)
            else:
                cmds.warning("One of the selected object is not a JOINT")            
        else:
            cmds.warning("Please select at least one target")            

    def withParent(self):
        self.defi()
        if len(self.obj)==1:     
            self.child= cmds.listRelatives(self.obj, pa=1, c=1)
            if self.child:
                realObj= self.obj + self.child
                testType=1
                for check in realObj:
                    if cmds.objectType(check)!="joint":
                        testType=[]
                if testType:          
                    allGood= self.preTest(realObj)
                    if allGood: 
                        self.jointSetup(realObj)
                        if self.obj[0] not in self.noFlip.split(", "):
                            newObj= self.obj[0].replace(self.jnt, "ctrl") + ", " + (self.obj[0].replace(self.sear, self.repl)).replace(self.jnt, "ctrl") 
                        else:
                            newObj= self.obj[0].replace(self.jnt, "ctrl")
                        for item in newObj.split(", "):
                            oldShp= cmds.listRelatives(item, c=1, pa=1, typ="nurbsCurve")
                            cmds.delete(oldShp)
                            sh= cmds.curve(d=1, n="temp", p=[(-0.0920624, 2.010909, 0), (-0.0920624, 1.98615, -0.314575), (-0.0920624, 1.912485, -0.621405), (-0.0920624, 1.791729, -0.912937), (-0.0920624, 1.626861, -1.181981), (-0.0920624, 1.421927, -1.421927), (-0.0920624, 1.181981, -1.626861), (-0.0920624, 0.912937, -1.791729), (-0.0920624, 0.621405, -1.912485), (-0.0920624, 0.314575, -1.98615), (-0.0920624, 0, -2.010909), (-0.0920624, -0.314575, -1.98615), (-0.0920624, -0.621405, -1.912485), (-0.0920624, -0.912937, -1.791729), (-0.0920624, -1.181981, -1.626861), (-0.0920624, -1.421927, -1.421927), (-0.0920624, -1.626861, -1.181981), (-0.0920624, -1.791729, -0.912937), (-0.0920624, -1.912485, -0.621405), (-0.0920624, -1.98615, -0.314575), (-0.0920624, -2.010909, 0), (-0.0920624, -1.98615, 0.314575), (-0.0920624, -1.912485, 0.621405), (-0.0920624, -1.791729, 0.912937), (-0.0920624, -1.626861, 1.181981), (-0.0920624, -1.421927, 1.421927), (-0.0920624, -1.181981, 1.626861), (-0.0920624, -0.912937, 1.791729), (-0.0920624, -0.621405, 1.912485), (-0.0920624, -0.314575, 1.98615), (-0.0920624, 0, 2.010909), (-0.0920624, 0.314575, 1.98615), (-0.0920624, 0.621405, 1.912485), (-0.0920624, 0.912937, 1.791729), (-0.0920624, 1.181981, 1.626861), (-0.0920624, 1.421927, 1.421927), (-0.0920624, 1.626861, 1.181981), (-0.0920624, 1.791729, 0.912937), (-0.0920624, 1.912485, 0.621405), (-0.0920624, 1.98615, 0.314575), (-0.0920624, 2.010909, 0), (0.0920624, 2.010909, 0), (0.0920624, 1.98615, -0.314575), (0.0920624, 1.912485, -0.621405), (0.0920624, 1.791729, -0.912937), (0.0920624, 1.626861, -1.181981), (0.0920624, 1.421927, -1.421927), (-0.0920624, 1.421927, -1.421927), (0.0920624, 1.421927, -1.421927), (0.0920624, 1.181981, -1.626861), (0.0920624, 0.912937, -1.791729), (0.0920624, 0.621405, -1.912485), (0.0920624, 0.314575, -1.98615), (0.0920624, 0, -2.010909), (-0.0920624, 0, -2.010909), (0.0920624, 0, -2.010909), (0.0920624, -0.314575, -1.98615), (0.0920624, -0.621405, -1.912485), (0.0920624, -0.912937, -1.791729), (0.0920624, -1.181981, -1.626861), (0.0920624, -1.421927, -1.421927), (-0.0920624, -1.421927, -1.421927), (0.0920624, -1.421927, -1.421927), (0.0920624, -1.626861, -1.181981), (0.0920624, -1.791729, -0.912937), (0.0920624, -1.912485, -0.621405), (0.0920624, -1.98615, -0.314575), (0.0920624, -2.010909, 0), (-0.0920624, -2.010909, 0), (0.0920624, -2.010909, 0), (0.0920624, -1.98615, 0.314575), (0.0920624, -1.912485, 0.621405), (0.0920624, -1.791729, 0.912937), (0.0920624, -1.626861, 1.181981), (0.0920624, -1.421927, 1.421927), (-0.0920624, -1.421927, 1.421927), (0.0920624, -1.421927, 1.421927), (0.0920624, -1.181981, 1.626861), (0.0920624, -0.912937, 1.791729), (0.0920624, -0.621405, 1.912485), (0.0920624, -0.314575, 1.98615), (0.0920624, 0, 2.010909), (-0.0920624, 0, 2.010909), (0.0920624, 0, 2.010909), (0.0920624, 0.314575, 1.98615), (0.0920624, 0.621405, 1.912485), (0.0920624, 0.912937, 1.791729), (0.0920624, 1.181981, 1.626861), (0.0920624, 1.421927, 1.421927), (-0.0920624, 1.421927, 1.421927), (0.0920624, 1.421927, 1.421927), (0.0920624, 1.626861, 1.181981), (0.0920624, 1.791729, 0.912937), (0.0920624, 1.912485, 0.621405), (0.0920624, 1.98615, 0.314575), (0.0920624, 2.010909, 0)])
                            newShp= cmds.listRelatives(sh, c=1, pa=1, typ="nurbsCurve")    
                            cmds.setAttr("%s.overrideEnabled"%newShp[0], 1)        
                            cmds.setAttr("%s.overrideColor"%newShp[0], 17)
                            cmds.parent(newShp, item, r=1, s=1)
                            cmds.rename(newShp, "%sShape"%item)
                            cmds.delete(sh)
                        #Create Surface    
                        self.surfaceC(self.flipObjPar, "ctrl_grp2")
                        #Extra BPM Group
                        bpmPar= cmds.duplicate(self.jntPar, n="%s"%self.jntPar.replace(self.jnt, "bpmJnt"))
                        cmds.setAttr("%s.v"%bpmPar[0], 0)
                        ch= cmds.listRelatives(bpmPar[0], ad=1, f=1, typ="transform")  
                        allE= sorted(ch)   
                        for x in range(len(allE)-1, -1, -1):
                            oldName = allE[x].split("|")[-1]  
                            cmds.rename(allE[x], oldName.replace(self.jnt, "bpmJnt")) 
                        extraPar= cmds.duplicate(self.jntPar, n="%s"%self.jntPar.replace(self.jnt, "extra"))
                        cmds.setAttr("%s.v"%extraPar[0], 0)
                        ch= cmds.listRelatives(extraPar[0], ad=1, f=1, typ="transform")  
                        allE= sorted(ch)   
                        for x in range(len(allE)-1, -1, -1):
                            oldName = allE[x].split("|")[-1]  
                            cmds.rename(allE[x], oldName.replace(self.jnt, "extra"))
                        tempDel1= "%s"%self.obj[0] + ", " + "%s"%self.obj[0].replace(self.sear, self.repl)
                        try:
                            cmds.delete((tempDel1.replace(self.jnt, "bpmJnt_offset")).split(", "))
                        except:
                            cmds.delete(self.obj[0].replace(self.jnt, "bpmJnt_offset"))
                        try:
                            cmds.delete((tempDel1.replace(self.jnt, "extra_offset")).split(", "))   
                        except:
                            cmds.delete(self.obj[0].replace(self.jnt, "extra_offset")) 
                        for tempDel in (", ".join(self.flipChild).replace(self.jnt, "extra")).split(", "):
                            cmds.delete(tempDel)
                        for recon in self.flipChild: 
                            oriCon= cmds.listConnections("%s.parentInverseMatrix"%recon.replace(self.jnt, "ctrl_grp2"), d=1, c=1, p=1)
                            cmds.connectAttr("%s.worldInverseMatrix"%recon.replace(self.jnt, "extra_offset"), oriCon[1], f=1)        
                        #Parent Constraint (bpm connection included inside)      
                        allAttr=["X", "Y", "Z"]
                        for thing in self.flipChild:
                            ctrlGrp= thing.replace(self.jnt, "ctrl_grp2")
                            ctrlOff= thing.replace(self.jnt, "ctrl_offset")
                            bpmGrp= thing.replace(self.jnt, "bpmJnt_grp2")
                            bpmGrpOff= thing.replace(self.jnt, "bpmJnt_offset")
                            extraGrp= thing.replace(self.jnt, "extra_grp2")
                            extraOff= thing.replace(self.jnt, "extra_offset")
                            if self.sear in thing:
                                cmds.parentConstraint(self.obj[0].replace(self.jnt, "ctrl"), ctrlOff ,mo=1, w=1)
                                cmds.parentConstraint(self.obj[0].replace(self.jnt, "ctrl_grp2"), extraOff ,mo=1, w=1)
                            else:
                                if self.obj[0] not in self.noFlip.split(", "):
                                    cmds.parentConstraint((self.obj[0].replace(self.jnt, "ctrl")).replace(self.sear, self.repl), ctrlOff ,mo=1, w=1) 
                                    cmds.parentConstraint((self.obj[0].replace(self.jnt, "ctrl_grp2")).replace(self.sear, self.repl), extraOff ,mo=1, w=1) 
                                else:
                                    cmds.parentConstraint((self.obj[0].replace(self.jnt, "ctrl")), ctrlOff ,mo=1, w=1) 
                                    cmds.parentConstraint((self.obj[0].replace(self.jnt, "ctrl_grp2")), extraOff ,mo=1, w=1)                     
                            mm01= cmds.createNode("multMatrix", n="%s_mm"%ctrlOff)
                            dm01= cmds.createNode("decomposeMatrix", n="%s_dm"%ctrlOff)
                            cmds.connectAttr("%s.worldMatrix[0]"%ctrlOff, "%s.matrixIn[0]"%mm01) 
                            cmds.connectAttr("%s.worldInverseMatrix[0]"%ctrlOff, "%s.matrixIn[1]"%mm01) 
                            cmds.connectAttr("%s.matrixSum"%mm01, "%s.inputMatrix"%dm01) 
                            for attr in allAttr:
                                cmds.connectAttr("%s.translate%s"%(ctrlGrp, attr), "%s.translate%s"%(bpmGrp, attr))
                                cmds.connectAttr("%s.rotate%s"%(ctrlGrp, attr), "%s.rotate%s"%(bpmGrp, attr))            
                                cmds.connectAttr("%s.translate%s"%(extraOff, attr), "%s.translate%s"%(bpmGrpOff, attr))
                                cmds.connectAttr("%s.rotate%s"%(extraOff, attr), "%s.rotate%s"%(bpmGrpOff, attr))
                                cmds.connectAttr("%s.outputScale%s"%(dm01, attr), "%s.scale%s"%(bpmGrpOff, attr))
                        #final Connect
                        cmds.select(cl=1)
                        for item in self.flipObjPar:
                            cmds.select(item.replace(self.jnt, "ctrl"), add=1)
                else:
                    cmds.warning("Selected object or one of the child is not a JOINT")            
            else:
                cmds.warning("Selected object doesn't have any joint child")
        else:
            cmds.warning("Please select ONE, the PARENT of the joints")               

    def example(self, meth):
        if meth==1:
            allJnt=[]
            for x, item in enumerate(zip([(3,-3),(4,0),(3,3)],[(45), (0),(-45)])):
                jnt= cmds.createNode("joint", n="LvnNorm%s_L_jnt"%x)
                cmds.xform(jnt, t=(item[0][0],0,item[0][1]), ws=1)
                cmds.setAttr("%s.jointOrientY"%jnt, item[1])
                allJnt.append(jnt)
            cmds.select(allJnt)
        else:
            self.jntPar= cmds.createNode("joint", n="LvnPar0_L_jnt") 
            cmds.xform(self.jntPar, t=(8,0,0), ws=1)  
            for x, item in enumerate(zip([(8,2,0),(8,0,2),(8,-2,0),(8,0,-2)],[(0),(90),(180),(-90)])):
                jnt= cmds.createNode("joint", n="LvnPar%s_L_jnt"%(x+1))
                cmds.xform(jnt, t=(item[0][0],item[0][1],item[0][2]), ws=1)
                cmds.setAttr("%s.jointOrientX"%jnt, item[1])
                cmds.parent(jnt,self.jntPar)
            cmds.select(self.jntPar)

    def helps(self):
        name="Help On CtrlSetup"
        helpTxt="""
        - Rig setup for tweaker layer



        1) Normal
        ===========
            - Create each individual ctrl

        2) Parent
        ===========
            - A parent ctrl that controls each individual ctrl under it

        (* <No Flip>, for middle ctrl that doesn't need to get mirror or asymmetric)
        (* This setup is special because have surface constraint 
           and also have extra joint can be use for bindPreMatrix)


        Eg. 
            Method 1
            ==========
                - Usual method to create ctrl for acc (without the use of follicle)

                0) Create for "belt ctrl"
                1) Create joint for setup. Run < Normal >
                2) Paint joint to "belt mesh"
                3) Select "body mesh" and copy weight to "belt_srf" (under noScaleGrp)
                    (Now belt will pin and follow body mesh like follicle)
                4) Constraint global ctrl (or see fit) to "scaleGrp"


            Method 2
            ==========
                - create tweak ctrl with bindPreMatrix

                0) Create for "sleeve ctrl"
                1) Create joint for setup. Run < Normal >

                2) BindPreMatrix setup
                    1. Sleeve should already have a base weight
                    2. Duplicate call it "sleeve_tweak"
                    3. Blendshape "sleeve_tweak mesh" > "sleeve mesh"
                    4. Show "sleeve_tweak mesh"
                    5. Hide "sleeve_tweak mesh"

                3) Paint joint to "sleeve_tweak mesh"
                4) Run BindPreMatrix on "sleeve_tweak mesh"
                5) Select "sleeve mesh" and copy weight to "sleeve_srf" (under noScaleGrp)
                    (When body move, sleeve ctrl will follow but will not activate cause of bpm)
                6) Constraint global ctrl (or see fit) to "scaleGrp"    

                (* May us < Parent > setup. Then for that have to use the bpmJnt to do bindPreMatrix)        
        """
        self.helpBoxClass.helpBox1(name, helpTxt) 

    def reloadSub(self):
        CtrlSetup()
    

if __name__=='__main__':
    CtrlSetup()