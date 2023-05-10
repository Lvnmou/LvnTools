import maya.cmds as cmds
import Mod.dialog as dialog
import Mod.sepBox as sepBox
import Mod.helpBox as helpBox

class CopyMirSDK(object):
    def __init__(self, *args):
        self.sepBoxClass= sepBox.SepBox()
        self.dialogClass= dialog.Dialog()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()


    def win(self):        
        try: 
            cmds.deleteUI("cmSDK") 
        except:
            pass    
        cmds.window("cmSDK", mb=1)              
        cmds.window("cmSDK", t="Copy Mirror Set Driven", s=1, e=1, wh=(490,420))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on CopyMirrorSetDriven", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload CopyMirrorSetDriven", c=lambda x:self.reloadSub())
        column1 = self.sepBoxClass.sepBoxMain() 
        cmds.tabLayout(p=column1, cr=1, scr=1) 
        form1= cmds.formLayout("Normal", nd=100) 
        txt11= cmds.text(l="Select TARGET", fn="smallObliqueLabelFont", en=0)    
        self.rb1= cmds.radioButtonGrp(l="", cw4=(20, 200, 140, 130), la3=["Driver search same with Driven", "Use Same Driver", "None"], nrb=3 , sl=1 , onc=lambda x:self.rbc())      
        sep1= cmds.separator( h=20, st="in" )     
        self.txt12= cmds.text("Driver", en=0)
        self.txtDrSear= cmds.textFieldGrp(l="Search :", tx="R", cw2=(60,150), en=0, adj=2)
        self.txtDrRepl= cmds.textFieldGrp(l="Replace :", tx="L", cw2=(60,150), en=0, adj=2)
        txt13= cmds.text("Driven")
        self.txtDnSear= cmds.textFieldGrp(l="Search :", tx="R", cw2=(60,150), adj=2, cc=lambda x:self.txc(self.txtDnSear, self.txtDrSear))
        self.txtDnRepl= cmds.textFieldGrp(l="Replace :", tx="L", cw2=(60,150), adj=2, cc=lambda x:self.txc(self.txtDnRepl, self.txtDrRepl))
        sep2= cmds.separator( h=20, st="in" )       
        txt14= cmds.text("--- Reverse Time ---")
        self.timeMain= cmds.checkBoxGrp(l="", ncb=2, la2=["All", "Custom"], cw3=(0,50,50), cc1=lambda x:self.ccAll(1))          
        self.timeTran= cmds.checkBoxGrp(l="", ncb=4, la4=["-Tran","X","Y","Z"], cw2=(0,50), vr=1, on1=lambda x:self.ccOnOff(self.timeTran,1), of1=lambda x:self.ccOnOff(self.timeTran,0),  cc=lambda x:self.ccSub(self.timeTran))   
        self.timeRot= cmds.checkBoxGrp(l="", ncb=4, la4=["-Rot","X","Y","Z"], cw2=(0,50), vr=1, on1=lambda x:self.ccOnOff(self.timeRot,1), of1=lambda x:self.ccOnOff(self.timeRot,0),  cc=lambda x:self.ccSub(self.timeRot))  
        self.timeScal= cmds.checkBoxGrp(l="", ncb=4, la4=["-Scal","X","Y","Z"], cw2=(0,50), vr=1, on1=lambda x:self.ccOnOff(self.timeScal,1), of1=lambda x:self.ccOnOff(self.timeScal,0),  cc=lambda x:self.ccSub(self.timeScal))     
        sep3= cmds.separator(h=100, st="in", hr=0, w=10) 
        txt15= cmds.text("--- Reverse Value ---")
        self.valMain= cmds.checkBoxGrp(l="", ncb=2, la2=["All", "Custom"], cw3=(0,50,50), cc1=lambda x:self.ccAll(2))                
        self.valTran= cmds.checkBoxGrp(l="", ncb=4, la4=["-Tran","X","Y","Z"], cw2=(0,50), vr=1, on1=lambda x:self.ccOnOff(self.valTran,1), of1=lambda x:self.ccOnOff(self.valTran,0),  cc=lambda x:self.ccSub(self.valTran))    
        self.valRot= cmds.checkBoxGrp(l="", ncb=4, la4=["-Rot","X","Y","Z"], cw2=(0,50), vr=1, on1=lambda x:self.ccOnOff(self.valRot,1), of1=lambda x:self.ccOnOff(self.valRot,0),  cc=lambda x:self.ccSub(self.valRot))  
        self.valScal= cmds.checkBoxGrp(l="", ncb=4, la4=["-Scal","X","Y","Z"], cw2=(0,50), vr=1, on1=lambda x:self.ccOnOff(self.valScal,1), of1=lambda x:self.ccOnOff(self.valScal,0),  cc=lambda x:self.ccSub(self.valScal))       
        b1= cmds.button(l="Copy / Mirror", c=lambda x:self.preTest()) 
        b2= cmds.button(l="All Driven", c=lambda x:self.allDn()) 
        b3= cmds.button(l="Connected Driver", c=lambda x:self.connDrDn(1)) 
        b4= cmds.button(l="Connected Driven", c=lambda x:self.connDrDn(2))  
        cmds.formLayout(form1, e=1,
                                af=[(txt11, "top", 10),
                                    (self.rb1, "top", 25),
                                    (sep1, "top", 45),
                                    (self.txt12, "top", 65),
                                    (self.txtDrSear, "top", 80),
                                    (self.txtDrRepl, "top", 103),
                                    (txt13, "top", 65),
                                    (self.txtDnSear, "top", 80),
                                    (self.txtDnRepl, "top", 103),
                                    (sep2, "top", 130),
                                    (txt14, "top", 150),
                                    (self.timeMain, "top", 178),
                                    (self.timeTran, "top", 200),
                                    (self.timeRot, "top", 200),
                                    (self.timeScal, "top", 200),
                                    (sep3, "top", 170),
                                    (txt15, "top", 150),
                                    (self.valMain, "top", 178),
                                    (self.valTran, "top", 200),
                                    (self.valRot, "top", 200),
                                    (self.valScal, "top", 200),
                                    (b1, "top", 280),
                                    (b2, "top", 306),
                                    (b3, "top", 306),
                                    (b4, "top", 306)],
                                ap=[(txt11, "left", 200, 0),
                                    (sep1, "left", 0, 0),
                                    (sep1, "right", 0, 100),
                                    (self.txt12, "left", 0, 0),
                                    (self.txt12, "right", 0, 50),
                                    (self.txtDrSear, "left", 0, 0),
                                    (self.txtDrSear, "right", 0, 50),
                                    (self.txtDrRepl, "left", 0, 0),
                                    (self.txtDrRepl, "right", 0, 50),
                                    (txt13, "left", 0, 51),
                                    (txt13, "right", 0, 100),
                                    (self.txtDnSear, "left", 0, 51),
                                    (self.txtDnSear, "right", 0, 100),
                                    (self.txtDnRepl, "left", 0, 51),
                                    (self.txtDnRepl, "right", 0, 100),
                                    (sep2, "left", 0, 0),
                                    (sep2, "right", 0, 100),
                                    (txt14, "left", 0, 0),
                                    (txt14, "right", 0, 50),
                                    (self.timeMain, "left", -50, 24),
                                    (self.timeMain, "right", 0, 26),
                                    (self.timeTran, "left", -80, 24),
                                    (self.timeTran, "right", 0, 26),
                                    (self.timeRot, "left", -20, 24),
                                    (self.timeRot, "right", 0, 26),
                                    (self.timeScal, "left", 40, 24),
                                    (self.timeScal, "right", 0, 26),
                                    (sep3, "left", 0, 40),
                                    (sep3, "right", 0, 60),
                                    (txt15, "left", 0, 50),
                                    (txt15, "right", 0, 100),
                                    (self.valMain, "left", -40, 74),
                                    (self.valMain, "right", 0, 76),
                                    (self.valTran, "left", -70, 74),
                                    (self.valTran, "right", 0, 76),
                                    (self.valRot, "left", -10, 74),
                                    (self.valRot, "right", 0, 76),
                                    (self.valScal, "left", 50, 74),
                                    (self.valScal, "right", 0, 76),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 100),
                                    (b2, "left", 0, 0),
                                    (b2, "right", 0, 33),
                                    (b3, "left", 0, 34),
                                    (b3, "right", 0, 67),
                                    (b4, "left", 0, 68),
                                    (b4, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        cmds.setParent("..") 
        form2= cmds.formLayout("Self", nd=100)
        txt21= cmds.text(l="Select DRIVEN (Can skip, usually its 0)", fn="smallObliqueLabelFont", en=0)
        self.floatF= cmds.floatFieldGrp(l="Mirror Axis Value :", cw2=(95,150), adj=2, pre=3)    
        b1= cmds.button(l="Min", c=lambda x:self.getMirVal(1)) 
        b2= cmds.button(l="Highest Negative", c=lambda x:self.getMirVal(2)) 
        b3= cmds.button(l="Lowest Positive", c=lambda x:self.getMirVal(3))  
        b4= cmds.button(l="Max", c=lambda x:self.getMirVal(4))  
        b5= cmds.button(l="Mirror Self SDK", c=lambda x:self.mirSelf()) 
        cmds.formLayout(form2, e=1,
                                af=[(txt21, "top", 10),
                                    (b1, "top", 25),
                                    (b2, "top", 25),
                                    (b3, "top", 25),
                                    (b4, "top", 25),
                                    (self.floatF, "top", 50),
                                    (b5, "top", 90)],
                                ap=[(txt21, "left", 0, 0),
                                    (txt21, "right", 0, 100),
                                    (self.floatF, "left", 0, 0),
                                    (self.floatF, "right", 0, 100),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 25),
                                    (b2, "left", 0, 26),
                                    (b2, "right", 0, 50),
                                    (b3, "left", 0, 51),
                                    (b3, "right", 0, 75), 
                                    (b4, "left", 0, 76),
                                    (b4, "right", 0, 100),                                    
                                    (b5, "left", 0, 0),
                                    (b5, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        cmds.showWindow("cmSDK")

    def defi(self):
        self.obj= cmds.ls(sl=1)
        self.drSear= cmds.textFieldGrp(self.txtDrSear, q=1, tx=1)
        self.drRepl= cmds.textFieldGrp(self.txtDrRepl, q=1, tx=1)    
        self.dnSear= cmds.textFieldGrp(self.txtDnSear, q=1, tx=1)
        self.dnRepl= cmds.textFieldGrp(self.txtDnRepl, q=1, tx=1)
        drTx,drTy,drTz,drRx,drRy,drRz,drSx,drSy,drSz,dnTx,dnTy,dnTz,dnRx,dnRy,dnRz,dnSx,dnSy,dnSz= 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1    
        #driver translate
        if cmds.checkBoxGrp(self.timeTran, q=1, v2=1):
            drTx=-1
        if cmds.checkBoxGrp(self.timeTran, q=1, v3=1):
            drTy=-1
        if cmds.checkBoxGrp(self.timeTran, q=1, v4=1):
            drTz=-1
        #drive rotate       
        if cmds.checkBoxGrp(self.timeRot, q=1, v2=1):
            drRx=-1
        if cmds.checkBoxGrp(self.timeRot, q=1, v3=1):
            drRy=-1
        if cmds.checkBoxGrp(self.timeRot, q=1, v4=1):
            drRz=-1
        #driver scale
        if cmds.checkBoxGrp(self.timeScal, q=1, v2=1):
            drSx=-1
        if cmds.checkBoxGrp(self.timeScal, q=1, v3=1):
            drSy=-1
        if cmds.checkBoxGrp(self.timeScal, q=1, v4=1):
            drSz=-1
        #driven translate
        if cmds.checkBoxGrp(self.valTran, q=1, v2=1):
            dnTx=-1
        if cmds.checkBoxGrp(self.valTran, q=1, v3=1):
            dnTy=-1
        if cmds.checkBoxGrp(self.valTran, q=1, v4=1):
            dnTz=-1
        #driven rotate       
        if cmds.checkBoxGrp(self.valRot, q=1, v2=1):
            dnRx=-1
        if cmds.checkBoxGrp(self.valRot, q=1, v3=1):
            dnRy=-1
        if cmds.checkBoxGrp(self.valRot, q=1, v4=1):
            dnRz=-1
        #driven scale
        if cmds.checkBoxGrp(self.valScal, q=1, v2=1):
            dnSx=-1
        if cmds.checkBoxGrp(self.valScal, q=1, v3=1):
            dnSy=-1
        if cmds.checkBoxGrp(self.valScal, q=1, v4=1):
            dnSz=-1 
        self.drdnAttr=["translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ"]
        self.drVal=[drTx, drTy, drTz, drRx, drRy, drRz, drSx, drSy, drSz]
        self.dnVal=[dnTx, dnTy, dnTz, dnRx, dnRy, dnRz, dnSx, dnSy, dnSz]
        self.ff= cmds.floatFieldGrp(self.floatF, v1=1, q=1)    

    def txc(self, txtFOri, txtF):
        line1= cmds.textFieldGrp(txtFOri, q=1, tx=1)    
        if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==1:  
            cmds.textFieldGrp(txtF, e=1, tx= line1)        
                              
    def rbc(self):
        if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==1 or cmds.radioButtonGrp(self.rb1, q=1, sl=1)==2:  
            cmds.textFieldGrp(self.txtDrSear, e=1, en=0)
            cmds.textFieldGrp(self.txtDrRepl, e=1, en=0)
            self.txc(self.txtDnSear, self.txtDrSear)
            self.txc(self.txtDnRepl, self.txtDrRepl)
            cmds.text(self.txt12, e=1, en=0)
        else:
            cmds.textFieldGrp(self.txtDrSear, e=1, en=1)   
            cmds.textFieldGrp(self.txtDrRepl, e=1, en=1)
            cmds.text("Driver", e=1, en=1)

    def ccAll(self, meth):
        if meth==1:
            method= self.timeMain, self.timeTran, self.timeRot, self.timeScal
        elif meth==2:
            method= self.valMain, self.valTran, self.valRot, self.valScal
        if cmds.checkBoxGrp(method[0], q=1, v1=1)==1: 
            cmds.checkBoxGrp(method[0], e=1, va2=[1,1]) 
            cmds.checkBoxGrp(method[1], e=1, va4=[1,1,1,1]) 
            cmds.checkBoxGrp(method[2], e=1, va4=[1,1,1,1]) 
            cmds.checkBoxGrp(method[3], e=1, va4=[1,1,1,1]) 
        else:
            cmds.checkBoxGrp(method[0], e=1, va2=[0,0]) 
            cmds.checkBoxGrp(method[1], e=1, va4=[0,0,0,0]) 
            cmds.checkBoxGrp(method[2], e=1, va4=[0,0,0,0]) 
            cmds.checkBoxGrp(method[3], e=1, va4=[0,0,0,0])    

    def ccOnOff(self, txt, val):
        cmds.checkBoxGrp(txt, e=1, va4=[val,val,val,val])
         
    def ccSub(self, txt):
        cmds.checkBoxGrp(txt, e=1, v1=1) 
        if cmds.checkBoxGrp(txt, q=1, v2=1)==1 and cmds.checkBoxGrp(txt, q=1, v3=1)==1 and cmds.checkBoxGrp(txt, q=1, v4=1)==1:
            cmds.checkBoxGrp(txt, e=1, v1=1) 
        else:
            cmds.checkBoxGrp(txt, e=1, v1=0)    

    def testVal(self, src, tar, meth):
        self.defi()           
        ans, test= 1, 1
        if meth==1:
            method= src, self.drdnAttr, self.drVal, self.timeMain
        elif meth==2:
            method= tar, self.drdnAttr, self.dnVal, self.valMain
        for item, thing in zip(method[1],method[2]):
            if item in method[0]:
                ans= thing
                test= []
        if cmds.checkBoxGrp(method[3], q=1, v1=1)==1:
            if test:
                ans=-1
        return ans    

    def preFinal(self, src, tar, curvs, dup): 
        dr= self.testVal(src, tar, 1)
        dn= self.testVal(src, tar, 2)           
        tim= cmds.keyframe(curvs, q=1, fc=1)
        val= cmds.keyframe(curvs, q=1, vc=1)
        if dr==1:
            for thing in enumerate(zip(tim,val)):                
                cmds.keyframe(dup, e=1, index=(thing[0],thing[0]), o="over", fc=dr* thing[1][0])
                cmds.keyframe(dup, e=1, index=(thing[0],thing[0]), o="over", vc=dn* thing[1][1])
        else:
            for thing in enumerate(reversed(zip(tim,val))): 
                cmds.keyframe(dup, e=1, index=(thing[0],thing[0]), o="over", fc=dr* thing[1][0])
                cmds.keyframe(dup, e=1, index=(thing[0],thing[0]), o="over", vc=dn* thing[1][1]) 
     
    def animCrvTest(self, obj, meth):
        allCrv, allTar, allBw, allCrvNoBw= [],[],[],[] 
        if meth==1:
            bw= cmds.listConnections(obj, t="blendWeighted", d=0, scn=1)
        elif meth==2:
            bw= cmds.listConnections(obj, t="blendWeighted", s=0, scn=1)
        if bw:
            for subBw in bw:
                obj.append(subBw)
                allBw.append(subBw)
        #is there any other way besides using loop to find SDK instead of keyframe?
        for animC in ["animCurveUA","animCurveUL","animCurveUT","animCurveUU"]:
            for item in obj:
                if meth==1:
                    crv= cmds.listConnections(item, t=animC, d=0, scn=1)
                elif meth==2:
                    crv= cmds.listConnections(item, t=animC, s=0, scn=1)
                if crv:
                    for subCrv in crv:
                        allCrv.append(subCrv)
                        if bw:
                            if item not in bw:
                                allCrvNoBw.append(subCrv)
                        else:
                            allCrvNoBw.append(subCrv)
        if allCrv:
            for subCrv in allCrv:
                if meth==1:
                    tar= cmds.listConnections(subCrv, d=0, scn=1)
                elif meth==2:
                    tar= cmds.listConnections(subCrv, s=0, scn=1)
                if tar:
                    for stuff in tar:
                        if cmds.objectType(stuff)!="nodeGraphEditorInfo" and cmds.objectType(stuff)!="hyperLayout":
                            if cmds.objectType(stuff)=="blendWeighted":
                                realTar= cmds.listConnections(stuff, s=0, scn=1)
                                if realTar:
                                    allTar.append(realTar[0])        
                            else:
                                if stuff not in allTar:
                                    allTar.append(stuff)
        return allCrv, allTar, allBw, allCrvNoBw

    def preTest(self):            
        self.defi() 
        test1= 1
        #test Driven same name
        conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(self.obj, self.dnSear, self.dnRepl)
        if conti:         
            #test after search replace, is it a driven
            for thing in self.obj:
                allCrv, allDriver, allBw, allCrvNoBw= self.animCrvTest([thing.replace(self.dnSear, self.dnRepl)], 1)
                if allCrv==[]:
                    test1=[]
            if test1:
                if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==1 or cmds.radioButtonGrp(self.rb1, q=1, sl=1)==3:
                    #test Driver same name
                    conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(allDriver, self.drRepl, self.drSear)
                    if conti:
                        self.mir()        
                else:
                    self.mir() 
            else:
                cmds.warning("Please select a TARGET instead OR one of the search replace SOURCE is not a driven object")                            

    def mir(self):                   
        self.defi()
        #Delete any existing SDK on target
        for item in self.obj:  
            allCrv, allTar, allBw, allCrvNoBw= self.animCrvTest([item], 1)
            if allCrv:
                cmds.delete(allCrv)
        for thing in self.obj:  
            allCrv, allTar, allBw, allCrvNoBw= self.animCrvTest([thing.replace(self.dnSear, self.dnRepl)], 1)
            if allCrvNoBw:
                for subCrv in allCrvNoBw:
                    src= cmds.listConnections("%s.input"%subCrv, p=1, scn=1)     
                    tar= cmds.listConnections("%s.output"%subCrv, p=1, scn=1)
                    #There are case where is a empty animCurve that didnt connect any source 
                    if src and tar:
                        dup= cmds.duplicate(subCrv, n=subCrv.replace(self.dnRepl, self.dnSear))
                        if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==2:
                            cmds.connectAttr(src[0], "%s.input"%dup[0], f=1)
                        else:  
                            cmds.connectAttr(src[0].replace(self.drRepl, self.drSear), "%s.input"%dup[0], f=1)
                        cmds.connectAttr("%s.output"%dup[0], tar[0].replace(self.dnRepl, self.dnSear), f=1)              
                        self.preFinal(src[0], tar[0], subCrv, dup[0])
            if allBw:
                for subBw in allBw:
                    bwSrc= cmds.listConnections("%s.input"%subBw,scn=1)     
                    bwTar= cmds.listConnections("%s.output"%subBw, p=1, scn=1)      
                    if bwSrc and bwTar:      
                        dupBw= cmds.duplicate(subBw, n=subBw.replace(self.dnRepl, self.dnSear))
                        cmds.connectAttr("%s.output"%dupBw[0], bwTar[0].replace(self.dnRepl, self.dnSear), f=1) 
                        for stuff in bwSrc:
                            preSrc= cmds.listConnections("%s.input"%stuff, p=1, scn=1) 
                            preTar= cmds.listConnections("%s.output"%stuff, p=1, scn=1) 
                            dupCrv= cmds.duplicate(stuff, n=stuff.replace(self.dnRepl, self.dnSear))
                            if preSrc and preTar:
                                if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==2:
                                    cmds.connectAttr(preSrc[0], "%s.input"%dupCrv[0], f=1)
                                else:     
                                    cmds.connectAttr(preSrc[0].replace(self.drRepl, self.drSear), "%s.input"%dupCrv[0], f=1)  
                                cmds.connectAttr("%s.output"%dupCrv[0], "%s.%s"%(dupBw[0],preTar[0].split(".")[1]), f=1)      
                                self.preFinal(preSrc[0], bwTar[0], stuff, dupCrv[0])

    def allDn(self): 
        finalTar= []
        curv= cmds.ls(typ=["animCurveUA","animCurveUL","animCurveUT","animCurveUU"])
        for item in curv:
            tar=[]
            chd= cmds.listConnections(item, s=0, scn=1, t="transform") 
            if chd:      
                for allChd in chd:
                    if cmds.objectType(allChd)=="blendWeighted":
                        realChd= cmds.listConnections(allChd, s=0, scn=1)
                        if realChd:
                            for stuff in realChd:
                                if stuff not in tar:
                                    tar.append(stuff)       
                    else:
                        tar.append(allChd)
                if tar:
                    for thing in tar:
                        if cmds.objectType(thing)!="nodeGraphEditorInfo" and cmds.objectType(thing)!="hyperLayout":
                            if thing not in finalTar:
                                finalTar.append(thing)                    
        if finalTar:
            cmds.select(finalTar)
            self.dialogClass.printingDialogUI2("< %s >   Driven"%len(finalTar), finalTar)                    
        else:
            cmds.warning("There is no any DRIVEN object in the scene!")

    def connDrDn(self, meth):
        self.defi()
        if self.obj:
            finalTar= []
            for item in self.obj:  
                if meth==1:
                    dTxt=("Driver","DRIVEN")
                    allCrv, allTar, allBw, allCrvNoBw= self.animCrvTest([item], 1)
                elif meth==2:
                    dTxt=("Driven","DRIVER")
                    allCrv, allTar, allBw, allCrvNoBw= self.animCrvTest([item], 2)
                if allTar:
                    for stuff in allTar:
                        if stuff not in finalTar:
                            finalTar.append(stuff)
            if finalTar:
                cmds.select(finalTar)
                self.dialogClass.printingDialogUI2("< %s >   Connected %s"%(len(finalTar),dTxt[0]), finalTar)
            else:
                cmds.warning("Selected object is not a %s, so that's there is no connected %s"%(dTxt[1],dTxt[0]))
        else:
            cmds.warning("Please select at least 1 object")
       
    def getMirVal(self, meth):
        self.defi()
        mainVal= {}
        if self.obj:
            if len(self.obj)==1:
                for item in self.obj:
                    allCrv, allTar, allBw, allCrvNoBw= self.animCrvTest([item], 1)
                    if allCrv:
                        for stuff in allCrv:
                            kf= cmds.keyframe(stuff, q=1, fc=1)
                            posV, negV= [],[]
                            if kf:
                                for thing in kf:
                                    if round(thing, 3)>=0:
                                        posV.append(thing)       
                                    if round(thing, 3)<=0:
                                        negV.append(thing)                       
                                if meth==1:
                                    tim= round(min(kf), 3)
                                elif meth==2:
                                    tim= max(negV)
                                elif meth==3: 
                                    tim= min(posV)
                                elif meth==4:
                                    tim= round(max(kf), 3)
                                mainVal[tim]=1 
                        if mainVal:
                            if meth==1 or meth==3:
                                cmds.floatFieldGrp(self.floatF, e=1, v1=min(mainVal))  
                            elif meth==2 or meth==4:
                                cmds.floatFieldGrp(self.floatF, e=1, v1=max(mainVal))  
                    else:
                        cmds.warning("Selected object is not a DRIVEN")      
            else:
                cmds.warning("Please select only 1  DRIVEN")
        else:
            cmds.warning("Please select at least 1 DRVEN") 

    def mirSelf(self):
        self.defi()
        if self.obj:
            for item in self.obj:
                allCrv, allTar, allBw, allCrvNoBw= self.animCrvTest([item], 1)
                if allCrv: 
                    for item in allCrv:
                        tim= cmds.keyframe(item, q=1, fc=1)
                        val= cmds.keyframe(item, q=1, vc=1)
                        if tim and val:
                            for x, things in enumerate(zip(tim,val)):
                                cmds.setKeyframe(item, f=(2*self.ff-(tim[x])), v=val[x])    
                else:
                    cmds.warning("Selected object is not a DRIVEN")
        else:
            cmds.warning("Please select at least 1 DRIVEN")      

    def helps(self):    
        name="Help On CopyMirrorSetDriven"
        helpTxt="""
        - To copy / mirror SDK from another object OR self (need to flip)



        < Normal >
        ===========
            1) Copy/Mirror
            ----------------
                A) Type
                --------
                    1. Driver search same with Driven
                       - Driver and Driven using same search replace
                
                    2. Use Same Driver
                        - Use back the same driver
                    
                    3. None
                        - Driver and Driven using different search replace

                B) Reverse
                -----------
                    - Time = Driver
                    - Value = Driven
                    - <Custom> is for custom attribute
                        
          
            2) Select Driver/Driven
            -------------------------
                1. All Driven
                    - Search for all objects that have set driven key
                
                2. Connected Driver
                    - Search SDK Driver object
                
                3. Connected Driven 
                    - Select SDK Driven object


        < Self >
        =========
            1) Min / Highest Negative / Lowest Positive / Max
            -----------------------------------------------------
                - This is to get the <Mirror axis value> from the SDK

                *(-90, -4, 4, 90 This are the example for these 4 options
                *BUT if there is 0, <Highest Negative>/<Lowest Positive> will be 0


            2) Mirror Axis Value 
            ----------------------
                - Which axis to mirror
                - Usually its 0 but sometimes might depends                
        """ 
        self.helpBoxClass.helpBox1(name, helpTxt) 

    def reloadSub(self):
        CopyMirSDK()
    

if __name__=='__main__':
    CopyMirSDK()


