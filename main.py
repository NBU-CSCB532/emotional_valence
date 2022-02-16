#from modules.A.NewsDownloader import NewsDownloader
from modules.B.entityCleaner import EntityCleaner
from modules.C.TextDecompositionIntoSentencesAndWords import TextDecompositionIntoSentencesAndWords
from modules.D.RetrievalOfOxfordTranscriptions import RetrievalOfOxfordTranscriptions
from modules.DictionaryPopulator import DictionaryPopulator
from modules.E.BiphonicParser import BiphonicParser
from modules.F.BiphonicRepresentationOfTexts import BiphonicRepresentationOfTexts
from modules.G.BiphoneWeights import BiphoneWeights
from modules.SyllableWeightPopulator import SyllableWeightPopulator

from modules.ProjectCleaner import ProjectCleaner

projectCleaner = ProjectCleaner()
projectCleaner.clean()

print("Start Module A [Internet news collector]")
#news_test = NewsDownloader()
print("End Module A [Internet news collector]")

print("Start Module B [Entity detection]")
entity_c = EntityCleaner()
print("End Module B [Entity detection]")

print("Start Zad3")




""" Old module replaced by the file Correlation"""
#########syllable_weight_populator = SyllableWeightPopulator()

#########syllable_weight_populator.find_correlation_between_vectors()
print("Populate syllable weights")
#########syllable_weight_populator.populate()
""" Old module replaced by the file Correlation"""




dictionary_populator = DictionaryPopulator()

print("Populate dictionaries")
dictionary_populator.populate()

print("Find correlation between two vectors")


print("End Zad3")

print("Start Module C [Text decomposition into sentences and words]")
textDecompositionModule = TextDecompositionIntoSentencesAndWords()

textDecompositionModule.replace_with_protected_text()
textDecompositionModule.decompose()
textDecompositionModule.merge()
textDecompositionModule.novels()

print("End Module C [Text decomposition into sentences and words]")

print("Start Module D [Retrieval of Oxford transcriptions]")
retrievalOfOxfordTranscriptions = RetrievalOfOxfordTranscriptions
retrievalOfOxfordTranscriptions.retrieve()
retrievalOfOxfordTranscriptions.populate_transcribed_and_not_transcribed()
print("End Module D [Retrieval of Oxford transcriptions]")

print("Start Module E [Biphonic parser]")
biphonic_parser = BiphonicParser()

biphonic_parser.prepare_dictionary_for_biphone()
biphonic_parser.startLazarScript()
biphonic_parser.populate_word_syllables()
print("End Module E [Biphonic parser]")

print("Start Module F [Biphonic Representation of the texts]")
biphonic_representatino_of_texts = BiphonicRepresentationOfTexts()

biphonic_representatino_of_texts.start()
print("End Module F [Biphonic Representation of the texts]")

print("Start Module G [Biphonic Weights of the texts]")
biphone_weights = BiphoneWeights()

biphone_weights.start()
print("End Module G [Biphonic Weights of the texts]")