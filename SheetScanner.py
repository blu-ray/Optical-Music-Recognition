import cv2
import numpy as np
import math
import sys
import subprocess
import time

def lineLengthArr(array): #this function get an array of lines, and return an array of lines lengths
    result = np.array([])
    for line in array:
        line = line[0]
        length2 = ((line[0] - line[2])*(line[0] - line[2]) + (line[1] - line[3])*(line[1] - line[3]))
        #print(line)
        #print(length2)
        #print("Ssssssss")
        result=np.concatenate((result,[length2]))
    return result

def selectBestLines(array,resolution): #Removing lines which are near each other(keep only the biggest one)
    #threshold = 100000
    sumi= 0
    for lineIndex in range(len(array)):
        for secondLineIndex in range(lineIndex+1, len(array)):
            sumi += linesAverageDistance(array[lineIndex][0], array[secondLineIndex][0])

    threshold = int(sumi/(len(array)*(len(array)+1))/5)
    print("Line Distance Threshold: ",threshold)
    for lineIndex in range(len(array)):
        if(array[lineIndex][0][0] == -1):
            continue
        for secondLineIndex in range(lineIndex+1, len(array)):
            if (array[secondLineIndex][0][0] == -1):
                continue
            if(linesAverageDistance(array[lineIndex][0], array[secondLineIndex][0]) < threshold): # lines are almost the same
                if(lineLength(array[lineIndex][0]) < lineLength(array[secondLineIndex][0])):
                    array[lineIndex][0] = [-1, -1, -1, -1]
                    break
                else:
                    array[secondLineIndex][0] = [-1, -1, -1, -1]
                    break

            l1 = array[lineIndex][0]
            l2 = array[secondLineIndex][0]
            if(l1[0] - l1[2] != 0):
                k1 = (l1[1]-l1[3])/(l1[0] - l1[2])
                b1 = l1[1] - k1 * l1[0]
                theta1 = math.atan(k1) * 180 / math.pi
            else:
                k1 = 9999
                b1 = l1[0]
                theta1 = 90

            if(l2[0] - l2[2] != 0):
                k2 = (l2[1]-l2[3])/(l2[0] - l2[2])
                b2 = l2[1] - k2 * l2[0]
                theta2 = math.atan(k2) * 180 / math.pi
            else:
                k2 = 9999
                b2 = l2[0]
                theta2 = 90

            if(theta1<-45 and theta2>45):
                theta1 += 180
            elif(theta2<-45 and theta1>45):
                theta2 += 180
            factor = int(100*(resolution/2))
            if( (abs(theta1 - theta2)<10) and (abs(b1 - b2) < factor*(1+abs((theta2+theta1)/2)))):
                if(lineLength(array[lineIndex][0]) < lineLength(array[secondLineIndex][0])):
                    array[lineIndex][0] = [-1, -1, -1, -1]
                    break
                else:
                    array[secondLineIndex][0] = [-1, -1, -1, -1]
                    break
    bests = []
    for lineIndex in range(len(array)):
        if(not(array[lineIndex][0][0]==-1)):
            bests.append(array[lineIndex])
    return np.array(bests)

def linesAverageDistance(line1,line2): #this function calculate distance of two endpoints of two lines from each other
    length1 = ((line1[0] - line2[0]) * (line1[0] - line2[0]) + (line1[1] - line2[1]) * (line1[1] - line2[1]))
    length1 += ((line1[2] - line2[2]) * (line1[2] - line2[2]) + (line1[3] - line2[3]) * (line1[3] - line2[3]))
    length2 = ((line1[0] - line2[2]) * (line1[0] - line2[2]) + (line1[1] - line2[3]) * (line1[1] - line2[3]))
    length2 += ((line1[2] - line2[0]) * (line1[2] - line2[0]) + (line1[3] - line2[1]) * (line1[3] - line2[1]))
    return min(length1,length2)

def lineMinimumDistance(line1,line2): #this function calculate minimum distance of two endpoints of two lines from each other
    length1 = ((line1[0] - line2[0]) * (line1[0] - line2[0]) + (line1[1] - line2[1]) * (line1[1] - line2[1]))
    length2 = ((line1[2] - line2[2]) * (line1[2] - line2[2]) + (line1[3] - line2[3]) * (line1[3] - line2[3]))
    length3 = ((line1[0] - line2[2]) * (line1[0] - line2[2]) + (line1[1] - line2[3]) * (line1[1] - line2[3]))
    length4 = ((line1[2] - line2[0]) * (line1[2] - line2[0]) + (line1[3] - line2[1]) * (line1[3] - line2[1]))
    return min(length1,length2,length3,length4)

def lineLength(line): #this function get a line and return it's length
    length2 = ((line[0] - line[2]) * (line[0] - line[2]) + (line[1] - line[3]) * (line[1] - line[3]))
    return length2

def line_intersection(line1, line2): #find intersection point of 2 lines
    xdiff = (line1[0] - line1[2], line2[0] - line2[2])
    ydiff = (line1[1] - line1[3], line2[1] - line2[3])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det([line1[0],line1[1]],[line1[2],line1[3]]), det([line2[0],line2[1]],[line2[2],line2[3]]))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]

def findPoints(lines): #find intersection points of 4 lines
    minDisFromFirst = [0]
    for i in range(1, len(lines)):
        minDisFromFirst.append(lineMinimumDistance(lines[0][0], lines[i][0]))

    parallelToFirst = minDisFromFirst.index(max(minDisFromFirst))

    points = []
    for i in range(1, len(lines)):
        if(i != parallelToFirst):
            points.append(line_intersection(lines[i][0], lines[0][0]))
            points.append(line_intersection(lines[i][0], lines[parallelToFirst][0]))

    return np.array(points)


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
         [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

def open_file(path):
    cmd = {'linux':'eog', 'win32':'explorer'}[sys.platform]
    subprocess.run([cmd, path])

def scan(sheetname):
    sheetAddress = "Sheets\\" + sheetname
    sheet = cv2.imread(sheetAddress, 0)
    sheetGrayScale = sheet
    ratio = int(sheet.shape[0]/600)
    print("ratio",ratio)
    cv2.imwrite("Sheets\\original.jpg",sheet)
    open_file("Sheets\\original.jpg")
    time.sleep(1)


    sheetc = cv2.imread(sheetAddress,1)
    imagHSL = cv2.cvtColor(sheetc,cv2.COLOR_BGR2HSV)
    lower_gr = np.array([0,0,100])
    upper_gr = np.array([255,40,255])
    mask = cv2.inRange(imagHSL, lower_gr, upper_gr)
    result = cv2.bitwise_and(sheetc,sheetc,mask=mask)
    sheetGrayScale = cv2.cvtColor(result,cv2.COLOR_HSV2BGR)
    sheetGrayScale = cv2.cvtColor(sheetGrayScale,cv2.COLOR_BGR2GRAY)

    '''
    kernel = np.ones((10, 10), np.uint8)
    sheetGrayScale = cv2.morphologyEx(sheetGrayScale, cv2.MORPH_OPEN, kernel)
    '''
    kernel = np.ones((30,30),np.uint8)
    sheetGrayScale = cv2.morphologyEx(sheetGrayScale, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((40,40),np.uint8)
    sheetGrayScale = cv2.morphologyEx(sheetGrayScale, cv2.MORPH_OPEN, kernel)
    result = sheetGrayScale
    result = cv2.resize(result,(int(result.shape[1]/ratio),int(result.shape[0]/ratio))) #resizing image for getting fit in screen



    #showing Gray level of Original Picture
    #sheetResize = cv2.resize(sheet,(int(sheet.shape[1]/ratio),int(sheet.shape[0]/ratio))) #resizing image for getting fit in screen
    #cv2.imshow("OriginalPicture",sheetResize)

    #this part shows detected edges of image with canny algorithm
    sheetGrayScale = cv2.GaussianBlur(sheetGrayScale, (5, 5), 0)
    sheetEdges = cv2.Canny(sheetGrayScale, 50, 130) #canny min and max values are very important
    cv2.imwrite("Sheets\\Edges.jpg",sheetEdges)
    open_file("Sheets\\Edges.jpg")
    time.sleep(1)
    sheetEdgesResize = cv2.resize(sheetEdges, (int(sheetEdges.shape[1]/ratio), int(sheetEdges.shape[0]/ratio))) #resizing image for getting fit in screen
    #cv2.imshow("Edges", sheetEdgesResize)


    #this part shows detected lines of edges of image with lsd algorithm
    lsd = cv2.createLineSegmentDetector(0)
    lines = lsd.detect(sheetEdges)[0]
    #sorting lines by their length
    predicate = lineLengthArr(lines)
    order = np.argsort(predicate)
    sortedLines = lines[order]
    print(len(lines))
    #fourBiggestLines = sortedLines
    fourBiggestLines = selectBestLines(sortedLines[-100:],ratio)[-4:] #this part needs to be improved. four lines must be selected using other methods
    print(len(fourBiggestLines))
    print(fourBiggestLines)
    fourPoints = findPoints(fourBiggestLines) #four corner points
    draw_img = lsd.drawSegments(sheet,fourBiggestLines)
    cv2.circle(draw_img,(fourPoints[0][0],fourPoints[0][1]),20,(0,255,255),-1)
    cv2.circle(draw_img,(fourPoints[1][0],fourPoints[1][1]),20,(0,255,255),-1)
    cv2.circle(draw_img,(fourPoints[2][0],fourPoints[2][1]),20,(0,255,255),-1)
    cv2.circle(draw_img,(fourPoints[3][0],fourPoints[3][1]),20,(0,255,255),-1)
    print(fourPoints)
    cv2.imwrite("Sheets\\Lsd.jpg",draw_img)
    open_file("Sheets\\Lsd.jpg")
    time.sleep(1)
    #draw_img = cv2.resize(draw_img,(int(draw_img.shape[1]/ratio),int(draw_img.shape[0]/ratio))) #resizing image for getting fit in screen
    #cv2.imshow("LSDonCanny",draw_img)



    '''
    #ret, thresh = cv2.threshold(sheet, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(sheetEdges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key = cv2.contourArea,reverse=True)[:10]
    cv2.drawContours(sheet,contours,-1,(0,255,0),2)
    sheetResize = cv2.resize(sheet,(int(sheet.shape[1]/2),int(sheet.shape[0]/2))) #resizing image for getting fit in screen
    cv2.imshow("Contours",sheetResize)
    '''
    warped = four_point_transform(sheet,fourPoints)
    cv2.imwrite("Sheets\\sheetext.jpg",warped)
    open_file("Sheets\\sheetext.jpg")
    time.sleep(1)

    #warped = cv2.resize(warped,(int(warped.shape[1]/ratio),int(warped.shape[0]/ratio))) #resizing image for getting fit in screen
    #cv2.imshow("SheetExtracted",warped)


    #cv2.waitKey()
    #cv2.destroyAllWindows()