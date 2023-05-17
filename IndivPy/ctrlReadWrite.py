import maya.cmds as cmds
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox
import json

class CtrlReadWrite(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):        
        try: 
            cmds.deleteUI("ctrlRW") 
        except:
            pass    
        cmds.window("ctrlRW", mb=1)              
        cmds.window("ctrlRW", t="Ctrl Read Write", s=1, e=1, wh=(350,330))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on CtrlReadWrite", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload CtrlReadWrite", c=lambda x:self.reloadSub())    
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Export")
        form1= cmds.formLayout(nd=100, p=column1)
        self.txtTar= cmds.textFieldButtonGrp(l="Targets : ", cw3=(50,50,50), adj=2, bl="  Grab  ", bc=lambda :self.grab()) 
        b1= cmds.button(l="Export", c= lambda x:self.exportCtrl())
        cmds.formLayout(form1, e=1,
                                af=[(self.txtTar, "top", 0),
                                    (b1, "top", 36)],
                                ap=[(self.txtTar, "left", 0, 0),
                                    (self.txtTar, "right", 0, 100),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 100)])  
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column2= self.uiStuffClass.sepBoxSub("Import")
        form2= cmds.formLayout(nd=100, p=column2)
        self.txtFImp= cmds.textFieldButtonGrp(l="Path : ", cw3=(40,50,50), adj=2, bl="  ...  ", bc=lambda :self.readPath()) 
        sep21= cmds.separator(h=5, st="in")
        self.cbSR= cmds.checkBoxGrp(l="", cw2=(10,10), cc=lambda x:self.cbx())
        self.txtFSear= cmds.textFieldGrp(l="Search :", cw2=(50,50), adj=2, en=0)   
        self.txtFRepl= cmds.textFieldGrp(l="Replace :", cw2=(50,50), adj=2, en=0)
        sep22= cmds.separator(h=5, st="in") 
        b21= cmds.button(l="Import Local", c=lambda x:self.importCtrl(1)) 
        b22= cmds.button(l="Import World", c=lambda x:self.importCtrl(2)) 
        b23= cmds.button(l="Select Ctrl From Path", c=lambda x:self.importCtrl(3)) 
        b24= cmds.button(l="Select Vertex", c=lambda x:self.selectVertex())     
        cmds.formLayout(form2, e=1,
                                af=[(self.txtFImp, "top", 0),
                                    (sep21, "top", 35),
                                    (self.cbSR, "top", 60),
                                    (self.txtFSear, "top", 50),
                                    (self.txtFRepl, "top", 73),
                                    (sep22, "top", 105),
                                    (b21, "top", 120),
                                    (b22, "top", 120),
                                    (b23, "top", 146),
                                    (b24, "top", 172)],
                                ap=[(self.txtFImp, "left", 0, 0),
                                    (self.txtFImp, "right", 0, 100),
                                    (sep21, "left", 0, 0),
                                    (sep21, "right", 0, 100),
                                    (self.cbSR, "left", 0, 0),
                                    (self.cbSR, "right", 0, 10),
                                    (self.txtFSear, "left", 40, 0),
                                    (self.txtFSear, "right", 0, 100),
                                    (self.txtFRepl, "left", 40, 0),
                                    (self.txtFRepl, "right", 0, 100),
                                    (sep22, "left", 0, 0),
                                    (sep22, "right", 0, 100),
                                    (b21, "left", 0, 0),
                                    (b21, "right", 0, 50),
                                    (b22, "left", 0, 51),
                                    (b22, "right", 0, 100),
                                    (b23, "left", 0, 0),
                                    (b23, "right", 0, 100),
                                    (b24, "left", 0, 0),
                                    (b24, "right", 0, 100)])
        cmds.setFocus(cmds.text(l= ""))
        cmds.showWindow("ctrlRW")

    def defi(self):
        self.obj= cmds.ls(sl=1)
        self.sear= cmds.textFieldGrp(self.txtFSear, tx=1, q=1)  
        self.repl= cmds.textFieldGrp(self.txtFRepl, tx=1, q=1) 
        self.fileDir= cmds.textFieldButtonGrp(self.txtFImp, tx=1, q=1)
        self.tar= cmds.textFieldButtonGrp(self.txtTar, tx=1, q=1).split(", ")

    def grab(self):
        self.defi()
        if self.obj:   
            test1= 1
            nonCtrl= []
            for item in self.obj:
                if cmds.listRelatives(item, pa=1, typ="nurbsCurve")==None:
                    test1= []
                    nonCtrl.append(item)
            conti1= self.dialogClass.printingDialog(nonCtrl, "< %s > successful\n< %s > are not CTRL"%(len(self.obj)-len(nonCtrl), len(nonCtrl)))
            if conti1:
                cmds.textFieldButtonGrp(self.txtTar, e=1, tx=", ".join(self.obj))                           
        else:
            cmds.warning("Select at least 1 CTRL")  

    def cbx(self):
        if cmds.checkBoxGrp(self.cbSR, q=1, v1=1):
            cmds.textFieldGrp(self.txtFSear, e=1, en=1)   
            cmds.textFieldGrp(self.txtFRepl, e=1, en=1)   
        else: 
            cmds.textFieldGrp(self.txtFSear, e=1, en=0)   
            cmds.textFieldGrp(self.txtFRepl, e=1, en=0)   
                    
    def exportCtrl(self):
        self.defi()
        test1= 1
        if self.tar:
            for item in self.tar:
                if cmds.listRelatives(item, pa=1, typ="nurbsCurve")==None:
                    test1=[]
            if test1: 
                filePath = cmds.fileDialog2(ff="*.json", ds=2, cap="Export Ctrl")      
                if filePath:
                    with open(filePath[0], "w") as f:                    
                        lv0,lv1= {},{}
                        self.uiStuffClass.loadingBar(1, len(self.tar))
                        for item in self.tar:
                            cp= cmds.xform(item, q=1, rp=1, ws=1)
                            rot= cmds.xform(item, q=1, ro=1, ws=1)
                            shp= cmds.listRelatives(item, pa=1, typ="nurbsCurve")
                            if shp:
                                lv2= {}
                                for stuff in shp:
                                    lv3= {}
                                    spans= cmds.getAttr("%s.spans"%stuff)
                                    deg= cmds.getAttr("%s.degree"%stuff)
                                    form= cmds.getAttr("%s.form"%stuff)
                                    if form==2:
                                        ans= spans
                                    else:
                                        ans= spans+deg
                                    for x in range(ans):
                                        pp= cmds.xform("%s.cv[%s]"%(stuff,x), q=1, t=1, ws=1)
                                        ppLocal= [round(pp[0]-cp[0], 4), round(pp[1]-cp[1], 4), round(pp[2]-cp[2], 4)]
                                        lv3["%s.cv[%s]"%(stuff,x)]= ppLocal

                                    lv2[stuff]= lv3
                                #Set the rotation here, as the 1st ctrlShape instead
                                lv2["%s, %s, %s"%(rot[0], rot[1], rot[2])]= []   
                                lv1[item]= lv2
                            self.uiStuffClass.loadingBar(2)    
                        lv0["LvnTools_CtrlReadWrite"]= lv1
                        json.dump(lv0, f, sort_keys=1, indent=4)                   
                        print("-----------------------------\nLvnTools_CtrlReadWrite Saved to ---- %s\n\n-----------------"%filePath[0])
                        self.uiStuffClass.loadingBar(3)
            else:
                cmds.warning("Selection included non-curve, please select ctrl only (Not the cvs)")
        else:
            cmds.warning("File path is empty, please insert the textfield")

    def readPath(self):
        filePath = cmds.fileDialog2(ff="*.json", ds=2, cap="Import Ctrl", fm=1)       
        fc, test1= [],[]
        if filePath:
            with open(filePath[0], "r") as f:
                fc= json.load(f)
        if fc:
            if list(fc.keys())[0]=="LvnTools_CtrlReadWrite":
                test1= 1
                cmds.textFieldButtonGrp(self.txtFImp, tx="%s"%filePath[0], e=1)
            if test1==[]:        
                cmds.warning("Selected an INCORRECT FILE")        
     
    def searRepl(self, tar):
        if cmds.checkBoxGrp(self.cbSR, q=1, v1=1)==1:
            tar= tar.replace(self.sear, self.repl)
        return tar

    def importCtrl(self, meth):
        self.defi()     
        fc, test1= [],[]
        #conti= 1
        if self.fileDir:
            with open(self.fileDir, "r") as f:
                fc= json.load(f)  
            if fc:  
                if list(fc.keys())[0]=="LvnTools_CtrlReadWrite":
                    lv1= list(fc.values())[0]

                    #Precheck
                    allCtrl, misCtrl, misShp, misCv= [],[],[],[]
                    self.uiStuffClass.loadingBar(1, len(lv1))
                    for ctrl in list(lv1.keys()):
                        self.uiStuffClass.loadingBar(2)
                        ctrl= self.searRepl(ctrl)
                        lv2= lv1[ctrl]
                        #Check if ctrl exists
                        if cmds.objExists(ctrl)==0:
                            misCtrl.append(ctrl)
                        else:
                            allCtrl.append(ctrl)
                            if meth==3:
                                continue

                            #Use sorted to flush out the stored orientation    
                            for x, shp in enumerate(sorted(lv2.keys())):
                                #The first one is storing the orientation
                                if x!=0:  
                                    shp= self.searRepl(shp)
                                    lv3= lv2[shp]
                                    
                                    #Check if ctrl shape exist (might change shape)
                                    if cmds.objExists(shp)==0:
                                        misShp.append(shp)
                                    else:     
                                        spans= cmds.getAttr("%s.spans"%shp)
                                        deg= cmds.getAttr("%s.degree"%shp)
                                        form= cmds.getAttr("%s.form"%shp)
                                        if form==2:
                                            ans= spans
                                        else:
                                            ans= spans+deg
                                        #Check if cvs number the same (might change shape without changing shape name)    
                                        if ans!=len(list(lv3.keys())):
                                            misCv.append(shp)
                    self.uiStuffClass.loadingBar(3)
                    if misCtrl==[] and misShp==[] and misCv==[]:
                        finalGrp=[]
                    else:
                        finalGrp= ["Missing Ctrl\n----------------------"]+misCtrl+["\n\nMissing Shape\n----------------------"]+misShp+["\n\nMisMatch Cvs\n----------------------"]+misCv
                    conti= self.dialogClass.printingDialog(finalGrp, "< %s > Missing Ctrl\n< %s > Missing Ctrl Shape\n< %s > Mismatch cvs number"%(len(misCtrl),len(misShp),len(misCv)))
                    if conti:
                        if meth!=3:
                            self.uiStuffClass.loadingBar(1, len(lv1))
                            for ctrl in list(lv1.keys()):
                                ctrl= self.searRepl(ctrl)
                                lv2= lv1[ctrl]
                                if cmds.objExists(ctrl):
                                    #Ctrl shape lv
                                    oldRot= sorted(lv2.keys())[0].split(", ")
                                    newRot= cmds.xform(ctrl, q=1, ro=1, ws=1)
                                    diffRot= [newRot[0]-float(oldRot[0]), newRot[1]-float(oldRot[1]), newRot[2]-float(oldRot[2])]

                                    #Use sorted to flush out the stored orientation 
                                    for x,shp in enumerate(sorted(lv2.keys())):
                                        
                                        #The first one is to get the orientation
                                        if x!=0:
                                            shp= self.searRepl(shp)
                                            lv3= lv2[shp]
                                            if cmds.objExists(shp):
                                                spans= cmds.getAttr("%s.spans"%shp)
                                                deg= cmds.getAttr("%s.degree"%shp)
                                                form= cmds.getAttr("%s.form"%shp)
                                                if form==2:
                                                    ans= spans
                                                else:
                                                    ans= spans+deg
                                                if ans==len(list(lv3.keys())):
                                                    
                                                    #Cv lv
                                                    for cvs in list(lv3.keys()):
                                                        cvs= self.searRepl(cvs)
                                                        lv4= lv3[cvs]
                                                        piv= cmds.xform(ctrl, q=1, ws=1, rp=1)
                                                        cmds.xform(cvs, t=(lv4[0]+piv[0], lv4[1]+piv[1], lv4[2]+piv[2]), ws=1)                                  

                                                        if meth==1:
                                                            cmds.rotate(diffRot[0], diffRot[1], diffRot[2], cvs, ws=1)
                                self.uiStuffClass.loadingBar(2)
                            self.uiStuffClass.loadingBar(3)
                        cmds.select(allCtrl)
                else:
                    cmds.warning("Selected an INCORRECT FILE")
        else:
            cmds.warning("File path is empty, please insert the textfield")  

    def selectVertex(self):
        obj= cmds.ls(sl=1)
        allCv= []
        if obj:
            self.uiStuffClass.loadingBar(1, len(obj))

            for item in obj:
                if ".cv" in item:
                    pass
                else:
                    shp= cmds.listRelatives(item, pa=1, typ="nurbsCurve")
                    if shp:
                        for stuff in shp:
                            allCv.append("%s.cv[*]"%stuff)
                self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3, sel=allCv)        
        else:
            cmds.warning("Please select a CTRL")

    def helps(self):    
        name="Help On CtrlReadWrite"
        helpTxt="""
        - To export / import ctrl position
        (* Eg. After create autorig and adjusted ctrl, if need to rebuild the ctrl sizes might be gone. So export / import the data to avoid redoing)



        A) Export
        ===========
            - <Grab> Get the selected ctrl you want to save the cvs position
            - <Export> Save out the cvs position as a .json
          
            
        B) Import
        ===========
            1. Path
                - Browse the file location

            2. Search Replace
                - (if there's name changes) use Search Replace for the ctrl in the .json file 

            3. Import Local / World
                - input the cvs position as local or world
                (* local meaning will work with different character but now didn't calculate the orientation)

            4. Select Ctrl From Path
                (* To double check is there any selection error)

            5. Select Vertex
                (* So you can proceed in scale locally, if needed)
        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)    
       
    def reloadSub(self):
        CtrlReadWrite()   
        
                     
if __name__=='__main__':
    CtrlReadWrite() 
                   
                

     
