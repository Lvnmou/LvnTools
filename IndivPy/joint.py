import maya.cmds as cmds
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox


class Joint(object):
    def __init__(self, *args):
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):       
        try: 
            cmds.deleteUI("jnts") 
        except:
            pass    
        cmds.window("jnts", mb=1)              
        cmds.window("jnts", t="Joint", s=1, e=1, wh=(365,515))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Joint", c=lambda x:self.helps())        
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Joint", c=lambda x:self.reloadSub())  
        self.uiStuffClass.sepBoxMain()
        column11= self.uiStuffClass.sepBoxSub("Edit", 0)
        form11= cmds.formLayout(nd=100, p=column11)
        txt101= cmds.text(l="Select TARGET", fn="smallObliqueLabelFont", en=0)
        txt102= cmds.text(l="Select PARENT", fn="smallObliqueLabelFont", en=0)
        b101= cmds.button(l="Zero Joint Orient", c=lambda x:self.zeroJointOrient()) 
        b102= cmds.button(l="Duplicate Joint Children Only",c=lambda x:self.dupJointChildOnly())
        txt103= cmds.text(l="Select PARENT then CHILD", fn="smallObliqueLabelFont", en=0)
        b103= cmds.button(l="Become Chain", c=lambda x:self.becomeChain()) 
        b104= cmds.button(l="Duplicate Become Chain", c=lambda x:self.dupBecomeChain(cmds.ls(sl=1, l=1))) 
        txt104= cmds.text(l="Select PARENT", fn="smallObliqueLabelFont", en=0)
        b105= cmds.button(l="Reverse Selected Chain", c=lambda x:self.reverseWholeChain()) 
        txt105= cmds.text(l="Select NOTHING", fn="smallObliqueLabelFont", en=0)
        b106= cmds.button(l="Joint Size (display)",c=lambda x:self.setJointSize())
        self.slider11= cmds.floatSliderGrp(f=1, cw2=(50,20), min=0.01, max=1, fmx=100, v=0.1, pre=2) 
        b107= cmds.button(l="All Joint Radius",c=lambda x:self.setJointRad())
        self.slider12= cmds.floatSliderGrp(f=1, cw2=(50,20), min=0.01, max=1, fmx=100, v=0.5, pre=2) 
        cmds.formLayout(form11, e=1,
                              af=[(txt101, "top", 0),
                                  (txt102, "top", 0),
                                  (b101, "top", 16),
                                  (b102, "top", 16),
                                  (txt103, "top", 52),
                                  (b103, "top", 68),
                                  (b104, "top", 68),
                                  (txt104, "top", 104),
                                  (b105, "top", 120),                                  
                                  (txt105, "top", 156),
                                  (b106, "top", 172),
                                  (self.slider11, "top", 172),
                                  (b107, "top", 198),
                                  (self.slider12, "top", 198)], 
                              ap=[(txt101, "left", 0, 0),
                                  (txt101, "right", 0, 50),
                                  (txt102, "left", 0, 51),
                                  (txt102, "right", 0, 100),
                                  (b101, "left", 0, 0),
                                  (b101, "right", 0, 50),
                                  (b102, "left", 0, 51),
                                  (b102, "right", 0, 100),
                                  (txt103, "left", 0, 0),
                                  (txt103, "right", 0, 100),
                                  (b103, "left", 0, 0),
                                  (b103, "right", 0, 50),
                                  (b104, "left", 0, 51),
                                  (b104, "right", 0, 100),
                                  (txt104, "left", 0, 0),
                                  (txt104, "right", 0, 100),
                                  (b105, "left", 0, 0),
                                  (b105, "right", 0, 100),
                                  (txt105, "left", 0, 0),
                                  (txt105, "right", 0, 100),
                                  (b106, "left", 0, 0),
                                  (b106, "right", 0, 40),
                                  (self.slider11, "left", 0, 41),
                                  (self.slider11, "right", 0, 100),
                                  (b107, "left", 0, 0),
                                  (b107, "right", 0, 40),
                                  (self.slider12, "left", 0, 41),
                                  (self.slider12, "right", 0, 100)]) 
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column21= self.uiStuffClass.sepBoxSub("Reorient")
        form21= cmds.formLayout(nd=100, p=column21)
        self.aimAx= cmds.optionMenuGrp(l="Aim Vector :", cw2=(60,10))
        cmds.menuItem(l="X")
        cmds.menuItem(l="Y")
        cmds.menuItem(l="Z")
        cmds.menuItem(l="-X")
        cmds.menuItem(l="-Y")
        cmds.menuItem(l="-Z")    
        self.upAx= cmds.optionMenuGrp(l="Up Vector :", cw2=(60,10))
        cmds.menuItem(l="X")
        cmds.menuItem(l="Y")
        cmds.menuItem(l="Z")
        cmds.menuItem(l="-X")
        cmds.menuItem(l="-Y")
        cmds.menuItem(l="-Z")
        cmds.optionMenuGrp(self.upAx, e=1, sl=2) 
        cmds.formLayout(form21, e=1,
                                af=[(self.aimAx, "top", 0),
                                    (self.upAx, "top", 26)],
                                ap=[(self.aimAx, "left", -50, 50),
                                    (self.aimAx, "right", 0, 100),
                                    (self.upAx, "left", -50, 50),
                                    (self.upAx, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        cmds.setParent("..")
        column22= self.uiStuffClass.sepBoxSub()   
        form22= cmds.formLayout(nd=100, p=column22)  
        txt201= cmds.text(l="Select SUBSELECTIONS / OBJECTS", fn="smallObliqueLabelFont", en=0)  
        b201= cmds.button(l="Create Center Locator (*Can Skip)", c=lambda x:self.loc(cmds.ls(sl=1, fl=1)))   
        txt202= cmds.text(l="Select 3:      AIM DIRECTION | TARGET | UP OBJECT", fn="smallObliqueLabelFont", en=0)  
        b202= cmds.button(l="Reorient Single Joint", c=lambda x:self.resj())
        cmds.formLayout(form22, e=1,
                                af=[(txt201, "top", 0),
                                    (b201, "top", 16),
                                    (txt202, "top", 56),
                                    (b202, "top", 72)],
                                ap=[(txt201, "left", 0, 0),
                                    (txt201, "right", 0, 100),
                                    (b201, "left", 0, 0),
                                    (b201, "right", 0, 100),
                                    (txt202, "left", 0, 0),
                                    (txt202, "right", 0, 100),
                                    (b202, "left", 0, 0),
                                    (b202, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column23= self.uiStuffClass.sepBoxSub()   
        form23= cmds.formLayout(nd=100, p=column23)
        self.txtTar= cmds.textFieldButtonGrp(l="Targets :", pht="<Grab highest in chain>", cw3=(50,100, 100), adj=2, bl="  Grab  ", bc=lambda :self.grab(self.txtTar))
        self.b211= cmds.button(l="Create Smart Up Object", en=0, c=lambda x:self.creaSm())
        self.txtUp= cmds.textFieldButtonGrp(l="Up Objs :", pht="<Grab highest in chain>", cw3=(50,100, 100), adj=2, bl="  Grab  ", bc=lambda :self.grab(self.txtUp))
        sep211= cmds.separator(h=5, st="in")  
        b212= cmds.button(l="Reorient Joint Chain", c=lambda x:self.rejc())
        b213= cmds.button(l="Delete Smart Up Object", c=lambda x:self.delSm())
        cmds.formLayout(form23, e=1,
                                af=[(self.txtTar, "top", 0),
                                    (self.b211, "top", 32),
                                    (self.txtUp, "top", 64),
                                    (sep211, "top", 98),
                                    (b212, "top", 114),
                                    (b213, "top", 140)],
                                ap=[(self.txtTar, "left", 0, 0),
                                    (self.txtTar, "right", 0, 100),
                                    (self.b211, "left", 0, 0),
                                    (self.b211, "right", 0, 100),
                                    (self.txtUp, "left", 0, 0),
                                    (self.txtUp, "right", 0, 100),
                                    (sep211, "left", 0, 0),
                                    (sep211, "right", 0, 100),
                                    (b212, "left", 0, 0),
                                    (b212, "right", 0, 100),
                                    (b213, "left", 0, 0),
                                    (b213, "right", 0, 100)])
        cmds.setFocus(cmds.text(l= ""))
        cmds.showWindow("jnts")
        
    def defi(self):
        opt=[1,2,3,4,5,6]
        val=[(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
        for item in zip(opt, val):
            for menuGrp in (self.aimAx, self.upAx):
                if cmds.optionMenuGrp(menuGrp, q=1, sl=1)==item[0]:
                    if menuGrp==self.aimAx:
                        self.aimV=item[1]  
                    else:
                        self.upV=item[1]           
        self.multiTar= cmds.textFieldButtonGrp(self.txtTar, q=1, tx=1) 
        self.multiUp= cmds.textFieldButtonGrp(self.txtUp, q=1, tx=1)   

    def grab(self, txt):
        obj= cmds.ls(sl=1, typ="joint")
        allJnt= []
        if obj:
            if len(obj)==1:
                allJnt.append(obj[0])
                allChd= cmds.listRelatives(obj, ad=1, pa=1, typ="joint") 
                if allChd:
                    for chd in reversed(allChd):
                        allJnt.append(chd)
                    cmds.textFieldButtonGrp(txt, e=1, tx=(", ".join(allJnt)))
                    if cmds.textFieldButtonGrp(self.txtTar, q=1, tx=1):
                        cmds.button(self.b211, e=1, en=1)  
                else:
                    cmds.warning("Selected object does not have any joint children")   
            else:
                cmds.warning("Please select only 1 JOINT CHAIN or grab the HIGHEST joint") 
        else:
            cmds.warning("Please select a JOINT CHAIN")

    def zeroJointOrient(self):
        obj= cmds.ls(sl=1)
        if obj:
            test1= 1
            for item in obj:
                if cmds.objectType(item)!="joint":
                    test1= []
            if test1:
                self.uiStuffClass.loadingBar(1, len(obj))
                for item in obj:
                    cmds.setAttr("%s.jointOrientX"%item, 0)
                    cmds.setAttr("%s.jointOrientY"%item, 0)
                    cmds.setAttr("%s.jointOrientZ"%item, 0)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)                    
            else:
                cmds.warning("One of the selected object is not a JOINT")
        else:
            cmds.warning("Please select at least 1 JOINT")            

    def dupJointChildOnly(self):
        obj= cmds.ls(sl=1)
        if obj:
            allObj=[]
            for item in obj:
                jnt= cmds.listRelatives(item, ad=1, pa=1, typ="joint")
                if jnt!=None:
                    allObj.append(item)
            if allObj:
                allDup=[]
                self.uiStuffClass.loadingBar(1, len(allObj))
                for tar in allObj:
                    dup= cmds.duplicate(tar, n="%s_newJChd"%tar.split("|")[-1])
                    chd= cmds.listRelatives(dup[0], ad=1, f=1, typ="transform")
                    if chd:
                        for allChd in reversed(sorted(chd)):
                            #Use try because when deleting some children will delete another linked object eg: lattice
                            try:
                                if cmds.objectType(allChd)=="transform":
                                    if cmds.listRelatives(allChd, ad=1, pa=1, typ="joint")==None:
                                        cmds.delete(allChd)
                                    else:
                                        par= cmds.listRelatives(allChd, p=1, pa=1)
                                        subChd= cmds.listRelatives(allChd, c=1, pa=1, typ="joint")
                                        if subChd==None:
                                            #This is if the joint have offsetGroup that create transform group
                                            subSubChd= cmds.listRelatives(allChd, c=1, pa=1, typ="transform")    
                                            cmds.parent(subSubChd, par)
                                            cmds.delete(allChd)
                                        else:
                                            cmds.parent(subChd, par)
                                            cmds.delete(allChd)
                                else:
                                    if cmds.objectType(allChd)!="joint":
                                        par= cmds.listRelatives(allChd, p=1, pa=1)
                                        subChd= cmds.listRelatives(allChd, c=1, pa=1, typ="joint")
                                        if subChd:
                                            cmds.parent(subChd, par)
                                        cmds.delete(allChd)
                            except:
                                pass
                    oldChd= cmds.listRelatives(dup[0], ad=1, pa=1)
                    for stuff in reversed(sorted(oldChd)):
                        cmds.rename(stuff, "%s_newJChd"%stuff.split("|")[-1])
                    if cmds.listRelatives(dup[0], p=1):
                        cmds.parent(dup[0], w=1)
                    allDup.append(dup[0])
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=dup[0])
            else:
                cmds.warning("There is no JOINT type children")
        else:
            cmds.warning("Please select at least 1 OBJECT")

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

    def becomeChain(self):
        obj= cmds.ls(sl=1, l=1)
        if len(obj)>1:
            self.uiStuffClass.loadingBar(1, len(obj)+1)
            conti= self.testScale(obj, "Joints")
            grp= cmds.group(em=1, n="becomeChain")
            if conti:
                #Because its just unparenting so need to sort to see which is the lowest in hierarchy to do that first
                for item in reversed(sorted(obj)):
                    cmds.parent(item, grp)
                    #Need to modify the name so that later can select (cannot use append because the order is different)
                    obj= ((", ").join(obj)).replace(item,"%s|%s"%(grp, item.split("|")[-1])).split(", ")
                    self.uiStuffClass.loadingBar(2)                

                #Reparent in order
                for x in range((len(obj)-1), 0, -1):
                    cmds.parent(obj[x], obj[x-1])
                cmds.parent(obj[0], w=1)
                cmds.delete(grp)
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel="|%s"%obj[0].split("|")[-1])  
        else:
            cmds.warning("Please select at least 2 OBJECT")

    def dupBecomeChain(self, obj, loading=1):
        tar= []
        if len(obj)>1:
            if loading:
                self.uiStuffClass.loadingBar(1, len(obj)+1)
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
                    if loading:    
                        self.uiStuffClass.loadingBar(2)

                #Reparent in order
                for x in range((len(tar)-1),0, -1):
                    cmds.parent(tar[x], tar[x-1])
                if loading:
                    self.uiStuffClass.loadingBar(2)
                    self.uiStuffClass.loadingBar(3, sel=tar[0])
                return tar    
        else:
            cmds.warning("Please select at least 2 OBJECT")

    def reverseWholeChain(self):
        obj= cmds.ls(sl=1)
        testChd= 1
        finalSel= [] 
        for item in obj:
            chd= cmds.listRelatives(item, ad=1, typ="transform", f=1)
            if chd==None:
                testChd=[]
                break

        if testChd:
            self.uiStuffClass.loadingBar(1, len(obj)+1)
            for item in obj:
                chd= cmds.listRelatives(item, ad=1, typ="transform", f=1)
                par= cmds.listRelatives(item, p=1, typ="transform", f=1)
                for x,thing in enumerate(chd):
                    if x==0:
                        if par:
                            prev= cmds.parent(thing, par)
                        else:
                            prev= cmds.parent(thing, w=1)   
                        finalSel.append(prev[0])             
                    else:
                        prev= cmds.parent(thing, prev)
                cmds.parent(item, prev)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(2)    
            self.uiStuffClass.loadingBar(3, sel=finalSel) 
        else:
            cmds.warning("One of the selected object doesn't have an immediate children")

    def setJointSize(self): 
        self.uiStuffClass.loadingBar(1, 2)
        self.uiStuffClass.loadingBar(2)
        js= cmds.floatSliderGrp(self.slider11, q=1, v=1) 
        cmds.jointDisplayScale(js)       
        self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3)

    def setJointRad(self):  
        jr= cmds.floatSliderGrp(self.slider12, q=1, v=1)  
        obj= cmds.ls(typ="joint")
        self.uiStuffClass.loadingBar(1, len(obj))
        for item in obj:
            lock= cmds.getAttr("%s.radius"%item, l=1)
            if lock==1:
                cmds.setAttr("%s.radius"%item, l=0)    
            cmds.setAttr("%s.radius"%item, jr)
            if lock==1:
                cmds.setAttr("%s.radius"%item, l=1) 
            self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3)     

    def loc(self, obj): 
        tar= cmds.spaceLocator(n="LvnReorient_loc")  
        if len((", ").join(obj).split(", "))>1:
            tempPivX, tempPivY, tempPivZ= [],[],[]
            for item in (", ").join(obj).split(", "):
                tempPiv= self.locPiv([item])
                for x,stuff in enumerate([tempPivX, tempPivY, tempPivZ]):
                    stuff.append(tempPiv[x])
            piv= [round((min(tempPivX)+max(tempPivX))/2, 3), round((min(tempPivY)+max(tempPivY))/2, 3), round((min(tempPivZ)+max(tempPivZ))/2, 3)]           
        else:
            piv= self.locPiv(obj)         
        cmds.xform(tar, t=(piv[0],piv[1],piv[2]), ws=1)
        return tar

    def locPiv(self, obj):
        if cmds.objectType(obj[0])=="transform" or cmds.objectType(obj[0])=="joint":                                   
            piv= cmds.xform(obj[0], q=1, rp=1, ws=1)
        elif cmds.objectType(obj[0])=="mesh" or cmds.objectType(obj[0])=="nurbsCurve" or cmds.objectType(obj[0])=="nurbsSurface":   
            tempPiv= cmds.exactWorldBoundingBox(obj)
            piv= [round((tempPiv[0]+tempPiv[3])/2, 3), round((tempPiv[1]+tempPiv[4])/2, 3), round((tempPiv[2]+tempPiv[5])/2, 3)]
        return piv

    def resj(self):
        self.defi()
        obj= cmds.ls(sl=1)
        if obj:    
            if len(obj)==3:
                self.uiStuffClass.loadingBar(1, 1)
                chd= cmds.listRelatives(obj[1], c=1, pa=1, typ="transform")
                if chd:
                    tempGrp= cmds.group(chd, w=1, n="tempGrp")
                    allChd=[]
                    for item in chd:
                        allChd.append("tempGrp|%s"%item.split("|")[-1])
                    if obj[0] in chd:
                        newChd= "tempGrp|%s"%obj[0].split("|")[-1]
                    else:
                        newChd= obj[0]
                else:
                    newChd= obj[0]
                cmds.aimConstraint(newChd, obj[1], w=1, wut="object", aim=self.aimV, u=self.upV, wuo=obj[2])
                aimC= cmds.listConnections(newChd, t="aimConstraint")
                cmds.delete(aimC) 
                if chd:
                    cmds.parent(allChd, obj[1])
                    cmds.delete(tempGrp)
                cmds.makeIdentity(obj[1], a=1, r=0, n=0, pn=1)
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=obj)  
            else:
                cmds.warning("Please select exactly 3 objects : AIM DIRECTION, TARGET, UP OBJECT")  
        else:
            cmds.warning("Please select a JOINT")        

    def creaSm(self):
        self.defi()
        if cmds.objExists("LvnReorient")==0:
            pos1= cmds.xform(self.multiTar.split(", ")[0], q=1, ws=1, rp=1)
            pos2= cmds.xform(self.multiTar.split(", ")[-1], q=1, ws=1, rp=1)
            pos= [(pos1[0]+pos2[0])/2, (pos1[1]+pos2[1])/2, (pos1[2]+pos2[2])/2]
            tempGrp= cmds.group(n="LvnReorient", em=1)
            cmds.xform(tempGrp, t=(pos[0],pos[1],pos[2]), ws=1)
            dup= cmds.duplicate(self.multiTar.split(", ")[0], n="%s_ObjUp"%self.multiTar.split(", ")[0].split("|")[-1])
            cmds.parent(dup[0], tempGrp)
            ch= cmds.listRelatives(dup[0], ad=1, pa=1)
            for item in ch:
                extra= cmds.rename(item, "%s_ObjUp"%item.split("|")[-1])
            cmds.xform(tempGrp, s=(1.5, 1.5, 1.5), ws=1)
            dups= cmds.listRelatives(tempGrp, ad=1, pa=1)
            newName=[]
            for stuff in reversed(dups):
                #There might be joint that have extra group
                if "transform" not in stuff:
                    newName.append(stuff)
            cmds.textFieldButtonGrp(self.txtUp, e=1, tx="%s"%", ".join(newName))
        else:
            cmds.warning("Smart Up Object already exist!")

    def delSm(self):
        if cmds.objExists("LvnReorient"):
            cmds.delete("LvnReorient")
        else:
            cmds.warning("There is no SMART UP OBJECT to delete")

    def rejc(self):
        self.defi()
        up= self.multiUp.split(", ")
        tar= self.multiTar.split(", ")
        pre= self.multiTar.split(", ")[1:]
        allDumJnt, test1= [],1
        if self.multiUp and self.multiTar:
            if len(up)==len(tar):
                #Cant unparent n parent joint, causes viewport didnt update the orientation that's why uses dummy joint
                lastPos= cmds.xform(tar[-1], q=1, t=1, ws=1)
                for allUp in up:
                    if cmds.objExists(allUp)==0:
                        test1= []
                        break
                if test1:
                    self.uiStuffClass.loadingBar(1, len(pre)*2)
                    for item in zip(pre, tar, up):
                        dumJnt= cmds.joint(item[1])
                        cmds.parent(dumJnt, w=1)
                        aimC= cmds.aimConstraint(item[0], dumJnt, w=1, wut="object", aim=self.aimV, u=self.upV, wuo=item[2])
                        cmds.delete(aimC)
                        cmds.makeIdentity(dumJnt, a=1, r=1, n=0, pn=1)
                        allDumJnt.append(dumJnt)  
                        self.uiStuffClass.loadingBar(2)
                    for stuff in zip(tar, allDumJnt):
                        if stuff[0]==tar[0]:
                            par= cmds.listRelatives(stuff[0], p=1, pa=1)
                        else:
                            par= prev
                        if par:
                            cmds.parent(stuff[1], par)  
                        pos= cmds.xform(stuff[1], q=1, t=1, ws=1)
                        cmds.xform(stuff[0], t=(pos[0],pos[1],pos[2]), ws=1)
                        jo= cmds.getAttr("%s.jointOrient"%stuff[1])
                        cmds.setAttr("%s.jointOrient"%stuff[0], jo[0][0], jo[0][1], jo[0][2])
                        prev= stuff[0]
                        cmds.delete(stuff[1])
                        self.uiStuffClass.loadingBar(2)
                    cmds.xform(tar[-1], t=(lastPos[0], lastPos[1], lastPos[2]), ws=1)
                    cmds.setAttr("%s.jointOrient"%tar[-1], 0,0,0)
                    self.uiStuffClass.loadingBar(3, sel=tar[0])
                else:
                    cmds.warning("One of the OBJECT UP doest not exist!")
            else:
                cmds.warning("Targets and Up Objects number DOES NOT MATCH")   
        else:
            cmds.warning("<TARGET> field or <UP OBJS> field is empty!") 
            
    def helps(self):
        name="Help On Joint"
        helpTxt=""" 
        - Joints functions
        - Reorient (workable for joints or objects)

        < Edit >
        ==========
            1) Zero Joint Orient
                (* So that the joint will align with its parent)

            2) Duplicate Joint Children Only
                (* Skin joint might have groups or other stuff, so to separate it out for any purposes)

            3) Become Chain
                - Selected joint become chain

            4) Duplicate Become Chain
                - Selected joint gets duplicated and become chain
                (* Might be already a chain, but you wanted a different order)

            5) Reverse Selected Chain
                - Reverse the chain order

            6) Joint Display
                - Same as maya's

            7) All Joint Radius
                - Set attribute to all joint's radius
                (* To standardize joint size because some scripts / autorig create joint with different radius attribute value)


        < Reorient >
        ===============
            - Basically using aim Constraint + object up to reorient then delete connections

            1) Single Joint
            ----------------
                1. Create Center Locator
                    - Basically its create locator as a proxy selection

                2. Reorient Single Joint
                    - Exactly like aim constraint but selection base

            2) Joint Chain
            ----------------
                - Similar to "Single" but work for joint chain
                - Can use <Smart Up Object>, will predict what you needed. Or manually create own <Up Objects>
                    (* Basically its just duplicating the joint chain that you want and scale it,
                       Mostly it works but sometimes need to re-adjust)

                (* If using maya's joint orient, usually will have messed up orientation if its curved joint chain, like a "U")


        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)    
       
    def reloadSub(self):
        Joint()   
        
                     
if __name__=='__main__':
    Joint() 
                   