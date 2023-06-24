

import itertools
WHITE = "white"
BLACK = "black"


class Game:
    
    def __init__(self):
        self.gameboard = {}
        self.playersturn = BLACK
        self.message = "buyruq kiriting"
        self.placePieces()
        print("shaxmat dasturi. harakatlarni algebraik yozuvda bo'sh joy bilan ajrating. Misol uchun: a7 a6")
        self.main()

        
    def placePieces(self):

        for i in range(0,8):
            self.gameboard[(i,1)] = Pawn(WHITE,uniDict[WHITE][Pawn],1)
            self.gameboard[(i,6)] = Pawn(BLACK,uniDict[BLACK][Pawn],-1)
            
        placers = [Rook,Knight,Bishop,Queen,Shoh,Bishop,Knight,Rook]
        
        for i in range(0,8):
            self.gameboard[(i,0)] = placers[i](WHITE,uniDict[WHITE][placers[i]])
            self.gameboard[((7-i),7)] = placers[i](BLACK,uniDict[BLACK][placers[i]])
        placers.reverse()

        
    def main(self):
        
        while True:
            self.printBoard()
            print(self.message)
            self.message = ""
            startpos,endpos = self.parseInput()
            try:
                target = self.gameboard[startpos]
            except:
                self.message = "ma'lumot topa olmadi; ehtimol, index diapazondan tashqarida"
                target = None
                
            if target:
                print("topildi "+str(target))
                if target.Color != self.playersturn:
                    self.message = "figuralar shaxmat doskasidan tashqarida harakatlanmaydi"
                    continue
                if target.isValid(startpos,endpos,target.Color,self.gameboard):
                    self.message = "bu to'g'ri harakat"
                    self.gameboard[endpos] = self.gameboard[startpos]
                    del self.gameboard[startpos]
                    self.isCheck()
                    if self.playersturn == BLACK:
                        self.playersturn = WHITE
                    else : self.playersturn = BLACK
                else : 
                    self.message = "no'tog'ri harakat" + str(target.availableMoves(startpos[0],startpos[1],self.gameboard))
                    print(target.availableMoves(startpos[0],startpos[1],self.gameboard))
            else : self.message = "bu bo'shliqda hech qanday ma'lumot yo'q"
                    
    def isCheck(self):
        #shohlarning qayerdaligini aniqlang, o'sha shohlarga qarama-qarshi rangdagi barcha qismlarni tekshiring,
        # so'ngra urilgan bo'lsa, uning figura ekanligini tekshiring.
        king = Shoh
        kingDict = {}
        pieceDict = {BLACK : [], WHITE : []}
        for position,piece in self.gameboard.items():
            if type(piece) == Shoh:
                kingDict[piece.Color] = position
            print(piece)
            pieceDict[piece.Color].append((piece,position))
        #white
        if self.canSeeKing(kingDict[WHITE],pieceDict[BLACK]):
            self.message = "o'yin Oq o'yinchi nazorat ostida"
        if self.canSeeKing(kingDict[BLACK],pieceDict[WHITE]):
            self.message = "o'yin Qora o'yinchi nazorat ostida"
        
        
    def canSeeKing(self,kingpos,piecelist):
        #parchalar roʻyxatidagi har qanday boʻlak (bu (boʻlak, joylashuv) kortejlar massivi) kingposda qirolni koʻra olishini tekshiradi.
        for piece,position in piecelist:
            if piece.isValid(position,kingpos,piece.Color,self.gameboard):
                return True
                
    def parseInput(self):
        try:
            a,b = input().split()
            a = ((ord(a[0])-97), int(a[1])-1)
            b = (ord(b[0])-97, int(b[1])-1)
            print(a,b)
            return (a,b)
        except:
            print("buyruqda xatolik. Iltimos, yana bir bor urinib ko'ring")
            return((-1,-1),(-1,-1))
    
        
    def printBoard(self):
        print("  1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")
        for i in range(0,8):
            print("-"*32)
            print(chr(i+97),end="|")
            for j in range(0,8):
                item = self.gameboard.get((i,j)," ")
                print(str(item)+' |', end = " ")
            print()
        print("-"*32)
            
           
        
    """o'yin sinfi. quyidagi a'zolar va usullarni o'z ichiga oladi:
    har bir o'yinchi uchun ikkita to'plam
    Ushbu qismlarga havolalar bilan 8x8 qismli massiv
    foydalanuvchi kiritgan ma'lumotni boshlang'ich va yakuniy nuqtalarni bildiruvchi
    ikkita kortej ro'yxatiga aylantiradigan tahlil qilish funktsiyasi
    o'yinchilarning matda ekanligini tekshiradigan checkmateExists funksiyasi
    har ikkala o'yinchining tekshirilayotganligini tekshiradigan checkExists funksiyasi (men bu noaniqlikni oldim)
    ma'lumotni qabul qiluvchi, uni tahlil qilish vositasidan o'tkazadigan,
    harakat to'g'ri yoki yo'qligini so'raydi va agar bo'lsa, bo'lakni siljitadi.
    agar harakat boshqa bo'lak bilan ziddiyatli bo'lsa, bu qism olib tashlanadi.
    ischeck(mate) ishga tushiriladi va agar mat bo'lsa, o'yin kim g'alaba qozonishi haqida xabar chiqaradi.
    """

class Piece:
    
    def __init__(self,color,name):
        self.name = name
        self.position = None
        self.Color = color
    def isValid(self,startpos,endpos,Color,gameboard):
        if endpos in self.availableMoves(startpos[0],startpos[1],gameboard, Color = Color):
            return True
        return False
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def availableMoves(self,x,y,gameboard):
        print("ERROR: asosiy sinf uchun harakat yo'q")
        
    def AdNauseum(self,x,y,gameboard, Color, intervals):
        """berilgan intervalni yana bir qism ishga tushguncha takrorlaydi.
        agar bu qism bir xil rangda bo'lmasa, u bo'sh katak qo'shiladi va
         keyin ro'yxat qaytariladi"""
        answers = []
        for xint,yint in intervals:
            xtemp,ytemp = x+xint,y+yint
            while self.isInBounds(xtemp,ytemp):
                #print(str((xtemp,ytemp))+"is in bounds")
                
                target = gameboard.get((xtemp,ytemp),None)
                if target is None: answers.append((xtemp,ytemp))
                elif target.Color != Color: 
                    answers.append((xtemp,ytemp))
                    break
                else:
                    break
                
                xtemp,ytemp = xtemp + xint,ytemp + yint
        return answers
                
    def isInBounds(self,x,y):
        "doskada pozitsiya mavjudligini tekshiradi"
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False
    
    def noConflict(self,gameboard,initialColor,x,y):
        "bitta pozitsiya shaxmat qoidalariga zid kelmasligini tekshiradi"
        if self.isInBounds(x,y) and (((x,y) not in gameboard) or gameboard[(x,y)].Color != initialColor) : return True
        return False
        
        
chessCardinals = [(1,0),(0,1),(-1,0),(0,-1)]
chessDiagonals = [(1,1),(-1,1),(1,-1),(-1,-1)]

def knightList(x,y,int1,int2):
    """rook uchun alohida, noConflict testlari uchun pozitsiya atrofida kerakli qiymatlarni almashtiradi"""
    return [(x+int1,y+int2),(x-int1,y+int2),(x+int1,y-int2),(x-int1,y-int2),(x+int2,y+int1),(x-int2,y+int1),(x+int2,y-int1),(x-int2,y-int1)]
def kingList(x,y):
    return [(x+1,y),(x+1,y+1),(x+1,y-1),(x,y+1),(x,y-1),(x-1,y),(x-1,y+1),(x-1,y-1)]



class Knight(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return [(xx,yy) for xx,yy in knightList(x,y,2,1) if self.noConflict(gameboard, Color, xx, yy)]
        
class Rook(Piece):
    def availableMoves(self,x,y,gameboard ,Color = None):
        if Color is None : Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals)
        
class Bishop(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessDiagonals)
        
class Queen(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals+chessDiagonals)
        
class Shoh(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return [(xx,yy) for xx,yy in kingList(x,y) if self.noConflict(gameboard, Color, xx, yy)]
        
class Pawn(Piece):
    def __init__(self,color,name,direction):
        self.name = name
        self.Color = color
        #Albatta, eng kichik bo'lakni kodlash eng qiyin.
        # Yo'nalish 1 yoki -1 bo'lishi kerak, agar piyoda "orqaga" ketayotgan bo'lsa -1 bo'lishi kerak"
        self.direction = direction
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers = []
        if (x+1,y+self.direction) in gameboard and self.noConflict(gameboard, Color, x+1, y+self.direction) : answers.append((x+1,y+self.direction))
        if (x-1,y+self.direction) in gameboard and self.noConflict(gameboard, Color, x-1, y+self.direction) : answers.append((x-1,y+self.direction))
        if (x,y+self.direction) not in gameboard and Color == self.Color : answers.append((x,y+self.direction))# va keyingi shart - matnni hisoblashda imkonsiz harakat ishlatilmasligiga ishonch hosil qilish.
        return answers

uniDict = {WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "♗", Shoh : "♔", Queen : "♕" }, BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "♝", Shoh : "♚", Queen : "♛" }}
        

        


Game()
