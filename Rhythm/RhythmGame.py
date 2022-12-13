import pygame
import os
import sys
import FileReadAndWrite as frw
import time #시작메뉴 전환 1초후 화면전환
import pyautogui # https://pyautogui.readthedocs.io/en/latest/msgbox.html


class Controller(): # 메인 컨트롤러 (얘가 반복문 안에서 화면에 표시할 내용 정해줄 거)
    def __init__(self):
        self.currentState = 1
        # 1 : 시작 화면
        # 2 : 음악 선택 화면
        # 3 : 게임 플레이 화면
        # 4 : 트랙 추가 화면
        self.pastState = self.currentState
        self.isChanged = False
        self.vo = None
        self.gameController = GameController(None)
        self.musicChoiceController = MusicChoiceController()
        self.startController = StartController()
        self.addTrackController = AddTrackController()
        self.dao = frw.DAO()
    
    def changeState(self, toNum):
        self.pastState = self.currentState
        self.currentState = toNum
        self.isChanged = True
    
    def mainFunction(self):
        if self.currentState == 1:
            if self.pastState != self.currentState:
                self.startController = StartController()
            elif self.pastState == self.currentState:
                event = self.startController.mainFunction()
                if event == "gameEnd":
                    pygame.quit()
                    sys.exit()
                elif event == "musicChoice":
                    self.changeState(2)
        elif self.currentState == 2:
            if self.pastState != self.currentState:
                self.musicChoiceController = MusicChoiceController()
            elif self.pastState == self.currentState:
                state = self.musicChoiceController.mainFuntion()
                if state == "none":
                    pass
                elif state == "play":
                    self.changeState(3)
                    self.vo = self.musicChoiceController.returnMusicVO() 
                elif state == "addTrack":
                    self.changeState(4)
                    self.vo = self.dao.lastAddedData()
        elif self.currentState == 3:
            if self.pastState != self.currentState:
                self.gameController = GameController(self.vo)
            elif self.pastState == self.currentState:
                event = self.gameController.mainFunction()
                if event == "backToChoice":
                    self.changeState(2)
        elif self.currentState == 4:
            if self.pastState != self.currentState:
                self.addTrackController.setting(self.vo)
            elif self.pastState == self.currentState:
                status = self.addTrackController.mainFunction()
                if status == "returnChoice":
                    self.changeState(2)
        if not self.isChanged:
            self.pastState = self.currentState
        else:
            self.isChanged = False

class StartController():
    def __init__(self):
        self.startImg1 = pygame.image.load(frw.getFilePath("startButton1.png", "png"))
        self.quitImg1 = pygame.image.load(frw.getFilePath("quitButton1.png", "png"))
        self.startImg2 = pygame.image.load(frw.getFilePath("startButton2.png", "png"))
        self.quitImg2 = pygame.image.load(frw.getFilePath("quitButton2.png", "png"))
    
    def mouseOnButton(self, imgType, x, y):
        screen = pygame.display.get_surface()
        mouseX, mouseY = pygame.mouse.get_pos()
        img1, img2 = None, None
        if imgType == "start":
            img1, img2 = self.startImg1, self.startImg2
        elif imgType == "quit":
            img1, img2 = self.quitImg1, self.quitImg2
        else:
            pass
        w = img1.get_width()
        h = img1.get_height()
        if mouseX in range(x, x + w) and mouseY in range(y, y + h):
            screen.blit(img2, (x, y))
            if pygame.mouse.get_pressed()[0]:
                if imgType == "start":
                    return imgType
                else: 
                    return imgType
        else:
            screen.blit(img1, (x, y))
            return "none"
    
    def mainFunction(self):
        screen = pygame.display.get_surface()   
        screen.fill(colorSampleDict["white"])
        font = pygame.font.SysFont("arial", 100, bold=True)
        text = font.render("Rhythm Game Start Menu", True, colorSampleDict["skyblue"])
        screen.blit(text, (450, 200))
        eventA = self.mouseOnButton("start", 450, 500)
        eventB = self.mouseOnButton("quit", 1070, 500)
        if eventA == "start":
            return "musicChoice"
        elif eventB == "quit":
            return "gameEnd"

class MusicChoiceController(): # 음악 선택 화면 구현
    def __init__(self): # 여기다가 변수 선언하면 됨
        dao = frw.DAO()
        self.musicList = dao.getMusicData()
        self.index = 0
        self.selectedIndex = 0
        self.arr = []
    
    def listOnScreen(self):
        FONT = pygame.font.Font(None,40)                         # 노래 제목 폰트 크기 지정
        self.arr = []

        for i in range(5):
            self.arr.append(len(self.musicList[self.index + i].getMusicName()))

        screen = pygame.display.get_surface()
        
        for i in range(5):
            pygame.draw.rect(screen, colorSampleDict["white"], (30, 150 + (i * 100), 70 + self.arr[i] * 14, 50))    # [5]
            pygame.draw.rect(screen, colorSampleDict["skyblue"], (30, 150 + (i * 100), 70 + self.arr[i] * 14, 50), 5)    # [5]
            musicName = FONT.render(self.musicList[self.index + i].getMusicName(),True, colorSampleDict["black"])
            screen.blit(musicName,[40, 160 + (i * 100)])

    def clickEventCheck(self):
        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            for i, length in enumerate(self.arr):
                if mouseX in range(30, 70 + length * 14):
                    if mouseY in range(150 + (i * 100), 200 + (i * 100)):
                        self.selectedIndex = self.index + i
    
    def musicOnScreen(self): 
        vo = self.musicList[self.selectedIndex]
        FONT = pygame.font.Font(None,100)
        screen = pygame.display.get_surface()

        x = 1600 - (len(vo.getMusicName()) * 35)
        pygame.draw.rect(screen, colorSampleDict["white"], (x, 150, 175 + len(vo.getMusicName()) * 35, 100))    # [5]
        pygame.draw.rect(screen, colorSampleDict["skyblue"], (x, 150, 175 + len(vo.getMusicName())* 35, 100), 5)    # [5]
        musicName = FONT.render(vo.getMusicName(),True, colorSampleDict["black"])
        screen.blit(musicName,[x + 10, 160])

        FONT = pygame.font.Font(None,40)
        x = 1700 - (len(vo.getAuthorName()) * 14)
        pygame.draw.rect(screen, colorSampleDict["white"], (x, 300, 70 + len(vo.getAuthorName()) * 14, 50))    # [5]
        pygame.draw.rect(screen, colorSampleDict["skyblue"], (x, 300, 70 + len(vo.getAuthorName()) * 14, 50), 5)    # [5]
        authorName = FONT.render(vo.getAuthorName(),True, colorSampleDict["black"])
        screen.blit(authorName,[x + 10, 310]) 

        score = str(vo.getScore())
        if len(score) <= 7:
            score = ("0" * (7 - len(score))) + score
        x = 1700 - len(score) * 14
        pygame.draw.rect(screen, colorSampleDict["white"], (x, 550, 70 + len(score) * 14, 50))    # [5]
        pygame.draw.rect(screen, colorSampleDict["skyblue"], (x, 550, 70 + len(score) * 14, 50), 5)    # [5]
        score = FONT.render(score,True, colorSampleDict["black"])
        screen.blit(score,[x + 10, 560])
    
    def isMouseScrolled(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    if self.index > 0:
                        self.index -= 1
                        if self.index > 5:
                            self.index = 0
                    else:
                        pass
                elif event.y < 0:
                    if self.index < len(self.musicList) - 5: 
                        self.index += 1
                    else:
                        self.index = len(self.musicList) - 5

    def playButtonAndPlusButton(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, colorSampleDict["white"], (30, 800, 175, 100))    
        pygame.draw.rect(screen, colorSampleDict["skyblue"], (30, 800, 175, 100), 5)   
        pygame.draw.line(screen, colorSampleDict["skyblue"], (87, 850), (147, 850), 5)
        pygame.draw.line(screen, colorSampleDict["skyblue"], (117, 825), (117, 875), 5)

        pygame.draw.rect(screen, colorSampleDict["white"], (1770 - 175, 800, 175, 100))   
        pygame.draw.rect(screen, colorSampleDict["skyblue"], (1770 - 175, 800, 175, 100), 5)  
        FONT = pygame.font.Font(None,80)
        play = FONT.render("play",True, colorSampleDict["skyblue"])
        screen.blit(play, [1770 - 175 + 20, 800 + 15])
    
    def playButtonEvent(self):
        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            if mouseX in range(1770 - 175, 1770) and mouseY in range(800, 800 + 100):
                # print("clickPlayButton")
                return "play"

    def plusButtonEvent(self):
        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            if mouseX in range(30, 30 + 175) and mouseY in range(800, 800 + 100):
                print("clickplusButton")
                status = self.prompt()
                if status == "addTrack":
                    return status
    
    def prompt(self):
        url = pyautogui.prompt("EX) www.youtube.com/watch?v=....", title="Enter The URL", default="")
        if url != None or url != "":
            vd = frw.VideoDownloader()
            status = vd.download(url)
            if status == "urlError":
                a = pyautogui.alert("Invalid URL", title="Alert")
            elif status == "runningException" or status == "fail":
                a = pyautogui.alert("Download Fail", title="Alert")
            elif status == "success":
                a = pyautogui.alert("Dowonload Complete\nYou will be taken to add track screen", title="Alert")
                return "addTrack"
                
    def returnMusicVO(self):
        return self.musicList[self.selectedIndex]
    
    def mainFuntion(self):
        self.listOnScreen()
        self.isMouseScrolled()
        self.playButtonAndPlusButton()
        self.musicOnScreen()
        self.clickEventCheck()
        pBE = self.playButtonEvent()
        if pBE == "play":
            return pBE
        status = self.plusButtonEvent()
        if status == "addTrack":
            return status
        return "none"
        
class GameController():
    def __init__(self, *args):
        self.state = 1 # 1 : 변수 설정, 2 : 게임플레이, 3 : 점수 화면, 4 : 게임오버
        self.fps = 60
        self.hpAndScore = None
        self.musicVO = args[0]
        self.boxArr = [] # 
        self.noteArr = [[], [], [], []] # 노트 
        self.notes = []
        self.events = None
        self.keys = None
        self.dao = frw.DAO()
        self.endEvent = None
    
    def start(self):
        # self.musicVO = musicVO # 바꿔야 함
        pygame.mixer.music.load(frw.getFilePath(self.musicVO.getMusicPath(), "mp3"))
        self.hpAndScore = HpAndScore()
        
        for i in range(4):
            self.boxArr.append(ClickBox(i))
        
        self.getNotes()
        
        pygame.mixer.music.play()
        self.endEvent = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.endEvent)
        self.state += 1
    
    def playing(self):
        try:
            self.getKeysAndEvents()
            self.createNoteArr()
            screen = pygame.display.get_surface()
            for event in pygame.event.get(): # 이 반복문이 현재 작동 안함(checkBoxEvent함수에 수정본 추가)
                if event.type == pygame.KEYUP:
                    for obj in self.boxArr:
                        obj.clickCountReset(event.key)
            for i, obj in enumerate(self.boxArr):
                if obj.checkBoxEvent(self.keys):
                    if len(self.noteArr[i]) > 0:
                        status = self.noteArr[i][0].checkHeightForScore(obj.clickBoxIndexY, obj.height)
                        del self.noteArr[i][0]
                        self.hpAndScore.calcScore(status)
                        # 점수 확인 추가 필요
                    else:
                        self.hpAndScore.decreaseHp() # hp 감소
                else:
                    pass
            for i, track in enumerate(self.noteArr): # [[obj, obj], [], [], []]
                for obj in track:
                    pygame.draw.rect(screen, obj.getBoxColor(), obj.getBoxPos())
                    outScreen = obj.moveDown(self.fps)
                    if outScreen:
                        del self.noteArr[i][0]   
                        self.hpAndScore.decreaseHp()    
                        self.hpAndScore.resetCombo()
                    else:
                        pass       
            
            for obj in self.boxArr:
                pygame.draw.rect(screen, obj.getBoxColor(), obj.getBoxPos(), obj.getBoxBorder())
                obj.resetAfterFrame()
            
            # print(hpAndScoreData.getHpAndScore())
            self.hpAndScore.createHpBoxWithGradient(screen, colorSampleDict["red"], colorSampleDict["yellow"], pygame.Rect(10, 10, 300, 30))
            self.hpAndScore.scoreOnScreen()
            self.hpAndScore.comboOnScreen()
            
            self.gameOverCheck()
            self.gameEndCheck()
        except Exception as e:
            print(e)
    
    def showScore(self):
        screen = pygame.display.get_surface()
        # 점수 저장
        font = pygame.font.SysFont("arial", 100, bold=True, italic=False)
        text1 = font.render("Congratulations!", True, colorSampleDict["white"])
        font = pygame.font.SysFont("arial", 50, bold=True, italic=False)
        text2 = font.render("return", True, colorSampleDict["white"])
        text3 = font.render(self.hpAndScore.getScore(), True, colorSampleDict["white"])
        screen.blit(text1, (1920 / 2 - 300, 1080 / 4))
        screen.blit(text2, (int((1920 / 2) - 30), int((1080 / 4) * 3)))
        screen.blit(text3, (1920 / 2 - 50, 1080 / 2))
        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            if int(mouseX) in range(920, 1060) and int(mouseY) in range(820, 860):
                return "backToChoice"

    def gameEndCheck(self):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pass
        #     if event.type == self.endEvent or event.type == pygame.mixer.music.get_endevent():
        #         print("endEvent 작동")
        #         self.state = 3
        if not pygame.mixer.music.get_busy() and not self.hpAndScore.isGameEnd():
            self.state = 3
            print(self.dao.updateScoreData(self.musicVO.getMusicNum(), self.hpAndScore.score))
    
    def gameOver(self):
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont("arial", 100, bold=True, italic=False)
        text1 = font.render("Game Over", True, colorSampleDict["white"])
        font = pygame.font.SysFont("arial", 50, bold=True, italic=False)
        text2 = font.render("return", True, colorSampleDict["white"])
        screen.blit(text1, (1920 / 2 - 200, 1080 / 4))
        posX, posY = int((1920 / 2) - 30), int((1080 / 4) * 3)
        screen.blit(text2, (posX, posY))
        # print("go")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                if int(mouseX) in range(920, 1060) and int(mouseY) in range(820, 860):
                    return "backToChoice"
        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            if int(mouseX) in range(920, 1060) and int(mouseY) in range(820, 860):
                return "backToChoice"
    
    def getKeysAndEvents(self):
        self.keys = pygame.key.get_pressed()
        self.events = pygame.event.get()
        
    def getNotes(self):
        # print(self.dao.getNoteData(self.musicVO.getMusicNum()))
        self.notes = self.dao.getNoteData(self.musicVO.getMusicNum())
    
    def createNoteArr(self):
        playTime = pygame.mixer.music.get_pos()
        deleteNoteArr = []
        for note in self.notes:
            ms, tracks = note.split(":")
            if int(ms) <= playTime:     
                deleteNoteArr.append(note)
                for track in tracks:
                    self.noteArr[int(track) - 1].append(Note(int(track) - 1, colorSampleDict["note"]))
        self.deleteNote(deleteNoteArr)
        
    def deleteNote(self, notes):
        for note in notes:
            self.notes.remove(note)
    
    def gameOverCheck(self):
        # for event in self.events:
        #     if event.type == self.endEvent:
        #         self.state += 1
        if self.hpAndScore.isGameEnd():
            pygame.mixer.music.stop()
            self.state = 4
       
    def mainFunction(self):
        # print(self.state)
        if self.state == 1: # 초기 세팅
            self.start() 
        elif self.state == 2: # 플레이 중
            self.playing()
        elif self.state == 3: # 점수 표시
            event = self.showScore()
            if event == "backToChoice":
                return event
        elif self.state == 4: # 게임 오버
            event = self.gameOver()
            if event == "backToChoice":
                return event
        else:
            pass
            
class ClickBox():
    def __init__(self, railNum):
        self.railNum = railNum # 레일 넘버
        self.width = 100 # 상자 넓이
        self.height = 50 # 상자 높이
        self.isClicked = False # 키를 눌렀는가 눌렀는가
        self.border = 5 # 테두리 두께
        self.boxColor = colorSampleDict["white"]
        self.clickBoxIndexY = 1080 - int(1080 * 0.2) # 상자 위치 Y 설정
        self.clickCount = 0
        # 상자 위치 X 설정
        self.clickBoxIndexX = getXIndexWithRailNum(self.railNum, self.width)
        if railNum == 0:
            self.eventKey = pygame.K_s
        elif railNum == 1:
            self.eventKey = pygame.K_d
        elif railNum == 2:
            self.eventKey = pygame.K_k
        elif railNum == 3:
            self.eventKey = pygame.K_l
        else:
            self.eventKey = pygame.K_s
        
    """
    def clickboxImageChange(self, key): #노트 바닥 이미지 변경
        image1 = pygame.image.load("노트바닥.png")
        image2 = pygame.image.load("노트 바닥 이펙트.png")
        if key[self.eventkey] != 1:
            self.blit(image1)
        if key[self.eventkey] == 1:
            self.blit(image2)
    """
    
    def resetAfterFrame(self): # 1프레임 마다 초기화
        self.isClicked = False
        self.boxColor = colorSampleDict["white"]
        
    def checkBoxEvent(self, key): # 키 입력 이벤트
        if key[self.eventKey] == 1:
            self.isClicked = True
            self.boxColor = colorSampleDict["gray"]
            self.clickCount += 1
            if self.clickCount == 1:
                return True
            else:
                return False
        else: # 수정본
            self.clickCount = 0
            # if self.clickCount == 1:
            #     global railBoxArr
            #     if len(railBoxArr[self.railNum]) > 0:
            #         railBoxArr[self.railNum][0].checkHeightForScore(self.clickBoxIndexY, self.height, level)
            #         del railBoxArr[self.railNum][0]
            #     else:
            #         pass
    
    def clickCountReset(self, key):
        if key == self.eventKey:
            self.clickCount = 0
            
    def getBoxColor(self): # 상자 색깔 반환
        return self.boxColor
    
    def getBoxPos(self): # 상자 위치 반환
        return (self.clickBoxIndexX, self.clickBoxIndexY, self.width, self.height)
    
    def getBoxBorder(self): # 상자 테두리 두께 반환
        return self.border     
    
    def getEventState(self):
        return self.isClicked

class Note():
    def __init__(self, railNum, boxColor):
        self.railNum = railNum # 레일 넘버
        self.width = 100 # 상자 넓이
        self.height = 50 # 상자 높이
        self.boxColor = boxColor # 상자 색깔
        self.noteIndexY = 0 - self.height # 상자 위치 Y 설정
        self.noteIndexX = getXIndexWithRailNum(railNum, self.width) # 상자 위치 X 설정
        self.boxSpeed = 300 # 초당 움직이는 픽셀
    """
    def noteImageChange(self): #내려오는 노트의 이미지 변경
        image = pygame.image.load("노트.png")
        self.blit(image)
    """
    def moveDown(self, fps):
        self.noteIndexY = self.noteIndexY + int(self.boxSpeed / fps)
        return self.getIsNoteOutOfScreen()
        # if self.getIsNoteOutOfScreen():
        #     hpAndScoreData.calcScore("Miss", level)
        #     for i in range(len(railBoxArr)):
        #         arr = railBoxArr[i]
        #         if self in arr:
        #             arr.remove(self)
        #             railBoxArr[i] = arr
        #             break
        
    def getIsNoteOutOfScreen(self):
        if self.noteIndexY >= 1080:
            return True
        else:
            return False
    
    def checkHeightForScore(self, clickBoxIndexY, clickBoxHeight):
        boxY1 = clickBoxIndexY
        boxY2 = clickBoxIndexY + clickBoxHeight
        Y1 = self.noteIndexY
        Y2 = self.noteIndexY + self.height
        if Y1 >= boxY1 - int(clickBoxHeight * 0.2) and Y2 <= boxY2 + int(clickBoxHeight * 0.2):
            return "Excellent"
        elif Y1 >= boxY1 - int(clickBoxHeight * 0.4) and Y2 <= boxY2 + int(clickBoxHeight * 0.4):
            return "Great"
        elif Y1 >= boxY1 - int(clickBoxHeight * 0.6) and Y2 <= boxY2 + int(clickBoxHeight * 0.6):
            return "Good"
        else:
            return "Miss"
        
    def getBoxColor(self): # 상자 색깔 반환
        return self.boxColor
    
    def getBoxPos(self): # 상자 위치 반환
        return (self.noteIndexX, self.noteIndexY, self.width, self.height)
    
class HpAndScore():
    def __init__(self):
        self.hp = 100
        self.score = 0
        self.combo = 0
    
    def resetValueAfterGameEnd(self):
        self.__init__
        
    def decreaseHp(self):
        self.hp -= 5
        if self.hp <= 0:
            self.hp = 0  
    
    def calcScore(self, state):
        value = 0
        if state == "Excellent":
            value = 50
        elif state == "Great":
            value = 20
        elif state == "Good":
            value = 10
        elif state == "Miss":
            value = 0
        else:
            value = 0
        if value == 0:
            self.decreaseHp()
            self.combo = 0
        else:
            self.combo += 1
        self.score += value + self.combo
    
    def getHpAndScore(self):
        return f"HP : {self.hp} | SCORE : {self.score}"
    
    def getHp(self):
        return self.hp
    
    def isGameEnd(self):
        if self.hp <= 0:
            return True
        else:
            return False
    
    def getScore(self):
        score = str(self.score)
        if len(score) <= 7:
            score = ("0" * (7 - len(score))) + score
        return score
        
    def scoreOnScreen(self):
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont("arial", 30, bold=True, italic=False)
        score = str(self.score)
        if len(score) <= 7:
            score = ("0" * (7 - len(score))) + score
        text = font.render(score, True, colorSampleDict["white"])
        screen.blit(text, (1800, 10))
    
    def comboOnScreen(self):
        screen = pygame.display.get_surface()
        if self.combo != 0:
            font = pygame.font.SysFont("arial", 40, bold=True, italic=False)
            text = font.render(str(self.combo), True, colorSampleDict["white"])
            combo = font.render("COMBO", True, colorSampleDict["white"])
            screen.blit(combo, (1920 / 2 - 50, 1080 / 2 - 50))
            screen.blit(text, (1920 / 2, 1080 / 2))
    
    def resetCombo(self):
        self.combo = 0
    
    def createHpBoxWithGradient(self, screen, left_color, right_color, target_rect):
        # https://stackoverflow.com/questions/62336555/how-to-add-color-gradient-to-rectangle-in-pygame 참고함
        color_rect = pygame.Surface((2, 2))
        pygame.draw.line(color_rect, left_color, (0, 0), (0, 1))
        pygame.draw.line(color_rect, right_color, (1, 0), (1, 1))
        color_rect = pygame.transform.smoothscale(color_rect, (target_rect.width, target_rect.height))
        screen.blit(color_rect, target_rect)
        pygame.draw.rect(screen, colorSampleDict["black"], (10 + int(target_rect.width * (self.getHp() / 100)), 10, 300, 30))
        pygame.draw.rect(screen, colorSampleDict["white"], target_rect, 5) 
        pass
   
class AddTrackController():
    def __init__(self):
        self.musicVO = None
        self.noteArr = [] # 트랙 추가 함수
        self.keys = []
        self.status = 1
        self.clicked = [False, False, False, False]
        self.clickedTime = [0, 0, 0, 0]
        self.keyDict = {
            0 : "S",
            1 : "D",
            2 : "K",
            3 : "L"
        }
        self.dao = frw.DAO()
    
    def setting(self, musicVO):
        self.musicVO = musicVO
        try:
            pygame.mixer.music.load(frw.getFilePath(self.musicVO.getMusicPath(), "mp3"))
        except Exception as e:
            print(e)
        pygame.mixer.music.play()
        self.status = 2

    def musicPlaying(self):
        self.keys = pygame.key.get_pressed()
        self.pressedButtonCheck()
        self.clickBoxOnScreen()
        self.appendNote()
        self.clicked = [False, False, False, False]
        if not pygame.mixer.music.get_busy():
            self.status = 3

    def saveData(self): # 교체 예정 저장안되는중
        self.dao.addNoteData({"musicNum" : self.musicVO.getMusicNum(), "note" : self.noteArr})
        print(self.noteArr)
        return "returnChoice"
    
    def clickBoxOnScreen(self):
        y, w, h = 500, 250, 125
        screen = pygame.display.get_surface()
        for i, value in enumerate(self.clicked):
            x = 310 + (i * 250) + (i * 100)
            if value:
                pygame.draw.rect(screen, colorSampleDict["gray"], (x, y, w, h))
            else:
                pygame.draw.rect(screen, colorSampleDict["white"], (x, y, w, h))
            pygame.draw.rect(screen, colorSampleDict["skyblue"], (x, y, w, h), 10)
            font = pygame.font.SysFont("arial", 50, bold=True, italic=False)
            text = font.render(self.keyDict[i], True, colorSampleDict["black"])
            screen.blit(text, (x + 115, y + 30))
    
    def pressedButtonCheck(self):
        if self.keys[pygame.K_s] == 1:
            self.clicked[0] = True
            self.clickedTime[0] += 1
        elif self.keys[pygame.K_s] != 1:
            self.clickedTime[0] = 0
            
        if self.keys[pygame.K_d] == 1:
            self.clicked[1] = True
            self.clickedTime[1] += 1
        elif self.keys[pygame.K_d] != 1:
            self.clickedTime[1] = 0  
              
        if self.keys[pygame.K_k] == 1:
            self.clicked[2] = True
            self.clickedTime[2] += 1
        elif self.keys[pygame.K_k] != 1:
            self.clickedTime[2] = 0   
            
        if self.keys[pygame.K_l] == 1:
            self.clicked[3] = True
            self.clickedTime[3] += 1
        elif self.keys[pygame.K_l] != 1:
            self.clickedTime[3] = 0    
            
    def appendNote(self):
        text = ""
        for i, value in enumerate(self.clicked):
            if value and self.clickedTime[i] == 1:
                text += f"{i + 1}"
        if text != "":        
            self.noteArr.append(f"{pygame.mixer.music.get_pos()}:{text}")
    
    def mainFunction(self):
        if self.status == 1:
            self.setting()
        elif self.status == 2:
            self.musicPlaying()
        elif self.status == 3:
            status = self.saveData()
            if status == "returnChoice":
                return status
        else:
            pass
        
# 레일 번호 별로 X 좌표 반환
def getXIndexWithRailNum(railNum, width):
    if railNum == 0:
        return int(1920 / 2) - int(width * 2)
    elif railNum == 1:
        return int(1920 / 2) - width
    elif railNum == 2:
        return int(1920 / 2)
    elif railNum == 3:
        return int(1920 / 2) + width
    else:
        return int(1920 / 2) - int(width * 2)


colorSampleDict = {
    "white" : (255, 255, 255),
    "black" : (0, 0, 0),
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "orange" : (255, 140, 0),
    "yellow" : (255, 255, 0),
    "purple" : (255, 0, 255),
    "gray" : (162, 162, 162),
    "note" : (19, 115, 209),
    "skyblue" : (135, 206, 235),
    "" : (0, 0, 0)
} 

def main():
    try:
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        
        screen_width = 1920
        screen_height = 1080
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Rhythm")
        
        clock = pygame.time.Clock()
        fps = 60
        
        # vo = frw.musicVO()
        # vo.musicNum = 10000001
        # vo.musicPath = "AJR - World's Smallest Violin.mp3"
        # GC = GameController()
        # GC.start(vo)
        controller = Controller()
            
        isRunning = True 
        
        while isRunning:
            clock.tick(fps)
            screen.fill(colorSampleDict["black"])
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        isRunning = False
                        
            controller.mainFunction()
            
            pygame.display.update()
        
    except Exception as e:
        print("def main Error")
        print(e)
    finally:
        print("Game End")
        pygame.quit()
        sys.exit()
      


if __name__ == "__main__":
    main()















            # if currentState == 1:
            #     createStartScreen(screen, screen_width, screen_height)
            # elif currentState == 2:
            #     screen.fill(colorSampleDict["red"])
                
            #     pass
            # elif currentState == 3:
            #     screen.fill(colorSampleDict["blue"])
                
            #     pass
            # elif currentState == 4:
            #     screen.fill(colorSampleDict["black"])
                
            #     pass
            # elif currentState == 5:
            #     pass
            # else:
            #     currentState = 1
            #     pass
            
            # clickBoxColorArr = [colorSampleDict["white"], colorSampleDict["white"], colorSampleDict["white"], colorSampleDict["white"]]
            
            
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         isRunning = False
                    
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_ESCAPE:
            #             isRunning = False
                    
            #     if event.type == pygame.KEYUP:
            #         for obj in clickBoxArr:
            #             obj.clickCountReset(event.key)
            # index = 0 # 0 ~ 4            
            #     if event.type == pygame.MOUSEWHEEL:
            #         if event.y > 0:
            #             index -= 1
            #         elif event.y < 0:
            #             print("마우스 내리는 중")
            #             index += 1
            #         else:
            #             pass
            
            
            # isClickBoxClicked = [False, False, False, False]
            # key = pygame.key.get_pressed()
            # # print(key[pygame.K_s], key[pygame.K_d], key[pygame.K_j], key[pygame.K_k])
            # if key[pygame.K_s] == 1:
            #     isClickBoxClicked[0] = True
            #     clickBoxColorArr[0] = colorSampleDict["blue"]
            # if key[pygame.K_d] == 1:
            #     isClickBoxClicked[1] = True
            #     clickBoxColorArr[1] = colorSampleDict["blue"]
            # if key[pygame.K_j] == 1:
            #     isClickBoxClicked[2] = True
            #     clickBoxColorArr[2] = colorSampleDict["blue"]
            # if key[pygame.K_k] == 1:
            #     isClickBoxClicked[3] = True
            #     clickBoxColorArr[3] = colorSampleDict["blue"]
            # print(isClickBoxClicked)
            
            # """
            # key = pygame.key.get_pressed()
            # for i, obj in enumerate(clickBoxArr):
            #     obj.checkBoxEvent(key, level = 1)
            # """
            
            # 배열로 정리해서 모았다가 한번에 띄우는 방식으로 만들어야 할듯            
            # text, textRect = createSurfaceInScreen("Hello", 30, colorSampleDict["black"], colorSampleDict["white"], (screen_width / 2, screen_height / 2))
            # screen.blit(text, textRect)
            
            # clickBoxHeight = screen_height - screen_height * 0.2
            # clickBoxWidth = [(1920 / 2) - 350, (1920 / 2) - 150, (1920 / 2) + 50, (1920 / 2) + 250]
            # screenObjectArr = []
            
            # movingBoxPos = (clickBoxWidth[0], 0 - 50 + minusHeight, 100, 50)
            # pygame.draw.rect(screen, colorSampleDict["red"], movingBoxPos)
            # minusHeight += 5
            # if minusHeight > screen_height:
            #     minusHeight = 0
            
            # for i in range(4):
            #     screenObjectArr.append((clickBoxWidth[i], clickBoxHeight, 100, 50))
            # # pygame.draw.rect(screen, colorSampleDict["white"], (100, 100, 100, 100))
            # for i, j in enumerate(screenObjectArr):
            #     pygame.draw.rect(screen, clickBoxColorArr[i], j, 5)
            
            # """
            # for i, arr in enumerate(railBoxArr):
            #     if arr == []:
            #         arr.append(Note(i, 60, colorSampleDict["red"]))
            
            # for arr in railBoxArr: # [[obj, obj], [], [], []]
            #     for obj in arr:
            #         pygame.draw.rect(screen, obj.getBoxColor(), obj.getBoxPos())
            #         obj.moveDown(fps, level = 1)
            
            # for obj in clickBoxArr:
            #     pygame.draw.rect(screen, obj.getBoxColor(), obj.getBoxPos(), obj.getBoxBorder())
            #     obj.resetAfterFrame()
            
            # # print(hpAndScoreData.getHpAndScore())
            # hpAndScoreData.createHpBoxWithGradient(screen, colorSampleDict["red"], colorSampleDict["yellow"], pygame.Rect(10, 10, 300, 30))
            # """