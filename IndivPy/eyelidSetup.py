import maya.cmds as cmds
import maya.mel as mel
import Mod.uiStuff as uiStuff
import Mod.dialog as dialog
import Mod.helpBox as helpBox
import IndivPy.Image as eyelidImg 
import re
import math
    
class EyelidSetup(object):
    def __init__(self, *args):
        self.uiStuffClass= uiStuff.UiStuff()
        self.dialogClass= dialog.Dialog()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()
        self.preCheck()


    def win(self):
        try: 
            cmds.deleteUI("eyelidSet") 
        except:
            pass    
        cmds.window("eyelidSet", mb=1)              
        cmds.window("eyelidSet", t="Eyelid Setup", s=1, e=1, wh=(275,620))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on EyelidSetup", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload EyelidSetup", c=lambda x:self.reloadSub())   
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Create")
        form1= cmds.formLayout(nd=100, p=column1)
        self.drop11= cmds.optionMenuGrp(l="", cw2=(1,0), cc=lambda x:self.om())
        cmds.menuItem(l="EyeAim + Eyelid")
        cmds.menuItem(l="EyeAim") 
        sep11= cmds.separator(h=5, st="in")
        cmds.formLayout(form1, e=1,
                                af=[(self.drop11, "top", 5),
                                    (sep11, "top", 35)],
                                ap=[(self.drop11, "left", -50, 49),
                                    (self.drop11, "right", 0, 51),
                                    (sep11, "left", 0, 0),
                                    (sep11, "right", 0, 100)]) 
        self.form2= cmds.formLayout(nd=100, p=column1)
        txt1= cmds.text(l="Select 1 MESH", fn="smallObliqueLabelFont", en=0, al="center")
        self.b111= cmds.button(l="Eyeball", c=lambda x:self.preCre(1, self.b112, "eyeball", "Eyeball"))
        self.b112= cmds.button(l="?", c=lambda x:self.instruc("1_eyeball", "Eyeball"), ebg=0, bgc=(0.55,0.55,0.55))    
        self.b113= cmds.button(l="Delete", c=lambda x:self.delePre(self.b112, "eyeball", "Eyeball"))
        txt2= cmds.text(l="Select 1 VERTEX", fn="smallObliqueLabelFont", en=0, al="center")  
        self.b211= cmds.button(l="Inner Corner Eyelid", c=lambda x:self.preCre(2, self.b212, "inCornEyelid", "Inner Corner Eyelid"))
        self.b212= cmds.button(l="?", c=lambda x:self.instruc("2_innerCorner", "Inner Corner Eyelid"), ebg=0, bgc=(0.55,0.55,0.55)) 
        self.b213= cmds.button(l="Delete", c=lambda x:self.delePre(self.b212, "inCornEyelid", "Inner Corner Eyelid"))
        self.b221= cmds.button(l="Outer Corner Eyelid", c=lambda x:self.preCre(2, self.b222, "outCornEyelid", "Outer Corner Eyelid"))
        self.b222= cmds.button(l="?", c=lambda x:self.instruc("3_outerCorner", "Outer Corner Eyelid"), ebg=0, bgc=(0.55,0.55,0.55))    
        self.b223= cmds.button(l="Delete", c=lambda x:self.delePre(self.b222, "outCornEyelid", "Outer Corner Eyelid"))
        self.b231= cmds.button(l="Middle Pupil", c=lambda x:self.preCre(2, self.b232, "midPupil", "Middle Pupil"))
        self.b232= cmds.button(l="?", c=lambda x:self.instruc("4_middlePupil", "Middle Pupil"), ebg=0, bgc=(0.55,0.55,0.55))   
        self.b233= cmds.button(l="Delete", c=lambda x:self.delePre(self.b232, "midPupil", "Middle Pupil"))
        txt3= cmds.text(l="Select 1 EDGELOOP", fn="smallObliqueLabelFont", en=0, al="center")  
        self.b311= cmds.button(l="Outer End Eyelid", c=lambda x:self.preCre(3, self.b312, "outEndEyelid", "Outer End Eyelid"))
        self.b312= cmds.button(l="?", c=lambda x:self.instruc("51_outerEndEyelid", "Outer End Eyelid"), ebg=0, bgc=(0.55,0.55,0.55))
        self.b313= cmds.button(l="Delete", c=lambda x:self.delePre(self.b312, "outEndEyelid", "Outer End Eyelid"))
        self.b321= cmds.button(l="Outer Main Eyelid", c=lambda x:self.preCre(3, self.b322, "outMainEyelid", "Outer Main Eyelid"))
        self.b322= cmds.button(l="?", c=lambda x:self.instruc("52_outerMainEyelid", "Outer Main Eyelid"), ebg=0, bgc=(0.55,0.55,0.55))
        self.b323= cmds.button(l="Delete", c=lambda x:self.delePre(self.b322, "outMainEyelid", "Outer Main Eyelid"))
        self.b331= cmds.button(l="Main Eyelid", c=lambda x:self.preCre(3, self.b332, "mainEyelid", "Main Eyelid"))
        self.b332= cmds.button(l="?", c=lambda x:self.instruc("53_mainEyelid", "Main Eyelid"), ebg=0, bgc=(0.55,0.55,0.55))
        self.b333= cmds.button(l="Delete", c=lambda x:self.delePre(self.b332, "mainEyelid", "Main Eyelid"))
        self.b341= cmds.button(l="Inner Main Eyelid", c=lambda x:self.preCre(3, self.b342, "inMainEyelid", "Inner Main Eyelid"))
        self.b342= cmds.button(l="?", c=lambda x:self.instruc("54_innerMainEyelid", "Inner Main Eyelid"), ebg=0, bgc=(0.55,0.55,0.55))    
        self.b343= cmds.button(l="Delete", c=lambda x:self.delePre(self.b342, "inMainEyelid", "Inner Main Eyelid"))    
        self.b351= cmds.button(l="Inner End Eyelid", c=lambda x:self.preCre(3, self.b352, "inEndEyelid", "Inner End Eyelid"))
        self.b352= cmds.button(l="?", c=lambda x:self.instruc("55_innerEndEyelid", "Inner End Eyelid"), ebg=0, bgc=(0.55,0.55,0.55)) 
        self.b353= cmds.button(l="Delete", c=lambda x:self.delePre(self.b352, "inEndEyelid", "Inner End Eyelid"))
        cmds.formLayout(self.form2, e=1,
                                af=[(txt1, "top", 0),
                                    (self.b111, "top", 16),
                                    (self.b112, "top", 16),
                                    (self.b113, "top", 16),
                                    (txt2, "top", 51),
                                    (self.b211, "top", 67),
                                    (self.b212, "top", 67),
                                    (self.b213, "top", 67),
                                    (self.b221, "top", 93),
                                    (self.b222, "top", 93),
                                    (self.b223, "top", 93),
                                    (self.b231, "top", 119),
                                    (self.b232, "top", 119),
                                    (self.b233, "top", 119),
                                    (txt3, "top", 154),
                                    (self.b311, "top", 170),
                                    (self.b312, "top", 170),
                                    (self.b313, "top", 170),
                                    (self.b321, "top", 196),
                                    (self.b322, "top", 196),
                                    (self.b323, "top", 196),
                                    (self.b331, "top", 222),
                                    (self.b332, "top", 222),
                                    (self.b333, "top", 222),
                                    (self.b341, "top", 248),
                                    (self.b342, "top", 248),
                                    (self.b343, "top", 248),
                                    (self.b351, "top", 274),
                                    (self.b352, "top", 274),
                                    (self.b353, "top", 274)],
                                ap=[(txt1, "left", 0, 0),
                                    (txt1, "right", 0, 100),
                                    (self.b111, "left", 0, 0),
                                    (self.b111, "right", 0, 55),
                                    (self.b112, "left", 0, 60),
                                    (self.b112, "right", 0, 65),
                                    (self.b113, "left", 0, 70),
                                    (self.b113, "right", 0, 100),
                                    (txt2, "left", 0, 0),
                                    (txt2, "right", 0, 100),
                                    (self.b211, "left", 0, 0),
                                    (self.b211, "right", 0, 55),
                                    (self.b212, "left", 0, 60),
                                    (self.b212, "right", 0, 65),
                                    (self.b213, "left", 0, 70),
                                    (self.b213, "right", 0, 100),
                                    (self.b221, "left", 0, 0),
                                    (self.b221, "right", 0, 55),
                                    (self.b222, "left", 0, 60),
                                    (self.b222, "right", 0, 65),
                                    (self.b223, "left", 0, 70),
                                    (self.b223, "right", 0, 100),
                                    (self.b231, "left", 0, 0),
                                    (self.b231, "right", 0, 55),
                                    (self.b232, "left", 0, 60),
                                    (self.b232, "right", 0, 65),
                                    (self.b233, "left", 0, 70),
                                    (self.b233, "right", 0, 100),
                                    (txt3, "left", 0, 0),
                                    (txt3, "right", 0, 100),
                                    (self.b311, "left", 0, 0),
                                    (self.b311, "right", 0, 55),
                                    (self.b312, "left", 0, 60),
                                    (self.b312, "right", 0, 65),
                                    (self.b313, "left", 0, 70),
                                    (self.b313, "right", 0, 100),
                                    (self.b321, "left", 0, 0),
                                    (self.b321, "right", 0, 55),
                                    (self.b322, "left", 0, 60),
                                    (self.b322, "right", 0, 65),
                                    (self.b323, "left", 0, 70),
                                    (self.b323, "right", 0, 100),
                                    (self.b331, "left", 0, 0),
                                    (self.b331, "right", 0, 55),
                                    (self.b332, "left", 0, 60),
                                    (self.b332, "right", 0, 65),
                                    (self.b333, "left", 0, 70),
                                    (self.b333, "right", 0, 100),
                                    (self.b341, "left", 0, 0),
                                    (self.b341, "right", 0, 55),
                                    (self.b342, "left", 0, 60),
                                    (self.b342, "right", 0, 65),
                                    (self.b343, "left", 0, 70),
                                    (self.b343, "right", 0, 100),
                                    (self.b351, "left", 0, 0),
                                    (self.b351, "right", 0, 55),
                                    (self.b352, "left", 0, 60),
                                    (self.b352, "right", 0, 65),
                                    (self.b353, "left", 0, 70),
                                    (self.b353, "right", 0, 100)])         
        form3= cmds.formLayout(nd=100, p=column1)
        sep31= cmds.separator(h=5, st="in")
        self.b1= cmds.button(l="Step 1", c=lambda x:self.step1()) 
        self.b2= cmds.button(l="Step 2", c=lambda x:self.step2()) 
        self.b3= cmds.button(l="Step 3", c=lambda x:self.step3())
        self.b4= cmds.button(l="Cage", c=lambda x:self.cage())  
        cmds.formLayout(form3, e=1,
                                af=[(sep31, "top", 15),
                                    (self.b1, "top", 20),
                                    (self.b2, "top", 46),
                                    (self.b3, "top", 72),
                                    (self.b4, "top", 118)],
                                ap=[(sep31, "left", 0, 0),
                                    (sep31, "right", 0, 100),
                                    (self.b1, "left", 0, 0),
                                    (self.b1, "right", 0, 100),
                                    (self.b2, "left", 0, 0),
                                    (self.b2, "right", 0, 100),
                                    (self.b3, "left", 0, 0),
                                    (self.b3, "right", 0, 100),
                                    (self.b4, "left", 0, 0),
                                    (self.b4, "right", 0, 100)]) 
        cmds.setFocus(cmds.text(l=""))   
        cmds.showWindow("eyelidSet")

    def om(self):
        if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
            for butt in [self.b211,self.b221,self.b311,self.b321,self.b331,self.b341,self.b351,self.b1,self.b2,self.b4]:
                cmds.button(butt, e=1, en=1)
        else:
            for butt in [self.b211,self.b221,self.b311,self.b321,self.b331,self.b341,self.b351,self.b1,self.b2,self.b4]:
                cmds.button(butt, e=1, en=0)
        self.preCheck()

    def preCheck(self):
        for thing,butt in zip(["eyeball","inCornEyelid","outCornEyelid","midPupil","outEndEyelid","outMainEyelid","mainEyelid","inMainEyelid","inEndEyelid"],[self.b112,self.b212,self.b222,self.b232,self.b312,self.b322,self.b332,self.b342,self.b352]):
            if cmds.objExists("%s_plc"%thing):
                cmds.button(butt, e=1, ebg=0, bgc=(0.3,0.9,0.3))
            else:
                cmds.button(butt, e=1, ebg=0, bgc=(0.55,0.55,0.55))

    def instruc(self, imageName, parts):
        #Find image location
        imgPath= eyelidImg.__file__.replace("\\__init__.pyc", "/%s.jpg"%imageName)

        #Create instruction window
        try: 
            cmds.deleteUI("instruction") 
        except:
            pass    
        cmds.window("instruction", mb=1)              
        cmds.window("instruction", t="Placer Instruction", s=1, e=1, wh=(300,200))  
        form1= cmds.formLayout(nd=100)
        txt1= cmds.text(l=parts, fn="smallObliqueLabelFont", en=0, al="center")
        img= cmds.iconTextButton(style="iconOnly", image1=imgPath, w=400,h=400)
        cmds.formLayout(form1, e=1,
                                af=[(txt1, "top", 0),
                                    (img, "top", 20),],
                                ap=[(txt1, "left", 0, 0),
                                    (txt1, "right", 0, 100)])                                      
        cmds.setFocus(cmds.text(l=""))   
        cmds.showWindow("instruction")

    def preCre(self, meth, butt, parts1, parts2):
        obj= cmds.ls(sl=1, fl=1)
        #Check placerGrp exist or not
        if cmds.objExists("Eye_Placer_GRP")==0:
            cmds.createNode("transform", n="Eye_Placer_GRP")
        if cmds.objExists("eyeMisc_plc_grp")==0:
            cmds.createNode("transform", n="eyeMisc_plc_grp")
            cmds.setAttr("eyeMisc_plc_grp.v", 0)
        for col,val in zip(["yellow", "green", "blue"], [(0.9,0.9,0.3),(0.3,0.9,0.3),(0.3,0.3,0.9)]):
            if cmds.objExists("%sSrfBall"%col)==0:    
                srfBall= cmds.sphere(n="%sSrfBall"%col, ax=(0,1,0), ssw=0, esw=360, r=0.33, d=3 ,s=8, nsp=4, ch=0)
                shaE= cmds.createNode("shadingEngine", n="%sSrfBall_shaE"%col)
                md= cmds.createNode("multiplyDivide", n="%sSrfBall_md"%col)
                self.noRender("%sShape"%srfBall[0])
                tempC= cmds.listConnections("%sShape.instObjGroups[0]"%srfBall[0], c=1, p=1)
                cmds.disconnectAttr("%s"%tempC[0], "%s"%tempC[1])
                cmds.connectAttr("%sShape.instObjGroups[0]"%srfBall[0], "%s.dagSetMembers[0]"%shaE)
                cmds.connectAttr("%s.input1"%md, "%s.surfaceShader"%shaE)
                cmds.setAttr("%s.input1"%md, *val)
                cmds.setAttr("%s.overrideEnabled"%srfBall[0], 1)
                cmds.setAttr("%s.overrideDisplayType"%srfBall[0], 2)
                cmds.parent(srfBall, "eyeMisc_plc_grp")
        if cmds.objExists("eyeCirExtru_crv")==0:
            exCrv= cmds.circle(n="eyeCirExtru_crv", nr=(0,1,0), sw=(360), r=0.33, d=1, tol=0.01, s=8, ch=1) 
            cmds.parent(exCrv[0], "eyeMisc_plc_grp")

        #Real function
        if meth==1:
            finalTest= self.grabMesh(obj, parts1, parts2)
        elif meth==2:
            finalTest= self.grabVert(obj, parts1, parts2)
        elif meth==3:
            finalTest= self.grabEdge(obj, parts1, parts2)
        
        #Change button color
        if finalTest:
            cmds.button(butt, e=1, ebg=0, bgc=(0.3,0.8,0.3))
            self.preCheck()

    def delePre(self, butt, parts1, parts2):
        obj= cmds.ls(sl=1)
        cmds.button(butt, e=1, ebg=0, bgc=(0.55,0.55,0.55))
        if cmds.objExists("%s_plc"%parts1):
            cmds.delete("%s_plc"%parts1)
            self.preCheck()
            try:
                cmds.select(obj)
            except:
                pass
        else:
            cmds.warning("%s Placer does not exist"%parts2)

    def createLoc1(self, locName, srfBallName, piv, scal=[]):
        loc= cmds.createNode("transform", n="%s"%locName)
        locShp= cmds.createNode("locator", p=loc, n="%s"%loc.replace("_plc","_plcShape"))             
        self.ctrlShp(loc, 13)
        for attr in ["rx","ry","rz","v"]:
            cmds.setAttr("%s.%s"%(loc,attr), l=1, k=0)  
        dupBall= cmds.duplicate("yellowSrfBall", n="%s"%srfBallName)
        self.multiGrp(dupBall,loc, "Eye_Placer_GRP")
        cmds.xform(loc, t=(piv[0],piv[1],piv[2]), ws=1)
        if scal:
            cmds.setAttr("%s.s"%loc, scal[0],scal[1],scal[2])
        cmds.connectAttr("%s.sx"%loc, "%s.sy"%loc)
        cmds.connectAttr("%s.sx"%loc, "%s.sz"%loc) 
        cmds.select(loc)

    def grabMesh(self, obj, parts1, parts2):   
        finalTest= []
        if cmds.objExists("%s_plc"%parts1)==0 and cmds.objExists("%s_plc_grp"%parts1)==0:
            if len(obj)==1:
                shp= cmds.listRelatives(obj, typ="mesh")
                if shp:
                    #Get world bounding box
                    dupTemp= cmds.duplicate(obj, po=1)
                    cmds.parent(shp, dupTemp, r=1 ,s=1)
                    newDup= cmds.duplicate(dupTemp)
                    cmds.parent(shp, obj, r=1 ,s=1)
                    cmds.makeIdentity(newDup, a=1, r=1, n=0, pn=1)
                    bb= cmds.xform(newDup, q=1, bb=1, ws=1)
                    scal= (abs(bb[0]-bb[3])/2*3, abs(bb[1]-bb[4])/2*3, abs(bb[2]-bb[5])/2*3)
                    cmds.delete(dupTemp, newDup)

                    #If pivot point is in origin, might be forget to center pivot so find the middle of bounding box
                    piv= cmds.xform(obj, q=1, rp=1, ws=1) 
                    if (round(piv[0],3),round(piv[1],3),round(piv[2],3))==(0.0,0.0,0.0):
                        piv= ((bb[0]+bb[3])/2, (bb[1]+bb[4])/2, (bb[2]+bb[5])/2)

                    self.createLoc1("%s_plc"%parts1, "%sSrfBall_plc"%parts1, piv, scal)
                    finalTest= 1
                else:
                    cmds.warning("Please select 1 MESH")
            else:
                cmds.warning("Please select only 1 MESH")
        else:
            cmds.warning("%s Placer already exist"%parts2)
        return finalTest

    def grabVert(self, obj, parts1, parts2):   
        finalTest= []
        if cmds.objExists("%s_plc"%parts1)==0 and cmds.objExists("%s_plc_grp"%parts1)==0:
            if len(obj)==1:  
                if ".vtx" in obj[0]:
                    piv= cmds.xform(obj[0], q=1, t=1, ws=1)
                    self.createLoc1("%s_plc"%parts1, "%sSrfBall_plc"%parts1, piv)
                    if cmds.objExists("eyeball_plc"):
                        scal= cmds.getAttr("eyeball_plc.sx")
                        if round(cmds.getAttr("%s_plc.sx"%parts1),3)== 1.0:
                            cmds.setAttr("%s_plc.sx"%parts1, scal/60)
                    finalTest= 1
                else:
                    cmds.warning("Please select 1 VERTEX")
            else:
                cmds.warning("Please select only 1 VERTEX") 
        else:
            cmds.warning("%s Placer already exist"%parts2)
        return finalTest

    def grabEdge(self, obj, parts1, parts2):   
        newObj, extra, test1, finalTest= [],[],[],[]
        test2= 1
        if cmds.objExists("%s_plc"%parts1)==0 and cmds.objExists("%s_plc_grp"%parts1)==0:
            if obj:  
                for item in obj:
                    if ".e" in item:
                        test1= 1
                        newObj.append(item)
                    if ".e" not in item:
                        test2= []
                    if ".vtx" in item:
                        extra.append(item)
                #Only for 1 edgeloop
                if test1 and test2:
                    self.createEdgeCrv(obj, parts1, "inCornEyelid_plc", "outCornEyelid_plc")
                    finalTest= 1
                #For 1 edgeloop + 2 vertex selection
                else:
                    if len(extra)==2:
                        tempPiv1= cmds.xform(extra[0], q=1, t=1, ws=1)
                        tempPiv2= cmds.xform(extra[1], q=1, t=1, ws=1) 
                        if tempPiv1[0]>tempPiv2[0]:
                            inCorn= extra[0]
                            outCorn= extra[1]
                        else:
                            inCorn= extra[1]  
                            outCorn= extra[0]
                        self.createEdgeCrv(newObj, parts1, inCorn, outCorn)  
                        finalTest= 1    
                    else:
                        cmds.warning("Please select only 1 EDGELOOP") 
            else:
                cmds.warning("Please select 1 EDGELOOP") 
        else:
            cmds.warning("%s Placer already exist"%parts2)
        return finalTest

    def createEdgeCrv(self, newObj, parts1, inCorn, outCorn):
        start = cmds.timerX()
        inCornEpTemp, outCornEpTemp, up_crv, low_crv, inPiv, outPiv, allInPiv, allOutPiv, sameVertPiv= [],[],[],[],[],[],[],[],[]
        #Apparently "polyToCurve" works better with selection instead of putting as a flag
        cmds.select(newObj)
        crv= cmds.polyToCurve(n="%s_plc"%parts1, form=2, dg=1, ch=0)
        spanCorn= cmds.getAttr("%s.spans"%crv[0])
        for corn,plc,par in zip([inCorn,outCorn], ["inCornEyelid_plc","outCornEyelid_plc"], [allInPiv,allOutPiv]):
            temp, allVertPiv= [],[]
            #If corner is not define
            if corn==plc and cmds.objExists(plc)==0:
                cornPiv= (0,0,0)
            else:
                cornPiv= cmds.xform(corn, q=1, t=1, ws=1)
            if cornPiv!= (0,0,0):
                allVert= cmds.ls(cmds.polyListComponentConversion(newObj, tv=1), fl=1)
                for item in allVert:
                    finalEdgeLoop= []
                    vertPiv= cmds.xform(item, q=1, t=1, ws=1)
                    finalPiv= (round(vertPiv[0],3),round(vertPiv[1],3),round(vertPiv[2],3))
                    convEdge= cmds.polyListComponentConversion(item, te=1)
                    allEdgeLoop= cmds.ls(cmds.polySelectSp(convEdge, q=1, l=1), fl=1)
                    for stuff in allEdgeLoop:
                        if stuff not in newObj:
                            finalEdgeLoop.append(stuff)
                    allVertLoop= cmds.ls(cmds.polyListComponentConversion(finalEdgeLoop, tv=1), fl=1)
                    for thing in allVertLoop:
                        pivTemp= cmds.xform(thing, q=1, t=1, ws=1)
                        #Break to optimize speed and even if corner is in same loop, they will be separated
                        if finalPiv not in sameVertPiv:
                            if (round(pivTemp[0],3),round(pivTemp[1],3),round(pivTemp[2],3))==(round(cornPiv[0],3),round(cornPiv[1],3),round(cornPiv[2],3)):
                                allVertPiv.append(finalPiv)   
                                sameVertPiv.append(finalPiv)
                                break
                    else:
                        continue
                    break

            #Noting each distance
            for x in range(spanCorn):
                cvPiv= cmds.xform("%s.ep[%s]"%(crv[0],x), q=1, t=1, ws=1)               
                if cornPiv== (0,0,0):
                    par.append(cvPiv[0])
                else:
                    #This is all distance
                    par.append(math.sqrt(abs(cvPiv[0]-cornPiv[0])**2 + abs(cvPiv[1]-cornPiv[1])**2 + abs(cvPiv[2]-cornPiv[2])**2))
                    #Find which Ep on crv that is on the side edgeloop
                    if (round(cvPiv[0],3),round(cvPiv[1],3),round(cvPiv[2],3)) in allVertPiv:
                        temp= x

            #If corner is not on vertex, then use shortest distance
            if corn== inCorn:
                if temp:
                    inCornEpTemp= temp
                else:
                    inCornEpTemp= par.index(min(par))
            else:
                if cornPiv!=(0,0,0):
                    if temp:
                        outCornEpTemp= temp
                    else:
                        outCornEpTemp= allOutPiv.index(min(allOutPiv))
                #Using max because corner is not define hence is the furthest from (0,0,0)
                else:
                    outCornEpTemp= allOutPiv.index(max(allOutPiv))
        #Determine which side should the ep0 start from
        inPivTemp= cmds.xform("%s.ep[%s]"%(crv[0],inCornEpTemp), q=1, t=1, ws=1)
        outPivTemp= cmds.xform("%s.ep[%s]"%(crv[0],outCornEpTemp), q=1, t=1, ws=1)
        if inPivTemp[0]>outPivTemp[0]:
            val1= outCornEpTemp
        else:
            val1= inCornEpTemp
        #when create crv, corner might not start from 0 that's why needa moveSeam  
        if inCornEpTemp-val1>=0:
            inCornEp= inCornEpTemp-val1
        else:
            inCornEp= spanCorn+inCornEpTemp-val1
        if outCornEpTemp-val1>=0:
            outCornEp= outCornEpTemp-val1
        else:
            outCornEp= spanCorn+outCornEpTemp-val1  
        if inCornEpTemp!=0 and outCornEpTemp!=0:
            cmds.select("%s.u[%s]"%(crv[0],val1))
            mel.eval('moveNurbsCurveSeam;')
            cmds.select(crv[0]) 

        #DetachCurve wont work well unless one of the point is [0] 
        upLow_crv= cmds.detachCurve("%s.ep[%s]"%(crv[0],inCornEp), "%s.ep[%s]"%(crv[0],outCornEp), cos=1, rpo=0, ch=0)
        cmds.xform(upLow_crv, crv, cp=1)
        upLowTemp1= cmds.xform(upLow_crv[0], q=1, rp=1, ws=1)
        upLowTemp2= cmds.xform(upLow_crv[1], q=1, rp=1, ws=1)   
        if upLowTemp1[1]> upLowTemp2[1]:
            up_crv= upLow_crv[0]
            low_crv= upLow_crv[1]
        else:
            up_crv= upLow_crv[1]
            low_crv= upLow_crv[0]
        crv0= cmds.rename(crv, "%s"%crv[0].replace("_plc", "Full_crv"))    
        crv1= cmds.rename(up_crv, "%sUp_crv"%parts1)
        crv2= cmds.rename(low_crv, "%sLow_crv"%parts1)
        #To fix the half curve's left right directions
        for crvs in [crv1,crv2]:
            inCrvPiv= cmds.xform("%s.ep[0]"%crvs, q=1, t=1, ws=1)  
            outCrvPiv= cmds.xform("%s.ep[%s]"%(crvs,outCornEp), q=1, t=1, ws=1) 
            if inCrvPiv[0]>outCrvPiv[0]:
                cmds.reverseCurve(crvs, ch=0, rpo=1)

        #To fix the full curve's updown directions
        upEp= cmds.xform("%s.ep[%s]"%(crv0, int(outCornEp*3/2)), q=1, t=1, ws=1)
        lowEp= cmds.xform("%s.ep[%s]"%(crv0, int(outCornEp/2)), q=1, t=1, ws=1)
        if lowEp[1]<upEp[1]:
            cmds.reverseCurve(crv0, ch=0, rpo=1)
        
        #Creating srf extrude
        grp= cmds.group(n="%s_plc"%parts1, em=1)
        cmds.parent(grp, "Eye_Placer_GRP")  
        for allCrv,col in zip([crv1,crv2],["green","blue"]):
            extru= cmds.extrude("eyeCirExtru_crv", allCrv, n="%s"%allCrv.replace("crv","srf"), ch=1, rn=0, po=0, et=2, ucp=1, fpt=1, upn=1, rsp=1)
            tempC1= cmds.listConnections("%sShape.instObjGroups[0]"%extru[0], c=1, p=1)
            cmds.disconnectAttr("%s"%tempC1[0], "%s"%tempC1[1])
            self.noRender("%sShape"%extru[0])
            tempC2= cmds.listConnections("%sSrfBallShape.instObjGroups[0]"%col)
            ind= cmds.getAttr("%s.dagSetMembers"%tempC2[0], mi=1)
            cmds.connectAttr("%sShape.instObjGroups[0]"%extru[0], "%s.dagSetMembers[%s]"%(tempC2[0], max(ind)+1))
            cmds.setAttr("%s.overrideEnabled"%extru[0], 1)
            cmds.setAttr("%s.overrideDisplayType"%extru[0], 2)
            cmds.xform(extru, cp=1)
            cmds.parent(extru[0], grp)
        cmds.parent(crv0, crv1, crv2, grp)
        cmds.select(grp) 

        scal= cmds.getAttr("eyeCirExtru_crv.sx")
        bb= cmds.xform(crv0, q=1, bb=1)
        ans= (bb[3]+bb[4]+bb[5]-bb[0]-bb[2]-bb[1])/3/60
        minVal= min(scal, ans)
        if round(scal, 3)==1.0 or minVal*10>ans:
            cmds.setAttr("eyeCirExtru_crv.s", ans, ans, ans)

    def noRender(self, shpN):
        for ren in ["castsShadows","receiveShadows","motionBlur","primaryVisibility","smoothShading","visibleInReflections","visibleInRefractions"]:
            cmds.setAttr("%s.%s"%(shpN,ren), 0)

    def multiGrp(self, *args):
        for item in args:
            if item!= args[-1]:
                cmds.parent(item, args[args.index(item)+1])

    def lockAttr(self, obj, attr):
        for item in attr:
            cmds.setAttr("%s.%s"%(obj,item), k=0, l=1)

    def ctrlShp(self, ctrl, color, meth=1):           
        shp= cmds.listRelatives(ctrl, typ="nurbsCurve")
        newShp= cmds.rename(shp, "%sShape"%ctrl.split("|")[-1])            
        cmds.setAttr("%s.overrideEnabled"%newShp, 1)
        if meth==1:
            cmds.setAttr("%s.overrideColor"%newShp, color)  
        elif meth==2:
            cmds.setAttr("%s.overrideDisplayType"%newShp, 2)
        return newShp

    def step1(self):
        self.final1()
        self.preCheck()

    def step2(self):
        self.final2()
        self.preCheck()

    def step3(self):
        self.final3()
        self.preCheck()

    def cal(self, mul):
        if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
            self.cv1Piv= cmds.getAttr("mainEyelidUp_crv.cv[0]")[0]
            self.cv2Piv= cmds.getAttr("mainEyelidUp_crv.cv[*]")[-1]
            self.spans= cmds.getAttr("mainEyelidUp_crv.spans") 
            self.midUp= cmds.xform("mainEyelidUp_crv", q=1, bb=1, ws=1)
            self.midLow= cmds.xform("mainEyelidLow_crv", q=1, bb=1, ws=1) 
            self.midPiv= (self.midUp[0]+self.midUp[3]+self.midLow[0]+self.midLow[3])/4*mul, (self.midUp[1]+self.midUp[4]+self.midLow[1]+self.midLow[4])/4, (self.midUp[2]+self.midUp[5]+self.midLow[2]+self.midLow[5])/4
        self.ebBB= cmds.xform("eyeballSrfBall_plc", q=1, bb=1, ws=1)
        ebPiv= cmds.xform("eyeball_plc", q=1, t=1, ws=1)
        pupPiv= cmds.xform("midPupil_plc", q=1, t=1, ws=1)        
        self.eyeballPiv= (ebPiv[0]*mul, ebPiv[1], ebPiv[2])
        self.pupilPiv= (pupPiv[0]*mul, pupPiv[1], pupPiv[2])
        self.pupilDis= math.sqrt((pupPiv[0]*mul-ebPiv[0]*mul)**2 + (pupPiv[1]-ebPiv[1])**2 + (pupPiv[2]-ebPiv[2])**2)
        #Future might use a fit skeleton to estimate ctrl size instead?     
        self.ctrlSize1= (self.ebBB[4]-self.ebBB[1])/6
        self.ctrlSize2= (self.eyeballPiv[0]*mul)/2

    def preTest1(self, meth):
        #Skip InOut Corner
        mis= []
        if meth==1:
            plc1= ["eyeball_plc","midPupil_plc","outEndEyelid_plc","outMainEyelid_plc","mainEyelid_plc","inMainEyelid_plc","inEndEyelid_plc"]
            plc2= ["Eyeball","Middle Pupil","Outer End Eyelid","Outer Main Eyelid","Main Eyelid","Inner Main Eyelid","Inner End Eyelid"]
        elif meth==2:
            plc1= ["eyeball_plc","midPupil_plc"]
            plc2= ["Eyeball","Middle Pupil"]
        for name1,name2 in zip(plc1,plc2):
            if cmds.objExists(name1)==0:
                mis.append(name2)
        if mis:
            cmds.warning("Some placer are not found! (%s)"%(", ").join(mis))
        return mis

    def preTest2(self):
        mis1, mis2, finalTest= [],[],[]
        if cmds.objExists("eyelid_rigTemp"):
            test1, test2= 1,1
            crvTemp= ["eyelid_15_L_crvTemp","eyelid_10_L_crvTemp","eyelid_00_L_crvTemp","eyelid_N10_L_crvTemp","eyelid_N15_L_crvTemp","eyelid_adj1ATemp","eyelid_adj1BTemp"]
            for item in crvTemp:
                if cmds.objExists(item):
                    try:
                        cmds.select(item)  
                    except:
                        test2= []
                        mis2.append(item)
                else:
                    test1= []
                    mis1.append(item)
            if test1:
                if test2:
                    finalTest= 1
                else:
                    cmds.warning("There are SAME NAME object (%s)"%(", ").join(mis2)) 
            else:
                cmds.warning("There are MISSING object (%s)"%(", ").join(mis1)) 
        else:
            cmds.warning("Please run step 1 first!")
        return finalTest

    def existStep(self, num, meth):
        if meth==1:
            conti= 1
            if cmds.objExists("eye_step%s"%num):
                conti= []
                cmds.warning("Step%s has been DONE before"%num)
            return conti
        elif meth==2:
            if cmds.objExists("Eye_Placer_GRP"):
                loc= cmds.spaceLocator(n="eye_step%s"%num)
                cmds.parent(loc, "eyeMisc_plc_grp")

    def hideObjHis(self, obj):
        allHist= []
        count= 0
        hist= mel.eval('historyPopupFill( "%s", 0, 0 )'%obj) + mel.eval('historyPopupFill( "%s", 1, 0 )'%obj)
        for subHist in hist.split(" "):
            if subHist!="":
                if subHist not in allHist:
                    allHist.append(subHist)  
        #This is to remove the first empty " "    
        if hist[0]==" ":
            ans= hist[1:]
        else:
            ans= hist[0]      
        if cmds.attributeQuery("hiddenHistory", node=obj, ex=1)==0:
            cmds.addAttr(obj, ln="hiddenHistory", dt="string")
            cmds.setAttr("%s.hiddenHistory"%obj, ans, typ="string")
        else:
            preHist= cmds.getAttr("%s.hiddenHistory"%obj)
            if preHist:
                cmds.setAttr("%s.hiddenHistory"%obj, "%s %s"%(preHist,ans), typ="string")
        for allSubHist in allHist:
            cmds.setAttr("%s.ihi"%allSubHist, 0)

    def final1(self):
        conti= self.existStep("1", 1)
        if conti:
            mis= self.preTest1(1)
            if mis==[]:
                self.uiStuffClass.loadingBar(1, 1)
                cmds.setAttr("Eye_Placer_GRP.v", 0)
                self.cal(1)
                self.adjustBsCrv1()
                self.existStep("1", 2)
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)

    def final2(self):
        conti= self.existStep("2", 1)
        if conti:
            test1= self.preTest2()
            if test1:
                self.uiStuffClass.loadingBar(1, 1)
                self.adjustBsCrv2()
                self.existStep("2", 2)
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)

    def final3(self):
        finalTest= []
        conti= self.existStep("3", 1)
        if conti:
            if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
                test1= self.preTest2()
                if test1:
                    finalTest= 1
            else:
                test1= self.preTest1(2)
                if test1==[]:
                    finalTest= 1
            if finalTest:
                self.uiStuffClass.loadingBar(1, 6*2+2)
                self.set1,eyeLidCtrlMGL,eyelidRigL,eyeLidCtrlMGR,eyelidRigR= [],[],[],[],[]
                if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
                    self.set1= cmds.sets(em=1, n="eyelidJnt_sets")
                self.set2= cmds.sets(em=1, n="eyeJnt_sets")
                cmds.sets(self.set1, self.set2, n="eye_sets")
                self.uiStuffClass.loadingBar(2)
                
                #L side
                self.cal(1)   
                if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
                    eyeLidCtrlMGL, eyelidRigL= self.preSetup("L")
                    self.createBsCrv("L", 1)
                    self.createLoc2("L", 1)
                    self.createTwkJntCtrl("L", 14, 1)
                    self.skinning()
                    self.createBliCtrl("L", 14, 1)
                eyeAimCtrlFollowL, eyeRigL, eyeAimSideLocL, eyeAimCtrlOffL= self.eyeAimSetup("L", 14, 1)
                piv1= (self.eyeballPiv[0], self.eyeballPiv[1], self.eyeballPiv[2]+self.pupilDis*25)

                #Opposite side
                self.cal(-1)
                if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
                    eyeLidCtrlMGR, eyelidRigR= self.preSetup("R")
                    self.createBsCrv("R", 2)
                    self.createLoc2("R", -1)
                    self.createTwkJntCtrl("R", 13, -1)
                    self.skinning()
                    self.createBliCtrl("R", 13, -1)
                eyeAimCtrlFollowR, eyeRigR, eyeAimSideLocR, eyeAimCtrlOffR= self.eyeAimSetup("R", 13, -1)
                piv2= (self.eyeballPiv[0], self.eyeballPiv[1], self.eyeballPiv[2]+self.pupilDis*25)

                #Setup Extra main aim
                eyeAimMainCtrl= cmds.curve(d=3, n="eyeAimMain_CTRL", p=[(0,0.95,0),(2.99,2.98,0),(5.38,2.6,0),(6.71,0.93,0),(6.71,-0.93,0),(5.38,-2.6,0),(2.99,-2.98,0),(0,-0.95,0),(-2.99,-2.98,0),(-5.38,-2.6,0),(-6.71,-0.93,0),(-6.71,0.93,0),(-5.38,2.6,0),(-2.99,2.98,0)])
                cmds.closeCurve(eyeAimMainCtrl, ps=0, rpo=1)
                self.ctrlShp(eyeAimMainCtrl, 17)
                cmds.xform(eyeAimMainCtrl, s=(self.ctrlSize2*1.1, self.ctrlSize2*1.1, self.ctrlSize2*1.1))
                cmds.refresh()
                cmds.makeIdentity(eyeAimMainCtrl, a=1, s=1, n=0, pn=1)
                eyeAimMainCtrlOff= cmds.group(em=1, n="%s_offset"%eyeAimMainCtrl)
                eyeAimMainCtrlDir= cmds.group(em=1, n="%s_dirGrp"%eyeAimMainCtrl)
                eyeAimMainCtrlMG= cmds.group(em=1, n="%s_mainGrp"%eyeAimMainCtrl)
                self.multiGrp(eyeAimMainCtrl,eyeAimMainCtrlOff,eyeAimMainCtrlDir, eyeAimMainCtrlMG)
                cmds.xform(eyeAimMainCtrlDir, t=((piv1[0]+piv2[0])/2, (piv1[1]+piv2[1])/2, (piv1[2]+piv2[2])/2))
                eyeAimMainLocL= cmds.spaceLocator(n="eyeAimMain_L_loc")
                eyeAimMainLocR= cmds.spaceLocator(n="eyeAimMain_R_loc")
                self.lockAttr(eyeAimMainCtrl, ["v"])
                #Connect L&R Aim
                for stuff, tar, piv in zip([eyeAimMainLocL,eyeAimMainLocR], [eyeAimCtrlFollowL,eyeAimCtrlFollowR], [piv1,piv2]):
                    cmds.xform(stuff, t=piv)
                    cmds.setAttr("%s.v"%stuff[0], 0)
                    mm= cmds.createNode("multMatrix", n="%s_mm"%stuff[0])
                    dcm1= cmds.createNode("decomposeMatrix", n="%s_dcm1"%stuff[0])
                    dcm2= cmds.createNode("decomposeMatrix", n="%s_dcm2"%stuff[0])
                    cmds.connectAttr("%s.worldMatrix"%stuff[0], "%s.matrixIn[0]"%mm)
                    cmds.connectAttr("%s.worldInverseMatrix"%eyeAimMainCtrlMG, "%s.matrixIn[1]"%mm)
                    cmds.connectAttr("%s.parentInverseMatrix"%tar, "%s.inputMatrix"%dcm1)
                    cmds.disconnectAttr("%s.parentInverseMatrix"%tar, "%s.inputMatrix"%dcm1)
                    cmds.connectAttr("%s.inputMatrix"%dcm1, "%s.matrixIn[2]"%mm)
                    cmds.connectAttr("%s.matrixSum"%mm, "%s.inputMatrix"%dcm2)
                    for attr, capAttr in zip(["x","y","z"], ["X","Y","Z"]):
                        cmds.connectAttr("%s.outputTranslate%s"%(dcm2,capAttr), "%s.t%s"%(tar,attr))
                        cmds.connectAttr("%s.outputRotate%s"%(dcm2,capAttr), "%s.r%s"%(tar,attr))
                cmds.parent(eyeAimMainLocL, eyeAimMainLocR, eyeAimMainCtrl)  
                    
                #EyeAimMain attr
                cmds.addAttr(eyeAimMainCtrl, ln="extra", at="enum")
                cmds.addAttr(eyeAimMainCtrl, ln="global", at="float", min=0, max=1)
                cmds.setAttr("%s.extra"%eyeAimMainCtrl, k=1, l=1)  
                cmds.setAttr("%s.global"%eyeAimMainCtrl, k=1) 
                glb= cmds.group(em=1, n="global_grp")
                glbLoc= cmds.spaceLocator(n="%s"%eyeAimMainCtrl.replace("CTRL","globalLoc"))
                headLoc= cmds.spaceLocator(n="%s"%eyeAimMainCtrl.replace("CTRL","headLoc"))
                cmds.parent(glbLoc, glb)
                parC= cmds.parentConstraint(glbLoc, headLoc, eyeAimMainCtrlDir, mo=1)
                cmds.connectAttr("%s.global"%eyeAimMainCtrl, "%s.%sW0"%(parC[0],glbLoc[0]))
                rev= cmds.createNode("reverse", n="%s_rev"%eyeAimMainCtrl)
                cmds.connectAttr("%s.global"%eyeAimMainCtrl, "%s.inputX"%rev)
                cmds.connectAttr( "%s.outputX"%rev, "%s.%sW1"%(parC[0],headLoc[0]))
                cmds.setAttr("%s.v"%glbLoc[0], 0)
                cmds.setAttr("%s.v"%headLoc[0], 0)
                #Slanted Attr
                if eyeAimSideLocL and eyeAimSideLocR:
                    cmds.addAttr(eyeAimMainCtrl, ln="slanted", at="float", min=0, max=1)
                    cmds.setAttr("%s.slanted"%eyeAimMainCtrl, k=1) 
                    for x,item in enumerate(zip([eyeAimSideLocL[0],eyeAimSideLocR[0]], [eyeAimCtrlOffL,eyeAimCtrlOffR])):
                        mm= cmds.createNode("multMatrix", n="%s_mm"%item[0])
                        dcm1= cmds.createNode("decomposeMatrix", n="%s_pim_dcm"%item[1])
                        dcm2= cmds.createNode("decomposeMatrix", n="%s_dcm"%item[0])
                        pim= cmds.getAttr("%s.parentInverseMatrix"%item[1])
                        cmds.connectAttr("%s.worldMatrix"%item[0], "%s.matrixIn[0]"%mm)
                        cmds.setAttr("%s.inputMatrix"%dcm1, pim, typ="matrix")
                        cmds.connectAttr("%s.inputMatrix"%dcm1, "%s.matrixIn[1]"%mm)
                        cmds.connectAttr("%s.matrixSum"%mm, "%s.inputMatrix"%dcm2)
                        pb= cmds.createNode("pairBlend", n="%s_pb"%item[0])
                        cmds.connectAttr("%s.outputTranslate"%dcm2, "%s.inTranslate2"%pb)
                        cmds.connectAttr("%s.slanted"%eyeAimMainCtrl, "%s.weight"%pb)
                        cmds.connectAttr("%s.outTranslate"%pb, "%s.t"%item[1])

                #External rearrange group for full facial rig (To know which to group to head)
                headGrp= cmds.group(em=1, n="eye_head_grp")
                worldGrp= cmds.group(em=1, n="eye_world_grp")
                cmds.parent(eyeAimMainCtrlMG,eyeLidCtrlMGL,eyeLidCtrlMGR,eyeRigL,eyeRigR,headLoc, headGrp)
                cmds.parent(eyelidRigL,eyelidRigR,glb, worldGrp)
                self.hideObjHis(eyeAimMainCtrl)
                if cmds.objExists("eyelid_rigTemp"):
                    cmds.delete("eyelid_rigTemp")
                cmds.setAttr("Eye_Placer_GRP.v", 0)
                self.existStep("3", 2)
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=[])

    def adjustBsCrv1(self):
        #Rebuild the curve so that beginning and end will have extra cvs to retain the custom shape (tear duct)
        for item, posNeg in zip(["mainEyelidUp_crv","mainEyelidLow_crv"],["10", "N10"]):
            crv= cmds.rebuildCurve(item, rt=0, end=1, kr=2, s=6, d=3, rpo=0, n="eyelid_%s_L_crvTemp"%posNeg)    
            crvTemp= cmds.rebuildCurve(item, rt=0, end=1, kr=2, s=14, d=3, rpo=0)
            #Rearrange cvs so that it kinda matches the shape
            for x in range(9):
                if x<3:
                    piv= cmds.xform("%s.cv[%s]"%(crvTemp[0], x), q=1, t=1, ws=1)
                elif x>5:
                    piv= cmds.xform("%s.cv[%s]"%(crvTemp[0], x+8), q=1, t=1, ws=1)
                else:
                    pivTemp= cmds.xform("%s.cv[%s]"%(crvTemp[0], 4*x-8), q=1, t=1, ws=1)
                    #Because deg3 curve will be offset, so need to scale up to match the shape
                    if x==4:
                        piv= (pivTemp[0]+(pivTemp[0]-self.midPiv[0])*0.15, pivTemp[1]+(pivTemp[1]-self.midPiv[1])*0.15, pivTemp[2]+(pivTemp[2]-self.midPiv[2])*0.15)
                    else:
                        piv= (pivTemp[0]+(pivTemp[0]-self.midPiv[0])*0.05, pivTemp[1]+(pivTemp[1]-self.midPiv[1])*0.05, pivTemp[2]+(pivTemp[2]-self.midPiv[2])*0.05)
                cmds.xform("%s.cv[%s]"%(crv[0], x), t=(piv[0], piv[1], piv[2]), ws=1)
            cmds.toggle(crv, cv=1)    
            if item=="mainEyelidUp_crv":
                crvPos10Temp= crv
            else:
                crvNeg10Temp= crv
            cmds.delete(crvTemp)

        #Creating Bs Temp  
        crv00Pre= cmds.duplicate(crvNeg10Temp)
        bsMidNameTemp= cmds.blendShape(crvPos10Temp, crv00Pre)
        cmds.setAttr("%s.%s"%(bsMidNameTemp[0], crvPos10Temp[0]), 0.5)
        crv00Temp= cmds.duplicate(crv00Pre, n="eyelid_00_L_crvTemp")
        cmds.delete(crv00Pre, "eyelid_00_L_crvTempShapeOrig")
        crvPos15Temp= cmds.duplicate(crv00Temp[0], n="eyelid_15_L_crvTemp")
        bsUpTemp= cmds.blendShape(crvPos10Temp, crvPos15Temp)
        cmds.setAttr("%s.%s"%(bsUpTemp[0], crvPos10Temp[0]), 1.5)
        crvNeg15Temp= cmds.duplicate(crv00Temp[0], n="eyelid_N15_L_crvTemp")
        bsLowTemp= cmds.blendShape(crvNeg10Temp, crvNeg15Temp)
        cmds.setAttr("%s.%s"%(bsLowTemp[0], crvNeg10Temp[0]), 1.5)

        #Create Adjust Power Ctrl
        adjGrpPar= cmds.group(em=1, n="eyelid_adjTemp_grp")
        finalTar=[]
        for x, txt in enumerate([("ADJUST", "FULL OPEN"), ("TWEAK CVS", "TO MATCH EYELID")]):
            adjGrp= cmds.group(em=1, n="eyelid_adj%sTemp_grp"%(x+1))
            crv0= cmds.curve(d=1, n="eyelid_adj%sTemp"%(x+1), p=[(0.05,0.30,0),(-0.35,0,0),(0.05,-0.30,0),(0.05,-0.12,0),(0.35,-0.12,0),(0.35,0.12,0),(0.05,0.12,0),(0.05,0.30,0)])
            crv1= cmds.textCurves(f="Arial|wt75|sz27.8|w700|st10", ch=0, t="%s"%txt[0]) 
            crv2= cmds.textCurves(f="Arial|wt75|sz27.8|w700|st10", ch=0, t="%s"%txt[1]) 
            self.multiGrp(crv0, adjGrp, adjGrpPar)
            cmds.xform(crv1[0], t=(1.5, 0.4, 0), s=(0.15, 0.15, 0.15))
            cmds.xform(crv2[0], t=(1.5, -0.4, 0), s=(0.15, 0.15, 0.15))
            cmds.makeIdentity(crv1[0],crv2[0],  a=1, t=1, r=1, s=1, n=0, pn=1)  
            for stuff in cmds.listRelatives(crv0,crv1,crv2, ad=1, typ="nurbsCurve"):
                cmds.setAttr("%s.ihi"%stuff, 0)
                cmds.setAttr("%s.overrideEnabled"%stuff, 1)
                cmds.setAttr("%s.overrideColor"%stuff, 17)
            self.lockAttr(crv0, ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"])

            #This is to create extra 1A, 1B adjust ctrl    
            if x==0:    
                for alpha,bs,bsAttr,mul in zip(["A","B"],[bsUpTemp,bsLowTemp], [crvPos10Temp,crvNeg10Temp], [1,-1]):
                    dup= cmds.duplicate(crv0, n="%s"%crv0.replace("1","1%s"%alpha))
                    dupPar= cmds.group(dup, n="%s"%adjGrp.replace("1","1%s"%alpha))
                    cmds.setAttr("%s.ty"%dup[0], k=1, l=0) 
                    cmds.xform(dup, t=(0,1.5,0), r=1)
                    cmds.transformLimits(dup, ty=(1.01,1.01), ety=(1,0))
                    cmds.xform(dupPar, t=(0,-0.6*mul,0), s=(1,1*mul,1))
                    cmds.rotate(0,0,-90, "%s.cv[*]"%dup[0])
                    cmds.connectAttr("%s.ty"%dup[0], "%s.%s"%(bs[0],bsAttr[0]))
                    finalTar.append(dup[0])
                cmds.delete(cmds.listRelatives(crv0, ad=1, pa=1, typ="nurbsCurve"))
            else:
                cmds.setAttr("%s.v"%adjGrp, 0)

            for stuff in cmds.listRelatives(crv1,crv2, ad=1, typ="nurbsCurve"):
                cmds.parent(stuff, crv0, r=1, s=1)
            cmds.delete(crv1[0], crv2[0])

        #Cleanup
        eyelidRigTemp= cmds.group(em=1, n="eyelid_rigTemp")
        bsCrvTemp= cmds.group(em=1, n="eyelid_bsCrvTemp")
        cmds.xform(adjGrpPar, s=(4*self.ctrlSize1,4*self.ctrlSize1,4*self.ctrlSize1))
        cmds.xform(adjGrpPar, t=(self.cv2Piv[0]+(self.cv2Piv[0]-self.cv1Piv[0]), self.cv2Piv[1], self.cv2Piv[2]), ws=1)
        cmds.parent(crvPos15Temp, crvPos10Temp, crv00Temp, crvNeg10Temp, crvNeg15Temp, bsCrvTemp)
        cmds.parent(bsCrvTemp, adjGrpPar, eyelidRigTemp)
        cmds.select(finalTar)

    def adjustBsCrv2(self):
        for posNeg,val in zip(["15","N15"], [0,1]):
            cmds.rename("eyelid_%s_L_crvTemp"%posNeg, "eyelid_%s_L_crvTwkTemp"%posNeg)
            cmds.duplicate("eyelid_%s_L_crvTwkTemp"%posNeg, n="eyelid_%s_L_crvTemp"%posNeg)
            cmds.delete("eyelid_%s_L_crvTwkTemp"%posNeg, "eyelid_%s_L_crvTwkTempShapeOrig"%posNeg, "eyelid_%s_L_crvTempShapeOrig"%posNeg)
            cmds.setAttr("eyelid_adj%sTemp_grp.v"%(val+1), val)
        cmds.reorder("eyelid_15_L_crvTemp", f=1)
        cmds.select("eyelid_15_L_crvTemp", "eyelid_10_L_crvTemp","eyelid_N10_L_crvTemp","eyelid_N15_L_crvTemp","eyelid_00_L_crvTemp")

    def preSetup(self, sides):
        eyelidRig= cmds.group(em=1, n="eyelid_%s_rig"%sides)
        self.crvMG= cmds.group(em=1, n="eyelid_%s_crv_mainGrp"%sides)
        self.bsCrvMG= cmds.group(em=1, n="eyelid_%s_bsCrv_mainGrp"%sides)    
        self.bliCrvMG= cmds.group(em=1, n="eyelid_%s_blinkCrv_mainGrp"%sides)
        self.twkCrvMG= cmds.group(em=1, n="eyelid_%s_twkCrv_mainGrp"%sides)
        #Loc
        self.locMG= cmds.group(em=1, n="eyelid_%s_loc_mainGrp"%sides)
        #Jnt
        jntMG= cmds.group(em=1, n="eyelid_%s_jnt_mainGrp"%sides)
        self.aimJntMG= cmds.group(em=1, n="eyelidAim_%s_jnt_mainGrp"%sides)
        self.twkJntMG= cmds.group(em=1, n="eyelidTweak_%s_jnt_mainGrp"%sides)
        #Ctrl
        ctrlMG= cmds.group(em=1, n="eyelid_%s_CTRL_mainGrp"%sides)
        self.bliCtrlMG= cmds.group(em=1, n="eyelidBlink_%s_CTRL_mainGrp"%sides)
        self.twkCtrlMG =cmds.group(em=1, n="eyelidTweak_%s_CTRL_grp"%sides)
        cmds.parent(self.bsCrvMG, self.bliCrvMG, self.twkCrvMG, self.crvMG)
        cmds.parent(self.aimJntMG, self.twkJntMG, jntMG)
        cmds.parent(self.bliCtrlMG, self.twkCtrlMG, ctrlMG)
        cmds.parent(self.crvMG, self.locMG, jntMG, ctrlMG, eyelidRig)
        self.tyPos= cmds.getAttr("eyelid_adj1ATemp.ty")
        self.tyNeg= cmds.getAttr("eyelid_adj1BTemp.ty")
        self.tyBoth= self.tyPos+self.tyNeg
        for vis in [self.crvMG, self.locMG]:
            cmds.setAttr("%s.v"%vis, 0)
        return ctrlMG, eyelidRig

    def createBsCrv(self, sides, meth):
        #Creating crv from ori crv
        self.crvPos15= cmds.duplicate("eyelid_15_L_crvTemp", n="eyelid_15_%s_crv"%sides)
        self.crvPos10= cmds.duplicate("eyelid_10_L_crvTemp", n="eyelid_10_%s_crv"%sides)
        self.crv00= cmds.duplicate("eyelid_00_L_crvTemp", n="eyelid_00_%s_crv"%sides)
        self.crvNeg10= cmds.duplicate("eyelid_N10_L_crvTemp", n="eyelid_N10_%s_crv"%sides)
        self.crvNeg15= cmds.duplicate("eyelid_N15_L_crvTemp", n="eyelid_N15_%s_crv"%sides)
        if meth==1:
            cmds.parent(self.crvPos15,self.crvPos10,self.crv00,self.crvNeg10,self.crvNeg15, self.bsCrvMG)
        elif meth==2:
            tempGrp= cmds.group(em=1)
            cmds.parent(self.crvPos15,self.crvPos10,self.crv00,self.crvNeg10,self.crvNeg15, tempGrp)
            cmds.setAttr("%s.sx"%tempGrp, -1)
            cmds.makeIdentity(tempGrp, a=1, s=1, n=0, pn=1)
            cmds.parent(self.crvPos15,self.crvPos10,self.crv00,self.crvNeg10,self.crvNeg15, self.bsCrvMG)
            cmds.delete(tempGrp)

        #Creating blendshapes
        self.bliCrv, self.twkCrv= [],[]
        for upDown, x in zip(["up","low"], [round(self.tyBoth+1,2),round(self.tyBoth-1,2)]):
            crv1= cmds.duplicate(self.crv00, n="%sEyelid_%s_blinkCrv"%(upDown, sides))
            crv2= cmds.duplicate(crv1, n="%sEyelid_%s_twkCrv"%(upDown, sides))
            bsName= cmds.blendShape(self.crvPos10, crv1, w=(0, x), n="%sEyelid_%s_blink_bs"%(upDown, sides))
            #Because need to be able to change crv00 shape and it cannot be at value 0
            cmds.blendShape(bsName, e=1, ib=1, t=["%s"%crv1[0], 0, "%s"%self.crvPos15[0], round(self.tyBoth+self.tyPos,2)])
            cmds.blendShape(bsName, e=1, ib=1, t=["%s"%crv1[0], 0, "%s"%self.crvPos10[0], round(self.tyBoth+1,2)])
            cmds.blendShape(bsName, e=1, ib=1, t=["%s"%crv1[0], 0, "%s"%self.crv00[0], round(self.tyBoth,2)])
            cmds.blendShape(bsName, e=1, ib=1, t=["%s"%crv1[0], 0, "%s"%self.crvNeg10[0], round(self.tyBoth-1,2)])
            cmds.blendShape(bsName, e=1, ib=1, t=["%s"%crv1[0], 0, "%s"%self.crvNeg15[0], round(self.tyBoth-self.tyNeg,2)])
            cmds.blendShape(crv1, crv2, w=(0, 1), n="%sEyelid_%s_blinkToTweak_bs"%(upDown, sides))
            if upDown=="up":
                self.bsName1= bsName
            else:
                self.bsName2= bsName
            self.bliCrv.append(crv1[0])    
            self.twkCrv.append(crv2[0]) 
        cmds.parent(self.bliCrv, self.bliCrvMG)  
        cmds.parent(self.twkCrv, self.twkCrvMG) 
        self.uiStuffClass.loadingBar(2)

    def createLoc2(self, sides, mul):    
        ciTemp= cmds.createNode("curveInfo")
        cmds.connectAttr("%s.worldSpace"%self.crv00[0], "%s.inputCurve"%ciTemp)
        crvLength= cmds.getAttr("%s.arcLength"%ciTemp)
        cmds.delete(ciTemp)
        locScale= crvLength/(self.spans+1)/2          
        self.upLoc= cmds.spaceLocator(n="eyelid_%s_upLoc"%sides)
        cmds.xform(self.upLoc, t=(self.eyeballPiv[0], self.eyeballPiv[1]+self.ebBB[4]-self.ebBB[1], self.eyeballPiv[2]), ws=1)  
        cmds.parent(self.upLoc, self.locMG)
        self.upAimTipNode, self.lowAimTipNode= [],[]
        for twkCrv, revTwkCrv, bsCrv, revBsCrv, upDown, bs, tyPosNeg in zip(self.twkCrv, [self.twkCrv[1], self.twkCrv[0]], ["mainEyelidUp_crv","mainEyelidLow_crv"], ["mainEyelidLow_crv","mainEyelidUp_crv"],["up","low"],[self.bsName1,self.bsName2],[(self.tyPos,1,-self.tyNeg), (-self.tyNeg,-1,-self.tyPos)]):       
            for x in range(self.spans+1):
                if upDown=="low":
                    if x==0 or x==self.spans:
                        continue
                #Create aimLoc
                if x==0:
                    aimLoc= cmds.spaceLocator(n="inEyelid_%s_aimLoc"%sides)
                elif x==self.spans:
                    aimLoc= cmds.spaceLocator(n="outEyelid_%s_aimLoc"%sides)
                else:
                    aimLoc= cmds.spaceLocator(n="%sEyelid_%s_%s_aimLoc"%(upDown, sides, x))
                cmds.setAttr("%s.s"%aimLoc[0], locScale, locScale, locScale)
                aimLocDir= cmds.group(em=1, n="%s_dirGrp"%aimLoc[0])
                cvPiv1= cmds.xform("%s.cv[%s]"%(bsCrv, x), q=1, t=1, ws=1)
                cmds.xform(aimLoc, t=(cvPiv1[0]*mul, cvPiv1[1], cvPiv1[2]), ws=1)
                param1= self.getParam((cvPiv1[0]*mul, cvPiv1[1], cvPiv1[2]), twkCrv)
                shp1= cmds.listRelatives(twkCrv, typ="nurbsCurve")
                poci1= cmds.createNode("pointOnCurveInfo", n="%s_poci"%aimLocDir)
                cmds.connectAttr("%s.worldSpace[0]"%shp1[0], "%s.inputCurve"%poci1)
                cmds.setAttr("%s.parameter"%poci1, param1)
                cmds.connectAttr("%s.position"%poci1,"%s.translate"%aimLocDir)
                pos1= cmds.getAttr("%s.position"%poci1)[0]
                piv1= (cvPiv1[0]*mul-pos1[0], cvPiv1[1]-pos1[1], cvPiv1[2]-pos1[2])

                #Temp get opposite aimLoc
                cvPiv2= cmds.xform("%s.cv[%s]"%(revBsCrv, x), q=1, t=1, ws=1)
                param2= self.getParam((cvPiv2[0]*mul, cvPiv2[1], cvPiv2[2]), revTwkCrv)
                shp2= cmds.listRelatives(revTwkCrv, typ="nurbsCurve")
                poci2= cmds.createNode("pointOnCurveInfo")
                cmds.connectAttr("%s.worldSpace[0]"%shp2[0], "%s.inputCurve"%poci2)
                cmds.setAttr("%s.parameter"%poci2, param2)
                pos2= cmds.getAttr("%s.position"%poci2)[0]
                piv2= (cvPiv2[0]*mul-pos2[0], cvPiv2[1]-pos2[1], cvPiv2[2]-pos2[2])
                cmds.delete(poci2)

                self.multiGrp(aimLoc,aimLocDir, self.locMG)
                locOff= cmds.duplicate(aimLoc, n="%sOffset"%aimLoc[0])  

                #Create Joint
                baseJnt= cmds.createNode("joint", n="%s_jnx"%aimLoc[0].replace("Loc","Base"))
                tipJnt= cmds.createNode("joint", n="%s_jnt"%aimLoc[0].replace("Loc","Tip"))
                cmds.xform(baseJnt, t=(self.eyeballPiv[0], self.eyeballPiv[1], self.eyeballPiv[2]))
                self.multiGrp(tipJnt,baseJnt, self.aimJntMG)
                cmds.xform(tipJnt, t=(cvPiv1[0]*mul, cvPiv1[1], cvPiv1[2]), ws=1)
                cmds.joint(baseJnt, e=1, oj="xyz", sao="yup")
                cmds.setAttr("%s.jointOrient"%tipJnt, 0,0,0)
                cmds.aimConstraint(aimLoc[0], baseJnt, mo=0, aim=(1,0,0), u=(0,1,0), wut="object", wuo=self.upLoc[0])
                
                #Remap1 to match lowResCurve loc to hiResCurve
                rmp1= cmds.createNode("remapValue", n="%s_rmp1"%aimLoc[0])
                cmds.setAttr("%s.inputValue"%rmp1, 1)
                cmds.setAttr("%s.color[0].color_Position"%rmp1, -1)
                cmds.setAttr("%s.color[1].color_ Position"%rmp1, 0)
                cmds.setAttr("%s.color[2].color_Position"%rmp1, 1)
                cmds.setAttr("%s.color[0].color_Color"%rmp1, *piv2)   
                cmds.setAttr("%s.color[1].color_Color"%rmp1, 0,0,0)    
                cmds.setAttr("%s.color[2].color_Color"%rmp1, *piv1)    
                for attr,rgb in zip(["x","y","z"], ["R","G","B"]):
                    cmds.connectAttr("%s.outColor%s"%(rmp1,rgb), "%s.t%s"%(aimLoc[0],attr))

                #Creating "Stretchy" eyelid tweaker?
                mm= cmds.createNode("multMatrix", n="%s_mm"%aimLoc[0])
                dcm= cmds.createNode("decomposeMatrix", n="%s_dcm"%aimLoc[0])
                cond1= cmds.createNode("condition", n="%s_cond1"%aimLoc[0])
                rmp2= cmds.createNode("remapValue", n="%s_rmp2"%aimLoc[0])
                pma= cmds.createNode("plusMinusAverage", n="%s_pma"%aimLoc[0])
                cmds.connectAttr("%s.worldMatrix"%aimLoc[0], "%s.matrixIn[0]"%mm)
                cmds.connectAttr("%s.parentInverseMatrix"%tipJnt, "%s.matrixIn[1]"%mm)
                cmds.connectAttr("%s.matrixSum"%mm, "%s.inputMatrix"%dcm)
                cmds.setAttr("%s.operation"%cond1, 2)
                cmds.connectAttr("%s.outputTranslateX"%dcm, "%s.input1D[0]"%pma)
                #So that blendshape will negate the tweakers's stretchy with or without "restriction" but md's value is added later
                cmds.setAttr("%s.value[0].value_Position"%rmp2, tyPosNeg[2])
                cmds.setAttr("%s.value[1].value_Position"%rmp2, -1)
                cmds.setAttr("%s.value[1].value_FloatValue"%rmp2, 0)  
                cmds.setAttr("%s.value[2].value_Position"%rmp2, 0)
                cmds.setAttr("%s.value[2].value_FloatValue"%rmp2, 0)                
                cmds.setAttr("%s.value[3].value_Position"%rmp2, 1)
                cmds.setAttr("%s.value[3].value_FloatValue"%rmp2, 0)
                cmds.setAttr("%s.value[4].value_Position"%rmp2, abs(tyPosNeg[0]))
                cmds.setAttr("%s.value[0].value_Interp"%rmp2, 1)
                cmds.setAttr("%s.value[1].value_Interp"%rmp2, 1)
                cmds.setAttr("%s.value[2].value_Interp"%rmp2, 1)
                cmds.setAttr("%s.value[3].value_Interp"%rmp2, 1)
                cmds.setAttr("%s.value[5].value_Interp"%rmp2, 1)
                cmds.setAttr("%s.operation"%pma, 2)
                cmds.connectAttr("%s.outValue"%rmp2, "%s.input1D[1]"%pma)
                cmds.connectAttr("%s.output1D"%pma, "%s.colorIfTrueR"%cond1)
                cmds.connectAttr("%s.output1D"%pma, "%s.firstTerm"%cond1)
                cmds.connectAttr("%s.outColorR"%cond1, "%s.tx"%tipJnt)
                cmds.sets(tipJnt, add="%s"%self.set1)
                if upDown=="up":
                    self.upAimTipNode.append((cond1,rmp1,rmp2))
                else:
                    self.lowAimTipNode.append((cond1,rmp1,rmp2))

                if x!=0 and x!=self.spans:
                    #Remap4 to match the blendshape deg3 curve 
                    rmp4= cmds.createNode("remapValue", n="%s_rmp4"%aimLoc[0])
                    cmds.setAttr("%s.value[0].value_Position"%rmp4, round(self.tyBoth-1,2))
                    cmds.setAttr("%s.value[1].value_Position"%rmp4, round(self.tyBoth+1,2))  
                    if upDown=="up":
                        cmds.setAttr("%s.value[1].value_FloatValue"%rmp4, param1)
                    else:
                        cmds.setAttr("%s.value[0].value_FloatValue"%rmp4.replace("low", "up"), param1)
                        paramPrev= cmds.getAttr("%s.value[1].value_FloatValue"%rmp4.replace("low", "up"))
                        cmds.setAttr("%s.value[1].value_FloatValue"%rmp4, paramPrev)
                        cmds.setAttr("%s.value[0].value_FloatValue"%rmp4, param1)
                    cmds.connectAttr("%s.%s"%(bs[0],self.crvPos10[0]), "%s.inputValue"%rmp4)
                    cmds.connectAttr("%s.outValue"%rmp4, "%s.parameter"%poci1)
        self.uiStuffClass.loadingBar(2)

    def createTwkJntCtrl(self, sides, color, mul):   
        #Find <follow> groups rotation
        aimTemp= cmds.group(em=1, n="aimTemp")
        followTemp= cmds.group(em=1, n="followTemp")
        cmds.xform(aimTemp, t=self.midPiv, ws=1)
        cmds.xform(followTemp, t=self.eyeballPiv, ws=1)
        acTemp= cmds.aimConstraint(aimTemp, followTemp, mo=0, aim=(0,0,1), u=(0,1,0), wut="object", wuo=self.upLoc[0])
        cmds.delete(acTemp, aimTemp)

        #Create Tweaker jnt
        self.inOutTwkJnt, self.upTwkJnt, self.lowTwkJnt= [],[],[]
        for bliCrv, upDown, bs, bsVal in zip(self.bliCrv, ["up","low"], [self.bsName1,self.bsName2], [round(self.tyBoth+1,2),round(self.tyBoth-1,2)]):
            for x in range(5):
                #So that followGrp is created when both bs is on 0 so that when close eyelid and move will be accurate
                cmds.setAttr("%s.%s"%(bs[0],self.crvPos10[0]), 0)
                if upDown=="low":
                    #Corner create once enough
                    if x==0 or x==4:
                        continue
                ans= (1.0/(4.0))*x
                y= int(x*1.5)
                if x==0:
                    twkJnt= cmds.createNode("joint", n="inEyelidTweak_%s_jnt"%sides)
                    self.inOutTwkJnt.append(twkJnt)
                elif x==4:
                    twkJnt= cmds.createNode("joint", n="outEyelidTweak_%s_jnt"%sides)
                    self.inOutTwkJnt.append(twkJnt)
                else:
                    y= x+1
                    twkJnt= cmds.createNode("joint", n="%sEyelidTweak%s_%s_jnt"%(upDown, x, sides))
                    if upDown=="up":
                        self.upTwkJnt.append(twkJnt)
                    else:
                        self.lowTwkJnt.append(twkJnt)
                twkJntDir1= cmds.group(em=1, n="%s_dirGrp1"%twkJnt)
                twkJntDir2= cmds.group(em=1, n="%s_dirGrp2"%twkJnt)
                twkJntOff= cmds.group(em=1, n="%s_offset"%twkJnt)
                folTran= cmds.duplicate(followTemp, n="%s"%twkJnt.replace("jnt", "followTran"))
                folRot= cmds.duplicate(followTemp, n="%s"%twkJnt.replace("jnt", "followRot"))
                folAim= cmds.duplicate(followTemp, n="%s"%twkJnt.replace("jnt", "followAim"))
                folGrp= cmds.duplicate(followTemp, n="%s_dirGrp"%twkJnt.replace("jnt", "follow"))
                bpm= cmds.group(em=1, n="%s"%twkJnt.replace("jnt", "bpm")) 
                cmds.parent(twkJnt, twkJntOff)
                cmds.parent(twkJntOff, twkJntDir1)
                cmds.parent(twkJntDir1, bpm, twkJntDir2)
                cmds.connectAttr("%s.editPoints[%s]"%(bliCrv,y), "%s.t"%twkJntDir2)
                self.multiGrp(twkJntDir1, folRot, folTran, folAim, folGrp, twkJntDir2, self.twkJntMG)
                cmds.xform(twkJntDir1, bpm, s=(1*mul,1,1), ws=1)

                #Create Tweaker Ctrl
                twkCtrl= cmds.curve(d=1, n="%s"%twkJnt.replace("jnt","CTRL"), p=[(0.0,0.0,-0.28),(0.04,0.0,-0.28),(0.09,0.0,-0.27),(0.13,0.0,-0.25),(0.17,0.0,-0.23),(0.2,0.0,-0.2),(0.23,0.0,-0.17),(0.25,0.0,-0.13),(0.27,0.0,-0.09),(0.28,0.0,-0.04),(0.28,0.0,0.0),(0.28,0.0,0.04),(0.27,0.0,0.09),(0.25,0.0,0.13),(0.23,0.0,0.17),(0.2,0.0,0.2),(0.17,0.0,0.23),(0.13,0.0,0.25),(0.09,0.0,0.27),(0.04,0.0,0.28),
                (0.0,0.0,0.28),(-0.04,0.0,0.28),(-0.09,0.0,0.27),(-0.13,0.0,0.25),(-0.17,0.0,0.23),(-0.2,0.0,0.2),(-0.23,0.0,0.17),(-0.25,0.0,0.13),(-0.27,0.0,0.09),(-0.28,0.0,0.04),(-0.28,0.0,0.0),(-0.28,0.0,-0.04),(-0.27,0.0,-0.09),(-0.25,0.0,-0.13),(-0.23,0.0,-0.17),(-0.2,0.0,-0.2),(-0.17,0.0,-0.23),(-0.13,0.0,-0.25),(-0.09,0.0,-0.27),(-0.04,0.0,-0.28),(0.0,0.0,-0.28),(0.0,0.04,-0.28),(0.0,0.09,-0.27),(0.0,0.13,-0.25),(0.0,0.17,-0.23),
                (0.0,0.2,-0.2),(0.0,0.23,-0.17),(0.0,0.25,-0.13),(0.0,0.27,-0.09),(0.0,0.28,-0.04),(0.0,0.28,0.0),(0.0,0.28,0.04),(0.0,0.27,0.09),(0.0,0.25,0.13),(0.0,0.23,0.17),(0.0,0.2,0.2),(0.0,0.17,0.23),(0.0,0.13,0.25),(0.0,0.09,0.27),(0.0,0.04,0.28),(0.0,0.0,0.28),(0.0,-0.04,0.28),(0.0,-0.09,0.27),(0.0,-0.13,0.25),(0.0,-0.17,0.23),
                (0.0,-0.2,0.2),(0.0,-0.23,0.17),(0.0,-0.25,0.13),(0.0,-0.27,0.09),(0.0,-0.28,0.04),(0.0,-0.28,0.0),(0.0,-0.28,-0.04),(0.0,-0.27,-0.09),(0.0,-0.25,-0.13),(0.0,-0.23,-0.17),(0.0,-0.2,-0.2),(0.0,-0.17,-0.23),(0.0,-0.13,-0.25),(0.0,-0.09,-0.27),(0.0,-0.04,-0.28),(0.0,0.0,-0.28),(0.0,0.04,-0.28),(0.0,0.09,-0.27),(0.0,0.13,-0.25),(0.0,0.17,-0.23),
                (0.0,0.2,-0.2),(0.0,0.23,-0.17),(0.0,0.25,-0.13),(0.0,0.27,-0.09),(0.0,0.28,-0.04),(0.0,0.28,0.0),(0.04,0.28,0.0),(0.09,0.27,0.0),(0.13,0.25,0.0),(0.17,0.23,0.0),(0.2,0.2,0.0),(0.23,0.17,0.0),(0.25,0.13,0.0),(0.27,0.09,0.0),(0.28,0.04,0.0),(0.28,0.0,0.0),(0.28,-0.04,0.0),(0.27,-0.09,0.0),(0.25,-0.13,0.0),(0.23,-0.17,0.0),
                (0.2,-0.2,0.0),(0.17,-0.23,0.0),(0.13,-0.25,0.0),(0.09,-0.27,0.0),(0.04,-0.28,0.0),(0.0,-0.28,0.0),(-0.04,-0.28,0.0),(-0.09,-0.27,0.0),(-0.13,-0.25,0.0),(-0.17,-0.23,0.0),(-0.2,-0.2,0.0),(-0.23,-0.17,0.0),(-0.25,-0.13,0.0),(-0.27,-0.09,0.0),(-0.28,-0.04,0.0),(-0.28,0.0,0.0),(-0.28,0.04,0.0),(-0.27,0.09,0.0),(-0.25,0.13,0.0),(-0.23,0.17,0.0),(-0.2,0.2,0.0),(-0.17,0.23,0.0),(-0.13,0.25,0.0),(-0.09,0.27,0.0),(-0.04,0.28,0.0),(0.0,0.28,0.0)])    
                self.ctrlShp(twkCtrl, color)
                twkCtrlDir= cmds.group(em=1, n="%s_dirGrp"%twkCtrl)
                twkCtrlNeg= cmds.group(em=1, n="%s_negGrp"%twkCtrl)
                twkCtrlOff= cmds.group(em=1, n="%s_offset"%twkCtrl)
                self.multiGrp(twkCtrl, twkCtrlOff, twkCtrlNeg, twkCtrlDir, self.twkCtrlMG)   
                #Here bs set back open state so that ctrl is at correct place 
                cmds.setAttr("%s.%s"%(bs[0],self.crvPos10[0]), bsVal)
                twkPiv= cmds.getAttr("%s.editPoints[%s]"%(bliCrv,y))
                cmds.setAttr("%s.t"%twkCtrlDir, *twkPiv[0])   
                cmds.xform(twkCtrlDir, s=(1*mul,1,1))           
                cmds.xform(twkCtrl, s=(self.ctrlSize1, self.ctrlSize1, self.ctrlSize1))
                cmds.makeIdentity(twkCtrl, a=1, s=1, n=0, pn=1)  
                md= cmds.createNode("multiplyDivide", n="%s_md"%twkCtrlNeg)
                for attr, capAttr in zip(("x","y","z"), ("X","Y","Z")):
                    cmds.connectAttr("%s.t%s"%(twkCtrl,attr), "%s.t%s"%(twkJnt,attr))
                    cmds.connectAttr("%s.t%s"%(twkCtrlOff,attr), "%s.t%s"%(twkJntOff,attr))
                    cmds.connectAttr("%s.r%s"%(twkCtrlOff,attr), "%s.r%s"%(twkJntOff,attr))
                    cmds.setAttr("%s.input2%s"%(md,capAttr), -1)
                    cmds.connectAttr("%s.t%s"%(twkCtrl,attr), "%s.input1%s"%(md,capAttr))
                    cmds.connectAttr("%s.output%s"%(md,capAttr), "%s.t%s"%(twkCtrlNeg,attr))
                self.lockAttr(twkCtrl, ["rx","ry","rz","sx","sy","sz","v"])
                self.hideObjHis(twkCtrl)
        cmds.delete(followTemp)
        self.uiStuffClass.loadingBar(2)

    def skinning(self):
        #Bind & bpm to tweak curve
        allUpperTwkJnt= (self.inOutTwkJnt+self.upTwkJnt)
        allLowerTwkJnt= (self.inOutTwkJnt+self.lowTwkJnt)
        for allJnt, crv in zip([allUpperTwkJnt, allLowerTwkJnt], self.twkCrv):      
            skinC= cmds.skinCluster(allJnt, crv, tsb=1, bm=0, sm=0, nw=1, wd=0, mi=3, dr=4) 
            for x, bpm in enumerate(allJnt):
                cmds.connectAttr("%s.worldInverseMatrix"%bpm.replace("jnt","bpm"), "%s.bindPreMatrix[%s]"%(skinC[0],x))
            
            #Hardcode the weights + weird arrangement 3,1,2, 5,8,6,7 because wanna get the longest (both ends) in the curve 
            for jnt, num in zip(self.inOutTwkJnt, [("3","1","2"),("5","8","6","7")]):
                for y in num :
                    pnt= cmds.xform("%s.cv[%s]"%(crv, y), q=1, t=1, ws=1)
                    param= self.getParam(pnt, crv)
                    arcLD= cmds.createNode("arcLengthDimension")
                    cmds.connectAttr("%s.worldSpace[0]"%crv, "%s.nurbsGeometry"%arcLD)
                    cmds.setAttr("%s.uParamValue"%arcLD, param)
                    if y=="3" or y=="5":
                        arcLTotal= cmds.getAttr("%s.arcLength"%arcLD)
                    elif y=="8":
                        arcLSpecial= cmds.getAttr("%s.arcLength"%arcLD)
                    else:    
                        arcL= cmds.getAttr("%s.arcLength"%arcLD)
                        if num==("3","1","2"):
                            ans= 1-(arcL/arcLTotal*0.8)
                        else:
                            ans= 1-((arcLSpecial-arcL)/(arcLSpecial-arcLTotal)*0.8)
                        cmds.skinPercent(skinC[0], "%s.cv[%s]"%(crv, y), tv=("%s"%jnt, ans))
                    cmds.delete(cmds.listRelatives(arcLD, ap=1))
        self.uiStuffClass.loadingBar(2)
                    
    def createBliCtrl(self, sides, color, mul):   
        #Create Blink Ctrl           
        bliCtrlDir= cmds.group(em=1, n="eyelidBlink_%s_CTRL_dirGrp"%sides)
        upBliCtrl= cmds.curve(d=3, n="upEyelidBlink_%s_CTRL"%sides, p=[(0.0,1.7,-0.0),(0.78,1.5,-0.0),(1.38,0.97,-0.0),(1.6,0.4,-0.0),(1.47,0.07,-0.0),(1.06,0.08,-0.0),(0.78,0.82,-0.0),(0.0,1.12,-0.0),(-0.78,0.82,-0.0),(-1.06,0.08,-0.0),(-1.47,0.07,-0.0),(-1.6,0.4,-0.0),(-1.38,0.97,-0.0),(-0.78,1.5,-0.0)])
        cmds.closeCurve(upBliCtrl, ps=0, rpo=1)
        self.ctrlShp(upBliCtrl, color)
        lowBliCtrl= cmds.duplicate(upBliCtrl, n="lowEyelidBlink_%s_CTRL"%sides)[0]
        for ctrl, val in zip([upBliCtrl,lowBliCtrl], [1,-1]):
            bliPar= cmds.group(em=1, n="%s_offset"%ctrl)
            self.multiGrp(ctrl, bliPar, bliCtrlDir)
            cmds.setAttr("%s.ty"%ctrl, 1)
            cmds.setAttr("%s.sy"%bliPar, val) 
        cmds.parent(bliCtrlDir, self.bliCtrlMG)   
        cmds.xform(bliCtrlDir, t=(self.eyeballPiv[0]*4+(self.ebBB[3]-self.ebBB[0])*mul, self.eyeballPiv[1], self.eyeballPiv[2]), s=(self.ctrlSize1*mul, self.ctrlSize1, self.ctrlSize1), ws=1)
        
        #Setting up Blink Ctrl connections
        for ctrl, bs, twkJnt, allNode in zip([upBliCtrl,lowBliCtrl], [self.bsName1,self.bsName2], [self.upTwkJnt,self.lowTwkJnt], [self.upAimTipNode,self.lowAimTipNode]):
            bliCtrlTxMd= cmds.createNode("multiplyDivide", n="%s_tx_md"%ctrl)
            bliCtrlTyMd= cmds.createNode("multiplyDivide", n="%s_ty_md"%ctrl)
            bliCtrlRzMd= cmds.createNode("multiplyDivide", n="%s_rz_md"%ctrl)
            pma1= cmds.createNode("plusMinusAverage", n="%s_pma"%ctrl)
            cmds.setAttr("%s.input1D[1]"%pma1, round(self.tyBoth,2))
            cmds.addAttr(ctrl, ln="rotation", at="float")
            cmds.setAttr("%s.rotation"%ctrl, k=1)      
            cmds.setAttr("%s.input2X"%bliCtrlTxMd, 30*mul*self.ctrlSize1)
            cmds.setAttr("%s.input2X"%bliCtrlRzMd, 10*mul)                    
            cmds.connectAttr("%s.tx"%ctrl, "%s.input1X"%bliCtrlTxMd)
            cmds.connectAttr("%s.rotation"%ctrl, "%s.input1X"%bliCtrlRzMd) 
            if ctrl==lowBliCtrl:
                cmds.setAttr("%s.input2X"%bliCtrlTyMd, -1)
                cmds.transformLimits(ctrl, ty=(-(round(self.tyPos,2)), round(self.tyNeg,2)), ety=(1,1))
            else:
                cmds.transformLimits(ctrl, ty=(-(round(self.tyNeg,2)), round(self.tyPos,2)), ety=(1,1))
            cmds.transformLimits(ctrl, tx=(-1,1), etx=(1,1))
            cmds.connectAttr("%s.ty"%ctrl, "%s.input1X"%bliCtrlTyMd)  
            cmds.connectAttr("%s.outputX"%bliCtrlTyMd, "%s.input1D[0]"%pma1)
            cmds.connectAttr("%s.output1D"%pma1, "%s.%s"%(bs[0],self.crvPos10[0]))
            self.lockAttr(ctrl, ["tz","rx","ry","rz","sx","sy","sz","v"])

            #Modifying blink Ctrl tx to control both side tweaker to move lesser so that it wont penetrate much
            piv0= cmds.xform(self.inOutTwkJnt[0].replace("jnt","followTran"), q=1, t=1, ws=1)
            piv1= cmds.xform(self.inOutTwkJnt[0], q=1, t=1, ws=1)
            piv2= cmds.xform(twkJnt[1], q=1, t=1, ws=1)
            piv3= cmds.xform(self.inOutTwkJnt[1], q=1, t=1, ws=1)
            angB1= cmds.createNode("angleBetween")
            angB2= cmds.createNode("angleBetween")
            #Angle Between uses vector so direction still important but weird is uses from mid point vector & output angle no direction
            cmds.setAttr("%s.vector1"%angB1, piv0[0]-piv1[0], piv0[1]-piv1[1], piv0[2]-piv1[2])
            cmds.setAttr("%s.vector2"%angB1, piv0[0]-piv3[0], piv0[1]-piv3[1], piv0[2]-piv3[2])
            cmds.setAttr("%s.vector1"%angB2, piv0[0]-piv1[0], piv0[1]-piv1[1], piv0[2]-piv1[2])
            cmds.setAttr("%s.vector2"%angB2, piv0[0]-piv2[0], piv0[1]-piv2[1], piv0[2]-piv2[2])
            angFull= cmds.getAttr("%s.angle"%angB1)     
            angHalf= cmds.getAttr("%s.angle"%angB2)  
            cmds.delete(angB1,angB2)
            for stuff in twkJnt:
                if stuff!= twkJnt[1]:
                    piv= cmds.xform(stuff, q=1, t=1, ws=1)
                    angB= cmds.createNode("angleBetween")
                    cond= cmds.createNode("condition", n="%s_cond"%stuff.replace("jnt","followTran"))
                    cmds.setAttr("%s.vector1"%angB, piv0[0]-piv[0], piv0[1]-piv[1], piv0[2]-piv[2])
                    cmds.setAttr("%s.vector2"%angB, piv0[0]-piv1[0], piv0[1]-piv1[1], piv0[2]-piv1[2])   
                    cmds.setAttr("%s.operation"%cond, 2)
                    cmds.connectAttr("%s.outputX"%bliCtrlTxMd, "%s.firstTerm"%cond)                 
                    ang= cmds.getAttr("%s.angle"%angB)   
                    sr1= cmds.createNode("setRange", n="%s_sr1"%stuff.replace("jnt","followTran"))
                    sr2= cmds.createNode("setRange", n="%s_sr2"%stuff.replace("jnt","followTran"))
                    #Use min max because both way are opposite which we need to reverse (basically both needa slow down)
                    cmds.setAttr("%s.oldMinY"%sr1, min(-angHalf,-ang))
                    cmds.setAttr("%s.minY"%sr1, max(-angHalf,-ang))
                    cmds.setAttr("%s.oldMaxY"%sr2, max(angFull-angHalf, angFull-ang))
                    cmds.setAttr("%s.maxY"%sr2, min(angFull-angHalf, angFull-ang))
                    cmds.connectAttr("%s.outputX"%bliCtrlTxMd, "%s.valueY"%sr1)
                    cmds.connectAttr("%s.outputX"%bliCtrlTxMd, "%s.valueY"%sr2)
                    cmds.connectAttr("%s.outValueY"%sr1, "%s.colorIfFalseR"%cond)
                    cmds.connectAttr("%s.outValueY"%sr2, "%s.colorIfTrueR"%cond)
                    cmds.connectAttr("%s.outColorR"%cond, "%s.ry"%stuff.replace("jnt","followTran"))
                    cmds.connectAttr("%s.outputX"%bliCtrlRzMd, "%s.rz"%stuff.replace("jnt","followRot"))
                    cmds.delete(angB)      
                else:
                    cmds.connectAttr("%s.outputX"%bliCtrlTxMd, "%s.ry"%stuff.replace("jnt","followTran"))
                    cmds.connectAttr("%s.outputX"%bliCtrlRzMd, "%s.rz"%stuff.replace("jnt","followRot"))
            for cond1, rmp1, rmp2 in allNode:
                cmds.connectAttr("%s.ty"%ctrl, "%s.inputValue"%rmp1)
                cmds.connectAttr("%s.ty"%ctrl, "%s.inputValue"%rmp2)

        #Doing another pma,rmp so upper lower lip can synch
        for cond1, rmp1, rmp2 in self.upAimTipNode:
            if "inEyelid" not in cond1 and "outEyelid" not in cond1:
                pma2= cmds.createNode("plusMinusAverage", n=cond1.replace("cond1","pma").replace("up","upLow"))
                valUp= cmds.getAttr("%s.colorIfTrueR"%cond1)
                valDown= cmds.getAttr("%s.colorIfTrueR"%cond1.replace("up","low"))
                cmds.setAttr("%s.operation"%pma2, 3)
                cmds.setAttr("%s.input1D[0]"%pma2, valUp)
                cmds.setAttr("%s.input1D[1]"%pma2, valDown)
                for subCond, ctrl1, val, valNeg in zip([cond1,cond1.replace("up","low")], [upBliCtrl,lowBliCtrl], [valUp,valDown], [valDown,valUp]):
                    rmp3= cmds.createNode("remapValue", n=subCond.replace("cond1","rmp3"))
                    cmds.setAttr("%s.value[1].value_FloatValue"%rmp3, val)
                    cmds.setAttr("%s.value[2].value_FloatValue"%rmp3, valNeg)
                    cmds.setAttr("%s.value[2].value_Position"%rmp3, -1)
                    cmds.setAttr("%s.value[2].value_Interp"%rmp3, 1)
                    cmds.connectAttr("%s.output1D"%pma2, "%s.value[0].value_FloatValue"%rmp3)
                    cmds.connectAttr("%s.ty"%ctrl1, "%s.inputValue"%rmp3)
                    cmds.connectAttr("%s.outValue"%rmp3, "%s.colorIfFalseR"%subCond)
                    cmds.connectAttr("%s.outValue"%rmp3, "%s.secondTerm"%subCond)
            else:
                #For corner, there is no up&down to change the minimum value
                fixVal= cmds.getAttr("%s.firstTerm"%cond1)
                cmds.setAttr("%s.secondTerm"%cond1, fixVal)
                cmds.setAttr("%s.colorIfFalseR"%cond1, fixVal)

        #Now only set md because prev need the ctrl to be connected to both upDown rmp only can get both value together
        for ctrl, allNode in zip([upBliCtrl,lowBliCtrl], [self.upAimTipNode,self.lowAimTipNode]):
            for cond1, rmp1, rmp2 in allNode:
                cmds.setAttr("%s.ty"%ctrl, -self.tyNeg)
                md1Val= cmds.getAttr("%s.colorIfTrueR"%cond1)-cmds.getAttr("%s.colorIfFalseR"%cond1) 
                cmds.setAttr("%s.ty"%ctrl, self.tyPos)
                md2Val= cmds.getAttr("%s.colorIfTrueR"%cond1)-cmds.getAttr("%s.colorIfFalseR"%cond1) 
                cmds.setAttr("%s.ty"%ctrl, 1)
                cmds.setAttr("%s.value[0].value_FloatValue"%rmp2, abs(md1Val))
                cmds.setAttr("%s.value[4].value_FloatValue"%rmp2, md2Val)                
            self.hideObjHis(ctrl)
        self.uiStuffClass.loadingBar(2)

    def eyeAimSetup(self, sides, color, mul):
        eyeRig= cmds.group(em=1, n="eye_%s_rig"%sides)
        eyeCtrlMG= cmds.group(em=1, n="eye_%s_ctrl_mainGrp"%sides)
        eyeJntMG= cmds.group(em=1, n="eye_%s_jnt_mainGrp"%sides)
        eyeLocMG= cmds.group(em=1, n="eye_%s_loc_mainGrp"%sides)
        cmds.parent(eyeCtrlMG, eyeJntMG, eyeLocMG, eyeRig)

        #Eyeball Loc
        eyeballUpLoc= cmds.spaceLocator(n="eyeball_%s_upLoc"%sides)
        eyeballUpLocOff= cmds.group(em=1, n="eyeball_%s_upLoc_offset"%sides)
        eyeballUpLocDir= cmds.group(em=1, n="eyeball_%s_upLoc_dirGrp"%sides)
        eyeballUpLocMG= cmds.group(em=1, n="eyeball_%s_upLoc_mainGrp"%sides)
        self.multiGrp(eyeballUpLoc,eyeballUpLocOff,eyeballUpLocDir,eyeballUpLocMG, eyeLocMG)
        cmds.xform(eyeballUpLocDir, t=(self.eyeballPiv[0], self.eyeballPiv[1]+self.ebBB[4]-self.ebBB[1], self.eyeballPiv[2]), ws=1)
        eyeAimLoc= cmds.spaceLocator(n="eyeAim_%s_loc"%sides)
        cmds.setAttr("%s.v"%eyeAimLoc[0], 0)

        #EyeAim Ctrl
        eyeAimCtrl= cmds.curve(d=3, n="eyeAim_%s_CTRL"%sides, p=[(0.0,1.49,0.0),(1.05,1.05,0.0),(1.49,0.0,0.0),(1.05,-1.05,0.0),(0.0,-1.49,0.0),(-1.05,-1.05,0.0),(-1.49,0.0,0.0),(-1.05,1.05,0.0)])
        cmds.closeCurve(eyeAimCtrl, ps=0, rpo=1)
        self.ctrlShp(eyeAimCtrl, color)
        eyeAimCtrlOff= cmds.group(em=1, n="%s_offset"%eyeAimCtrl)
        eyeAimCtrlFollow= cmds.group(em=1, n="%s_follow"%eyeAimCtrl)
        eyeAimCtrlDirGrp= cmds.group(em=1, n="%s_dirGrp"%eyeAimCtrl)
        eyeAimCtrlMG= cmds.group(em=1, n="%s_mainGrp"%eyeAimCtrl)
        self.multiGrp(eyeAimCtrl,eyeAimCtrlOff,eyeAimCtrlFollow,eyeAimCtrlDirGrp,eyeAimCtrlMG, eyeCtrlMG)
        cmds.xform(eyeAimCtrlOff, s=(self.ctrlSize2, self.ctrlSize2, self.ctrlSize2))
        cmds.refresh()
        cmds.makeIdentity(eyeAimCtrlOff, a=1, s=1, n=0, pn=1)
        eyeballCtrl= cmds.duplicate(eyeAimCtrl, n="eyeball_%s_CTRL"%sides)
        cmds.parent(eyeAimLoc,eyeAimCtrl)
        cmds.xform(eyeAimCtrlDirGrp, t=(self.eyeballPiv[0], self.eyeballPiv[1], self.eyeballPiv[2]+self.pupilDis*25))
        
        #EyeBall Ctrl
        eyeballCtrlOff= cmds.group(em=1, n="%s_offset"%eyeballCtrl[0])
        eyeballCtrlDirGrp= cmds.group(em=1, n="%s_dirGrp"%eyeballCtrl[0])
        eyeballCtrlMG= cmds.group(em=1, n="%s_mainGrp"%eyeballCtrl[0])
        self.multiGrp(eyeballCtrl,eyeballCtrlOff,eyeballCtrlDirGrp,eyeballCtrlMG, eyeCtrlMG)      
        if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
            cmds.xform(eyeballCtrl, t=(0,0,0), s=(self.ctrlSize1/3, self.ctrlSize1/3, self.ctrlSize1/3), ws=1)
        else:
            cmds.xform(eyeballCtrl, t=(0,0,0), s=(self.ctrlSize1, self.ctrlSize1, self.ctrlSize1), ws=1)
        cmds.xform(eyeballCtrlDirGrp, t=(self.eyeballPiv[0]*4+(self.ebBB[3]-self.ebBB[0])*mul, self.eyeballPiv[1], self.eyeballPiv[2]), ws=1)
        cmds.makeIdentity(eyeballCtrlMG, a=1, s=1, n=0, pn=1)  

        #Eyeball Jnt
        eyeballJnt= cmds.createNode("joint", n="eyeball_%s_jnt"%sides)
        eyeballEndJnt= cmds.createNode("joint", n="eyeballEnd_%s_jnx"%sides)
        eyeballJntGrp= cmds.group(em=1, n="%s_grp"%eyeballJnt)
        eyeballJntDirGrp= cmds.group(em=1, n="%s_dirGrp"%eyeballJnt)
        eyeballJntMG= cmds.group(em=1, n="%s_mainGrp"%eyeballJnt)        
        self.multiGrp(eyeballEndJnt,eyeballJnt,eyeballJntGrp,eyeballJntDirGrp,eyeballJntMG, eyeJntMG)
        cmds.xform(eyeballJntDirGrp, t=(self.eyeballPiv[0], self.eyeballPiv[1], self.eyeballPiv[2]), ws=1)  
        cmds.xform(eyeballEndJnt, t=(self.eyeballPiv[0], self.eyeballPiv[1], self.eyeballPiv[2]+self.pupilDis*3), ws=1)
        #EyeSocket Jnt
        eyeSocketJnt= cmds.createNode("joint", n="eyeSocket_%s_jnt"%sides)
        eyeSocketEndJnt= cmds.createNode("joint", n="eyeSocketEnd_%s_jnx"%sides)
        eyeSocketJntGrp= cmds.group(em=1, n="%s_grp"%eyeSocketJnt)
        eyeSocketJntDirGrp= cmds.group(em=1, n="%s_dirGrp"%eyeSocketJnt)
        eyeSocketJntMG= cmds.group(em=1, n="%s_mainGrp"%eyeSocketJnt)
        self.multiGrp(eyeSocketEndJnt, eyeSocketJnt,eyeSocketJntGrp,eyeSocketJntDirGrp,eyeSocketJntMG, eyeJntMG)
        cmds.xform(eyeSocketJntDirGrp, t=(self.eyeballPiv[0], self.eyeballPiv[1], self.eyeballPiv[2]), ws=1)
        cmds.xform(eyeSocketEndJnt, t=(self.eyeballPiv[0], self.eyeballPiv[1], self.eyeballPiv[2]+self.pupilDis*2), ws=1)
        ac1= cmds.aimConstraint(eyeAimLoc, eyeballJntGrp, mo=1, aim=(0,0,1), u=(0,1,0), wut="object", wuo=eyeballUpLoc[0])
        
        #Offset for eyeAimCtrl
        ac2= cmds.aimConstraint(eyeballJntGrp, eyeAimLoc, mo=1, aim=(0,0,-1), u=(0,1,0), wut="vector")
        dcm= cmds.createNode("decomposeMatrix", n="%s_rm_dcm"%eyeAimLoc[0])
        cmds.connectAttr("%s.inverseMatrix"%eyeAimLoc[0], "%s.inputMatrix"%dcm)
        cmds.connectAttr("%s.outputRotate"%dcm, "%s.offset"%ac1[0])
        #So that the aimContraint ignore both offset & offsetGrp(this is actually eyeAimMainCtrl)
        mm= cmds.createNode("multMatrix", n="%sOffset_mm"%eyeAimCtrl)
        cmds.connectAttr("%s.parentInverseMatrix"%eyeAimCtrlFollow, "%s.matrixIn[0]"%mm)
        cmds.connectAttr("%s.parentMatrix"%eyeAimCtrlOff, "%s.matrixIn[1]"%mm)
        cmds.connectAttr("%s.worldInverseMatrix"%eyeAimCtrlOff, "%s.matrixIn[2]"%mm)
        cmds.connectAttr("%s.matrixSum"%mm, "%s.constraintParentInverseMatrix"%ac2[0], f=1)
        
        for attr in ("x","y","z"):        
            cmds.connectAttr("%s.t%s"%(eyeballCtrl[0],attr), "%s.t%s"%(eyeballJntGrp,attr))
            cmds.connectAttr("%s.s%s"%(eyeballCtrl[0],attr), "%s.s%s"%(eyeballJntGrp,attr))
            cmds.connectAttr("%s.r%s"%(eyeballCtrl[0],attr), "%s.r%s"%(eyeballJnt,attr))
            cmds.connectAttr("%s.t%s"%(eyeballJntGrp,attr), "%s.t%s"%(eyeSocketJntGrp,attr))
            cmds.connectAttr("%s.s%s"%(eyeballJntGrp,attr), "%s.s%s"%(eyeSocketJntGrp,attr))
            cmds.connectAttr("%s.t%s"%(eyeballJntGrp,attr), "%s.t%s"%(eyeballUpLocOff,attr))

        #EyeballSide Loc (for slanted eyes like quadruped)
        eyeAimSideLoc= cmds.spaceLocator(n="eyeAim_%s_sideLoc"%sides)
        eyeAimSideLocOff= cmds.group(em=1, n="eyeball_%s_sideLoc_offset"%sides)
        eyeAimSideLocDir= cmds.group(em=1, n="eyeball_%s_sideLoc_dirGrp"%sides)
        eyeAimSideLocMG= cmds.group(em=1, n="eyeball_%s_sideLoc_mainGrp"%sides)
        self.multiGrp(eyeAimSideLoc,eyeAimSideLocOff,eyeAimSideLocDir,eyeAimSideLocMG, eyeLocMG)
        cmds.xform(eyeAimSideLocDir, t=(self.pupilPiv[0], self.pupilPiv[1], self.pupilPiv[2]), ws=1)  
        cmds.setAttr("%s.tz"%eyeAimSideLocOff, (self.pupilDis*25)-self.pupilDis)      
        ac3= cmds.aimConstraint(eyeballJntGrp, eyeAimSideLocDir, mo=0, aim=(0,0,-1), u=(0,1,0), wut="object", wuo=eyeballUpLoc[0])
        cmds.delete(ac3)
        if cmds.getAttr("%s.r"%eyeAimSideLocDir)==[(0.0, 0.0, 0.0)]:
            eyeAimSideLoc=[]

        #Create guide
        guide= cmds.curve(d=1, n="eyeAim_%s_guideCrv"%sides, p=[(0,0,0),(0,0,1)])
        newShp= self.ctrlShp(guide, 0, 2)
        for x, thing in enumerate((eyeAimCtrl,eyeballJnt)):
            mm= cmds.createNode("multMatrix", n="%s_mm"%thing)
            dcm= cmds.createNode("decomposeMatrix", n="%s_dcm"%thing)
            cmds.connectAttr("%s.worldMatrix"%thing, "%s.matrixIn[0]"%mm)
            cmds.connectAttr("%s.worldInverseMatrix"%guide, "%s.matrixIn[1]"%mm)
            cmds.connectAttr("%s.matrixSum"%mm, "%s.inputMatrix"%dcm)
            cmds.connectAttr("%s.outputTranslate"%dcm, "%s.controlPoints[%s]"%(newShp,x))
        cmds.parent(guide, eyeRig)

        #If didnt build eyelid, then no need to connect to eyeAim
        if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
            cmds.addAttr(eyeAimCtrl, ln="eyelid", at="enum")
            cmds.addAttr(eyeAimCtrl, ln="upperWeight", at="float", min=0, max=1)
            cmds.addAttr(eyeAimCtrl, ln="lowerWeight", at="float", min=0, max=1)
            cmds.setAttr("%s.eyelid"%eyeAimCtrl, k=1, l=1)          
            cmds.setAttr("%s.upperWeight"%eyeAimCtrl, 0.5, k=1)         
            cmds.setAttr("%s.lowerWeight"%eyeAimCtrl, 0.5, k=1)  
            for upDown, follow in zip(("up","low"),(self.upTwkJnt,self.lowTwkJnt)):
                for stuff in follow:
                    pb= cmds.createNode("pairBlend", n="%s_pb"%eyeballJnt)
                    cmds.setAttr("%s.rotInterpolation"%pb, 1)
                    if upDown=="up":
                        cmds.connectAttr("%s.upperWeight"%eyeAimCtrl, "%s.weight"%pb)
                    else:
                        cmds.connectAttr("%s.lowerWeight"%eyeAimCtrl, "%s.weight"%pb)
                    for attr, capAttr in zip(["x","y","z"], ["X","Y","Z"]):
                        cmds.connectAttr("%s.r%s"%(guide,attr), "%s.inRotate%s1"%(pb,capAttr))
                        cmds.connectAttr("%s.r%s"%(eyeballJnt.replace("jnt","jnt_grp"),attr), "%s.inRotate%s2"%(pb,capAttr))
                        cmds.connectAttr("%s.outRotate%s"%(pb,capAttr), "%s.r%s"%(stuff.replace("jnt","followAim"),attr))
        self.lockAttr(eyeAimCtrl, ["rx","ry","rz","sx","sy","sz","v"])
        self.lockAttr(eyeballCtrl[0], ["v"])

        #cleanup
        cmds.setAttr("%s.v"%eyeLocMG, 0)
        cmds.sets(eyeballJnt, eyeSocketJnt, add="%s"%self.set2)
        self.hideObjHis(eyeAimCtrl)
        self.uiStuffClass.loadingBar(2)
        return eyeAimCtrlFollow, eyeRig, eyeAimSideLoc, eyeAimCtrlOff

    def getParam(self, pnt, crv):
        npoc= cmds.createNode("nearestPointOnCurve")  
        cmds.setAttr("%s.inPosition"%npoc, pnt[0], pnt[1], pnt[2])
        cmds.connectAttr("%s.worldSpace[0]"%crv, "%s.inputCurve"%npoc)
        param= cmds.getAttr("%s.parameter"%npoc)
        cmds.delete(npoc)
        return param

    def cage(self):   
        obj= cmds.ls(sl=1)
        full= ["outEndEyelidFull_crv","outMainEyelidFull_crv","mainEyelidFull_crv","inMainEyelidFull_crv","inEndEyelidFull_crv"] 
        test1, test2, mis, tipJnt= [],[],[],[]
        if len(obj)==1:
            if cmds.listRelatives(obj, typ="mesh"):
                test1= 1
                skinC0= mel.eval("findRelatedSkinCluster %s"%obj[0])
                if skinC0=="":
                    test2= 1
        if test1:
            if test2:
                for item in full:
                    if cmds.objExists(item)==0:
                        mis.append(item.replace("Full_crv", ""))
                if mis==[]:
                    spans= cmds.getAttr("mainEyelidFull_crv.spans")
                    baseJnt= cmds.createNode("joint", n="base_jnt")
                    srf= cmds.loft(full, n="eyelidCage_srf", d=1, ch=0, rn=1, po=0, rsn=0)

                    #Finding tip joint. Should i have planB if the sets is deleted?
                    cmds.select("eyelidJnt_sets")
                    for jnt in cmds.ls(sl=1):
                        #if "_L_" in jnt:
                            tipJnt.append(jnt)

                    #Skin
                    skinC1= cmds.skinCluster(tipJnt, srf, tsb=1, bm=0, sm=0, nw=1, wd=0, mi=1, dr=4) 
                    cmds.skinCluster(skinC1, e=1, lw=1, tsb=1, ai=baseJnt, wt=0)
                    
                    for x in range(spans):
                        #flushing outEnd, inEnd skinWeight to baseJnt
                        for y in [0,4]:
                            cmds.skinPercent(skinC1[0], "%s.cv[%s][%s]"%(srf[0],y,x), tv=(baseJnt, 1))
                        #flushing outMain, inMain skinWeight to mainJnt
                        valTemp= cmds.skinPercent(skinC1[0], "%s.cv[2][%s]"%(srf[0],x), q=1, v=1)
                        bindJnt= cmds.skinPercent(skinC1[0], "%s.cv[2][%s]"%(srf[0],x), q=1, t=None)
                        #Is it confirm that there will be a 1?? what if no?
                        cmds.skinPercent(skinC1[0], "%s.cv[1][%s]"%(srf[0],x), tv=(bindJnt[valTemp.index(1)], 1))
                        cmds.skinPercent(skinC1[0], "%s.cv[3][%s]"%(srf[0],x), tv=(bindJnt[valTemp.index(1)], 1))

                    #Copy Weight
                    dum= cmds.nurbsToPoly(srf, mnd=1, ch=1, f=3, chr=0.1, ut=1, vt=1, ucr=0, cht=0.2, ntr=0, mrt=0, uss=1)
                    cmds.delete(dum[0], ch=1)
                    skinC2= cmds.skinCluster(tipJnt, baseJnt, dum[0], tsb=1)
                    skinC3= cmds.skinCluster(tipJnt, baseJnt, obj, tsb=1, sm=1)
                    cmds.copySkinWeights(nm=1, sa="closestPoint", ia=("name", "closestJoint"), ss=skinC1[0], ds=skinC2[0])     
                    cmds.copySkinWeights(nm=1, sa="closestPoint", ia=("name", "closestJoint"), ss=skinC2[0], ds=skinC3[0])  
                    cmds.copySkinWeights(mm="YZ", sa="closestPoint", ia="closestJoint", ss=skinC3[0], ds=skinC3[0])
                    cmds.delete(srf, dum[0])
                    cmds.select(obj)
                else:
                    cmds.warning("There are missing placers (%s)"%(", ").join(mis))
            else:
                cmds.warning("Selected mesh already have skinCluster")
        else:
            cmds.warning("Please select 1 MESH (Eyelid mesh, not the main head mesh)")


    def helps(self):
        name="Help On EyelidSetup"
        helpTxt="""
        - To create Eyelid, Eyeball, Eyeaim setup



        1) Eyelid Ctrl 
        ===============
            - Have eyelid tweaker ctrl
                - To control all the joints on the eyelid
            - Have eyeblink ctrl
                - To control a blendshape curve to drive the blink shape 
                - you can modify the blink shape by modifying the curve (to have custom shape eg. tear duct)

        2) Eyeball Ctrl 
        ===============
            - Move the eyeball mesh around with the eyelid
            - Due to eyeball_jnt will be constantly aiming, there will be a "eyeSocket_jnt" to bind to eyelid

        3) EyeAim Ctrl 
        ===============
            - Standard eyeAim ctrl but its workable with slanted eye without affecting its movement when moving eyeAim to z-axis
        """
        self.helpBoxClass.helpBox1(name, helpTxt)    

    def reloadSub(self):
        EyelidSetup()   
            

if __name__=='__main__':
    EyelidSetup() 
