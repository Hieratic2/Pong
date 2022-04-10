import pygame
pygame.init()

WIDTH ,HEIGHT = 700,500 
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
WHITE =  (255,255,255)
BLACK = (0,0,0)
BALL_RADIUS = 7
WINNING_SCORE = 5

PADDLE_WIDTH,PADDLE_HEIGHT = 20,100
SCORE_FONT = pygame.font.SysFont("comicsans",50)

class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self,x,y,width,height):
        self.x= x
        self.y= y
        self.width= width
        self.height= height
    
    def draw(self):
        pygame.draw.rect(WIN, self.COLOR,(self.x,self.y,self.width,self.height))

    def move(self,up=True):
        if up:
            self.y -= self.VELOCITY 
        else:
            self.y += self.VELOCITY
    
    def reset(self,x,y):
        self.x = x
        self.y = y

class Ball:
    COLOR = WHITE
    MAX_VEL = 5

    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self):
        pygame.draw.circle(WIN,WHITE,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.x_vel = self.MAX_VEL
        self.y_vel = 0


def draw(paddles,ball,left_score,right_score):
    WIN.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}",1,WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}",1,WHITE)
    WIN.blit(left_score_text,(WIDTH//4 - left_score_text.get_width()//2,20))
    WIN.blit(right_score_text,(WIDTH*(3/4) - right_score_text.get_width()//2,20))

    for paddle in paddles:
        paddle.draw()
    
    ball.draw()
    draw_middle_line()

    pygame.display.update()

def draw_middle_line():
    height = 8
    width = 5
    x = WIDTH // 2 - height//2
    y = 10
    space_between = 10
    while y + height <= HEIGHT - 10:
        pygame.draw.rect(WIN,WHITE,(x,y,width,height))
        y += height + space_between


def handle_collison_movement(ball,left_paddle,right_paddle):
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1

    if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
        if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
            middle_point = left_paddle.y + left_paddle.height // 2 
            difference_y = middle_point - ball.y
            interval_height = (left_paddle.height/2) / Ball.MAX_VEL
            velocity = difference_y / interval_height
            ball.y_vel = -1 *velocity
            ball.x_vel *= -1

    if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
        if ball.x + ball.radius >= right_paddle.x:
            middle_point = right_paddle.y + right_paddle.height // 2 
            difference_y = middle_point - ball.y
            interval_height = (right_paddle.height/2) / Ball.MAX_VEL
            velocity = difference_y / interval_height
            ball.y_vel = -1 *velocity 
            ball.x_vel *= -1
    

def handle_paddle_movement(keys,left_paddle,right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move()
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move()
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height  <= HEIGHT:
        right_paddle.move(False)
    
def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10,HEIGHT//2 - PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - (10 + PADDLE_WIDTH),HEIGHT//2 - PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    ball = Ball(WIDTH//2,HEIGHT//2,BALL_RADIUS) 
    left_score = 0
    right_score = 0
    won = False
    while run:
        clock.tick(FPS)
        draw([left_paddle,right_paddle],ball,left_score,right_score)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys,left_paddle,right_paddle)

        ball.move()
        handle_collison_movement(ball,left_paddle,right_paddle)
        if ball.x <= 0:
            right_score += 1
            ball.reset()
            
        elif ball.x >= WIDTH:
            left_score += 1
            ball.reset()
        
        
        if left_score == WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        
        elif right_score == WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"


        if won:
            text = SCORE_FONT.render(win_text,1,WHITE)
            WIN.blit(text,(WIDTH//2 - text.get_width()//2,HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)
            left_paddle.reset(10,HEIGHT//2 - PADDLE_HEIGHT//2)
            right_paddle.reset(WIDTH - (10 + PADDLE_WIDTH),HEIGHT//2 - PADDLE_HEIGHT//2)
            left_score = 0
            right_score = 0
            won = False
        

    pygame.quit()



if __name__ == '__main__' :
    main()



