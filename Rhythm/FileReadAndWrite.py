import csv # https://docs.python.org/ko/3/library/csv.html
from pytube import YouTube
import ffmpeg # subprocess로 ffmpeg 사용 (아마 이 모듈은 코드상에선 안 쓸듯)
import os
import subprocess
import re # 정규표현식
import json # https://docs.python.org/ko/3/library/json.html

# 파일 경로 찾기
def getFilePath(fileName, fileType):
    try:
        dirPath = os.path.dirname(__file__)
        folderName = ""
        if fileType == "ttf":
            folderName = "font\MaruBuriTTF"
        elif fileType == "png" or fileType =="jpg" or fileType == "img":
            folderName = "img"
        elif fileType == "mp3":
            folderName = "mp3"
        elif fileType == "data":
            folderName = "data"
        else:
            return "canNotFindFilePath"
        folderPath = os.path.join(dirPath, folderName)
        filePath = os.path.join(folderPath, fileName)
        return filePath
    except Exception as e:
        return "canNotFindFilePath"

# https://twpower.github.io/17-with-usage-in-python
# r : 읽기모드
# w : 쓰기모드
# a : 추가모드

class DAO():
    def __init__(self):
        self.filePathDict = {
            "" : "",
            "noteList" : getFilePath("noteList.txt", "data"),
            "musicInfo" : getFilePath("musicInfo.csv", "data")
        }

    def getMusicData(self):
        try:
            with open(self.filePathDict["musicInfo"], "r", encoding="UTF-8") as file:
                reader = csv.DictReader(file)
                arr = []
                for line in reader:
                    vo = musicVO()
                    vo.setMusicNum(line["musicNum"])
                    vo.setMusicPath(line["musicPath"])
                    vo.setMusicName(line["musicName"])
                    vo.setAuthorName(line["authorName"])
                    vo.setScore(line["score"])
                    arr.append(vo)
                return arr
        except Exception as e:
            print(e)
            return "fail"
    
    def lastAddedData(self):
        try:
            musicNum = self.getMaxMusicNum()
            if musicNum != "fail":
                musicNum = int(musicNum) - 1
                with open(self.filePathDict["musicInfo"], "r", encoding="UTF-8") as file:
                    reader = csv.DictReader(file)
                    vo = musicVO()
                    for line in reader:
                        if line["musicNum"] == str(musicNum):
                            vo.setMusicNum(line["musicNum"])
                            vo.setMusicPath(line["musicPath"])
                            vo.setMusicName(line["musicName"])
                            vo.setAuthorName(line["authorName"])
                            vo.setScore(line["score"])
                    return vo
            else:
                return "fail"
        except Exception as e:
            return "fail"
    
    def getNoteData(self, musicNum):
        try:
            if type(musicNum) is str:
                musicNum = int(musicNum)
            with open(self.filePathDict["noteList"], "r", encoding="UTF-8") as file:
                data = json.load(file)
                for i in data:
                    if i["musicNum"] == musicNum:
                        return i["note"]
                return "fail"
        except Exception as e:
            print("getNoteData |", e)
            return "fail"
        
    def addMusicData(self, musicVO):
        try:
            with open(self.filePathDict["musicInfo"], "a", encoding="UTF-8", newline="") as file:
                writer = csv.writer(file, delimiter=",", lineterminator="\r\n", quotechar="'")
                writer.writerow(musicVO.toString())
                print(musicVO.toString())
                return "success"
        except Exception as e: 
            print(e)
            return "fail"
        
    def getMaxMusicNum(self):
        try:
            with open(self.filePathDict["musicInfo"], "r", encoding="UTF-8") as file:
                reader = csv.DictReader(file)
                arr = []
                for line in reader:
                    num = line["musicNum"]
                    if type(num) is int:
                        arr.append(num)
                    else:
                        arr.append(int(num))
                return max(arr) + 1
        except Exception as e:
            print(e)
            return "fail"
        
    def getAllNoteData(self):
        try:
            with open(self.filePathDict["noteList"], "r", encoding="UTF-8") as file:
                data = json.load(file)
                return data
        except Exception as e:
            print("getNoteData |", e)
            return "fail"
    
    def addNoteData(self, data): # data 형식은 dictionary
        try:
            noteArr = self.getAllNoteData()
            if noteArr != "fail":
                for obj in noteArr:
                    if obj["musicNum"] == data["musicNum"]:
                        return "duplicateValue" # 중복값
                if type(data["musicNum"]) is str:
                    data["musicNum"] = int(data["musicNum"])
                noteArr.append(data)
                with open(self.filePathDict["noteList"], "w", encoding="UTF-8") as file:
                    json.dump(noteArr, file, indent=4)
                return "success"
            else:
                return "fail"
        except Exception as e:
            print("addScoreData |", e)
            return "fail"
    
    def isHighScore(self, musicNum, score):
        try:
            with open(self.filePathDict["musicInfo"], "r", encoding="UTF-8") as file:
                reader = csv.DictReader(file)
                for line in reader:
                    if line["musicNum"] == str(musicNum):
                        if int(line["score"]) < score:
                            return "highScore"
                        else:
                            return "noHighScore"
                return "noData"
        except Exception as e:
            return "fail"
        
    def updateScoreData(self, musicNum, score):
        status = self.isHighScore(musicNum, score)
        print(status)
        if status == "highScore":
            try:
                data = []
                with open(self.filePathDict["musicInfo"], "r", encoding="UTF-8") as file:
                    reader = csv.DictReader(file, delimiter=",")
                    for line in reader:
                        if line["musicNum"] == str(musicNum):
                            line["score"] = score
                        else:
                            line["score"] = int(line["score"])
                        line["musicNum"] = int(line["musicNum"])
                        line["musicPath"] = "\"" + line["musicPath"] + "\""
                        line["musicName"] = "\"" + line["musicName"] + "\""
                        line["authorName"] = "\"" + line["authorName"] + "\""
                        data.append(line)
                if data == []:
                    return "fail"        
                else:
                    fieldNames = ["musicNum", "musicPath", "musicName", "authorName", "score"]
                    with open(self.filePathDict["musicInfo"], "w", encoding="UTF-8", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=fieldNames, lineterminator="\r\n", quotechar="'")
                        writer.writeheader()
                        for line in data:
                            writer.writerow(line)     
                        return "success"
            except Exception as e:
                return "faile"
        elif status == "noHighScore":
            return "noHighScore"
        else:
            return "fail"
    
class VideoDownloader():  
    def __init__(self):
        self.videoTitle = ""
        self.videoAuthor = ""
        self.musicNum = 0
        self.musicPath = ""
        self.dao = DAO()
    
    def __createFileNameWithTitleAndAuthor(self, authorStr, titleStr): # file명 생성
        # print("=== createFileNameWithTitleAndAuthor ===")
        filterWord = re.compile(r"[a-zA-Z]")
        value = ""
        for c in authorStr:
            if c == " ":
                value += ""
            elif filterWord.match(c):
                value += c        
        value += "-"
        for c in titleStr:
            if c == " ":
                value += ""
            elif filterWord.match(c):
                value += c
        return value + ".mp4"
    
    def __createMusicName(self, title):
        filterWord = re.compile(r"[a-zA-Z]")
        str = ""
        for word in title:
            if len(str) >= 25:
                str += "..."
                break
            if word == " ":
                str += " "
            elif filterWord.match(word):
                str += word
            else:
                str += "_"
        return str

    def __createAuthorName(self, authorName):
        filterWord = re.compile(r"[a-zA-Z]")
        str = ""
        for word in authorName:
            if filterWord.match(word):
                str += word
        if str == "":
            return "Unknown"
        else:
            return str

    def __getVideoFromYoutube(self, url): # 유튜브에서 영상 다운해서 mp3로 저장
        # https://pytube.io/en/latest/user/exceptions.html      pytube 
        # https://docs.python.org/3.9/library/subprocess.html   subprocess
        try:
            mp3FolderPath = ""
            dirPath = os.path.dirname(__file__)
            mp3FolderPath = os.path.join(dirPath, "mp3")
            # print(mp3FolderPath) 
            fileName = ""
            if "www.youtube.com/watch?v=" in url: # https://www.youtube.com/watch?v=_G4wz7vmH5E
                yt = YouTube(url)
                # print(yt.title) # 영상 제목
                # print(yt.author) # 영상 게시자
                # print(yt.thumbnail_url) # 썸네일 주소
                # yt.streams.first().download(mp3FolderPath)
                # fileName = f"{yt.author} - {yt.title}"
                self.videoAuthor = self.__createAuthorName(yt.author)
                self.videoTitle = self.__createMusicName(yt.title)
                fileName = self.__createFileNameWithTitleAndAuthor(yt.author, yt.title)
                self.musicPath = fileName[0:-3] + "mp3"
                # print(yt.description)
                
                yt_streams = yt.streams.filter(only_audio=True).first()
                targetFile = yt_streams.download(output_path=mp3FolderPath, filename=fileName) # 다운로드 된 파일 (mp4)
                print("Video Download Complete")
                command = "ffmpeg -i " + targetFile + " " + targetFile[0:-3] + "mp3"
                subprocess.run(command)
                os.remove(targetFile)
                
                return "success"
            elif "youtu.be/" in url: # https://youtu.be/_G4wz7vmH5E
                arr = url.split("/")
                str = f"www.youtube.com/watch?v={arr[len(arr) - 1]}"
                # print(str)
                return self.__getVideoFromYoutube(str)
            else:
                print("wrong url")
                return "urlError"
        except Exception as e:
            print(e)
            return "runningException"
        
    def getMusicVO(self):
        vo = musicVO()
        vo.setMusicName(self.videoTitle)
        vo.setAuthorName(self.videoAuthor)
        vo.setMusicNum(self.musicNum)
        vo.setMusicPath(self.musicPath)
        vo.setScore(0)
        return vo    

    def download(self, url):
        status = self.__getVideoFromYoutube(url)
        if status == "success":
            self.musicNum = self.dao.getMaxMusicNum()
            if self.musicNum == "fail":
                return "fail"
            else:
                vo = self.getMusicVO()
                status2 = self.dao.addMusicData(vo)
                return status2
            # 여기서 csv에 저장하는 코드 삽입 예정
        elif status == "runningException":
            return status
        elif status == "urlError":
            return status
        
       
class musicVO():
    def __init__(self):
        self.musicNum = ""
        self.musicPath = ""
        self.score = ""
        self.note = ""
        self.musicName = ""
        self.authorName = ""
    
    def getMusicNum(self):
        return self.musicNum

    def getAuthorName(self):
        return self.authorName
    
    def getScore(self):
        return self.score
    
    def getMusicName(self):
        return self.musicName

    def getMusicPath(self):
        return self.musicPath
    
    def toString(self):
        return self.musicNum, ("\"" + self.musicPath + "\""), ("\"" + self.musicName + "\""), ("\"" + self.authorName + "\""), self.score
    
    def setMusicNum(self, musicNum):
        self.musicNum = musicNum
    
    def setMusicPath(self, musicPath):
        self.musicPath = musicPath
        
    def setMusicName(self, musicName):
        self.musicName = musicName
    
    def setAuthorName(self, authorName):
        self.authorName = authorName
    
    def setScore(self, score):
        self.score = score

    
        
 
# 코드 테스트용
def main():
    # dao = DAO()
    # print(dao.updateScoreData(10000001, 10))
    # vo = musicVO()
    # vo.setAuthorName("sample")
    # vo.setMusicName("sample1")
    # vo.setMusicNum(dao.getMaxMusicNum())
    # vo.setMusicPath("sample")
    # vo.setScore(0)
    # dao.addMusicData(vo)
    # print(dao.getMusicData())
    # arr = dao.getMusicData()
    # for i in arr:
    #     print(i.toString())
    # print(dao.getNoteData(10000001))
    # print(dao.addNoteData({'musicNum': 10000002, 'note': ["111:1", "1234:1234"]}))
    # dao.getMusicData()
    # dao.getNoteData()
    # dao.saveNoteDataToCSV(12)   
        
    # vd = VideoDownloader()
    # vd.download("https://www.youtube.com/watch?v=cHHLHGNpCSA")
    # command = getVideoFromYoutube("https://www.youtube.com/watch?v=_G4wz7vmH5E")

    
    # if command == "":
    #     pass
    # elif command == "":
    #     pass
    # else:
    #     try :
    #         print("convertFileToMp3")
    #         print(command)
    #         subprocess.run(command)           
    #     except Exception as e:
    #         print(e)
    pass

    
if __name__ == "__main__":
    main()