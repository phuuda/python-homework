import re
import unittest

with open('sample.txt', 'r', encoding = 'utf-8') as f:
    text = f.read()

def to_table(results):

    """
    input is list of lists, each in the following form:
    [left context, keyword, right context]

    to_table prints each contained list as a KWIQ format table
    """
    
    before_res = []
    end = ''
    
    for line in results:
        p = len(line[0])
        before_res.append(p)
        
    max_left_len = max(before_res)
    for line in results:
        
        left_len = len(line[0])
        left_space_len = max_left_len - left_len + 3
        space = ''
        
        for x in range(left_space_len):
            space += ' '
            
        add = ''
        add += line[0]
        add += space
        add += line[1]
        add += '   '
        add += line[2]
        
        end += add
        end += '\n'
        
    return(end)


def kwiq(word, text, num = 3):

    """
    finds all instances of input 'word' in 'text
    
    returns list of lists, each in the following form:
    [left context, keyword, right context]

    num - number of words contained in right and left context each
    
    """
    

    results = []
    punct = ['\"', '\?', '!', '\.', ',', ':', ';', '-',
             '--', '!\"', ',--', '?\"', '),', '(']

    if isinstance(num,str):
        return('num must be integer')
    
    if num:
        if isinstance(text,str):
            if isinstance(word,str):

                while '\n' in text:
                    text = text.replace('\n', ' ')
                while '  ' in text:
                    text = text.replace('  ', ' ')
                words = text.split(' ') 
                
                for i, j in enumerate(words):
                    word_no_punct = j
                
                    for n in punct:
                        while n in word_no_punct:
                            word_no_punct = word_no_punct.replace(n, '')                

                    if word_no_punct.lower() == word.lower():
                        word_index = i


                        if i - num >= 0:
                            before = words[i-num:i]
                            before = ' '.join(before)
                    
                        if i - num < 0:
                            before = words[0:i]
                            before = ' '.join(before)

                                                   
                        middle = words[i]

                        last_ind = len(words) - 1
                        
                        if i + num + 1 <= last_ind:
                        
                            after = words[i+1:i+num+1]
                            after = ' '.join(after)

                        if i + num + 1 > last_ind:
                            
                            after = words[i+1:last_ind]
                            after = ' '.join(after)
                            after += ' '
                            after += words[last_ind]

                        results.append([before, middle, after])
                  
            return results
        
        if isinstance(text,int):
            return('text must be string')
        
        if isinstance(word,int):
            return('word must be string')
        
                      
print(to_table(kwiq('Давид', text, num = 9)))

class KWIQTest(unittest.TestCase):
    def test_bad_case(self):
        self.assertEqual(kwiq('Давид', 5), 'text must be string')
        self.assertEqual(kwiq('Давид', 'Давид', num = 'я'), 'num must be integer')        
    
if __name__ == '__main__':
    unittest.main()
    
    
