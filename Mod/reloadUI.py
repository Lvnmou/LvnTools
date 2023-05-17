import sys
import IndivPy
import Mod
import Logs
import imp


def reloadUI(*Args):
    #Reload all modules
    test1, test2, test3= [],[],[]
    testAll= [test1, test2, test3]
    mainRel= [IndivPy, Logs, Mod]
    subRel= ["IndivPy", "Logs", "Mod"]
    for item, stuff, test in zip(mainRel, subRel, testAll):
        for thing in dir(item):
            if "__" not in thing:
                try:   
                    sys.modules.pop("%s.%s"%(stuff,thing))
                except:
                    test=1
    if test1:        
        print("reload <IndivPy> -- Fail")
    if test2:        
        print("reload <Logs> -- Fail") 
    if test3: 
        print("reload <Mod> -- Fail")   
    #Reload mainUI            
    import Mod.LvnUI as LvnUI          
    imp.reload(LvnUI) 
    LvnUI.LvnUI()



