import maya.cmds as cmds
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox

class Snapper(object):
    def __init__(self, *args):
        self.uiStuffClass= uiStuff.UiStuff()        
        self.helpBoxClass= helpBox.HelpBox()
        self.win()


    def win(self):
        try:
            cmds.deleteUI("snp")
        except:
            pass          
        cmds.window("snp", mb=1)
        cmds.window("snp",t="Snapper", e=1, s=1, wh=(360,325)) 
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Snapper", c=lambda x: self.helps())       
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Snapper", c=lambda x: self.reloadSub()) 
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Create")
        form1= cmds.formLayout(nd=100, p=column1)
        self.cb11= cmds.checkBoxGrp(ncb=4, l="", la4=["Locator", "Null", "Joint", "FixJoint"], cw5=(20,80,70,70,70), cc=lambda x: self.cbx11())
        sep11= cmds.separator(h=5, st="in")
        self.slidy11= cmds.floatSliderGrp(l="Scale :", f=1, cw3=(75,62,120), min=0.1, max=10, fmx=100, fmn=0.01, pre=2, v=1)
        self.drop11= cmds.optionMenuGrp(l="Method :", cw2=(75,100), cc=lambda x: self.om())
        cmds.menuItem(l="Each  ")
        cmds.menuItem(l="Center  ")
        self.drop12= cmds.optionMenuGrp(l="Parent :", cw2=(75,100))
        cmds.menuItem(l="World   ")
        cmds.menuItem(l="Same ")
        cmds.menuItem(l="Under ")  
        self.drop13= cmds.optionMenuGrp(l="Rotate Order :", cw2=(75,100))  
        cmds.menuItem(l="Default")
        cmds.menuItem(l="Follow")
        txt11= cmds.text(l="Select OBJECTS / SUBSELECTIONS", fn="smallObliqueLabelFont", en=0)
        b11= cmds.button(l="Create", c= lambda x: self.snapCreate())  
        cmds.formLayout(form1, e=1,
                                af=[(self.cb11, "top", 0),
                                    (sep11, "top", 30),
                                    (self.slidy11, "top", 50),
                                    (self.drop11, "top", 75),
                                    (self.drop12, "top", 97),
                                    (self.drop13, "top", 119),
                                    (txt11, "top", 157),
                                    (b11, "top", 170)],
                                ap=[(sep11, "left", 0, 0),
                                    (sep11, "right", 0, 100),
                                    (self.slidy11, "left", 0, 0),
                                    (self.slidy11, "right", 0, 100),
                                    (txt11, "left", 0, 0),
                                    (txt11, "right", 0, 100),
                                    (b11, "left", 0, 0),
                                    (b11 , "right", 0, 100)]) 
        self.uiStuffClass.multiSetParent(4)
        column2= self.uiStuffClass.sepBoxSub("Snap")    
        form2= cmds.formLayout(nd=100, p=column2)
        self.rb21= cmds.radioButtonGrp(l="", cw4=(5,80,100,50), la3=["Pivot", "Translate", "Translate + Rotate"], nrb=3 , sl=2)
        sep21= cmds.separator(h=5, st="in")
        self.cbTar= cmds.checkBoxGrp(ncb=1, l="", cw2=(5,100), v1=0, cc=lambda x: self.cbx21()) 
        self.txtTar= cmds.textFieldButtonGrp(l="Targets : ", en=0, cw3=(53,100,10), adj=2, bl="  Grab  ", bc= lambda : self.grab(self.txtTar))
        self.txtSour= cmds.textFieldButtonGrp(l="Sources : ", en=0, cw3=(53,100,10), adj=2, bl="  Grab  ", bc= lambda : self.grab(self.txtSour))
        self.txt21= cmds.text(l="Select TARGET then SOURCES", fn="smallObliqueLabelFont", en=0)
        b21= cmds.button(l="Snap", c= lambda x: self.snapPivTranRot())  
        cmds.formLayout(form2, e=1,
                                af=[(self.rb21, "top", 0),
                                    (sep21, "top", 30),
                                    (self.cbTar, "top", 63),
                                    (self.txtTar, "top", 45),
                                    (self.txtSour, "top", 71),
                                    (self.txt21, "top", 116),
                                    (b21, "top", 131)],
                                ap=[(sep21, "left", 0, 0),
                                    (sep21, "right", 0, 100),
                                    (self.txtTar, "left", 30, 0),
                                    (self.txtTar, "right", 0, 100),
                                    (self.txtSour, "left", 30, 0),
                                    (self.txtSour, "right", 0, 100),    
                                    (self.txt21, "left", 0, 0),
                                    (self.txt21 , "right", 0, 100),                                
                                    (b21, "left", 0, 0),
                                    (b21, "right", 0, 100)])    
        self.uiStuffClass.multiSetParent(4)
        column3= self.uiStuffClass.sepBoxSub("Aligner") 
        form31= cmds.formLayout(nd=100, p=column3)
        b31= cmds.button(l="Up", c=lambda x:self.advSnap(1,1))
        b32= cmds.button(l="Left", c=lambda x:self.advSnap(0,0))
        b33= cmds.button(l="Right", c=lambda x:self.advSnap(0,1))
        b34= cmds.button(l="Down", c=lambda x:self.advSnap(1,0))         
        b35= cmds.button(l="Front", c=lambda x:self.advSnap(2,1))
        b36= cmds.button(l="Back", c=lambda x:self.advSnap(2,0))  
        b37= cmds.button(l="Y   Up Down", c=lambda x:self.advSnap(1,2))
        b38= cmds.button(l="X   Left Right", c=lambda x:self.advSnap(0,2))
        b39= cmds.button(l="Z   Front Back", c=lambda x:self.advSnap(2,2))
        cmds.formLayout(form31, e=1,
                                af=[(b31, "top", 0),
                                    (b32, "top", 26),
                                    (b33, "top", 26),
                                    (b34, "top", 52),
                                    (b35, "top", 95),
                                    (b36, "top", 95),
                                    (b37, "top", 12),
                                    (b38, "top", 38),
                                    (b39, "top", 95)],
                                ap=[(b31, "left", 0, 50),
                                    (b31, "right", 0, 80),
                                    (b32, "left", 0, 34),
                                    (b32, "right", 0, 64),
                                    (b33, "left", 0, 65),
                                    (b33, "right", 0, 95),
                                    (b34, "left", 0, 50),
                                    (b34, "right", 0, 80),
                                    (b35, "left", 0, 34),
                                    (b35, "right", 0, 64),
                                    (b36, "left", 0, 65),
                                    (b36, "right", 0, 95),
                                    (b37, "left", 0, 0),
                                    (b37, "right", 0, 28),
                                    (b38, "left", 0, 0),
                                    (b38, "right", 0, 28),
                                    (b39, "left", 0, 0),
                                    (b39, "right", 0, 28)]) 
        cmds.showWindow("snp")


    def cbx11(self):
        if cmds.checkBoxGrp(self.cb11, q=1, v4=1):
            cmds.optionMenuGrp(self.drop12, e=1, en=1, sl=2)
            cmds.optionMenuGrp(self.drop13, e=1, en=0, sl=2) 
        else:
            cmds.optionMenuGrp(self.drop13, e=1, en=1, sl=1)

    def om(self):
        if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
            cmds.optionMenuGrp(self.drop12, e=1, en=1)
            cmds.optionMenuGrp(self.drop13, e=1, en=1)
        else:
            cmds.optionMenuGrp(self.drop12, e=1, en=0, sl=1)
            cmds.optionMenuGrp(self.drop13, e=1, en=0, sl=1)                       
                          
    def cbx21(self):
        if cmds.checkBoxGrp(self.cbTar, q=1, v1=1):     
            cmds.textFieldButtonGrp(self.txtTar, e=1, en=1)
            cmds.textFieldButtonGrp(self.txtSour, e=1, en=1)
            cmds.text(self.txt21, e=1, l="Select NOTHING")
        else:
            cmds.textFieldButtonGrp(self.txtTar, e=1, en=0)
            cmds.textFieldButtonGrp(self.txtSour, e=1, en=0)
            cmds.text(self.txt21, e=1, l="Select TARGET then SOURCES")

    def grab(self, txt):   
        obj= cmds.ls(os=1, fl=1)
        if obj:   
            cmds.textFieldButtonGrp(txt, e=1, tx=", ".join(obj))
        else:
            cmds.warning("Please select at least 1 OBJECT")   

    def mode(self, meth):
        if meth==1:
            cmds.formLayout(self.form33, e=1, vis=0)
            cmds.formLayout(self.form32, e=1, vis=1)
        else:
            cmds.formLayout(self.form32, e=1, vis=0)
            cmds.formLayout(self.form33, e=1, vis=1)

    def pivRot(self, obj):
        if cmds.objectType(obj)=="transform" or cmds.objectType(obj)=="joint":                                   
            piv= cmds.xform(obj, q=1, rp=1, ws=1)
            rot= cmds.xform(obj, q=1, ro=1, ws=1) 
            rotOr= cmds.xform(obj, q=1, roo=1) 
        elif cmds.objectType(obj)=="mesh" or cmds.objectType(obj)=="nurbsCurve" or cmds.objectType(obj)=="nurbsSurface":   
            tempPiv= cmds.exactWorldBoundingBox(obj)
            piv= [round((tempPiv[0]+tempPiv[3])/2, 3), round((tempPiv[1]+tempPiv[4])/2, 3), round((tempPiv[2]+tempPiv[5])/2, 3)]
            rot= [0,0,0]
            rotOr= "xyz"
        return piv, rot, rotOr
    
    def createType(self, meth, obj):
        size= cmds.floatSliderGrp(self.slidy11, q=1, v=1)
        extra=[]
        if meth==1:
            tar= cmds.createNode("transform", n="%s_loc"%obj.split(".")[0])
            extra= cmds.createNode("locator", p=tar, n="%s"%tar.replace("_loc","_locShape"))
        elif meth==2:
            tar= cmds.createNode("transform", n="%s_null"%obj.split(".")[0])            
        elif meth==3:   
            tar= cmds.createNode("joint", n="%s_jnt"%obj.split(".")[0])
        elif meth==4:
            for x in [1,2,3,4,5,6,7,8,9,10]:
                if cmds.objExists("%s_fixJnt%s"%(obj.split(".")[0].replace("_jnt",""),x))==0:
                    break
            tar= cmds.createNode("transform", n="%s_fixJnt%s_grp"%(obj.split(".")[0].replace("_jnt",""),x)) 
            extra= cmds.createNode("joint", p=tar, n="%s_fixJnt%s"%(obj.split(".")[0].replace("_jnt",""),x))   
        if meth==1 or meth==2:
            cmds.setAttr("%s.scale"%tar, size, size, size) 
        elif meth==3: 
            cmds.setAttr("%s.radius"%tar, size)
        elif meth==4: 
            cmds.setAttr("%s.radius"%extra, size)            
        return tar, extra

    def cleanupSnp(self, obj, tar, piv, rot, rotOr, extra):     
        if cmds.optionMenuGrp(self.drop13, q=1, sl=1)==2:
            cmds.xform(tar, roo=rotOr)
            if cmds.checkBoxGrp(self.cb11, q=1, v4=1):
                cmds.xform(extra, roo=rotOr)      
        cmds.xform(tar, t=(piv[0],piv[1],piv[2]), ro=(rot[0],rot[1],rot[2]), ws=1)     
        if cmds.objectType(obj)=="transform" or cmds.objectType(obj)=="joint":      
            if cmds.optionMenuGrp(self.drop12, q=1, sl=1)==2:    
                par= cmds.listRelatives(obj, p=1, pa=1)
                if par:
                    tar= cmds.parent(tar, par)[0]
            elif cmds.optionMenuGrp(self.drop12, q=1, sl=1)==3:
                tar= cmds.parent(tar, obj)[0]
        return tar

    def pivCent(self, obj):
        tempPivX, tempPivY, tempPivZ, tempRotX, tempRotY, tempRotZ= [],[],[],[],[],[]
        for item in obj:
            tempPiv, tempRot, emp= self.pivRot(item)
            for x,stuff in enumerate(zip([tempPivX, tempPivY, tempPivZ],[tempRotX, tempRotY, tempRotZ])):
                stuff[0].append(tempPiv[x])
                stuff[1].append(tempRot[x])
        piv= [round((min(tempPivX)+max(tempPivX))/2, 3), round((min(tempPivY)+max(tempPivY))/2, 3), round((min(tempPivZ)+max(tempPivZ))/2, 3)]           
        rot= [round((min(tempRotX)+max(tempRotX))/2, 3), round((min(tempRotY)+max(tempRotY))/2, 3), round((min(tempRotZ)+max(tempRotZ))/2, 3)]
        rotOr= "xyz"           
        return piv, rot, rotOr

    def createTar(self, obj, meth): 
        finalTar= [] 
        if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:
            for item in obj:
                piv, rot, rotOr= self.pivRot(item) 
                tar, extra= self.createType(meth, item)
                tar= self.cleanupSnp(item, tar, piv, rot, rotOr, extra)
                finalTar.append(tar)
                self.uiStuffClass.loadingBar(2)
        else:
            piv, rot, emp= self.pivCent(obj)
            tar, extra= self.createType(meth, obj[0])
            tar= self.cleanupSnp(obj[0], tar, piv, rot, emp, extra)
            finalTar.append(tar)
            self.uiStuffClass.loadingBar(2)
        return finalTar 

    def snapCreate(self):
        obj= cmds.ls(os=1, fl=1)
        tar1,tar2,tar3,tar4= [],[],[],[]
        ans1,ans2,ans3,ans4= 0,0,0,0
        if obj:     
            if cmds.checkBoxGrp(self.cb11, v1=1, q=1) or cmds.checkBoxGrp(self.cb11, v2=1, q=1) or cmds.checkBoxGrp(self.cb11, v3=1, q=1) or cmds.checkBoxGrp(self.cb11, v4=1, q=1):    
                if cmds.checkBoxGrp(self.cb11, v1=1, q=1)==1:    
                    ans1=1
                if cmds.checkBoxGrp(self.cb11, v2=1, q=1)==1:  
                    ans2=1  
                if cmds.checkBoxGrp(self.cb11, v3=1, q=1)==1:    
                    ans3=1
                if cmds.checkBoxGrp(self.cb11, v4=1, q=1)==1:    
                    ans4=1    
                if cmds.optionMenuGrp(self.drop11, q=1, sl=1)==1:    
                    self.uiStuffClass.loadingBar(1, len(obj)*(ans1+ans2+ans3+ans4))
                else:
                    self.uiStuffClass.loadingBar(1, (ans1+ans2+ans3+ans4))

                if cmds.checkBoxGrp(self.cb11, v1=1, q=1)==1:           
                    tar1= self.createTar(obj, 1)
                if cmds.checkBoxGrp(self.cb11, v2=1, q=1)==1:
                    tar2= self.createTar(obj, 2)
                if cmds.checkBoxGrp(self.cb11, v3=1, q=1)==1:
                    tar3= self.createTar(obj, 3) 
                if cmds.checkBoxGrp(self.cb11, v4=1, q=1)==1:
                    tar4= self.createTar(obj, 4)
                self.uiStuffClass.loadingBar(3, sel=tar1+tar2+tar3+tar4) 
            else:
                cmds.warning("Please tick 1 of the CHECKBOX (Locator / Null / Joint / FixJoint)")
        else:
            cmds.warning("Please select at least 1 Target (Object / Subselections)")   

    def cusPiv(self, item):
        #Test custom pivot
        dup= cmds.duplicate(item, po=1)
        preRP= cmds.xform(dup[0], rp=1, q=1, ws=1)
        cmds.xform(dup[0], ztp=1, ws=1)
        postRP= cmds.xform(dup[0], rp=1, q=1, ws=1)
        cmds.delete(dup)       
        return preRP, postRP                         

    def snapPivTranRot(self):  
        test1, test2= [],[]
        if cmds.checkBoxGrp(self.cbTar, q=1, v1=1):
            tempTar= cmds.textFieldButtonGrp(self.txtTar, q=1, tx=1)
            tempSour= cmds.textFieldButtonGrp(self.txtSour, q=1, tx=1)
            if tempTar:
                if tempSour:
                    sel= cmds.ls(os=1, fl=1)
                    tar= tempTar.split(", ")
                    obj= tempSour.split(", ")
                    for item in obj:
                        if item not in tar:
                            test2= 1
                    if test2:
                        test1= 1
                    else:
                        cmds.warning("<TARGETS> and <SOURCES> cannot have the same object")
                else:
                    cmds.warning("<SOURCES> text field is empty!")                    
            else:
                cmds.warning("<TARGETS> text field is empty!")
        else:
            if len(cmds.ls(os=1, fl=1))>1:
                tar= [cmds.ls(os=1, fl=1)[0]] 
                obj= cmds.ls(os=1, fl=1)[1:]
                sel= cmds.ls(os=1, fl=1)
                test1= 1
            else:
                cmds.warning("Please select 1 TARGET and at least 1 SOURCE")
        if test1:
            self.uiStuffClass.loadingBar(1, len(tar))
            if len(obj)==1:
                piv, rot, emp= self.pivRot(obj[0]) 
            else:
                piv, rot, emp= self.pivCent(obj)
            for item in tar:
                if cmds.objectType(item)=="transform" or cmds.objectType(item)=="joint":  
                    if cmds.radioButtonGrp(self.rb21, sl=1, q=1)==1:
                        cmds.xform(item, rp=(piv[0],piv[1],piv[2]), sp=(piv[0],piv[1],piv[2]), ws=1)
                    else:
                        preRP, postRP= self.cusPiv(item)                       
                        if cmds.radioButtonGrp(self.rb21, sl=1, q=1)==2:
                            cmds.xform(item, t=(piv[0],piv[1],piv[2]), ws=1)
                        else: 
                            cmds.xform(item, t=(piv[0],piv[1],piv[2]), ro=(rot[0],rot[1],rot[2]), ws=1)
                        if preRP!= postRP:
                            cmds.xform(item, t=(postRP[0]-preRP[0],postRP[1]-preRP[1],postRP[2]-preRP[2]), r=1, wd=1)
                elif cmds.objectType(item)=="mesh" or cmds.objectType(item)=="nurbsCurve" or cmds.objectType(item)=="nurbsSurface":
                    #For subselection especially edge, face cannot use xform(ws=1)
                    bb= cmds.xform(item, bb=1, q=1, ws=1)
                    oriPiv= [round((bb[0]+bb[3])/2, 3), round((bb[1]+bb[4])/2, 3), round((bb[2]+bb[5])/2, 3)]
                    cmds.xform(item, t=(piv[0]-oriPiv[0],piv[1]-oriPiv[1],piv[2]-oriPiv[2]), r=1, wd=1)
                self.uiStuffClass.loadingBar(2)  
            self.uiStuffClass.loadingBar(3, sel=sel)         

    def advSnap(self, meth1, meth2):
        obj= cmds.ls(os=1, fl=1)
        allPiv= []
        if obj and len(obj)>1:
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                piv, rot, emp= self.pivRot(item) 
                allPiv.append(piv[meth1])
            if meth2==0:
                val= min(allPiv)
            elif meth2==1:
                val= max(allPiv)
            else:
                val= (min(allPiv)+max(allPiv))/2
            for item in obj:
                if cmds.objectType(item)=="transform" or cmds.objectType(item)=="joint": 
                    oriPiv= cmds.xform(item, rp=1, q=1, ws=1)
                elif cmds.objectType(item)=="mesh" or cmds.objectType(item)=="nurbsCurve" or cmds.objectType(item)=="nurbsSurface":
                    bb= cmds.xform(item, bb=1, q=1, ws=1)
                    oriPiv= [round((bb[0]+bb[3])/2, 3), round((bb[1]+bb[4])/2, 3), round((bb[2]+bb[5])/2, 3)]
                if meth1==0:
                    cmds.xform(item, t=(val-oriPiv[0],0,0), r=1, ws=1)
                elif meth1==1:
                    cmds.xform(item, t=(0,val-oriPiv[1],0), r=1, ws=1)
                else:
                    cmds.xform(item, t=(0,0,val-oriPiv[2]), r=1, ws=1)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3, sel=obj, tim=0.05)
        else:
            cmds.warning("Please select at least 2 SELECTIONS (Objects/subselections)")

    def helps(self):
        name="Help On Snapper"
        helpTxt="""
        - To create "Locator" / "Joint" / "Empty Group" (Null) / "FixJoint" at desire location
        - Snap to desire location or change pivot (specific or center)
        - To align


        < Create >
        ===========
            - Create <Locator> / <Joint> / <Null> / <FixJoint>
                - If select "Object", will snap to pivot point
                - If select "Subselection", will snap to it
                - If select multiple, will snap to center of it

            1) Method
            -----------
                1. Each
                    - Create for each selection
                2. Center
                    - Create only 1 on the center of all selection

            2) Parent
            -----------
                1. World
                    - Create on world
                2. Same
                    - Create on same hierachy as selection (meaning sharing same parent)
                3. Under
                    - Create as a child of the selection    

            3) Rotate Order
            ----------------
                1. Default
                    - "xyz"

                2. Follow
                    - Follow current selected object's rotate order


            (* Center is the same as center pivot)
            (eg: Average is (6+6+2)/3 =4.667 but this find the min and max like center pivot 
                 Max=6, Min=2 So Center = (6+2)/2 = 4)


        < Snap >
        ===========
            - Snap <Pivot> / <Translate> / <Translate + Rotate>

            (* For subselection, all 3 mods will work as <Translate>)


        < Aligner >
        ===========
            - Aligning Objects / Subselections

            (* For Edge/Face, will maintain their shape and snap according their center point)
            (* For objects, will use their pivot, so depends should you "Center Pivot" it before align)

            (* For now cant work with "Transform Constraint" so can maintain the shape)
        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)
        
    def reloadSub(self):
        Snapper()   
             
             
if __name__=='__main__':
    Snapper()


