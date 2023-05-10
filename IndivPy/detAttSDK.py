import maya.cmds as cmds
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox
import Mod.dialog as dialog


class DetAttSDK(object):
    def __init__(self, *args):
        self.uiStuffClass= uiStuff.UiStuff()
        self.dialogClass= dialog.Dialog()
        self.win()

    def win(self):    
        try:
            cmds.deleteUI("daSDK")
        except:
            pass            
        cmds.window("daSDK", mb=1)
        cmds.window("daSDK", t="Detach Attach Set Driven", e=1,s=1, wh=(260,355))   
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Detach Attach Set Driven", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Detach Attach Set Driven", c=lambda x:self.reloadSub()) 
        self.uiStuffClass.sepBoxMain()
        column11= self.uiStuffClass.sepBoxSub("Create")
        form11= cmds.formLayout(nd=100, p=column11)
        txt11= cmds.text(l="Select TARGET", fn="smallObliqueLabelFont", en=0)    
        b11= cmds.button(l="Detach", w=145, c=lambda x: self.det())    
        cmds.formLayout(form11, e=1,
                                af=[(txt11, "top", 0),
                                    (b11, "top", 16)],
                                ap=[(txt11, "left", 0, 0),
                                    (txt11, "right", 0, 100),
                                    (b11, "left", 0, 0),
                                    (b11, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column12= self.uiStuffClass.sepBoxSub()
        form12= cmds.formLayout(nd=100, p=column12)        
        txt121= cmds.text(l="To check parent name \nsee <Extra Attributes> under 'attribute editor'", fn="smallObliqueLabelFont", en=0)    
        self.cbSR= cmds.checkBoxGrp(l="", cw=(1,10), cc= lambda x:self.cbx())
        self.txtSear= cmds.textFieldGrp(l="Search :", cw2=(60,50), adj=2, en=0)
        self.txtRepl= cmds.textFieldGrp(l="Replace :", cw2=(60,50), adj=2, en=0)
        sep12= cmds.separator(h=5, st="in")
        txt122= cmds.text(l="Select TARGET", fn="smallObliqueLabelFont", en=0)    
        b12= cmds.button(l="Attach", c= lambda x: self.att()) 
        cmds.formLayout(form12, e=1,
                                af=[(txt121, "top", 0),
                                    (self.cbSR, "top", 50),
                                    (self.txtSear, "top", 35),
                                    (self.txtRepl, "top", 58),
                                    (sep12, "top", 90),
                                    (txt122, "top", 110),
                                    (b12, "top", 126)],
                                ap=[(txt121, "left", 0, 0),
                                    (txt121, "right", 0, 100),
                                    (self.cbSR, "left", 0, 0),
                                    (self.cbSR, "right", 0, 100),
                                    (self.txtSear, "left", 30, 0),
                                    (self.txtSear, "right", 0, 100),
                                    (self.txtRepl, "left", 30, 0),
                                    (self.txtRepl, "right", 0, 100),
                                    (sep12, "left", 0, 0),
                                    (sep12, "right", 0, 100),
                                    (txt122, "left", 0, 0),
                                    (txt122, "right", 0, 100),
                                    (b12, "left", 0, 0),
                                    (b12, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        cmds.showWindow("daSDK")

    def cbx(self):
        if cmds.checkBoxGrp(self.cbSR, q=1, v1=1):
            cmds.textFieldGrp(self.txtSear, e=1, en=1)
            cmds.textFieldGrp(self.txtRepl, e=1, en=1)        
        else:
            cmds.textFieldGrp(self.txtSear, e=1, en=0)
            cmds.textFieldGrp(self.txtRepl, e=1, en=0)   

    def defi(self):
        self.obj= cmds.ls(sl=1)
        self.sear= cmds.textFieldGrp(self.txtSear, tx=1, q=1)       
        self.repl= cmds.textFieldGrp(self.txtRepl, tx=1, q=1)       

    def preTest(self, obj):
        test1, tar, nonTar= [],[],[]
        test2= 1
        for item in obj:
            allAttr= cmds.listAttr(item, ud=1)
            if allAttr:
                if "lvnParent" not in allAttr:
                    test1= 1
                    nonTar.append(item)
                else:
                    test2= []
                    tar.append(item)
            else:
                test1= 1
                nonTar.append(item)
        return test1, test2, tar, nonTar

    def animCrvTest(self, obj):
        allCrv, allObj= [],[]
        #Loop for all children as well
        chd= cmds.listRelatives(obj, ad=1, pa=1)
        if chd:
            for allChd in chd:
                if allChd not in allObj:
                    allObj.append(allChd)
        allObj= obj+allObj
        bw= cmds.listConnections(allObj, t="blendWeighted", d=0, scn=1)
        if bw:
            for subBw in bw:
                allObj.append(subBw)
        for animC in ["animCurveUA","animCurveUL","animCurveUT","animCurveUU"]:
            for item in allObj:
                crv= cmds.listConnections(item, t=animC, d=0, scn=1)
                if crv:
                    for subCrv in crv:
                        allCrv.append(subCrv)
        return allCrv, allObj

    def detAttAnimCrv(self, obj, meth):
        for item in obj: 
            if meth==1:
                src= cmds.listConnections("%s.input"%item, p=1, scn=1)
                if src:
                    cmds.disconnectAttr(src[0], "%s.input"%item)
                    cmds.addAttr(item, ln="lvnParent", dt="string")    
                    cmds.setAttr("%s.lvnParent"%item, "%s"%src[0], typ="string")  
            else:
                exi= cmds.attributeQuery("lvnParent", n=item, ex=1)
                if exi:
                    par= cmds.getAttr("%s.lvnParent"%item)
                    if par:
                        if cmds.checkBoxGrp(self.cbSR, q=1, v1=1):
                            cmds.connectAttr(par.replace(self.sear, self.repl), "%s.input"%item)    
                        else:
                            cmds.connectAttr(par, "%s.input"%item)    
                    cmds.deleteAttr(item, at="lvnParent")                

    def det(self):
        self.defi()
        test1, test2, tar, nonTar= self.preTest(self.obj)
        finalTar, test3= [],[]
        for item in self.obj:
            par= cmds.listRelatives(item, p=1, pa=1)
            if par:
                test3= 1
        allCrv, allObj= self.animCrvTest(self.obj)
        if test1:
            conti= 1
            if test3 or allCrv:
                if test2==[]:
                    conti= self.dialogClass.printingDialog(tar, "< %s > can continue\n< %s > already been DETACHED"%(len(nonTar),len(tar)))
                if conti:
                    self.uiStuffClass.loadingBar(1, len(nonTar))
                    self.detAttAnimCrv(allCrv, 1)
                    for item in nonTar:
                        par= cmds.listRelatives(item, p=1, pa=1)
                        cmds.addAttr(item, ln="lvnParent", dt="string")  
                        if par: 
                            cmds.setAttr("%s.lvnParent"%item, "%s"%par[0], l=1, typ="string")    
                        for attr,cus in zip(["t","r","s","jointOrient"],["lvnTran","lvnRot","lvnScal","lvnJntOr"]):
                            #If its joint only add this jointOrient attr
                            if cus=="lvnJntOr":
                                if cmds.objectType(item)!="joint":
                                    break
                            val= cmds.getAttr("%s.%s"%(item,attr))        
                            cmds.addAttr(item, ln="%s"%cus, at="double3")
                            for subAttr in ("X","Y","Z"):
                                cmds.addAttr(item, ln="%s%s"%(cus,subAttr), p="%s"%cus, at="double")
                            cmds.setAttr("%s.%s"%(item,cus), val[0][0],val[0][1],val[0][2], l=1)
                        if par:
                            item= cmds.parent(item, w=1)[0]
                        finalTar.append(item) 
                        self.uiStuffClass.loadingBar(2)
                    self.uiStuffClass.loadingBar(3, sel=finalTar)
            else: 
                cmds.warning("There is no PARENT group and SET DRIVEN KEY for all the selected object, including their children")
        else:
            cmds.warning("All of the selected object already been DETACHED")

    def att(self):
        self.defi()
        test1, test2, tar, nonTar= self.preTest(self.obj)
        allCrv, allObj= self.animCrvTest(self.obj)
        newTar= []
        if test2==[]:
            conti= 1
            if test1:
                conti= self.dialogClass.printingDialog(nonTar, "< %s > can continue\n< %s > have not been DETACH"%(len(tar),len(nonTar)))
            if conti:
                self.uiStuffClass.loadingBar(1, len(tar))
                self.detAttAnimCrv(allCrv, 2)
                for item in tar:
                    par= cmds.getAttr("%s.lvnParent"%item)
                    if par:
                        if cmds.checkBoxGrp(self.cbSR, q=1, v1=1):
                            item= cmds.parent(item, par.replace(self.sear,self.repl))[0]
                        else:
                            item= cmds.parent(item, par)[0]
                    cmds.setAttr("%s.lvnParent"%item, l=0)    
                    cmds.deleteAttr("%s"%item, at="lvnParent")     
                    for attr,cus in zip(["t","r","s","jointOrient"],["lvnTran","lvnRot","lvnScal","lvnJntOr"]):
                        #If its joint only add this jointOrient attr
                        if cus=="lvnJntOr":
                            if cmds.objectType(item)!="joint":
                                break
                        val= cmds.getAttr("%s.%s"%(item,cus))        
                        cmds.setAttr("%s.%s"%(item,attr), val[0][0],val[0][1],val[0][2])
                        cmds.setAttr("%s.%s"%(item,cus), l=0)  
                        cmds.deleteAttr(item, at="%s"%cus)
                    newTar.append(item)
                    self.uiStuffClass.loadingBar(2) 
                self.uiStuffClass.loadingBar(3, sel=newTar)
        else:
            cmds.warning("All of the selected object have not been DETACHED")
        
    def helps(self):
        name="Help On DetachAttachSetDriven"
        helpTxt=""" 
        - Mainly use to move fix joint to another file 
        (* Fix joint must have SDK and parent to use this script)



        A) Detach 
        ==========
            - Record all transform
            - Record its parent and unparent it
            - Search for any set driven key(animCurve), record the "source" and disconnect/reconnect it
                (* SDK will run through all the children)   

        B) Attach
        ============
            - Parent back
            - Set back transformation
            - Connect back any set driven key(animCurve)
                (* SDK will run through all the children)   
            
        """
        self.helpBoxClass.helpBox1(name, helpTxt)    
       
    def reloadSub(self):
        DetAttSDK()   
        
                     
if __name__=='__main__':
    DetAttSDK() 