import maya.cmds as cmds
import Mod.uiStuff as uiStuff
import Mod.helpBox as helpBox


class Retrace(object):
    def __init__(self, *args):
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):  
        try: 
            cmds.deleteUI("retr") 
        except:
            pass    
        cmds.window("retr", mb=1)              
        cmds.window("retr", t="Retrace", s=1, e=1, wh=(350,510))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Retrace", c=lambda x:self.helps())        
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Retrace", c=lambda x:self.reloadSub())     
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Rotate")
        form1= cmds.formLayout(nd=100, p=column1)
        txt11= cmds.text(l="<Preview> then check both <Result 1> <Result 2>\nWhich result is the one you want\n\nIf both result is incorrect, then <COG> is wrong\nPlace the <COG> as perpendicular as both <Front> & <Up>\n\nFor better result, please select multiple subselection for the textfield", al="left", fn="smallObliqueLabelFont", en=1) 
        sep11= cmds.separator(h=5, st="in")
        self.txtTar= cmds.textFieldButtonGrp(l="Target :", cw3=(45,0,0), adj=2, bl="  Grab  ", bc=lambda :self.grab(self.txtTar, 1))
        self.txtCog= cmds.textFieldButtonGrp(l="COG:", cw3=(45,0,0), adj=2, bl="  Grab  ", bc=lambda :self.grab(self.txtCog, 2))        
        self.txtF= cmds.textFieldButtonGrp(l="Front :", pht="<Where point world Z>", cw3=(45,0,0), adj=2, bl="  Grab  ", bc=lambda :self.grab(self.txtF, 2))
        self.txtUp= cmds.textFieldButtonGrp(l="Up :", pht="<Where point world Y>", cw3=(45,0,0), adj=2, bl="  Grab  ", bc=lambda :self.grab(self.txtUp, 2))
        self.txtRes1= cmds.textFieldGrp(vis=0)
        self.txtRes2= cmds.textFieldGrp(vis=0)
        bSwi= cmds.button(l="Switch", c=lambda x:self.swi())
        txt12= cmds.text(l="Select NOTHING", fn="smallObliqueLabelFont", en=0)  
        b11= cmds.button(l="Get Target's Current Rotation (*Can Skip)", c=lambda x:self.getOriRot())
        self.txtOriRot= cmds.textFieldGrp(vis=0)
        self.b12= cmds.button(l="Preview Zero Rotation", c=lambda x:self.previewZR())
        b13= cmds.button(l="Result 1", c=lambda x:self.res(1))
        b14= cmds.button(l="Result 2", c=lambda x:self.res(2))
        self.b15= cmds.button(l="Retrace Rotate", en=0, c=lambda x:self.retRot()) 
        cmds.formLayout(form1, e=1,
                                af=[(txt11, "top", 0),
                                    (sep11, "top", 105),
                                    (self.txtTar, "top", 130),
                                    (self.txtCog, "top", 156),
                                    (self.txtF, "top", 182),
                                    (self.txtUp, "top", 208),
                                    (bSwi, "top", 195),
                                    (txt12, "top", 254),
                                    (b11, "top", 270),
                                    (self.b12, "top", 306),
                                    (b13, "top", 332),
                                    (b14, "top", 332),
                                    (self.b15, "top", 358)],
                                ap=[(txt11, "left", 0, 0),
                                    (txt11, "right", 0, 100),
                                    (sep11, "left", 0, 0),
                                    (sep11, "right", 0, 100),
                                    (self.txtTar, "left", 0, 0),
                                    (self.txtTar, "right", 0, 100),
                                    (self.txtCog, "left", 0, 0),
                                    (self.txtCog, "right", 0, 100),                                    
                                    (self.txtF, "left", 0, 0),
                                    (self.txtF, "right",60, 100),
                                    (self.txtUp, "left", 0, 0),
                                    (self.txtUp, "right", 60, 100),
                                    (bSwi, "left", -60, 100),
                                    (bSwi, "right", 0, 100),
                                    (txt12, "left", 0, 0),
                                    (txt12, "right", 0, 100),
                                    (b11, "left", 0, 0),
                                    (b11, "right", 0, 100),
                                    (self.b12, "left", 0, 0),
                                    (self.b12, "right", 0, 100),
                                    (b13, "left", 0, 0),
                                    (b13, "right", 0, 50),
                                    (b14, "left", 0, 51),
                                    (b14, "right", 0, 100),
                                    (self.b15, "left", 0, 0),
                                    (self.b15, "right", 0, 100)])     
        cmds.setFocus(cmds.text(l=""))
        self.uiStuffClass.multiSetParent(4)
        column2= self.uiStuffClass.sepBoxSub("Translate")
        form2= cmds.formLayout(nd=100, p=column2)
        txt21= cmds.text(l="Select TARGETS", fn="smallObliqueLabelFont", en=0)  
        b21= cmds.button(l="Retrace Translate", c=lambda x:self.retTran())
        cmds.formLayout(form2, e=1,
                                af=[(txt21, "top", 0),
                                    (b21, "top", 16)],
                                ap=[(txt21, "left", 0, 0),
                                    (txt21, "right", 0, 100),
                                    (b21, "left", 0, 0),
                                    (b21, "right", 0, 100)])
        cmds.setFocus(cmds.text(l="")) 
        cmds.showWindow("retr")

    def defi(self):
        self.frontD= cmds.textFieldButtonGrp(self.txtF, q=1, tx=1) 
        self.upD= cmds.textFieldButtonGrp(self.txtUp, q=1, tx=1) 
        self.cog= cmds.textFieldButtonGrp(self.txtCog, q=1, tx=1)
        self.tar= cmds.textFieldGrp(self.txtTar, q=1, tx=1)
        self.res1= cmds.textFieldGrp(self.txtRes1, q=1, tx=1)
        self.res2= cmds.textFieldGrp(self.txtRes2, q=1, tx=1)  
        self.oriRot= cmds.textFieldGrp(self.txtOriRot, q=1, tx=1)  

    def grab(self, txt, meth):
        obj= cmds.ls(sl=1, fl=1) 
        if obj:
            if meth==1:
                if len(obj)==1:
                    if "." not in obj[0]:
                        cmds.textFieldButtonGrp("%s"%txt, e=1, tx="%s"%obj[0])
                    else:
                        cmds.warning("Please select TRANSFORM only")
                else:
                    cmds.warning("Please select only 1 TARGET")
            else:
                cmds.textFieldButtonGrp("%s"%txt, e=1, tx=", ".join(obj))
        else:
            cmds.warning("Select 1 TARGET")      

    def swi(self):
        self.defi()
        cmds.textFieldButtonGrp(self.txtF, e=1, tx=self.upD) 
        cmds.textFieldButtonGrp(self.txtUp, e=1, tx=self.frontD)         

    def getOriRot(self):
        self.defi()
        rot= cmds.xform(self.tar, q=1, ro=1, ws=1)
        cmds.textFieldGrp(self.txtOriRot, e=1, tx="%s"%rot)
        cmds.button(self.b15, e=1, en=1)

    def loc(self, obj): 
        tar= cmds.spaceLocator()  
        if len(obj.split(", "))>1:
            tempPivX, tempPivY, tempPivZ= [],[],[]
            for item in obj.split(", "):
                tempPiv= self.locPiv([item])
                for x,stuff in enumerate([tempPivX, tempPivY, tempPivZ]):
                    stuff.append(tempPiv[x])
            piv= [round((min(tempPivX)+max(tempPivX))/2, 3), round((min(tempPivY)+max(tempPivY))/2, 3), round((min(tempPivZ)+max(tempPivZ))/2, 3)]           
        else:
            piv= self.locPiv(obj.split(", "))         
        cmds.xform(tar, t=(piv[0],piv[1],piv[2]), ws=1)
        return tar

    def locPiv(self, obj):
        if cmds.objectType(obj)=="joint":                                   
            piv= cmds.xform(obj, q=1, rp=1, ws=1)
        else:   
            tempPiv= cmds.exactWorldBoundingBox(obj)
            piv= [round((tempPiv[0]+tempPiv[3])/2, 3), round((tempPiv[1]+tempPiv[4])/2, 3), round((tempPiv[2]+tempPiv[5])/2, 3)]
        return piv

    def previewZR(self):
        self.defi()
        if self.tar:
            if self.tar!= self.frontD and self.tar!= self.upD: 
                self.uiStuffClass.loadingBar(1, 1)
                realF= self.loc(self.frontD)
                realU= self.loc(self.upD)
                realC1= self.loc(self.cog)
                realC2= cmds.duplicate(realC1)
                dup= cmds.duplicate(self.tar, po=1)
                cmds.makeIdentity(dup, a=1, r=1, n=0, pn=1)
                #Result 1
                cmds.aimConstraint(realF[0], realC1[0], w=1, wut="object", aim=[0,0,1], u=[0,1,0], wuo=realU[0])
                cmds.orientConstraint(realC1[0], dup, mo=1, w=1)
                cmds.xform(realC1, ro=(0,0,0)) 
                #Result 2
                cmds.aimConstraint(realU[0], realC2[0], w=1, wut="object", aim=[0,1,0], u=[0,0,1], wuo=realF[0])
                oc= cmds.orientConstraint(realC2[0], self.tar, mo=1, w=1)
                cmds.xform(realC2, ro=(0,0,0))
                ans1= cmds.xform(dup, q=1, ro=1, r=1)
                ans2= cmds.xform(self.tar, q=1, ro=1, r=1)
                cmds.textFieldGrp(self.txtRes1, e=1, tx="%s"%ans1)            
                cmds.textFieldGrp(self.txtRes2, e=1, tx="%s"%ans2)
                cmds.delete(oc, realC1, realC2, dup, realF, realU)
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=self.tar)
            else:
                cmds.warning("<TARGET> should NOT be the same as <Front> or <Up>")
        else:
            cmds.warning("<TARGET> textfield is empty!")

    def res(self, meth):
        self.defi()
        if self.tar:
            if self.res1 and self.res2:
                if meth==1:
                    val= eval(self.res1)
                else:
                    val= eval(self.res2)
                cmds.xform(self.tar, ro=(val[0],val[1],val[2]))
            else:
                cmds.warning("Please run <Preview Zero Rotation> first!")
        else:
            cmds.warning("<TARGET> textfield is empty!")

    def retRot(self):
        self.defi()
        if self.tar:
            if self.res1 and self.res2:
                self.uiStuffClass.loadingBar(1, 1)
                oriRot= eval(self.oriRot)
                dup= cmds.duplicate(self.tar, po=1)
                tempTar= cmds.duplicate(self.tar, po=1)
                cmds.makeIdentity(self.tar, tempTar, a=1, r=1)
                cmds.parent(tempTar, dup)
                cmds.xform(dup, ro=(oriRot[0], oriRot[1], oriRot[2]))
                cmds.parent(tempTar, w=1)
                rot= cmds.xform(tempTar, ro=1, q=1, ws=1)
                cmds.xform(self.tar, ro=(rot[0], rot[1], rot[2]), ws=1)
                #cleanup
                cmds.delete(dup, tempTar)
                cmds.textFieldGrp(self.txtRes1, e=1, tx="")
                cmds.textFieldGrp(self.txtRes2, e=1, tx="") 
                self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=self.tar)
            else:
                cmds.warning("Please run <Preview Zero Rotation> first!")
        else:
            cmds.warning("<TARGET> textfield is empty!")

    def retTran(self):
        obj= cmds.ls(sl=1)
        test1, test2= [],[]
        if obj:
            for item in obj:
                if "." not in item:
                    test1=1
        else:
            cmds.warning("Please select at least 1 TARGET")
        if test1:
            for item in obj:
                rPiv= cmds.xform(item, q=1, rp=1, ws=1)
                prePos= cmds.xform(item, q=1, t=1, ws=1)
                if [round(rPiv[0],4),round(rPiv[1],4),round(rPiv[2],4)]!=[round(prePos[0],4),round(prePos[1],4),round(prePos[2],4)]:
                    test2= 1
            if test2:
                self.uiStuffClass.loadingBar(1, len(obj))
                for item in obj:
                    rPiv= cmds.xform(item, q=1, rp=1, ws=1)
                    dup= cmds.duplicate(item, po=1)
                    par= cmds.listRelatives(item, p=1, pa=1)
                    if par:
                        newItem= cmds.parent(item, w=1)
                    else:
                        newItem= item
                    chd= cmds.listRelatives(item, c=1, pa=1)
                    finalChd= []
                    if chd:
                        for allChd in chd:
                            if cmds.objectType(allChd)!="mesh":
                                finalChd.append(allChd)
                        if finalChd:
                            newChd= cmds.parent(finalChd, w=1)
                    else:
                        finalChd= chd
                    cmds.move(0,0,0, item, rpr=1)    
                    cmds.makeIdentity(item, a=1, t=1, n=0, pn=1)
                    cmds.xform(item, t=(rPiv[0],rPiv[1],rPiv[2]), ws=1)
                    cmds.delete(dup[0])  
                    if par:
                        cmds.parent(item, par)
                    if finalChd:
                        cmds.parent(finalChd, item)
                    self.uiStuffClass.loadingBar(2)
                self.uiStuffClass.loadingBar(3, sel=obj)
            else:
                cmds.warning("All of the selected TARGET already have a correct translate")

    def helps(self):
        name="Help On Retrace"
        helpTxt=""" 
        - To retrace object's rotation / translation before freeze



        < Rotate >
        ========== 
            1) Textfield
            ------------
                - Except for "Target", better select multiple subselection (vertex) to get the most accurate data for each textfield
                
                - COG   = This is the most crucial. Best position is perpendicular to both <Front>, <Up>
                          (* If cant then perpendicular to one of them and use <Result> to test)
                          (* Something like the center of the basic shape NOT center pivot of current shape)
                          (* eg. steering = circle/oval; rock = cube)
                - Front = After retrace, when zero rotation, which direction is point world Z
                - Up    = After retrace, when zero rotation, which direction is point world Y


            2) Retracing
            ------------
                1. Get Target Current Rotation
                    - Get the current rotation so that can snap back the object to original postion
                    (* Can skip this step if you wanted it to be back to zero rotation)

                2. Preview Zero Rotation
                    - To check when the object is at zero, is it correct
                    (* Can freeze from here if you don't need to revert back to the custom rotation)

                3. Result 1 / Result 2
                    -This is just a different result of <Preview Zero Rotation> because depends on COG accuracy

                4. Retrace Rotate
                    - Will put back target to how it was but with rotation value


        < Translate >
        ==============
            - Retrace original translation 
        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)    
       
    def reloadSub(self):
        Retrace()   
        
                     
if __name__=='__main__':
    Retrace() 
                   
