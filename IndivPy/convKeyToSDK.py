import maya.cmds as cmds
import Mod.sepBox as sepBox
import Mod.helpBox as helpBox


class ConvKeyToSDK(object):
    def __init__(self, *args):
        self.sepBoxClass= sepBox.SepBox()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()

    def win(self): 
        try: 
            cmds.deleteUI("cktSDK") 
        except:
            pass    
        cmds.window("cktSDK", mb=1)              
        cmds.window("cktSDK", t="Convert Key To Set Driven", s=1, e=1, wh=(300,100))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on ConvertKeyToSetDriven", c=lambda x:self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload ConvertKeyToSetDriven", c=lambda x:self.reloadSub())  
        column1= self.sepBoxClass.sepBoxMain()    
        form1= cmds.formLayout(nd=100, p=column1) 
        self.txtDriven= cmds.textFieldButtonGrp(l="Driven Targets :", cw3=(90,100,100), adj=2, bl="  Grab  ", bc=lambda :self.grab2())
        self.txtDrAttr= cmds.textFieldButtonGrp(l="Driver Attribute :", cw3=(90,100,100), adj=2, bl="  Grab  ", bc=lambda :self.grab1())
        self.txtMin= cmds.floatFieldGrp(l="Driver Min Value :",cw2=(90,70), adj=2)
        self.txtMax= cmds.floatFieldGrp(l="Max Value :", cw2=(80,70), adj=2)
        txt1= cmds.text(l="*Currently only can convert to linear graph", fn="smallObliqueLabelFont", en=0)
        b1= cmds.button(l="Convert", c=lambda x:self.final()) 
        cmds.formLayout(form1, e=1,
                                af=[(self.txtDriven, "top", 0),
                                    (self.txtDrAttr, "top", 26),
                                    (self.txtMin, "top", 52),
                                    (self.txtMax, "top", 52),
                                    (txt1, "top", 88),
                                    (b1, "top", 103)],
                                ap=[(self.txtDriven, "left", 0, 0),
                                    (self.txtDriven, "right", 0, 100),
                                    (self.txtDrAttr, "left", 0, 0),
                                    (self.txtDrAttr, "right", 0, 100),
                                    (self.txtMin, "left", 0, 0),
                                    (self.txtMin, "right", 0, 50),
                                    (self.txtMax, "left", 0, 51),
                                    (self.txtMax, "right", 0, 100),
                                    (txt1, "left", 0, 0),
                                    (txt1, "right", 0, 100),
                                    (b1, "left", 0, 0),
                                    (b1, "right", 0, 100)])
        cmds.setFocus(cmds.text(l=""))  
        cmds.showWindow("cktSDK")

    def defi(self):
        self.obj= cmds.ls(sl=1)
        self.sour= cmds.textFieldButtonGrp(self.txtDrAttr, q=1,tx=1)
        self.drMin= cmds.floatFieldGrp(self.txtMin, q=1,v=1)
        self.drMax= cmds.floatFieldGrp(self.txtMax, q=1,v=1)
        self.tar= cmds.textFieldButtonGrp(self.txtDriven, q=1,tx=1)   

    def grab1(self):
        self.defi() 
        attr= cmds.channelBox("mainChannelBox", sma=1,q=1)      
        if attr:                                   
            cmds.textFieldButtonGrp(self.txtDrAttr, e=1, tx="%s.%s"%(self.obj[0], attr[0]))                           
        else:
            cmds.warning("Select 1 attribute")     
                                   
    def grab2(self):  
        self.defi()           
        if self.obj:                                
            cmds.textFieldButtonGrp(self.txtDriven, e=1, tx="%s"%", ".join(self.obj))                                       
        else:
            cmds.warning("Select at least 1 driven object")                        

    def final(self):                      
        self.defi() 
        animC1= ["animCurveTL", "animCurveTA", "animCurveTU", "animCurveTT"]
        animC2= ["animCurveUL", "animCurveUA", "animCurveUU", "animCurveUT"] 
        test1, test2= 1,1
        for item in self.tar.split(", "):
            if item==self.sour.split(".")[0]:
                test1=[] 
            ac1= cmds.listConnections(item, d=0, t="animCurveTL") 
            ac2= cmds.listConnections(item, d=0, t="animCurveTA") 
            ac3= cmds.listConnections(item, d=0, t="animCurveTU") 
            ac4= cmds.listConnections(item, d=0, t="animCurveTT") 
            if ac1==None and ac2==None and ac3==None and ac4==None:
                test2=[]     
        if test1:
            if test2:
                for item in self.tar.split(", "):
                    for stuff, thing in zip(animC1, animC2):       
                        oriCurv= cmds.listConnections(item, d=0, t="%s"%stuff)   
                        if oriCurv:    
                            for cur in oriCurv: 
                                #try:     
                                """      
                                ix=cmds.keyTangent(cur, q=1, ix=1)
                                iy=cmds.keyTangent(cur, q=1, iy=1)
                                ox=cmds.keyTangent(cur, q=1, ox=1)
                                oy=cmds.keyTangent(cur, q=1, oy=1)
                                #Because change to all linear, so temporary doesnt need this
                                ia=cmds.keyTangent(cur, q=1, ia=1)
                                iw=cmds.keyTangent(cur, q=1, iw=1)
                                oa=cmds.keyTangent(cur, q=1, oa=1)
                                ow=cmds.keyTangent(cur, q=1, ow=1)
                                """
                                timeC= cmds.keyframe(cur,q=1, tc=1)
                                valueC= cmds.keyframe(cur,q=1, vc=1)
                                tempTime=[]
                                dis= cmds.listConnections("%s.output"%cur, c=1, p=1)
                                cmds.delete(cur)           
                                #rematch duration  
                                tMul= (self.drMax[0]-self.drMin[0])/((max(timeC))-(min(timeC)))
                                for stuff in timeC: 
                                    if self.drMax[0]>self.drMin[0]:  
                                        tempTime.append((stuff-min(timeC))*tMul+self.drMin[0])
                                    else:
                                        tempTime.append(self.drMax[0]-(stuff-min(timeC))*tMul)                                     
                                for goods in tempTime:         
                                    cmds.setAttr(self.sour, goods)
                                    cmds.setDrivenKeyframe("%s.%s"%(item,dis[1].split(".")[1]), cd=self.sour)
                                new= cmds.listConnections(dis[1], t="%s"%thing)
                                new2= cmds.rename(new, cur.replace("_","_SDK_"))
                                cmds.setAttr(self.sour, self.drMin[0])
                                """
                                #copying tangent
                                outTan Weight= *24      
                                outTan Angle= /23.7
                                wrong, doesnt apply to all

                                #Acacia Echo API animation curve (website)

                                """
                                if self.drMax[0]>self.drMin[0]: 
                                    for num,items in enumerate(valueC):
                                        cmds.keyframe(new2, e=1, index=(num,num), vc=items)    
                                        cmds.keyTangent(new2, e=1, l=0, a=1, index=(num,num), itt="linear", ott="linear")
                                else:
                                    for num,items in enumerate(reversed(valueC)):
                                        cmds.keyframe(new2, e=1, index=(num,num), vc=items)    
                                        cmds.keyTangent(new2, e=1, l=0, a=1, index=(num,num), itt="linear", ott="linear")                                     
                                """
                                for num,items in enumerate(zip(ia,iw,oa,ow)):
                                    cmds.keyTangent(new2, e=1, l=0, a=1, index=(num,num), ia=items[0], iw=items[1], oa=items[2], ow=items[3])    
                                for num,items in enumerate(zip(ix,iy,ox,oy)):
                                    cmds.keyTangent(new2, e=1, l=0, a=1, index=(num,num), ix=items[0], iy=items[1], ox=items[2], oy=items[3])       
                                """
                                #except:
                                    #pass
            else:
                cmds.warning("One of the target does not have KEYFRAME animation")
        else:
            cmds.warning("One of the target is same as DRIVER, cannot set driven to self")        

    def helps(self):
        name="Help On ConvertKeyToSetDriven"
        helpTxt="""
        - Take a animated object (with keyframe) and convert it to Set Driven Key
        - Set the min, max value of the attribute (it will remap the animation to it)
            (* workable as reverse as well. eg. 0~-5 instead of -5~0)

        (* Currently cannot copy the other tangent of the maps except for linear)           
        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)    
       
    def reloadSub(self):
        ConvKeyToSDK()   
        
                     
if __name__=='__main__':
    ConvKeyToSDK() 
