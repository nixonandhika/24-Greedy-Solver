from random import randint, sample

def symbol_switch(arg):
    listSym = ["H","C","D","S"]
    return listSym[arg-1]

class Cards:
    def __init__(self, num, sym):
        self.num = num
        self.sym = sym

class BackEnd():
    def __init__(self, deck, scoreList):
        self.scoreList = {'+':5, '-':4, '*':3, '/':2}
        self.deck = []


    def getNums(self):
        availableIndex = sorted(list(sample(range(0,len(self.deck)),4)),reverse=True)
        nums = [self.deck[idx] for idx in availableIndex]
        for idx in availableIndex:
            del self.deck[idx]
        return nums

    def reset(self):
        self.deck = [None] * 52
        self.reset_deck()

    def reset_deck(self):
        sym_num = 0
        for i in range(52):
            if (i % 13 == 0):
                sym_num += 1
            self.deck[i] = Cards(((i % 13) + 1), symbol_switch(sym_num))

    def solution(self,listNum):
        listNum.sort(reverse = True)
        expr = str(listNum.pop(0))
        cExpr1 = expr
        TempExpr1 = cExpr1
        for num in listNum:
            maxPoint1 = -50
            maxPoint2 = -50

            for key, val in self.scoreList.items():
                cExpr = TempExpr1

                #Untuk proses kurungnya
                #jika ekspresi mengandung + atau -, dan operator yang sedang dipertimbangkan adalah * atau /
                if (cExpr.find('+') != -1 or cExpr.find('-')!= -1) and (key == '*' or key =='/'):
                    if (cExpr.count('+')+cExpr.count('-')+cExpr.count('*')+cExpr.count('/')) == 1: #jika ekspresi masih hanya mengandung 1 operator
                        cExpr = "(" + cExpr + ")"
                    else: #jika operasi sudah mengandung lebih dari 1 operator
                        #mencari indeks operator + atau -
                        OpIdx1 = cExpr.find('+')
                        if OpIdx1 == -1:
                            OpIdx1 = cExpr.find('-')
                        OpIdx2 = cExpr[OpIdx1+1:].find('+')
                        if OpIdx2 == -1:
                            OpIdx2 = cExpr[OpIdx1+1:].find('-')
                        if OpIdx2 > 0: #jika kedua operator adalah + atau -, berikan kurung
                            cExpr = '(' + cExpr + ')'
                        elif (cExpr.find('*')!=-1 and OpIdx1>cExpr.find('*')) or (cExpr.find('/')!=-1 and OpIdx1>cExpr.find('/')):
                            OpIdx3 = cExpr.find('*')
                            if OpIdx3 == -1:
                                OpIdx3 = cExpr.find('/')
                            cExpr = cExpr[0:OpIdx3+1] + '(' + cExpr[OpIdx3+1:] + ')'
                #persamaan yang pake kurung
                cExpr1 = cExpr + key + str(num)
                #persamaan yang tanpa kurung
                cExpr2 = expr + key + str(num)
                #dari yg pake kurung dan tidak dicari masing2 tertingginya
                if self.calcPoint(cExpr1) > maxPoint1:
                    maxPoint1 = self.calcPoint(cExpr1)
                    choice1 = cExpr1
                if self.calcPoint(cExpr2) > maxPoint2:
                    maxPoint2 = self.calcPoint(cExpr2)
                    choice2 = cExpr2
            TempExpr1 = choice1

            #yang nilainya = 24 diambil dulu
            #Kalo gaada ambil yang pointnya tertinggi antara pers. yg pake kurung
            #dan yang ngga
            if (eval(choice1)==24):
                expr = choice1
                maxPoint = maxPoint1
            elif (eval(choice2)==24):
                expr = choice2
                maxPoint = maxPoint2
            else:
                if maxPoint1 >= maxPoint2 :
                    expr = choice1
                    maxPoint = maxPoint1
                else:
                    expr = choice2
                    maxPoint = maxPoint2
                #sampe sini

        expr = expr + ' = ' + str(eval(expr))
        return expr, maxPoint

    def calcPoint(self,expr):
        result = eval(expr)
        score = -abs(result-24)
        for key, val in self.scoreList.items():
            score += expr.count(key)*val
        #tambahan kurung

        return (score - expr.count('('))
