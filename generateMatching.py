"""
TODO- method 1: based on Men-Proposing Deferred Acceptance, develop a Device-Proposing Deferred Acceptance. See course slides

TODO- method 2: based on method 1, the order of proposing from Devices should be randomized

TODO- method 3..: other possible matching algorithm

"""
import random

# TODO- method 1
def mpda(edgesPref, devsPref):
    deviceDict = devsPref.copy()
    edgeDict = edgesPref.copy()
    matchingGraph = []
    n = len(deviceDict)
    

    # Initially, all n men are unmarried
    unmarriedMen = list(devsPref)
    # None of the men has a spouse yet, we denote this by the value None
    manSpouse = []                     
    # None of the women has a spouse yet, we denote this by the value None
    womanSpouse = [None] * n                      
    # Each man made 0 proposals, which means that 
    # his next proposal will be to the woman number 0 in his list
    nextManChoice = [0] * n                       
    
    # While there exists at least one unmarried man:
    while unmarriedMen:
        # Pick an arbitrary unmarried man
        his_name = unmarriedMen[0]
        he = unmarriedMen.index(his_name)
        # Store his ranking in this variable for convenience
        hisPreferences = list(deviceDict.values())[he]
        # Find a woman to propose to
        her_name = hisPreferences[nextManChoice[he]]
        she = hisPreferences.index(her_name)
        # Store her ranking in this variable for convenience
        herPreferences = list(edgeDict.values())[she]
        # Find the present husband of the selected woman (it might be None)
        currentHusband = womanSpouse[she]
       
        
        # Now "he" proposes to "she". 
        # Decide whether "she" accepts, and update the following fields
        # 1. manSpouse
        # 2. womanSpouse
        # 3. unmarriedMen
        # 4. nextManChoice
        if currentHusband == None:
          #No Husband case
          #"She" accepts any proposal
          womanSpouse[she] = his_name
          manSpouse.append((his_name, her_name))
          #"His" nextchoice is the next woman
          #in the hisPreferences list
          nextManChoice[he] = nextManChoice[he] + 1
          #Delete "him" from the 
          #Unmarried list
          unmarriedMen.pop(0)
        else:
          #Husband exists
          #Check the preferences of the 
          #current husband and that of the proposed man's
          currentIndex = herPreferences.index(currentHusband)
          hisIndex = herPreferences.index(he)
          #Accept the proposal if 
          #"he" has higher preference in the herPreference list
          if currentIndex > hisIndex:
             #New stable match is found for "her"
             womanSpouse[she] = he
             manSpouse.remove((currentHusband, her_name))
             manSpouse.append((his_name, her_name))
             nextManChoice[he] = nextManChoice[he] + 1
             #Pop the newly wed husband
             unmarriedMen.pop(0)
             #Now the previous husband is unmarried add
             #him to the unmarried list
             unmarriedMen.insert(0,currentHusband)
          else:
             nextManChoice[he] = nextManChoice[he] + 1
             
           
            
  
    return manSpouse



# TODO- method 2
def mpda_random(edgesPref, devsPref):
    deviceDict = devsPref.copy()
    edgeDict = edgesPref.copy()
    matchingGraph = []
    n = len(deviceDict)
    

    # Initially, all n men are unmarried
    unmarriedMen = list(devsPref)
    # None of the men has a spouse yet, we denote this by the value None
    manSpouse = []                     
    # None of the women has a spouse yet, we denote this by the value None
    womanSpouse = [None] * n                      
    # Each man made 0 proposals, which means that 
    # his next proposal will be to the woman number 0 in his list
    nextManChoice = [0] * n                       
    
    # While there exists at least one unmarried man:
    while unmarriedMen:
        random.shuffle(unmarriedMen)
        # Pick an arbitrary unmarried man
        his_name = unmarriedMen[0]
        he = unmarriedMen.index(his_name)
        # Store his ranking in this variable for convenience
        hisPreferences = list(deviceDict.values())[he]
        # Find a woman to propose to
        her_name = hisPreferences[nextManChoice[he]]
        she = hisPreferences.index(her_name)
        # Store her ranking in this variable for convenience
        herPreferences = list(edgeDict.values())[she]
        # Find the present husband of the selected woman (it might be None)
        currentHusband = womanSpouse[she]
       
        
        # Now "he" proposes to "she". 
        # Decide whether "she" accepts, and update the following fields
        # 1. manSpouse
        # 2. womanSpouse
        # 3. unmarriedMen
        # 4. nextManChoice
        if currentHusband == None:
          #No Husband case
          #"She" accepts any proposal
          womanSpouse[she] = his_name
          manSpouse.append((his_name, her_name))
          #"His" nextchoice is the next woman
          #in the hisPreferences list
          nextManChoice[he] = nextManChoice[he] + 1
          #Delete "him" from the 
          #Unmarried list
          unmarriedMen.pop(0)
        else:
          #Husband exists
          #Check the preferences of the 
          #current husband and that of the proposed man's
          currentIndex = herPreferences.index(currentHusband)
          hisIndex = herPreferences.index(he)
          #Accept the proposal if 
          #"he" has higher preference in the herPreference list
          if currentIndex > hisIndex:
             #New stable match is found for "her"
             womanSpouse[she] = he
             manSpouse.remove((currentHusband, her_name))
             manSpouse.append((his_name, her_name))
             nextManChoice[he] = nextManChoice[he] + 1
             #Pop the newly wed husband
             unmarriedMen.pop(0)
             #Now the previous husband is unmarried add
             #him to the unmarried list
             unmarriedMen.insert(0,currentHusband)
          else:
             nextManChoice[he] = nextManChoice[he] + 1
             
           
            
  
    return manSpouse
