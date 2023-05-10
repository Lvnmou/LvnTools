def allLogs(*Args):
    texts="""
v1.05   =   10-05-2023
v1.04   =   24-09-2019
v1.03   =   27-06-2018
v1.02   =   23-05-2018 
v1.01   =   14-05-2018


    
    v1.05
    ----------   
        1) NEW
        ==============
            1. Joint
            2. Constraint's <Edit> tab
            3. Skin Weight's <Vertex Weight>, <Cleanup>
            4. Maya Settings

        2) REMOVE

        3) MOVED
        ================
            1. Group Maker's <Fix Joint>     > Snapper  
            1. Unhider (old name "unlocker") > Attributes
            2. Skin Weight's <Extra> tab     > Joint
            3. Reorient                      > Joint (*new)
            4. Load Plugins (all)            > Maya Settings


        4) ADD FUNCTION
        ================
            All except
                1. Constraint
                2. all set Driven
                    - Convert Key To Set Driven
                    - Copy Mirror Set Driven
                    - Detach Attach Set Driven
                3. Bind Pre Matrix
                4. Ctrl Setup


        5) FIX
        ============
            1. Group Maker
            -------------------------
                - (Fix) Can group a chain objects with random order
                - Remove "numeric / alphabetical" (only numeric) 


            2. Connect Attribute
            -------------------------
                - (Fix) Workable even if <replace> is empty 
                - (Fix) Create warning if selected back source / target
                - Negate using inverseMatrix

            3. Renamer
            -------------------------
                <Prefix/Suffix>
                    - (Fix) <Remove letter> will have warning when cannot delete anymore
                    - (Fix) If after search replace is no name, give warning, eg. search Cube1 replace " "
                <Batch>    
                    - increase padding's max to 100
                    - Remove alphabet padding

                    - (Fix) Can rename in a chain objects with random order
                    - (Fix) If after rename is left with numeric, or some issue, will have warning
                    
                    - Changed some cmds.ls(sl=1,l=1) without the long name. coz will have long name in printing

            4. Snapper
            -------------------------
                <Create>
                    - (Fix) <Parent "same">, create twice on same object won't have sameName issue anymore

                <Aligner>
                    - (Fix) now use xform, even if object have translate, rotate, scale, it works

            5. Cleaner
            -------------------------
                <Select>
                    - (Fix) <No Shader Objects> update to detect better. Previously if i delete shader, it wont get detect because there's still something connected to the <shading engine>. now check deeper to see the <shading engine> got connection at <surface shader> bo
                    - (Fix) <Same Name> if scene object have namespace, then will not run  
                <Fix>
                    - (Fix) <Transform Override> will pop out dialog if there is transform without no shape. then if continue will fix for it too, needa fix, if its ctrl fix and transfer enabled, display, color to shape. If transform, just disabled
                <Hide/Show>
                    - (Fix) <Hide/show history> revamp
                    - (Fix) <Show object all History> sometimes if the object itself got prob using input/output window. will show warning saying this object got prob

            6. Skin Weight
            -------------------------
                <Skinning>
                    - (Fix) workable with 1 joint even using paint type <joint Chain>
                <Influence>
                    - (Fix) <Add search replace influence> only print newly added joint that doesn't exist inside the skin cluster
                    - (Fix) <Remove influence> still selecting whatever is selected
                    - (Fix) <Add/remove Influence> if have better warning, got joint/mesh or not, added/remove new influence or not (For now cannot add mesh as influence)
                <Cleanup>
                    - (Fix) <Remove unused influence> exit paint mode

            7. Paint Middle Vertex Weight
            -------------------------
                - (Fix) There's a button to choose all joint for <Joint>, <Unlock> 
                - (Fix) Smarter detection for <Joint>, only pop out non zero weights for the selected vertex
                - (Fix) Fix unlock not unlocking properly
                - (Fix) If the mirrored joint is not found inside the influece, will pop dialog. if continue, will still continue using "try"

            8. Attribute
            -------------------------
                - (Fix) "Vector" Works correctly for <Create>, <Updown>, <Copy/Move> (previously <Create> its not under 1 parent)
                <Edit>
                    - (Fix) <Copy>/<move> will copy state if its unkey or lock
                    - (Fix) <Search Replace> will check name
                <Limiter>
                    - (Fix) <Limiter> if already have a limit, will announce before running so we wont accidentally replace it
     
            9. Surface Maker
            -------------------------
                <Create>
                    - (Fix) <More Hull (Arc)> will remain as <More Hull (Linear)> if that 3 points are collinear (* But script editor still will print)
                <Constraint>
                    - (Fix) <Surface WorldSpace> is the same setup as Local
                    - (Fix) If Surface is under a group that have value, will pop out dialog (because will have problem)
                    - Remove surface name (redundant)

            10. Ctrl Maker
            -------------------------
                <Create>
                    - (Fix) after <Parent Ctrl Shape>, reorder so that shape node is directly below (so that press down is shape node first)
                    - (Fix) If target have rotation, new create will also have
                    - (Fix) If its joint created by "Snapper", will smart replace rename "_jnt" to "_ctrl" (instead of adding suffix "_jnt_ctrl")
                    - (Fix) <Parent Ctrl Shape> + <Replace Existing shape> now work with multiple source ctrl
                    - (Fix) All <Inbetween> work for locator as a target (will work even target doesnt have nurbs shape node)

            11. Bind Pre Matrix
            -------------------------
                - (Fix) <Setup> Have warning if one of them doesn't have skin
                - (Fix) <Setup>, <Break> workable with multiple target 
                - Search replace will have dialogue if got issue
                - If <using parentInverseMatrix> will autoDetect is there a bpmJnt first, if have, will pop out warning

            12. Ctrl Read Write
            -------------------------
                - (Change) Import/export file to json 

            13. Joint
            -------------------------
                <Edit>
                    - (Fix) <becomeChain/dupBecomeChain> workable even got samename and reverse order
                <Reorient>
                    - (Fix) <Chain> Workable even if selected joint have same name
                    - (Fix) <Chain> <smart obj up> won't be able to create multiple times anymore
                    - (Fix) <Single> workable for non-joint

            14. Blendshape
            -------------------------
                <Basic>
                    - (Fix) create blendshape always arrange below skincluster

            15. Ctrl Setup 
            -------------------------
                - (Fix) Created scale group (to scale constraint)

            16. Detach Attach Set Driven 
            -------------------------
                - (Fix) If all no parent only warning (not if one no parent)
                - (Fix) Won't have error when one of the target doesnt have parent

            17. Retrace
            -------------------------
                <Rotate>
                    - (Fix) Allow <Grab> able to grab multiple selection?

            18. Eyelid Setup
            -------------------------
                - (Fix) Fixed if the eyes is pointing sides ways (where there are no translateZ) then the eyeAimMain will be at tz=0
                - (Fix) Now even for slanted eyes, the ctrl will be build in front (Z). Then have a attr like "slanted" that make the ctrl align where the eye ball is really pointing too?  useful for quadruped
                - (Fix) EyeAim & EyeTwk's all pairblend use "quaternion" (mainly for quadruped)
                - (Fix) Change twkCtrl Corner paintweight to be smoother
                - (Fix) Eyeblink tx and rotation is independent to each other
                - (Fix) Base guide now following correctly
                - (Fix) No need "C_Character_M" to generate global_grp anymore
                - (Fix) Turned off render stat for surface (because it can be rendered)
                - (Fix) Instead of searching eyeball mesh pivot in (0,0,0), use bounding box as a guide, if its within bounding box then clear
                - (Fix) Tweak Jnt have auto restriction (tz). Can stretch cannot squash
                - (Fix) Remap revamp, so that updown will match same position not just when closing in middle (for tx,ty)
                - (Fix) Upper lower length might be different hence when closing, might have a gap. Similar to remap, when its in the middle, its using both divide by 2. but when its going up then its following upper shape, if going down following lower shape. (this is like for tz)
                - (Fix) Eyeblink tx should control all 3 tweaker in a different pace so it wont penetrate so much    

                - (Change) Use placer format instead of grabbing to textfield
                - (Change) UI revamped, cannot skip any step or redo the same step (will have a check)


            *LvnTools*
            -------------
                All
                ======   
                    - Add progress bar

                LvnUI
                ======   
                    - (Change) Help on LvnTools > About
                    - (Fix) Logs window name

                Dialog
                ====== 
                    - Add "Continue Dialog". Its similar to printing but reverse, activate when target is [ ] and wont print anything 

                Logs
                =========  
                    - Modify / cleanup a little






    v1.04
    ----------   
        1) NEW
        ==============
            1. Blendshape
            2. Constraints
            3. Convert Key To Set Driven
            4. CtrlReadWrite
            5. Ctrl Setup
            6. Detach Attach Set Driven
            7. Reorient
            8. Retrace

        2) REMOVE
        ================
            1. Scale Curve Shape
            2. General
            3. Weighted

        3) MOVED
        ================
            1. Aligner (Old Name "Ctrl Vertex Snap") > Snapper 
            2. Color Changer                         > Ctrl Maker
            3. Surface Constraint                    > Surface Maker

        3) ADD FUNCTION
        ================
            1. All except "Unlocker"


        4) FIX
        ============
            1. Connect Attribute
            -------------------------
                - Remove "Same Attribute"

            2. BindPreMatrix
            -------------------------
                - (Fix) Simplify <Break Bpm> and now it works better

            3. Attribute
            -------------------------
                - (Fix) Adding empty attribute will not proceed (which make adding any attribute in future impossible) 
        
            4. Unlocker
            -------------------------
                - Remove <Lock>
                - Remove <Select all joint> (Maya itself have)  

            5. Transfer Attribute
            -------------------------
                - (Fix) "SWITCH" are able to choose too
                - (Fix) Change <Reverse> to individual negative

            6. Renamer
            -------------------------
                - (Fix) Hierarchy error when select both parent and child
                - Remove "Underscore"

            7. Paint Middle Vertex Weight  
            -------------------------
                - (Old Name) "Mirror Paint Vertex"
                - (Fix) Can mirror multiple joint together 
                - Remove <Presets>

            8. Cleaner
            -------------------------
                - (Fix) <Multiple object> change name to <Same Name> and added rename function 
                - (Fix) If nothing to clean, will have message
                - (Fix) Optimize speed

            9. Copy Mirror Set Driven 
            -------------------------
                - (Old Name) "Copy Set Driven"
                - (Fix) <Custom> is just for custom attribute, not all attribute
                - (Fix) Won't get animated key
                - (Fix) Workable even if there is an empty SDK connected
                - Change to select TARGET instead of SOURCE

            10. Group Maker
            -------------------------
                - (Fix) Detect lock object
                - (Fix) Change rotation order according to target
                - (Fix) Will remind to freeze if target is joint
                - (Fix) Fixjoint can use "numeric"
                - Remove <Same Parent>
                - Extract <Detach>, <Attach>

            11. Snapper
            -------------------------
                - (Old Name) "Pivot Snapper"
                - (Fix) Create according to selection order
                - (Fix) Method's <Inbetween> change to <Center>
                    (*Different Function. Previously is average, now same as center pivot)
                - (Fix) Minimum amount= 0.01
                - (Fix) Optimize speed (change from create cluster to use xform boundingbox) 
                - (Fix) Subselection can be target to be snapped

             12. Ctrl Maker 
            -------------------------
                - (Old Name) "Shape Maker"
                - (Fix) Workable for freezed object
                - (Fix) All ctrlShape will rename
                - (Fix) tick "Replace Existing Shape" won't delete all children's ctrl
                - (Fix) giving error when in world
                - (Fix) Remove annoying warning when no shape is deleted
                - Remove "Aim Axis", "Flip Ctrl" for <Parent Ctrl Shape (Inbetween)>
                - more shape, better resolution

                - (Fix) Workable with flat ctrl

            13. Surface Maker 
            -------------------------
                    - (Fix) <More Hull> won't flip anymore

                    - (Fix) <Create Surface> workable even if ctrl transform is locked
                    - (Fix) <Create Surface> workable even target got children
                    - (Fix) <Create Surface> workable with negative scale object

                    - (Fix) <Constraint To Surface> better constraint, prevent flipped
                    - (Fix) <Constraint To Surface> workable with negative scale in parent group
                    - (Fix) <Constraint To Surface> if target is joint(without constraint new group), will auto zero joint orient or else double rotation
                        
            14. Copy Weight
            -------------------------
                - (Old Name = CopyPaintWeight)
                - (Fix) <Remove unused influence> also cleanup influence color (node editor)
                - (Fix) <Add Influence> now get the correct skinCluster
                - (Fix) <BindSkin> & <HeatMap> looped properly
                - (Fix) <CopyWeight> copy skinmethod as well (*eg. classic / dual quarternion)
                - (Fix) <CopyWeight> joint / mesh "Search Replace" works better and have better indication
                - (Fix) <Add influence> will still continue even one of the selected joint is already added
                - (Fix) <Copy Weight>'s mirror function is separated with joint search, more versatile
                        So <Replace Joint> & <Replace Mesh and Joint> can choose to mirror or not (extra 2 choice)
                - Most function will show paintweight after click
                - Wrote Instruction for <Create Dummy set>



            *LvnTools*
            -------------
                All
                ======   
                    - Have better instruction and to know what to select
                    - Change everything to class (solve multiple script cannot exist at the same time)
                    - Modify UI to become tabLayout
                    - More warning issue to prevent weird error
                    - Search & Replace more details warning, will test for same name & existing
                    - Loop properly
                    - Mostly support multiple target

                LvnUI
                ======   
                    - Rearrange
                        - Scripts that have sub scripts are list on menu
                        - Those stands alone are inside "Tools"
                        - Merge Menu "Help", "Reload"
                    - Will load "Matrix" and "track selection order" automatically
                    - Dockable

                Dialog
                ====== 
                    - Add "successDialog", "sameNameOrNoExistDialog"
                    - Change "continueDialog" to "PrintingDialog"     
                    - Clean up (optimize) 

                Directory 
                =========== 
                    - Add "Icon"
                    - (Merge) "UI" "& "Modules" and change to Mod
                    - Change "LvnTools" from .py to .mel (modify become drag drop installer)

                Reload
                =========  
                    - (Fix) Print once only if fail and shorten script





             
    v1.03
    ---------- 
        1) NEW
        ==============
            1. BindPreMatrix
            2. ShapeMaker

        2) REMOVE

        3) MOVED

        4) ADD FUNCTION
        ================
            1. Connect Attribute
            2. General
            3. Cleaner
            4. BindPreMatrix
            5. Copy Weight


        5) FIX
        ============
            1. Copy Weight
            --------------------           
                - (Fix) <Unused Influence> after click will update paintweight tool

            2. Surface Maker
            --------------------  
                - (Fix) Workable in Maya15

            3. Transfer Attribute
            -------------------------   
                - (Fix) Able to transfer individual value (x,y,z)

            4. Color Changer
            -------------------  
                - (Fix) Same name issue

            5. Scale Curve Shape
            -------------------------- 
                - (Fix) Able to straight subselect after use "Select Vertex"

            6. Renamer
            ---------------       
                - (Fix) Under suffix prefix, even without children, tick "Hierarchy" won't have error

            7. General
            --------------       
                - Change <Hierarcy Joint> rename to <joint child>
                - (Fix) <Joint Child> able to select same name
                 
            8. Connect Attribute
            -----------------------  
                - Remove textfield for grabbing object
                - (Fix) <Search & Replace>

            9. Pivot Snapper
            -----------------------   
                - (Fix) <Pivot> works with subselection
                - (Fix) Create "Locater/Joint" have better naming


            10. Group Maker
            -------------------  
                - (Fix) Workable same name
                - (Fix) Workable with custom pivot/freeze object
                - (Fix) Minor for "Fixjoint", "Detach", "Attach" 



            *LvnTools*
            ----------------   
                All
                ========   
                    - Add <Reload>
                    - Add text to some (describe to select what)   

                LvnUI
                =======   
                    - Add <Reload>
                    - Add <Kill All>

                Help
                ========  
                    - Make it bigger 
                 
                
                           
       


    v1.02
    ----------  
        1) NEW
        ==============
            1. SurfaceMaker
            2. SurfaceConstraint
            
        2) REMOVE

        3) MOVED

        4) ADD STUFF

        5) FIX
        ============   
            1. Scale Curve Shape
            -----------------------       
                - (Fix) <Select Vertex> become subselection mode



            *LvnTools*
            -------------    
                LvnUI
                ========
                    - Rearrange scripts according to alphabet
             
             
             
                           
           

    v1.01
    ---------- 
        1) NEW

        2) REMOVE

        3) MOVED

        4) ADD FUNCTION
        ================
            1. Copy Weight


        5) FIX
        ============  
            1. CopyWeight
            -------------------------       
                - (Fix) Revamp (add more maya skin tools and some arrangement)
                - (Fix) All become Search & Replace
                - (Fix) <CopyWeightReplaceMesh> won't replace joint name but just mesh name
                - (Fix) <copyWeightReplaceMesh> warning pop out once

            2. ScaleCurveShape
            ------------------------- 
                - (Fix) become subselection 



            *LvnTools*
            -------------   
                All
                ==============       
                    -Change (*empty) to (*Args)

                SeparatorBox
                ==============   
                    - Remove one return variable (form, because didnt need it)






    """
    return texts
