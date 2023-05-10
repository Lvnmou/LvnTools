import maya.cmds as cmds
import maya.mel as mel
import Mod.uiStuff as uiStuff
import Mod.dialog as dialog
import Mod.helpBox as helpBox
import time


class MayaSetting(object):
    def __init__(self, *args):
        self.dialogClass= dialog.Dialog()
        self.uiStuffClass= uiStuff.UiStuff()
        self.helpBoxClass= helpBox.HelpBox()
        self.win()


    def win(self):   
        try: 
            cmds.deleteUI("mSet") 
        except:
            pass    
        cmds.window("mSet", mb=1)              
        cmds.window("mSet", t="Maya Setting", s=1, e=1, wh=(890,400))
        cmds.menu(l="Help")
        cmds.menuItem(l="Help on Maya Setting", c=lambda x: self.helps()) 
        cmds.menu(l="Reload")
        cmds.menuItem(l="Reload Maya Setting", c=lambda x: self.reloadSub()) 
        self.uiStuffClass.sepBoxMain()
        column1= self.uiStuffClass.sepBoxSub("Create")
        form1= cmds.formLayout(nd=100, p=column1)              
        self.cb11= cmds.checkBoxGrp(l="", l1="Poly Count", cw=(1,10), v1=1)
        self.cb12= cmds.checkBoxGrp(l="", l1="Frame Rate", cw=(1,10), v1=1)
        self.cb13= cmds.checkBoxGrp(l="", l1="View Cube", cw=(1,10), v1=1)
        self.cb14= cmds.checkBoxGrp(l="", l1="View Axis", cw=(1,10), v1=1)
        self.cb15= cmds.checkBoxGrp(l="", l1="Current Camera Name", cw=(1,10), v1=1)
        self.cb16= cmds.checkBoxGrp(l="", l1="Background Color", cw=(1,10), v1=1)  
        self.cb17= cmds.checkBoxGrp(l="", l1="Grid Color", cw=(1,10), v1=1)          
        self.cb21= cmds.checkBoxGrp(l="", l1="Undo Infinite", cw=(1,10), v1=1)
        self.cb22= cmds.checkBoxGrp(l="", l1="Auto Keyframe", cw=(1,10), v1=1)
        self.cb23= cmds.checkBoxGrp(l="", l1="Track Selection Order", cw=(1,10), v1=1)     
        self.cb24= cmds.checkBoxGrp(l="", l1="Evaluation", cw=(1,10), v1=1)
        self.cb25= cmds.checkBoxGrp(l="", l1="Key Tangent", cw=(1,10), v1=1)
        self.cb26= cmds.checkBoxGrp(l="", l1="Time Unit", cw=(1,10), v1=1) 
        self.cb27= cmds.checkBoxGrp(l="", l1="Grid Unit", cw=(1,10), v1=1, w=380)
        self.drop21= cmds.optionMenuGrp(l=" : ", cw2=(10,10))
        cmds.menuItem(l="DG")
        cmds.menuItem(l="Serial")
        cmds.menuItem(l="Parallel")            
        self.drop22= cmds.optionMenuGrp(l=" : ", cw2=(10,10))
        cmds.menuItem(l="spline")
        cmds.menuItem(l="linear")
        cmds.menuItem(l="clamped")
        cmds.menuItem(l="flat")
        cmds.menuItem(l="plateau")
        cmds.menuItem(l="auto")
        cmds.optionMenuGrp(self.drop22, e=1, sl=2)
        self.drop23= cmds.optionMenuGrp(l=" : ", cw2=(10,10))
        cmds.menuItem(l="game - 15")
        cmds.menuItem(l="film - 24")
        cmds.menuItem(l="pal - 25")
        cmds.menuItem(l="ntsc - 30")
        cmds.menuItem(l="ntscf - 60")
        cmds.optionMenuGrp(self.drop23, e=1, sl=2)
        self.drop24= cmds.optionMenuGrp(l=" : ", cw2=(10,10))
        cmds.menuItem(l="millimeter")
        cmds.menuItem(l="centimeter")
        cmds.menuItem(l="meter")
        cmds.menuItem(l="kilometer")
        cmds.optionMenuGrp(self.drop24, e=1, sl=2)
        self.cb31= cmds.checkBoxGrp(l="", l1="\"o\" = Outliner", cw=(1,10), v1=1)
        self.cb32= cmds.checkBoxGrp(l="", l1="\"n\" = Node Editor", cw=(1,10), v1=1)
        txt31= cmds.text(l="(* Maya17 Wont Work)", fn="smallObliqueLabelFont", en=0) 
        self.cb41= cmds.checkBoxGrp(l="", l1="Maya Default Function", cw=(1,10), v1=1)
        #self.cb42= cmds.checkBoxGrp(l="", l1="Custom Scripts", cw=(1,10), v1=1)
        self.cb51= cmds.checkBoxGrp(l="", l1="OBJ Export", cw=(1,10), v1=1)
        self.cb52= cmds.checkBoxGrp(l="", l1="Matrix Nodes", cw=(1,10), v1=1)
        self.cb53= cmds.checkBoxGrp(l="", l1="Quat Nodes", cw=(1,10), v1=1)
        self.cb54= cmds.checkBoxGrp(l="", l1="Unfold 3D", cw=(1,10), v1=1)
        self.cb55= cmds.checkBoxGrp(l="", l1="Modeling Toolkit", cw=(1,10), v1=1)  
        self.cb56= cmds.checkBoxGrp(l="", l1="Maya Muscle", cw=(1,10))  
        b11= cmds.button(l="HUD", c=lambda x: self.mSet1()) 
        b12= cmds.button(l="Clear HUD", c=lambda x: self.mClear1())
        b21= cmds.button(l="Preferences", c=lambda x: self.mSet2())  
        b31= cmds.button(l="HotKey", c=lambda x: self.mSet3())
        b41= cmds.button(l="Shelf", c=lambda x: self.mSet4()) 
        b42= cmds.button(l="Clear Shelf", c=lambda x: self.mClear4()) 
        b51= cmds.button(l="Plugins", c=lambda x: self.mSet5()) 
        sep0= cmds.separator(h=5, st="in")
        b0= cmds.button(l="Set All", c=lambda x: self.mSet0()) 
        sep1= cmds.separator(h=155, hr=0, st="double", bgc=(1,1,1), nbg=1)
        sep2= cmds.separator(h=155, hr=0, st="double", bgc=(1,1,1), nbg=1)
        sep3= cmds.separator(h=155, hr=0, st="double", bgc=(1,1,1), nbg=1)
        sep4= cmds.separator(h=155, hr=0, st="double", bgc=(1,1,1), nbg=1)
        cmds.formLayout(form1, e=1,
                                af=[(self.cb11, "top", 0),
                                    (self.cb12, "top", 22),
                                    (self.cb13, "top", 44),
                                    (self.cb14, "top", 66),
                                    (self.cb15, "top", 88),
                                    (self.cb16, "top", 110),
                                    (self.cb17, "top", 132),
                                    (self.cb21, "top", 0),
                                    (self.cb22, "top", 22),
                                    (self.cb23, "top", 44),
                                    (self.cb24, "top", 66),
                                    (self.cb25, "top", 88),
                                    (self.cb26, "top", 110),
                                    (self.cb27, "top", 132),
                                    (self.drop21, "top", 66),
                                    (self.drop22, "top", 88),
                                    (self.drop23, "top", 110),
                                    (self.drop24, "top", 132),
                                    (self.cb31, "top", 0),
                                    (self.cb32, "top", 22),
                                    (txt31, "top", 145),
                                    (self.cb41, "top", 0),
                                    #(self.cb42, "top", 22),
                                    (self.cb51, "top", 0),
                                    (self.cb52, "top", 22),
                                    (self.cb53, "top", 44),
                                    (self.cb54, "top", 66),
                                    (self.cb55, "top", 88),
                                    (self.cb56, "top", 110),
                                    (b11, "top", 165),
                                    (b12, "top", 191),
                                    (b21, "top", 165),
                                    (b31, "top", 165),
                                    (b41, "top", 165),
                                    (b42, "top", 191),
                                    (b51, "top", 165),
                                    (sep0, "top", 225),
                                    (b0, "top", 240)],
                                ap=[(self.cb21, "left", 0, 21),
                                    (self.cb21, "right", 0, 45),
                                    (self.cb22, "left", 0, 21),
                                    (self.cb22, "right", 0, 45),
                                    (self.cb23, "left", 0, 21),
                                    (self.cb23, "right", 0, 45),
                                    (self.cb24, "left", 0, 21),
                                    (self.cb24, "right", 0, 45),
                                    (self.cb25, "left", 0, 21),
                                    (self.cb25, "right", 0, 45),
                                    (self.cb26, "left", 0, 21),
                                    (self.cb26, "right", 0, 45),
                                    (self.cb27, "left", 0, 21),
                                    (self.cb27, "right", 0, 45),
                                    (self.drop21, "left", 95, 21),
                                    (self.drop21, "right", 0, 45),
                                    (self.drop22, "left", 95, 21),
                                    (self.drop22, "right", 0, 45),
                                    (self.drop23, "left", 95, 21),
                                    (self.drop23, "right", 0, 45),
                                    (self.drop24, "left", 95, 21),
                                    (self.drop24, "right", 0, 45),
                                    (txt31, "left", 0, 46),
                                    (txt31, "right", 0, 62),
                                    (self.cb31, "left", 0, 46),
                                    (self.cb31, "right", 0, 62),
                                    (self.cb32, "left", 0, 46),
                                    (self.cb32, "right", 0, 62),
                                    (self.cb41, "left", 0, 63),
                                    (self.cb41, "right", 0, 83),
                                    #(self.cb42, "left", 0, 63),
                                    #(self.cb42, "right", 0, 83),
                                    (self.cb51, "left", 0, 84),
                                    (self.cb51, "right", 0, 100),
                                    (self.cb52, "left", 0, 84),
                                    (self.cb52, "right", 0, 100),
                                    (self.cb53, "left", 0, 84),
                                    (self.cb53, "right", 0, 100),
                                    (self.cb54, "left", 0, 84),
                                    (self.cb54, "right", 0, 100),
                                    (self.cb55, "left", 0, 84),
                                    (self.cb55, "right", 0, 100),
                                    (self.cb56, "left", 0, 84),
                                    (self.cb56, "right", 0, 100),
                                    (sep1, "left", 0, 20),
                                    (sep1, "right", 0, 21),
                                    (sep2, "left", 0, 45),
                                    (sep2, "right", 0, 46),
                                    (sep3, "left", 0, 62),
                                    (sep3, "right", 0, 63),
                                    (sep4, "left", 0, 83),
                                    (sep4, "right", 0, 84),  
                                    (b11, "left", 0, 0),
                                    (b11, "right", 0, 20), 
                                    (b12, "left", 0, 0),
                                    (b12, "right", 0, 20),
                                    (b21, "left", 0, 21),
                                    (b21, "right", 0, 45),
                                    (b31, "left", 0, 46),
                                    (b31, "right", 0, 62),
                                    (b41, "left", 0, 63),
                                    (b41, "right", 0, 83),
                                    (b42, "left", 0, 63),
                                    (b42, "right", 0, 83),
                                    (b51, "left", 0, 84),
                                    (b51, "right", 0, 100),
                                    (sep0, "left", 0, 0),
                                    (sep0, "right", 0, 100),
                                    (b0, "left", 0, 0),
                                    (b0, "right", 0, 100)]) 
        cmds.setFocus(cmds.text(l="")) 
        cmds.showWindow("mSet")

    def polyCount(self):
        if cmds.checkBoxGrp(self.cb11, q=1, v1=1)!= cmds.headsUpDisplay("HUDPolyCountVerts", q=1, vis=1):
            cmds.TogglePolyCount()

    def frameRate(self):
        if cmds.checkBoxGrp(self.cb12, q=1, v1=1)!= cmds.headsUpDisplay("HUDFrameRate", q=1, vis=1):
            cmds.ToggleFrameRate()     
               
    def viewCube(self):
        if cmds.checkBoxGrp(self.cb13, q=1, v1=1)!= cmds.viewManip(q=1, v=1):
            cmds.ToggleViewCube()    

    def viewAxis(self):
        if cmds.checkBoxGrp(self.cb14, q=1, v1=1)!= cmds.headsUpDisplay("HUDViewAxis", q=1, vis=1):
            cmds.ToggleViewAxis() 

    def cameraNames(self):
        if cmds.checkBoxGrp(self.cb15, q=1, v1=1)!= cmds.headsUpDisplay("HUDCameraNames", q=1, vis=1):
            cmds.ToggleCameraNames()
            #This is for Maya 15 Below
            cmds.displayColor("headsUpDisplayLabels", 16, d=1)

    def bgColor(self):
        if cmds.checkBoxGrp(self.cb16, q=1, v1=1):     
            cmds.displayRGBColor("backgroundTop", 0.4, 0.5, 0.6)
            cmds.displayRGBColor("backgroundBottom", 0.02, 0.02, 0.02)
        else:
            cmds.displayRGBColor("backgroundTop", 0.535, 0.617, 0.702)
            cmds.displayRGBColor("backgroundBottom", 0.05, 0.05, 0.05)            

    def gridColor(self):
        if cmds.checkBoxGrp(self.cb17, q=1, v1=1): 
            cmds.displayColor("grid", 3, d=1)
            cmds.displayColor("gridHighlight", 3, d=1)
            cmds.displayColor("gridAxis", 1, d=1)
        else:
            cmds.displayColor("grid", 2, d=1)
            cmds.displayColor("gridHighlight", 2, d=1)
            cmds.displayColor("gridAxis", 2, d=1)            

    def mSet1(self, meth=1):
        if meth==1:
            self.uiStuffClass.loadingBar(1, 2)
            self.uiStuffClass.loadingBar(2)
        self.polyCount()
        self.frameRate()
        self.viewCube()
        self.viewAxis()
        self.cameraNames()
        self.bgColor()
        self.gridColor()
        if meth==1:        
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)

    def mClear1(self):
        if cmds.headsUpDisplay("HUDPolyCountVerts", q=1, vis=1):
            cmds.TogglePolyCount()
        if cmds.headsUpDisplay("HUDFrameRate", q=1, vis=1):
            cmds.ToggleFrameRate()     
        if cmds.viewManip(q=1, v=1):
            cmds.ToggleViewCube()    
        if cmds.headsUpDisplay("HUDViewAxis", q=1, vis=1):
            cmds.ToggleViewAxis() 
        if cmds.headsUpDisplay("HUDCameraNames", q=1, vis=1):
            cmds.ToggleCameraNames()

    def undoInfinite(self):
        undoInf= cmds.checkBoxGrp(self.cb21, q=1, v1=1)
        cmds.undoInfo(st=1, infinity=undoInf)

    def autoKeyframe(self):
        autoKey= cmds.checkBoxGrp(self.cb22, q=1, v1=1)   
        cmds.autoKeyframe(st=autoKey)

    def trackSelectionOrder(self):
        track= cmds.checkBoxGrp(self.cb23, q=1, v1=1)
        cmds.selectPref(tso=track)

    def evaluationMode(self):
        #Evaluation only work for maya16 above. Available string [off | serial | parallel]
        om1= cmds.optionMenuGrp(self.drop21, q=1, v=1)
        try: 
            if om1== "DG":
                cmds.evaluationManager(m="off")
            else:            
                cmds.evaluationManager(m="%s"%om1)
        except:
            pass

    def keyTangent(self):   
        #Available string [spline | linear | clamped | flat | plateau | auto]
        om2= cmds.optionMenuGrp(self.drop22, q=1, v=1)    
        cmds.keyTangent(g=1, itt="%s"%om2, ott="%s"%om2)

    def timeUnit(self):
        #Available string [hour | min | sec | millisec | game(15) | film(24)| pal(25)| ntsc(30)| show | palf | ntscf(60)]
        om3= cmds.optionMenuGrp(self.drop23, q=1, v=1)
        cmds.currentUnit(t="%s"%om3.split(" ")[0])

    def gridUnit(self):
        #Available string [mm/millimeter | cm/centimeter | m/meter | km/kilometer | in/inch | ft/foot | yd/yard | mi/mile]
        om4= cmds.optionMenuGrp(self.drop24, q=1, v=1)
        cmds.currentUnit(l="%s"%om4) 

    def mSet2(self, meth=1):    
        if meth==1:        
            self.uiStuffClass.loadingBar(1, 2)
            self.uiStuffClass.loadingBar(2)
        self.undoInfinite()
        self.autoKeyframe()
        self.trackSelectionOrder()
        self.evaluationMode()
        self.keyTangent()
        self.timeUnit()
        self.gridUnit()
        if meth==1:        
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)

    def hotkey1(self):
        if cmds.checkBoxGrp(self.cb31, q=1, v1=1):
            cmds.hotkey(k="o", n="OutlinerWindowNameCommand")

    def hotkey2(self):
        if cmds.checkBoxGrp(self.cb32, q=1, v1=1):
            cmds.hotkey(k="n", n="NodeEditorWindowNameCommand")

    def mSet3(self, meth=1): 
        if meth==1:        
            self.uiStuffClass.loadingBar(1, 2)
            self.uiStuffClass.loadingBar(2)   
        self.hotkey1()
        self.hotkey2()
        #Marking Menu?
        if meth==1:        
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)

    def mSet4(self, meth=1):
        if meth==1:        
            self.uiStuffClass.loadingBar(1, 2)
            self.uiStuffClass.loadingBar(2)
        mel.eval("global string $gShelfTopLevel;")
        self.currentShelf= mel.eval("tabLayout -query -selectTab $gShelfTopLevel;")
        self.mClear4()
        if cmds.checkBoxGrp(self.cb41, q=1, v1=1):
            dShelf01= cmds.shelfButton(i1="menuIconModify.png", ann="Freeze transformations options", iol="Fto", l="identityApplyItemOption", p=self.currentShelf, stp="mel", c="FreezeTransformationsOptions")
            dShelf02= cmds.shelfButton(i1="menuIconModify.png", ann="Freeze transformations", iol="FT", l="Freeze Transformations", p=self.currentShelf, stp="mel", c="FreezeTransformations")
            dShelf03= cmds.shelfButton(i1="menuIconModify.png", ann="Center pivot", iol="CP", l="Center Pivot", p=self.currentShelf, stp="mel", c="CenterPivot")
            dShelf04= cmds.shelfButton(i1="menuIconEdit.png", ann="Delete construction history", l="History", iol="Hist", p=self.currentShelf, stp="mel", c="DeleteHistory")
            dShelf05= cmds.shelfButton(i1="menuIconEdit.png", ann="Invert selection", iol="IS", l="Invert Selection", p=self.currentShelf, stp="mel", c="InvertSelection")
            dShelf06= cmds.shelfButton(i1="menuIconKeys.png", ann="Set driven key options", iol="Set.", l="Set DK", p=self.currentShelf, stp="mel", c="SetDrivenKeyOptions")
            dShelf07= cmds.shelfButton(i1="menuIconWindow.png", ann="Graph editor", iol="GE", l="Graph Editor", p=self.currentShelf, stp="mel", c="GraphEditor")
            dShelf08= cmds.shelfButton(i1="menuIconWindow.png", ann="Component editor", iol="cpEd", l="Component Editor", p=self.currentShelf, stp="mel", c="ComponentEditor")
            dShelf09= cmds.shelfButton(i1="menuIconWindow.png", ann="Connection editor", iol="CE", l="Connection Editor", p=self.currentShelf, stp="mel", c="ConnectionEditor")
            dShelf10= cmds.shelfButton(i1="menuIconWindow.png", ann="Blendshape editor", iol="Blnd", l="Blend Shape", p=self.currentShelf, stp="mel", c="BlendShapeEditor")
            dShelf11= cmds.shelfButton(i1="menuIconDisplay.png", ann="Customize the joint scale", iol="JS", l="Joint Size", p=self.currentShelf, stp="mel", c="jdsWin")
            dShelf12= cmds.shelfButton(i1="locator.png", ann="Create a locator object on the grid", iol="", l="Locator", p=self.currentShelf, stp="mel", c="CreateLocator")
            dShelf13= cmds.shelfButton(i1="kinJoint.png", ann="Create joint", iol="", l="Joint Tool", p=self.currentShelf, stp="mel", c="JointTool")
            dShelf14= cmds.shelfButton(i1="menuIconModify.png", ann="Convert polygon edges to nurbs curves options.", iol="Cpetnco", l="polyToCurveItem2", p=self.currentShelf, stp="mel", c="CreateCurveFromPolyOptions")
            dShelf15= cmds.shelfButton(i1="menuIconDisplay.png", ann="Toggle local rotation axis visibility", iol="LRA", l="Local Rotation Axes", p=self.currentShelf, stp="mel", c="ToggleLocalRotationAxes")
            dShelf16= cmds.shelfButton(i1="menuIconDisplay.png", ann="Toggle selection handle visibility", iol="SH", l="Selection Handles", p=self.currentShelf, stp="mel", c="ToggleSelectionHandles")
            dShelf17= cmds.shelfButton(i1="menuIconDisplay.png", ann="Toggle CV visibility", iol="CVs", l="CVs", p=self.currentShelf, stp="mel", c="ToggleCVs")
            dShelf18= cmds.shelfButton(i1="paintSkinWeights.png", ann="Paint Weight", iol="", l="Paint Skin Weights Tool", p=self.currentShelf, stp="mel", c="ArtPaintSkinWeightsTool")
            dShelf19= cmds.shelfButton(i1="menuIconEdit.png", ann="Select all joints", iol="join", l="Joints", p=self.currentShelf, stp="mel", c="SelectAllJoints")
            dShelf20= cmds.shelfButton(i1="menuIconEdit.png", ann="Select all IK handles", iol="ikH", l="IK Handles", p=self.currentShelf, stp="mel", c="SelectAllIKHandles")
            dShelf21= cmds.shelfButton(i1="menuIconEdit.png", ann="Select all clusters", iol="clus", l="Clusters", p=self.currentShelf, stp="mel", c="SelectAllClusters")
            self.allDefShelf=[dShelf01,dShelf02,dShelf03,dShelf04,dShelf05,dShelf06,dShelf07,dShelf08,dShelf09,dShelf10,dShelf11,dShelf12,dShelf13,dShelf14,dShelf15,dShelf16,dShelf17,dShelf18,dShelf19,dShelf20,dShelf21]
        #if cmds.checkBoxGrp(self.cb42, q=1, v1=1):
            cusScript1=""" 
// parentToSurface (Follicle)
// This mel command allows one to attach selected objects to a selected mesh or nurbs surface.
// The objects will follow any deformation or transformation of the surface.
// Usage: put this script in your local scripts directory. In Maya select object(s) to attach
//        followed by a mesh or nurbs surface to attach then enter "parentToSurface" in the
//        command line. A follicle node will be created at the point on surface closest to
//        the center of the object and the object will be parented to this follicle. Note that
//      if the surface to attach to is a mesh it must have well defined UVs that range from 0-1
//      with no areas sharing the same value.
//
//        For convenience drag the parentToSurface string onto the shelf to make a shelf button.
// 
// This command uses the follicle node, which is normally used by the hair system. The follicle node
// is currently the only node in maya that can derive a rotate and translate based on a uv position
// for both meshes and nurbs surfaces.
//
// One use of this script might be to attach buttons to a cloth object, or any deforming surface. To
// attach several buttons, first position the buttons where desired then select them followed by the
// object to attach to and run this command.
// For more info or to report problems with this script go to Duncan's Corner:
// http://area.autodesk.com/blogs/blog/7/

proc float convertToCmFactor()
{
    string $unit = `currentUnit -q -linear`;
    if( $unit == "mm" ){
        return( 0.1 );
    } else if( $unit == "cm" ){
        return( 1.0 );
    } else if( $unit == "m" ){
        return( 100.0 );
    } else if( $unit == "in" ){
        return( 2.54 );
    } else if( $unit == "ft" ){
        return( 30.48 );
    } else if( $unit == "yd" ){
        return( 91.44 );
    } else {
        return( 1.0 );
    }
}

proc attachObjectToSurface(string $obj, string $surface, float $u, float $v )
{
    string $follicle = `createNode follicle`;
    string $tforms[] = `listTransforms $follicle`;
    string $follicleDag = $tforms[0];

    
    connectAttr ($surface + ".worldMatrix[0]") ($follicle + ".inputWorldMatrix");
    string $nType = `nodeType $surface`;
    if( "nurbsSurface" == $nType ){ 
        connectAttr ($surface + ".local") ($follicle + ".inputSurface");
    } else {
        connectAttr ($surface + ".outMesh") ($follicle + ".inputMesh");
    }
    connectAttr ($follicle + ".outTranslate") ($follicleDag + ".translate");
    connectAttr ($follicle + ".outRotate") ($follicleDag + ".rotate");
    setAttr -lock true  ($follicleDag + ".translate");
    setAttr -lock true  ($follicleDag + ".rotate");
    setAttr ($follicle + ".parameterU") $u;
    setAttr ($follicle + ".parameterV") $v;
    
    //parent -addObject -shape $obj $follicleDag;
    parent $obj $follicleDag;
}

global proc parentToSurface()
{
    string $sl[] = `ls -sl`;
    int $numSel =size($sl);
    if( $numSel < 2 ){
        warning( "ParentToSurface: select object(s) to parent followed by a mesh or nurbsSurface to attach to.");
        return;
    }
    string $surface = $sl[$numSel-1];
    if( nodeType($surface) == "transform" ){
        string $shapes[] = `ls -dag -s -ni -v $surface`;
        if( size( $shapes ) > 0 ){
            $surface = $shapes[0];
        } 
    }
    string $nType = `nodeType $surface`;
    if( $nType != "mesh" && $nType != "nurbsSurface"){
        warning( "ParentToSurface: Last selected item must be a mesh or nurbsSurface.");
        return;
    }
    string $clPos = "";
    float $minU, $minV, $sizeU, $sizeV;
    float $convertFac = 1.0;

    if( $nType == "nurbsSurface" ){
        $clPos = `createNode closestPointOnSurface`;    
        connectAttr ($surface + ".worldSpace[0]") ($clPos + ".inputSurface");

        $minU = `getAttr ($surface+".mnu")`;
        float $maxU = `getAttr ($surface+".mxu")`;
        $sizeU = $maxU - $minU;
        $minV = `getAttr ($surface+".mnv")`;
        float $maxV = `getAttr ($surface+".mxv")`;
        $sizeV = $maxV - $minV;
    } else {
        int $pomLoaded = `pluginInfo -query -l nearestPointOnMesh`;
        if( !$pomLoaded ){
            loadPlugin nearestPointOnMesh;
            $pomLoaded = `pluginInfo -query -l nearestPointOnMesh`;
            if( !$pomLoaded ){
                warning( "ParentToSurface: Can't load nearestPointOnMesh plugin.");
                    return;
            }
        }
        // The following is to overcome a units bug in the nearestPointOnMesh plugin
        // If at some point it correctly handles units, then we need to take out the
        // following conversion factor. 
        $convertFac = convertToCmFactor();

        $clPos = `createNode nearestPointOnMesh`;
        connectAttr ($surface + ".worldMesh") ($clPos + ".inMesh");
    }
    
    int $i;
    float $closestU, $closestV;
    for( $i = 0; $i < $numSel -1; $i++ ){
        string $obj = $sl[$i];
        if( nodeType( $obj )!= "transform" ){
            warning( "ParentToSurface: select the transform of the node(s) to constrain");
            continue;
        }
        float $bbox[] = `xform -q -ws -bb $obj`;
        float $pos[3];
        $pos[0] = ($bbox[0] + $bbox[3])*0.5;
        $pos[1] = ($bbox[1] + $bbox[4])*0.5;
        $pos[2] = ($bbox[2] + $bbox[5])*0.5;
        setAttr ($clPos + ".inPosition") -type double3 
            ($pos[0]*$convertFac) 
            ($pos[1]*$convertFac)
            ($pos[2]*$convertFac);
        $closestU = getAttr( $clPos + ".parameterU");
        $closestV = getAttr( $clPos + ".parameterV");
        if( $nType == "nurbsSurface" ){
            $closestU = ($closestU + $minU)/$sizeU;
            $closestV = ($closestV + $minV)/$sizeV;
        }

        attachObjectToSurface( $obj, $surface, $closestU, $closestV );
    }

    if( $clPos != "" ){
        delete $clPos;
    }
}

parentToSurface()
"""
            cusScript2=""" 
#Object does not exist" meaning target/source got same name
#ikParameter error = sameName
#influence not found = shapeNode sameName
#after skin object fly = surface not freezed

# Copy Weight from surface

import maya.cmds as cmds
# import pymel.core as pm 
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim

#TODO: Selected verts
#TODO: Duplicate copy srf - Skinpercent
#TODO: Nearest joint
def copyWeights_nurbsToPoly():
    polyMesh= cmds.ls(sl=1)[1]
    nurbsSurface= cmds.ls(sl=1)[0]
    # setupWeights(srcMesh=polyMesh,desSurface=nurbsSurface)
    createTempSetup(src=nurbsSurface,des=polyMesh)

def getDagPath(node):
    selList = om.MSelectionList()
    selList.add(node)
    nodeDagPath = om.MDagPath()
    selList.getDagPath(0,nodeDagPath)
    return nodeDagPath

def getMObject(node):
    selList = om.MSelectionList()
    selList.add(node)
    nodeMObject = om.MObject()
    selList.getDependNode(0,nodeMObject)
    return nodeMObject

# def getMObject(node):
#     nodeDagPath = getDagPath(node)
#     nodeMObject = nodeDagPath.node()
#     return nodeMObject

# def calcDistance(sObj,eObj):
#     # Get the worldspace translates of both objects 
#     sPnt = cmds.xform(sObj,q=1,rp=1,ws=1)
#     ePnt = cmds.xform(eObj,q=1,rp=1,ws=1)
#     # Calculate the distance between them
#     distance = math.sqrt((ePnt[0]-sPnt[0])**2 + (ePnt[1]-sPnt[1])**2 + (ePnt[2]-sPnt[2])**2)
#     return round(distance,3)

# def getSkinCluster(node):
#   return [s for s in cmds.listHistory(node) if cmds.nodeType(s) == 'skinCluster']

def getSkinCluster(node):
    shape = cmds.listRelatives(node, s=1, ni=1)
    nodeMObj = getMObject(shape[0])
    dagIterator = om.MItDependencyGraph(nodeMObj,om.MFn.kSkinClusterFilter,om.MItDependencyGraph.kUpstream)
    while not dagIterator.isDone():
        skinCluster = omAnim.MFnSkinCluster(dagIterator.currentItem())
        dagIterator.next()
    return skinCluster

def createTempSetup(src='',des=''):
    origSkinCls = getSkinCluster(src)
    origInfObjDagArray = om.MDagPathArray()
    origSkinCls.influenceObjects(origInfObjDagArray)
    origInfs = [origInfObjDagArray[inf].partialPathName() for inf in range(origInfObjDagArray.length())]
    origSrfDagP = getDagPath(src)
    
    #Bind mesh to Nurbs influences
    cmds.skinCluster(des, origInfs,tsb=1)
    meshSkinCls = getSkinCluster(des)

    #Duplicate nurbs setup
    dupedSetupWidget = []
    dupedSetupWidget.append(cmds.duplicate(src)[0])
    createDupeInfs(dupedSetupWidget, origInfs)
    # Skin duplicate surface
    cmds.skinCluster(dupedSetupWidget[1:], dupedSetupWidget[0],tsb=1)

    dupedSkinCls = getSkinCluster(dupedSetupWidget[0])
    dupedInfObjDagArray = om.MDagPathArray()
    dupedSkinCls.influenceObjects(dupedInfObjDagArray)
    dupedInfs = [dupedInfObjDagArray[inf].partialPathName() for inf in range(dupedInfObjDagArray.length())]

    cpyWtsOrigSrfToDupedSrf(getDagPath(cmds.listRelatives(src,s=1)[0]),
                            origSkinCls,
                            dupedSkinCls,
                            origInfs,
                            dupedInfs,
                            src,
                            dupedSetupWidget[0])
    
    # origSrfWts = getWeights(getDagPath(cmds.listRelatives(src,s=1)[0]),
    #                         origSkinCls,
    #                         origInfs,
    #                         src)
    # print origSrfWts

    setupWeights(src=dupedSetupWidget[0],des=des,tempInfs=dupedInfs,origInfs=origInfs,desMeshSknCls=meshSkinCls)
    cmds.delete(dupedSetupWidget)

# def getWeights(shapeDag,mfnSkinCls,origInfluences,origSrfXform):
#     numComps = 0
#     if shapeDag.node().hasFn(om.MFn.kMesh):
#         # meshIt = om.MItMeshVertex(shapeDag)
#         # numComps = meshIt.count()
#         numComps = len(cmds.ls("{0}.vtx[*]".format(origSrfXform),fl=1))
#         components = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
#     elif shapeDag.node().hasFn(om.MFn.kNurbsSurface):
#         # nurbsIt = om.MItSurfaceCV(shapeDag)
#         numComps = len(cmds.ls("{0}.cv[*][*]".format(origSrfXform),fl=1))
#         components = om.MFnDoubleIndexedComponent().create(om.MFn.kSurfaceCVComponent)
#     apiCVS = om.MIntArray(numComps,0)
#     [apiCVS.set(i,i) for i in range(numComps)]
#     om.MFnDoubleIndexedComponent(components).addElements(apiCVS)
#     numInfluencesUtil = om.MScriptUtil()
#     numInfluencesUtil.createFromInt(0) 
#     wts = om.MDoubleArray(0)
#     mfnSkinCls.getWeights(shapeDag,components,wts,numInfluencesUtil.asUintPtr())
#     return wts

def cpyWtsOrigSrfToDupedSrf(shapeDag,origMfnSkinCls,dupedMfnSkinCls,origInfluences,dupedInfluences,origSrfXform,dupedSrfXform):
    numComps = cmds.ls("{0}.cv[*][*]".format(origSrfXform),fl=1)
    for comp in numComps:
        for origInf,dupedInf in zip(origInfluences,dupedInfluences):
            val = cmds.skinPercent( origMfnSkinCls.name(), comp, q=1,t=origInf )
            cmds.skinPercent(dupedMfnSkinCls.name(), comp.replace(origSrfXform,dupedSrfXform), tv=[dupedInf,val])

def createDupeInfs(dupedSetupWidget, origInfs):
    for inf in origInfs:
        cmds.select(cl=1)
        tempJnt = cmds.joint(n="{0}_TEMP".format(inf))
        origTra, origRot = getXforms(inf)
        cmds.xform(tempJnt, t=[origTra[0], origTra[1], origTra[2]])
        dupedSetupWidget.append(tempJnt)

def getXforms(node):
    translation = cmds.xform(node,q=1,ws=1,t=1)
    rotation = cmds.xform(node,q=1,ro=1)
    return translation,rotation

def getNewParamPos(desSrf, origPos, paramU, paramV):
    newPos = om.MPoint()
    desSrf.getPointAtParam(paramU, paramV, newPos, om.MSpace.kWorld)
    distance = newPos.distanceTo(origPos)
    return distance

def setupWeights(src='',des='',tempInfs='',origInfs='',desMeshSknCls=''):
    srcDagPath = getDagPath(src)
    desDagPath = getDagPath(des)

    desMeshVerts = om.MItMeshVertex(desDagPath)
    desSrf = om.MFnNurbsSurface(srcDagPath)
    while not desMeshVerts.isDone():
        srcVertPnt = desMeshVerts.position(om.MSpace.kWorld)
        srcVertInd = desMeshVerts.index()

        paramUUtil, paramVUtil = om.MScriptUtil(), om.MScriptUtil()
        paramUPtr, paramVPtr = paramUUtil.asDoublePtr(), paramVUtil.asDoublePtr()
        
        origPos = desSrf.closestPoint(srcVertPnt,paramUPtr,paramVPtr,om.MSpace.kWorld)
        paramU, paramV = paramUUtil.getDouble(paramUPtr), paramVUtil.getDouble(paramVPtr)
        wtsDict = {}
        for tempInf,origInf in zip(tempInfs,origInfs):
            moveInfluence(tempInf)
            distance = getNewParamPos(desSrf, origPos, paramU, paramV)
            moveInfluence(tempInf,origPos=1)
            wtsDict[origInf] = distance

        cmds.skinPercent(desMeshSknCls.name(),'{0}.vtx[{1}]'.format(des,srcVertInd), tv=[[k,v] for k,v in wtsDict.iteritems()])
        desMeshVerts.next() #Iterate vert

def moveInfluence(inf='',origPos = None):
    if origPos:
        moveAmount = -1
    else:
        moveAmount = 1
    val = cmds.getAttr('{0}.ty'.format(inf)) + moveAmount
    cmds.setAttr('{0}.ty'.format(inf),val)


obj= cmds.ls(sl=1)
for item in cmds.ls(sl=1)[1:]:
    cmds.select(obj[0])
    cmds.select(item, add=1)
    copyWeights_nurbsToPoly()

"""   
            cusScript3=""" 
# Duplicate object while unlock all attribute
import maya.cmds as cmds

obj= cmds.ls(sl=1)
allDup=[]
if obj:
    for item in obj:
        dup= cmds.duplicate(item)
        attr="x","y","z"
        for stuff in attr:
            cmds.setAttr("%s.t%s"%(dup[0],stuff), k=1, l=0)
            cmds.setAttr("%s.r%s"%(dup[0],stuff), k=1, l=0)
            cmds.setAttr("%s.s%s"%(dup[0],stuff), k=1, l=0)
        allDup.append(dup[0])
    cmds.select(allDup)
else:
    cmds.warning("Please select at least 1 OBJECT")
"""   
            cusScript4=""" 
# Open new ports
import maya.cmds as cmds

cmds.commandPort(name=":7001", sourceType="mel")
cmds.commandPort(name=":7002", sourceType="python")
"""   
            cusScript5=""" 
# Close ports if they were already open under another configuration
import maya.cmds as cmds

try:
    cmds.commandPort(name=":7001", close=True)
except:
    cmds.warning('Could not close port 7001 (maybe it is not opened yet...)')

try:
    cmds.commandPort(name=":7002", close=True)
except:
    cmds.warning('Could not close port 7002 (maybe it is not opened yet...)')
"""         
            #cShelf01= cmds.shelfButton(i1="commandButton.png", ann="follicle", iol="fol", l="follicle", p=self.currentShelf, stp="mel", c=cusScript1)
            #cShelf02= cmds.shelfButton(i1="pythonFamily.png", ann="copyweight from surface", iol="srf", l="surface", p=self.currentShelf, stp="python", c=cusScript2)
            #cShelf03= cmds.shelfButton(i1="pythonFamily.png", ann="duplicate", iol="dupUn", l="duplicate", p=self.currentShelf, stp="python", c=cusScript3)
            #cShelf04= cmds.shelfButton(i1="pythonFamily.png", ann="load sublime port", iol="load", l="load", p=self.currentShelf, stp="python", c=cusScript4)
            #cShelf05= cmds.shelfButton(i1="pythonFamily.png", ann="unload sublime port", iol="unload", l="unload", p=self.currentShelf, stp="python", c=cusScript5)
            #self.allCusShelf=[cShelf01,cShelf02,cShelf03,cShelf04,cShelf05]
        if meth==1:        
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)

    def mClear4(self):
        try:
            for item in self.allDefShelf:
                try:
                    cmds.deleteUI(item, ctl=1)
                except:
                    pass
        except:
            pass
        try:
            for item in self.allCusShelf:
                try:
                    cmds.deleteUI(item, ctl=1)
                except:
                    pass
        except:
            pass

    def mSet5(self, meth=1):
        if meth==1:
            self.uiStuffClass.loadingBar(1, 2)
            self.uiStuffClass.loadingBar(2)
        allPlugins= []
        if cmds.checkBoxGrp(self.cb51, q=1, v1=1):
            allPlugins.append("objExport")      
        if cmds.checkBoxGrp(self.cb52, q=1, v1=1):
            allPlugins.append("matrixNodes") 
        if cmds.checkBoxGrp(self.cb53, q=1, v1=1):
            allPlugins.append("quatNodes") 
        if cmds.checkBoxGrp(self.cb54, q=1, v1=1):
            allPlugins.append("Unfold3D") 
        if cmds.checkBoxGrp(self.cb55, q=1, v1=1):
            allPlugins.append("modelingToolkit") 
        if cmds.checkBoxGrp(self.cb56, q=1, v1=1):
            allPlugins.append("MayaMuscle") 
        if allPlugins:
            ver= cmds.about(v=1)
            for nodes in allPlugins:
                if nodes not in cmds.pluginInfo(q=1, ls=1):
                    try:
                        cmds.loadPlugin("C:/Program Files/Autodesk/Maya%s/bin/plug-ins/%s.mll"%(ver,nodes))
                    except:
                        cmds.warning("<%s> plugin missing from <C:/Program Files/Autodesk/Maya%s/bin/plug-ins/%s.mll>"%(nodes, ver,nodes))
        if meth==1:
            self.uiStuffClass.loadingBar(2)
            self.uiStuffClass.loadingBar(3)

    def mSet0(self):
        self.uiStuffClass.loadingBar(1, 2)  
        self.uiStuffClass.loadingBar(2)
        self.mSet1(0)
        self.mSet2(0)
        self.mSet3(0)
        self.mSet4(0)
        self.mSet5(0)
        self.uiStuffClass.loadingBar(2)
        self.uiStuffClass.loadingBar(3)

    def helps(self):
        name="Help On MayaSetting"
        helpTxt="""
        - Set Starter Pack Maya Setting 



        A) HUD
        =======
            - Poly Count
            - Frame Rate
            - View Cube (doesn't show on viewport 2.0)
            - View Axis
            - Current Camera Name
            - Background Color
            - Grid Color

        B) Preferences
        =============== 
            - Undo Infinite
            - Auto Keyframe
            - Track Selection Order
            - Evaluation
            - Key Tangent
            - Time Unit
            - Grid Unit     


        C) HotKey
        ===========
            - "o" = Outliner
            - "n" = Node Editor   

            (* For now doesnt work for Maya17. Needa manually create it first because Maya17 have a folder for hotkey)


        D) Shelf
        =========
            1. Maya Default Function
                - Freeze Option
                - Freeze
                - Center Pivot
                - Delete History
                - Invert Selection
                - Set Driven Key
                - Graph Editor
                - Component Editor
                - Connection Editor
                - Blendshape Editor
                - Joint Size
                - Create Locator
                - Create Joint
                - View Local Rotation Axis
                - View Selection Handle
                - View CVs
                - Paint Weight Tool
                - Select All Joints
                - Select All Ik Handle
                - Select All Cluster
                - Convert Polygon Edge To Nurbs Curves

            2. Custom Script     
                - Follicle
                - Surface Copy weight
                - Duplicate Unlock
                - Load Sublime
                - Unload Sublime 

            (* Created shelf cannot undo... so needa delete using <Clear Shelf>)
            (* For now its not detecting what already exist but create a new one)

        E) Plugins
        ============   
            - OBJ Export
            - Matrix Nodes
            - Quat Nodes
            - Unfold 3D
            - Modeling Toolkit
            - Maya Muscle

        """ 
        self.helpBoxClass.helpBox1(name, helpTxt)


    def reloadSub(self):
        MayaSetting()  
    
                          
if __name__=='__main__':
    MayaSetting()



