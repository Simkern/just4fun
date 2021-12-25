import tkinter as tk



BG = "#6a329f"
FIELD_COLORS = [ "#9fc5e8", "#17be66", "#2a6b99", "#152631" ]
COLOR_MAP = { i:FIELD_COLORS[0] for i in range(1,10) }
COLOR_MAP.update({i:FIELD_COLORS[1] for i in range(10, 20)})
COLOR_MAP.update({i:FIELD_COLORS[2] for i in range(20, 30)})
COLOR_MAP.update({i:FIELD_COLORS[3] for i in range(30, 37)})
GRID_MAP = { 1: (0,0), 2:(5,4), 3:(4,2), 4:(3,5), 5:(2,3), 6:(0,2),
			 7: (1,5), 8:(5,0), 9:(2,1), 10:(1,4), 11:(1,1), 12:(5,2),
			 13:(4,5), 14:(1,0), 15:(0,3), 16:(3,1), 17:(4,3), 18:(2,4),
			 19:(4,0), 20:(3,2), 21:(5,1), 22:(0, 4), 23:(2,5), 24:(3,0),
			 25:(4,4), 26:(5,3), 27:(1,2), 28:(0,5), 29:(3,3), 30:(2,0),
			 31:(2,2), 32:(1,3), 33:(0,1), 34:(5,5), 35:(4,1), 36:(3,4) }

FIELD_LENGTH = 100
SIDE_LENGTH = 6*FIELD_LENGTH + 20
CENTER = int(FIELD_LENGTH/2)
RADIUS = int(0.9*(FIELD_LENGTH/2))
SMALL_RADIUS = int(FIELD_LENGTH/8.5)
FONT_SIZE = SMALL_RADIUS
PAD = 1

def getRGB(r, g, b):
	return "#" + ''.join( "0"*(2-len(hex(i)[2:])) + hex(i)[2:] for i in [r,g,b] )
def getTriplet(rgb):
	return int(rgb[1:3], 16), int(rgb[3:5], 16), int(rgb[5:], 16)

def drawGradient(parent, baseColor):
	r1, g1, b1 = 200, 200, 200
	r2, g2, b2 = getTriplet(baseColor)
	#m = max(r2,g2,b2)
	#if m == 0:
	#	m=1
	#r1, g1, b1 = 255/m * r2, 255/m * g2, 255/m * b2
	
	r_grad = (r2-r1)/RADIUS
	g_grad = (g2-g1)/RADIUS
	b_grad = (b2-b1)/RADIUS
	
	for i in range(RADIUS):
		nr = int(r1 + r_grad*i)
		ng = int(g1 + g_grad*i)
		nb = int(b1 + b_grad*i)
		c = getRGB(nr, ng, nb)
		parent.create_oval(CENTER-i, CENTER-i, CENTER+i, CENTER+i, width=1, outline=c, outlinestipple="gray75")
		
def drawSites(parent, baseColor):
	r1, g1, b1 = 255, 255, 255
	r2, g2, b2 = getTriplet(baseColor)
	
	r, g, b = [ i + (j-i)*0.5 for (i,j) in zip([r1,g1,b1], [r2,g2,b2]) ]
	c = getRGB(int(r),int(g),int(b))
	
	dirx = [ -int(FIELD_LENGTH/5), 0, int(FIELD_LENGTH/5), 0 ]
	diry = [ int(FIELD_LENGTH/5)*i for i in [0,1,0,-1] ]
	for (i,j) in zip(dirx,diry):
		parent.create_oval(CENTER+i-SMALL_RADIUS, CENTER+j-SMALL_RADIUS, CENTER+i+SMALL_RADIUS, CENTER+j+SMALL_RADIUS, width=3, outline=c)
	
def drawNumbers(parent, num):
	x = [ int(FIELD_LENGTH/2), int(FIELD_LENGTH-FONT_SIZE/2), int(FIELD_LENGTH/2), int(FONT_SIZE/2) ]
	y = [ int(FIELD_LENGTH-FONT_SIZE/2), int(FIELD_LENGTH/2), int(FONT_SIZE/2), int(FIELD_LENGTH/2)]
	angle = [0, 90, 180, 270]
	for (i,j,a) in zip(x,y,angle):
		parent.create_text(i,j, text=str(num), angle=a, font=("Times",FONT_SIZE,"bold"), fill="#ffffff")

def createField(parent, num, color):
	f = tk.Canvas( bg=color, height=FIELD_LENGTH, width=FIELD_LENGTH )
	drawGradient(f, color)
	drawSites(f, color)
	drawNumbers(f, num)
	return f


root = tk.Tk()

canvas = tk.Canvas(root, bg=BG, height=SIDE_LENGTH, width=SIDE_LENGTH)
canvas.grid(row=0, column=0, rowspan=8,columnspan=8)


for i in range(1,37):
	y, x = GRID_MAP[i]
	c = COLOR_MAP[i]
	f = createField(canvas, i, c)
	f.grid(row=x+1, column=y+1, padx=PAD, pady=PAD)



root.mainloop()
