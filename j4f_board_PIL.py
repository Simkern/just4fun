from PIL import Image, ImageDraw, ImageFont


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

FIELD_LENGTH = 700
BUFFER = 10
PAD = 1
SIDE_LENGTH = 6*FIELD_LENGTH + 2*BUFFER + 5*PAD
CENTER = int(FIELD_LENGTH/2)
RADIUS = int(0.9*(FIELD_LENGTH/2))
SMALL_RADIUS = int(FIELD_LENGTH/8.5)
SMALL_CIRCLE_WIDTH=10
FONT_SIZE = SMALL_RADIUS
FONT = ImageFont.truetype("/usr/share/fonts/truetype/tlwg/TlwgTypo-Bold.ttf", FONT_SIZE)



def getRGB(r, g, b):
	return "#" + ''.join( "0"*(2-len(hex(i)[2:])) + hex(i)[2:] for i in [r,g,b] )
def getTriplet(rgb):
	return int(rgb[1:3], 16), int(rgb[3:5], 16), int(rgb[5:], 16)

def drawGradient(draw, initx, inity, baseColor):
	r1, g1, b1 = 170, 170, 170
	r2, g2, b2 = getTriplet(baseColor)
	
	r_grad = (r2-r1)/RADIUS
	g_grad = (g2-g1)/RADIUS
	b_grad = (b2-b1)/RADIUS
	
	for i in range(RADIUS):
		nr = int(r1 + r_grad*i)
		ng = int(g1 + g_grad*i)
		nb = int(b1 + b_grad*i)
		c = getRGB(nr, ng, nb)
		draw.ellipse(
			(initx+CENTER-i, inity+CENTER-i, initx+CENTER+i, inity+CENTER+i), 
			width=1, 
			outline=c, 
			fill=None)
		
def drawSites(draw, initx, inity, baseColor):
	r1, g1, b1 = 255, 255, 255
	r2, g2, b2 = getTriplet(baseColor)
	
	r, g, b = [ i + (j-i)*0.5 for (i,j) in zip([r1,g1,b1], [r2,g2,b2]) ]
	c = getRGB(int(r),int(g),int(b))
	
	dirx = [ -int(FIELD_LENGTH/5), 0, int(FIELD_LENGTH/5), 0 ]
	diry = [ int(FIELD_LENGTH/5)*i for i in [0,1,0,-1] ]
	for (i,j) in zip(dirx,diry):
		draw.ellipse(
			(initx + CENTER+i-SMALL_RADIUS, inity+CENTER+j-SMALL_RADIUS, initx+CENTER+i+SMALL_RADIUS, inity+CENTER+j+SMALL_RADIUS), 
			width=SMALL_CIRCLE_WIDTH, 
			outline=c,
			fill=None)
	
def drawNumbers(image, draw, initx, inity, num):
	wi, hi = FONT.getsize(str(num))
	
	x = [ int(FIELD_LENGTH/2-wi/2), int(FIELD_LENGTH-FONT_SIZE/2-hi), int(FIELD_LENGTH/2-wi/2), int(FONT_SIZE/2) ]
	y = [ int(FIELD_LENGTH-hi-FONT_SIZE/2), int(FIELD_LENGTH/2-hi/2), int(FONT_SIZE/2), int(FIELD_LENGTH/2-hi/2)]
	angle = [0, 90, 180, 270]
	w = [ wi, hi, wi, hi ]
	h = [ hi, wi, hi, wi ]
	for (i,j,a,w1,h1) in zip(x,y,angle,w,h):
		img = image.crop(
			(initx+i, inity+j, initx+w1+i, inity+h1+j)
			)
		img = img.rotate(360-a, expand=1)
		d = ImageDraw.Draw(img)
		d.text( (0,0), text=str(num), font=FONT, fill=(255,255,255) )
		img = img.rotate(a, expand=1)
		image.paste(img, (initx+i, inity+j))

def createField(image, draw, x, y, num, color):
	initx = BUFFER + x*(FIELD_LENGTH+PAD)
	inity = BUFFER + y*(FIELD_LENGTH+PAD)
	draw.rectangle( 
		(initx, inity, initx + FIELD_LENGTH, inity + FIELD_LENGTH ),
		fill=getTriplet(color),
		outline=getTriplet(BG)
		)
	drawGradient(draw, initx, inity, color)
	drawSites(draw, initx, inity, color)
	drawNumbers(image, draw, initx, inity, num)


img = Image.new("RGB", (SIDE_LENGTH, SIDE_LENGTH), getTriplet(BG))
draw = ImageDraw.Draw(img)



for i in range(1,37):
	y, x = GRID_MAP[i]
	c = COLOR_MAP[i]
	f = createField(img, draw, x, y, i, c)



img.show()
