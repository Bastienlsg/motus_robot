class WordFinder:
    @staticmethod
    def calculate_score(word, good_letters, bad_place_letters, bad_letters):
        score = 0
        for letter in word:
            if (letter, word.index(letter)) in good_letters:
                score += 3
            elif letter in [l[0] for l in bad_place_letters]:
                score += 2
            elif letter not in bad_letters:
                score += 1
        return score

    @staticmethod
    def find_best_word(words, good_letters, bad_place_letters, bad_letters):
        best_word = ""
        best_score = 0
        for word in words:
            score = WordFinder.calculate_score(word, good_letters, bad_place_letters, bad_letters)
            if score > best_score:
                best_word = word
                best_score = score
        return best_word
