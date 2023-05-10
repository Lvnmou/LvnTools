import maya.cmds as cmds
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox
import re


class Renamer(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()        
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):        
        try: 
            cmds.deleteUI("ren") 
        except:
            pass    
        cmds.window("ren", mb=1)              
        cmds.window("ren", t="Renamer", s=1, e=1, wh=(340,320))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Renamer", c=lambda x: self.helps())
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Renamer", c=lambda x: self.reloadSub())         
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Prefix/Suffix")
        form1= cmds.formLayout(nd=100, p=column1)
        self.txtPrx= cmds.textFieldGrp(l="Prefix :", cw2=(55,100), adj=2)
        self.txtSfx= cmds.textFieldGrp(l="Suffix :", cw2=(55,100), adj=2)
        self.slider11= cmds.intSliderGrp(f=1, l="Remove :", cw3=(55,30,10), min=1, max=10, fmx=100, v=1)   
        self.cb11= cmds.checkBoxGrp(l="", l1="Hierarchy", cw2=(55,80))
        b11= cmds.button(l="Add Prefix / Suffix", c=lambda x: self.addRemove(1))     
        b12= cmds.button(l="Remove First x letter", c=lambda x: self.addRemove(2))
        b13= cmds.button(l="Remove Last x letter", c=lambda x: self.addRemove(3))
        txt11= cmds.text(l="* <Remove x letter> might cause same name issue\nSo the target might get some extra numeric", fn="smallObliqueLabelFont", en=0) 
        cmds.formLayout(form1, e=1,
                                af=[(self.txtPrx, "top", 0),
                                    (self.txtSfx, "top", 23),
                                    (self.slider11, "top", 69),
                                    (self.cb11, "top", 46),
                                    (b11, "top", 105),
                                    (b12, "top", 131),
                                    (b13, "top", 131),
                                    (txt11, "top", 165)],
                                ap=[(self.txtPrx, "left", 0, 0),
                                    (self.txtPrx, "right", 0, 100),
                                    (self.txtSfx, "left", 0, 0),
                                    (self.txtSfx, "right", 0, 100),
                                    (b11, "left", 0, 0),
                                    (b11, "right", 0, 100),
                                    (self.slider11, "left", 0, 0),
                                    (self.slider11, "right", 0, 100),
                                    (b12, "left", 0, 0),
                                    (b12, "right", 0, 50),
                                    (b13, "left", 0, 51),
                                    (b13, "right", 0, 100),
                                    (txt11, "left", 0, 0),
                                    (txt11, "right", 0, 100)]) 
        self.uiStuffClass.multiSetParent(4)
        column2= self.uiStuffClass.sepBoxSub("Batch")
        form2= cmds.formLayout(nd=100, p=column2)
        self.txtNN= cmds.textFieldGrp(l="New Name :", cw2=(65,150), adj=2)
        self.slider21= cmds.intSliderGrp(f=1, l="Padding :", cw3=(65,40,10), fmx=100, min=1, max=10, v=1)
        self.slider22= cmds.intSliderGrp(f=1, l="From :", cw3=(65,40,10), fmx=10000, min=1, v=1)  
        b21= cmds.button(l="Batch Rename", c=lambda x: self.batch())
        cmds.formLayout(form2, e=1,
                                af=[(self.txtNN, "top", 0),
                                    (self.slider21, "top", 26),
                                    (self.slider22, "top", 52),
                                    (b21, "top", 88)],
                                ap=[(self.txtNN, "left", 0, 0),
                                    (self.txtNN, "right", 0, 100),
                                    (self.slider21, "left", 0, 0),
                                    (self.slider21, "right", 0, 100),
                                    (self.slider22, "left", 0, 0),
                                    (self.slider22, "right", 0, 100),
                                    (b21, "left", 0, 0),
                                    (b21, "right", 0, 100)]) 
        self.uiStuffClass.multiSetParent(4)
        column3= self.uiStuffClass.sepBoxSub("Search Replace")
        form3= cmds.formLayout(nd=100, p=column3)
        self.txtSear= cmds.textFieldGrp(l="Search :", cw2=(50,50), adj=2) 
        self.txtRepl= cmds.textFieldGrp(l="Replace :", cw2=(50,50), adj=2)
        self.rb31= cmds.radioButtonGrp(l="", cw4=(50,100,100,80), la3=["Hierarchy", "Selected", "All"], nrb=3 , sl=2)
        b31= cmds.button(l="Replace", c=lambda x: self.rep())
        b32= cmds.button(l="Duplicate Rename", c=lambda x: self.dupRen(1))  
        b33= cmds.button(l="DupRen Group Scale", c=lambda x: self.dupRen(2))  
        b34= cmds.button(l="Grab Child Name", c=lambda x: self.renParChd(1, "child"))
        b35= cmds.button(l="Rename According Child", c=lambda x: self.renParChd(2, "child"))
        b36= cmds.button(l="Grab Parent Name", c=lambda x: self.renParChd(3, "parent"))
        b37= cmds.button(l="Rename According Parent", c=lambda x: self.renParChd(4, "parent"))
        cmds.formLayout(form3, e=1,
                                af=[(self.txtSear, "top", 0),
                                    (self.txtRepl, "top", 23),
                                    (self.rb31, "top", 46),
                                    (b31, "top", 80),
                                    (b32, "top", 106),
                                    (b33, "top", 106),
                                    (b34, "top", 142),
                                    (b35, "top", 142),
                                    (b36, "top", 168),
                                    (b37, "top", 168)],
                                ap=[(self.txtSear, "left", 0, 0),
                                    (self.txtSear, "right", 0, 100),
                                    (self.txtRepl, "left", 0, 0),
                                    (self.txtRepl, "right", 0, 100),
                                    (b31, "left", 0, 0),
                                    (b31, "right", 0, 100),
                                    (b32, "left", 0, 0),
                                    (b32, "right", 0, 50),
                                    (b33, "left", 0, 51),
                                    (b33, "right", 0, 100),
                                    (b34, "left", 0, 0),
                                    (b34, "right", 0, 50),
                                    (b35, "left", 0, 51),
                                    (b35, "right", 0, 100),
                                    (b36, "left", 0, 0),
                                    (b36, "right", 0, 50),
                                    (b37, "left", 0, 51),
                                    (b37, "right", 0, 100)])   
        cmds.showWindow("ren")

    def defi(self):
        self.obj= cmds.ls(sl=1)
        self.sear= cmds.textFieldGrp(self.txtSear, q=1, tx=1)
        self.repl= cmds.textFieldGrp(self.txtRepl, q=1 ,tx=1)   

    def addRemove(self, meth):
        obj= cmds.ls(sl=1)
        prx= cmds.textFieldGrp(self.txtPrx, q=1 ,tx=1)
        sfx= cmds.textFieldGrp(self.txtSfx, q=1 ,tx=1)  
        x= cmds.intSliderGrp(self.slider11, q=1, v=1)
        testFirstIsDigit, testMinNum= 1,1
        testErr= []
        if obj:
            newObj=[]
            for item in obj:
                newObj.append(item)
            if cmds.checkBoxGrp(self.cb11, q=1, v1=1):
                chd= cmds.listRelatives(obj, typ="transform", f=1, ad=1)
                if chd:
                    for allChd in chd:
                        if allChd not in newObj:
                            newObj.append(allChd)
            if meth==1:
                if prx or sfx:
                    if prx:
                        if str.isdigit(str(prx[0])):
                            testFirstIsDigit=[]
                    if testFirstIsDigit:
                        self.uiStuffClass.loadingBar(1, len(newObj)) 
                        for stuff in reversed(sorted(newObj)):
                            cmds.rename(stuff, "%s%s%s"%(prx,stuff.split("|")[-1],sfx)) 
                            self.uiStuffClass.loadingBar(2)
                        self.uiStuffClass.loadingBar(3) 
                    else:
                        cmds.warning("Prefix first letter cannot be a numeric")
                else:
                    cmds.warning("<Prefix> or <Suffix> textfield is empty!")
            else:
                for stuff in reversed(sorted(newObj)): 
                    if len(stuff)>2 and x>= len(stuff)-1:
                        testFirstIsDigit= []
                if testFirstIsDigit:
                    for stuff in reversed(sorted(newObj)): 
                        if len(stuff.split("|")[-1])==1:
                            testMinNum= []
                    if testMinNum:
                        self.uiStuffClass.loadingBar(1, len(newObj)) 
                        for stuff in reversed(sorted(newObj)):
                            try: 
                                if meth==2:
                                    cmds.rename(stuff, "%s"%stuff.split("|")[-1][x:])    
                                elif meth==3:
                                    cmds.rename(stuff, "%s"%stuff.split("|")[-1][:-x])
                            except:
                                testErr.append(stuff)
                            self.uiStuffClass.loadingBar(2)
                        self.uiStuffClass.loadingBar(3)
                        if testErr:
                            cmds.warning("Proceeded but there are some object that have some naming issue : <%s>"%(", ").join(testErr))
                    else:
                        cmds.warning("One of the selection item cannot remove anymore letter")
                else:
                    cmds.warning("cannot remove more than the object name")
        else:
            cmds.warning("Please select at least 1 OBJECT") 


    def renList(self, currentList, sear, repl):
        #This is to update the list
        newList=[] 
        if currentList:
            for item in currentList:
                newItem= re.sub(r"^%s"%re.escape("%s|"%sear), "%s|"%repl, item)
                newList.append(newItem)
            return newList    

    def batch(self):
        obj= cmds.ls(sl=1, l=1)
        newName= cmds.textFieldGrp(self.txtNN, q=1 ,tx=1)
        slidy1= cmds.intSliderGrp(self.slider21, q=1, v=1)
        slidy2= cmds.intSliderGrp(self.slider22, q=1, v=1)
        if obj:
            if newName:
                self.uiStuffClass.loadingBar(1, len(obj)) 
                for x in range(0, len(obj)):
                    #change the padding + start from which number
                    newNum= ("%0"+"%s"%slidy1+"d")%(x+slidy2)
                    newRen= cmds.rename(obj[x], "%s%s"%(newName,newNum))
                    
                    #to update the list
                    obj= self.renList(obj, obj[x], newRen)                         
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("<New Name> textfield is empty!")               
        else:
            cmds.warning("Please select at least 1 OBJECT") 

    def testName(self, tar):
        sameName, conti= [],[]
        for item in tar:
            #which one should i use? previous i ditch split[-1] but why now choose back.
            if item.split("|")[-1].replace(self.sear,self.repl)==item.split("|")[-1]:
            #if item.replace(self.sear,self.repl)==item:
                sameName.append(item)
        if len(sameName)!=len(tar):
            conti= self.dialogClass.printingDialog(sameName, "< %s > successful \n< %s > same name object"%(len(tar)-len(sameName),len(sameName)))
        return conti

    def repRen(self, conti, tar):       
        if conti:
            testNoName= 1
            testErr= []
            for stuff in reversed(sorted(tar)): 
                if (stuff.split("|")[-1]).replace(self.sear,self.repl)=="":
                    testNoName=[]
            if testNoName:
                self.uiStuffClass.loadingBar(1, len(tar))
                for stuff in reversed(sorted(tar)):  
                    #Use "try" for <ALL> because might deal with locked node
                    try:
                        cmds.rename(stuff, (stuff.split("|")[-1]).replace(self.sear,self.repl))
                    except:
                        testErr.append(stuff)
                    self.uiStuffClass.loadingBar(2)    
                self.uiStuffClass.loadingBar(3)
                if testErr:
                    cmds.warning("Proceeded but there are some object that have some naming issue : <%s>"%(", ").join(testErr))
            else:
                cmds.warning("One of the object after search replace have no name, please change <Replace>")

    def rep(self):
        self.defi()         
        if self.sear:
            if cmds.radioButtonGrp(self.rb31, q=1, sl=1)==3:
                tar= cmds.ls(l=1, mod=1)
                allTar= []
                for subTar in tar:
                    if self.sear in subTar:
                        allTar.append(subTar)  
                if allTar:        
                    self.repRen(1, allTar)   
                else:
                    cmds.warning("There is no <%s> in all of the OBJECT in this scene"%self.sear)   
            else:    
                if self.obj:         
                    if cmds.radioButtonGrp(self.rb31, q=1, sl=1)==1:
                        chd= cmds.listRelatives(self.obj, typ="transform", f=1, ad=1)  
                        if chd:
                            newObj= chd
                            for item in self.obj:
                                if item not in newObj:
                                    newObj.append(item)
                        else:
                            newObj= self.obj
                        conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(newObj, self.sear, self.repl, exist=[])
                        self.repRen(conti, newObj)
                    elif cmds.radioButtonGrp(self.rb31, q=1, sl=1)==2:
                        conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(self.obj, self.sear, self.repl, exist=[])
                        self.repRen(conti, self.obj)     
                else:
                    cmds.warning("Please select at least 1 OBJECT")               
        else:
            cmds.warning("<SEARCH> textfield is empty!")

    def dupRen(self, meth):   
        self.defi()  
        allTar, tempSour= [],[]
        test1= 1
        if self.obj:
            if self.sear:
                sourChd= cmds.listRelatives(self.obj, f=1, ad=1)
                if sourChd:
                    tempSour= sourChd
                    for tempSourChd in self.obj:
                        if tempSourChd not in tempSour:
                            tempSour.append(tempSourChd)
                else:
                    for tempSourChd in self.obj:
                        tempSour.append(tempSourChd)
                conti= self.testName(tempSour)
                if conti:
                    if meth==2:
                        for item in self.obj: 
                            if cmds.objectType(item)=="joint":
                                test1=[]
                    if test1:
                        self.uiStuffClass.loadingBar(1, len(tempSour))                                               
                        for item in self.obj:   
                            dup= cmds.duplicate(item, n=item.split("|")[-1].replace(self.sear,self.repl))
                            chd= cmds.listRelatives(dup[0], f=1, ad=1)
                            if chd:
                                for allChd in chd:
                                    newName= cmds.rename(allChd, allChd.split("|")[-1].replace(self.sear,self.repl))
                                    for attr in ("t","r","s","tx","ty","tz","rx","ry","rz","sx","sy","sz"):
                                        try:
                                            cmds.setAttr("%s.%s"%(newName,attr), k=1, l=0)
                                        except:
                                            pass
                                    self.uiStuffClass.loadingBar(2)
                            self.uiStuffClass.loadingBar(2)
                            if meth==2:
                                rot= cmds.xform(dup[0], q=1, ro=1, ws=1)
                                if (round(rot[0],3), round(rot[1],3), round(rot[2],3))!=(0.0,0.0,0.0):
                                    par= cmds.listRelatives(dup[0], pa=1, p=1)
                                    tempGrp= cmds.group(em=1)
                                    cmds.parent(dup[0], tempGrp)
                                    cmds.xform(tempGrp, s=(-1,1,1), ws=1)    
                                    if par:
                                        cmds.parent(dup[0], par)
                                    else:
                                        cmds.parent(dup[0], w=1)
                                    cmds.delete(tempGrp)
                                else: 
                                    piv= cmds.xform(dup[0], q=1, rp=1, ws=1)
                                    cmds.xform(dup[0], sp=(0,0,0), s=(-1,1,1), ws=1)
                                    if (round(piv[0],3), round(piv[1],3), round(piv[2],3))!=(0.0,0.0,0.0):
                                        cmds.xform(dup[0], rp=(-piv[0],piv[1],piv[2]), sp=(-piv[0],piv[1],piv[2]), ws=1)
                            allTar.append(dup[0])    
                        self.uiStuffClass.loadingBar(3, sel=allTar)
                    else:
                        cmds.warning("One of the select OBJECT is a JOINT, please select the group above it instead")
                else:
                    cmds.warning("There is no \"%s\" in the selected OBJECT"%self.sear)  
            else:
                cmds.warning("<SEARCH> textfield is empty!")
        else:
            cmds.warning("Please select at least 1 OBJECT")
  
    def renParChd(self, meth, parChd):  
        self.defi()
        allTar= []
        if self.obj:            
            testHaveTar, testNoName= 1,1
            testErr= []
            for item in self.obj:
                tar= self.parentOrChild(item, meth)
                if tar==None:
                    testHaveTar=[]
            if testHaveTar:
                if meth==1 or meth==3:
                    tar= self.parentOrChild(self.obj[0], meth)
                    cmds.textFieldGrp(self.txtSear, e=1, tx="%s"%tar[0])  
                else:  
                    for item in self.obj:                
                        tar= self.parentOrChild(item, meth)
                        if (tar[0].replace(self.sear,self.repl)).split("|")[-1]=="":
                            testNoName=[]
                        else:
                            allTar.append(tar[0])
                    if testNoName:     
                        conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(allTar, self.sear, self.repl, exist=[])
                        if conti:
                            self.uiStuffClass.loadingBar(1, len(self.obj))
                            for item in self.obj:
                                tar= self.parentOrChild(item, meth)
                                try:
                                    newP= cmds.rename(item, (tar[0].replace(self.sear,self.repl)).split("|")[-1])  
                                except:
                                    testErr.append(item)
                                self.uiStuffClass.loadingBar(2)
                            self.uiStuffClass.loadingBar(3)
                            if testErr:
                                cmds.warning("Proceeded but there are some object that have some naming issue <%s>"%(", ").join(testErr))
                    else:
                        cmds.warning("One of the object after search replace have no name, please change <Replace>")
            else:
                cmds.warning("One of the selected object does not have a %s"%parChd)
        else:
            cmds.warning("Please select at least 1 OBJECT")  

    def parentOrChild(self, source, meth):
        if meth==1 or meth==2:
            tar= cmds.listRelatives(source, c=1, typ="transform")
        elif meth==3 or meth==4:
            tar= cmds.listRelatives(source, p=1, typ="transform")
        return tar

    def helps(self):
        name="Help On Renamer"
        helpTxt="""
        - To Rename



        < Prefix / Suffix >
        ===================
            - Add prefix / suffix 
            - <Hierarchy> include all children
            - <Remove> is for <remove x letter> to determine how many letter to remove
             

        < Batch >
        =========
            - Batch rename all selected object with numeric 
            - Padding digits(1-100)
            - From which digit onwards (1-10000)

           
        < Search & Replace >
        ===================
            1) Search & Replace
            -----------------------
               - Same as maya 
                
            2) Duplicate Rename
            ---------------------
                1. Duplicate Rename 
                    - Duplicate and rename (include all children)

                2. DupRen Group Scale (include all children)
                    - Duplicate and rename
                    - Create a group in world and negative its scaleX
                        (* Usually its for those left right object)

                
            3) Rename According Parent / Child 
            --------------------------------------
                1. Grab Name (Parent/Child)
                    - Will grab its parent/child  name

                2. Rename According (Parent/Child)
                    - Just like Search and replace but rename according to parent/child name

                (*Eg. belt_stickJnt have a group name "Null1"
                        - select "Null1" and run <Grab Child Name>
                        - <Search> "_stickJnt", <Replace>  "_fol"
                        - run <Rename According Child>
                        - selected "Null1" will be rename to "belt_fol")
        """
        self.helpBoxClass.helpBox1(name, helpTxt)

    def reloadSub(self):
        Renamer() 
        
        
if __name__=='__main__':
    Renamer()            

