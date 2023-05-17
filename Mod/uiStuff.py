import maya.cmds as cmds
import time

class UiStuff(object):
    def sepBoxMain(self):
        cmds.columnLayout(adj=1)
        self.pb1= cmds.progressBar()
        self.pb2= cmds.progressBar(pr=0, vis=0)  
        cmds.setParent("..")
        cmds.tabLayout(cr=1, scr=1)

    def sepBoxSub(self, name=[], ebg=1):
        if name:
            cmds.columnLayout("%s"%name, adj=1)
            cmds.setFocus(cmds.text(l=""))
        form = cmds.formLayout(nd=100)
        column= cmds.frameLayout(lv=0, bv=0)
        cmds.setParent("..")
        sep1= cmds.separator(h=1, st="none", bgc=(0,0,0))
        sep2= cmds.separator(h=1, st="none", bgc=(0,0,0))
        sep3= cmds.separator(hr=0, w=1, st="none", bgc=(0,0,0))
        sep4= cmds.separator(hr=0, w=1, st="none", bgc=(0,0,0))
        cmds.formLayout(form, e=1, 
                            af=[(sep1, "top", 0),
                                (sep1, "left", 5),
                                (sep1, "right", 5),
                                (sep2, "bottom", 5),
                                (sep2, "left", 5),
                                (sep2, "right", 5),
                                (sep3, "top", 0),
                                (sep3, "left", 5),
                                (sep3, "bottom", 5),
                                (sep4, "top", 0),
                                (sep4, "right", 5),
                                (sep4, "bottom", 5),
                                (column, "top", 10),
                                (column, "bottom", 15),
                                (column, "left", 8),
                                (column, "right", 8)])         
        cmds.setParent("..")
        return column  

    def multiSetParent(self, num):
        for x in range(num):
            cmds.setParent("..")

    def loadingBar(self, meth, maxLen=1, sel=[], tim=0.1):
        if meth==1: 
            cmds.progressBar(self.pb1, e=1, vis=0)
            cmds.progressBar(self.pb2, e=1, vis=1, max=maxLen, pr=0) 
        elif meth==2: 
            cmds.progressBar(self.pb2, e=1, s=1)
        elif meth==3:   
            time.sleep(tim)
            if sel:                 
                cmds.select(sel)            
            cmds.progressBar(self.pb2, e=1, vis=0, pr=0)
            cmds.progressBar(self.pb1, e=1, vis=1)   
            print("")

