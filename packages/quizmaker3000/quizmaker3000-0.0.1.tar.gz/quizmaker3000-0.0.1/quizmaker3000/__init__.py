import time
from colorama import Fore,init,Back,Style

init()
class quiz():
  def __init__(self):
    self.difficulties = []
    self.difficulties_num = 0
    self.questions_gotten_right = []
    self.questions_gotten_right_num = 0
    self.questions_gotten_wrong = []
    self.questions_gotten_wrong_num = 0
    self.order = []
    self.guesses = []
  def add_difficulty(self,difficulty):
    self.difficulties_num += 1
    if not self.difficulties_num >= 2:
      self.difficulties.append({"name":str(difficulty),"questions":[]})
    else:
      print('Sadly, it\'s glitched and you can\'t make more than one!')
    
    
    
  def add_question(self,question,answer,difficulty):
    for i in self.difficulties:
      if i['name'] == str(difficulty):
        i['questions'].append({"question":str(question),"answer":str(answer),"multiple_answer":False,'difficulty':str(difficulty)})
  def add_multiple_answer_question(self,question:str,answers:list,difficulty:str):
    for i in self.difficulties:
      if i['name'] == str(difficulty):
        i['questions'].append({'question':str(question),'answer':answers,'multiple_answer':True,'difficulty':str(difficulty)})
    
      
    
  def ez(self):
    print(self.difficulties)
  def start(self,difficulty):
    print(Fore.BLUE,'Starting..')
    time.sleep(1)
    a = False
    for l in self.difficulties:
      if True:
        
      
        for m in l['questions']:
          if not m['multiple_answer']:
            
            print(Fore.RED,'The question is...')
            print(Fore.RED,m['question'])
            print(Fore.GREEN,'Input your answer V')
            inp = input(' ')
            if str(inp).upper() == m['answer'].upper():
              self.guesses.append({"question":str(m['question']),"guess":str(inp),"answer":str(m['answer'])})
              self.questions_gotten_right.append(m)
              self.questions_gotten_right_num += 1
            else:
              self.guesses.append({"question":str(m['question']),"guess":str(inp),"answer":str(m['answer'])})
              self.questions_gotten_wrong.append(m)
              self.questions_gotten_wrong_num += 1
          else:
            bob = ''
            last = 0
            for i in m['answer']:
              if not last >= (len(m) - 1):
                last += 1
              else:
                bob += ', or '
              
              
              
              
            print(Fore.RED,'The question is...')
            print(Fore.RED,m['question'])
            print(Fore.GREEN,'Input your answer V')
            inp = input(' ')
            for answer in m['answer']:
              if str(inp).upper() == answer.upper():
                self.guesses.append({"question":str(m['question']),"guess":str(inp),"answer":str(m['answer'])})
                self.questions_gotten_right.append(m)
                self.questions_gotten_right_num += 1
                a = True
                break
            if not a:
              self.guesses.append({"question":str(m['question']),"guess":str(inp),"answer":str(m['answer'])})
              self.questions_gotten_wrong.append(m)
              self.questions_gotten_wrong_num += 1
              
    print(f'\n\n\nYou got {self.questions_gotten_right_num} right!')
    print(f'Though, you got {self.questions_gotten_wrong_num} wrong :(')
    print('\n')
    for i in self.guesses:
      print(f'The question was: ',i['question'],'.')
      print(f'\nThe answer was: ',i['answer'])
      if i['guess'].upper() == i['answer'].upper():   
        print(f'\nYour guess was: ',i['guess'],Fore.GREEN,'.... You got that one right!')
      else:
        print(f'\nYour guess was: ',i['guess'],Fore.RED,'... Sadly, you got that one wrong :(')
        print(Fore.GREEN,'')
    
    
  def start_all(self):
    for i in self.order:
      self.start(i)
      
