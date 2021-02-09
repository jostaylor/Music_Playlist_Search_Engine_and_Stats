# This program finds different statistics about Dueber and David's Daily Jams

import tkinter
import math
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


# Asks user where they are
'''
location = 0
while location != 1 and location != 2 and location != 3 and location != 4:
    location = int(input("Are you at\n1)The School\n2)Your moms house\n3)On your laptop"))
    if location == 1:
        # Opens folder
        jamList = open("H:\\PythonStuff\\CanopyFiles\\JamList.txt", "r")

    elif location == 2:
        # Opens folder
        jamList = open("C:\\Users\\Josh\\Desktop\\Everything\\Music and Movies\\JamList.txt", "r")

    elif location == 3:
        # Opens folder
        jamList = open("C:\\Users\\josha\\Desktop\\Everything\\Music and Movies\\JamList.txt", "r")

    else:
        print("Please choose one of the options listed")
    print(location)
'''

# Above code has been removed because the text file is now in the same folder (for Github)
jamList = open("JamList.txt", "r")

# Declares empty arrays
songNames = []
songArtists = []
songLengths = []
songDateAdded = []

'''Reads the jam list file and inserts data into arrays'''

# Iterates through file and adds file info to the arrays
count = 0
for line in jamList:
    if count == 0:
        songNames.append(line)
    elif count == 1:
        songArtists.append(line)
    elif count == 2:
        songLengths.append(line)
    elif count == 3:
        songDateAdded.append(line)

    if count < 4:
        count += 1
    else:
        count = 0


listOfJamsAndYears = open("C:\\Users\\josha\\Desktop\\Everything\\Music and Movies\\JamYearsFileCompleted.txt", "r")
yearCount = 0
songYears = []
for line in listOfJamsAndYears:
    if yearCount == 1:
        songYears.append(line)
    if yearCount >= 2:
        yearCount = 0
    else:
        yearCount += 1


'''Takes out the '\n' from each value in the arrays'''
# Loop that iterates through all 4 arrays
for i in range(len(songNames)):
    # Replaces song names
    fixedName = songNames[i].replace("\n", "")
    songNames[i] = fixedName

    # Replaces song artists
    fixedArtist = songArtists[i].replace("\n", "")
    songArtists[i] = fixedArtist

    # Replaces song lengths
    fixedLength = songLengths[i].replace("\n", "")
    songLengths[i] = fixedLength

    # Replaces song dates
    fixedDateAdded = songDateAdded[i].replace("\n", "")
    songDateAdded[i] = fixedDateAdded

    fixedYear = songYears[i].replace("\n", "")
    songYears[i] = fixedYear


def getDurationOfJamsBetween(startIndex, endIndex):

    # Iterates through the songLengths array and accumulates values
    totalSongTimeInSeconds = 0
    for i in range(endIndex-startIndex):
        minutes = int(songLengths[startIndex+i][0])
        seconds = int(songLengths[startIndex+i][2:])
        songDurationInSeconds = (minutes*60) + seconds
        totalSongTimeInSeconds += songDurationInSeconds

    # Calculates extra time in minutes and seconds
    totalSongTimeInHours = float(totalSongTimeInSeconds) / 3600
    totalSongTimeExtraMinutes = totalSongTimeInHours - int(totalSongTimeInHours)
    totalSongTimeExtraMinutes *= 60
    totalSongTimeExtraSeconds = totalSongTimeExtraMinutes - int(totalSongTimeExtraMinutes)
    totalSongTimeExtraSeconds *= 60

    # Converts to integers; these are the correct values
    totalSongTimeInHours = int(totalSongTimeInHours)
    totalSongTimeExtraMinutes = int(totalSongTimeExtraMinutes)
    totalSongTimeExtraSeconds = int(totalSongTimeExtraSeconds)

    # Puts values into array
    totalDuration = [totalSongTimeInHours, totalSongTimeExtraMinutes, totalSongTimeExtraSeconds]
    return totalDuration


'''Finds average length of the jams'''

# Gets total time in hours
totalMinutes = getDurationOfJamsBetween(0, len(songLengths))[1] + \
               (float(getDurationOfJamsBetween(0, len(songLengths))[2]) / 60)
totalTimeInHours = getDurationOfJamsBetween(0, len(songLengths))[0] + totalMinutes / 60

# Gets average length of jams
totalTimeInSeconds = totalTimeInHours * 3600
averageJamLengthInSeconds = totalTimeInSeconds / len(songLengths)
averageJamLengthInSeconds /= 60  # Average length of jam in minutes
aslString = str(averageJamLengthInSeconds)

# Converts to string to isolate decimal to and converts to minute and seconds form
extraAverageSeconds = aslString[1:]
totalExtraAverageSeconds = float(extraAverageSeconds) * 60  # Average length (seconds)
totalAverageMinutes = int(aslString[:1])  # Average length (minutes)

'''Sorts the jams in order of length'''

# Puts the song lengths array into seconds
songLengthsInSeconds = []
for time in songLengths:
    minutes = time[:1]
    seconds = int(minutes) * 60
    seconds += int(time[2:])
    songLengthsInSeconds.append(seconds)

# Sorts the indexes of the song lengths array
songLengthIndexes = sorted(list(range(len(songLengthsInSeconds))), key=lambda k: songLengthsInSeconds[k])

# Sorts the jam titles in a new array
songNamesSortedByTime = []
for i in range(len(songNames)):
    songNamesSortedByTime.append(songNames[songLengthIndexes[i]])

# Sorts the jam lengths in a new array
songLengthsSortedByTime = []
for i in range(len(songLengths)):
    songLengthsSortedByTime.append(songLengths[songLengthIndexes[i]])

'''Sorts the jams in order of the amount of songs each artist has on jams'''

# Sorts the artist alphabetically
songArtistsSorted = sorted(songArtists)

# Puts them into a array without repeats and finds how many song each artist has
artistWithoutRepeats = []  # Each item is a list of two values: [song artist, how many songs]
for artist in songArtistsSorted:  # Iterates through all the songs
    for newArtist in artistWithoutRepeats:  # Iterates through all songs already iterated
        if newArtist[0] == artist:
            newArtist[1] += 1
            break
    else:
        artistWithoutRepeats.append([artist, 1])

# Sorts artistWithoutRepeats array by the amount of songs each artist has

for i in range(len(artistWithoutRepeats)-1, 0, -1):
    for j in range(i):
        if artistWithoutRepeats[j][1] < artistWithoutRepeats[j+1][1]:
            temp = artistWithoutRepeats[j+1]
            artistWithoutRepeats[j+1] = artistWithoutRepeats[j]
            artistWithoutRepeats[j] = temp


'''Sorts the jams into what year they were released chronologically'''

# Sorts indexes of songYears array (puts them in order)
songYearsIndexes = sorted(list(range(len(songYears))), key=lambda k: songYears[k])
#print songYearsIndexes
# Sorts song names into a new array
songNamesSortedByYear = []
for i in range(len(songYears)):
    songNamesSortedByYear.append(songNames[songYearsIndexes[i]])

# Sorts song years into a new array
songYearsSortedByYear = []
for i in range(len(songYears)):
    songYearsSortedByYear.append(songYears[songYearsIndexes[i]])

# Finds which year has the most jams
# PRACTICALLY USELESS NOT SINCE I KNOW THE ANSWER
mostYears = 0
mostYearsYear = 0
currentYearCount = 1
for i in range(len(songYearsSortedByYear)):

    if i == 0:
        currentYear = songYearsSortedByYear[i]
        mostYears += 1
        currentYearCount = 1
    else:
        if songYearsSortedByYear[i] == songYearsSortedByYear[i-1]:
            currentYearCount += 1
        else:
            currentYearCount = 1
    if currentYearCount > mostYears:
        mostYears += 1
        mostYearsYear = songYearsSortedByYear[i]

'''Calculates other info about the jams in relation to the year a song was released'''

# Calculates average year
bigAssInt = 0
for i in range(len(songYears)):
    bigAssInt += int(songYears[i])
jamAvgYear = bigAssInt / len(songYears)

# Gets median year
jamMedianYear = songYearsSortedByYear[int(((len(songYearsSortedByYear)) / 2) + 0.5)]

# Calculates how many songs there are from each decade
jamsReleasedInThe60s = []
jamsReleasedInThe70s = []
jamsReleasedInThe80s = []
jamsReleasedInThe90s = []
jamsReleasedInThe00s = []

for i in range(len(songNames)):
    if songYears[i][2] == '6':
        jamsReleasedInThe60s.append([i+1, songNames[i], songYears[i]])
    if songYears[i][2] == '7':
        jamsReleasedInThe70s.append([i+1, songNames[i], songYears[i]])
    if songYears[i][2] == '8':
        jamsReleasedInThe80s.append([i + 1, songNames[i], songYears[i]])
    if songYears[i][2] == '9':
        jamsReleasedInThe90s.append([i+1, songNames[i], songYears[i]])
    if songYears[i][2] == '0':
        jamsReleasedInThe00s.append([i+1, songNames[i], songYears[i]])


'''Finds how often a jam is added to the playlist during different eras'''

def getRateJamsWereAdded(firstDateIndex, lastDateIndex):
    """Finds the rate the jams were added between two points.
    Returns a list with two value [rate, totalDays]"""
    # NOTE: Pre-summer jams are jams 1-46. Summer jams are 47-81. The new school year is 82-present

    # Gets the first and last date
    firstDate = songDateAdded[firstDateIndex]
    lastDate = songDateAdded[lastDateIndex]

    # Finds the difference in time between the first and last dates
    years = int(lastDate[:4]) - int(firstDate[:4])
    months = int(lastDate[5:7]) - int(firstDate[5:7])
    days = int(lastDate[8:]) - int(firstDate[8:])

    # Converts the total time into days
    totalDays = 0
    totalDays += (years * 365.25)
    totalDays += (months * 30.42)
    totalDays += days

    # Gets the final rate
    jamAddedRate = totalDays / ((lastDateIndex - firstDateIndex) + 1)

    return [jamAddedRate, totalDays]

'''Organizes the jams based on David's and Ethan's Jams'''

# Iterates through the songNames and put them into two lists
ethansJams = []
davidsJams = []
for i in range(len(songNames)):
    # Adds Take Me Home Tonight to both lists because it was a mutual jam
    if i == 0:
        ethansJams.append(songNames[i])
        davidsJams.append(songNames[i])
    elif i % 2 == 0:
        davidsJams.append(songNames[i])
    else:
        ethansJams.append(songNames[i])

'''Makes the search engine where one can search a jam or an artist and find info'''


def searchEngine(inpt):
    # Creates empty lists and puts input to lowercase
    songResults = []
    artistResults = []
    inpt = inpt.lower()

    # Goes through song names
    for i in range(len(songNames)):  # Iterates through all the songs
        for j in range(0, len(songNames[i]) - (len(inpt) - 1)):   # Iterates through each character of the song, but
            # subtracts the length of the input to avoid an index out of range error
            if songNames[i][j:(j+len(inpt))].lower() == inpt:   # Checks to see if the section (that is the length of
                # the input) is the same of the input
                songResults.append(songNames[i])  # Adds to the results
                break

    # Goes through artist names (copy and paste of above)
    for i in range(len(songArtists)):  # Iterates through all the artists
        for j in range(0, len(songArtists[i]) - (len(inpt) - 1)):   # Iterates through each character of the artist,
            # but subtracts the length of the input to avoid an index out of range error
            if songArtists[i][j:(j+len(inpt))].lower() == inpt:   # Checks to see if the section (that is the length
                # of the input) is the same of the input
                for result in artistResults:  # Iterates through results. This process gets rid of artist repeats
                    if songArtists[i] == result:
                        break
                else:
                    artistResults.append(songArtists[i])  # Adds to the results
                    break

    # Combines the two results arrays
    totalResults = []
    for song in songResults:
        totalResults.append(song)
    for artist in artistResults:
        totalResults.append(artist)

    if len(totalResults) == 0:
        print("\nNo results were returned")
        print("Please input again")
        response = input("")
        if response.lower() == 'end':
            return None
        else:
            searchEngine(response)

    # Prints all the results
    print("\nHere are the results. Enter the number of the jam or artist you would like to search.")
    print("Jams:")
    for i in range(len(songResults)):
        print("%d: %s" % (i+1, songResults[i]))
    if len(songResults) == 0:
        print("No results")

    print("\nArtists:")
    for i in range(len(artistResults)):
        print("%d: %s" % (len(songResults) + i+1, artistResults[i]))
    if len(artistResults) == 0:
        print("No results")

    # Handles input and runs one of the getInfo methods
    while True:
        response = int(input("\n"))
        if len(songResults) >= response > 0:
            getSongInfo(totalResults[response - 1])
            break
        elif len(songResults) < response <= len(totalResults):
            getArtistInfo(totalResults[response - 1])
            break
        else:
            print('Please enter a valid value.')


def getSongInfo(song):
    """Gets this info: The artist, the duration of the song, who it was added
    by, the date it was added, the number jam it is, how long the jams were when
    this song was added, the jams added before and after this jam, the other
    jams by that artist"""

    # Gets song index
    songIndex = 0
    for i in range(len(songNames)):
        if song == songNames[i]:
            songIndex = i
            break

    # Gets song duration
    songLength = songLengths[songIndex]
    songDurationInMinutes = int(songLength[0])
    songDurationInSeconds = int(songLength[2:])

    # Gets the date and who added it
    if songIndex % 2 == 0:
        whoAddedSong = "David"
    else:
        whoAddedSong = "Ethan"
    dateSongAdded = songDateAdded[songIndex]

    # Gets other songs by that artist
    artist = songArtists[songIndex]
    otherSongsByArtist = ""
    for i in range(len(songArtists)):
        if i == songIndex:
            continue
        elif songArtists[i] == artist:
            otherSongsByArtist += "%s, " % songNames[i]
    otherSongsByArtist = otherSongsByArtist[:-2]

    # Prints information
    print(song)
    print("Artist: %s" % songArtists[songIndex])
    print("Released: %s" % songYears[songIndex])
    print("Duration: %d minutes and %d seconds" % (songDurationInMinutes, songDurationInSeconds))
    print("Jam #%d" % (songIndex + 1))
    print("Added by: %s" % whoAddedSong)
    print("Date Added: %s" % dateSongAdded)
    print("Other jams by %s: %s" % (artist, otherSongsByArtist))
    print("Duration of the jams after song was added: %d hours, %d minutes, and %d seconds" % \
          (getDurationOfJamsBetween(0, songIndex + 1)[0], getDurationOfJamsBetween(0, songIndex + 1)[1],
           getDurationOfJamsBetween(0, songIndex + 1)[2]))
    # These if statements prevent errors involving the first and last jams
    if songIndex != 0:
        print("Song that came before %s: %s" % (song, songNames[songIndex-1]))
    if songIndex != len(songNames) - 1:
        print("Song that came after %s: %s" % (song, songNames[songIndex+1]))
    else:
        print("Fun Fact: This is the most recently added jam!")

    # Prints prompt for next search
    print("\nSearch for another jam or artist.. (Enter \'end\' to quit to the main menu)")
    response = input("")
    if response.lower() != 'end':
        searchEngine(response)

def getArtistInfo(artist):
    """Gets the info: How many jams the artist has, what the jams are and their
    dates added and duration, who added each jam of this artist, the amount of
    time in days between each jam, """

    songsByArtist = []
    songDurationsByArtist = []
    songDatesAddedByArtist = []
    whoAddedSongByArtist = []
    songIndexesByArtist = []

    for i in range(len(songArtists)):
        if songArtists[i] == artist:

            songsByArtist.append(songNames[i])
            songDurationsByArtist.append(songLengths[i])
            songDatesAddedByArtist.append(songDateAdded[i])
            songIndexesByArtist.append(i)

            if i % 2 == 0:
                whoAddedSongByArtist.append("David")
            else:
                whoAddedSongByArtist.append("Ethan")

    # Makes new duration list that is a list of lists with 2 values (minutes and seconds for each value
    songDurationsByArtist2dList = []  # [Minutes, seconds]
    for time in songDurationsByArtist:
        songDurationsByArtist2dList.append([int(time[0]), int(time[2:])])

    # Prints the information
    print("%s has %d song(s):" % (artist, len(songsByArtist)))
    for i in range(len(songsByArtist)):
        print("%s:" % songsByArtist[i])
        print("\tJam #%d" % (songIndexesByArtist[i]))
        print("\tJam Added by: %s" % (whoAddedSongByArtist[i]))
        print("\tDuration: %d minutes and %s seconds" % (songDurationsByArtist2dList[i][0],
                                                         songDurationsByArtist2dList[i][1]))
        print("\tReleased: %s" % songYears[songIndexesByArtist[i]])
        print("\tDate Added: %s" % (songDatesAddedByArtist[i]))

    # Prints prompt for next search
    print("\nSearch for another jam or artist.. (Enter \'end\' to quit to the main menu)")
    response = input("")
    if response.lower() != 'end':
        searchEngine(response)

'''Tkinter code'''
'''
window = Tkinter.Tk()

inputString = Tkinter.StringVar()
inputString.set("")
speed_intvar = Tkinter.IntVar()
speed_intvar.set(5)

stopAnimation = Tkinter.BooleanVar()
stopAnimation.set(False)

direction = 0.5


def stopAnimate():
    stopAnimation.set(True)

# Creates the layout
jam_entry = Tkinter.Entry(window, textvariable=inputString)
jam_entry.grid(row=1, column=3)

entry_label = Tkinter.Label(window, text="Input a jam or artist here:")
entry_label.grid(row=0, column=3)

search_button = Tkinter.Button(window, text='Search', command=stopAnimate)
search_button.grid(row=1, column=4)

canvas = Tkinter.Canvas(window, width=500, height=500, background="black")
canvas.grid(row=2, column=1, columnspan=5)

theJamsLogoBackground = canvas.create_rectangle(200, 250, 362, 300, fill="black")
theJamsLogoText = canvas.create_text(280, 280, text="THE JAMS", font=("Comic Sans", 25), fill='blue')

# Animates the Jams logo
def animateLogo():
    # Get the slider data and create x- and y-components of velocity
    velocity_x = speed_intvar.get() * math.cos(direction)  # adj = hyp*cos()
    velocity_y = speed_intvar.get() * math.sin(direction)  # opp = hyp*sin()

    # Change the canvas item's coordinates

    canvas.move(theJamsLogoText, velocity_x, velocity_y)
    canvas.move(theJamsLogoBackground, velocity_x, velocity_y)

    x1, y1, x2, y2 = canvas.coords(theJamsLogoBackground)
    global direction

    # If crossing left or right of canvas
    if x2 > canvas.winfo_width() or x1 < 0:
        direction = math.pi - direction  # Reverse the x-component of velocity
    # If crossing top or bottom of canvas
    if y2 > canvas.winfo_height() or y1 < 0:
        direction *= -1  # Reverse the y-component of velocity

    # Insert a break for when screen changes

    if stopAnimation.get() is 0:
        canvas.after(1, animateLogo)


animateLogo()

window.mainloop()
'''


'''Prints info and displays interface'''

# Prints options
choice = 0
while choice != 69:
    print("\nWhat would you like to know about the jams?")
    print("1) General Info")
    print("2) The Jams in chronological order")
    print("3) The Jams sorted by the song length")
    print("4) The Jams sorted by the amount of songs each artist has")
    print("5) The Jams sorted by who added each jam")
    print("6) Search info for a jam or an artist")
    print("7) The Jams sorted by year released")
    print("8) Search Years Online (cAreful here)")
    print("69) Exit")
    choice = int(input())
    print("")  # new line

    # Puts options with the print code
    if choice == 1:
        # Prints the info of the jams
        print("There are %d jams as of %s" % (len(songNames), songDateAdded[len(songDateAdded) - 1]))
        print("The total length of the jams is %d hours, %d minutes, and %d seconds." % \
              (getDurationOfJamsBetween(0, len(songLengths))[0], getDurationOfJamsBetween(0, len(songLengths))[1],
               getDurationOfJamsBetween(0, len(songLengths))[2]))
        print("The average jam is %d minutes and %d seconds" % (totalAverageMinutes, totalExtraAverageSeconds))
        print("Over %d days, 1 jam was added every %f days" % (getRateJamsWereAdded(0, len(songDateAdded) - 1)[1],
                                                              getRateJamsWereAdded(0, len(songDateAdded) - 1)[0]))
        # TODO the values above and below must be altered when the jams are no longer in session :_(

        schoolYearRate = (getRateJamsWereAdded(0, 45)[0] + getRateJamsWereAdded(81, len(songDateAdded) - 1)[0]) / 2
        print("\tDuring the school year, 1 jam was added every %f days." % schoolYearRate)
        print("\tHowever, during the summer (over the course of %d days), 1 jam was added every %f days"\
              % (getRateJamsWereAdded(46, 80)[1], getRateJamsWereAdded(46, 80)[0]))
        print("Amount of songs released in the 60s: %d" % (len(jamsReleasedInThe60s)))
        print("Amount of songs released in the 70s: %d" % (len(jamsReleasedInThe70s)))
        print("Amount of songs released in the 80s: %d" % (len(jamsReleasedInThe80s)))
        print("Amount of songs released in the 90s: %d" % (len(jamsReleasedInThe90s)))
        print("Amount of songs released in the 00s: %d" % (len(jamsReleasedInThe00s)))
        print("The years with the most songs on the Jams are 1970 and 1972, both with 17 jams")
        print("The average of all the years is the same as the median being %d" % (jamAvgYear))
        # TODO who (david and ethan) added songs from what years.

    elif choice == 2:
        for i in range(len(songNames)):
            print("%d. %s (%s)" % (i+1, songNames[i], songLengths[i]))

    elif choice == 3:
        for i in range(len(songNamesSortedByTime)):
            print("%s (%s)" % (songNamesSortedByTime[i], songLengthsSortedByTime[i]))

    elif choice == 4:
        for i in range(len(artistWithoutRepeats)):  # Iterates through each artist

            # Finds all the songs the artist has in the playlist
            songsOfArtist = []
            for artistIndex in range(len(songArtists)):
                if artistWithoutRepeats[i][0] == songArtists[artistIndex]:
                    songsOfArtist.append(songNames[artistIndex])

            # Puts all the songs in songsOfArtist into one string
            songsOfArtistString = ""
            for j in range(len(songsOfArtist)):
                if j < len(songsOfArtist)-1:
                    songsOfArtistString += "%s, " % (songsOfArtist[j])
                else:
                    songsOfArtistString += songsOfArtist[j]

            # Prints the final product
            print("%s[%d]:" % (artistWithoutRepeats[i][0], artistWithoutRepeats[i][1],))
            print(songsOfArtistString, "\n")

    elif choice == 5:
        # Prints David's Jams
        print("David's Jams")
        for i in range(len(davidsJams)):
            print("%d: %s" % ((i*2) + 1, davidsJams[i]))

        # Prints Ethan's Jams
        print("\nEthan's Jams")
        print("1: Take Me Home Tonight")
        for i in range(1, len(ethansJams)):
            print("%d: %s" % ((i*2), ethansJams[i]))

    elif choice == 6:
        searchEngine(input("Input a song or artist\n"))

    elif choice == 7:
        for i in range(len(songYears)):
            print("%d: %s (%s)" % (i+1, songNamesSortedByYear[i], songYearsSortedByYear[i]))

    elif choice == 8:

        '''Gets the year each song came out'''

        jamYearsFile = open('C:\\Users\\josha\\Desktop\\Everything\\Music and Movies\\JamYearsFile.txt', 'w')

        # Tracks the amount of time this damn process takes
        start_time = datetime.now()
        print(start_time)

        # Declares lists
        songYears = []
        yearsToCheck = []
        searchesThatDontWork = []

        # Loops through each song in songNames
        for i in range(len(songNames)):

            jamYearsFile.write(songNames[i])
            jamYearsFile.write("\n")

            # Forms a string that is safe and good to search via url
            songName = songNames[i].replace(" ", "_")
            songName = songName.replace("'", "")
            songName = songName.replace("(", "_")
            songName = songName.replace(")", "_")
            songName = songName.replace("&", "and")

            songArtist = songArtists[i].replace(" ", "_")
            songArtist = songArtist.replace("'", "")
            songArtist = songArtist.replace("(", "_")
            songArtist = songArtist.replace(")", "_")
            songArtist = songArtist.replace("&", "and")

            # Creates url
            url = "https://www.google.com/search?q=" + songName + '+by+' + songArtist

            # Web-scrapes the url via html
            r = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, "lxml")

            # print which song we are on and creates itWorked boolean
            print(i+1, url)
            itWorked = False

            # Finds the little pieces of html that most likely have the year
            for node in soup.find_all("span", "_tA"):
                year = node.contents
                year = str(year)

                # Narrows down to the year a little more
                if len(year) == 9:

                    # Checks to see if the song is from the 90s or 2000s and organizes them separately
                    if year[3] == '2' or year[5] == '9':
                        yearsToCheck.append([i+1, songNames[i], year[3:7]])
                        itWorked = True

                    # Effectively grabs the year and organizes it
                    doubleResultCheckerThatIsSupposedToFixit = False
                    if year[3] == '1' or year[3] == '2':  # This finds the year

                        if doubleResultCheckerThatIsSupposedToFixit is True:
                            continue

                        itWorked = True
                        print(i+1, year, url, songNames[i])
                        doubleResultCheckerThatIsSupposedToFixit = True

                        jamYearsFile.write(year[3:7])
                        jamYearsFile.write("\n")
                        jamYearsFile.write("\n")



            # Checks if no year was found in the song search
            if itWorked is False:
                searchesThatDontWork.append([i+1, songNames[i], url])
                songYears.append('didnt work')
                print(songNames[i], "didn't work")

            # Updates the time
            print((datetime.now() - start_time))

        # Prints the full list of songs and years
        print("songNames length: %d \nsongYears length: %d \n songYearsToCheck length: %d" \
              % (len(songNames), len(songYears), len(yearsToCheck)))
        print('\nFull list:')
        for i in range(len(songNames) - 1):
            print("%d) %s: %s" % (i+1, songNames[i], songYears[i]))

        # Prints the jams to check from 90s and 2000s
        print('\nYears to check:')
        for i in range(len(yearsToCheck)):
            print(yearsToCheck[i])

        # Prints the year searches that didn't work
        print("\nsearches that didn't work:")
        for i in range(len(searchesThatDontWork)):
            print(searchesThatDontWork[i])



    elif choice == 69:
        print("ok bye bye")

    else:
        print("Not an option")
