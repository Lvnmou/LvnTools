import maya.cmds as cmds
import Mod.dialog as dialog
import Mod.uiStuff as uiStuff
import Mod.genFunc as genFunc
import Mod.helpBox as helpBox
import re

class GrpMaker(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()
        self.genFuncClass= genFunc.GenFunc()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self):    
        try:
            cmds.deleteUI("grpM")
        except:
            pass            
        cmds.window("grpM", mb=1)
        cmds.window("grpM", t="Group Maker", e=1, s=1, wh=(240,280))   
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on GroupMaker", c=lambda x: self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload GroupMaker", c=lambda x: self.reloadSub()) 
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Create")
        form1= cmds.formLayout(nd=100, p=column1)
        self.txtF1= cmds.textFieldGrp(l="Suffix :", cw2=(50,50), tx="_grp", adj=2)
        self.txtSear= cmds.textFieldGrp(l="Search :", cw2=(50,50), adj=2)
        self.txtRepl= cmds.textFieldGrp(l="Replace :", cw2=(50,50), adj=2)
        self.slider= cmds.intSliderGrp(f=1, l="Groups :", cw3=(50,30,50), min=1, max=10, fmx=100, v=1)    
        b1= cmds.button(l="Group", c=lambda x: self.final())
        cmds.formLayout(form1, e=1,
                                af=[(self.txtF1, "top", 0),
                                    (self.txtSear, "top", 26),
                                    (self.txtRepl, "top", 52),
                                    (self.slider, "top", 78),
                                    (b1, "top", 114)],
                                ap=[(self.txtF1, "left", 0, 0),
                                    (self.txtF1, "right", 0, 100),
                                    (self.txtSear, "left", 0, 0),
                                    (self.txtSear, "right", 0, 100),
                                    (self.txtRepl, "left", 0, 0),
                                    (self.txtRepl, "right", 0, 100),
                                    (self.slider, "left", 0, 0),
                                    (self.slider, "right", 0, 100),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 100)])  
        cmds.showWindow("grpM")

    def transfer(self, tar, grp1):  
        tran= cmds.xform(tar, q=1, t=1, ws=1)
        rot= cmds.xform(tar, q=1, ro=1, ws=1)
        scal= cmds.xform(tar, q=1, s=1, ws=1)
        piv= cmds.xform(tar, q=1, rp=1, ws=1) 
        rotOr= cmds.getAttr("%s.rotateOrder"%tar)
        cmds.setAttr("%s.rotateOrder"%grp1, rotOr)  
        cmds.xform(grp1, t=(tran[0],tran[1],tran[2]), ro=(rot[0],rot[1],rot[2]), s=(scal[0],scal[1],scal[2]))             
        cmds.xform(grp1, ws=1, rp=(piv[0], piv[1], piv[2]), sp=(piv[0], piv[1], piv[2]))        

    def updateList(self, currentList, sear, repl):
        newList=[] 
        if currentList:
            for item in currentList:
                newItem= re.sub(r"^%s"%re.escape("%s|"%sear), "%s|"%repl, item)
                newList.append(newItem)
            return newList    

    def final(self):
        obj= sorted(cmds.ls(sl=1, l=1))
        sfx= cmds.textFieldGrp(self.txtF1, q=1, tx=1)
        sear= cmds.textFieldGrp(self.txtSear, q=1, tx=1)
        repl= cmds.textFieldGrp(self.txtRepl, q=1, tx=1)
        slidy1= cmds.intSliderGrp(self.slider, q=1, v=1)
        finalTar, allJnt, allTar, firstGrp, lastGrp= [],[],[],[],[]
        test1, test2= 1,1
        attr=["tx","ty","tz","rx","ry","rz","sx","sy","sz"]
        attrVal=[0.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0]           
        if obj:
             
            for item in obj:
                for stuff in zip(attr,attrVal):
                    if cmds.getAttr("%s.%s"%(item,stuff[0]), l=1)==1:
                        val= cmds.getAttr("%s.%s"%(item,stuff[0]))
                        if round(val, 3)!=stuff[1]:
                            test1=[] 
                if cmds.objectType(item)=="joint":
                    allJnt.append(item)
            if test1:
                conti1= self.dialogClass.printingDialog(allJnt, "< %s > successful \n< %s > are joints, did you FREEZE the joints??"%(len(obj)-len(allJnt),len(allJnt)))
                if conti1:
                    self.uiStuffClass.loadingBar(1, len(obj))
                    for x,item in enumerate(obj):
                        par= cmds.listRelatives(obj[x], f=1, p=1)

                        #Search Replace OR adding suffix
                        if sear:
                            grp1= cmds.group(obj[x], em=1, n=(obj[x].split("|")[-1]).replace(sear,repl))
                        else:
                            if sfx:
                                if slidy1==1:
                                    grp1= cmds.group(obj[x], em=1, n="%s%s"%(obj[x].split("|")[-1],sfx)) 
                                else:
                                    grp1= cmds.group(obj[x], em=1, n="%s%s1"%(obj[x].split("|")[-1],sfx)) 
                            else:
                                grp1= cmds.group(obj[x], em=1, n="%s1"%(obj[x].split("|")[-1]))
                        self.transfer(obj[x], grp1)  
                        for y in range(slidy1, 1, -1):
                            grps= cmds.duplicate(grp1)
                            #might have same name especially if run <Group> multiple time
                            grps= cmds.rename(grps, grp1.replace("|","").replace("%s1"%sfx, "%s%s"%(sfx, y)))
                            if y==slidy1:
                                lastGrp= grps
                            else:
                                grps= cmds.parent(grps, preGrp)
                            if y==2:
                                firstGrp= grps                                    
                            preGrp= grps
                        if firstGrp:
                            newTar= self.genFuncClass.multiGrp(obj[x], grp1, firstGrp)
                        else:
                            newTar= self.genFuncClass.multiGrp(obj[x], grp1)
                        if par:
                            if lastGrp:
                                cmds.parent(lastGrp, par)
                            else:
                                cmds.parent(grp1, par)
                            newTar= "%s%s"%(par[0],newTar)
                        obj= self.updateList(obj, obj[x], newTar)
                        finalTar.append(newTar)
                        self.uiStuffClass.loadingBar(2)
                    self.uiStuffClass.loadingBar(3, sel=finalTar)  
            else:
                cmds.warning("One of the target is LOCKED (will work for locked object if all attribute is zero)")                   
        else:
            cmds.warning("Please select at least 1 TARGET")                           
       
    def helps(self):
        name="Help On GroupMaker"
        helpTxt=""" 
        - Create group that have the same channel value, pivot point, rotation order
        - So that the target that you select have clean channel value (zero)



        < Create >
        ============
            1. Work for normal, custom pivot, freeze object
            2. For joint, must FREEZE or else will mess up

            (* Search & replace is usually use for creating groups for groups 
               eg. joint1
                   joint1_grp
                   joint1_fixGrp)


            
        """
        self.helpBoxClass.helpBox1(name, helpTxt)

    def reloadSub(self):
        GrpMaker()  
        
        
if __name__ == '__main__':
    GrpMaker()

