import maya.cmds as cmds

class SepBox(object):
    def sepBoxMain(self):
        form = cmds.formLayout(numberOfDivisions=100)
        column= cmds.frameLayout(lv=0, bv=0)
        cmds.setParent("..")
        sep0= cmds.separator(h=1.5, st="none", bgc=(0.4,0.4,0.4))
        sep1= cmds.separator(h=1, st="none", bgc=(0,0,0))
        sep2= cmds.separator(h=1, st="none", bgc=(0,0,0))
        sep3= cmds.separator(hr=0, w=1, st="none", bgc=(0,0,0))
        sep4= cmds.separator(hr=0, w=1, st="none", bgc=(0,0,0))              
        cmds.formLayout(form, e=1, 
                            af=[(sep0, "top", 3),
                                (sep1, "top", 13),
                                (sep1, "left", 5),
                                (sep1, "right", 5),
                                (sep2, "bottom", 5),
                                (sep2, "left", 5),
                                (sep2, "right", 5),
                                (sep3, "top", 13),
                                (sep3, "left", 5),
                                (sep3, "bottom", 5),
                                (sep4, "top", 13),
                                (sep4, "right", 5),
                                (sep4, "bottom", 5),
                                (column, "top", 22),
                                (column, "bottom", 5),
                                (column, "left", 8),
                                (column, "right", 8)], 
                            ap=[(sep0, "left", 0, 0),
                                (sep0, "right", 0, 100)]) 
        return column  

    def sepBoxSub(self):
        form = cmds.formLayout(numberOfDivisions=100)
        column= cmds.frameLayout(lv=0, bv=0)
        cmds.setParent("..")
        sep1= cmds.separator(h=1, st="none", bgc=(0,0,0))
        sep2= cmds.separator(h=1, st="none", bgc=(0,0,0))
        sep3= cmds.separator(hr=0, w=1, st="none", bgc=(0,0,0))
        sep4= cmds.separator(hr=0, w=1, st="none", bgc=(0,0,0))                  
        cmds.formLayout(form, e=1, 
                            af=[(sep1, "top", 10),
                                (sep1, "left", 5),
                                (sep1, "right", 5),
                                (sep2, "bottom", 5),
                                (sep2, "left", 5),
                                (sep2, "right", 5),
                                (sep3, "top", 10),
                                (sep3, "left", 5),
                                (sep3, "bottom", 5),
                                (sep4, "top", 10),
                                (sep4, "right", 5),
                                (sep4, "bottom", 5),
                                (column, "top", 18),
                                (column, "bottom", 7),
                                (column, "left", 8),
                                (column, "right", 8)]) 
        return column  
