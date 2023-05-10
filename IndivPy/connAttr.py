import maya.cmds as cmds
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox


class ConnAttr(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):        
        try: 
            cmds.deleteUI("connA") 
        except:
            pass    
        cmds.window("connA", mb=1)              
        cmds.window("connA", t="Connect Attribute", s=1, e=1, wh=(380,595))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on ConnectAttribute", c=lambda x: self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload ConnectAttribute", c=lambda x: self.reloadSub())  
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Connect")
        form1= cmds.formLayout(nd=100, p=column1)
        self.txt1= cmds.text(l="Select SOURCE then TARGETS", fn="smallObliqueLabelFont", en=0)
        self.txtSourAttr= cmds.textFieldButtonGrp(l="Source Attr :", pht="<Connector>", adj=2, cw3=(70,0,0), bl="   Grab   ", bc=lambda : self.grab1(self.txtSourAttr))
        self.txtTarAttr= cmds.textFieldButtonGrp(l="Target Attr :", pht="<Connected>", adj=2, cw3=(70,0,0), bl="   Grab   ", bc=lambda : self.grab1(self.txtTarAttr))
        sep1= cmds.separator(h=5, st="in")
        self.cbSour= cmds.checkBoxGrp(l="", cw2=(5,0), cc=lambda x: self.cbx1())
        self.txtSour= cmds.textFieldButtonGrp(l="Source :", en=0, adj=2, cw3=(50,0,0), bl="   Grab   ", bc= lambda : self.grab2(self.txtSour))
        sep2= cmds.separator(h=5, st="in")
        self.cbTar= cmds.checkBoxGrp(l="", cw2=(5,0), cc=lambda x: self.cbx2())
        self.txt2= cmds.text(l="Select SOURCE", fn="smallObliqueLabelFont", en=0)
        self.txtTar= cmds.textFieldButtonGrp(l="Target :", en=0, adj=2, cw3=(75,0,0), bl="   Grab   ", bc= lambda : self.grab2(self.txtTar))
        self.txtRevTar= cmds.textFieldButtonGrp(l="Reverse Tar:", pht="<Can be blank>", en=0, adj=2, cw3=(75,0,0), bl="   Grab   ", bc= lambda : self.grab2(self.txtRevTar))
        self.txtRevTarAttr= cmds.textFieldButtonGrp(l="Reverse Attr:", en=0, pht="<REVERSE Node>", adj=2, cw3=(75,0,0), bl="   Grab   ", bc= lambda : self.grab1(self.txtRevTarAttr))
        txt3= cmds.text(l="* Can grab output history, like blendshape\n* Reverse is not negative but adding a reverse node!", fn="smallObliqueLabelFont", en=0)
        self.bSwitch= cmds.button(l="Switch", en=0, c=lambda x: self.switch(self.txtTar, self.txtRevTar)) 
        sep3= cmds.separator(h=5, st="in")
        self.cbSR= cmds.checkBoxGrp(l="", cw2=(5,0), cc=lambda x: self.cbx3())
        self.txt4= cmds.text(l="Select SOURCE", fn="smallObliqueLabelFont", en=0)
        self.txtSear= cmds.textFieldGrp(l="Search :", cw2=(50,0), adj=2, en=0)
        self.txtRepl= cmds.textFieldGrp(l="Replace :", cw2=(50,0), adj=2, en=0)
        sep4= cmds.separator(h=5, st="in")  
        self.cbMult= cmds.checkBoxGrp(l="", cw2=(5,0), cc=lambda x: self.cbx4())
        self.mult= cmds.floatFieldGrp(l="Multiply :", en=0, adj=2, cw2=(50,0), pre=3)
        sep5= cmds.separator(h=5, st="in") 
        b1= cmds.button(l="Connect", c=lambda x: self.final(1))
        b2= cmds.button(l="Force Connect", c=lambda x: self.final(2))
        self.b3= cmds.button(l="Negate Translate", c=lambda x: self.final(3))
        self.b4= cmds.button(l="Negate Rotate", c=lambda x: self.final(4))  
        cmds.formLayout(form1, e=1,
                                af=[(self.txt1, "top", 0),
                                    (self.txtSourAttr, "top", 15),
                                    (self.txtTarAttr, "top", 41),
                                    (sep1, "top", 72),
                                    (self.cbSour, "top", 96),
                                    (self.txtSour, "top", 90),
                                    (sep2, "top", 122),
                                    (self.cbTar, "top", 185),
                                    (self.txt2, "top", 137),
                                    (self.txtTar, "top", 152),
                                    (self.txtRevTar, "top", 178),
                                    (self.txtRevTarAttr, "top", 204),
                                    (self.bSwitch, "top", 193),                                    
                                    (txt3, "top", 237),
                                    (sep3, "top", 269),
                                    (self.cbSR, "top", 309),
                                    (self.txt4, "top", 284),
                                    (self.txtSear, "top", 299),
                                    (self.txtRepl, "top", 322),
                                    (sep4, "top", 354),
                                    (self.cbMult, "top", 374),
                                    (self.mult, "top", 369),
                                    (sep5, "top", 401),
                                    (b1, "top", 416),
                                    (b2, "top", 416),
                                    (self.b3, "top", 442),
                                    (self.b4, "top", 442)],
                                ap=[(self.txt1, "left", 0, 0),
                                    (self.txt1, "right", 0, 100),
                                    (self.txtSourAttr, "left", 0, 0),
                                    (self.txtSourAttr, "right", 0, 100),
                                    (self.txtTarAttr, "left", 0, 0),
                                    (self.txtTarAttr, "right", 0, 100),
                                    (sep1, "left", 0, 0),
                                    (sep1, "right", 0, 100),   
                                    (self.txt2, "left", 0, 0),
                                    (self.txt2, "right", 0, 100),
                                    (self.txtSour, "left", 30, 0),
                                    (self.txtSour, "right", 0, 100),
                                    (sep2, "left", 0, 0),
                                    (sep2, "right", 0, 100),   
                                    (self.txtTar, "left", 30, 0),
                                    (self.txtTar, "right", 0, 100),
                                    (self.txtRevTar, "left", 30, 0),
                                    (self.txtRevTar, "right", 55, 100),
                                    (self.txtRevTarAttr, "left", 30, 0),
                                    (self.txtRevTarAttr, "right", 55, 100),
                                    (self.bSwitch, "left", -55, 100),
                                    (self.bSwitch, "right", 0, 100),                                    
                                    (txt3, "left", 0, 0),
                                    (txt3, "right", 0, 100),
                                    (sep3, "left", 0, 0),
                                    (sep3, "right", 0, 100),
                                    (self.txt4, "left", 0, 0),
                                    (self.txt4, "right", 0, 100),                                    
                                    (self.txtSear, "left", 30, 0),
                                    (self.txtSear, "right", 0, 100),
                                    (self.txtRepl, "left", 30, 0),
                                    (self.txtRepl, "right", 0, 100),
                                    (sep4, "left", 0, 0),
                                    (sep4, "right", 0, 100),
                                    (self.mult, "left", 30, 0),
                                    (self.mult, "right", 0, 100),
                                    (sep5, "left", 0, 0),
                                    (sep5, "right", 0, 100),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 50),
                                    (b2, "left", 0, 51),
                                    (b2, "right", 0, 100),
                                    (self.b3, "left", 0, 0),
                                    (self.b3, "right", 0, 50),
                                    (self.b4, "left", 0, 51),
                                    (self.b4, "right", 0, 100)])  
        cmds.showWindow("connA")

    def defi(self):
        self.obj= cmds.ls(sl=1)     
        self.line1= cmds.textFieldButtonGrp(self.txtSourAttr, q=1,tx=1)
        self.line2= cmds.textFieldButtonGrp(self.txtTarAttr, q=1,tx=1)
        self.line3= cmds.textFieldButtonGrp(self.txtRevTarAttr, q=1,tx=1)
        self.sear= cmds.textFieldGrp(self.txtSear, q=1, tx=1)
        self.repl= cmds.textFieldGrp(self.txtRepl, q=1, tx=1) 

    def grab1(self, txt):  
        mainCB= cmds.channelBox("mainChannelBox", sma=1, q=1)
        hisCB= cmds.channelBox("mainChannelBox", sha=1, q=1)
        outCB= cmds.channelBox("mainChannelBox", soa=1, q=1) 
        sub1, sub2, sub3= 0, 0, 0
        if mainCB:
            sub1=1      
        if hisCB:
            sub2=1      
        if outCB:
            sub3=1 
        subAll= sub1 + sub2 + sub3
        if subAll==1:
            if mainCB:   
                cmds.textFieldButtonGrp(txt, e=1, tx=", ".join(mainCB))        
            if hisCB:   
                cmds.textFieldButtonGrp(txt, e=1, tx=", ".join(hisCB))         
            if outCB:   
                cmds.textFieldButtonGrp(txt, e=1, tx=", ".join(outCB))                  
        elif subAll>1:
            cmds.warning("Please select only 1 section of attribute") 
        else:
            cmds.warning("Please select at least 1 attribute")            

    def grab2(self, txt):
        tranObj= cmds.ls(sl=1, tr=1)
        allObj= cmds.ls(sl=1)
        obj=[]
        #This is to grab the history, instead of the object itself
        if tranObj!=allObj:
            if tranObj:
                #But if select multiple target and 1 history, will ignore the history
                if len(tranObj)>1:
                    obj= tranObj
                else:
                    for item in allObj:
                        if item not in tranObj:
                            obj.append(item)
            else:
                obj=allObj
        else:
            obj=allObj
        if obj:      
            cmds.textFieldButtonGrp(txt, e=1, tx=", ".join(obj))                           
        else:
            cmds.warning("Please select at least 1 target")   
      
    def cbx1(self):
        if cmds.checkBoxGrp(self.cbSour, q=1, v1=1):  
            cmds.textFieldButtonGrp(self.txtSour, e=1, en=1)
            cmds.text(self.txt1, e=1, l="Select TARGETS")
            cmds.text(self.txt2, e=1, l="Select NOTHING")
            cmds.text(self.txt4, e=1, l="Select NOTHING")
        else:  
            cmds.textFieldButtonGrp(self.txtSour, e=1, en=0)
            cmds.text(self.txt1, e=1, l="Select SOURCE then TARGETS")
            cmds.text(self.txt2, e=1, l="Select SOURCE")
            cmds.text(self.txt4, e=1, l="Select SOURCE")

    def cbx2(self):
        if cmds.checkBoxGrp(self.cbTar, q=1, v1=1):  
            for txt in (self.txtTar, self.txtRevTar, self.txtRevTarAttr):
                cmds.textFieldButtonGrp(txt, e=1, en=1)
            cmds.button(self.bSwitch, e=1, en=1)
            cmds.textFieldGrp(self.txtSear, e=1, en=0)
            cmds.textFieldGrp(self.txtRepl, e=1, en=0) 
            cmds.checkBoxGrp(self.cbSR, e=1, v1=0)
        else:  
            for txt in (self.txtTar, self.txtRevTar, self.txtRevTarAttr):
                cmds.textFieldButtonGrp(txt, e=1, en=0)
            cmds.button(self.bSwitch, e=1, en=0)

    def cbx3(self):
        if cmds.checkBoxGrp(self.cbSR, q=1, v1=1):   
            for txt in (self.txtTar, self.txtRevTar, self.txtRevTarAttr):  
                cmds.textFieldButtonGrp(txt, e=1, en=0)  
            cmds.textFieldGrp(self.txtSear, e=1, en=1)
            cmds.textFieldGrp(self.txtRepl, e=1, en=1)
            cmds.checkBoxGrp(self.cbTar, e=1, v1=0)
            cmds.button(self.bSwitch, e=1, en=0)   
        else:  
            cmds.textFieldGrp(self.txtSear, e=1, en=0)
            cmds.textFieldGrp(self.txtRepl, e=1, en=0) 

    def cbx4(self):
        if cmds.checkBoxGrp(self.cbMult, q=1, v1=1):  
            cmds.floatFieldGrp(self.mult, e=1, en=1) 
        else:
            cmds.floatFieldGrp(self.mult, e=1, en=0)  

    def switch(self, txt1, txt2):
        line1= cmds.textFieldButtonGrp(txt1, q=1, tx=1)
        line2= cmds.textFieldButtonGrp(txt2, q=1, tx=1) 
        cmds.textFieldButtonGrp(txt1, e=1, tx="%s"%line2)
        cmds.textFieldButtonGrp(txt2, e=1, tx="%s"%line1)  

    def connPreTest(self, tar, line1, line2):
        test1= 1
        for attr1, attr2 in zip(line1.split(", "), line2.split(",")):
            connect1= cmds.listConnections("%s.%s"%(tar,attr2), p=1, d=0, scn=1)
            if connect1:
                test1= []       
        return test1 

    def conn(self, sour, tar, line1, line2, meth, rev):
        if meth==2:
            for attrs in line2.split(", "):
                dis= cmds.listConnections("%s.%s"%(tar,attrs), p=1)
                if dis:
                    cmds.disconnectAttr(dis[0], "%s.%s"%(tar,attrs))
        for attr1, attr2 in zip(line1.split(", "), line2.split(",")):
            if rev==0:
                if cmds.checkBoxGrp(self.cbMult, q=1, v1=1): 
                    mul= cmds.floatFieldGrp(self.mult, q=1, v1=1)
                    md= cmds.createNode("multiplyDivide", n="%s_%s_md"%(sour,attr1))
                    cmds.setAttr("%s.input2X"%md, mul)
                    cmds.connectAttr("%s.%s"%(sour, attr1), "%s.input1X"%md) 
                    cmds.connectAttr("%s.outputX"%md, "%s.%s"%(tar, attr2), f=1) 
                else:
                    cmds.connectAttr("%s.%s"%(sour, attr1), "%s.%s"%(tar, attr2), f=1)
            else:
                if cmds.checkBoxGrp(self.cbMult, q=1, v1=1): 
                    mul= cmds.floatFieldGrp(self.mult, q=1, v1=1)
                    md= cmds.createNode("multiplyDivide", n="%s_%s_md"%(sour,attr1))
                    cmds.setAttr("%s.input2X"%md, mul)
                    rev= cmds.createNode("reverse", n="%s_%s_rev"%(sour,attr1))
                    cmds.connectAttr("%s.%s"%(sour, attr1), "%s.input1X"%md) 
                    cmds.connectAttr("%s.outputX"%md, "%s.inputX"%rev) 
                    cmds.connectAttr("%s.outputX"%rev, "%s.%s"%(tar, attr2), f=1)                  
                else:
                    rev= cmds.createNode("reverse", n="%s_%s_rev"%(sour,attr1))
                    cmds.connectAttr("%s.%s"%(sour, attr1), "%s.inputX"%rev) 
                    cmds.connectAttr("%s.outputX"%rev, "%s.%s"%(tar, attr2))  

    def negate(self, sour, tar, meth):
        if meth==3:
            dcm= cmds.createNode("decomposeMatrix", n="%s_tran_dcm"%sour)
            cmds.connectAttr("%s.inverseMatrix"%sour, "%s.inputMatrix"%dcm)
            for attr in ("X","Y","Z"):
                cmds.connectAttr("%s.outputTranslate%s"%(dcm,attr), "%s.translate%s"%(tar,attr))
        elif meth==4:
            dcm= cmds.createNode("decomposeMatrix", n="%s_rot_dcm"%sour)
            cmds.connectAttr("%s.inverseMatrix"%sour, "%s.inputMatrix"%dcm)
            for attr in ("X","Y","Z"):
                cmds.connectAttr("%s.outputRotate%s"%(dcm,attr), "%s.rotate%s"%(tar,attr))

    def final(self, meth):  
        self.defi()
        test1,test2,test3,test4,test5,testSour,allGood= 1,1,1,1,1,1,1
        finalTar=[]
        if meth==3: 
            self.line1=self.line2= "tx, ty, tz"
        elif meth==4:
            self.line1=self.line2= "rx, ry, rz"
        if self.line1 and self.line2:
            if len(self.line1.split(", "))==len(self.line2.split(", ")):
                if cmds.checkBoxGrp(self.cbSour, q=1, v1=1):
                    tempSour= cmds.textFieldButtonGrp(self.txtSour, q=1, tx=1)
                    if tempSour:
                        sour=[]
                        for item in tempSour.split(", "):
                            sour.append(item)
                    else:
                        testSour=[]
                        cmds.warning("<SOURCE> textfield is empty!")
                else:
                    sour= self.obj
                    if self.obj==[]:
                        testSour=[]
                        cmds.warning("Please select at least 1 OBJECT(Source)") 
                if testSour:       
                    if cmds.checkBoxGrp(self.cbSR, q=1, v1=1):
                        if self.sear:
                            conti, finalTar= self.dialogClass.sameNameOrNoExistDialog(sour, self.sear, self.repl)
                            if conti:
                                if meth!=2:
                                    for item in sour:
                                        preTest= self.connPreTest(item.replace(self.sear, self.repl), self.line1, self.line2)
                                        if preTest==[]:
                                            allGood=[]
                                if allGood:
                                    self.uiStuffClass.loadingBar(1, len(sour))
                                    for item in sour:
                                        if meth==1 or meth==2:
                                            self.conn(item, item.replace(self.sear, self.repl), self.line1, self.line2, meth, 0) 
                                        else:
                                            self.negate(item, item.replace(self.sear, self.repl), meth)
                                        finalTar.append(item)
                                        self.uiStuffClass.loadingBar(2)
                                    self.uiStuffClass.loadingBar(3, sel=sour)
                                else:
                                    cmds.warning("One of the target's attribute is already CONNECTED")    
                        else:
                            cmds.warning("<SEARCH> or <REPLACE> textfield is empty!")                                        
                    elif cmds.checkBoxGrp(self.cbTar, q=1, v1=1):
                        tar= cmds.textFieldButtonGrp(self.txtTar, q=1, tx=1)
                        rev= cmds.textFieldButtonGrp(self.txtRevTar, q=1, tx=1)
                        if tar or rev:
                            if rev and self.line3=="":
                                cmds.warning("<REVERSE ATTR> textfield is empty!")
                            else:
                                for item in sour:
                                    if item in tar.split(", "):
                                        test3= []
                                    if item in rev.split(", "):
                                        test4= []
                                if test3 and test4:
                                    for item in tar.split(", "):
                                        if item in rev.split(", "):
                                            test1=[]
                                    for stuff in rev.split(", "):
                                        if stuff in tar.split(", "):
                                            test2=[]
                                    if test1 and test2:    
                                        if meth!=2:    
                                            if tar:  
                                                for item in tar.split(", "): 
                                                    preTest= self.connPreTest(item, self.line1, self.line2)
                                                    if preTest==[]:
                                                        allGood=[]
                                            if rev:    
                                                for stuff in rev.split(", "):
                                                    preTest= self.connPreTest(stuff, self.line1, self.line2)
                                                    if preTest==[]:
                                                        allGood=[]
                                        if allGood:
                                            if tar:
                                                ans1= len(tar.split(", "))
                                            else:
                                                ans1= 0
                                            if rev:
                                                ans2= len(rev.split(", "))
                                            else:
                                                ans2= 0 
                                            if len(sour)==1:
                                                self.uiStuffClass.loadingBar(1, (ans1+ans2))      
                                                if tar:  
                                                    for item in tar.split(", "): 
                                                        if meth==1 or meth==2:
                                                            self.conn(sour[0], item, self.line1, self.line2, meth, 0)
                                                        else:
                                                            self.negate(sour[0], item, meth)
                                                        self.uiStuffClass.loadingBar(2) 
                                                if rev:    
                                                    for stuff in rev.split(", "):
                                                        if meth==1 or meth==2:
                                                            self.conn(sour[0], stuff, self.line1, self.line3, meth, 1)
                                                        else:
                                                            self.negate(sour[0], stuff, meth)
                                                        self.uiStuffClass.loadingBar(2)
                                                self.uiStuffClass.loadingBar(3, sel=sour) 
                                            else:
                                                if tar:
                                                    if len(sour)!=len(tar.split(", ")):
                                                        test5=[]
                                                if rev:
                                                    if len(sour)!=len(rev.split(", ")):
                                                        test5=[]
                                                if test5:
                                                    self.uiStuffClass.loadingBar(1, (ans1+ans2))  
                                                    if tar:
                                                        for thing, item in zip(sour, tar.split(", ")):
                                                            if meth==1 or meth==2: 
                                                                self.conn(thing, item, self.line1, self.line2, meth, 0)
                                                            else:
                                                                self.negate(thing, item, meth)
                                                            self.uiStuffClass.loadingBar(2)
                                                    if rev:
                                                        for thing, stuff in zip(sour, rev.split(", ")):
                                                            if meth==1 or meth==2: 
                                                                self.conn(thing, stuff, self.line1, self.line3, meth, 1)
                                                            else:
                                                                self.negate(thing, stuff, meth)  
                                                            self.uiStuffClass.loadingBar(2)
                                                    self.uiStuffClass.loadingBar(3, sel=sour)                                                    
                                                else:
                                                    cmds.warning("<SOURCE> and <TARGET> must be the same amount! (<REVERSE TAR> too if got)")
                                        else:
                                            cmds.warning("One of the target's attribute is already CONNECTED")
                                    else:
                                        cmds.warning("<TARGET> textfield and <REVERSE TAR> textfield have same object")
                                else:
                                    if cmds.checkBoxGrp(self.cbSour, q=1, v1=1):
                                        cmds.warning("One of the <SOURCE> textfield have same object in <TARGET> or <REVERSE TAR> textfield ")
                                    else:
                                        cmds.warning("One of the selected object same with <TARGET> or <REVERSE TAR> textfield")
                        else:
                            cmds.warning("<TARGET> textfield is empty!")
                    else:
                        if cmds.checkBoxGrp(self.cbSour, q=1, v1=1):
                            if self.obj:
                                for item in sour:
                                    if item in self.obj:
                                        test1= []        
                                if test1:
                                    if len(sour)>1:
                                        if len(sour)!=len(self.obj):
                                            test2= []
                                    if test2:
                                        if meth!=2:
                                            for item in sour:
                                                preTest= self.connPreTest(item, self.line1, self.line2)
                                                if preTest==[]:
                                                    allGood=[]

                                        if allGood:
                                            self.uiStuffClass.loadingBar(1, len(self.obj))                                               
                                            for item,stuff in zip(self.obj,sour):
                                                if meth==1 or meth==2:
                                                    self.conn(stuff, item, self.line1, self.line2, meth, 0) 
                                                else:
                                                    self.negate(stuff, item, meth)
                                                self.uiStuffClass.loadingBar(2)
                                            self.uiStuffClass.loadingBar(3, sel=self.obj)      
                                        else:
                                            cmds.warning("One of the target's attribute is already CONNECTED")
                                    else:
                                        cmds.warning("number of <SOURCE> is not the same as selected target, unless only have 1 <SOURCE>")
                                else:
                                    cmds.warning("One of the selected object same with <SOURCE> textfield")
                            else:
                                cmds.warning("Please select at least 1 TARGET")
                        else:
                            if len(self.obj)>1:
                                if meth!=2:
                                    for item in self.obj:
                                        if item!=self.obj[0]:
                                            preTest= self.connPreTest(item, self.line1, self.line2)
                                            if preTest==[]:
                                                allGood=[]
                                if allGood:
                                    self.uiStuffClass.loadingBar(1, len(self.obj)-1) 
                                    for item in self.obj:
                                        if item!=self.obj[0]:
                                            if meth==1 or meth==2:
                                                self.conn(self.obj[0], item, self.line1, self.line2, meth, 0) 
                                            else:
                                                self.negate(self.obj[0], item, meth)
                                            self.uiStuffClass.loadingBar(2)
                                    self.uiStuffClass.loadingBar(3, sel=self.obj) 
                                else:
                                    cmds.warning("One of the target's attribute is already CONNECTED")
                            else:
                                cmds.warning("Please select at least 2 object (1 source, 1+ targets)")  
            else:
                cmds.warning("The amount for <SOURCE ATTR> & <TARGET ATTR> must be SAME")                     
        else:
            cmds.warning("Either <SOURCE ATTR> or <TARGET ATTR> textfield are empty!")

    def helps(self):
        name="Help On ConnectAttribute"
        helpTxt="""
        - Connects one attribute to another without using "Connection Editor"



        A) Attribute
        ==================
            1. Choose which attribute to connect from and to (can be different type but amount must be same)
            (*eg. tx,ty,tz > rx,ry,rz  3 to 3) 


        B) Source
        ================== 
            1. If 1 source, then connect 1 source to all target
            2. If multiple source, then connect by zip. 1 source to 1 target


        C) Target
        ==================
            1. To connect multiple TARGET
            2. <Reverse> simply connect to a reverse node 
                (* Reverse is not negative multiply divide)
                (* usually use when connect enum or visibility)       


        D) Search & Replace
        ====================== 
            1. To connect multiple SOURCE to multiple TARGET
                (*<Targets> and <Search Replace> cannot use simultaneously)    


        E) Multiply
        ==================
            - Each attribute is linked to a multiply divide node
            (*eg. translateX,Y,Z each will have 1 multiply divide node)    


        F) Force Connect
        ==================
            - Disconnect existing connection and connect whatever that you want 
            (* because the flag f=1 won't work if it already connected to what you want)  


        F) Negate
        ==================
            - Connect inverse Matrix        
        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)


    def reloadSub(self):
        ConnAttr()  
    
                          
if __name__=='__main__':
    ConnAttr()



