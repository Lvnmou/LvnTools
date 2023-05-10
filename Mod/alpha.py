import maya.cmds as cmds
import string

class Alpha(object):
    def __init__(self, *args):
        self.win()

    def win(self):
        alpha= string.letters[:26].upper()
        z, alpha1, alpha2, alpha3=["0"],[],[],[]
        for item in alpha:
            alpha1.append(item)     
        for item in alpha:
            for thing in alpha:
                alpha2.append(item+thing)           
        for item in alpha:
            for thing in alpha2:
                alpha3.append(item+thing)    
        self.alpha1= z + alpha1 + alpha2 + alpha3
        self.alpha2= z + alpha2 + alpha3
        self.alpha3= z + alpha3

