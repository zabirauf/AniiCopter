import pygame
from math import pi

def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

DEFAULT_SKIP_POS = 2


def get_new_rect_pos_from_event(prev_x,prev_y,event,center_x,center_y,radius):

	temp_prev_x,temp_prev_y = prev_x,prev_y

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_UP:
			get_new_rect_pos_from_event.IS_DOWN_Y = -DEFAULT_SKIP_POS
		elif event.key == pygame.K_DOWN:
			get_new_rect_pos_from_event.IS_DOWN_Y = DEFAULT_SKIP_POS
		elif event.key == pygame.K_LEFT:
			get_new_rect_pos_from_event.IS_DOWN_X = -DEFAULT_SKIP_POS
		elif event.key == pygame.K_RIGHT:
			get_new_rect_pos_from_event.IS_DOWN_X = DEFAULT_SKIP_POS

	elif event.type == pygame.KEYUP:
		if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
			get_new_rect_pos_from_event.IS_DOWN_Y = 0
		elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
			get_new_rect_pos_from_event.IS_DOWN_X = 0

	temp_prev_x += get_new_rect_pos_from_event.IS_DOWN_X
	temp_prev_y += get_new_rect_pos_from_event.IS_DOWN_Y

	if in_circle(center_x,center_y,radius,temp_prev_x,temp_prev_y):
		return temp_prev_x,temp_prev_y

	return prev_x,prev_y

get_new_rect_pos_from_event.IS_DOWN_X = 0
get_new_rect_pos_from_event.IS_DOWN_Y = 0

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE  = (0,0,255)
RED	  = (255,0,0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MID_X = SCREEN_WIDTH/2
MID_Y = SCREEN_HEIGHT/2
RADIUS = SCREEN_WIDTH/6
SPACING_FROM_MID = RADIUS/2
SQUARE_SIDE_LENGTH = RADIUS/6
SQUARE_SIDE_LENGTH_HALF = SQUARE_SIDE_LENGTH/2


if __name__ == "__main__":
	pygame.init()
	size = [SCREEN_WIDTH,SCREEN_HEIGHT]

	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Analog stick viewer")
	done = False
	clock = pygame.time.Clock()
	CIRCLE_RADIUS_X_LEFT = MID_X-RADIUS-SPACING_FROM_MID
	CIRCLE_RADIUS_X_RIGHT = MID_X+RADIUS+SPACING_FROM_MID

	J_X = CIRCLE_RADIUS_X_LEFT-SQUARE_SIDE_LENGTH_HALF
	J_Y = MID_Y-SQUARE_SIDE_LENGTH_HALF
	while not done:
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			
			J_X,J_Y = get_new_rect_pos_from_event(J_X,J_Y,event,CIRCLE_RADIUS_X_LEFT,MID_Y,RADIUS)


		J_X,J_Y = get_new_rect_pos_from_event(J_X,J_Y,event,CIRCLE_RADIUS_X_LEFT,MID_Y,RADIUS)
		
		screen.fill(WHITE)
		

		pygame.draw.circle(screen,RED,[CIRCLE_RADIUS_X_LEFT,MID_Y],RADIUS,3)
		pygame.draw.circle(screen,RED,[CIRCLE_RADIUS_X_RIGHT,MID_Y],RADIUS,3)
		
		pygame.draw.rect(screen,BLUE,[J_X,J_Y,SQUARE_SIDE_LENGTH,SQUARE_SIDE_LENGTH],2)
		pygame.draw.rect(screen,BLUE,[CIRCLE_RADIUS_X_RIGHT-SQUARE_SIDE_LENGTH_HALF,MID_Y-SQUARE_SIDE_LENGTH_HALF,SQUARE_SIDE_LENGTH,SQUARE_SIDE_LENGTH],2)

		pygame.display.flip()

	pygame.quit()

