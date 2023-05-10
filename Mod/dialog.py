import maya.cmds as cmds
import maya.mel as mel
import time

class Dialog(object):
    def successDialog(self):
        cmds.confirmDialog( t="Success", m="Function Success!    ", button=["Ok"])        
        print ""

    def warningDialog(self, msg):
        cmds.confirmDialog(t="Warning", m=msg, button=["Return"])     

    def sameNameOrNoExistDialog(self, obj, sear, repl, noPop=[], exist=1):
        conti= 1
        sameName,noExist,success,finalTar,dupName= [],[],[],[],[]
        for item in obj:
            #Super long because for same name object, just replace the [-1] and needa put back the front parent name
            realName= item.split("|")[-1]
            parName= ("|").join(item.split("|")[:-1])
            if realName.replace(sear, repl)==realName:
                sameName.append(item)
            else:    
                if parName:
                    newName= "%s|%s"%(parName, realName.replace(sear,repl))
                else:
                    newName= realName.replace(sear,repl)

                #Checking noExist/dupName/success/finalTar    
                if cmds.objExists(newName)==0:
                    noExist.append("%s    ( %s )"%(item, newName))
                else:
                    if len(cmds.ls(newName))>1:
                        dupName.append("%s    ( %s )"%(item, newName))
                    else:
                        success.append(item)
                        finalTar.append(newName)
            
        #exist is for renamer because it no need to search for a target
        if exist==[]:
            noExist= []    

        #Pop out layoutDialog              
        if sameName or noExist or dupName:    
            if noPop==[]:
                ans= cmds.layoutDialog(t="Continue Or Not", ui=lambda :self.sameNameOrNoExistDialogUI1(sameName, noExist, dupName, success))
                if ans=="Continue":
                    conti= 1
                elif ans=="No + Print":
                    conti=[]
                    self.sameNameOrNoExistDialogUI2(sameName, noExist, dupName, success)
                else:
                    conti=[]
        return conti, finalTar 
  
    #This is just for copyWeight's Search Replace Influence because need to stack    
    def sameNameOrNoExistSrDialog(self, obj, sear, repl, noPop=[], sameName=[], noExist=[], success=[], dupName=[]):
        conti= 1
        finalTar,newSuccess,newFinalTar,newSameName= [],[],[],[]
        if obj:
            for item in obj:
                #Super long because for same name object, just replace the [-1] and needa put back the front parent name
                realName= item.split("|")[-1]
                parName= ("|").join(item.split("|")[:-1])
                if realName.replace(sear, repl)==realName:
                    sameName.append(item)
                else:    
                    if parName:
                        newName= "%s|%s"%(parName, realName.replace(sear,repl))
                    else:
                        newName= realName.replace(sear,repl)

                    #Checking noExist/dupName/success/finalTar    
                    if cmds.objExists(newName)==0:
                        noExist.append("%s    ( %s )"%(item, newName))
                    else:
                        if len(cmds.ls(newName))>1:
                            dupName.append("%s    ( %s )"%(item, newName))
                        else:
                            #finalTar is after item become search replace
                            finalTar.append(newName)
                            if newName not in obj:
                                newSuccess.append("%s    ( %s )"%(item, newName))
                                newFinalTar.append(newName)
            for stuff in sameName:
                if stuff not in finalTar:
                    newSameName.append(stuff)
            success,finalTar,sameName= newSuccess,newFinalTar,newSameName

        #Pop out layoutDialog              
        if sameName or noExist or dupName:   
            if noPop==[]:
                ans= cmds.layoutDialog(t="Continue Or Not", ui=lambda :self.sameNameOrNoExistDialogUI1(sameName, noExist, dupName, success))
                if ans=="Continue":
                    conti= 1
                elif ans=="No + Print":
                    conti=[]
                    self.sameNameOrNoExistDialogUI2(sameName, noExist, dupName, success)
                else:
                    conti=[]
        return conti, finalTar, sameName, noExist, success, dupName 

    def sameNameOrNoExistDialogUI1(self, tar1, tar2, tar3, tar4):
        form= cmds.setParent(q=1)
        cmds.formLayout(form, e=1, nd=100, w=500)
        txt1= cmds.text(l="< %s > Same Name As Source"%len(tar1))
        txt2= cmds.text(l="< %s > Name Does Not Exist"%len(tar2))
        txt3= cmds.text(l="< %s > Duplicated Target"%len(tar3))
        txt4= cmds.text(l="< %s > Success"%len(tar4))
        sf1= cmds.scrollField(ed=0, fn="plainLabelFont", tx="- %s"%("\n- ".join(tar1)))
        sf2= cmds.scrollField(ed=0, fn="plainLabelFont", tx="- %s"%("\n- ".join(tar2)))
        sf3= cmds.scrollField(ed=0, fn="plainLabelFont", tx="- %s"%("\n- ".join(tar3)))
        sf4= cmds.scrollField(ed=0, fn="plainLabelFont", tx="- %s"%("\n- ".join(tar4)))
        but1= cmds.button(l="Continue", c="cmds.layoutDialog(dis='Continue')")
        but2= cmds.button(l="No", c="cmds.layoutDialog(dis='No')")
        but3= cmds.button(l="No + Print", c="cmds.layoutDialog(dis='No + Print')")
        cmds.formLayout(form, e=1,
                            af=[(txt1, "top", 10),
                                (txt2, "top", 10),
                                (txt3, "top", 10),
                                (txt4, "top", 10),
                                (sf1, "top", 31),
                                (sf2, "top", 31),
                                (sf3, "top", 31),
                                (sf4, "top", 31),
                                (but1, "bottom", 5),
                                (but2, "bottom", 5),
                                (but3, "bottom", 5)],
                            ac=[(sf1, "bottom", 10, but1),
                                (sf2, "bottom", 10, but1),
                                (sf3, "bottom", 10, but1),
                                (sf4, "bottom", 10, but1)],    
                            ap=[(txt1, "left", 0, 0),
                                (txt1, "right", 0, 25),
                                (txt2, "left", 0, 26),
                                (txt2, "right", 0, 50),
                                (txt3, "left", 0, 51),
                                (txt3, "right", 0, 75),
                                (txt4, "left", 0, 76),
                                (txt4, "right", 0, 100),
                                (sf1, "left", 0, 0),
                                (sf1, "right", 0, 25),
                                (sf2, "left", 0, 26),
                                (sf2, "right", 0, 50),
                                (sf3, "left", 0, 51),
                                (sf3, "right", 0, 75),
                                (sf4, "left", 0, 76),
                                (sf4, "right", 0, 100),
                                (but1, "left", 0, 0),
                                (but1, "right", 0, 33),
                                (but2, "left", 0, 34),
                                (but2, "right", 0, 66),
                                (but3, "left", 0, 67),
                                (but3, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))

    def sameNameOrNoExistDialogUI2(self, tar1, tar2, tar3, tar4):
        try: 
            cmds.deleteUI("snone") 
        except:
            pass  
        cmds.window("snone")
        cmds.window("snone", e=1, t="Targets With Naming Problem", s=1, wh=(700,300))
        snone1= cmds.paneLayout(cn="vertical4", w=700)
        cmds.paneLayout(snone1, e=1, ps=[1,25,25])
        cmds.paneLayout(snone1, e=1, ps=[2,25,25])
        cmds.paneLayout(snone1, e=1, ps=[3,25,25])
        cmds.paneLayout(snone1, e=1, ps=[4,25,25])
        cmds.scrollField(ed=0, fn="plainLabelFont", tx="< %s > Same Name As Source\n-----------------------------------\n\n%s"%(len(tar1),"- %s"%("\n- ".join(tar1))))
        cmds.scrollField(ed=0, fn="plainLabelFont", tx="< %s > Name Does Not Exist\n----------------------------------\n\n%s"%(len(tar2),"- %s"%("\n- ".join(tar2))))
        cmds.scrollField(ed=0, fn="plainLabelFont", tx="< %s > Duplicated Target\n------------------------------\n\n%s"%(len(tar3),"- %s"%("\n- ".join(tar3))))
        cmds.scrollField(ed=0, fn="plainLabelFont", tx="< %s > Succeeded\n---------------------\n\n%s"%(len(tar4),"- %s"%("\n- ".join(tar4))))
        cmds.showWindow("snone")

    def continueDialog(self, tar, msg):
        if tar:
            conti= 1
        else:
            ans= cmds.confirmDialog(t="Continue Or Not", m="%s"%msg, button=["Continue", "No"])        
            if ans=="Continue":
                conti= 1
            else:
                conti= []
        return conti

    def printingDialog(self, tar, msg):
        conti= 1
        if tar:
            ans= cmds.layoutDialog(t="Continue Or Not", ui=lambda :self.printingDialogUI1(msg, tar))
            if ans=="Continue":
                conti= 1
            elif ans=="No + Print":
                self.printingDialogUI2(msg, tar)
                conti= []
            else:
                conti= []
        return conti  

    def printingDialogUI1(self, msg, tar):
        form= cmds.setParent(q=1)
        t1= cmds.text(l=msg)
        sf= cmds.scrollField(ed=0, fn="plainLabelFont", tx="\n".join(tar), ip=100)
        but1= cmds.button(l="Continue", c="cmds.layoutDialog(dis='Continue')")
        but2= cmds.button(l="No", c="cmds.layoutDialog(dis='No')")
        but3= cmds.button(l="No + Print", c="cmds.layoutDialog(dis='No + Print')")
        cmds.setFocus(cmds.text(l=""))
        cmds.formLayout(form, e=1, nd=100, w=400,
                            af=[(t1, "top", 10),
                                (sf, "top", 50),
                                (but1, "bottom", 5),
                                (but2, "bottom", 5),
                                (but3, "bottom", 5)],
                            ac=[(sf, "bottom", 10, but1)],    
                            ap=[(t1, "left", 0, 0),
                                (t1, "right", 0, 100),
                                (sf, "left", 0, 0),
                                (sf, "right", 0, 100),
                                (but1, "left", 0, 0),
                                (but1, "right", 0, 33),
                                (but2, "left", 0, 34),
                                (but2, "right", 0, 66),
                                (but3, "left", 0, 67),
                                (but3, "right", 0, 100)])

    def printingDialogUI2(self, msg, tar):
        try: 
            cmds.deleteUI("pd") 
        except:
            pass  
        cmds.window("pd")
        cmds.window("pd", e=1, t="Target List", s=1, wh=(200,300))
        cmds.frameLayout("pd1", lv=0)
        cmds.separator(h=5, st="none") 
        cmds.setFocus(cmds.text(l=msg))
        cmds.separator(h=5, st="none")
        cmds.scrollField(ed=0, fn="plainLabelFont", tx="\n".join(tar))
        cmds.showWindow("pd")

