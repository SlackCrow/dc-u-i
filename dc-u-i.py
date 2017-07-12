#!/usr/bin/python3
#Licensed under the 2-Clause BSD License
# 0.0000233333333333333 b
#Slack Crow 2017

import csv
import sys
import os
import requests
import json
import time

currentBoard = ""
currentPage = 0
currentThread = 0
currentPost = 0

#clears the current console
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def printTop():
    global currentBoard
    global currentPage
    print("----------------------------------")
    print("-----Welcome to Danger/u/ BBS-----")
    print("----------------------------------")
    print("Interests                    Misc.")
    print("")
    print("Anime & Manga(a)         Random(u)")
    print("Cyberpunk(cyb)          Burg(burg)")
    print("Doujin(d)                News(new)")
    print("music(mu)")
    print("Technology(tech)")
    print("Video Games(v)")
    print("")
    print("Goto?")
    currentBoard = input()
    currentPage = 0
    clear()
def getBoard():
    jsonReceived = requests.get("https://boards.dangeru.us/api.php?type=index&board=" + currentBoard + "&ln=" + "250")
    jsonReceived = jsonReceived.text.replace('\n', ' ').replace('\r', '')
    return jsonReceived

def getBoardName(boardID):
    if boardID == "a":
        return "Anime & Manga"
    elif boardID == "cyb":
        return "Cyberpunk"
    elif boardID == "d":
        return "Doujin"
    elif boardID == "tech":
        return "Technology"
    elif boardID == "v":
        return "Video Games"
    elif boardID == "u":
        return "Random"
    elif boardID == "burg":
        return "Burg"
    elif boardID == "new":
        return "News"
    else:
         return "null"

def getThread():
    jsonReceived = requests.get("https://boards.dangeru.us/api.php?type=thread&board=" + currentBoard + "&ln=" + "100" + "&thread=" + str(currentThread))
    jsonReceived = jsonReceived.text.replace('\n', ' ').replace('\r', '')
    return jsonReceived

def printCurrent():
    print("You are now at... "+ getBoardName(currentBoard))
    print("Page "+str(currentPage+1))

def printThread():
    global currentPost
    processedFetch = json.loads(getThread())
    print("----------------------------------")
    print("Title:" + processedFetch["meta"][0]["title"])
    print("----------------------------------")
    i = 9*currentPost
    while i < len(processedFetch["replies"]) and i < 9*(currentPost+1):
        print("- "+processedFetch["replies"][i]["post"])
        i = i + 1
    print("----------------------------------")
    print("next(n)/before(b)/return(r)/write(w)")
    toDo = input()
    if toDo[0] == "r":
        clear()
        printBoard()
    elif toDo[0] == "n":
        currentPost = currentPost + 1
        clear()
        printThread()
    elif toDo[0] == "b":
        if currentPost == 0:
            print("There is no previous page")
        else:
            currentPost = currentPost - 1
        clear()
        printThread()
    elif toDo[0] == "w":
        postComment()
    else:
        print("error")

def postThread():
    clear()
    print("Title")
    print("----------------------------------")
    title = input()
    clear()
    print("Body")
    print("\"#submit\" to submit")
    print("----------------------------------")
    userInput = input()
    body = userInput
    while (not(userInput == "#submit")):
        userInput = input()
        if not userInput == "#submit":
            body = body + "/n" + userInput
    body = body.replace(" ","%20")
    title = title.replace(" ","%20")
    requests.get("https://boards.dangeru.us/api.php?type=post&board=" + currentBoard + "&title=" + title + "&body=" + body)
    clear()
    printBoard()

def postComment():
    print("\"#submit\" to submit")
    print("----------------------------------")
    userInput = input()
    body = userInput
    while (not(userInput == "#submit")):
        userInput = input()
        if not userInput == "#submit":
            body = body + "/n" + userInput
    body = body.replace(" ","%20")
    requests.get("https://boards.dangeru.us/api.php?type=comment&board=" + currentBoard + "&thread=" + str(currentThread) + "&body=" + body)
    clear()
    printThread()

def printBoard():
    global currentThread
    global currentPage
    threadList = json.loads(getBoard())
    printCurrent()
    i = 9*currentPage
    print("----------------------------------")
    while i < len(threadList[u'threads']) and i < 9*(currentPage+1):
        print(str(i)+". "+ threadList[u'threads'][i][u'title'])
        i = i + 1
    print("----------------------------------")
    print("goto(g) <>/next(n)/before(b)/top(t)/write(w)")
    toDo = input()
    if toDo[0] == "g":
        clear()
        currentThread = threadList[u'threads'][int(toDo[2:])][u'id']
        printThread()
    elif toDo[0] == "t":
        main()
    elif toDo[0] == "n":
        currentPage = currentPage + 1
        clear()
        printBoard()
    elif toDo[0] == "n":
        currentPage = currentPage + 1
        clear()
        printBoard()
    elif toDo[0] == "b":
        if currentPage == 0:
            print("There is no previous page")
        else:
            currentPage = currentPage - 1
        clear()
        printBoard()
    elif toDo[0] == "w":
        postThread()
    else:
        print("error, returing to top")
        main()

def main():
    clear()
    printTop()
    printBoard()

main()
