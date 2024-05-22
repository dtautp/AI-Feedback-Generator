from gramformer import Gramformer
import torch

def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(1212)

gf = Gramformer(models = 1, use_gpu=False) # 1=corrector, 2=detector

cad = "Nathaly and I made 3 friends, Raffaelle is Italian, he's a graphic designer, he have 21 years old and Suzy and Anna are mexican, they're sisters and they have 18 years old, they are studying languages, and Suzy is working as a writer for the campus newspaper ."

print(gf.correct(cad, max_candidates=1))