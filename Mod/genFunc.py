import maya.cmds as cmds

class GenFunc(object):
    def multiGrp(self, *args):
        for item in reversed(args):
            if item!= args[-1]:
                #Same name issue
                if item==args[-2]:
                    chd= cmds.parent(item, args[args.index(item)+1])
                    tar= cmds.listRelatives(args[args.index(item)+1], f=1)
                else:
                    cmds.parent(item, chd)
                    tar= cmds.listRelatives(chd, f=1)
        return tar[0]

    def lockAttr(self, obj, attr):
        for item in attr:
            cmds.setAttr("%s.%s"%(obj,item), k=0, l=1)

    def ctrlShp(self, ctrl, color, meth=1):           
        shp= cmds.listRelatives(ctrl, typ="nurbsCurve")
        newShp= cmds.rename(shp, "%sShape"%ctrl.split("|")[-1])            
        cmds.setAttr("%s.overrideEnabled"%newShp, 1)
        if meth==1:
            cmds.setAttr("%s.overrideColor"%newShp, color)  
        elif meth==2:
            cmds.setAttr("%s.overrideDisplayType"%newShp, 2)
        return newShp
        
    def hideObjHis(self, obj):
        allHist= []
        count= 0
        hist= mel.eval('historyPopupFill( "%s", 0, 0 )'%obj) + mel.eval('historyPopupFill( "%s", 1, 0 )'%obj)
        for subHist in hist.split(" "):
            if subHist!="":
                if subHist not in allHist:
                    allHist.append(subHist)  
        #This is to remove the first empty " "    
        if hist[0]==" ":
            ans= hist[1:]
        else:
            ans= hist[0]      
        if cmds.attributeQuery("hiddenHistory", node=obj, ex=1)==0:
            cmds.addAttr(obj, ln="hiddenHistory", dt="string")
            cmds.setAttr("%s.hiddenHistory"%obj, ans, typ="string")
        else:
            preHist= cmds.getAttr("%s.hiddenHistory"%obj)
            if preHist:
                cmds.setAttr("%s.hiddenHistory"%obj, "%s %s"%(preHist,ans), typ="string")
        for allSubHist in allHist:
            cmds.setAttr("%s.ihi"%allSubHist, 0)