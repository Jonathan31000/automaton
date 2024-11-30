def am_I_struggle(i):
      while i < 5:
         i + 1
         if i == 5:
            return True
         else:
            return i
        
def fonction(a):
    b = 0
    i=am_I_struggle(a)
    while b < 10:
        i=am_I_struggle(a)
        print(i)
        print(b)
        b + 1
        
uiAutoPort = {
    "127.0.0.1:5555": 8200, 
    "127.0.0.1:5585": 8201, 
    "127.0.0.1:5595": 8202
}
(80,79,68)
print(uiAutoPort["127.0.0.1:5555"])
