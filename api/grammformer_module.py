import torch
import spacy
from gramformer import Gramformer
import errant
import time

class gramm():

    

    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")
        self.gf = Gramformer(models = 1, use_gpu=False)
        self.annotator = errant.load('en')
        self.e_types = {
            'AJD':'Adjective',
            'ADV':'Adverb',
            'CONJ':'Conjunction',
            'DET':'Determiner',
            'NOUN':'Noun',
            'PART':'Particle',
            'PREP':'Preposition',
            'PRON':'Pronoun',
            'PUNCT':'Punctuation',
            'VERB':'Verb',
            'CONTR':'Contraction',
            'MORPH':'Morphology',
            'ORTH':'Orthography',
            'OTHER':'Other',
            'SPELL':'Spelling',
            'WO':'Word Order',
            'ADJ:FORM':'Adjective Form',
            'NOUN:INFL':'Noun Inflection',
            'NOUN:NUM':'Noun Number',
            'NOUN:POSS':'Noun Possessive',
            'VERB:FORM':'Verb Form',
            'VERB:INFL':'Verb Inflection',
            'VERB:SVA':'Verb Agreement',
            'VERB:TENSE':'Verb Tense',
            'SPACE':'space'
        }
        torch.manual_seed(1212)

    def extrae_oraciones(self, caso):
        doc = self.nlp(caso)
        influent_sentences = [sent.text for sent in doc.sents if sent.text!='\n' or sent.text!='']
        return influent_sentences

    def corrige_oracion(self, sentence):
        if sentence == '' or sentence == '\n':
            return None
        else:
            return list(self.gf.correct(sentence, max_candidates=1))[0]
    
    def extrae_errores(self, sentence, sentence_cor):
        orig = self.annotator.parse(sentence, tokenise=True )
        cor = self.annotator.parse(sentence_cor, tokenise=True )
        edits = self.annotator.annotate(orig, cor)
        return (orig,cor,edits)
    
    def comillas(self, cad):
        return ' "'+cad+'" '
    
    def convierte_errores(self, sentence, orig, cor, edits):
        res_err = {'sentence':sentence,'mistakes':[]}
        for e in edits:
            try:
                if (e.type[2:] == 'SPACE') and ( (e.o_toks.root.i == len(orig)-1) or (e.o_toks.root.i == 0) ):
                    continue
                    
                if(e.type[0]=='M'):
                    res_err['mistakes'].append('Missing ' + self.e_types[e.type[2:]] + self.comillas(e.c_str) + ".")
                if(e.type[0]=='U'):
                    if len(e.o_toks) < 5:
                        res_err['mistakes'].append('Unnecessary ' + self.e_types[e.type[2:]] + self.comillas(e.o_str)+ ".")
                if(e.type[0]=='R'):
                    res_err['mistakes'].append('Replace ' + self.e_types[e.type[2:]] + self.comillas(e.o_str) + 'for' + self.comillas(e.c_str)+ ".")
            except Exception as exc:
                print(exc)
        return res_err
    
    def gramm_best(self, caso):
        start = time.time() #---------------
        influent_sentences = self.extrae_oraciones(caso)
        lis_mistakes = []
        for sentence in influent_sentences:
            sentence_cor = self.corrige_oracion(sentence)
            if (sentence_cor == None):
                continue
            (orig,cor,edits) = self.extrae_errores(sentence, sentence_cor)
            lis_mistakes.append(self.convierte_errores(sentence,orig,cor,edits))
        cad = ''
        for i in lis_mistakes:
            cad += "Sentence:\n " + i['sentence']
            cad += "\n\nMistakes:\n"
            for j in i['mistakes']:
                cad += "- " + j + "\n"
        print("Tiempo de Ejecución ","{:10.2f}".format(time.time() - start),' segundos')
        return cad
    
    def test_gram(self):
        return "GrammFormer works perfectly!!!"