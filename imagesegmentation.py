from __future__ import division
import cv2
import numpy as np
import os
import sys
from math import exp, pow
from fordfulkerson import fordFulkerson

# np.set_printoptions(threshold=np.inf)

SIGMA = 30
# LAMBDA = 1
OBJCOLOR, BKGCOLOR = (0, 0, 255), (0, 255, 0)
OBJCODE, BKGCODE = 1, 2
OBJ, BKG = "OBJ", "BKG"

CUTCOLOR = (0, 0, 255)

SOURCE, SINK = -2, -1
SIZE = 100
LOADSEEDS = False
sf = 10
# drawing = False

def show_image(image):
    windowname = "window"
    cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
    cv2.startWindowThread()
    cv2.imshow(windowname, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def plantSeed(image):
    
    if LOADSEEDS:
        seeds = np.load(pathname + "seeds.npy")
    else:
        seeds = np.zeros(image.shape, dtype="uint8")
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        image = cv2.resize(image, (0, 0), fx=sf, fy=sf)

        radius = 10
        thickness = -1 # fill the whole circle
        global drawing
        drawing = False
        

        def drawLines(x, y, pixelType):
            if pixelType == OBJ:
                color, code = OBJCOLOR, OBJCODE
            else:
                color, code = BKGCOLOR, BKGCODE
            cv2.circle(image, (x, y), radius, color, thickness)
            cv2.circle(seeds, (x // sf, y // sf), radius // sf, code, thickness)

            # image[x][y] = color
            # seeds[x][y] = color

        def onMouse(event, x, y, flags, pixelType):
            global drawing
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                drawLines(x, y, pixelType)
            elif event == cv2.EVENT_MOUSEMOVE and drawing:
                drawLines(x, y, pixelType)
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False

        def paintSeeds(pixelType):
            global drawing
            drawing = False
            windowname = "window"
            cv2.namedWindow(windowname, cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback(windowname, onMouse, pixelType)
            while (1):
                cv2.imshow(windowname, image)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            cv2.destroyAllWindows()

        print "plant obj seeds"
        paintSeeds(OBJ)
        print "plant bkg seeds"
        paintSeeds(BKG)
        seedname = pathname + "seeds.npy"
        np.save(seedname, seeds)
        print "Saved seeds as", seedname
    print "seeds:"
    print seeds

    savename = pathname + "seeds.jpg"
    
    cv2.imwrite(savename, image)
    
    print "Saved seeded image as", savename

    return seeds



# Large when ip - iq < sigma, and small otherwise
def boundaryPenalty(ip, iq):
    # return 100 * exp(- pow(int(ip) - int(iq), 2) / (2 * pow(SIGMA, 2)))
    bp = 100 * exp(- pow(int(ip) - int(iq), 2) / (2 * pow(SIGMA, 2))) #int(100 * exp(- abs(int(ip) - int(iq)) / SIGMA))
    # print ip, iq, bp
    return bp#(2 * pow(SIGMA, 2)))

def regionalPenalty(ip, ap):
    pass

def buildGraph(image):
    V = image.size + 2
    graph = np.zeros((V, V), dtype='int32')

    K = makeNLinks(graph, image)

    seeds = plantSeed(image)
    print "got seeds"
    makeTLinks(graph, seeds, K)

    return graph

def makeNLinks(graph, image):
    K = -float("inf")
    r, c = image.shape
    for i in xrange(r):
        for j in xrange(c):
            x = i * c + j
            if i + 1 < r: # pixel below
                y = (i + 1) * c + j
                bp = boundaryPenalty(image[i][j], image[i + 1][j])
                graph[x][y] = graph[y][x] = bp
                K = max(K, bp)
            if j + 1 < c: # pixel to the right
                y = i * c + j + 1
                bp = boundaryPenalty(image[i][j], image[i][j + 1])
                graph[x][y] = graph[y][x] = bp
                K = max(K, bp)

    print "finished building nlinks"
    print graph
    return K



def makeTLinks(graph, seeds, K):
    print "making T links"
    print graph.shape
    print "k =", K

    
    r, c = seeds.shape

    for i in xrange(r):
        for j in xrange(c):
            x = i * c + j
            if seeds[i][j] == OBJCODE:
                # graph[x][source] = K
                graph[SOURCE][x] = K
            elif seeds[i][j] == BKGCODE:
                graph[x][SINK] = K
                # graph[sink][x] = K
            # else:
            #     graph[x][source] = LAMBDA * regionalPenalty(image[i][j], BKG)
            #     graph[x][sink]   = LAMBDA * regionalPenalty(image[i][j], OBJ)

    print "finished tlinks"


def displayCut(image, cuts):
    def colorPixel(i, j):
        image[i][j] = CUTCOLOR

    r, c = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    for c in cuts:
        colorPixel(c[0] // r, c[0] % r)
        colorPixel(c[1] // r, c[1] % r)

    return image
    # show_image(image)





def imageSegmentation():
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    # image = cv2.resize(image, (0, 0), fx=sf, fy=sf)
    print image.shape
    # show_image(image)

    graph = buildGraph(image)
    global SOURCE, SINK
    SOURCE += len(graph) 
    SINK   += len(graph)
    print graph
    cuts = fordFulkerson(graph, SOURCE, SINK)
    print "cuts:"
    print cuts
    image = displayCut(image, cuts)
    image = cv2.resize(image, (0, 0), fx=sf, fy=sf)
    savename = pathname + "cut.jpg"
    cv2.imwrite(savename, image)
    print "Saved image as", savename
    

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "missing filename argument"

    else:
        filename = sys.argv[1]
        pathname = os.path.splitext(filename)[0]
        imageSegmentation()
    





