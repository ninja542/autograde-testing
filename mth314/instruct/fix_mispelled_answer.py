# check for mispelled ANSWER in source code

def check_mispelled(suspect):
    correct_word = "ANSWER"
    letters_nearby = {
        "A": ["S","W","Q","Z"],
        "N": ["B","M","H","J"],
        "S": ["D","E","W","A","Z","X"],
        "W": ["Q","E","A","S","D"],
        "E": ["W","S","D","R","F"],
        "R": ["E","D","F","G","T"]
    }
    for i,char in enumerate(suspect):
        try:
            if char != correct_word[i]:
                print(char)
                print(letters_nearby[correct_word[i]])
                if char not in letters_nearby[correct_word[i]]:
                    return False
        except:
            return False
    return True