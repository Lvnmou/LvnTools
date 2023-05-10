import maya.cmds as cmds

class HelpBox(object): 
	def helpBox1(self, name, helpTxt):
	    try:
	        cmds.deleteUI("%s"%name)
	    except:
	        pass    
	    Hb= cmds.window("%s"%name, mb=1)
	    cmds.window(Hb, t="%s"%name, e=1, s=1, h=500, w=500)
	    cmds.paneLayout(cn="single")
	    cmds.scrollField(fn="plainLabelFont", ed=0, ww=1, tx="%s"%helpTxt)
	    cmds.showWindow(Hb)   


__doc__="""
1. helpBox1()  ~ [2 arg    = name, helpTxt]
                 


    name 
    ------------
        - name of this window
        - name MUST be continuous or else got problem

    helpText
    ------------
        - whatever help text message

""" 
