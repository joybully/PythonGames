import tkinter as tk
import random
import math

def point_calc(a,b,c):
        D = (b**2) - (4*a*c)
        if D>0:
            r1= (-b + (b**2-4*a*c)**0.5)/(2*a)
            r2 = (-b - (b**2-4*a*c)**0.5)/(2*a)
            return[r1,r2]
        elif D==0:
            x = -b / 2*a
            return [x]
        else:
            r1= (-b + (b**2-4*a*c)**0.5)/(2*a)
            r2 = (-b - (b**2-4*a*c)**0.5)/(2*a)
            return 'no coords'

def ref_vec(n_vec, in_vec):
    sc = -2*(n_vec[0]*in_vec[0]+n_vec[1]*in_vec[1])
    return [sc*n_vec[0]+in_vec[0], sc*n_vec[1]+in_vec[1]]

def nor_vec(vec):
    a = vec[0]**2+vec[1]**2
    b = a**0.5
    return [vec[0]/b,vec[1]/b]

def inner_dot(in_vec, n_vec):
    inner = in_vec[0]*n_vec[0]+in_vec[1]*n_vec[1]
    if(inner<0):
        return True
    else:
        return False

class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.x_radian = math.pi*(315/180)
        self.y_radian = math.pi*(315/180)
        self.direction = [math.cos(self.x_radian), math.sin(self.y_radian)]
        self.speed = 10
        self.ball_image = tk.PhotoImage(file = 'ball2.png')
        item = canvas.create_image(x, y,image = self.ball_image)
        super(Ball, self).__init__(canvas, item)

    def get_position(self):
        list = self.canvas.coords(self.item)
        x = list[0]
        y = list[1]
        return [x-self.radius, y-self.radius, x+self.radius, y+self.radius]

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def meetpoint( self, line_x1,line_x2, line_y1,line_y2, circle_x, circle_y, radius):
    #line_x, line_y are edge of rec
    #circle_x and circle_y are center of circle
    #radius is radius of circle
        point_list = []
        if(line_x1>line_x2):
            c = line_x1
            line_x1 = line_x2
            line_x2 = c
        if(line_y1>line_y2):
            c = line_y1
            line_y1 = line_y2
            line_y2 = c
        a = 1
        b = -2*circle_y
        c = (line_x1-circle_x)**2-radius**2+circle_y**2
        co_y = point_calc(a,b,c)
        if (type(co_y)==str):
            True
        elif (len(co_y)==1):
            if(line_y1<=co_y[0]and co_y[0]<=line_y2):
                point_list.append([line_x1,co_y[0]])
        elif(len(co_y)==2):
            if(line_y1<=co_y[0]and co_y[0]<=line_y2):
                point_list.append([line_x1,co_y[0]])
            if(line_y1<=co_y[1]and co_y[1]<=line_y2):
                point_list.append([line_x1,co_y[1]])
        a = 1
        b = -2*circle_y
        c = (line_x2-circle_x)**2-radius**2+circle_y**2
        co_y = point_calc(a,b,c)
        if (type(co_y)==str):
            True
        elif (len(co_y)==1):
            if(line_y1<=co_y[0]and co_y[0]<=line_y2):
                point_list.append([line_x2,co_y[0]])
        elif (len(co_y)==2):
            if(line_y1<=co_y[0]and co_y[0]<=line_y2):
                point_list.append([line_x2,co_y[0]])
            if(line_y1<=co_y[1]and co_y[1]<=line_y2):
                point_list.append([line_x2,co_y[1]])
        a = 1
        b = -2*circle_x
        c = circle_x**2+(line_y1-circle_y)**2-radius**2
        co_x = point_calc(a,b,c)
        if(type(co_x)==str):
            True
        elif(len(co_x)==1):
            if(line_x1<=co_x[0] and co_x[0]<=line_x2 ):
                point_list.append([co_x[0],line_y1])
        elif(len(co_x)==2):
            if(line_x1<=co_x[0] and co_x[0]<=line_x2 ):
                point_list.append([co_x[0],line_y1])
            if(line_x1<=co_x[1] and co_x[1]<=line_x2 ):
                point_list.append([co_x[1],line_y1])
        a = 1
        b = -2*circle_x
        c = circle_x**2+(line_y2-circle_y)**2-radius**2
        co_x = point_calc(a,b,c)
        if(type(co_x)==str):
            True
        elif(len(co_x)==1):
            if(line_x1<=co_x[0] and co_x[0]<=line_x2 ):
                point_list.append([co_x[0],line_y1])
        elif(len(co_x)==2):
            if(line_x1<=co_x[0] and co_x[0]<=line_x2 ):
                point_list.append([co_x[0],line_y1])
            if(line_x1<=co_x[1] and co_x[1]<=line_x2 ):
                point_list.append([co_x[1],line_y1])
        return point_list
    
    def collide(self, game_objects):
        coords = self.get_position()
        radius = self.radius
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:#여러개랑 부딪힌 경우
            ob1 = game_objects[0]
            ob2 = game_objects[1]
            ob1_coords = ob1.get_position()
            ob2_coords = ob2.get_position()
            if(ob1_coords[0]==ob2_coords[0] and ob1_coords[2] ==ob2_coords[2] ):
                self.direction[0] *= -1
            else:
                self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            square_coords = game_object.get_position()
            ball_coords = self.get_position()
            
            square_ix = (square_coords[0]+square_coords[2])/2
            square_iy = (square_coords[1]+square_coords[3])/2
            ball_ix = (ball_coords[0]+ball_coords[2])/2
            ball_iy = (ball_coords[1]+ball_coords[3])/2
            meet_points = self.meetpoint(square_coords[0],square_coords[2],square_coords[1],square_coords[3],ball_ix,ball_iy, radius)
            if(len(meet_points)==1):
                if(meet_points[0][0]==square_coords[0] or meet_points[0][0]==square_coords[2]):
                    self.direction[0] *=-1
                if(meet_points[0][1]==square_coords[1] or meet_points[0][1]==square_coords[3]):
                    self.direction[1] *=-1
            elif(len(meet_points)==2):
                eps = 0.1
                x1 = meet_points[0][0]
                x2 = meet_points[1][0]
                y1 = meet_points[0][1]
                y2 = meet_points[1][1]
                if (x1>x2):
                    c = x1
                    x1 = x2
                    x2 = c
                    c = y1
                    y1 = y2
                    y2 = c
                if(x1==x2):
                    self.direction[0]*=-1
                elif(y1 == y2):
                    self.direction[1]*=-1
                elif(square_coords[0]-eps<=x1 and x1<=square_coords[0]+eps):
                    if(square_coords[1]-eps <= y2 and y2<=square_coords[1]+eps):
                        new_vec = [-y1+y2, -x2+x1]
                        n_vec = nor_vec(new_vec)
                        if(inner_dot(n_vec, self.direction)):
                            out_vec = ref_vec(n_vec,self.direction)
                            self.direction[0] = out_vec[0]
                            self.direction[1] = out_vec[1]
                    elif(square_coords[3]-eps <= y2 and y2<=square_coords[3]+eps):
                        new_vec = [+y1-y2, +x2-x1]
                        n_vec = nor_vec(new_vec)
                        if(inner_dot(n_vec, self.direction)):
                            out_vec = ref_vec(n_vec,self.direction)
                            self.direction[0] = out_vec[0]
                            self.direction[1] = out_vec[1]
                elif(square_coords[2]-eps<=x2 and x2<=square_coords[2]+eps):
                    if(square_coords[1]-eps <= y1 and y1<=square_coords[1]+eps):
                        new_vec = [-y1+y2, -x2+x1]
                        n_vec = nor_vec(new_vec)
                        if(inner_dot(n_vec, self.direction)):
                            out_vec = ref_vec(n_vec,self.direction)
                            self.direction[0] = out_vec[0]
                            self.direction[1] = out_vec[1]
                    if(square_coords[3]-eps <= y1 and y1<=square_coords[3]+eps):
                        new_vec = [+y1-y2, +x2-x1]
                        n_vec = nor_vec(new_vec)
                        if(inner_dot(n_vec, self.direction)):
                            out_vec = ref_vec(n_vec,self.direction)
                            self.direction[0] = out_vec[0]
                            self.direction[1] = out_vec[1]

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()

class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='blue')
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)


class Brick(GameObject):
    COLORS = {1: '#999999', 2: '#777777', 3: '#555555', 4: '#333333', 5: '#111111'}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.item,
                                   fill=Brick.COLORS[self.hits])


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = 610
        self.height = 400
        self.level = 1
        self.canvas = tk.Canvas(self, bg='#aaaaff',
                                width=self.width,
                                height=self.height,)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle
        list1 = list(range(5, self.width - 5, 75))
        list2 = []
        for i in list1:
            k = random.randint(0,1)
            if(k==0):
                list2.append(i)
        for x in list2:
            self.add_brick(x + 37.5, 50, 1)
            #self.add_brick(x + 37.5, 70, 1)
            #self.add_brick(x + 37.5, 90, 1)

        self.hud = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>',
                         lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>',
                         lambda _: self.paddle.move(10))

    def setup_game(self):
           self.add_ball()
           self.update_lives_text()
           self.text = self.draw_text(300, 200,
                                      'Press Space to start')
           self.canvas.bind('<space>', lambda _: self.start_game())

    def next_level(self):
            self.add_ball()
            self.update_lives_text()
            self.text = self.draw_text(300, 200,
                                      'Press Space to start next level',20)
            self.canvas.bind('<space>', lambda _: self.go_to_next_level())

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text,
                                       font=font)

    def update_lives_text(self):
        text = 'Lives: %d Level: %d' % (self.lives,self.level)
        if self.hud is None:
            self.hud = self.draw_text(80, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def go_to_next_level(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        brick_height = self.level
        for y in range(0,brick_height):
            list1 = list(range(5, self.width - 5, 75))
            list2 = []
            for i in list1:
                k = random.randint(0,1)
                if(k==0):
                    list2.append(i)
            for x in list2:
                self.add_brick(x + 37.5, 50+y*20, brick_height-y)
                #self.add_brick(x + 37.5, 70, 1)
                #self.add_brick(x + 37.5, 90, 1)
        self.game_loop()

    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0: 
            if self.level == 5:
                self.ball.speed = None
                self.draw_text(300, 200, 'You win!')
            else:
                self.ball.speed = None
                self.level += 1
                self.after(1000, self.next_level)
                #self.draw_text(300, 200, 'You win!')
        elif self.ball.get_position()[3] >= self.height: 
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'Game Over')
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)



if __name__ == '__main__':
    root = tk.Tk()
    root.title('Hello, Pong!')
    game = Game(root)
    game.mainloop()
