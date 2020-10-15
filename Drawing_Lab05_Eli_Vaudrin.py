#ETGG 1801
#Eli Vaudrin
#Lab05-Game Loops
#Date:10/3/20

import pygame as pyg
import pygame.gfxdraw
import sys, math

pyg.init()
pyg.event.set_allowed([pyg.QUIT, pyg.MOUSEMOTION, pyg.MOUSEBUTTONDOWN, pyg.KEYDOWN])


windowClock = pygame.time.Clock()
fps = 120

res = (500, 500)
realres = (res[0]*1.2, res[1]*1.2)

updated = False
drects = []


clear = (0, 0, 0, 0)
w = (255, 255, 255)
gray = (220, 220, 220)
blck = (0, 0, 0)
rd = (255, 0, 0)
g = (0, 232, 0)
b = (0, 45, 242)
y = (252, 243, 5)
p = (132, 0, 165)
o = (249, 137, 11)


myColors = [w, blck, rd, g, b, y, p, o]

myWindow = pyg.display.set_mode(res, pyg.DOUBLEBUF)
myWindow.fill(w)
myCanvas = pyg.Surface((realres[0], realres[1]*0.84)).convert_alpha()
myCanvas.fill(w)
L1 = myCanvas.copy()
L2 = myCanvas.copy()
L3 = myCanvas.copy()
L4 = myCanvas.copy()
L5 = myCanvas.copy()
layers = [L1, L2, L3, L4, L5]
for layer in layers:
    layer.fill(clear)
overlay = pyg.Surface(res).convert_alpha()

realrect = pyg.Rect(0, 0, realres[0], int(realres[1]*0.84))
screenrect = pyg.Rect(0, 0, res[0], int(res[1]*0.84))
colorBar = pyg.Rect(0, 420, 500, 80)

r = 25
clr = blck
startpoint = None
endpoint = None
ongoing = False
undone = 0
maxundone = 0
holdClick = False

def button(color, rect):
    global clr,holdClick
    if 0 <= rect <= 9:
        rect = pyg.Rect(48*rect+12, 446, 44, 44)
        if pyg.mouse.get_pressed()[0] and rect.collidepoint(mosPos) and not holdClick:
            clr = color
            drects.append(colorBar)
        if clr == color:
            pyg.draw.rect(overlay, color, rect)
            pyg.draw.rect(overlay, blck, rect, 3)
        else:
            pyg.draw.rect(overlay, color, (rect[0]+4, rect[1]+4, rect[2]-8, rect[3]-8))
            pyg.draw.rect(overlay, blck, (rect[0]+4, rect[1]+4, rect[2]-8, rect[3]-8), 3)

def drawline():
    global startpoint, endpoint, start
    if startpoint == None:
        startpoint = x, y
    endpoint = x, y
    if r > 1:
        if startpoint != endpoint:
            dx, dy = endpoint[0]-startpoint[0], endpoint[1]-startpoint[1]
            angle = math.atan2(-dy, dx)%(2*math.pi)
            dx, dy = math.sin(angle)*(r*0.999), math.cos(angle)*(r*0.999)
            a = startpoint[0]+dx, startpoint[1]+dy
            b = startpoint[0]-dx, startpoint[1]-dy
            c = endpoint[0]-dx, endpoint[1]-dy
            d = endpoint[0]+dx, endpoint[1]+dy
            pointlist = [a, b, c, d]
            pyg.draw.polygon(L1, clr, pointlist)
        pyg.draw.circle(L1, clr, (x, y), r)
    else:
        pyg.draw.line(L1, clr, startpoint, endpoint, r)
    startpoint = x, y

def shiftdown():
    for layer in reversed(layers):
        if layer == L5:
            myCanvas.blit(L5, (0, 0))
        else:
            layers[layers.index(layer)+1].blit(layer, (0, 0))

def shiftup():
    for layer in layers:
        if layer == L5:
            layer.fill(clear)
        else:
            layer.fill(clear)
            layer.blit(layers[layers.index(layer)+1], (0, 0))

overlay.fill(clear)
pyg.draw.rect(overlay, gray, colorBar)
pyg.draw.rect(overlay, blck, colorBar, 3)

overlaybg = overlay.copy()

while True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT or pyg.key.get_pressed()[pyg.K_ESCAPE]:
            pyg.quit()
            sys.exit()

        if event.type == pyg.MOUSEMOTION:
            mosPos = pyg.mouse.get_pos()
            x = int(mosPos[0]*(realres[0]/res[0]))
            y = int(mosPos[1]*(realres[1]/res[1]))
            holdingclick = True
            if screenrect.collidepoint(mosPos):
                drects.append(screenrect)

        if event.type == pyg.MOUSEBUTTONDOWN:
            holdingclick = False
            if screenrect.collidepoint(mosPos):
                drects.append(screenrect)

            if event.button == 4 and r < 100:
                r += 1
                drects.append(screenrect)
            elif event.button == 5 and r > 2:
                r -= 1
                drects.append(screenrect)

        if event.type == pyg.KEYDOWN:

            if event.key == pyg.K_DELETE or pyg.K_BACKSPACE:
                myCanvas.fill(w)
                L1.fill(clear)
                L2.fill(clear)
                L3.fill(clear)
                L4.fill(clear)
                L5.fill(clear)
                undone = 0
                maxundone = 0
                drects.append(screenrect)


    if pyg.mouse.get_pressed()[0] and screenrect.collidepoint(mosPos):
        if not ongoing:
            while undone > 0:
                shiftup()
                undone -= 1
                maxundone -= 1
            shiftdown()
        drawline()
        ongoing = True
    else:
        startpoint = None
        if ongoing:
            if maxundone < 5:
                maxundone += 1
            ongoing = False

    if screenrect in drects:

        myWindow.fill(w)
        for layer in layers:
            if layers.index(layer) == undone:
                myWindow.blit(pyg.transform.smoothscale(layer, (screenrect[2], screenrect[3])), screenrect)

        overlay.fill(clear)
        if r > 1:
            pyg.gfxdraw.aacircle(overlay, mosPos[0], mosPos[1], int(r*res[0]/realres[0]), gray)
    overlay.blit(overlaybg, screenrect)
    for color in myColors:
        button(color, myColors.index(color))
    myWindow.blit(overlay, screenrect)

    pyg.display.set_caption('Draw   |   FPS: ' + str(int(windowClock.get_fps())))
    windowClock.tick(fps)

    if not updated:
        pyg.display.update()
        updated = True
    pyg.display.update(drects)
    drects.clear()