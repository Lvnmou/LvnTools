import maya.cmds as cmds
import Mod.uiStuff as uiStuff
import Mod.dialog as dialog
import Mod.helpBox as helpBox
import re


class Attribute(object):
    def __init__(self, *args):
        self.uiStuffClass= uiStuff.UiStuff()
        self.dialogClass= dialog.Dialog()        
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):
        try:
            cmds.deleteUI("attrs")
        except:
            pass          
        cmds.window("attrs", mb=1)
        cmds.window("attrs",t="Attributes", e=1, s=1, wh=(370,460))     
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Attributes", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Attributes", c=lambda x:self.reloadSub())     
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Create")
        form11= cmds.formLayout(nd=100, p=column1)
        self.txtFAttr= cmds.textFieldGrp(l="Attr Name :", pht="<attr1, attr2, ...>", cw2=(60,60), adj=2)
        self.ffMin= cmds.floatFieldGrp(l="Min :", v1=0, en=0, cw2=(28,50), adj=2, pre=2)
        self.cbMin= cmds.checkBoxGrp(cc=lambda x:self.cbx11(self.cbMin, self.ffMin))
        self.ffMax= cmds.floatFieldGrp(l="Max :", v1=10, en=0, cw2=(28,50), adj=2, pre=2)   
        self.cbMax= cmds.checkBoxGrp(cc=lambda x:self.cbx11(self.cbMax, self.ffMax))   
        self.txtFEnum= cmds.textFieldGrp(l="Enum Value :", tx="Hide:Show:", pht="<Hide:Show:....>", cw2=(70,60), adj=2)
        txt111= cmds.text(l="Select OBJECTS", fn="smallObliqueLabelFont", en=0)
        b111= cmds.button(l="Integer", c=lambda x:self.createAttr(1))
        b112= cmds.button(l="Float", c=lambda x:self.createAttr(2))
        b113= cmds.button(l="Vector", c=lambda x:self.createAttr(3))
        b114= cmds.button(l="Enum", c=lambda x:self.createAttr(4))
        b115= cmds.button(l="Boolean", c=lambda x:self.createAttr(5))
        cmds.formLayout(form11, e=1,
                                af=[(txt111, "top", 0),
                                    (self.txtFAttr, "top", 15),
                                    (self.ffMin, "top", 41),
                                    (self.cbMin, "top", 45),
                                    (self.ffMax, "top", 41),
                                    (self.cbMax, "top", 45),
                                    (self.txtFEnum, "top", 67),
                                    (b111, "top", 105),
                                    (b112, "top", 105),
                                    (b113, "top", 105),
                                    (b114, "top", 131),
                                    (b115, "top", 131)],
                                ap=[(self.txtFAttr, "left", 0, 0),
                                    (self.txtFAttr, "right", 0, 100),
                                    (self.cbMin, "left", 90, 0),
                                    (self.ffMax, "right", 25, 100),  
                                    (self.cbMax, "right", 5, 100),  
                                    (self.txtFEnum, "left", 0, 0),
                                    (self.txtFEnum, "right", 0, 100),
                                    (txt111, "left", 0, 0),
                                    (txt111, "right", 0, 100),
                                    (b111, "left", 0, 0),
                                    (b111, "right", 0, 33),
                                    (b112, "left", 0, 34),
                                    (b112, "right", 0, 66),
                                    (b113, "left", 0, 67),
                                    (b113, "right", 0, 100),
                                    (b114, "left", 0, 0),
                                    (b114, "right", 0, 50),
                                    (b115, "left", 0, 51),
                                    (b115, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column12= self.uiStuffClass.sepBoxSub()
        form12= cmds.formLayout(nd=100, p=column12)
        txt121= cmds.text(l="Select ATTRIBUTES", fn="smallObliqueLabelFont", en=0)
        b120= cmds.button(l="UnKeyable", c=lambda x:self.attrSet(1))
        b121= cmds.button(l="Lock", c=lambda x:self.attrSet(2))
        b122= cmds.button(l="Lock and Hide", c=lambda x:self.attrSet(3))
        b123= cmds.button(l="Unlock and Keyable", c=lambda x:self.attrSet(4))
        b124= cmds.button(l="Unlock All Custom", c=lambda x:self.attrSet(5))
        b125= cmds.button(l="Delete Attributes", c=lambda x:self.attrSet(6))
        b126= cmds.button(l="Up", c=lambda x:self.attrUpDown(1))
        b127= cmds.button(l="Down", c=lambda x:self.attrUpDown(2)) 
        b128= cmds.button(l="Top", c=lambda x:self.attrUpDown(3))
        b129= cmds.button(l="Bottom", c=lambda x:self.attrUpDown(4))  
        cmds.formLayout(form12, e=1,
                                af=[(txt121, "top", 0),
                                    (b120, "top", 20),
                                    (b121, "top", 20),
                                    (b122, "top", 20),
                                    (b123, "top", 46),
                                    (b124, "top", 46),
                                    (b125, "top", 72),
                                    (b126, "top", 108),
                                    (b127, "top", 108),
                                    (b128, "top", 108),
                                    (b129, "top", 108)],
                                ap=[(txt121, "left", 0, 0),
                                    (txt121, "right", 0, 100),                                    
                                    (b120, "left", 0, 0),
                                    (b120, "right", 0, 33),
                                    (b121, "left", 0, 34),
                                    (b121, "right", 0, 66),
                                    (b122, "left", 0, 67),
                                    (b122, "right", 0, 100),
                                    (b123, "left", 0, 0),
                                    (b123, "right", 0, 50),
                                    (b124, "left", 0, 51),
                                    (b124, "right", 0, 100),
                                    (b125, "left", 0, 0),
                                    (b125, "right", 0, 100),                                    
                                    (b126, "left", 0, 0),
                                    (b126, "right", 0, 25),
                                    (b127, "left", 0, 26),
                                    (b127, "right", 0, 50),
                                    (b128, "left", 0, 51),
                                    (b128, "right", 0, 75),
                                    (b129, "left", 0, 76),
                                    (b129, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column21= self.uiStuffClass.sepBoxSub("Edit")
        form21= cmds.formLayout(nd=100, p=column21)
        txt211= cmds.text(l="Select at least 3 :      TARGETS / SOURCE / ATTRIBUTE", fn="smallObliqueLabelFont", en=0)    
        b211= cmds.button(l="Copy", c=lambda x:self.copyMoveAttr(1)) 
        b212= cmds.button(l="Move", c=lambda x:self.copyMoveAttr(2))
        cmds.formLayout(form21, e=1,
                                af=[(txt211, "top", 0),
                                    (b211, "top", 16),
                                    (b212, "top", 16)],
                                ap=[(txt211, "left", 0, 0),
                                    (txt211, "right", 0, 100),
                                    (b211, "left", 0, 1),
                                    (b211, "right", 0, 50),
                                    (b212, "left", 0, 51),
                                    (b212, "right", 0, 99)])   
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column22= self.uiStuffClass.sepBoxSub()
        form22= cmds.formLayout(nd=100, p=column22)
        txt221= cmds.text(l="Select ATTRIBUTES", fn="smallObliqueLabelFont", en=0)    
        self.txtFAttrName= cmds.textFieldGrp(l="Attr Name :", cw2=(60,60), adj=2)
        b221= cmds.button(l="Rename Attr", c=lambda x:self.attrRen(1))
        self.txtFEnumName= cmds.textFieldGrp(l="Enum Name :", cw2=(70,60), adj=2, pht="<enum1:enum2:enum3>")
        b222= cmds.button(l="Rename Enum Value", c=lambda x:self.attrRen(2))
        sep22= cmds.separator(h=20, st="in")  
        self.txtFSear= cmds.textFieldGrp(l="Search :", cw2=(60,60), adj=2)
        self.txtFRepl= cmds.textFieldGrp(l="Replace :", cw2=(60,60), adj=2)
        b223= cmds.button(l="Replace Attr", c=lambda x:self.attrSR(1))
        b224= cmds.button(l="Replace Enum Value", c=lambda x:self.attrSR(2))
        cmds.formLayout(form22, e=1,
                                af=[(txt221, "top", 0),
                                    (self.txtFAttrName, "top", 16),
                                    (b221, "top", 42),
                                    (self.txtFEnumName, "top", 78),
                                    (b222, "top", 104),
                                    (sep22, "top", 137),
                                    (self.txtFSear, "top", 164),
                                    (self.txtFRepl, "top", 190),
                                    (b223, "top", 216),
                                    (b224, "top", 216)],
                                ap=[(txt221, "left", 0, 0),
                                    (txt221, "right", 0, 100),
                                    (self.txtFAttrName, "left", 0, 0),
                                    (self.txtFAttrName, "right", 0, 100),
                                    (b221, "left", 0, 0),
                                    (b221, "right", 0, 100),
                                    (self.txtFEnumName, "left", 0, 0),
                                    (self.txtFEnumName, "right", 0, 100),                                    
                                    (b222, "left", 0, 0),
                                    (b222, "right", 0, 100),
                                    (sep22, "left", 0, 0),
                                    (sep22, "right", 0, 100),
                                    (self.txtFSear, "left", 0, 0),
                                    (self.txtFSear, "right", 0, 100),
                                    (self.txtFRepl, "left", 0, 0),
                                    (self.txtFRepl, "right", 0, 100),
                                    (b223, "left", 0, 0),
                                    (b223, "right", 0, 50),
                                    (b224, "left", 0, 51),
                                    (b224, "right", 0, 100)])         
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column31= self.uiStuffClass.sepBoxSub("Limiter")
        form31= cmds.formLayout(nd=100, p=column31)
        b311= cmds.button(l="Search Limit", c=lambda x:self.searchL()) 
        txt311= cmds.text(l="TRANSLATE")
        txt312= cmds.text(l="ROTATE") 
        txt313= cmds.text(l="SCALE") 
        sep311= cmds.separator(h=5, st="in") 
        sep312= cmds.separator(h=5, st="in")
        sep313= cmds.separator(h=5, st="in")
        txt31m1= cmds.text(l="  Min", en=0) 
        txt31m2= cmds.text(l="  Max", en=0) 
        txt31m3= cmds.text(l="  Min", en=0) 
        txt31m4= cmds.text(l="  Max", en=0) 
        txt31m5= cmds.text(l="  Min", en=0) 
        txt31m6= cmds.text(l="  Max", en=0) 
        txt314= cmds.text(l="X : ")
        txt315= cmds.text(l="Y : ")
        txt316= cmds.text(l="Z : ")
        self.minTx= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.maxTx= cmds.textFieldGrp(adj=1, cw=(1,40))    
        self.minRx= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.maxRx= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.minSx= cmds.textFieldGrp(adj=1, cw=(1,40))    
        self.maxSx= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.minTy= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.maxTy= cmds.textFieldGrp(adj=1, cw=(1,40))    
        self.minRy= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.maxRy= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.minSy= cmds.textFieldGrp(adj=1, cw=(1,40))    
        self.maxSy= cmds.textFieldGrp(adj=1, cw=(1,40))       
        self.minTz= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.maxTz= cmds.textFieldGrp(adj=1, cw=(1,40))    
        self.minRz= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.maxRz= cmds.textFieldGrp(adj=1, cw=(1,40))
        self.minSz= cmds.textFieldGrp(adj=1, cw=(1,40))    
        self.maxSz= cmds.textFieldGrp(adj=1, cw=(1,40))  
        b312= cmds.button(l="Set Limit", c=lambda x:self.setL()) 
        cmds.formLayout(form31, e=1,
                                af=[(b311, "top", 0),
                                    (txt311, "top", 35),
                                    (txt312, "top", 35),
                                    (txt313, "top", 35),
                                    (sep311, "top", 50),
                                    (sep312, "top", 50),
                                    (sep313, "top", 50),                                    
                                    (txt31m1, "top", 55),
                                    (txt31m2, "top", 55),
                                    (txt31m3, "top", 55),
                                    (txt31m4, "top", 55),
                                    (txt31m5, "top", 55),   
                                    (txt31m6, "top", 55),                                     
                                    (txt314, "top", 70),
                                    (txt315, "top", 93),   
                                    (txt316, "top", 116), 
                                    (self.minTx, "top", 68),
                                    (self.maxTx, "top", 68),
                                    (self.minRx, "top", 68),
                                    (self.maxRx, "top", 68),
                                    (self.minSx, "top", 68),
                                    (self.maxSx, "top", 68),
                                    (self.minTy, "top", 91),
                                    (self.maxTy, "top", 91),
                                    (self.minRy, "top", 91),
                                    (self.maxRy, "top", 91),
                                    (self.minSy, "top", 91),
                                    (self.maxSy, "top", 91),
                                    (self.minTz, "top", 114),
                                    (self.maxTz, "top", 114),
                                    (self.minRz, "top", 114),
                                    (self.maxRz, "top", 114),
                                    (self.minSz, "top", 114),
                                    (self.maxSz, "top", 114),
                                    (b312, "top", 140)],
                                ap=[(b311, "left", 0, 0),
                                    (b311, "right", 0, 100),
                                    (txt311, "left", 0, 9),
                                    (txt311, "right", 0, 33),
                                    (txt312, "left", 0, 40),
                                    (txt312, "right", 0, 64),
                                    (txt313, "left", 0, 71),
                                    (txt313, "right", 0, 96),
                                    (sep311, "left", 0, 9),
                                    (sep311, "right", 0, 33),
                                    (sep312, "left", 0, 40),
                                    (sep312, "right", 0, 64),
                                    (sep313, "left", 0, 71),
                                    (sep313, "right", 0, 96),
                                    (txt31m1, "left", 0, 9),
                                    (txt31m1, "right", 0, 20),
                                    (txt31m2, "left", 0, 22),
                                    (txt31m2, "right", 0, 33),
                                    (txt31m3, "left", 0, 40),
                                    (txt31m3, "right", 0, 51),
                                    (txt31m4, "left", 0, 53),
                                    (txt31m4, "right", 0, 64),
                                    (txt31m5, "left", 0, 71),
                                    (txt31m5, "right", 0, 82),
                                    (txt31m6, "left", 0, 84),
                                    (txt31m6, "right", 0, 96),   
                                    (txt314, "left", 0, 3),
                                    (txt314, "right", 0, 7),
                                    (txt315, "left", 0, 3),
                                    (txt315, "right", 0, 7),
                                    (txt316, "left", 0, 3),
                                    (txt316, "right", 0, 7),
                                    (self.minTx, "left", 0, 9),
                                    (self.minTx, "right", 0, 20),
                                    (self.maxTx, "left", 0, 22),
                                    (self.maxTx, "right", 0, 33),
                                    (self.minRx, "left", 0, 40),
                                    (self.minRx, "right", 0, 51),
                                    (self.maxRx, "left", 0, 53),
                                    (self.maxRx, "right", 0, 64),
                                    (self.minSx, "left", 0, 71),
                                    (self.minSx, "right", 0, 82),
                                    (self.maxSx, "left", 0, 84),
                                    (self.maxSx, "right", 0, 96),
                                    (self.minTy, "left", 0, 9),
                                    (self.minTy, "right", 0, 20),
                                    (self.maxTy, "left", 0, 22),
                                    (self.maxTy, "right", 0, 33),
                                    (self.minRy, "left", 0, 40),
                                    (self.minRy, "right", 0, 51),
                                    (self.maxRy, "left", 0, 53),
                                    (self.maxRy, "right", 0, 64),
                                    (self.minSy, "left", 0, 71),
                                    (self.minSy, "right", 0, 82),
                                    (self.maxSy, "left", 0, 84),
                                    (self.maxSy, "right", 0, 96),
                                    (self.minTz, "left", 0, 9),
                                    (self.minTz, "right", 0, 20),
                                    (self.maxTz, "left", 0, 22),
                                    (self.maxTz, "right", 0, 33),
                                    (self.minRz, "left", 0, 40),
                                    (self.minRz, "right", 0, 51),
                                    (self.maxRz, "left", 0, 53),
                                    (self.maxRz, "right", 0, 64),
                                    (self.minSz, "left", 0, 71),
                                    (self.minSz, "right", 0, 82),
                                    (self.maxSz, "left", 0, 84),
                                    (self.maxSz, "right", 0, 96),                                   
                                    (b312, "left", 0, 0),
                                    (b312, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column32= self.uiStuffClass.sepBoxSub()
        form32= cmds.formLayout(nd=100, p=column32)
        txt321= cmds.text(l="*Able to SET multiple custom attribute limit but GET only 1", fn="smallObliqueLabelFont", en=0)    
        b321= cmds.button(l="Search Custom Limit", c=lambda x:self.searchCL())
        txt322= cmds.text(l="  Min", en=0) 
        txt323= cmds.text(l="  Max", en=0) 
        self.minC= cmds.textFieldGrp(l="Custom :", adj=2, cw2=(50,40))     
        self.maxC= cmds.textFieldGrp(adj=1, cw=(1,40)) 
        b322= cmds.button(l="Set Custom Limit", c=lambda x:self.setCL()) 
        cmds.formLayout(form32, e=1,
                                af=[(txt321, "top", 0), 
                                    (b321, "top", 16),
                                    (txt322, "top", 45),
                                    (txt323, "top", 45),
                                    (self.minC, "top", 60),
                                    (self.maxC, "top", 60),
                                    (b322, "top", 90)],
                                ap=[(txt321, "left", 0, 0),
                                    (txt321, "right", 0, 100),
                                    (b321, "left", 0, 0),
                                    (b321, "right", 0, 100),
                                    (txt322, "left", 0, 21),
                                    (txt322, "right", 0, 50),
                                    (txt323, "left", 0, 51),
                                    (txt323, "right", 0, 77),
                                    (self.minC, "left", 0, 11),
                                    (self.minC, "right", 0, 50),
                                    (self.maxC, "left", 0, 51),
                                    (self.maxC, "right", 0, 77),
                                    (b322, "left", 0, 0),
                                    (b322, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column41= self.uiStuffClass.sepBoxSub("Unhider")
        form41= cmds.formLayout(nd=100, p=column41)
        self.rb41= cmds.radioButtonGrp(cw4=(10,90,110,10), l="", la3=["All", "Radius", "Individual"], nrb=3, sl=1, cc=lambda x: self.rb())
        sep41= cmds.separator(h=15, st="in")
        self.cb41= cmds.checkBoxGrp(ncb=4, l="", la4=["Visibility","Translate","Rotate","Scale"], va4=[1,1,1,1], cw5=(10,80,90,70,10), cc=lambda x: self.cbx41())
        b411= cmds.button(l="Unhide All", c=lambda x: self.unlockFromCc()) 
        cmds.formLayout(form41, e=1,
                                af=[(self.rb41, "top", 0),
                                    (sep41, "top", 20),
                                    (self.cb41, "top", 40),
                                    (b411, "top", 76)],
                                ap=[(sep41, "left", 0, 0),
                                    (sep41, "right", 0, 100),
                                    (b411, "left", 0, 0),
                                    (b411, "right", 0, 100)])    
        cmds.setFocus(cmds.text(l=""))    
        cmds.showWindow("attrs")

    def cbx11(self, cb, ff):
        if cmds.checkBoxGrp(cb, q=1, v1=1):
            cmds.floatFieldGrp(ff, e=1, en=1)   
        else:
            cmds.floatFieldGrp(ff, e=1, en=0)    

    def rb(self):
        if cmds.radioButtonGrp(self.rb41, q=1, sl=1)==1:
            cmds.checkBoxGrp(self.cb41, e=1, v1=1, v2=1, v3=1, v4=1)
        elif cmds.radioButtonGrp(self.rb41, q=1, sl=1)==2:
            cmds.checkBoxGrp(self.cb41, e=1, v1=0, v2=0, v3=0, v4=0) 
        else:
            cmds.checkBoxGrp(self.cb41, e=1, v1=1, v2=0, v3=0, v4=0)                    
        
    def cbx41(self):
        if cmds.checkBoxGrp(self.cb41, q=1, v1=1) or cmds.checkBoxGrp(self.cb41, q=1, v2=1) or cmds.checkBoxGrp(self.cb41, q=1, v3=1) or cmds.checkBoxGrp(self.cb41, q=1, v4=1):
            cmds.radioButtonGrp(self.rb41, e=1, sl=3)     

    def checkName(self, test, attr, obj):
        if cmds.attributeQuery(attr, node=obj, ex=1):
            test= []
        else:
            #Test for vector
            if cmds.attributeQuery("%sX"%attr, node=obj, ex=1):
                test= []
            elif cmds.attributeQuery("%sY"%attr, node=obj, ex=1):
                test= []
            elif cmds.attributeQuery("%sZ"%attr, node=obj, ex=1):
                test= []       
        return test 

    def checkNameNSpace(self, attr, obj, test1, test2, meth=1, sel=[]):
        realAttr= []
        for thing in attr.split(", "):
            for stuff in thing.split(","):
                if " " in stuff:
                    test1= []
                else:
                    for item in obj:
                        if meth==1:
                            test2= self.checkName(test2, stuff, item) 
                        elif meth==2:
                            if len(sel)==1:
                                test2= self.checkName(test2, stuff, item) 
                            elif len(sel)>2:
                                for x in range(1, len(sel)+1):
                                    test2= self.checkName(test2, "%s%s"%(stuff,x), item)
                    realAttr.append(stuff)
        return test1, test2, realAttr

    def createAttr(self, meth):
        obj= cmds.ls(sl=1)
        attrName= cmds.textFieldGrp(self.txtFAttr, q=1 ,tx=1)   
        minV= cmds.floatFieldGrp(self.ffMin, q=1, v1=1)
        maxV= cmds.floatFieldGrp(self.ffMax, q=1, v1=1)    
        cbxMin= cmds.checkBoxGrp(self.cbMin, q=1, v1=1) 
        cbxMax= cmds.checkBoxGrp(self.cbMax, q=1, v1=1)         
        enumVal= cmds.textFieldGrp(self.txtFEnum, q=1, tx=1)
        if obj:
            if attrName:
                test1, test2, test3= 1,1,1
                test1, test3, realAttr= self.checkNameNSpace(attrName, obj, test1, test3)
                if test1:
                    if test3:
                        self.uiStuffClass.loadingBar(1, len(obj))
                        for item in obj:
                            for thing in attrName.split(", "): 
                                for stuff in thing.split(","):
                                    if stuff!="":
                                        if meth==1 or meth==2:
                                            if meth==1:
                                                at= "long"
                                            else:
                                                at= "float"
                                            if cbxMin==1 and cbxMax==1:
                                                cmds.addAttr(item, ln=stuff, at=at, min=minV, max=maxV)
                                            elif cbxMin==1 and cbxMax==0: 
                                                cmds.addAttr(item, ln=stuff, at=at, min=minV)
                                            elif cbxMin==0 and cbxMax==1: 
                                                cmds.addAttr(item, ln=stuff, at=at, max=maxV)
                                            else:     
                                                cmds.addAttr(item, ln=stuff, at=at)
                                            cmds.setAttr("%s.%s"%(item,stuff), k=1)     
                                        elif meth==3:  
                                            cmds.addAttr(item, ln=stuff, at="double3")
                                            if cbxMin==1 and cbxMax==1:
                                                cmds.addAttr(item, ln="%sX"%stuff, at="double", p=stuff, min=minV, max=maxV)
                                                cmds.addAttr(item, ln="%sY"%stuff, at="double", p=stuff, min=minV, max=maxV)
                                                cmds.addAttr(item, ln="%sZ"%stuff, at="double", p=stuff,  min=minV, max=maxV)
                                            elif cbxMin==1 and cbxMax==0: 
                                                cmds.addAttr(item, ln="%sX"%stuff, at="double", p=stuff,  min=minV)
                                                cmds.addAttr(item, ln="%sY"%stuff, at="double", p=stuff,  min=minV)
                                                cmds.addAttr(item, ln="%sZ"%stuff, at="double", p=stuff,  min=minV)
                                            elif cbxMin==0 and cbxMax==1: 
                                                cmds.addAttr(item, ln="%sX"%stuff, at="double", p=stuff,  max=maxV)
                                                cmds.addAttr(item, ln="%sY"%stuff, at="double", p=stuff,  max=maxV)
                                                cmds.addAttr(item, ln="%sZ"%stuff, at="double", p=stuff,  max=maxV)
                                            else:     
                                                cmds.addAttr(item, ln="%sX"%stuff, at="double", p=stuff)
                                                cmds.addAttr(item, ln="%sY"%stuff, at="double", p=stuff)
                                                cmds.addAttr(item, ln="%sZ"%stuff, at="double", p=stuff)
                                            cmds.setAttr("%s.%sX"%(item,stuff), k=1)
                                            cmds.setAttr("%s.%sY"%(item,stuff), k=1)  
                                            cmds.setAttr("%s.%sZ"%(item,stuff), k=1)   
                                        elif meth==4:
                                            cmds.addAttr(item, ln=stuff, at="enum", en=enumVal)
                                            cmds.setAttr("%s.%s"%(item,stuff), k=1)     
                                        elif meth==5:
                                            cmds.addAttr(item, ln=stuff, at="bool")
                                            cmds.setAttr("%s.%s"%(item,stuff), k=1)  
                            self.uiStuffClass.loadingBar(2) 
                        self.uiStuffClass.loadingBar(3)                                                            
                    else:
                        cmds.warning("One of the attribute NAME existed, please CHANGE NAME")
                else:
                    cmds.warning("One of the attribute NAME is incorrect, please remove EMPTY SPACE")
            else:
                cmds.warning("<ATTR Name> textfield is empty!")
        else:
            cmds.warning("Please select at least one target")

    def checkVec(self, sel, obj, tempSel):
        for subSel in sel:
            if cmds.getAttr("%s.%s"%(obj[0],subSel), typ=1)=="double":
                #If its a float, cannot do to the sub attribute but the main instead
                if cmds.attributeQuery("%s"%subSel[:-1], node=obj[0], ex=1):
                    if subSel[:-1] not in tempSel:
                        tempSel.append(subSel[:-1])
                else:
                    tempSel.append(subSel)    
            else:
                tempSel.append(subSel)
        return tempSel

    def attrSet(self, meth):
        obj= cmds.ls(sl=1)
        sel= cmds.channelBox("mainChannelBox", sma=1, q=1)
        test1, test2= [],[]
        test3= 1
        allAttr=[]
        if meth==5:
            if obj:
                self.uiStuffClass.loadingBar(1, len(obj))
                for item in obj:
                    allSel= cmds.listAttr(item, ud=1)
                    if allSel:
                        for allAttr in allSel:
                            if cmds.getAttr("%s.%s"%(item,allAttr), k=1)==0 or cmds.getAttr("%s.%s"%(item,allAttr), l=1)==1: 
                                cmds.setAttr("%s.%s"%(item,allAttr), k=1, l=0)       
                                test2= 1             
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
                if test2==[]:
                    cmds.warning("There is no custom attribute that is HIDDEN")
            else:
                cmds.warning("Please select at least 1 OBJECT")
        else:    
            if sel:
                if meth==6:
                    conti1, conti2, missAttr= self.checkCusAttr(sel, obj, obj)
                    if conti1:
                        if conti2:
                            self.uiStuffClass.loadingBar(1,1)
                            sel= self.checkVec(sel, obj, [])
                            for item in obj:
                                for attr in sel:
                                    if cmds.getAttr("%s.%s"%(item,attr), typ=1)=="double3":
                                        for thing in ["X","Y","Z"]:
                                            cmds.setAttr("%s.%s%s"%(item,attr,thing), k=1, l=0, cb=1)
                                    else:
                                        cmds.setAttr("%s.%s"%(item,attr), k=1, l=0, cb=1)
                                    cmds.deleteAttr("%s.%s"%(item,attr))
                            self.uiStuffClass.loadingBar(2)
                            self.uiStuffClass.loadingBar(3) 
                        else:
                            cmds.warning("<%s> attribute does not exist in one of the selected object"%(", ").join(missAttr))                            
                    else:
                        cmds.warning("One of the selected attribute is not a CUSTOM attribute")                   
                else:
                    self.uiStuffClass.loadingBar(1,1)
                    for item in obj:
                        for attr in sel:
                            if meth==1:
                                cmds.setAttr("%s.%s"%(item,attr), k=0, l=0, cb=1)
                            elif meth==2:
                                cmds.setAttr("%s.%s"%(item,attr), l=1)
                            elif meth==3:
                                cmds.setAttr("%s.%s"%(item,attr), k=0, l=1, cb=0)
                                self.sel= sel
                                self.obj= obj
                            elif meth==4:
                                cmds.setAttr("%s.%s"%(item,attr), k=1, l=0)
                    self.uiStuffClass.loadingBar(2)
                    self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("Please select at least 1 ATTRIBUTE")
        
    def attrUpDown(self, meth):
        obj= cmds.ls(sl=1)
        sel= cmds.channelBox("mainChannelBox", sma=1, q=1)
        if obj:
            if sel:
                conti1, conti2, missAttr= self.checkCusAttr(sel, obj, obj)
                if conti1:
                    if conti2:
                        sel= self.checkVec(sel, obj, [])                      
                        self.uiStuffClass.loadingBar(1, len(obj)) 
                        for item in obj:
                            allAttr=[]
                            attTest1= cmds.listAttr(item, ud=1)
                            attTest2= cmds.listAttr(item, ud=1, k=1)
                            attTest3= cmds.listAttr(item, ud=1, cb=1)
                            #Is there any other way to find out shown ud attr either unkeyable or lock                           
                            for subAttTest in attTest1:
                                if subAttTest in attTest2:
                                    allAttr= self.checkVec([subAttTest], [item], allAttr)
                                else:
                                    if attTest3:
                                        if subAttTest in attTest3:
                                            allAttr= self.checkVec([subAttTest], [item], allAttr)    
                            allNum, revAllNum, fullOrder, newAttr, newOrder, testLock= [],[],[],[],[],[]
                            for stuff in sel:
                                allNum.append(allAttr.index(stuff))
                                revAllNum.append(len(allAttr)-1-allAttr.index(stuff))
                            for x in range(len(allAttr)):
                                fullOrder.append(x)
                            for attrs in allAttr:
                                lock= cmds.getAttr("%s.%s"%(item,attrs), l=1)
                                if lock==1:
                                    cmds.setAttr("%s.%s"%(item,attrs), l=0)
                                    testLock.append("%s.%s"%(item,attrs))
                            if meth==1:
                                #y is to check is the top
                                #z is to check if selected is continuing selection
                                y= 0
                                z= 1
                                for thing in fullOrder:
                                    if thing in allNum:
                                        if thing==y:
                                            newAttr.append("%s.%s"%(item,allAttr[thing]))
                                            newOrder.append(thing)
                                            y= y+1  
                                        else:  
                                            if (thing+1) not in allNum:
                                                newAttr.append("%s.%s"%(item,allAttr[thing-z]))
                                                newOrder.append(thing-z)    
                                                z= 1
                                            else:
                                                newAttr.append("%s.%s"%(item,allAttr[thing+1]))
                                                newOrder.append(thing+1) 
                                                z= z+1                          
                                    elif (thing+1) in allNum:
                                        newAttr.append("%s.%s"%(item,allAttr[thing+1]))
                                        newOrder.append(thing+1)
                                    else:
                                        newAttr.append("%s.%s"%(item,allAttr[thing]))
                                        newOrder.append(thing)
                                if newOrder!=fullOrder:
                                    newAttr.reverse()
                                    cmds.deleteAttr(newAttr) 
                                    cmds.undo() 
                            elif meth==2:
                                y= len(allAttr)-1
                                z= 1
                                for thing in reversed(fullOrder):
                                    if thing in allNum:
                                        if thing==y:
                                            newAttr.append("%s.%s"%(item,allAttr[thing]))
                                            newOrder.append(thing)
                                            y= y-1  
                                        else:  
                                            if (thing-1) not in allNum:
                                                newAttr.append("%s.%s"%(item,allAttr[thing+z]))
                                                newOrder.append(thing+z)   
                                                z= 1 
                                            else:
                                                newAttr.append("%s.%s"%(item,allAttr[thing-1]))
                                                newOrder.append(thing-1) 
                                                z= z+1        
                                    elif (thing-1) in allNum:
                                        newAttr.append("%s.%s"%(item,allAttr[thing-1]))
                                        newOrder.append(thing-1)
                                    else:
                                        newAttr.append("%s.%s"%(item,allAttr[thing]))
                                        newOrder.append(thing)                                      
                                newOrder.reverse()        
                                if newOrder!=fullOrder:
                                    cmds.deleteAttr(newAttr) 
                                    cmds.undo() 
                            elif meth==3:                              
                                invNum, del1, del2= [],[],[]
                                aboveGrp, belowGrp= [], []
                                for subAttr in allAttr:
                                    if subAttr not in sel:
                                        invNum.append(allAttr.index(subAttr))
                                for num in reversed(invNum):
                                    if num<min(allNum):  
                                        aboveGrp.append("%s.%s"%(item,allAttr[num]))
                                    else:
                                        belowGrp.append("%s.%s"%(item,allAttr[num]))
                                if aboveGrp:
                                    cmds.deleteAttr(aboveGrp)
                                    cmds.undo()
                                if len(allNum)*(len(allNum)+1)/2-len(allNum)!=sum(allNum):
                                    if belowGrp:
                                        cmds.deleteAttr(belowGrp) 
                                        cmds.undo()                                         
                            else:
                                if len(allNum)*(len(allNum)+1)/2-len(allNum)!=sum(revAllNum):
                                    leftOver= []
                                    for num in reversed(allNum):
                                        leftOver.append("%s.%s"%(item,allAttr[num]))
                                    cmds.deleteAttr(leftOver)    
                                    cmds.undo()  
                            if testLock:
                                for unlock in testLock:
                                    cmds.setAttr(unlock, l=1)
                            self.uiStuffClass.loadingBar(2) 
                        self.uiStuffClass.loadingBar(3, tim=0.05)            
                    else:
                        cmds.warning("<%s> attribute does not exist in one of the selected object"%(", ").join(missAttr))                            
                else:
                    cmds.warning("One of the selected attribute is not a CUSTOM attribute")
            else:
                cmds.warning("Please select at least 1 CUSTOM attribute") 
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def checkCusAttr(self, selAttr, tar, obj):
        conti1, conti2= 1,1
        missAttr= []
        uds= cmds.listAttr(tar, ud=1)
        if uds:
            #Test if selected is custom attr
            for attr in selAttr:
                if attr not in uds:
                    conti1= []
        else:
            conti1= []
        #Test if selected custom attr exist in all selected object
        if conti1:
            for item in obj:
                subUds= cmds.listAttr(item, ud=1)
                if subUds:
                    for attr in selAttr:
                        if attr not in subUds:
                            conti2= []
                            missAttr.append(attr)
                else:
                    conti2= []
                    missAttr.append(attr)    
        return conti1, conti2, missAttr

    def checkState(self, sel, obj):
        realSel=[]
        val=[]
        for subSel in sel:
            if cmds.getAttr("%s.%s"%(obj[0],subSel), typ=1)=="double3":
                for item in ["X","Y","Z"]:
                    realSel.append("%s%s"%(subSel,item))
            else:
                realSel.append(subSel)
        for realSubSel in realSel:
            key= cmds.getAttr("%s.%s"%(obj[0],realSubSel), k=1)
            lock= cmds.getAttr("%s.%s"%(obj[0],realSubSel), l=1)
            show= cmds.getAttr("%s.%s"%(obj[0],realSubSel), cb=1)
            val.append([key,lock,show])
        return realSel, val

    def copyMoveAttr(self, meth): 
        obj= cmds.ls(sl=1)
        if len(obj)>=2:
            sour= obj[-1]
            tar= obj[:-1]
            sel= cmds.channelBox("mainChannelBox", sma=1, q=1)
            test1= 1
            if sel:
                conti1, conti2, missAttr= self.checkCusAttr(sel, sour, obj)
                if conti1:
                    sel= self.checkVec(sel, [sour], []) 
                    for item in tar:
                        for stuff in sel:
                            test1= self.checkName(test1, stuff, item) 
                    if test1:
                        self.uiStuffClass.loadingBar(1, 2)
                        self.uiStuffClass.loadingBar(2)
                        for item in tar:
                            realSel, val= self.checkState(sel, [sour])
                            for stuff in sel: 
                                attrType= cmds.attributeQuery(stuff, n=sour, at=1) 
                                if attrType=="enum":
                                    enumVal= cmds.attributeQuery(stuff, n=sour, le=1)  
                                    cmds.addAttr(item, ln=stuff, at=attrType, en=enumVal[0])
                                    cmds.setAttr("%s.%s"%(item,stuff), k=1) 
                                elif attrType=="bool":
                                    cmds.addAttr(item, ln=stuff, at=attrType)
                                    cmds.setAttr("%s.%s"%(item,stuff), k=1)                                     
                                else:
                                    if cmds.attributeQuery(stuff, n=sour, mne=1):
                                        minV= cmds.attributeQuery(stuff, n=sour, min=1)
                                    else:
                                        minV= []
                                    if cmds.attributeQuery(stuff, n=sour, mxe=1):        
                                        maxV= cmds.attributeQuery(stuff, n=sour, max=1)
                                    else:
                                        maxV= [] 
                                    if attrType=="double3":
                                        cmds.addAttr(item, ln=stuff, at="double3")
                                        if minV and maxV:  
                                            cmds.addAttr(item, ln="%sX"%stuff, at="double", p=stuff, min=minV, max=maxV)
                                            cmds.addAttr(item, ln="%sY"%stuff, at="double", p=stuff, min=minV, max=maxV)
                                            cmds.addAttr(item, ln="%sZ"%stuff, at="double", p=stuff, min=minV, max=maxV)
                                        elif  minV and maxV==[]:
                                            cmds.addAttr(item, ln="%sX"%stuff, at="double", p=stuff, min=minV)
                                            cmds.addAttr(item, ln="%sY"%stuff, at="double", p=stuff, min=minV)
                                            cmds.addAttr(item, ln="%sZ"%stuff, at="double", p=stuff, min=minV)
                                        elif minV==[] and maxV: 
                                            cmds.addAttr(item, ln="%sX"%stuff, at="double", p=stuff, max=maxV)
                                            cmds.addAttr(item, ln="%sY"%stuff, at="double", p=stuff, max=maxV)
                                            cmds.addAttr(item, ln="%sZ"%stuff, at="double", p=stuff, max=maxV)
                                        else:     
                                            cmds.addAttr(item, ln="%sX"%stuff, at="double", p=stuff)
                                            cmds.addAttr(item, ln="%sY"%stuff, at="double", p=stuff)
                                            cmds.addAttr(item, ln="%sZ"%stuff, at="double", p=stuff)
                                        cmds.setAttr("%s.%sX"%(item,stuff), k=1)
                                        cmds.setAttr("%s.%sY"%(item,stuff), k=1)  
                                        cmds.setAttr("%s.%sZ"%(item,stuff), k=1) 
                                    else:    
                                        if minV and maxV:  
                                            cmds.addAttr(item, ln=stuff, at=attrType, min=minV[0], max=maxV[0])                               
                                        elif  minV and maxV==[]:
                                            cmds.addAttr(item, ln=stuff, at=attrType, min=minV[0])
                                        elif minV==[] and maxV:
                                            cmds.addAttr(item, ln=stuff, at=attrType, max=maxV[0])
                                        else:
                                            cmds.addAttr(item, ln=stuff, at=attrType)
                                        cmds.setAttr("%s.%s"%(item,stuff), k=1)  
                                if meth==2:    
                                    cmds.copyAttr(sour, item, at=stuff, v=1, oc=1)    
                                    cmds.deleteAttr(sour, at=stuff)
                            for realSubSel, subVal in zip(realSel,val):
                                cmds.setAttr("%s.%s"%(item,realSubSel), k=subVal[0])
                                cmds.setAttr("%s.%s"%(item,realSubSel), l=subVal[1])
                                if subVal[2]:
                                    cmds.setAttr("%s.%s"%(item,realSubSel), cb=subVal[2])
                        self.uiStuffClass.loadingBar(2)
                        self.uiStuffClass.loadingBar(3, sel=tar)
                    else:
                        cmds.warning("One of the attribute NAME existed, please CHANGE NAME") 
                else:    
                    cmds.warning("One of the selected attribute is not a CUSTOM attribute")
            else:
                cmds.warning("Please select at least 1 CUSTOM attribute")             
        else:
            cmds.warning("Please select at least 1 TARGET and only 1 SOURCE")

    def attrRen(self, meth):
        obj= cmds.ls(sl=1)
        sel= cmds.channelBox("mainChannelBox", sma=1, q=1)
        if meth==1:
            newName= cmds.textFieldGrp(self.txtFAttrName, q=1, tx=1) 
        else:
            newName= cmds.textFieldGrp(self.txtFEnumName, q=1, tx=1) 
        test1, test2, test3, test4= 1,1,1,1
        if obj:
            if sel:
                conti1, conti2, missAttr= self.checkCusAttr(sel, obj, obj)
                if conti1:
                    if conti2:
                        if newName:
                            test1, test2, realAttr= self.checkNameNSpace(newName, obj, test1, test2, 2, sel)
                            if test1:
                                if meth==1:
                                    if test2:
                                        if len(realAttr)==1:
                                            self.uiStuffClass.loadingBar(1, 2)
                                            self.uiStuffClass.loadingBar(2)
                                            if len(sel)==1:
                                                for item in obj:
                                                    cmds.renameAttr("%s.%s"%(item,sel[0]), newName)
                                            else:
                                                for x, attr in enumerate(sel):
                                                    for item in obj:
                                                        cmds.renameAttr("%s.%s"%(item,attr), "%s%s"%(newName,x+1))
                                            self.uiStuffClass.loadingBar(2)
                                            self.uiStuffClass.loadingBar(3, sel=obj)    
                                        else:
                                            cmds.warning("Please only input 1 NAME without any comma (,)")                                    
                                    else:
                                        cmds.warning("One of the attribute NAME existed, please CHANGE NAME") 
                                else:
                                    enumNum= []
                                    for item in obj:
                                        for attr in sel:
                                            if cmds.getAttr("%s.%s"%(item,attr), typ=1)!="enum":
                                                test3= []
                                                break
                                            else:
                                                enumVal= cmds.addAttr("%s.%s"%(item,attr), q=1, en=1)
                                                enumNum.append(len(enumVal.split(":")))    
                                    if test3:
                                        if max(enumNum)!=len(newName.split(":")):
                                            test4= []
                                        conti3= self.dialogClass.continueDialog(test4, "Enum numbers mismatch!\n\n%s new name vs %s enum,\n Proceed?"%(len(newName.split(":")), max(enumNum)))
                                        if conti3:
                                            self.uiStuffClass.loadingBar(1, 2)
                                            self.uiStuffClass.loadingBar(2)
                                            for item in obj:
                                                for attr in sel:
                                                    cmds.addAttr("%s.%s"%(item,attr), e=1, en=":".join(realAttr))
                                            self.uiStuffClass.loadingBar(2)
                                            self.uiStuffClass.loadingBar(3, sel=obj)
                                    else:
                                        cmds.warning("One of the attribute selected is NOT a ENUM")
                            else:
                                cmds.warning("One of the attribute NAME is incorrect, please remove EMPTY SPACE")
                        else:
                            cmds.warning("<NEW NAME> textfield are empty!")
                    else:
                        cmds.warning("<%s> attribute does not exist in one of the selected object"%(", ").join(missAttr))                            
                else:
                    cmds.warning("One of the selected attribute is not a CUSTOM attribute")
            else:
                cmds.warning("Please select at least 1 CUSTOM attribute")
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def attrSR(self, meth):
        obj= cmds.ls(sl=1)
        sel= cmds.channelBox("mainChannelBox", sma=1, q=1)
        sear= cmds.textFieldGrp(self.txtFSear, q=1, tx=1)
        repl= cmds.textFieldGrp(self.txtFRepl, q=1, tx=1)           
        test1= []
        test2= 1
        if obj:
            if sel:
                conti1, conti2, missAttr= self.checkCusAttr(sel, obj, obj)
                if conti1:
                    if conti2:
                        if sear:
                            if meth==1:
                                for attr in sel:
                                    if sear in attr:
                                        test1= 1
                                if test1:
                                    self.uiStuffClass.loadingBar(1, 2)
                                    self.uiStuffClass.loadingBar(2)
                                    for item in obj:
                                        for attr in sel:
                                            if sear in attr:
                                                cmds.renameAttr("%s.%s"%(item, attr), attr.replace(sear, repl))
                                    self.uiStuffClass.loadingBar(2)
                                    self.uiStuffClass.loadingBar(3, sel=obj)
                                else:
                                    cmds.warning("All attribute does not contain '%s' OR could be capital problem (Try capitalize/decapitalize the first letter)"%sear)
                            elif meth==2:
                                for item in obj:
                                    for attr in sel:
                                        if cmds.getAttr("%s.%s"%(item, attr), typ=1)=="enum":
                                            val= cmds.addAttr("%s.%s"%(item, attr), q=1, en=1)
                                            if sear in val:
                                                test1= 1
                                        else:
                                            test2= []
                                if test2:
                                    if test1:
                                        self.uiStuffClass.loadingBar(1, 2)
                                        self.uiStuffClass.loadingBar(2)
                                        for item in obj:
                                            for attr in sel:
                                                val= cmds.addAttr("%s.%s"%(item, attr), q=1, en=1)
                                                if sear in val:
                                                    cmds.addAttr("%s.%s"%(item, attr), e=1, en=val.replace(sear,repl))
                                        self.uiStuffClass.loadingBar(2)
                                        self.uiStuffClass.loadingBar(3, sel=obj)
                                    else:
                                        cmds.warning("All Enum's value does not contain '%s' OR could be capital problem (Try capitalize/decapitalize the first letter)"%sear)
                                else:
                                    cmds.warning("One of the attribute selected is NOT a ENUM")
                        else:
                            cmds.warning("<SEARCH> textfield are empty!")
                    else:
                        cmds.warning("<%s> attribute does not exist in one of the selected object"%(", ").join(missAttr))                            
                else:
                    cmds.warning("One of the selected attribute is not a CUSTOM attribute")
            else:
                cmds.warning("Please select at least 1 CUSTOM attribute")
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def searchL(self):
        obj= cmds.ls(sl=1)
        if obj:
            attrStr= ["minTransX","maxTransX","minTransY","maxTransY","minTransZ","maxTransZ","minRotX","maxRotX","minRotY","maxRotY","minRotZ","maxRotZ","minScaleX","maxScaleX","minScaleY","maxScaleY","minScaleZ","maxScaleZ"]
            attrVar= [self.minTx,self.maxTx,self.minTy,self.maxTy,self.minTz,self.maxTz,self.minRx,self.maxRx,self.minRy,self.maxRy,self.minRz,self.maxRz,self.minSx,self.maxSx,self.minSy,self.maxSy,self.minSz,self.maxSz]
            self.uiStuffClass.loadingBar(1, len(obj))
            for item in obj:
                for stuff in zip(attrStr,attrVar):
                    limitEn= cmds.getAttr("%s.%sLimitEnable"%(item,stuff[0]))
                    if limitEn==1:
                        limit= cmds.getAttr("%s.%sLimit"%(item,stuff[0]))
                        cmds.textFieldGrp(stuff[1], e=1, tx="%s"%limit) 
                    else:
                        cmds.textFieldGrp(stuff[1], e=1, tx="")
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def setL(self):
        obj= cmds.ls(sl=1)
        if obj:
            test1, test2, test3= 1,1,1
            attrVar= [[self.minTx,self.maxTx],[self.minTy,self.maxTy],[self.minTz,self.maxTz],[self.minRx,self.maxRx],[self.minRy,self.maxRy],[self.minRz,self.maxRz],[self.minSx,self.maxSx],[self.minSy,self.maxSy],[self.minSz,self.maxSz]]
            attrStr= [["minTransX","maxTransX"],["minTransY","maxTransY"],["minTransZ","maxTransZ"],["minRotX","maxRotX"],["minRotY","maxRotY"],["minRotZ","maxRotZ"],["minScaleX","maxScaleX"],["minScaleY","maxScaleY"],["minScaleZ","maxScaleZ"]]
            for item in obj:
                for stuff in zip(attrVar,attrStr):
                    minVal= cmds.textFieldGrp(stuff[0][0], q=1, tx=1)
                    maxVal= cmds.textFieldGrp(stuff[0][1], q=1, tx=1)
                    newMinVal= ".".join(re.findall("-?\d+", minVal))
                    newMaxVal= ".".join(re.findall("-?\d+", maxVal))
                    if minVal:
                        if newMinVal=="":
                            test1=[]
                    if maxVal:
                        if newMaxVal=="":
                            test1=[]
                    if newMinVal and newMaxVal:
                        if float(newMinVal)>float(newMaxVal):
                            test2=[]  
                    limitEn1= cmds.getAttr("%s.%sLimitEnable"%(item,stuff[1][0]))
                    limitEn2= cmds.getAttr("%s.%sLimitEnable"%(item,stuff[1][1]))
                    if limitEn1==1 or limitEn2==1:
                        test3=[]
            if test1:   
                if test2:  
                    conti1= self.dialogClass.continueDialog(test3, "Have existing limit, overwrite it?")
                    if conti1:
                        self.uiStuffClass.loadingBar(1, len(obj)) 
                        for item in obj:
                            for stuff in zip(attrVar,attrStr):  
                                minVal= cmds.textFieldGrp(stuff[0][0], q=1, tx=1)
                                maxVal= cmds.textFieldGrp(stuff[0][1], q=1, tx=1)
                                newMinVal= ".".join(re.findall("-?\d+", minVal))
                                newMaxVal= ".".join(re.findall("-?\d+", maxVal))                        
                                if newMinVal:
                                    cmds.setAttr("%s.%sLimitEnable"%(item,stuff[1][0]), 1)
                                else:
                                    cmds.setAttr("%s.%sLimitEnable"%(item,stuff[1][0]), 0)
                                if newMaxVal:
                                    cmds.setAttr("%s.%sLimitEnable"%(item,stuff[1][1]), 1)
                                else:
                                    cmds.setAttr("%s.%sLimitEnable"%(item,stuff[1][1]), 0)
                                minLimit= cmds.getAttr("%s.%sLimit"%(item,stuff[1][0]))
                                maxLimit= cmds.getAttr("%s.%sLimit"%(item,stuff[1][1]))
                                if newMinVal or newMaxVal:
                                    if newMinVal=="":
                                        cmds.setAttr("%s.%sLimit"%(item,stuff[1][0]), float(newMaxVal)) 
                                        cmds.setAttr("%s.%sLimit"%(item,stuff[1][1]), float(newMaxVal))  
                                    elif newMaxVal=="":
                                        cmds.setAttr("%s.%sLimit"%(item,stuff[1][1]), float(newMinVal))
                                        cmds.setAttr("%s.%sLimit"%(item,stuff[1][0]), float(newMinVal))    
                                    else:
                                        cmds.setAttr("%s.%sLimit"%(item,stuff[1][0]), float(newMinVal)) 
                                        cmds.setAttr("%s.%sLimit"%(item,stuff[1][1]), float(newMaxVal))
                            self.uiStuffClass.loadingBar(2)
                        self.uiStuffClass.loadingBar(3)
                else:
                    cmds.warning("Min value cannot be HIGHER than max value")
            else:
                cmds.warning("Please input VALUE only")
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def searchCL(self):
        obj= cmds.ls(sl=1)
        sel= cmds.channelBox("mainChannelBox", sma=1, q=1)    
        test1= []
        test2= 1
        if obj:
            if len(obj)==1:
                if sel:
                    if len(sel)==1:
                        uds= cmds.listAttr(obj[0], ud=1)
                        if sel[0] in uds:
                            test1= 1
                    else:
                        test2= []
                else:
                    test1= []
                if test1:
                    if test2:
                        self.uiStuffClass.loadingBar(1, 1) 
                        minC= cmds.addAttr("%s.%s"%(obj[0],sel[0]), q=1, min=1)
                        maxC= cmds.addAttr("%s.%s"%(obj[0],sel[0]), q=1, max=1)                        
                        if minC==None:
                            minC=""
                        if maxC==None:
                            maxC=""
                        cmds.textFieldGrp(self.minC, e=1, tx="%s"%minC)  
                        cmds.textFieldGrp(self.maxC, e=1, tx="%s"%maxC) 
                        self.uiStuffClass.loadingBar(2)
                        self.uiStuffClass.loadingBar(3)
                    else:
                        cmds.warning("Please select only 1 CUSTOM attribute") 
                else:
                    cmds.warning("Please select 1 CUSTOM attribute")       
            else:
                cmds.warning("Please select only 1 OBJECT")    
        else:
            cmds.warning("Please select 1 OBJECT") 

    def setCL(self):
        obj= cmds.ls(sl=1)
        sel= cmds.channelBox("mainChannelBox", sma=1, q=1)    
        test1= []
        test2, test3, test4= 1,1,1
        if obj:
            if sel:
                for item in obj:
                    uds= cmds.listAttr(item, ud=1)
                    if sel[0] in uds:
                        test1= 1
                    else:
                        test2= []
            else:
                test1= []
            if test1:
                if test2:
                    minC= cmds.textFieldGrp(self.minC, q=1, tx=1)
                    maxC= cmds.textFieldGrp(self.maxC, q=1, tx=1) 
                    newMinC= ".".join(re.findall("-?\d+", minC))
                    newMaxC= ".".join(re.findall("-?\d+", maxC))
                    if minC:
                        if newMinC=="":
                            test3=[]
                    if maxC:
                        if newMaxC=="":
                            test3=[]
                    if newMinC and newMaxC:
                        if float(newMinC)>float(newMaxC):
                            test4=[]  
                    if test3:
                        if test4:
                            self.uiStuffClass.loadingBar(1, len(obj))
                            for item in obj:
                                for stuff in sel:
                                    #This is to force enable limit first or else cannot compare bigger or smaller
                                    if cmds.addAttr("%s.%s"%(item,stuff), q=1, hnv=1)==False:
                                        cmds.addAttr("%s.%s"%(item,stuff), e=1, hnv=1) 
                                    if cmds.addAttr("%s.%s"%(item,stuff), q=1, hxv=1)==False:
                                        cmds.addAttr("%s.%s"%(item,stuff), e=1, hxv=1)    
                                    oldMinC= cmds.addAttr("%s.%s"%(item,sel[0]), q=1, min=1)
                                    oldMaxC= cmds.addAttr("%s.%s"%(item,sel[0]), q=1, max=1) 
                                    if newMinC=="":
                                        cmds.addAttr("%s.%s"%(item,stuff), e=1, hnv=0)  
                                    if newMaxC=="":
                                        cmds.addAttr("%s.%s"%(item,stuff), e=1, hxv=0)
                                    if newMinC or newMaxC:
                                        if newMinC=="":
                                            cmds.addAttr("%s.%s"%(item,stuff), e=1, max=float(newMaxC))
                                            cmds.addAttr("%s.%s"%(item,stuff), e=1, min=float(newMaxC))
                                            cmds.addAttr("%s.%s"%(item,stuff), e=1, hnv=0)
                                        elif newMaxC=="":
                                            cmds.addAttr("%s.%s"%(item,stuff), e=1, min=float(newMinC))
                                            cmds.addAttr("%s.%s"%(item,stuff), e=1, max=float(newMinC))
                                            cmds.addAttr("%s.%s"%(item,stuff), e=1, hxv=0)
                                        else:
                                            if float(newMinC)>float(oldMaxC):
                                                cmds.addAttr("%s.%s"%(item,stuff), e=1, max=float(newMaxC))
                                                cmds.addAttr("%s.%s"%(item,stuff), e=1, min=float(newMinC))
                                            else:
                                                cmds.addAttr("%s.%s"%(item,stuff), e=1, min=float(newMinC))
                                                cmds.addAttr("%s.%s"%(item,stuff), e=1, max=float(newMaxC)) 
                                self.uiStuffClass.loadingBar(2)
                            self.uiStuffClass.loadingBar(3)    
                        else:
                            cmds.warning("Min value cannot be HIGHER than max value")
                    else:
                        cmds.warning("Please input VALUE only")
                else:
                    cmds.warning("One of the selected object does not have the selected CUSTOM attribute")
            else:
                cmds.warning("Select at least 1 CUSTOM attribute") 
        else:
            cmds.warning("Please select at least 1 OBJECT")

    def unlockFromCc(self):
        if cmds.radioButtonGrp(self.rb41, q=1, sl=1)==2:
            obj= cmds.ls(sl=1, typ="joint") 
            if obj:
                self.uiStuffClass.loadingBar(1, 1)
                for item in obj:
                    cmds.setAttr("%s.radius"%item, k=1, l=0)
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("Please select at least 1 JOINT")
        else:
            obj= cmds.ls(sl=1, tr=1)
            if obj:
                self.uiStuffClass.loadingBar(1, 1)
                for item in obj:
                    if cmds.checkBoxGrp(self.cb41, q=1, v1=1):     
                        cmds.setAttr("%s.v"%item, k=1, l=0)
                    for stuff in ["x","y","z",""]:
                        if cmds.checkBoxGrp(self.cb41, q=1, v2=1):    
                            cmds.setAttr("%s.t%s"%(item,stuff), k=1, l=0)       
                        if cmds.checkBoxGrp(self.cb41, q=1, v3=1): 
                            cmds.setAttr("%s.r%s"%(item,stuff), k=1, l=0)  
                        if cmds.checkBoxGrp(self.cb41, q=1, v4=1): 
                            cmds.setAttr("%s.s%s"%(item,stuff), k=1, l=0) 
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3)     
            else:
                cmds.warning("Please select at least 1 OBJECT") 

    def helps(self):
        name="Help On Attributes"
        helpTxt="""
        - To create / edit custom attribute
        - To set limit
        - To unhide (like in channel control)

 
        < Create >
        ==========
            1) Integer/Float/Vector, Enum, Boolean
                - Can set min/max value
                - Each enum value must comes with a ":" (* no space after :) 
                - Value is default "on/off"
            
            2) UnKeyable, Lock, Lock & Hide, Unlock & Keyable
                - Make attribute unkeyable
                - Make attribute locked
                - Make attribute Locked & Hidden
                - Unlock any attribute in any state (unkeyable, locked, hidden) 
                    (* Special!!! If the last action you did is lock & hide, it can detect and unlock it!)

            3) Unlock All Custom
                - Unlock all custom attribute from channel control

            4) Delete Attribute
                - Delete attribute
                (* Able to delete in "locked" state and works for "Vector" type!)

            5) Up, Down, Top, Bottom
                - Move single/multi custom attribute


        < Edit >
        =========
            1) Copy / Move 
            -----------------   
                1. Copy 
                    - Duplicate the custom attribute to another target
                    (* Include max/min limit and state)

                2. Move
                    - Move the same custom attribute to another target
                    - Delete original source custom attribute
                    (* Will move all the outgoing connections)

            2) Rename Attr, Enum Value
            ------------------------------
                - Rename custom attributes name
                - Rename Enum type custom attribute's value
                (* For multiple selection, suffix will add according from top to bottom, not selection order)


            3) Replace Attr, Enum Value
            -------------------------------
                - Replace custom attributes name
                - Replace Enum type custom attribute's value


        < Limiter >
        ============
            (* Empty textfield meaning DISABLE LIMIT)
            (* Unlike maya, still can proceed even if new lower limit is higher than current higher limit)

            1) Default attribute
            ------------------------
                - <Search> and <Set> limit

            2) Custom attribute
            -----------------------
                - <Search> and <Set> limit
                (* Search limit only allow 1 attribute but set can be multiple)


        < Unhider >
        ===========
            - Unhide, Unlock, Keyable from channel control

        """
        self.helpBoxClass.helpBox1(name, helpTxt)    

    def reloadSub(self):
        Attribute()   
        
        
if __name__=='__main__':
    Attribute() 
                   