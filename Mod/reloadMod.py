import sys
import inspect

def ReloadMod(userPath, *args):
    userPath = userPath.lower()
    toDelete = []
    
    # Iterate over all the modules that are currently loaded
    for key, module in sys.modules.iteritems():
        # There's a few modules that are going to complain if you try to query them
        try:
            # Use the "inspect" library to get the moduleFilePath that the current module was loaded from
            moduleFilePath = inspect.getfile(module).lower()

            # Don't try and remove the startup script, that will break everything
            if moduleFilePath == userPath.lower():
              continue

            if moduleFilePath.startswith(userPath):
              toDelete.append(key)
        except:
            pass

    for module in toDelete:
        del (sys.modules[module])        