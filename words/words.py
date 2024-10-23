class Words :
    def __init__(self,word_english,word_pershin,) -> None:
        self.word_english = word_english
        self.word_pershin = word_pershin
    def meaning(self):
            return f" : {self.word_english} , {self.word_pershin}"
    def show(self):
           return f"see all words  : {self.word_english} , {self.word_pershin}"