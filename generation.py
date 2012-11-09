import random
import re

class MarkovChains:

    START_STATE = 0

    def __init__(self, delimiters):
        self.delimiters = delimiters    # delimits sentences
        self.cardinalities = dict()     # cardinality of each state's sample space        
        self.occurrences = dict()       # state occurrences
        self.cardinalities[MarkovChains.START_STATE] = 0
        self.occurrences[MarkovChains.START_STATE] = dict()
        
    def _add_chain(self, chain):
        states = chain.split()
        if len(states) > 0:

            prevState = MarkovChains.START_STATE
            self.cardinalities[MarkovChains.START_STATE] += 1
            
            for state in states:
                
                if prevState in self.occurrences:
                    if state in self.occurrences[prevState]:
                        self.occurrences[prevState][state] += 1
                    else:
                        self.occurrences[prevState][state] = 1
                else:
                    self.occurrences[prevState] = dict()
                    self.occurrences[prevState][state] = 1
                        
                prevState = state
                    
                if state in self.cardinalities:
                    self.cardinalities[state] += 1
                else:
                    self.cardinalities[state] = 1    

    def add_text(self, text):        
        for chain in re.split(r"[" + self.delimiters + "]+", text):
            self._add_chain(chain)

    def generate_text(self, sentenceCount):
        text = ""
        for i in range(0, sentenceCount):
            text += " ".join(self._generate_text_sentence()) + ".\n"
        return text        

    def _generate_text_sentence(self):
        sentence = []
        state = self._get_random_state(MarkovChains.START_STATE)
        while not state is None:            
            sentence.append(state)
            if state in self.occurrences:
                state = self._get_random_state(state)
            else:
                state = None
        return sentence

    def _get_random_state(self, state):        
        states = list(self.occurrences[state].keys())
        cardinalities = list(self.occurrences[state].values())
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
        for tail, pairs in self.occurrences.items():        
            for head, occurrence in pairs.items():
                if tail == MarkovChains.START_STATE:
                    print("[Start] -> {0} ({1}/{2})".format(head, occurrence, self.cardinalities[tail]))
                else:
                    print("{0} -> {1} ({2}/{3})".format(tail, head, occurrence, self.cardinalities[tail]))                  

    
    
            
