import maya.cmds as cmds
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox


class TransAttr(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()        
        self.helpBoxClass= helpBox.HelpBox()        
        self.win()

    def win(self):        
        try: 
            cmds.deleteUI("ta") 
        except:
            pass    
        cmds.window("ta", mb=1)              
        cmds.window("ta", t="Transfer Attribute", s=1, e=1, wh=(400,460))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on TransferAttribute", c=lambda x: self.helps())        
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload TransferAttribute", c=lambda x: self.reloadSub())
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Create")
        form1= cmds.formLayout(nd=100, p=column1)
        txt1= cmds.text(l="Select TARGETS", fn="smallObliqueLabelFont", en=0)
        txt2= cmds.text(l="Select SOURCE then TARGETS", fn="smallObliqueLabelFont", en=0)
        self.rb1= cmds.radioButtonGrp(l="", la4=["UP","DOWN", "COPY", "SWITCH"], cw5=(10,75,100,85,100), nrb=4 , sl=3, cc=lambda x: self.radio())
        sep0= cmds.separator(h=15, st="in") 
        txt3= cmds.text(l="TRANSLATE")
        txt4= cmds.text(l="ROTATE") 
        txt5= cmds.text(l="SCALE") 
        sep1= cmds.separator(w=100, st="in") 
        sep2= cmds.separator(w=80, st="in") 
        sep3= cmds.separator(w=62, st="in")
        txt6= cmds.text(l="     X : ")
        txt7= cmds.text(l="     Y : ")
        txt8= cmds.text(l="     Z : ")
        self.posT= cmds.checkBoxGrp(ncb=4, l="", cw2=(0,50), la4=["All","+","+","+"], vr=1, on1=lambda x: self.ccOn(self.posT, self.negT), of1=lambda x: self.ccOff(self.posT), cc=lambda x: self.ccSub(self.posT, self.negT), va4=(1,1,1,1)) 
        self.negT= cmds.checkBoxGrp(ncb=4, l="", cw2=(0,50), la4=["All","-","-","-"], vr=1, on1=lambda x: self.ccOn(self.negT, self.posT), of1=lambda x: self.ccOff(self.negT),cc=lambda x: self.ccSub(self.negT, self.posT))  
        self.posR= cmds.checkBoxGrp(ncb=4, l="", cw2=(0,50), la4=["All","+","+","+"], vr=1, on1=lambda x: self.ccOn(self.posR, self.negR), of1=lambda x: self.ccOff(self.posR), cc=lambda x: self.ccSub(self.posR, self.negR), va4=(1,1,1,1)) 
        self.negR= cmds.checkBoxGrp(ncb=4, l="", cw2=(0,50), la4=["All","-","-","-"], vr=1, on1=lambda x: self.ccOn(self.negR, self.posR), of1=lambda x: self.ccOff(self.negR), cc=lambda x: self.ccSub(self.negR, self.posR))  
        self.posS= cmds.checkBoxGrp(ncb=4, l="", cw2=(0,50), la4=["All","+","+","+"], vr=1, on1=lambda x: self.ccOn(self.posS, self.negS), of1=lambda x: self.ccOff(self.posS), cc=lambda x: self.ccSub(self.posS, self.negS), va4=(1,1,1,1))  
        self.negS= cmds.checkBoxGrp(ncb=4, l="", cw2=(0,50), la4=["All","-","-","-"], vr=1, on1=lambda x: self.ccOn(self.negS, self.posS), of1=lambda x: self.ccOff(self.negS), cc=lambda x: self.ccSub(self.negS, self.posS))          
        sep4= cmds.separator(h=5, st="in")
        txt9= cmds.text(l="Select SOURCE", fn="smallObliqueLabelFont", en=0)  
        self.cb2= cmds.checkBoxGrp(l="", l1="~", cw=(1,10), cc= lambda x: self.sr())  
        self.txtSear= cmds.textFieldGrp(l="Search :", en=0, cw2=(50,100), adj=2)
        self.txtRepl= cmds.textFieldGrp(l="Replace :", en=0, cw2=(50,100), adj=2)
        b1= cmds.button(l="Transfer (main attribute)", c= lambda x: self.final(1))  
        b2= cmds.button(l="Transfer (custom attribute)", c= lambda x: self.final(2)) 
        cmds.formLayout(form1, e=1,
                                af=[(txt1, "top", 0),
                                    (txt2, "top", 0),
                                    (self.rb1, "top", 20),
                                    (sep0, "top", 45),
                                    (txt3, "top", 66),
                                    (txt4, "top", 66),
                                    (txt5, "top", 66),
                                    (sep1, "top", 85),
                                    (sep2, "top", 85),
                                    (sep3, "top", 85),
                                    (txt6, "top", 110),
                                    (txt7, "top", 127),
                                    (txt8, "top", 143),
                                    (self.posT, "top", 90),
                                    (self.negT, "top", 90),
                                    (self.posR, "top", 90),
                                    (self.negR, "top", 90),
                                    (self.posS, "top", 90),
                                    (self.negS, "top", 90),
                                    (sep4, "top", 180),
                                    (txt9, "top", 195),
                                    (self.cb2, "top", 220),
                                    (self.txtSear, "top", 210),
                                    (self.txtRepl, "top", 233),
                                    (b1, "top", 278),
                                    (b2, "top", 304)],
                                ap=[(txt1, "left", 50, 0),
                                    (txt2, "left", 200, 0),
                                    (self.rb1, "left", 0, 0),
                                    (self.rb1, "right", 0, 100),
                                    (sep0, "left", 0, 0),
                                    (sep0, "right", 0, 100),
                                    (txt3, "left", 0, 5),
                                    (txt3, "right", 0, 35),
                                    (txt4, "left", 0, 37),
                                    (txt4, "right", 0, 67),
                                    (txt5, "left", 0, 67),
                                    (txt5, "right", 0, 97),
                                    (sep1, "left", -50, 20),
                                    (sep2, "left", -40, 52),
                                    (sep3, "left", -30, 82),
                                    (self.posT, "left", -30, 20),
                                    (self.negT, "left", 5, 20),
                                    (self.posR, "left", -30, 52),
                                    (self.negR, "left", 5, 52),
                                    (self.posS, "left", -25, 82),
                                    (self.negS, "left", 10, 82),
                                    (sep4, "left", 0, 0),
                                    (sep4, "right", 0, 100),
                                    (txt9, "left", 0, 10),
                                    (txt9, "right", 0, 100),
                                    (self.txtSear, "left", 50, 0),
                                    (self.txtSear, "right", 0, 100),
                                    (self.txtRepl, "left", 50, 0),
                                    (self.txtRepl, "right", 0, 100),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 100),
                                    (b2, "left", 0, 0),
                                    (b2, "right", 0, 100)])    
        cmds.showWindow("ta")      
       
    def defi(self):
        self.obj= cmds.ls(sl=1, tr=1)
        if self.obj==[]:
            self.obj= cmds.ls(sl=1)
        self.sear= cmds.textFieldGrp(self.txtSear, q=1, tx=1)
        self.repl= cmds.textFieldGrp(self.txtRepl, q=1, tx=1)    
        tx,ty,tz,rx,ry,rz,sx,sy,sz= 0,0,0,0,0,0,0,0,0
        #Translate
        if cmds.checkBoxGrp(self.posT, q=1, v2=1)==1:
            tx=1
        if cmds.checkBoxGrp(self.negT, q=1, v2=1)==1:
            tx=-1
        if cmds.checkBoxGrp(self.posT, q=1, v3=1)==1:
            ty=1
        if cmds.checkBoxGrp(self.negT, q=1, v3=1)==1:
            ty=-1
        if cmds.checkBoxGrp(self.posT, q=1, v4=1)==1:
            tz=1
        if cmds.checkBoxGrp(self.negT, q=1, v4=1)==1:
            tz=-1
        #Rotate
        if cmds.checkBoxGrp(self.posR, q=1, v2=1)==1:
            rx=1
        if cmds.checkBoxGrp(self.negR, q=1, v2=1)==1:
            rx=-1
        if cmds.checkBoxGrp(self.posR, q=1, v3=1)==1:
            ry=1
        if cmds.checkBoxGrp(self.negR, q=1, v3=1)==1:
            ry=-1
        if cmds.checkBoxGrp(self.posR, q=1, v4=1)==1:
            rz=1
        if cmds.checkBoxGrp(self.negR, q=1, v4=1)==1:
            rz=-1
        #Scale
        if cmds.checkBoxGrp(self.posS, q=1, v2=1)==1:
            sx=1
        if cmds.checkBoxGrp(self.negS, q=1, v2=1)==1:
            sx=-1
        if cmds.checkBoxGrp(self.posS, q=1, v3=1)==1:
            sy=1
        if cmds.checkBoxGrp(self.negS, q=1, v3=1)==1:
            sy=-1
        if cmds.checkBoxGrp(self.posS, q=1, v4=1)==1:
            sz=1
        if cmds.checkBoxGrp(self.negS, q=1, v4=1)==1:
            sz=-1
        self.allAttr=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]          
        self.allVal=[tx, ty, tz, rx, ry, rz, sx, sy, sz]        

    def radio(self): 
        if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==3 or cmds.radioButtonGrp(self.rb1, q=1, sl=1)==4 :    
            self.sr()
            cmds.checkBoxGrp(self.cb2, e=1, en=1)
        else: 
            cmds.checkBoxGrp(self.cb2, e=1, en=0)
            cmds.textFieldGrp(self.txtSear, e=1, en=0)
            cmds.textFieldGrp(self.txtRepl, e=1, en=0)            

    def ccOn(self, txt, negTxt):
        cmds.checkBoxGrp(txt, e=1, va4=[1,1,1,1]) 
        cmds.checkBoxGrp(negTxt, e=1, va4=[0,0,0,0])   

    def ccOff(self, txt):
        cmds.checkBoxGrp(txt, e=1, va4=[0,0,0,0])  

    def ccSub(self, txt, negTxt):
        #Same column 3in1
        if cmds.checkBoxGrp(txt, q=1, v2=1)==1 and cmds.checkBoxGrp(txt, q=1, v3=1)==1 and cmds.checkBoxGrp(txt, q=1, v4=1)==1:
            cmds.checkBoxGrp(txt, e=1, v1=1) 
        else:
            cmds.checkBoxGrp(txt, e=1, v1=0)
        #Untick different column
        if cmds.checkBoxGrp(txt, q=1, v2=1)==1:
            cmds.checkBoxGrp(negTxt, e=1, v2=0)       
        if cmds.checkBoxGrp(txt, q=1, v3=1)==1:
            cmds.checkBoxGrp(negTxt, e=1, v3=0) 
        if cmds.checkBoxGrp(txt, q=1, v4=1)==1:
            cmds.checkBoxGrp(negTxt, e=1, v4=0) 
        #Untick different column Main 
        if cmds.checkBoxGrp(negTxt, q=1, v2=1)==1 and cmds.checkBoxGrp(negTxt, q=1, v3=1)==1 and cmds.checkBoxGrp(negTxt, q=1, v4=1)==1:
            cmds.checkBoxGrp(negTxt, e=1, v1=1) 
        else:
            cmds.checkBoxGrp(negTxt, e=1, v1=0)  

    def sr(self):
        if cmds.checkBoxGrp(self.cb2, q=1, v1=1):
            cmds.textFieldGrp(self.txtSear, e=1, en=1)
            cmds.textFieldGrp(self.txtRepl, e=1, en=1)       
        else:
            cmds.textFieldGrp(self.txtSear, e=1, en=0)
            cmds.textFieldGrp(self.txtRepl, e=1, en=0)   

    def testLock1(self, sour, tar, searMeth, mainMeth):
        finalConti, mainAttr, finalCusAttr1= [],[],[]
        if mainMeth==1:
            #Check which main attribute need to check
            for attr, val in zip(self.allAttr, self.allVal):
                if val!=0:
                    mainAttr.append(attr)     
            if mainAttr:        
                #Check Main Attribute
                testMainAttrLock1, testCusAttrLock1, testNoCus1, finalCusAttr1= self.testLock2(sour, 1, mainAttr, mainMeth)
                testMainAttrLock2, testCusAttrLock2, testNoCus2, finalCusAttr2= self.testLock2(tar, searMeth, mainAttr, mainMeth)
                if testMainAttrLock1 and testMainAttrLock2:
                    finalConti= 1
                else:
                    cmds.warning("One of the SOURCE/TARGET main attribute (Ticked checkbox) is LOCKED") 
            else:
                cmds.warning("No channel is ticked to transfer")
        elif mainMeth==2:
            #Check if selected is Custom Attribute
            gotCusAttr= 1
            selAttr= cmds.channelBox("mainChannelBox", sma=1, q=1) 
            if selAttr:
                for attrs in selAttr:
                    if attrs in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]:
                        gotCusAttr=[]
            else:
                gotCusAttr= [] 

            #Check Custom Attribute
            if gotCusAttr:
                testMainAttrLock1, testCusAttrLock1, testNoCus1, finalCusAttr1= self.testLock2(sour, 1, mainAttr, mainMeth)
                testMainAttrLock2, testCusAttrLock2, testNoCus2, finalCusAttr2= self.testLock2(tar, searMeth, mainAttr, mainMeth)
                if testNoCus1 and testNoCus2:
                    if testCusAttrLock1 and testCusAttrLock2:
                        finalConti= 1
                    else:
                        cmds.warning("One of the SOURCE/TARGET CUSTOM attribute is LOCKED")
                else:
                    cmds.warning("One of the TARGET does not have the selected Custom Attribute")
            else:
                cmds.warning("please select a CUSTOM attribute in channelbox")
        return finalConti, finalCusAttr1

    def testLock2(self, tar, searMeth, mainAttr, mainMeth):
        self.defi()
        allCusAttr, finalCusAttr= [],[]
        testMainAttrLock, testCusAttrLock, testNoCus= 1,1,1
        for item in tar:
            if searMeth==2:
                item= cmds.listRelatives(item, typ="transform", ap=1, f=1)[0]    
            elif searMeth==3:
                item= cmds.listRelatives(item, typ="transform", c=1, f=1)[0]
            elif searMeth==4:
                item= item.replace(self.sear,self.repl)  
            #Check main attribute
            if mainMeth==1:     
                for stuff in mainAttr:
                    #"Try" because it doesnt work with non transform like blendshape or deformer
                    try:
                        if cmds.getAttr("%s.%s"%(item, stuff), l=1)==1:
                            testMainAttrLock= [] 
                    except:
                        pass  

            #Check custom attribute
            elif mainMeth==2:
                selAttr= cmds.channelBox("mainChannelBox", sma=1, q=1) 
                if selAttr:
                    allCusAttr= cmds.listAttr(item, ud=1)
                    if allCusAttr:
                        for attrs in selAttr:
                            if attrs in allCusAttr:
                                #Or else multiple target's custom attr will get stack
                                if attrs not in finalCusAttr:
                                    finalCusAttr.append(attrs)
                                if cmds.getAttr("%s.%s"%(item, attrs), l=1)==1: 
                                    testCusAttrLock= []
                            else:
                                testNoCus= [] 
                    else:
                        testNotCus= []            
        return testMainAttrLock, testCusAttrLock, testNoCus, finalCusAttr

    def TR1(self, sour, cusAttr, meth, searMeth, mainMeth):
        self.defi() 
        self.uiStuffClass.loadingBar(1, len(sour))
        for item in sour:
            if meth==1:
                tar= cmds.listRelatives(item, typ="transform", ap=1, f=1)[0]
            elif meth==2:
                tar= cmds.listRelatives(item, typ="transform", c=1, f=1)[0]
            elif meth==3 or meth==4: 
                if searMeth==4:
                    tar= item.replace(self.sear, self.repl)  
                elif searMeth==1:
                    tar= item 
                    item= self.obj[0]
            #For main attribute
            if mainMeth==1:
                #"Try" because it doesnt work with non transform like blendshape or deformer
                try:
                    trans1= cmds.xform(item, q=1, t=1, r=1)
                    rot1= cmds.xform(item, q=1, ro=1, r=1)
                    scal1= cmds.xform(item, q=1, s=1, r=1)    
                    allAns1= trans1 + rot1 + scal1
                    trans2= cmds.xform(tar, q=1, t=1, r=1)
                    rot2= cmds.xform(tar, q=1, ro=1, r=1)
                    scal2= cmds.xform(tar, q=1, s=1, r=1)    
                    allAns2= trans2 + rot2 + scal2
                    for x, attrVal in enumerate(zip(self.allAttr, self.allVal)):
                        if attrVal[1]!=0:
                            cmds.setAttr("%s.%s"%(tar, attrVal[0]), attrVal[1]*allAns1[x]) 
                            #For <Up/Down>
                            if meth==1 or meth==2:
                                if "s" in attrVal[0]:
                                    cmds.setAttr("%s.%s"%(item, attrVal[0]), 1) 
                                else:
                                    cmds.setAttr("%s.%s"%(item, attrVal[0]), 0) 
                            #For <Switch>
                            if meth==4:  
                                cmds.setAttr("%s.%s"%(item, attrVal[0]), attrVal[1]*allAns2[x])  
                except:
                    pass
            #For custom attribute
            elif mainMeth==2:
                if cusAttr:
                    for subAttr in cusAttr:
                        cusVal1= cmds.getAttr("%s.%s"%(item,subAttr))
                        cusVal2= cmds.getAttr("%s.%s"%(tar,subAttr))
                        cmds.setAttr("%s.%s"%(tar,subAttr), cusVal1)
                        if meth==1 or meth==2:
                            cmds.setAttr("%s.%s"%(item,subAttr), 0)
                        elif meth==4:
                            cmds.setAttr("%s.%s"%(item,subAttr), cusVal2)

            self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3) 

    def final(self, mainMeth):
        self.defi()  
        if self.obj:
            test1, test2= 1,1
            #Up
            if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==1:
                for item in self.obj:
                    tar= cmds.listRelatives(item, typ="transform", ap=1, f=1)
                    if tar==None:
                        test1=[]    
                if test1:
                    finalConti, cusAttr= self.testLock1(self.obj, self.obj, 2, mainMeth) 
                    if finalConti:   
                        self.TR1(self.obj, cusAttr, 1, 1, mainMeth) 
                else:
                    cmds.warning("One of the TARGET do not have a PARENT")
            #Down         
            elif cmds.radioButtonGrp(self.rb1, q=1, sl=1)==2:
                for item in self.obj: 
                    tar= cmds.listRelatives(item, typ="transform", c=1, f=1)  
                    if tar==None: 
                        test1= [] 
                    elif len(tar)>1:
                        test2= []     
                if test1:
                    if test2:
                        finalConti, cusAttr= self.testLock1(self.obj, self.obj, 3, mainMeth) 
                        if finalConti:   
                            self.TR1(self.obj, cusAttr, 2, 1, mainMeth)
                    else:
                        cmds.warning("Target have more than 1 CHILDREN") 
                else:
                    cmds.warning("One of the TARGET do not have a CHILDREN")  
            #Copy & Switch        
            else: 
                #With Search Replace
                if cmds.checkBoxGrp(self.cb2, q=1, v1=1):
                    conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(self.obj, self.sear, self.repl)
                    if conti:
                        if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==3:
                            finalConti, cusAttr= self.testLock1(self.obj, self.obj, 4, mainMeth) 
                            if finalConti:
                                self.TR1(self.obj, cusAttr, 3, 4, mainMeth)
                        elif cmds.radioButtonGrp(self.rb1, q=1, sl=1)==4:
                            finalConti, cusAttr= self.testLock1(self.obj, self.obj, 4, mainMeth) 
                            if finalConti:
                                self.TR1(self.obj, cusAttr, 4, 4, mainMeth)
                #Without Search Replace   
                else:
                    if cmds.radioButtonGrp(self.rb1, q=1, sl=1)==3:
                        if len(self.obj)>1:
                            finalConti, cusAttr= self.testLock1([self.obj[0]], self.obj[1:], 1, mainMeth) 
                            if finalConti:     
                                self.TR1(self.obj[1:], cusAttr, 3, 1, mainMeth)
                        else:
                            cmds.warning("Please select 1 SOURCE and 1 TARGET")
                    elif cmds.radioButtonGrp(self.rb1, q=1, sl=1)==4: 
                        if len(self.obj)==2: 
                            finalConti, cusAttr= self.testLock1([self.obj[0]], self.obj[1:], 1, mainMeth) 
                            if finalConti:   
                                self.TR1(self.obj[1:], cusAttr, 4, 1, mainMeth)
                        else:
                            cmds.warning("Please select only 2 objects (1 SOURCE, 1 TARGET)")   
        else:
            cmds.warning("Please select at least 1 object")      

    def helps(self):
        name="Help On TransferAttribute"
        helpTxt=""" 
        - Allow to transfer, copy or swap main/custom attribute



        A) UP
        =========
            1. Transfer attributes to parent
                (* meaning will zero out selected object (Only apply to ticked attribute)) 
        
        
        B) DOWN
        =========
            1. Transfer attributes to child
                (* meaning will zero out selected object (Only apply to ticked attribute))  
        
        
        C) COPY
        =========
            1. Copy attributes to Target
            

        D) SWITCH
        =========
            1. Swap attributes from each other
        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)
             
    def reloadSub(self):
        TransAttr()  
        

if __name__=='__main__':
    TransAttr() 
                        

