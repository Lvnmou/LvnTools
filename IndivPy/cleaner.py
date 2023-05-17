import maya.cmds as cmds
import maya.mel as mel
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox


class Cleaner(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()        
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):
        try:
            cmds.deleteUI("clean")
        except:
            pass          
        cmds.window("clean", mb=1)
        cmds.window("clean", t="Cleaner", e=1, s=1, wh=(330,335))   
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Cleaner", c=lambda x: self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Cleaner", c=lambda x: self.reloadSub())     
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Select")
        form1= cmds.formLayout(nd=100, p=column1)
        b101= cmds.button(l="Tri", c=lambda x: self.meshCleanup(1, "TRI")) 
        b102= cmds.button(l="NGon", c=lambda x: self.meshCleanup(2, "NGON"))    
        b103= cmds.button(l="Concave", c=lambda x: self.meshCleanup(3, "CONCAVE"))    
        b104= cmds.button(l="Nonmanifold", c=lambda x: self.meshCleanup(4, "NON-MANIFOLD"))
        b105= cmds.button(l="No Shader Objects", c=lambda x: self.noShad())
        b106= cmds.button(l="cMuscle", c=lambda x: self.cMus())
        b107= cmds.button(l="Same Name Objects", c=lambda x: self.sameName("transform"))
        b108= cmds.button(l="Same Name Shapes", c=lambda x: self.sameName("shape"))        
        b109= cmds.button(l="All Children", c=lambda x: self.sChildren(1))
        b110= cmds.button(l="Children", c=lambda x: self.sChildren(2))
        self.txtSear= cmds.textFieldGrp(l="Search :", tx="_L", adj=2, cw2=(45,10))
        self.txtRepl= cmds.textFieldGrp(l="Replace :", tx="_R", adj=2, cw2=(50,10))   
        b111= cmds.button(l="Left / Right", c=lambda x: self.leftRight(1))
        b112= cmds.button(l="Left + Right", c=lambda x: self.leftRight(2))  
        cmds.formLayout(form1, e=1,
                            af=[(b101, "top", 0),
                                (b102, "top", 0),
                                (b103, "top", 0),
                                (b104, "top", 0),
                                (b105, "top", 26),
                                (b106, "top", 26),
                                (b107, "top", 52),
                                (b108, "top", 52),
                                (b109, "top", 78),
                                (b110, "top", 78),
                                (self.txtSear, "top", 114),
                                (self.txtRepl, "top", 114),
                                (b111, "top", 140),
                                (b112, "top", 140)],
                            ap=[(b101, "left", 0, 0),
                                (b101, "right", 0, 24),
                                (b102, "left", 0, 25),
                                (b102, "right", 0, 50),
                                (b103, "left", 0, 51),
                                (b103, "right", 0, 74),
                                (b104, "left", 0, 75),
                                (b104, "right", 0, 100),
                                (b105, "left", 0, 0),
                                (b105, "right", 0, 50),
                                (b106, "left", 0, 51),
                                (b106, "right", 0, 100),
                                (b107, "left", 0, 0),
                                (b107, "right", 0, 50),
                                (b108, "left", 0, 51),
                                (b108, "right", 0, 100),
                                (b109, "left", 0, 0),
                                (b109, "right", 0, 50),
                                (b110, "left", 0, 51),
                                (b110, "right", 0, 100),
                                (self.txtSear, "left", 0, 0),
                                (self.txtSear, "right", 0, 50),
                                (self.txtRepl, "left", 0, 51),
                                (self.txtRepl, "right", 0, 100),
                                (b111, "left", 0, 0),
                                (b111, "right", 0, 50),
                                (b112, "left", 0, 51),
                                (b112, "right", 0, 100)]) 
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column2= self.uiStuffClass.sepBoxSub("Delete")
        form2= cmds.formLayout(nd=100, p=column2)            
        b201= cmds.button(l="Unused Expression", c=lambda x: self.delType("expression", "UNUSED EXPRESSION",1))
        b202= cmds.button(l="All Expression", c=lambda x: self.delType("expression", "EXPRESSION",2))        
        b203= cmds.button(l="Unused Constraint", c=lambda x: self.delType("constraint","UNUSED CONSTRAINT",1))  
        b204= cmds.button(l="All Constraint", c=lambda x: self.delType("constraint","CONSTRAINT",2))  
        b205= cmds.button(l="Namespace (except reference)", c=lambda x: self.delAllNamespace())            
        b206= cmds.button(l="Unknown Nodes", c=lambda x: self.delUnknownNodes())  
        b207= cmds.button(l="Unknown Plugin", c=lambda x: self.delUnknownPlugin())  
        b208= cmds.button(l="Unused Nodes", c=lambda x: self.delUnusedN())
        b209= cmds.button(l="Unused Orig Shape", c=lambda x: self.delType("mesh","UNUSED ORIG SHAPE",3)) 
        b210= cmds.button(l="All Unused Skin Influence", c=lambda x: self.removeAllUnusedSkinInf())       
        b211= cmds.button(l="All BindPose (DagPose)", c=lambda x: self.delType("dagPose","BINDPOSE(DagPose)",2))       
        cmds.formLayout(form2, e=1,
                            af=[(b201, "top", 0),
                                (b202, "top", 0),
                                (b203, "top", 26),
                                (b204, "top", 26),
                                (b205, "top", 52),
                                (b206, "top", 78),
                                (b207, "top", 104),
                                (b208, "top", 130),
                                (b209, "top", 156),
                                (b210, "top", 182),
                                (b211, "top", 208)],
                            ap=[(b201, "left", 0, 0),
                                (b201, "right", 0, 50),
                                (b202, "left", 0, 51),
                                (b202, "right", 0, 100),
                                (b203, "left", 0, 0),
                                (b203, "right", 0, 50),
                                (b204, "left", 0, 51),
                                (b204, "right", 0, 100),
                                (b205, "left", 0, 0),
                                (b205, "right", 0, 100),
                                (b206, "left", 0, 0),
                                (b206, "right", 0, 100),
                                (b207, "left", 0, 0),
                                (b207, "right", 0, 100),  
                                (b208, "left", 0, 0),
                                (b208, "right", 0, 100),
                                (b209, "left", 0, 0),
                                (b209, "right", 0, 100),
                                (b210, "left", 0, 0),
                                (b210, "right", 0, 100),
                                (b211, "left", 0, 0),
                                (b211, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)     
        column3= self.uiStuffClass.sepBoxSub("Hide/Show")
        form3= cmds.formLayout(nd=100, p=column3)                            
        b301= cmds.button(l="Hide All Joint", c=lambda x: self.hideShowAllJnt(2)) 
        b302= cmds.button(l="Show All Joint", c=lambda x: self.hideShowAllJnt(0))    
        b303= cmds.button(l="Hide Object All Shape", c=lambda x: self.hideShowObjShapeIhi(0))  
        b304= cmds.button(l="Show Object All Shape", c=lambda x: self.hideShowObjShapeIhi(1)) 
        b305= cmds.button(l="*Hide Object All History", c=lambda x: self.hideObjHis(1))
        b306= cmds.button(l="*Show Object All History", c=lambda x: self.showObjHis())
        b307= cmds.button(l="*Hide Object Input History", c=lambda x: self.hideObjHis(2)) 
        b308= cmds.button(l="*Hide Object Output History", c=lambda x: self.hideObjHis(3)) 
        b309= cmds.button(l="*Hide Object Selected History", c=lambda x: self.hideSelHis())
        cmds.formLayout(form3, e=1,
                            af=[(b301, "top", 0),
                                (b302, "top", 0),
                                (b303, "top", 26),
                                (b304, "top", 26),
                                (b305, "top", 66),
                                (b306, "top", 66),
                                (b307, "top", 92),
                                (b308, "top", 118),
                                (b309, "top", 144)],
                            ap=[(b301, "left", 0, 0),
                                (b301, "right", 0, 50),
                                (b302, "left", 0, 51),
                                (b302, "right", 0, 100),
                                (b303, "left", 0, 0),
                                (b303, "right", 0, 50),
                                (b304, "left", 0, 51),
                                (b304, "right", 0, 100),
                                (b305, "left", 0, 0),
                                (b305, "right", 0, 50),
                                (b306, "left", 0, 51),
                                (b306, "right", 0, 100),
                                (b307, "left", 0, 0),
                                (b307, "right", 0, 100),
                                (b308, "left", 0, 0),
                                (b308, "right", 0, 100),
                                (b309, "left", 0, 0),
                                (b309, "right", 0, 100)]) 
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4) 
        column4= self.uiStuffClass.sepBoxSub("Lock/Unlock")
        form4= cmds.formLayout(nd=100, p=column4)
        b401= cmds.button(l="Lock Selected Node", c=lambda x: self.lockUnlockObjN(1)) 
        b402= cmds.button(l="Unlock Selected Node", c=lambda x: self.lockUnlockObjN(0))   
        b403= cmds.button(l="Unlock All Node", c=lambda x: self.unlockAllN()) 
        b404= cmds.button(l="Lock All Mesh", c=lambda x: self.lockUnlockAllMesh(1,2)) 
        b405= cmds.button(l="Unlock All Mesh", c=lambda x: self.lockUnlockAllMesh(0,0))   
        b406= cmds.button(l="Lock Select Mesh", c=lambda x: self.lockSelMesh()) 
        cmds.formLayout(form4, e=1,
                              af=[(b401, "top", 0),
                                  (b402, "top", 0),
                                  (b403, "top", 26),
                                  (b404, "top", 52),
                                  (b405, "top", 52),
                                  (b406, "top", 78)],
                              ap=[(b401, "left", 0, 0),
                                  (b401, "right", 0, 50),
                                  (b402, "left", 0, 51),
                                  (b402, "right", 0, 100),
                                  (b403, "left", 0, 0),
                                  (b403, "right", 0, 100),
                                  (b404, "left", 0, 0),
                                  (b404, "right", 0, 50),
                                  (b405, "left", 0, 51),
                                  (b405, "right", 0, 100),
                                  (b406, "left", 0, 0),
                                  (b406, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)  
        column5= self.uiStuffClass.sepBoxSub("Fix")
        form5= cmds.formLayout(nd=100, p=column5)
        b501= cmds.button(l="Reset Default Camera", c=lambda x: self.resetCam(1))
        b502= cmds.button(l="Smart Guess Camera", c=lambda x: self.resetCam(2))
        b503= cmds.button(l="Fix Transform Override Color", c=lambda x: self.fixTranOver())
        b504= cmds.button(l="Fix Black Color Mesh (Delete All Color Set)", c=lambda x: self.fixBlackColMesh())
        cmds.formLayout(form5, e=1,
                              af=[(b501, "top", 0),
                                  (b502, "top", 0),
                                  (b503, "top", 26),
                                  (b504, "top", 52)],
                              ap=[(b501, "left", 0, 0),
                                  (b501, "right", 0, 50),
                                  (b502, "left", 0, 51),
                                  (b502, "right", 0, 100),
                                  (b503, "left", 0, 0),
                                  (b503, "right", 0, 100),
                                  (b504, "left", 0, 0),
                                  (b504, "right", 0, 100)])
        cmds.setFocus(cmds.text(l="")) 
        cmds.showWindow("clean")

    def meshCleanup(self, meth, types):
        shp= cmds.ls(typ="mesh")   
        obj=[]
        for item in shp:
            par= cmds.listRelatives(item, ap=1, pa=1)
            if par not in obj:
                obj.append(par[0])
        cmds.select(obj)        
        if meth==1:
            cmds.polySelectConstraint(m=3, t=8, sz=1)
        elif meth==2:
            cmds.polySelectConstraint(m=3, t=8, sz=3)
        elif meth==3:
            cmds.polySelectConstraint(m=3, t=8, c=1)
        else:
            cmds.polySelectConstraint(m=3, t=1, nm=1)

        #Need turn off       
        cmds.polySelectConstraint(dis=1)
        tarShp= cmds.ls(sl=1)
        if tarShp:
            self.uiStuffClass.loadingBar(1, len(tarShp)+1)
            tar=[]
            for stuff in tarShp:
                self.uiStuffClass.loadingBar(2)
                if stuff.split(".")[0] not in tar:
                    tar.append(stuff.split(".")[0])        
            if meth==1 or meth==2 or meth==3:
                cmds.selectType(fc=1)
            elif meth==4:
                cmds.selectType(v=1)
            cmds.hilite(tar)
            cmds.selectMode(co=1) 
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3, sel=tarShp)
        else:
            cmds.warning("Everything is clean, there is no <%s>"%types) 

    def noShad(self):
        obj= cmds.ls(typ="mesh")
        tempObj, sh, newObj, tar=[], [], [], []
        for item in obj:
            if "Orig" not in item:
                sh.append(item)                     
        for stuff in sh:
            try:   
                shade1= cmds.listConnections(stuff, type="shadingEngine", scn=1)
                if shade1:
                    ss= cmds.listConnections("%s.surfaceShader"%shade1[0], s=1, d=0, scn=1)  
                    if ss==None:
                        tempObj.append(stuff)  
                else:
                    tempObj.append(stuff)
            except:
                tempObj.append(stuff)
        #Some object didnt delete history, so recheck again using the shape node's transform     
        if tempObj:
            for stuff  in tempObj:
                par= cmds.listRelatives(stuff, p=1, pa=1)
                if par not in newObj:
                    newObj.append(par[0])  
            self.uiStuffClass.loadingBar(1, len(newObj)+1)     
            for thing in newObj:  
                dagObj= cmds.ls(thing, dag=1, s=1)  
                test=[]
                for allSh in dagObj:  
                    shade1= cmds.listConnections(allSh, type="shadingEngine", scn=1)
                    if shade1:
                        ss= cmds.listConnections("%s.surfaceShader"%shade1[0], s=1, d=0, scn=1)  
                        if ss==None:
                            tar.append(thing)                        
                        else:
                            test=1    
                if test==[]:
                    tar.append(thing)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3, sel=tar)
        if tar==[]:           
            cmds.warning("Everyhing is clean, there is no object with <NO SHADER>") 

    def cMus(self):
        cMus= cmds.ls(typ="cMuscleSpline")
        allcMus=[]
        if cMus:
            self.uiStuffClass.loadingBar(1, len(cMus)+1) 
            for item in cMus:
                par= cmds.listRelatives(item, p=1)
                if par:
                    allcMus.append(par[0])
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3, sel=allcMus)
        else:
            cmds.warning("There is no CMUSCLE in the scene")
        
    def sameName(self, types): 
        sno= {}
        test1= 1
        for item in cmds.ls(l=1, typ=types):
            if ":" in item:
                test1=[]
                break
        if test1:
            self.uiStuffClass.loadingBar(1, len(cmds.ls(typ=types))) 
            for item in cmds.ls(typ=types):
                if "|" in item:
                    dupName= item.split("|")[-1] 
                    if len(cmds.ls(dupName, typ=types))>1: 
                        if dupName not in sno:                       
                            sno[dupName]= 1
                        else:
                            sno[dupName]= sno[dupName] + 1  
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)
            if sno:
                dupItem= list(sno.keys())
                dupNum= list(sno.values())
                finalPrint=[]
                for stuff in dupItem:
                    finalPrint.append("%s - %s"%(sno[stuff], stuff))
                conti= self.dialogClass.printingDialog(finalPrint, "< %s > Names to rename\n< %s > Duplicated %s"%(len(sno),sum(dupNum),types))
                if conti: 
                    newTar=[]
                    for thing in dupItem: 
                        tar= cmds.ls(thing, typ=types)
                        for x, dup in enumerate(reversed(sorted(tar))):
                            newName= cmds.rename(dup, dup.split("|")[-1]+"_new%s"%(x+1))
                            newTar.append(newName)
                    cmds.select(newTar)
                else:
                    allTar= cmds.ls(dupItem, typ=types)
                    cmds.select(allTar)
            else:
                cmds.warning("There is no <%s> with same name"%types)
        else:
            cmds.warning("One of the object in the scene have <NAMESPACE>. Please remove it before running <SAME NAME>")

    def sChildren(self, meth):
        obj= cmds.ls(sl=1)
        tar= []
        if meth==1:
            chd= cmds.listRelatives(obj, ad=1, pa=1, typ="transform")
        else:    
            chd= cmds.listRelatives(obj, c=1, pa=1, typ="transform")
        if chd:
            self.uiStuffClass.loadingBar(1, len(chd)) 
            for item in chd:  
                tar.append(item)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3, sel=tar+obj)
        else:
            cmds.warning("Selected object don't not have children") 

    def leftRight(self, meth):
        sear= cmds.textFieldGrp(self.txtSear, q=1, tx=1) 
        repl= cmds.textFieldGrp(self.txtRepl, q=1, tx=1) 
        obj= cmds.ls(sl=1)
        tar1, tar2, leftOutTar1, leftOutTar2= [], [], [], []
        test1, test2= 1,1
        self.uiStuffClass.loadingBar(1, len(obj)+1) 
        for item in obj:
            if item.replace(sear, repl)!=item:
                if cmds.objExists(item.replace(sear, repl)):
                    tar1.append(item.replace(sear, repl))
                else:
                    test1= []
                    leftOutTar1.append(item)
            else:
                test1=[]
                leftOutTar1.append(item)
            self.uiStuffClass.loadingBar(2)
        if test1==[]:
            for item in obj:
                if item.replace(repl, sear)!=item:
                    if cmds.objExists(item.replace(repl, sear)):
                        tar2.append(item.replace(repl, sear))
                    else:
                        test2= []
                        leftOutTar2.append(item)
                else:
                    test2=[]
                    leftOutTar2.append(item)
        leftOutTar= leftOutTar1 + leftOutTar2
        self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3)
        if test1:
            if meth==1:
                cmds.select(tar1)
            else:
                cmds.select(tar1, obj)
        elif test2:
            if meth==1:
                cmds.select(tar2)
            else:
                cmds.select(tar2, obj)
        else: 
            #But for now the mixing one dun have warning dialog... hard to do
            if len(obj)!=len(tar1)+len(tar2):
                #When Search Replace wrong
                if tar1==[] and tar2==[]:
                    conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(obj, sear, repl)
                #When mixed of got opposite and no opposite  
                else:
                    if meth==1:
                        if tar1==[] and tar2:
                            cmds.select(leftOutTar2+tar2, r=1)
                        elif tar2==[]and tar1:
                            cmds.select(leftOutTar1+tar1, r=1)
                        else:
                            cmds.select(tar1+tar2, add=1)
                    else:
                        cmds.select(tar1+tar2, add=1)
            #When mixed of got opposite and no opposite + some selected LR  
            else:
                if meth==1:
                    cmds.select(list(set(tar1+tar2).difference(leftOutTar)), list(set(tar1+tar2).intersection(leftOutTar)))
                else:
                    cmds.select(tar1, tar2, leftOutTar)

    def delType(self, type, name, meth):
        obj= cmds.ls(typ=type)
        unused= []
        if obj:
            #Delete all
            if meth==2:
                unused= obj
            
            #Delete unused
            else:
                for item in obj:
                    if meth==1:
                        test= cmds.listConnections(item, d=1, s=0, scn=1)
                        if test==None:
                            unused.append(item) 
                    if meth==3:
                        if "Orig" in item:
                            test= cmds.listConnections(item, d=1, s=0, scn=1, c=1, p=1)
                            if test:
                                #Forgotten what's this for
                                if test[1].split(".")[1]=="inMesh":
                                    unused.append(item)
                            else:
                                unused.append(item)
        if unused:
            self.uiStuffClass.loadingBar(1, 2)
            self.uiStuffClass.loadingBar(2)
            cmds.delete(unused)
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)
        else:
            cmds.warning("Everyhing is clean, there is no <%s> to delete"%name)    

    def delAllNamespace(self):
        ns= cmds.namespaceInfo(lon=1, r=1)
        refTest= cmds.ls(ro=1)
        skip=["UI", "shared"]
        deleted=[]
        if refTest:
            for item in reversed(ns):
                if item not in skip:
                    #To prevent delete reference's namespace
                    testObj= cmds.ls("*%s:*"%item, ro=1)
                    if testObj:
                        skip.append(item)
        for item in reversed(ns):
            if item not in skip:
                cmds.namespace(rm="%s"%item, mnr=1)
                deleted.append(item)

        if deleted==[]:
            cmds.warning("Everyhing is clean, there is no more <NAMESPACE> to delete except from reference editor (if any)")
        else:
            self.uiStuffClass.loadingBar(1, 1) 
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3) 

    def delUnknownPlugin(self):
        obj= cmds.unknownPlugin(q=1, l=1)
        if obj:
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                cmds.unknownPlugin(item, r=1)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)
        else:
            cmds.warning("Everyhing is clean, there is no <UNKNOWN PLUGIN>")
    
    def delUnknownNodes(self):
        obj= cmds.ls(typ="unknown")
        if obj:
            self.uiStuffClass.loadingBar(1, 1) 
            self.uiStuffClass.loadingBar(2)
            cmds.delete(obj)
            self.uiStuffClass.loadingBar(3)        
        else:
            cmds.warning("Everyhing is clean, there is no <UNKNOWN NODE>")        

    def delUnusedN(self):    
        self.uiStuffClass.loadingBar(1, 2)
        self.uiStuffClass.loadingBar(2)
        #mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");') 
        num= mel.eval('MLdeleteUnused;')

        #maya20 will have issue cannot delete "standardSurface1"
        ver= cmds.about(v=1)
        if ver=="2020":
            #Weird thing, if there's no unused, will delete 2 times "standardSurface1"
            #If there's at least 1 unused, will delete 3 times "standardSurface1"
            #Heard there'll be a fix in the future
            if num==2:
                num=0
            elif num>3:
                num=num-3
    
        self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3)
        if num==0:
            cmds.warning("Everyhing is clean, there is no <Unused Node>") 

    def removeAllUnusedSkinInf(self):  
        self.uiStuffClass.loadingBar(1, 2)
        self.uiStuffClass.loadingBar(2)
        num= mel.eval('removeAllUnusedSkinInfs();')
        self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3)
        if num==0:
            cmds.warning("Everyhing is clean, there is no <Unused Skin Influence>") 

    def hideShowAllJnt(self, drawStyle):
        obj= cmds.ls(typ="joint")
        if obj:
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                cmds.setAttr("%s.drawStyle"%item, drawStyle)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)
        else:
            cmds.warning("There is no JOINT in the scene")
            
    def hideShowObjShapeIhi(self, hideShow):
        obj= cmds.ls(sl=1, tr=1)
        if obj:
            sh= cmds.listRelatives(obj, pa=1, typ="nurbsCurve")   
            if sh:
                self.uiStuffClass.loadingBar(1, len(sh))
                for item in sh:
                    cmds.setAttr("%s.ihi"%item, hideShow)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=obj)
            else:
                cmds.warning("Selected object does not have a shape node") 
        else:
            cmds.warning("Please select an object")    

    def hideObjHis(self, meth):
        obj= cmds.ls(sl=1)
        allHist, errObj= [],[]
        count= 0
        self.uiStuffClass.loadingBar(1, len(obj)+1)
        for item in obj:
            try:
                if meth==1:
                    hist= mel.eval('historyPopupFill( "%s", 0, 0 )'%item) + mel.eval('historyPopupFill( "%s", 1, 0 )'%item)
                elif meth==2:
                    hist= mel.eval('historyPopupFill( "%s", 0, 0 )'%item)
                elif meth==3:
                    hist= mel.eval('historyPopupFill( "%s", 1, 0 )'%item)
            #Weirdly enough some times even maya show input/output will have error, but if hide individually can bypass
            except:
                errObj.append(item)
                break
            if hist:  
                for subHist in hist.split(" "):
                    if subHist!="":
                        if subHist not in allHist:
                            allHist.append(subHist)  

                #This is to remove the first empty " "    
                if hist[0]==" ":
                    ans= hist[1:]
                else:
                    ans= hist[0]      
                if cmds.attributeQuery("hiddenHistory", node=item, ex=1)==0:
                    cmds.addAttr(item, ln="hiddenHistory", dt="string")
                    cmds.setAttr("%s.hiddenHistory"%item, ans, typ="string")
                else:
                    preHist= cmds.getAttr("%s.hiddenHistory"%item)
                    if preHist:
                        cmds.setAttr("%s.hiddenHistory"%item, "%s %s"%(preHist,ans), typ="string")
                    else:
                        count+=1
            else:
                count+=1
            self.uiStuffClass.loadingBar(2)
        if allHist:
            for allSubHist in allHist:
                cmds.setAttr("%s.ihi"%allSubHist, 0)
        self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3)
        if errObj:
            cmds.warning("<%s> have problem with history, try to hide the history 1 by 1 manually"%errObj[0])
        if count==len(obj):
            cmds.warning("Selected object's history is already hidden")

    def showObjHis(self):
        obj= cmds.ls(sl=1)
        test1= 1
        if obj:
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                if cmds.attributeQuery("hiddenHistory", node=item, ex=1):
                    test1= []
                    hist= cmds.getAttr("%s.hiddenHistory"%item)
                    for subHist in hist.split(" "):
                        cmds.setAttr("%s.ihi"%subHist, 2)
                    cmds.deleteAttr("%s.hiddenHistory"%item)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3, [], obj)
            if test1:
                cmds.warning("There is no hidden history to show (or unable to show because not hidden by this script)")
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def hideSelHis(self):
        his= cmds.ls(sl=1)
        obj= cmds.ls(sl=1, tr=1)
        if len(obj)==1:
            if his!=obj:
                self.uiStuffClass.loadingBar(1, len(his))
                if cmds.attributeQuery("hiddenHistory", node=obj[0], ex=1)==0:
                    cmds.addAttr(obj, ln="hiddenHistory", dt="string")
                for item in his:
                    if item!=obj[0]:
                        try:    
                            cmds.setAttr("%s.ihi"%item, 0)
                            preHist= cmds.getAttr("%s.hiddenHistory"%obj[0])
                            if preHist==None:
                                cmds.setAttr("%s.hiddenHistory"%obj[0], item, typ="string")
                            else:    
                                cmds.setAttr("%s.hiddenHistory"%obj[0], "%s %s"%(preHist,item), typ="string")
                        except:
                            pass
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, [], obj)
            else:
                cmds.warning("Please select an INPUT or OUTPUT node") 
        elif len(obj)>1:
            cmds.warning("Select only 1 object")  
        else:
            cmds.warning("Please select 1 object")   

    def lockUnlockObjN(self, lock):
        obj= cmds.ls(sl=1)
        if obj:
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                cmds.lockNode(item, l=lock)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)
        else:
            cmds.warning("Please select at least 1 object")

    def unlockAllN(self):
        obj= cmds.ls(dag=1, tr=1)
        if obj:
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                cmds.lockNode(item, l=0)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)

    def lockUnlockAllMesh(self, enabled, display):
        obj= cmds.ls(typ="mesh")
        if obj:
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                if "Orig" not in item:
                    cmds.setAttr("%s.overrideEnabled"%item, enabled)
                    cmds.setAttr("%s.overrideDisplayType"%item, display)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)
        else:
            cmds.warning("There is no MESH in the scene")            

    def lockSelMesh(self):    
        obj= cmds.ls(sl=1)
        test1= []
        if obj:
            for item in obj:
                sh= cmds.listRelatives(obj, pa=1, typ="mesh")
                if sh:
                    test1=1 
            if test1:
                self.uiStuffClass.loadingBar(1, len(obj))
                for item in obj:
                    sh= cmds.listRelatives(obj, pa=1, typ="mesh")
                    if sh:    
                        for stuff in sh:    
                            if "Orig" not in stuff:
                                cmds.setAttr("%s.overrideEnabled"%stuff, 1)
                                cmds.setAttr("%s.overrideDisplayType"%stuff, 2)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("Selected object is not a mesh")
        else:
            cmds.warning("Please select at least 1 mesh")               

    def resetCam(self, meth):
        #Use "Try Except" because the camera might not exist and attr might lock
        cam= ["persp", "top", "front", "side", "left", "back", "bottom"]
        attrs=["tx","ty","tz","rx","ry","rz"]
        camAttr= ["horizontalFilmAperture","verticalFilmAperture","focalLength","lensSqueezeRatio","fStop","focusDistance","shutterAngle","centerOfInterest"]
        exAttr1=["orthographicWidth"]
        exAttr2=["centerOfInterest"]
        camVal= [1.417, 0.945, 35, 1, 5.6, 5, 144, 100]
        allGood=1
        for item in cam:
            for test in (attrs+camAttr):
                try:
                    res= cmds.getAttr("%s.%s"%(item,test), l=1)
                    if res==1:
                        allGood=[]
                except:
                    pass                 
        if allGood:    
            self.uiStuffClass.loadingBar(1, len(cam))
            for item in cam:                  
                for con1, con2 in zip(camAttr,camVal):
                    try:
                        cmds.setAttr("%s.%s"%(item,con1), con2)
                    except:
                        pass 
                allAttr= attrs + exAttr1
                if item=="persp":
                    attrsVal=[28,21,28,-28,45,0,45]  
                    allAttr= attrs + exAttr2        
                elif item=="top":
                    attrsVal=[0,100,0,-90,0,0,30]  
                elif item=="front":
                    attrsVal=[0,0,100,0,0,0,30]                     
                elif item=="side":
                    attrsVal=[100,0,0,0,90,0,30]                         
                elif item=="left":
                    attrsVal=[-100,0,0,0,-90,0,30]                   
                elif item=="back":
                    attrsVal=[0,0,-100,0,180,0,30]                   
                elif item=="bottom":
                    attrsVal=[0,-100,0,90,0,0,30] 
                for stuff, thing in zip(allAttr, attrsVal):
                    try:
                        cmds.setAttr("%s.%s"%(item, stuff), thing)
                    except:
                        pass 
                if item=="persp":
                    try:
                        cmds.setAttr("%s.orthographic"%item, 0)
                    except:
                        pass 
                else:
                    try:
                        cmds.setAttr("%s.orthographic"%item, 1)
                    except:
                        pass   
                try:
                    cmds.viewClipPlane(item, ncp=0.1, fcp=10000)
                except:
                    pass 
                if meth==2:
                    try:              
                        cmds.viewFit(item, all=1)
                        cmds.viewClipPlane(item, acp=1)
                        cp= cmds.viewClipPlane(item, ncp=1, fcp=1, q=1)
                        if cp[1]<10000:
                            cmds.viewClipPlane(item, ncp=0.1, fcp=10000)
                        else:
                            cmds.viewClipPlane(item, ncp=1, fcp=cp[1]*10)
                        #Guess orthographic view (Need to untick and viewFit first)
                        if cmds.getAttr("%s.orthographic"%item)==1:
                            cmds.setAttr("%s.orthographic"%item, 0)
                            cmds.viewFit(item, all=1)
                            cmds.setAttr("%s.orthographic"%item, 1)
                    except:
                        pass 
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)                        
        else:
            cmds.warning("There is locked attribute in one of the camera")

    def fixTranOver(self):
        obj= cmds.ls(dag=1, tr=1)
        err1, err2= [],[]
        conti= 1
        self.uiStuffClass.loadingBar(1, len(obj))
        for item in obj:
            if cmds.getAttr("%s.overrideEnabled"%item)==1:
                #test is it connected to layer, if it is the ignore
                test1= cmds.listConnections("%s.drawOverride"%item, s=1, scn=1)
                if test1: 
                    if cmds.objectType(test1)!="displayLayer":
                        err1.append(item)
                else:
                    err1.append(item)
                      
            self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3)     
        if err1:
            for stuff in err1:
                sh= cmds.listRelatives(stuff, pa=1, typ="nurbsCurve")
                if sh==None:
                    err2.append(stuff)
            if err2:
                conti= self.dialogClass.printingDialog(err2, "< %s > Object with no shape have enabled overrides"%len(err2))
            if conti: 
                self.uiStuffClass.loadingBar(1, len(err1))
                for stuff in err1:
                    sh= cmds.listRelatives(stuff, pa=1, typ="nurbsCurve")
                    col= cmds.getAttr("%s.overrideColor"%stuff)
                    disp= cmds.getAttr("%s.overrideDisplayType"%stuff)

                    #if its empty transform, empty it
                    cmds.setAttr("%s.overrideEnabled"%stuff, 0)

                    #if its ctrl, then change enabled override, display, color
                    if sh:
                        if col!=0:
                            for thing in sh:
                                cmds.setAttr("%s.overrideEnabled"%thing, 1)
                                cmds.setAttr("%s.overrideDisplayType"%thing, disp)
                                cmds.setAttr("%s.overrideColor"%thing, col)                          
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=err1)                      
        else:
            cmds.warning("Everything is clean, there is no transform object that have enabled overrides")

    def fixBlackColMesh(self):
        mesh= cmds.ls(g=1)
        test1= []
        if mesh:
            self.uiStuffClass.loadingBar(1, len(mesh))
            for item in mesh:
                cs= cmds.polyColorSet(item, acs=1, q=1)
                if cs:
                    #untick the display colors
                    cmds.setAttr("%s.displayColors"%item, 0)

                    #delete all the color sets
                    for stuff in cs:
                        cmds.polyColorSet(item, cs="%s"%stuff, d=1)
                    test1= 1
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)
        if test1==[]:
            cmds.warning("Everyhing is clean, there is no <Color Set>") 

    def helps(self):
        name="Help On Cleaner"
        helpTxt="""
        - All sorts of file cleanup



        < Select >
        =============
            1) Mesh Cleanup
            -----------------
                1. Tri
                    - Select 3-sided faces 

                2. NGon
                    - Select faces more than 4-sided

                3. Concave
                    - Select faces that are concave

                4. Nonmanifold
                    - Select nonmanifold parts
                    (*Google for more info. Sharing vertex / edge / face)
                

            2) No Shader Objects
            ---------------------
                - Select object that does not have any shader (transparent)
                    (* Might take longer for bigger scene) 

            3) cMuscle
            ----------
                - Select cMuscle 
                    (* if cMuscle is not hidden, will cause problem to camera when press F)

            4) Same Name
            -------------
                - Select same name objects
                - Select same name shapes

                (* Renaming is optional)

            5) Children
            -------------
                - Select all children 
                - Select instant children (one level below)       

            6) Left Right 
            --------------
                - Using <Search> textfield

                - Select Left OR Right side (* Workable for both sides without changing sides)
                - Select Left AND Right side


        < Delete >
        =============
            1) Expression
            ---------------
                - In "Expression Editor"

                - Unused expression that's not doing anything or any object in the scene (left over from imported files)
                - All expression (even is connected) 


            2) Constraint
            --------------
                - Unused constraint (Constraint that doesn't have connections, exist when duplicate a constrained object)
                - All constraint in the scene (even is connected)  

            3) Namespace
            --------------
                - All namespace in "Namespace Editor" except for reference objects

            4) Unknown Nodes
            ----------------------   
                - All Unknown Nodes

            5) Unknown Plugins
            ---------------------
                (* This Will boost file opening speed if there's any)        

            6) Unused Nodes
            ------------------
                (* Same as the hypergraph function)
  
            7) Unused Orig Shape
            --------------------------
                - those that don't have connections
                (* Exist when duplicate a blendshape or skinned object because they already have orig shape)

            8) All Unused Skin Influence
            --------------------------------
                (* Same as Optimize file size menu)

            9) All BindPose (DagPose)
            ----------------------------
                - Delete Bindpose (DagPose is the type)
                (* When skin an object, it will create a Bindpose)



        < Hide / Show >
        ================  
            1) Joint
            ---------
                - Hide all the joint
                - Show all the joint
                (* Actually just change draw type) 

            2) Shape Node
            --------------
                - Hide / Show all the shape node of the selected object
                (* Using setAttr ".ihi")

            3) History
            --------------
                - All unstable yet. That's why *

                1. Hide Object All History
                    - Hide all the Input/Output history of the selected object

                2. Hide Object Input History
                    - Hide < INPUT > history of the selected object

                3. Hide Object Output History
                    - Hide < OUTPUT > history of the selected object

                4. Hide Object Selected History
                    - Hide a selected input/output from an object
                    (* eg. select pCube1's skincluster/blendshape and hide it) 


        < Lock / Unlock >
        =============== 
            1) Node  
            --------
                1. Lock Selected Node
                    - Lock the node for selected object to prevent deleting
                    (* You can't delete a lock node)

                2. Unlock Selected Node
                    - Unlock the node for selected object to enable deleting

                3. Unlock All Node
                    - Unlock all node in the scene

            2) Mesh       
            ---------
                1. Lock All Mesh
                    - Lock all mesh to prevent from selecting
                    (* Just change the shape node to reference)

                2. Unlock All Mesh
                    - Unlock all mesh to enable selecting
                    (* Just change the shape node to normal)

                3. Lock Selected Mesh
                    - Lock selected mesh to prevent from selecting


        < Fix >
        =============
            1) Camera
            ----------
                1. Reset Default Camera
                    - Reset default camera to default
                    (* Doesn't include custom create camera) 

                2. Smart Guess Camera
                    - Estimate all object's position in scene    

                (* Modify position, clip plane, orthographic)

            2) Fix Transform Override Color
            ---------------------------------
                - Detect which transform node that enabled override. Then switch the color to the shape node instead, if any
                (* Situation when some people change the color of the transform node instead of the shape node)

            3) Fix Black Color Mesh (Delete All Color Set)
            --------------------------------------------------------
                - Using maya17 sculpt freeze tool, assign color to vertex which maya15 doesnt have it so couldn't detect the color/layer
                - under "meshComponenetDisplay" untick "Display Colors" to not show the color but deleting colorset under <color>, <color editor> will reduce file size. 

        """
        self.helpBoxClass.helpBox1(name, helpTxt)

    def reloadSub(self):
        Cleaner()  
        
        
if __name__=='__main__':
    Cleaner() 
                        




