
TABYAML = "  "

class State :
    def __init__(self,name,entry,transitions):
        self.name = name
        self.entry = entry
        self.transitions = transitions

    def renderTransition(self):
        text  = ""
        for transitions in self.transitions:
            text += transitions.render()
        return text

    def render(self):
        return TABYAML*3+"""- name: """+self.name+"""
"""+TABYAML*4+"""on entry: |
"""+TABYAML*5+self.entry+"""
"""+TABYAML*4+"""transitions:
"""+self.renderTransition() 

class Transition : 
    def __init__(self,target,event):
        self.target = target
        self.event = event
    def render(self):
        return TABYAML*4+"""- target: """+self.target+"""
"""+TABYAML*5+"""event : """+self.event+"""
"""
