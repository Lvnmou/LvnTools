import maya.cmds as cmds
import Mod.uiStuff as uiStuff
import Mod.dialog as dialog
import Mod.helpBox as helpBox
import re


class Blendshape(object):
    def __init__(self, *args):
        self.uiStuffClass= uiStuff.UiStuff()
        self.dialogClass= dialog.Dialog()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):    
        try: 
            cmds.deleteUI("bs") 
        except:
            pass    
        cmds.window("bs", mb=1)              
        cmds.window("bs", t="Blendshape", s=1, e=1, wh=(290,550))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Blendshape", c=lambda x:self.helps())        
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Blendshape", c=lambda x:self.reloadSub())  
        self.uiStuffClass.sepBoxMain()
        column11= self.uiStuffClass.sepBoxSub("Basic")
        form11= cmds.formLayout(nd=100, p=column11)
        self.cb111= cmds.checkBoxGrp(l="", cw=(1,10), cc= lambda x:self.cbx1())
        self.txtSear= cmds.textFieldGrp(l="Search :", cw2=(50,50), adj=2, en=0) 
        self.txtRepl= cmds.textFieldGrp(l="Replace :", cw2=(50,50), adj=2, en=0) 
        sep111= cmds.separator(h=5, st="in")
        self.cb112= cmds.checkBoxGrp(l="", l1="Check Topology", cw2=(0,10), v1=1)
        self.cb113= cmds.checkBoxGrp(l="", l1="Activate", cw2=(0,10), v1=1) 
        #self.cb114= cmds.checkBoxGrp(l="", l1="Share Same Node", cw2=(0,10))        
        self.txt11= cmds.text(l="Select TARGET then BASE", fn="smallObliqueLabelFont", en=0)         
        b11= cmds.button(l="Create Blendshape", c=lambda x:self.creBS())   
        cmds.formLayout(form11, e=1,
                                af=[(self.cb111, "top", 15),
                                    (self.txtSear, "top", 0),
                                    (self.txtRepl, "top", 26),
                                    (sep111, "top", 60),
                                    (self.cb112, "top", 75),
                                    (self.cb113, "top", 95),
                                    #(self.cb114, "top", 115),
                                    (self.txt11, "top", 146),
                                    (b11, "top", 162)],
                                ap=[(self.txt11, "left", 0, 0),
                                    (self.txt11, "right", 0, 100),
                                    (self.txtSear, "left", 40, 0),
                                    (self.txtSear, "right", 0, 100),
                                    (self.txtRepl, "left", 40, 0),
                                    (self.txtRepl, "right", 0, 100),
                                    (sep111, "left", 0, 0),
                                    (sep111, "right", 0, 100),
                                    (self.cb112, "left", -50, 50),
                                    (self.cb112, "right", 0, 100),
                                    (self.cb113, "left", -50, 50),
                                    (self.cb113, "right", 0, 100), 
                                    #(self.cb114, "left", -50, 50),
                                    #(self.cb114, "right", 0, 100),                                    
                                    (b11, "left", 0, 0),
                                    (b11, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column12= self.uiStuffClass.sepBoxSub()
        form12= cmds.formLayout(nd=100, p=column12)
        self.cb121= cmds.checkBoxGrp(l="", l1="Check Topology", cw2=(0,10), v1=1)
        txt12= cmds.text(l="Select at least 3 :       TARGETS / BASE / BLENDSHAPE", fn="smallObliqueLabelFont", en=0)         
        b121= cmds.button(l="Add Target", c=lambda x:self.addRemBS(1))      
        b122= cmds.button(l="Remove Target", c=lambda x:self.addRemBS(2))   
        cmds.formLayout(form12, e=1,
                                af=[(self.cb121, "top", 0),
                                    (txt12, "top", 26),
                                    (b121, "top", 42),
                                    (b122, "top", 68)],
                                ap=[(self.cb121, "left", -50, 50),
                                    (self.cb121, "right", 0, 100),
                                    (txt12, "left", 0, 0),
                                    (txt12, "right", 0, 100),
                                    (b121, "left", 0, 0),
                                    (b121, "right", 0, 100),
                                    (b122, "left", 0, 0),
                                    (b122, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        column13= self.uiStuffClass.sepBoxSub()
        form13= cmds.formLayout(nd=100, p=column13)
        txt13= cmds.text(l="Select NEW then OLD", fn="smallObliqueLabelFont", en=0) 
        b13= cmds.button(l="Replace Target", c=lambda x:self.rBS())     
        cmds.formLayout(form13, e=1,
                                af=[(txt13, "top", 0),
                                    (b13, "top", 16)],
                                ap=[(txt13, "left", 0, 0),
                                    (txt13, "right", 0, 100),
                                    (b13, "left", 0, 0),
                                    (b13, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column2= self.uiStuffClass.sepBoxSub("Facial Checker")
        form2= cmds.formLayout(nd=100, p=column2)
        txt21= cmds.text(l="Select HEAD Geometry", fn="smallObliqueLabelFont", en=0) 
        b21= cmds.button(l="Setup Facial Checker", c=lambda x:self.fbc())     
        b22= cmds.button(l="Add Extra Target", c=lambda x:self.extraTar())  
        txt22= cmds.text(l="*Creates temporary facial ctrl and blendshape targets\ncan straight away sculpt on those\n\n*You can adjust the position of blendshape and ctrl", fn="smallObliqueLabelFont", en=0) 
        cmds.formLayout(form2, e=1,
                                af=[(txt21, "top", 0),
                                    (b21, "top", 16),
                                    (b22, "top", 42),
                                    (txt22, "top", 81)],
                                ap=[(txt21, "left", 0, 0),
                                    (txt21, "right", 0, 100),
                                    (b21, "left", 0, 0),
                                    (b21, "right", 0, 100),
                                    (b22, "left", 0, 0),
                                    (b22, "right", 0, 100),
                                    (txt22, "left", 0, 0),
                                    (txt22, "right", 0, 100)])        
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column3= self.uiStuffClass.sepBoxSub("Add Inbetween")
        form3= cmds.formLayout(nd=100, p=column3)
        txt31= cmds.text(l="Select BLENDSHAPE or BLENDSHAPE Attribute", fn="smallObliqueLabelFont", en=0) 
        b31=  cmds.button(l="Get Blendshape Index", c=lambda x:self.grabInd()) 
        sep31= cmds.separator(h=5, st="in")
        self.txtMesh= cmds.textFieldGrp(l="Mesh :", cw2=(70,10), adj=2, tx="", en=0) 
        self.txtBsName= cmds.textFieldGrp(l="Blendshape :", cw2=(70,10), adj=2, tx="", en=0) 
        self.txtInd= cmds.intFieldGrp(l="Index :", cw2=(70,10), adj=2, en=0) 
        self.slidy= cmds.floatSliderGrp(l="Weight : ", f=1, cw3=(70,50,80), min=0, max=1, fmn=-10, fmx=10, pre=2, v=0.5)
        self.cb311= cmds.checkBoxGrp(l="", l1="Check Topology", cw2=(100,10), v1=1)
        txt32= cmds.text(l="Select Inbetween Target", fn="smallObliqueLabelFont", en=0) 
        b32= cmds.button(l="Add Inbetween", c=lambda x:self.inBs()) 
        cmds.formLayout(form3, e=1,
                                af=[(txt31, "top", 0),
                                    (b31, "top", 16),
                                    (sep31, "top", 50),
                                    (self.txtMesh, "top", 70),
                                    (self.txtBsName, "top", 96),
                                    (self.txtInd, "top", 122),
                                    (self.slidy, "top", 148),
                                    (self.cb311, "top", 174),
                                    (txt32, "top", 216),
                                    (b32, "top", 232),
                                    #(self.sf, "bottom", 10)
                                    ],
                                ap=[(txt31, "left", 0, 0),
                                    (txt31, "right", 0, 100),
                                    (b31, "left", 0, 0),
                                    (b31, "right", 0, 100),
                                    (sep31, "left", 0, 0),
                                    (sep31, "right", 0, 100),
                                    (self.txtMesh, "left", 0, 0),
                                    (self.txtMesh, "right", 0, 100),
                                    (self.txtBsName, "left", 0, 0),
                                    (self.txtBsName, "right", 0, 100),
                                    (self.txtInd, "left", 0, 0),
                                    (self.txtInd, "right", 0, 100),
                                    (self.slidy, "left", 0, 0),
                                    (self.slidy, "right", 0, 100),
                                    (txt32, "left", 0, 0),
                                    (txt32, "right", 0, 100),
                                    (b32, "left", 0, 0),
                                    (b32, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(3)
        self.sf= cmds.scrollField(fn="plainLabelFont", h=150, ed=0, ww=1)          
        cmds.setFocus(cmds.text(l= ""))      
        cmds.showWindow("bs")  

    def cbx1(self):
        if cmds.checkBoxGrp(self.cb111, q=1, v1=1):
            cmds.textFieldGrp(self.txtSear, e=1, en=1) 
            cmds.textFieldGrp(self.txtRepl, e=1, en=1) 
            #cmds.checkBoxGrp(self.cb114, e=1, en=0)
            cmds.text(self.txt11, e=1, l="Select TARGET")
        else:
            cmds.textFieldGrp(self.txtSear, e=1, en=0) 
            cmds.textFieldGrp(self.txtRepl, e=1, en=0) 
            #cmds.checkBoxGrp(self.cb114, e=1, en=1)  
            cmds.text(self.txt11, e=1, l="Select TARGET then BASE")

    def bsCal(self, allBsIn):
        D1, D3= {}, {}
        for item in range(0, len(allBsIn)-1, 2):
            num= re.findall("\d+", allBsIn[item+1])[0]
            D1[num]= allBsIn[item]  
        #Need to sorted due to its string
        newNum= sorted(D1, key=lambda x: int(re.sub('\D*', "", x)))  
        #Some index doenst match weight number due to deleted blendshape or what?
        #So use enumerate to find the correct number
        for x, stuff in enumerate(newNum):
            D3[x+1] =D1[stuff]
        fullD=[]
        for k, v in zip(D3.keys(), D3.values()):
            fullD.append("%02d"%k)
            fullD.append(v+"\n")
        return D1, fullD

    def creBS(self):
        obj= cmds.ls(sl=1, tr=1)
        topo= cmds.checkBoxGrp(self.cb112, q=1, v1=1)
        acti= cmds.checkBoxGrp(self.cb113, q=1, v1=1)
        sear= cmds.textFieldGrp(self.txtSear, q=1, tx=1) 
        repl= cmds.textFieldGrp(self.txtRepl, q=1, tx=1) 

        if cmds.checkBoxGrp(self.cb111, q=1, v1=1):
            if obj:
                conti1, tar= self.dialogClass.sameNameOrNoExistDialog(obj, sear, repl)
                if conti1:
                    for item in obj:
                        base= item.replace(sear,repl)
                        if tar!= item:
                            if cmds.objExists(base):
                                bs= cmds.blendShape(item, base, foc=1, tc=topo)
                                cmds.setAttr("%s.%s"%(bs[0],item), acti)
            else:
                cmds.warning("Please select at least 1 MESH")
        else:
            if len(obj)>1:
                """
                if cmds.checkBoxGrp(self.cb114, q=1, v1=1): 
                    bs= cmds.blendShape(obj[0], obj[-1], foc=1, tc=topo)
                    for x,stuff in enumerate(obj[:-1]):
                        if x!=0:
                            cmds.blendShape("%s"%bs[0], e=1, t=(obj[-1], x, stuff ,1), tc=topo)
                        cmds.setAttr("%s.%s"%(bs[0],stuff), acti) 
                else:
                """    
                bs= cmds.blendShape(obj[:-1], obj[-1], foc=1, tc=topo)
                for stuff in obj[:-1]:
                    cmds.setAttr("%s.%s"%(bs[0],stuff), acti)

            else:
                cmds.warning("Please select at least 1 TARGET and 1 BASE")

    def addRemBS(self, meth):
        obj= cmds.ls(sl=1, tr=1)
        bs= cmds.ls(sl=1, typ="blendShape")
        tar= obj[:-1]
        if len(obj)>1:
            if bs:
                allBsIn= cmds.aliasAttr("%s"%bs[0], q=1)
                if allBsIn:
                    D1, fullD= self.bsCal(allBsIn)  
                realD1=[]      
                for item in D1.keys():
                    realD1.append(int(item))            
                val= max(realD1)
                topo= cmds.checkBoxGrp(self.cb121, q=1, v1=1)
                if meth==1:
                    for x, thing in enumerate(tar):
                        cmds.blendShape("%s"%bs[0], e=1, t=(obj[-1], val+x+1, thing ,1), tc=topo)   
                elif meth==2:
                    for thing in tar:
                        cmds.blendShape("%s"%bs[0], e=1, rm=1, t=(obj[-1], 0, thing ,1))   
            else:
                cmds.warning("There is no BLENDSHAPE NODE selected")
        else:
            cmds.warning("Please select at least 1 TARGET, 1 BASE and 1 BLENDSHAPE NODE")

    def rBS(self):
        obj= cmds.ls(sl=1)
        if len(obj)==2:
            ori= cmds.listRelatives(obj[1], s=1)
            new= cmds.listRelatives(obj[0], s=1)
            con= cmds.listConnections("%s.worldMesh"%ori[0], d=1, c=1, p=1)
            if con:
                cmds.connectAttr("%s.worldMesh"%new[0], con[1], f=1)
                #Below is just to change the blendshape attribute name to new target name (will update for any expression as well)
                bsName= con[1].split(".")[0]
                num= con[1].split(".")[2].replace("inputTargetGroup","")
                allBsIn= cmds.aliasAttr(bsName, q=1)
                for x, item in enumerate(allBsIn):
                    if num in item:
                        tarNum= x-1
                cmds.aliasAttr("%s"%obj[0], "%s.%s"%(bsName, allBsIn[tarNum]))
            else:
                cmds.warning("Second object is not a BLENDSHAPE TARGET")
        else:
            cmds.warning("Please select 1 TARGET & 1 SOURCE")

    def creCtrl(self, c1Name, s1Name, par):
        c1= cmds.curve(d=3, n=c1Name, p=[(0, 0.32, 0), (0.22, 0.22, 0), (0.32, 0, 0), (0.22, -0.22, 0), (0, -0.32, 0), (-0.22, -0.22, 0), (-0.32, 0, 0), (-0.22, 0.22, 0)]) 
        cmds.closeCurve(c1, ps=0, rpo=1)
        s1= cmds.curve(d=1, n=s1Name, p=[(-1.3, 1.3, 0), (1.3, 1.3, 0), (1.3, -1.3, 0), (-1.3, -1.3, 0), (-1.3, 1.3, 0)])
        cmds.makeIdentity(c1,s1, t=1, r=1, s=1, a=1)
        cmds.transformLimits(c1, tx=(-1,1), etx=(1,1), ty=(-1,1), ety=(1,1))
        attr=["tz","rx","ry","rz","sx","sy","sz","v"]
        for item in attr:
            cmds.setAttr("%s.%s"%(c1, item), l=1, k=0)
        s1Shp= cmds.listRelatives(s1, s=1)    
        cmds.setAttr("%s.overrideEnabled"%s1Shp[0] , 1)
        cmds.setAttr("%s.overrideDisplayType"%s1Shp[0] ,2)      
        cmds.parent(c1, s1)
        cmds.parent(s1, par)
        return s1

    def fbc(self):
        obj=cmds.ls(sl=1, tr=1)
        if len(obj)==1:
            test1, test2, test3= [], [], []
            if cmds.objExists("BlendshapeCheck_grp"):
                test1=1
            if cmds.objExists("CtrlTemp_Grp"):
                test2=1
            if cmds.objExists("fbc_BS"):
                test3=1
            if test1==1 and test2==1 and test3==1:
                cmds.warning("Facial Blendshape Checker already exist")
            elif test1==1:
                cmds.warning("<BlendshapeCheck_grp> exist in scene, please rename the object for Facial Blendshape Checker to work")
            elif test2==1:
                cmds.warning("<CtrlTemp_Grp> exist in scene, please rename object for Facial Blendshape Checker to work")   
            elif test3==1:
                cmds.warning("<fbc_BS> exist in scene, please rename blendshape for Facial Blendshape Checker to work")               
            else:
                geoShp= cmds.listRelatives(obj, s=1, typ="mesh")
                if geoShp:
                    bsTemp= cmds.listConnections("%s.inMesh"%geoShp[0], s=1, t="blendShape")
                    if bsTemp==None:
                        bb= cmds.xform(obj, bb=1, q=1)  
                        disX= round(bb[3]-bb[0], 2)
                        disY= round(bb[4]-bb[1], 2)  
                        disZ= round(bb[5]-bb[2], 2)  
                        #Create Dummy to get center pivot
                        dumm= cmds.duplicate(obj, n="bsDummy")
                        if cmds.listRelatives(dumm, p=1):
                            cmds.parent(dumm, w=1)
                        cmds.xform(dumm, cp=1)
                        tran= cmds.xform(dumm, rp=1, q=1, ws=1)   
                        cmds.delete(dumm)
                        ctrlGrp= cmds.group(em=1, n="CtrlTemp_Grp")  
                        ctrls= ["Mouth_Ctrl", "Lips_Ctrl","Cheek_Ctrl"] 
                        for stuff, dis in zip(ctrls, [-3,0,3]):
                            s1= self.creCtrl(stuff, stuff.replace("Ctrl", "CtrlGrp"), ctrlGrp)
                            cmds.xform(s1, t=(dis,0,0), ws=1)
                        cmds.xform(ctrlGrp, t=(disX*1.5,tran[1],tran[2]), s=(disX/6,disX/6,disX/6), r=1)    
                        #Duplicate meshes
                        bsGrp= cmds.group(em=1, n="BlendshapeCheck_grp")
                        bsName=["up_BS", "down_BS","wide_BS","narrow_BS","UpperLipRollOut_BS","UpperLipRollIn_BS","LowerLipRollOut_BS","LowerLipRollIn_BS","puffyCheeks_BS","suckCheeks_BS","sneer_BS"]
                        dupTranX=[-3.6,-1.2,1.2,3.6, -3.6,-1.2,1.2,3.6, -3.6,-1.2,1.2,3.6]
                        dupTranY=[2,2,2,2, 3.2,3.2,3.2,3.2, 4.4,4.4,4.4]
                        unlAttr=["t","r","tx","ty","tz","rx","ry","rz"]
                        allDup=[]
                        for item, dupX, dupY in zip(bsName, dupTranX, dupTranY):
                            dup= cmds.duplicate(obj, n="%s"%item)
                            for unl in unlAttr:
                                cmds.setAttr("%s.%s"%(dup[0], unl), l=0, k=1)
                            cmds.xform(dup, t=(disX*dupX, disY*dupY, 0), r=1)    
                            cmds.parent(dup, bsGrp) 
                            allDup.append(dup[0])           
                        cmds.blendShape(allDup[0],allDup[1],allDup[2],allDup[3],allDup[4],allDup[5],allDup[6],allDup[7],allDup[8],allDup[9],allDup[10], obj, n="fbc_BS")        
                        #Create expression    
                        cmds.expression(n="fbc_exp", o="", ae=1, uc="all", s="fbc_BS.%s= clamp(0,1, Mouth_Ctrl.ty);\nfbc_BS.%s= clamp(0,1, -Mouth_Ctrl.ty);\n\nfbc_BS.%s= clamp(0,1, Mouth_Ctrl.tx);\nfbc_BS.%s= clamp(0,1, -Mouth_Ctrl.tx);\n\nfbc_BS.%s= clamp(0,1, Lips_Ctrl.ty);\nfbc_BS.%s= clamp(0,1, -Lips_Ctrl.ty);\n\nfbc_BS.%s= clamp(0,1, Lips_Ctrl.tx);\nfbc_BS.%s= clamp(0,1, -Lips_Ctrl.tx);\n\nfbc_BS.%s= clamp(0,1, Cheek_Ctrl.tx);\nfbc_BS.%s= clamp(0,1, -Cheek_Ctrl.tx);\n\nfbc_BS.%s= clamp(0,1, Cheek_Ctrl.ty);\n"%(allDup[0],allDup[1],allDup[2],allDup[3],allDup[4],allDup[5],allDup[6],allDup[7],allDup[8],allDup[9],allDup[10]))
                        cmds.select(obj)
                    else:
                        cmds.warning("Selected object have an existing blendshape")
                else:
                    cmds.warning("Please select 1 GEOMETRY")
        else:
            cmds.warning("Please select 1 HEAD geometry")

    def extraTar(self):
        obj=cmds.ls(sl=1, tr=1)
        test1, test2= [], []    
        if len(obj)==1:
            geoShp= cmds.listRelatives(obj, s=1, typ="mesh")
            if geoShp:
                bsTemp= cmds.listConnections("%s.inMesh"%geoShp[0], s=1, t="blendShape")
                tgTemp= cmds.listConnections("%s.inMesh"%geoShp[0], s=1, t="transformGeometry")
                if bsTemp==["fbc_BS"] or tgTemp:  
                    if cmds.objExists("BlendshapeCheck_grp"):
                        test1=1
                    if cmds.objExists("CtrlTemp_Grp"):
                        test2=1
                    if test1==1 and test2==1:
                        ctrlBB= cmds.xform("CtrlTemp_Grp", bb=1, q=1)   
                        ctrlScale= cmds.getAttr("CtrlTemp_Grp.sx")
                        #8.6 is original ctrl bb
                        ctrlDis= round((ctrlBB[3]-ctrlBB[0])/ctrlScale-8.6, 2)
                        #/3 because original got 3 ctrl
                        sfx= int(ctrlDis/3+1)  
                        s1= self.creCtrl("Extra%s_Ctrl"%sfx, "Extra%s_CtrlGrp"%sfx, "CtrlTemp_Grp")
                        cmds.xform(s1, t=(ctrlDis+6,0,0), s=(1,1,1))
                        bbObj= cmds.xform(obj, bb=1, q=1, ws=1)  
                        center= round((bbObj[1]+bbObj[4])/2, 2) 
                        disX= round(bbObj[3]-bbObj[0], 2)
                        disY= round(bbObj[4]-bbObj[1], 2)  
                        disZ= round(bbObj[5]-bbObj[2], 2)
                        bsBB= cmds.xform("BlendshapeCheck_grp", bb=1, q=1, ws=1) 
                        #3.4 is original bs bb, /1.2 because the distance between blendshape is 1.2 ratio
                        bsDis= round((bsBB[4]-bsBB[1])/disY-3.4, 2)/disY/1.2
                        bsName=["extra%s_up_BS"%sfx, "extra%s_down_BS"%sfx,"extra%s_right_BS"%sfx,"extra%s_left_BS"%sfx]
                        dupTranX=[-3.6,-1.2,1.2,3.6]
                        unlAttr=["t","r","tx","ty","tz","rx","ry","rz"]
                        allDup=[]
                        for item, dupX in zip(bsName, dupTranX):
                            dup= cmds.duplicate(obj, n="%s"%item)
                            for unl in unlAttr:
                                cmds.setAttr("%s.%s"%(dup[0], unl), l=0, k=1)
                            tempY= cmds.xform(dup[0], q=1, t=1, ws=1) 
                            #is actually -0.5 (to get the last bs position) then add 1.2 = 0.7
                            #-center+tempY[1] is if the object is freeze
                            cmds.xform(dup, t=(disX*dupX, ((bsBB[4]+disY*0.7-center+tempY[1])), 0), ws=1)
                            cmds.parent(dup, "BlendshapeCheck_grp")
                            allDup.append(dup[0])  
                        #Adding blendshape
                        allBsIn= cmds.aliasAttr("fbc_BS", q=1)
                        D1, fullD= self.bsCal(allBsIn)  
                        realD1=[]      
                        for item in D1.keys():
                            realD1.append(int(item))            
                        val= max(realD1)
                        for x, thing in enumerate(allDup):
                            cmds.blendShape("fbc_BS", e=1, t=(obj[0], val+x+1, thing ,1))   
                        #Create expression    
                        cmds.expression(n="fbc_exp", o="", ae=1, uc="all", s="fbc_BS.%s= clamp(0,1, Extra%s_Ctrl.ty);\nfbc_BS.%s= clamp(0,1, -Extra%s_Ctrl.ty);\n\nfbc_BS.%s= clamp(0,1,Extra%s_Ctrl.tx);\nfbc_BS.%s= clamp(0,1, -Extra%s_Ctrl.tx);"%(allDup[0],sfx,allDup[1],sfx,allDup[2],sfx,allDup[3],sfx))
                        cmds.select(obj)
                    elif test1==[] and test2==[]:
                        cmds.warning("There is no Facial Blendshape Checker in the scene or it has been renamed")
                else:
                    cmds.warning("Selected object does not have Facial Blendshape Checker or it has been renamed")        
            else:
                cmds.warning("Please select 1 GEOMETRY")
        else:
            cmds.warning("Please select 1 head geometry")

    def grabInd(self):
        bsName= cmds.ls(sl=1, typ="blendShape")
        if len(bsName)==1 :    
            allBsIn= cmds.aliasAttr(bsName, q=1)
            if allBsIn:
                D1, fullD= self.bsCal(allBsIn)
                inCB= cmds.channelBox("mainChannelBox", sha=1, q=1)
                outCB= cmds.channelBox("mainChannelBox", soa=1, q=1)  
                try:
                    if inCB:
                        bsTar= inCB[0]
                        bsIn= int(D1.keys()[D1.values().index("%s"%bsTar)])+1
                    elif outCB:
                        bsTar= outCB[0]
                        bsIn= int(D1.keys()[D1.values().index("%s"%bsTar)])+1
                    else:
                        bsTar="--"
                        bsIn= 0    
                    cmds.scrollField(self.sf, e=1, tx="%s"%(".  ".join(fullD).replace("\n.  ", "\n")))
                    cmds.textFieldGrp(self.txtMesh, e=1, en=1, tx="%s"%cmds.ls(sl=1, tr=1)[0])
                    cmds.textFieldGrp(self.txtBsName, e=1, en=1, tx="%s"%bsName[0])
                    cmds.intFieldGrp(self.txtInd, e=1, en=1, v1=bsIn)
                except:
                    cmds.warning("Selected <Envelop>, which can't be used or selected incorrect attribute")
            else:
                cmds.warning("Selected node is not a blendshape")        
        else:
            cmds.warning("Please select 1 blendshape")

    def inBs(self):
        obj= cmds.ls(sl=1, tr=1)
        mesh= cmds.textFieldGrp(self.txtMesh, q=1, tx=1)
        bs= cmds.textFieldGrp(self.txtBsName, q=1, tx=1)
        ind= cmds.intFieldGrp(self.txtInd, q=1, v1=1)
        slide= cmds.floatSliderGrp(self.slidy, q=1, v=1)
        if mesh:
            if bs:
                if ind!=0:
                    if obj:
                        if len(obj)==1:
                            if cmds.checkBoxGrp(self.cb311, q=1, v1=1):
                                cmds.blendShape("%s"%bs, e=1, ib=1, t=(mesh, ind-1, obj[0], slide), tc=1) 
                            else:
                                #Some confusing shit, if use blendshape command, the index number need minus 1??
                                cmds.blendShape("%s"%bs, e=1, ib=1, t=(mesh, ind-1, obj[0], slide), tc=0) 
                            cmds.select(mesh)
                        else:
                            cmds.warning("Please select only 1 blendshape inbetween target")
                    else:
                        cmds.warning("Please select 1 blendshape inbetween target")
                else:
                    cmds.warning("<INDEX> field is empty!")
            else:
                cmds.warning("BLENDSHAPE text field is empty!")
        else:
            cmds.warning("MESH text field is empty!")

    def helps(self):
        name="Help On Blendshape"
        helpTxt=""" 
        - To create / remove blendshape (inbetween blendshape too)
        - To simulate facial rig to ease sculpt blendshape 



        < Basic >
        ===========
            1) Create Blendshape
                - Similar to <Create Blendshape> in Maya 
                (* Set to "Front of Chain", meaning its below to existing skincluster)

            2) Add / Remove Target
                - Similar to <Add/Remove target> in Maya but with selection base
                (* No need to manually specify which blendshape)

            3) Replace Target
                - Replace the blendshape target
                (* It will reconnect any connection if there is any)
                (* Will rename blendshape attribute and update expression that uses the name)


        < Facial Checker >
        ====================
            1. Setup Facial Checker
                - Create 11 blendshape targets that are connected to 3 facial ctrl

            2. Add xtra Target
                - To add extra blendshape target and ctrl to existing facial checker

            (* To ease modeller so they can test the combine expression and straight away sculpt)


        < Add Inbetween >
        =================
            - Similar to <Add Inbetween target> in Maya but will find the index for you
            (* Select that particular bs attribute it will find that index or else needa input the index you want from the scroll field)
            (* Works better than AliasAttr query because sometimes weight's index doesnt match blendshape index
                but this will rearrange and give you the exact number)
        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)    
       
    def reloadSub(self):
        Blendshape()   
        
                     
if __name__=='__main__':
    Blendshape() 
                   