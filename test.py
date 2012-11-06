from generation import MarkovChains
import re

file = open("sonnets.txt")
text = re.sub(r'\n.+\n', '', file.read())

markov = MarkovChains()
markov.add_text(text)
print(markov.generate_text(2))
