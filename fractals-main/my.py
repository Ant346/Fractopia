import turtle
import fract_L as fr
# ************** чтобы окно появлялось в левом верхнем углу с размерами 1200x600
width = 1200
height = 600
screen = turtle.Screen()
screen.setup(width, height, 0, 0)
# **************

t = turtle.Turtle()
t.ht()          # скрываем черепашку

pen_width = 2   # толщина линии рисования (в пикселах)
f_len = 10      # длина одного сегмента прямой (в пикселах)




#l_sys.add_rules(("F", "FF"), ("A", "F[+A][-A]"))	# для дерева 2
#l_sys.add_rules(("F", "F[+F]F[-F]F"))			# для травы 1
#l_sys.add_rules(("F", "FF-[-F+F+F]+[+F-F-F]"))		# для травы 2


# Рисуем дерево 1
angle = 33	# для дерева (1 и 2)
axiom = "F"	# для дерева и трав
l_sys = fr.LSystem2D(t, axiom, pen_width, f_len, angle)
l_sys.add_rules(("F", "F[+F][-F]"))			# для дерева 1
l_sys.generate_path(5)
print(l_sys.state)

l_sys.draw_turtle( (0, -200), 90)

turtle.done()        # чтобы окно не закрывалось после отрисовки