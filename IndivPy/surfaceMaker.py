import maya.cmds as cmds
import maya.mel as mel
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox


class SurfaceMaker(object):
    def __init__(self, *args):
        self.uiStuffClass= uiStuff.UiStuff()
        self.dialogClass= dialog.Dialog()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):
        try: 
            cmds.deleteUI("surfM") 
        except:
            pass    
        cmds.window("surfM", mb=1)              
        cmds.window("surfM", t="Surface Maker", s=1, e=1, wh=(350,440))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on SurfaceMaker", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload SurfaceMaker", c=lambda x:self.reloadSub())    
        self.uiStuffClass.sepBoxMain()
        column11= self.uiStuffClass.sepBoxSub("Create")
        form11= cmds.formLayout(nd=100, p=column11)
        self.srfWidth= cmds.floatFieldGrp(l="Width :", cw2=(55,40), adj=2, v1=0.1, pre=2 )
        self.aimAxis= cmds.optionMenuGrp(l="Aim Axis :", cw2=(55,10), adj=2)
        cmds.menuItem(l="X")
        cmds.menuItem(l="Y")
        cmds.menuItem(l="Z")
        cmds.menuItem(l="- X")
        cmds.menuItem(l="- Y")
        cmds.menuItem(l="- Z")    
        self.upAxis= cmds.optionMenuGrp(l="Up Axis :", cw2=(55,10), adj=2)
        cmds.menuItem(l="X")
        cmds.menuItem(l="Y")
        cmds.menuItem(l="Z")
        cmds.menuItem(l="- X")
        cmds.menuItem(l="- Y")
        cmds.menuItem(l="- Z")
        cmds.optionMenuGrp(self.upAxis, e=1, sl=2)
        sep1= cmds.separator(h=110, hr=0, st="in")
        self.cbEach= cmds.checkBoxGrp(l="", l1="Each (Create Multi)", cw2=(10,10), cc=lambda x:self.cbxOnOffEach())        
        sep2= cmds.separator(h=5, st="in")
        self.cbHull1= cmds.checkBoxGrp(l="", l1="More Hull (Linear)", cw2=(10,10), cc=lambda x:self.cbxOnOff(self.cbHull1,self.cbHull2))
        self.cbHull2= cmds.checkBoxGrp(l="", l1="More Hull (Arc)", cw2=(10,10), cc=lambda x:self.cbxOnOff(self.cbHull2,self.cbHull1))
        self.cbZeroJO= cmds.checkBoxGrp(l="", l1="Zero Orient Last Joint", v1=1, cw2=(10,10), cc=lambda x:self.cbxOnOff(self.cbZeroJO,self.cbCloseEnd))
        self.cbCloseEnd= cmds.checkBoxGrp(l="", l1="Close End (Circular)", cw2=(10,10), cc=lambda x:self.cbxOnOff(self.cbCloseEnd,self.cbZeroJO))
        b11= cmds.button(l="Create Surface",c=lambda x:self.cSrf()) 
        cmds.formLayout(form11, e=1,
                                af=[(self.srfWidth, "top", 15),
                                    (self.aimAxis, "top", 40),
                                    (self.upAxis, "top", 65),
                                    (sep1, "top", 0),
                                    (self.cbEach, "top", 0),
                                    (sep2, "top", 23),
                                    (self.cbHull1, "top", 30),
                                    (self.cbHull2, "top", 50),
                                    (self.cbZeroJO, "top", 70),
                                    (self.cbCloseEnd, "top", 90),
                                    (b11, "top", 120)],
                                ap=[(self.srfWidth, "left", 0, 0),
                                    (self.srfWidth, "right", 0, 40),
                                    (self.aimAxis, "left", 0, 0),
                                    (self.aimAxis, "right", 0, 40),
                                    (self.upAxis, "left", 0, 0),
                                    (self.upAxis, "right", 0, 40),
                                    (sep1, "left", 0, 42),
                                    (sep1, "right", 0, 50),
                                    (self.cbEach, "left", 0, 50),
                                    (self.cbEach, "right", 0, 100),
                                    (sep2, "left", 0, 51),
                                    (sep2, "right", 0, 95),
                                    (self.cbHull1, "left", 0, 50),
                                    (self.cbHull1, "right", 0, 100),
                                    (self.cbHull2, "left", 0, 50),
                                    (self.cbHull2, "right", 0, 100),
                                    (self.cbZeroJO, "left", 0, 50),
                                    (self.cbZeroJO, "right", 0, 100),
                                    (self.cbCloseEnd, "left", 0, 50),
                                    (self.cbCloseEnd, "right", 0, 100),
                                    (b11, "left", 0, 0),
                                    (b11, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column12= self.uiStuffClass.sepBoxSub()
        form12= cmds.formLayout(nd=100, p=column12)
        self.txtFU= cmds.textFieldButtonGrp(l="Upper :", cw3=(50,10,10), adj=2, pht="left to right", bl="  Grab  ", bc= lambda :self.grab1(self.txtFU))  
        self.txtFL= cmds.textFieldButtonGrp(l="Lower :", cw3=(50,10,10), adj=2, pht="left to right", bl="  Grab  ", bc= lambda :self.grab1(self.txtFL))  
        txt11= cmds.text(l="*Input even number VERTEX", fn="smallObliqueLabelFont", en=0)
        b12= cmds.button(l="Create Surface Plane", c=lambda x:self.cSrfPlane()) 
        cmds.formLayout(form12, e=1,
                                af=[(self.txtFU, "top", 0),
                                    (self.txtFL, "top", 26),
                                    (txt11, "top", 52),
                                    (b12, "top", 82)],
                                ap=[(txt11, "left", 0, 0),
                                    (txt11, "right", 0, 100),
                                    (self.txtFU, "left", 0, 0),
                                    (self.txtFU, "right", 0, 100),
                                    (self.txtFL, "left", 0, 0),
                                    (self.txtFL, "right", 0, 100),
                                    (b12, "left", 0, 0),
                                    (b12, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column21= self.uiStuffClass.sepBoxSub("Edit")
        form21= cmds.formLayout(nd=100, p=column21)
        self.nIso= cmds.intSliderGrp(l="Number of Isoparms :", f=1, cw3=(115,50,50), min=1, max=10, fmx=100, v=1)
        self.omDirec= cmds.optionMenuGrp(l="Direction :", cw2=(60,10))
        cmds.menuItem(l="V")
        cmds.menuItem(l="U")
        b211= cmds.button(l="Add Isoparms",c=lambda x:self.cIso(1))
        b212= cmds.button(l="Remove Isoparms",c=lambda x:self.cIso(2))
        cmds.formLayout(form21, e=1,
                                af=[(self.nIso, "top", 0),
                                    (self.omDirec, "top", 25),
                                    (b211, "top", 55),
                                    (b212, "top", 55)],
                                ap=[(self.nIso, "left", 0, 0),
                                    (self.nIso, "right", 0, 100),
                                    (self.omDirec, "left", 0, 0),
                                    (self.omDirec, "right", 0, 100),
                                    (b211, "left", 0, 0),
                                    (b211, "right", 0, 50),
                                    (b212, "left", 0, 51),
                                    (b212, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column22= self.uiStuffClass.sepBoxSub()
        form22= cmds.formLayout(nd=100, p=column22)
        txt221= cmds.text(l="Select 3 VERTEX :       xx / TARGET/ xx", fn="smallObliqueLabelFont", en=0)
        txt222= cmds.text(l="Select 2 VERTEX", fn="smallObliqueLabelFont", en=0)
        b221= cmds.button(l="Snap Inbetween Fix", c=lambda x:self.sFix(3, 1))
        b222= cmds.button(l="Swap Position Fix", c=lambda x:self.sFix(2, 2))
        cmds.formLayout(form22, e=1,
                                af=[(txt221, "top", 0),
                                    (b221, "top", 16),
                                    (txt222, "top", 50),
                                    (b222, "top", 66)],
                                ap=[(txt221, "left", 0, 0),
                                    (txt221, "right", 0, 100),
                                    (txt222, "left", 0, 0),
                                    (txt222, "right", 0, 100),
                                    (b221, "left", 0, 0),
                                    (b221, "right", 0, 100),
                                    (b222, "left", 0, 0),
                                    (b222, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column23= self.uiStuffClass.sepBoxSub()
        form23= cmds.formLayout(nd=100, p=column23)
        b231= cmds.button(l="Preview X-axis Direction", c=lambda x:self.checkSrfDirec(1))  
        b232= cmds.button(l="Delete Preview", c=lambda x:self.checkSrfDirec(2))  
        b233= cmds.button(l="Rotate Surface Direction", c=lambda x:self.checkSrfDirec(3))  
        cmds.formLayout(form23, e=1,
                              af=[(b231, "top", 0),
                                  (b232, "top", 26),
                                  (b233, "top", 26)],
                              ap=[(b231, "left", 0, 0),
                                  (b231, "right", 0, 100),
                                  (b232, "left", 0, 0),
                                  (b232, "right", 0, 50),
                                  (b233, "left", 0, 51),
                                  (b233, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column31= self.uiStuffClass.sepBoxSub("Constraint")
        form31= cmds.formLayout(nd=100, p=column31)
        self.cbNG= cmds.checkBoxGrp(l="", l1="Constraint New Group", cw2=(5,100), v1=1, ncb=1)   
        self.cbWs= cmds.checkBoxGrp(l="", l1="Surface WorldSpace (Affects Targets When Moving)", cw2=(5,100), ncb=1)  
        sep31= cmds.separator(h=10, st="in")
        self.txtFSrf= cmds.textFieldButtonGrp(l="Surface :", cw3=(50,150,10), adj=2, bl="   Grab   ", bc=lambda :self.grab31())
        self.txtFTar= cmds.textFieldButtonGrp(l="Targets :", cw3=(50,150,10), adj=2, bl="   Grab   ", bc=lambda :self.grab32())
        b31= cmds.button(l="Constraint To Surface",c=lambda x:self.srfConst()) 
        cmds.formLayout(form31, e=1,
                              af=[(self.cbNG, "top", 0),
                                  (self.cbWs, "top", 20),
                                  (sep31, "top", 45),
                                  (self.txtFSrf, "top", 60),
                                  (self.txtFTar, "top", 86),
                                  (b31, "top", 121)],
                              ap=[(sep31, "left", 0, 0),
                                  (sep31, "right", 0, 100),
                                  (self.txtFSrf, "left", 0, 0),
                                  (self.txtFSrf, "right", 0, 100),
                                  (self.txtFTar, "left", 0, 0),
                                  (self.txtFTar, "right", 0, 100),
                                  (b31, "left", 0, 0),
                                  (b31, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l="")) 
        cmds.showWindow("surfM")

    def cbxOnOff(self, cbOn, cbOff):
        if cmds.checkBoxGrp(cbOn, q=1, v1=1):
            cmds.checkBoxGrp(cbOff, e=1, v1=0)  

    def cbxOnOffEach(self):
        if cmds.checkBoxGrp(self.cbEach, q=1, v1=1):
            cmds.checkBoxGrp(self.cbHull1, e=1, en=0)  
            cmds.checkBoxGrp(self.cbHull2, e=1, en=0) 
            cmds.checkBoxGrp(self.cbZeroJO, e=1, en=0)   
            cmds.checkBoxGrp(self.cbCloseEnd, e=1, en=0)   
        else:
            cmds.checkBoxGrp(self.cbHull1, e=1, en=1)  
            cmds.checkBoxGrp(self.cbHull2, e=1, en=1) 
            cmds.checkBoxGrp(self.cbZeroJO, e=1, en=1)   
            cmds.checkBoxGrp(self.cbCloseEnd, e=1, en=1)               

    def defi1(self):
        self.obj=cmds.ls(sl=1)
        self.wid= cmds.floatFieldGrp(self.srfWidth, q=1, v1=1)
        self.aimAx= cmds.optionMenuGrp(self.aimAxis, q=1, sl=1)    
        self.preUpAx= cmds.optionMenuGrp(self.upAxis, q=1, sl=1)
        if self.preUpAx==1:
            self.upAx=[1,0,0]
        elif self.preUpAx==2:
            self.upAx=[0,1,0]        
        elif self.preUpAx==3:
            self.upAx=[0,0,1]         
        elif self.preUpAx==4:
            self.upAx=[-1,0,0] 
        elif self.preUpAx==5:
            self.upAx=[0,-1,0]
        elif self.preUpAx==6:
            self.upAx=[0,0,-1]  
        self.txtU= cmds.textFieldButtonGrp(self.txtFU, q=1, tx=1)  
        self.txtL= cmds.textFieldButtonGrp(self.txtFL, q=1, tx=1)

    def grab1(self, txtF):
        obj= cmds.ls(os=1, fl=1)
        if len(obj)>1:             
            test1= 1    
            for item in obj:
                if ".vtx" not in item:
                    test1= []
            if test1:
                cmds.textFieldButtonGrp(txtF, e=1, tx="%s"%", ".join(obj))  
            else:
                cmds.warning("Please select VERTEX only")
        else:
            cmds.warning("Please select at least 2 VERTEX")      

    def negRot(self, tar):
        #Do this way cause xform cant detect object with negative scale
        dcm= cmds.createNode("decomposeMatrix")
        cmds.connectAttr("%s.worldMatrix"%tar, "%s.inputMatrix"%dcm)
        rot= cmds.getAttr("%s.outputRotate"%dcm)
        cmds.delete(dcm)
        return rot

    def cSrf(self):
        self.defi1()
        test1= 1
        for item in self.obj:
            if len(item.split("."))==2:
                    test1= []       
        if test1:
            self.uiStuffClass.loadingBar(1, 2)
            self.uiStuffClass.loadingBar(2)
            if cmds.checkBoxGrp(self.cbEach, v1=1, q=1)==1:
                srf= []
                for item in self.obj:
                    srfSub= cmds.nurbsPlane(n="srf", ax=self.upAx, d=1, ch=0, w=self.wid, lr=1)
                    tran= cmds.xform(item, q=1, rp=1, ws=1)
                    rot= self.negRot(item)
                    #Probably need find rotate pivot?  
                    cmds.xform(srfSub, t=(tran[0], tran[1], tran[2]), ro=(rot[0][0],rot[0][1],rot[0][2]), ws=1) 
                    srf.append(srfSub[0])
            else:     
                srf= cmds.nurbsPlane(n="srf", ax=self.upAx, d=1, ch=0, w=self.wid, lr=1)
                if len(self.obj)==1:
                    tran= cmds.xform(self.obj, q=1, rp=1, ws=1)
                    rot= self.negRot(self.obj[0])
                    cmds.xform(srf, t=(tran[0],tran[1],tran[2]), ro=(rot[0][0],rot[0][1],rot[0][2]), ws=1) 
                elif len(self.obj)>=2:
                    if cmds.checkBoxGrp(self.cbHull1, q=1, v1=1) or cmds.checkBoxGrp(self.cbHull2, q=1, v1=1):
                        self.moreHull(srf)
                    else:   
                        self.lessHull(srf)  
                    if cmds.checkBoxGrp(self.cbCloseEnd, q=1, v1=1):
                        cmds.closeSurface(srf[0], ch=0, ps=0, rpo=1, d=0)    
            cmds.select(srf, self.obj)
            cmds.toggle(srf, cv=1)
            cmds.xform(srf, cp=1)   
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)     
        else:
            cmds.warning("Please select transform object, not subselection like vertex")

    def lessHull(self, srf):
        if len(self.obj)==3:
            cmds.rebuildSurface(srf, du=2, dv=1, dir=0, su=1, sv=1, ch=0)
        elif len(self.obj)>=4:        
            cmds.rebuildSurface(srf, du=3, dv=1, dir=0, su=(len(self.obj)-3), sv=1, ch=0)
        for each, stuff in enumerate(self.obj): 
            self.snapSurf(each, stuff, srf)
                         
    def moreHull(self, srf):  
        if cmds.checkBoxGrp(self.cbCloseEnd, q=1, v1=1):
            if len(self.obj)>=2:        
                cmds.rebuildSurface(srf, du=3, dv=1, dir=0, su=(len(self.obj)*2-3), sv=1, ch=0) 
            x= len(self.obj)*2
        else:    
            if len(self.obj)==2:
                cmds.rebuildSurface(srf, du=2, dv=1, dir=0, su=1, sv=1, ch=0)           
            elif len(self.obj)>=3:        
                cmds.rebuildSurface(srf, du=3, dv=1, dir=0, su=(len(self.obj)*2-4), sv=1, ch=0) 
            x= len(self.obj)*2-1
        mainCv, subCv= [],[]
        for y in range(0, x):
            if y%2:    
                subCv.append(y)
            else:
                mainCv.append(y)     
        for each, stuff in zip(mainCv, self.obj):
            self.snapSurf(each, stuff, srf)
        #Snap inbetween linearly
        for each in subCv:
            for thing in (0,1):           
                tran1= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-1,thing), q=1, t=1, ws=1)
                if cmds.checkBoxGrp(self.cbCloseEnd, q=1, v1=1):
                    if each==subCv[-1]:    
                        tran2= cmds.xform("%s.cv[%s][%s]"%(srf[0],subCv[0]-1,thing), q=1, t=1, ws=1)    
                    else:
                        tran2= cmds.xform("%s.cv[%s][%s]"%(srf[0],each+1,thing), q=1, t=1, ws=1)
                else:
                    tran2= cmds.xform("%s.cv[%s][%s]"%(srf[0],each+1,thing), q=1, t=1, ws=1) 
                cmds.xform("%s.cv[%s][%s]"%(srf[0],each,thing), t=((tran1[0]+tran2[0])/2,(tran1[1]+tran2[1])/2,(tran1[2]+tran2[2])/2), ws=1)  
                #Readjust inbetween to have arc angle
                if cmds.checkBoxGrp(self.cbHull2, q=1, v1=1):
                    tpcaCrv= cmds.curve(d=1, p=[(0,0,0),(1,1,1)])
                    mtpca= cmds.createNode("makeThreePointCircularArc") 
                    npoc= cmds.createNode("nearestPointOnCurve")  
                    if cmds.checkBoxGrp(self.cbCloseEnd, q=1, v1=1):
                        if each==subCv[-1]:     
                            p1= cmds.xform("%s.cv[%s][%s]"%(srf[0],subCv[0]-1,thing), q=1, t=1, ws=1)  
                            p2= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-1,thing), q=1, t=1, ws=1)  
                            p3= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-3,thing), q=1, t=1, ws=1)
                        elif each==subCv[-2]:     
                            p1= cmds.xform("%s.cv[%s][%s]"%(srf[0],each+1,thing), q=1, t=1, ws=1)  
                            p2= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-1,thing), q=1, t=1, ws=1)  
                            p3= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-3,thing), q=1, t=1, ws=1)                           
                        else:
                            p1= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-1,thing), q=1, t=1, ws=1)  
                            p2= cmds.xform("%s.cv[%s][%s]"%(srf[0],each+1,thing), q=1, t=1, ws=1)  
                            p3= cmds.xform("%s.cv[%s][%s]"%(srf[0],each+3,thing), q=1, t=1, ws=1)                       
                    else:
                        if each==subCv[-1]:     
                            p1= cmds.xform("%s.cv[%s][%s]"%(srf[0],each+1,thing), q=1, t=1, ws=1)  
                            p2= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-1,thing), q=1, t=1, ws=1)  
                            p3= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-3,thing), q=1, t=1, ws=1) 
                        else:
                            p1= cmds.xform("%s.cv[%s][%s]"%(srf[0],each-1,thing), q=1, t=1, ws=1)  
                            p2= cmds.xform("%s.cv[%s][%s]"%(srf[0],each+1,thing), q=1, t=1, ws=1)  
                            p3= cmds.xform("%s.cv[%s][%s]"%(srf[0],each+3,thing), q=1, t=1, ws=1)                         
                    cmds.setAttr("%s.point1"%mtpca, p1[0],p1[1],p1[2])
                    cmds.setAttr("%s.point2"%mtpca, p2[0],p2[1],p2[2])
                    cmds.setAttr("%s.point3"%mtpca, p3[0],p3[1],p3[2])
                    cmds.connectAttr("%s.outputCurve"%mtpca,"%s.create"%tpcaCrv)
                    cmds.connectAttr("%s.worldSpace"%tpcaCrv,"%s.inputCurve"%npoc)
                    cmds.setAttr("%s.inPosition"%npoc, (tran1[0]+tran2[0])/2,(tran1[1]+tran2[1])/2,(tran1[2]+tran2[2])/2)
                    pos= cmds.getAttr("%s.position"%npoc)
                    #If thr point is collinear.... is there any other method to fix it?
                    if pos!= [(0,0,0)]:
                        cmds.xform("%s.cv[%s][%s]"%(srf[0],each,thing), t=(pos[0][0],pos[0][1],pos[0][2]), ws=1)
                    cmds.delete(tpcaCrv, mtpca)  

    def snapSurf(self, each, stuff, srf): 
        srfTemp= cmds.nurbsPlane(n="srf", ax=self.upAx, d=1, ch=0, w=self.wid, lr=1)
        srfTempGrp= cmds.group(srfTemp, w=1)
        tran= cmds.xform(stuff, q=1, rp=1, ws=1)
        rot= self.negRot(stuff)
        if stuff==self.obj[-1]:
            if cmds.checkBoxGrp(self.cbZeroJO, q=1, v1=1)==1:
                rot= self.negRot(self.obj[-2])
        cmds.xform(srfTempGrp, t=(tran[0],tran[1],tran[2]), ro=(rot[0][0],rot[0][1],rot[0][2]))                             
        #because no other way, can only determine all possible orientation
        if self.aimAx==1:
            cmds.setAttr("%s.tx"%srfTemp[0], (self.wid/2)) 
        if self.aimAx==2:
            cmds.setAttr("%s.ty"%srfTemp[0], (self.wid/2))   
            if self.preUpAx==1:
                cmds.setAttr("%s.rx"%srfTemp[0], 90)
            elif self.preUpAx==4:
                cmds.setAttr("%s.rx"%srfTemp[0], -90)  
            elif self.preUpAx==3 or self.preUpAx==6:
                cmds.setAttr("%s.rz"%srfTemp[0], 90)
        if self.aimAx==3:
            cmds.setAttr("%s.tz"%srfTemp[0], (self.wid/2))    
            if self.preUpAx==1:
                cmds.setAttr("%s.rx"%srfTemp[0], 180)
            elif self.preUpAx==2 or self.preUpAx==5:
                cmds.setAttr("%s.ry"%srfTemp[0], -90)
        if self.aimAx==4:
            cmds.setAttr("%s.tx"%srfTemp[0], (self.wid/-2))  
            if self.preUpAx==3 or self.preUpAx==6:
                cmds.setAttr("%s.rz"%srfTemp[0], 180)
            elif self.preUpAx==2 or self.preUpAx==5:
                cmds.setAttr("%s.ry"%srfTemp[0], 180)
        if self.aimAx==5:
            cmds.setAttr("%s.ty"%srfTemp[0], (self.wid/-2))   
            if self.preUpAx==1:
                cmds.setAttr("%s.rx"%srfTemp[0], -90)
            elif self.preUpAx==4:
                cmds.setAttr("%s.rx"%srfTemp[0], 90)
            elif self.preUpAx==3 or self.preUpAx==6:
                cmds.setAttr("%s.rz"%srfTemp[0], -90)   
        if self.aimAx==6:
            cmds.setAttr("%s.tz"%srfTemp[0], (self.wid/-2))  
            if self.preUpAx==4:
                cmds.setAttr("%s.rx"%srfTemp[0], 180)
            elif self.preUpAx==2 or self.preUpAx==5:
                cmds.setAttr("%s.ry"%srfTemp[0], 90)
        for thing in (0,1):            
            finalTran= cmds.xform("%s.cv[0][%s]"%(srfTemp[0], thing), q=1, t=1, ws=1)      
            cmds.xform("%s.cv[%s][%s]"%(srf[0],each,thing), t=(finalTran[0],finalTran[1],finalTran[2]), ws=1)
        cmds.delete(srfTempGrp)

    def cSrfPlane(self):
        self.defi1()
        if self.txtU:
            if self.txtL:
                if len(self.txtU.split(", "))>1:
                    if len(self.txtL.split(", "))>1: 
                        if len(self.txtU.split(", "))==len(self.txtL.split(", ")) and (len(self.txtU.split(", "))+len(self.txtL.split(", ")))%2==0:
                            obj= self.txtU.split(", ")+ self.txtL.split(", ")
                            self.uiStuffClass.loadingBar(1, 2)
                            self.uiStuffClass.loadingBar(2)
                            srf=cmds.nurbsPlane(n="srf", ax=[0,1,0], d=1, ch=0, lr=1)
                            if len(self.txtU.split(", "))+len(self.txtL.split(", "))==6:
                                cmds.rebuildSurface(srf, du=2, dv=1, dir=0, su=1, sv=1, ch=0)
                            elif len(obj)>=8:        
                                cmds.rebuildSurface(srf, du=3, dv=1, dir=0, su=(len(obj)/2-3), sv=1, ch=0)
                            for x, stuff in enumerate(obj): 
                                pp= cmds.xform(stuff, q=1, t=1, ws=1)
                                if x>=len(obj)/2:
                                    cmds.xform("%s.cv[%s][%s]"%(srf[0],x-len(obj)/2,0), t=(pp[0],pp[1],pp[2]), ws=1)
                                else:    
                                    cmds.xform("%s.cv[%s][%s]"%(srf[0],x,1), t=(pp[0],pp[1],pp[2]), ws=1)
                            cmds.xform(srf, cp=1)  
                            cmds.toggle(srf, cv=1)
                            self.uiStuffClass.loadingBar(2)
                            self.uiStuffClass.loadingBar(3)
                        else:
                            cmds.warning("<UPPER> and <LOWER> must have the same amount")
                    else:
                        cmds.warning("<LOWER> textfield must have at least 2 VERTEX")
                else:
                    cmds.warning("<UPPER> textfield must have at least 2 VERTEX")
            else:
                cmds.warning("<LOWER> textfield is empty!")
        else:
            cmds.warning("<UPPER> textfield is empty!")

    def cIso(self, meth):
        obj= cmds.ls(sl=1)
        self.iso= cmds.intSliderGrp(self.nIso, q=1, v=1)   
        preDirec= cmds.optionMenuGrp(self.omDirec, q=1, sl=1)        
        test1= 1
        if obj:
            if len(obj)==1:               
                shp= cmds.listRelatives(obj[0], typ="nurbsSurface")    
                if shp==None: 
                    test1=[] 
                if test1:
                    self.uiStuffClass.loadingBar(1, 1)
                    spaUV= cmds.getAttr("%s.spansUV"%obj[0])
                    degUV= cmds.getAttr("%s.degreeUV"%obj[0])
                    if meth==1:
                        if preDirec==1:
                            cmds.rebuildSurface(obj, rt=0, end=1, dir=2, kr=1, su=spaUV[0][0], sv=spaUV[0][1]+self.iso, du=degUV[0][0], dv=degUV[0][1], rpo=1) 
                        else:
                            cmds.rebuildSurface(obj, rt=0, end=1, dir=2, kr=1, su=spaUV[0][0]+self.iso, sv=spaUV[0][1], du=degUV[0][0], dv=degUV[0][1], rpo=1) 
                    else:
                        if preDirec==1:
                            if spaUV[0][1]-self.iso>0:
                                cmds.rebuildSurface(obj, rt=0, end=1, dir=2, kr=1, su=spaUV[0][0], sv=spaUV[0][1]-self.iso, du=degUV[0][0], dv=degUV[0][1], rpo=1) 
                            else:
                                cmds.rebuildSurface(obj, rt=0, end=1, dir=2, kr=1, su=spaUV[0][0], sv=1, du=degUV[0][0], dv=degUV[0][1], rpo=1) 
                        else:
                            if spaUV[0][0]-self.iso>0:
                                cmds.rebuildSurface(obj, rt=0, end=1, dir=2, kr=1, su=spaUV[0][0]-self.iso, sv=spaUV[0][1], du=degUV[0][0], dv=degUV[0][1], rpo=1) 
                            else:
                                cmds.rebuildSurface(obj, rt=0, end=1, dir=2, kr=1, su=1, sv=spaUV[0][1], du=degUV[0][0], dv=degUV[0][1], rpo=1) 
                    self.uiStuffClass.loadingBar(2)
                    self.uiStuffClass.loadingBar(3, sel=obj, tim=0.1)
            else:
                cmds.warning("Please select only 1 SURFACE")
        else:
            cmds.warning("Please select 1 SURFACE")

    def sFix(self, num, meth):
        obj= cmds.ls(sl=1, fl=1)
        test1= 1
        for item in obj:
            if ".cv" not in item:
                test1= []
        if test1:
            if len(obj)==num:
                self.uiStuffClass.loadingBar(1, 1)
                p1= cmds.xform(obj[0], q=1, t=1, ws=1)
                if meth==1:
                    p2= cmds.xform(obj[2], q=1, t=1, ws=1)
                    cmds.xform(obj[1], t=((p1[0]+p2[0])/2,(p1[1]+p2[1])/2,(p1[2]+p2[2])/2), ws=1)
                elif meth==2:
                    p2= cmds.xform(obj[1], q=1, t=1, ws=1)
                    cmds.xform(obj[1], t=(p1[0], p1[1], p1[2]), ws=1)
                    cmds.xform(obj[0], t=(p2[0], p2[1], p2[2]), ws=1)                     
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, tim=0.1)
            else:
                cmds.warning("Please select only 3 CV")
        else:
            cmds.warning("Please select 3 CV")

    def checkSrfDirec(self, meth):
        obj= cmds.ls(sl=1)
        test1, test2, test3= 1, 1, 1
        if obj:    
            for item in obj:
                shp= cmds.listRelatives(item, typ="nurbsSurface")    
                if shp:               
                    uv= cmds.getAttr("%s.degreeUV"%item)
                    if uv[0][0]!=1:
                        test2=[]
                else:
                    test1=[]
            if test1:
                if test2:  
                    self.uiStuffClass.loadingBar(1, 1)
                    if meth==1:
                        for item in obj:
                            pd1= cmds.createNode("paramDimension", n="%s_pd1"%item)
                            cmds.connectAttr("%s.worldSpace[0]"%item, "%s.nurbsGeometry"%pd1) 
                            cmds.setAttr("%s.vParamValue"%pd1, 0.5)
                            cmds.setAttr("%s.uParamValue"%pd1, 1) 
                        cmds.select(obj)  
                    elif meth==2:
                        for stuff in obj:
                            shp= cmds.listRelatives(stuff, typ="nurbsSurface")  
                            pd= cmds.listConnections(shp, t="paramDimension")
                            if pd:
                                cmds.delete(pd) 
                                test3= []
                        if test3:
                            cmds.warning("All of the surface have no preview to delete")      
                    else:
                        for item in obj:
                            pp1= cmds.xform("%s.cv[0][1]"%item, q=1, t=1, ws=1)
                            pp2= cmds.xform("%s.cv[1][1]"%item, q=1, t=1, ws=1)
                            pp3= cmds.xform("%s.cv[1][0]"%item, q=1, t=1, ws=1)
                            pp4= cmds.xform("%s.cv[0][0]"%item, q=1, t=1, ws=1)
                            cmds.xform("%s.cv[0][1]"%item, t=(pp2[0],pp2[1],pp2[2]), ws=1) 
                            cmds.xform("%s.cv[1][1]"%item, t=(pp3[0],pp3[1],pp3[2]), ws=1) 
                            cmds.xform("%s.cv[1][0]"%item, t=(pp4[0],pp4[1],pp4[2]), ws=1) 
                            cmds.xform("%s.cv[0][0]"%item, t=(pp1[0],pp1[1],pp1[2]), ws=1) 
                    self.uiStuffClass.loadingBar(2)
                    self.uiStuffClass.loadingBar(3, tim=0.1)
                else:
                    cmds.warning("One of the selected surface have more than 4 CONTROL VERTEX")
            else:
                cmds.warning("One of the selected object is not a SURFACE")
        else:
            cmds.warning("Please select at least one SURFACE")

    def grab31(self):
        obj= cmds.ls(sl=1)
        if obj:           
            if len(obj)==1:                  
                shp= cmds.listRelatives(obj, typ="nurbsSurface")                   
                if shp:
                    cmds.textFieldButtonGrp(self.txtFSrf, e=1, tx="%s"%obj[0])
                else:
                    cmds.warning("Selected object is not a SURFACE")   
            else:
                cmds.warning("Please select only 1 SURFACE")
        else:
            cmds.warning("Please select 1 SURFACE")

    def grab32(self):
        obj= cmds.ls(sl=1)
        if obj:                    
            cmds.textFieldButtonGrp(self.txtFTar, e=1, tx="%s"%", ".join(obj))  
        else:
            cmds.warning("Please select at least 1 TARGET")      

    def srfConst(self):    
        obj= cmds.ls(sl=1)
        srf= cmds.textFieldGrp(self.txtFSrf, q=1, tx=1)   
        tar= cmds.textFieldGrp(self.txtFTar, q=1, tx=1)      
        test1, test2, test3= 1,1,1
        if srf:
            if tar:
                if srf not in tar.split(", "):
                    #Because will reparent target, so cannot work with duplicated object
                    for item in tar.split(", "):
                        if "|" in item:
                            test1=[]
                    if test1:  
                        dup= cmds.duplicate(srf, n="%s_srfTemp"%srf)
                        cmds.xform(dup[0], ztp=1)
                        skinClusterName= mel.eval("findRelatedSkinCluster %s"%srf)
                        if skinClusterName:
                            test2=[]
                        else:
                            attrStatus=[]
                            for stuff in ("tx","ty","tz","rx","ry","rz","sx","sy","sz"):
                                attrStatus.append(cmds.getAttr("%s.%s"%(srf,stuff), l=1))
                                cmds.setAttr("%s.%s"%(srf,stuff), l=0)
                            #Freeze the surface
                            cmds.makeIdentity(srf, a=1, t=1, r=1, s=1, n=0, pn=1)
                            for stuff, thing in zip(["tx","ty","tz","rx","ry","rz","sx","sy","sz"],attrStatus):
                                if thing==1:
                                    cmds.setAttr("%s.%s"%(srf,stuff), l=1) 
                        cmds.delete(dup)     
                        if test2:
                            piv= cmds.xform(srf, t=1, q=1, ws=1)
                            if [round(piv[0],2), round(piv[1],2), round(piv[2],2)]!=[0.0, 0.0, 0.0]:
                                if cmds.checkBoxGrp(self.cbWs, q=1, v1=1)==0:
                                    test3= []
                            conti1= self.dialogClass.continueDialog(test3, "Surface is under a group that channel value, will have problem if continue without using <WorldSpace>")
                            if conti1:
                                self.uiStuffClass.loadingBar(1, 1)
                                for item in tar.split(", "):
                                    if cmds.checkBoxGrp(self.cbNG, q=1, v1=1):
                                        tempTar= cmds.group(n="%s_surfaceCons"%item, em=1, p=item)
                                        par= cmds.listRelatives(item, p=1, pa=1)
                                        if par:
                                            realTar= cmds.parent(tempTar, par)
                                        else:
                                            realTar= cmds.parent(tempTar, w=1)
                                    else:
                                        if cmds.objectType(item)=="joint":
                                            cmds.setAttr("%s.jointOrient"%item, 0,0,0)
                                        realTar= [item]   
                                    dcmTemp= cmds.createNode("decomposeMatrix")            
                                    cposTemp= cmds.createNode("closestPointOnSurface") 
                                    posi= cmds.createNode("pointOnSurfaceInfo", n="%s_posi"%realTar[0]) 
                                    fbfm= cmds.createNode("fourByFourMatrix", n="%s_fbfm"%realTar[0]) 
                                    mm= cmds.createNode("multMatrix", n="%s_mm"%realTar[0]) 
                                    dcm= cmds.createNode("decomposeMatrix", n="%s_dcm"%realTar[0]) 
                                    cmds.connectAttr("%s.worldMatrix[0]"%realTar[0], "%s.inputMatrix"%dcmTemp)        
                                    cmds.connectAttr("%s.outputTranslate"%dcmTemp, "%s.inPosition"%cposTemp)
                                    if cmds.checkBoxGrp(self.cbWs, q=1, v1=1):
                                        cmds.connectAttr("%s.worldSpace"%srf, "%s.inputSurface"%cposTemp)
                                        cmds.connectAttr("%s.worldSpace"%srf, "%s.inputSurface"%posi)
                                    else:
                                        cmds.connectAttr("%s.local"%srf, "%s.inputSurface"%cposTemp)
                                        cmds.connectAttr("%s.local"%srf, "%s.inputSurface"%posi)
                                    cmds.connectAttr("%s.parameterU"%cposTemp, "%s.parameterU"%posi)
                                    cmds.connectAttr("%s.parameterV"%cposTemp, "%s.parameterV"%posi)          
                                    cmds.disconnectAttr("%s.parameterU"%cposTemp, "%s.parameterU"%posi)
                                    cmds.disconnectAttr("%s.parameterV"%cposTemp, "%s.parameterV"%posi)             
                                    cmds.delete(dcmTemp,cposTemp)
                                    for x, stuff in enumerate(["X","Y","Z"]):
                                        cmds.connectAttr("%s.normalizedTangentU%s"%(posi,stuff), "%s.in0%s"%(fbfm, x))        
                                        cmds.connectAttr("%s.normalizedNormal%s"%(posi,stuff), "%s.in1%s"%(fbfm, x))        
                                        cmds.connectAttr("%s.normalizedTangentV%s"%(posi,stuff), "%s.in2%s"%(fbfm, x))        
                                        cmds.connectAttr("%s.position%s"%(posi,stuff), "%s.in3%s"%(fbfm, x))    
                                        cmds.connectAttr("%s.outputTranslate%s"%(dcm, stuff), "%s.translate%s"%(realTar[0], stuff))        
                                        cmds.connectAttr("%s.outputRotate%s"%(dcm, stuff), "%s.rotate%s"%(realTar[0], stuff))                 
                                    cmds.connectAttr("%s.output"%fbfm, "%s.matrixIn[0]"%mm)
                                    cmds.connectAttr("%s.parentInverseMatrix[0]"%realTar[0], "%s.matrixIn[1]"%mm)
                                    cmds.connectAttr("%s.matrixSum"%mm, "%s.inputMatrix"%dcm)   
                                    if cmds.checkBoxGrp(self.cbNG, q=1, v1=1):
                                        cmds.parent(item, realTar)
                                self.uiStuffClass.loadingBar(2)
                                self.uiStuffClass.loadingBar(3, sel=srf)
                        else:
                            cmds.warning("Selected surface have skinCluster hence cannot freeze or unfreeze")  
                    else:
                        cmds.warning("One of the selected target have duplicated names")            
                else:
                    cmds.warning("Cannot contrain to self")                
            else:
                cmds.warning("<TARGETS> textField is empty!")  
        else:
            cmds.warning("<SURFACE> textField is empty!")                


    def helps(self):
        name="Help On SurfaceMaker"
        helpTxt="""
        - Create, Edit, Constraint surface for rigging purpose



        < Create >
        ==========
            1) Create Surface
            --------------------
                - Create surface at selection

                - <Each> (Create Multi)
                    - Create Multiple surface on each selections (if any) instead of a single surface

                - <More Hull> (Linear) / (Arc)
                    - Add extra inbetween CVs 
                    (*Linear / Arc determine the extra CVs position)

                - <Zero Orient Last Joint> 
                    - Make the end of surface straighter (follow the 2nd last orientation)

                - <Close End> (Circular)
                    - Will close the end of surface to the start             

                *(The smaller the width, the more accurate for copy weight, usually i use 0.1)


            2) Create Surface Plane
            -------------------------
                - Create plane according to vertex selection
                (* This is to create dummy surface according to geometry for copy weight)
                (* Up and down position if can should match because copy weight depends on the isoparm line)

                (* Tested that dummy surface for different shape, plane > sphere. Dummy geo for same shape, cube > cube)

                        
        < Edit >
        =========
            1) Isoparms
            -------------
                - Add / remove horizontally/vertically
                (* V= horizontal, U= vertical)        

            2) Fix
            ------
                1. Snap Inbetween Fix
                    - Fix middle cv by snapping inbetween 2 cvs 

                2. Swap Position Fix
                    - Exchange position of 2 cvs that are flipped   

            3) Check Surface Direction 
            ---------------------------
                1. Preview X-axis Direction
                    - Will create a "parameter dimension" on the surface to indicate x-axis direction when use <Surface Constraint>
                    - This also determine direction will affect shear, which will not 

                2. Delete Preview

                3. Rotate Surface Direction
                    - Rotate the surface CV to change the x-axis direction


    < Surface Constraint >
    ==========================
        - Constraint something(joint) to a surface
        - Able to constraint multiple target
        - Eg.
            - Create ribbon joints
            - Wan a tweak ctrl that follow a skinned object (similar to follicle but depends on skin)
            - Use for if you wan less bindjoint/ctrl but u wan smooth deformation

        <Constrained New group>    
            - Will create a new group and constraint it instead the target
            - When use this, it works even if the surface and target have different orientation

        <Surface WorldSpace>
            - Without it, will use "local" for input. When move the surface, target wont move unless move the cv
            - With it, will use "worldSpace" for input. When move the surface, target will move

            (* Both procedure will freeze the surface except if the surface have skincluster)
            (* Will have issue when surface is under a group that have value and using <local>)
        """
        self.helpBoxClass.helpBox1(name, helpTxt) 

    def reloadSub(self):
        SurfaceMaker()
    

if __name__=='__main__':
    SurfaceMaker()