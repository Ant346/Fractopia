import turtle
import random
import fract_L as fr
from tkinter import *
global my_t
my_t=turtle.Turtle()
turtle.tracer(1, 0) 
pen_width = 2   # толщина линии рисования (в пикселах)
f_len = 10      # длина одного сегмента прямой (в пикселах)
angle=90
len_=20
a=-500
b=-400
my_t.pensize(pen_width)
my_t.ht()          # скрываем черепашку

def grass(a=-500):
    my_t.up()
    my_t.goto(a,b)
    my_t.down()
    my_t.pensize(1)
    for i in range (100):
        my_t.left(angle)
        my_t.left(-15)
        my_t.forward(25)

        my_t.up()
        my_t.goto(a,b)
        a+=5
        my_t.seth(115)
        my_t.down()

        my_t.forward(len_)

        my_t.up()
        my_t.goto(a,b)
        a+=5
        my_t.seth(115)
        my_t.down()

        my_t.forward(30)
        my_t.up()
        my_t.goto(a,b)
        a+=3
        my_t.seth(0)
        my_t.down()

    a=-500
    for i in range(100):
        my_t.up()
        my_t.goto(random.randint(-500,1000),b)
        my_t.seth(115)
        my_t.down()
        for i in range (5):
            my_t.forward(5)
            my_t.left(2.5)

    a=-500
    for i in range(100):
        my_t.up()
        my_t.goto(random.randint(-500,1000),b)
        my_t.seth(75)
        my_t.down()
        for i in range (6):
            my_t.forward(5)
            my_t.left(4)
def grass_1(a=-400,b=-400):
    # Рисуем траву 1
    angle = 25.7	# для дерева (1 и 2)
    axiom = "F"	# для дерева и трав
    l_sys = fr.LSystem2D(my_t, axiom, pen_width, f_len, angle)
    l_sys.add_rules(("F", "F[+F]F[-F]F"))		# для травы 1
    l_sys.generate_path(3)
    print(l_sys.state)
    l_sys.draw_turtle( (a,b), 90)
def grass_2(a=200,b=-400):
    # Рисуем траву 2
    angle = 22.5	# для дерева (1 и 2)
    axiom = "F"	# для дерева 2
    l_sys = fr.LSystem2D(my_t, axiom, pen_width, f_len, angle)
    l_sys.add_rules(("F", "FF-[-F+F+F]+[+F-F-F]"))	# для травы 2
    l_sys.generate_path(3)
    print(l_sys.state)
    l_sys.draw_turtle( (a, b), 90)





def home():
    pen_width = 2   # толщина линии рисования (в пикселах)
    f_len = 4     # длина одного сегмента прямой (в пикселах)
    angle = 90      # фиксированный угол поворота (в градусах)
    axiom = "F+F+F+F"

    l_sys = fr.LSystem2D(my_t, axiom, pen_width, f_len, angle)
    #l_sys.add_rules(("F", "F+F--F+F"))
    #l_sys.add_rules(("F", "F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"))
    l_sys.add_rules(("F", "F+S-FF+F+FF+FS+FF-S+FF-F-FF-FS-FFF"), ('S', 'SSSSSS'))
    l_sys.generate_path(2)
    l_sys.draw_turtle( (-400, 0), 0)

def dragon():
    pen_width = 2   # толщина линии рисования (в пикселах)
    f_len = 4     # длина одного сегмента прямой (в пикселах)
    angle = 90      # фиксированный угол поворота (в градусах)
    axiom = "F+F+F+F"

    l_sys = fr.LSystem2D(my_t, axiom, pen_width, f_len, angle)
    #l_sys.add_rules(("F", "F+F--F+F"))
    l_sys.add_rules(("F", "F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"))
    #l_sys.add_rules(("F", "F+S-FF+F+FF+FS+FF-S+FF-F-FF-FS-FFF"), ('S', 'SSSSSS'))
    l_sys.generate_path(2)
    l_sys.draw_turtle( (-300, -50), 0)

def tree(my_t=my_t,a=0):
    import turtle
    import re
    import random


    # список функций для управления параметаризированными командами
    # у всех функций будет префикс cmd_ и первый параметр t - черепашка
    def cmd_turtle_fd(t, length, *args):
        my_t.pensize(args[1])
        my_t.fd(length*args[0])

    def cmd_turtle_left(my_t, angle, *args):
        my_t.left(args[0])

    def cmd_turtle_right(my_t, angle, *args):
        my_t.right(args[0])

    class LSystem2D:
        def __init__(self, my_t, axiom, width, length, angle):
            self.axiom = axiom      # инициатор
            self.state = axiom      # строка с набором команд для фрактала (вначале это инициатор)
            self.width = width      # толщина линии рисования
            self.length = length    # длина одного линейного сегмента кривой
            self.angle = angle      # фиксированный угол поворота
            self.my_t = my_t              # сама черепашка
            self.rules = {}  # словарь для хранения правил формирования кривых
            self.my_t.pensize(self.width)
            self.rules_key = None
            self.key_re_list = []  # список шаблонов команд
            self.cmd_functions = {}  # словарь связей параметаризованных команд и функций

        def add_rules(self, *rules):
            for r in rules:
                p = 1
                if len(r) == 3:
                    key, value, p = r
                else:
                    key, value = r

                key_re = key.replace("(", r"\(")
                key_re = key_re.replace(")", r"\)")
                key_re = key_re.replace("+", r"\+")
                key_re = key_re.replace("-", r"\-")

                if not isinstance(value, str):  # ключ с параметрами
                    key_re = re.sub(r"([a-z]+)([, ]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2), key_re)
                    self.key_re_list.append(key_re)

                if not self.rules.get(key):
                    self.rules[key] = [(value, key_re, p)]
                else:
                    self.rules[key].append((value, key_re, p))

        def get_random_rule(self, rules):
            p = random.random()  # случайное вещественное число в интервале [0; 1]
            off = 0
            for v in rules:
                if p < (v[2]+off):
                    return v
                off += v[2]

            return rules[0]

        def update_param_cmd(self, m):
            if not self.rules_key:
                return ""

            rule = self.rules_key[0] if len(self.rules_key) == 1 else self.get_random_rule(self.rules_key)

            if isinstance(rule[0], str):
                return rule[0].lower()
            else:
                args = list(map(float, m.groups()))
                return rule[0](*args).lower()

        def generate_path(self, n_iter):
            for n in range(n_iter):
                for key, rules in self.rules.items():
                    self.rules_key = rules
                    self.state = re.sub(rules[0][1], self.update_param_cmd, self.state)
                    self.rules_key = None

                self.state = self.state.upper()


        def set_turtle(self, my_tuple):
            self.my_t.up()
            self.my_t.goto(my_tuple[0], my_tuple[1])
            self.my_t.seth(my_tuple[2])
            self.my_t.down()

        def add_rules_move(self, *moves):
            for key, func in moves:
                self.cmd_functions[key] = func

        def draw_turtle(self, start_pos, start_angle):
                # ***************
                turtle.tracer(1, 0)  # форсажный режим для черепашки
                self.my_t.up()  # черепашка воспаряет над поверхностью (чтобы не было следа)
                self.my_t.setpos(start_pos)  # начальная стартовая позиция
                self.my_t.seth(start_angle)  # начальный угол поворота
                self.my_t.down()  # черепашка опускается на "грешную землю"
                turtle_stack = []
                key_list_re = "|".join(self.key_re_list)
                # ***************
                # for move in self.state:
                for values in re.finditer(r"(" + key_list_re + r"|.)", self.state):
                    cmd = values.group(0)
                    args = [float(x) for x in values.groups()[1:] if x]

                    if 'F' in cmd:
                        if len(args) > 0 and self.cmd_functions.get('F'):
                            self.cmd_functions['F'](my_t, self.length, *args)
                        else:
                            self.my_t.fd(self.length)
                    elif 'S' in cmd:
                        if len(args) > 0 and self.cmd_functions.get('S'):
                            self.cmd_functions['S'](my_t, self.length, *args)
                        else:
                            self.my_t.up()
                            self.my_t.forward(self.length)
                            self.my_t.down()
                    elif '+' in cmd:
                        if len(args) > 0 and self.cmd_functions.get('+'):
                            self.cmd_functions['+'](my_t, self.angle, *args)
                        else:
                            self.my_t.left(self.angle)
                    elif '-' in cmd:
                        if len(args) > 0 and self.cmd_functions.get('-'):
                            self.cmd_functions['-'](my_t, self.angle, *args)
                        else:
                            self.my_t.right(self.angle)
                    elif "[" in cmd:
                        turtle_stack.append((self.my_t.xcor(), self.my_t.ycor(), self.my_t.heading(), self.my_t.pensize()))
                    elif "]" in cmd:
                        xcor, ycor, head, w = turtle_stack.pop()
                        self.set_turtle((xcor, ycor, head))
                        self.width = w
                        self.my_t.pensize(self.width)

                      


    

    
    f_len = 20      # длина одного сегмента прямой (в пикселах)
    angle = 20

    axiom = "A"

    l_sys = LSystem2D(my_t, axiom, pen_width, f_len, angle)

    l_sys.add_rules(("A", f"F(1, 1)[+({angle})A][-({angle})A]", 0.5),
                    ("A", f"F(1, 1)[++({angle})A][+({angle})A][-({angle})A][--({angle})A]", 0.4),
                    ("A", f"F(1, 1)[-({angle})A]", 0.05),
                    ("A", f"F(1, 1)[+({angle})A]", 0.05),

                    ("F(x, y)", lambda x, y: f"F({(1.2+random.triangular(-0.5, 0.5, random.gauss(0, 1)))*x}, {1.4*y})"),
                    ("+(x)", lambda x: f"+({x + random.triangular(-10, 10, random.gauss(0, 2))})"),
                    ("-(x)", lambda x: f"-({x + random.triangular(-10, 10, random.gauss(0, 2))})"),
                    )

    l_sys.add_rules_move(("F", cmd_turtle_fd), ("+", cmd_turtle_left), ("-", cmd_turtle_right))
    l_sys.generate_path(9)
    print(l_sys.state)
    l_sys.draw_turtle( (a, -200), 90)


tree(my_t=my_t,a=-50)
#grass()
#grass(a=-450)
#grass_1(-350,-400)
#grass_2(200,-400)
#grass_1(-450,-400)
#grass_2(370,-400)
#dragon()
home()
my_t.ht()          # скрываем черепашку
ts = turtle.getscreen()
ts.getcanvas().postscript(file=str(random.randint(0,9999999))+".eps")
turtle.done()        # чтобы окно не закрывалось после отрисовки
