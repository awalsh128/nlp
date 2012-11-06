import random
import re

class MarkovChains:

    START_STATE = 0

    def __init__(self):
        self.cardinalities = dict() # cardinality of each state's sample space        
        self.transitions = dict()   # state transitions
        self.cardinalities[MarkovChains.START_STATE] = 0
        self.transitions[MarkovChains.START_STATE] = dict()
        
    def _add_chain(self, chain):
        states = chain.split()
        if len(states) > 0:

            prevState = MarkovChains.START_STATE
            self.cardinalities[MarkovChains.START_STATE] += 1
            
            for state in states:
                
                if prevState in self.transitions:
                    if state in self.transitions[prevState]:
                        self.transitions[prevState][state] += 1
                    else:
                        self.transitions[prevState][state] = 1
                else:
                    self.transitions[prevState] = dict()
                    self.transitions[prevState][state] = 1
                        
                prevState = state
                    
                if state in self.cardinalities:
                    self.cardinalities[state] += 1
                else:
                    self.cardinalities[state] = 1    

    def add_text(self, text):        
        for chain in re.split(r"[.!?]+", text):
            self._add_chain(chain)

    def generate_text(self, sentenceCount):
        text = ""
        for i in range(0, sentenceCount):
            text += " ".join(self._generate_text_sentence()) + ". "
        return text        

    def _generate_text_sentence(self):
        sentence = []
        state = self._get_random_state(MarkovChains.START_STATE)
        while not state is None:            
            sentence.append(state)
            if state in self.transitions:
                state = self._get_random_state(state)
            else:
                state = None
        return sentence

    def _get_random_state(self, state):        
        states = list(self.transitions[state].keys())
        cardinalities = list(self.transitions[state].values())
        if len(states) > 0:
            mix = []
            for i in range(0, len(states)):
                j = cardinalities[i]
                while j >= 0:
                    mix.append(states[i])
                    j -= 1
            return mix[random.randint(0, len(mix) - 1)]
        else:
            return None

    def print_chains(self):
        for tail, headCardinalityPairs in self.transitions.items():        
            for head, cardinality in headCardinalityPairs.items():
                if tail == MarkovChains.START_STATE:
                    print("[Start] -> {0} ({1}/{2})".format(head, cardinality, self.cardinalities[tail]))
                else:
                    print("{0} -> {1} ({2}/{3})".format(tail, head, cardinality, self.cardinalities[tail]))                  

    
    
            
