import itertools, random
from timeit import default_timer as timer
#import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.base import runTouchApp


###################################################################################################
# Puzzle Area
###################################################################################################

class PuzzleCell(Label):
    def __init__(self, **kwargs):
        super(PuzzleCell, self).__init__(**kwargs)
        Label.__init__(self, **kwargs)
        with self.canvas.before:
            Color(0, 0, 0)
            self.pn_bg = Rectangle(size_hint_x=.1, size_hint_y=.1)
        self.bind(size=self._update_pn_bg, pos=self._update_pn_bg)
        #
        self.nodes = {}
        self.randomize = False
        self.font_name = "Gameplay.ttf"

    def _update_pn_bg(self, instance, value):
        self.pn_bg.pos = instance.pos
        self.pn_bg.size = instance.size

class PuzzleGrid(GridLayout):
    def __init__(self, puzzle, **kwargs):
        super(PuzzleGrid, self).__init__(**kwargs)
        self.spacing = 2
        self.padding = 5
        GridLayout.__init__(self, cols=9, rows=9);
        self.cells = {}
        with self.canvas.before:
            Color(1, 0, 0)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        #
        self.update_pg(puzzle.clues)
        Clock.schedule_interval(self._randomizer, .1)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _randomizer(self, event):
        for cell in self.cells:
            if self.cells[cell].randomize:
                self.cells[cell].text = random.choice("123456789")

    def update_pg(self, data):
        #                *sigh*
        # TODO: Fix this mess
        if self.cells:
            for i, c in enumerate("".join(data)):
                self.cells[i].randomize = True if c == "?" else False
                self.cells[i].text = c
        else:
            for i, c in enumerate("".join(data)):
                self.cells[i] = PuzzleCell(text=c)
                self.add_widget(self.cells[i])
                self.cells[i].randomize = True if c == "?" else False

###################################################################################################
# Logging Display Area
###################################################################################################

class LogBox(ScrollView):
    text = StringProperty("")
    def __init__(self, text, **kwargs):
        super(LogBox, self).__init__(**kwargs)
        ScrollView.__init__(self, **kwargs)
        with self.canvas.before:
            Color(0, 0, 0)
            self.lb = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_lb, pos=self._update_lb)
        self.text = text
        self.add_widget(Label( text=text))

    def _update_lb(self, instance, value):
        self.lb.pos = instance.pos
        self.lb.size = instance.size

class LogBoxContainer(GridLayout):
    def __init__(self, text,**kwargs):
        super(LogBoxContainer, self).__init__(**kwargs)
        self.padding = 5
        GridLayout.__init__(self, cols=1, rows=1)
        with self.canvas.before:
            Color(1, 0, 0)
            self.lbc_bg = Rectangle()#size=self.size, pos=self.pos)
        self.bind(size=self._update_lbc_bg, pos=self._update_lbc_bg)
        self.add_widget(LogBox(text=text))

    def _update_lbc_bg(self, instance, value):
        self.lbc_bg.pos = instance.pos
        self.lbc_bg.size = instance.size

###################################################################################################
# Right Side Menu Area
###################################################################################################

class StatusLabel(Label):
    def __init__(self, main, **kwargs):
        super(StatusLabel, self).__init__(**kwargs)
        Label.__init__(self, **kwargs)
        with self.canvas.before:
            Color(0, 0, 0)
            self.pn_bg = Rectangle(size_hint_x=.5, size_hint_y=.5)
        self.bind(size=self._update_pn_bg, pos=self._update_pn_bg)
        self.text = "STATUS"
        self.size_hint_y = None
        self.height = 50
        self.font_name = "Gameplay.ttf"

    def _update_pn_bg(self, instance, value):
        self.pn_bg.pos = instance.pos
        self.pn_bg.size = instance.size

class InfoLabel(Label):
    def __init__(self, main, **kwargs):
        super(InfoLabel, self).__init__(**kwargs)
        Label.__init__(self, **kwargs)
        with self.canvas.before:
            Color(1, 0, 0)
            self.pn_bg = Rectangle(size_hint_x=.5, size_hint_y=.5)
        self.bind(size=self._update_pn_bg, pos=self._update_pn_bg)
        self.font_name = "Gameplay.ttf"
        self.font_size = 10
        self.time = "0.00"
        self.text = "Time: " + self.time

    def update_time(self, time):
        self.time = time
        self.text = "Time: " + str(self.time)

    def _update_pn_bg(self, instance, value):
        self.pn_bg.pos = instance.pos
        self.pn_bg.size = instance.size


class SolverSelector(Button):
    def __init__(self, main, **kwargs):
        super(SolverSelector, self).__init__(**kwargs)
        #Button.__init__(self, **kwargs)
        self.font_name = "Gameplay.ttf"
        self.text = "Select Solver Here"
        self.on_release = self.drop_list
        self.main = main
        self.size_hint_y = None
        self.height = 50

    def drop_list(self):
        self.dropdown = DropDown()

        for s in self.main.puzzle.solvers:
            btn = Button(text=s, size_hint_y=None, height=44, font_name="Gameplay.ttf")
            btn.bind(on_release=lambda btn: self._update_current_solver(btn))
            self.dropdown.add_widget(btn)

        self.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self, "text", x))

    def _update_current_solver(self, btn):
        self.dropdown.select(btn.text)
        self.main.puzzle.set_solver(self.main.puzzle.solvers[btn.text])


class ButtStart(Button):
    def __init__(self, main, **kwargs):
        super(ButtStart, self).__init__(**kwargs)
        Label.__init__(self, **kwargs)
        self.main = main
        self.on_press=self.bs_clicked
        self.font_size = 20
        self.text = "START"
        self.background_color = (1,1,1,1)
        self.size_hint_x=1
        self.size_hint_y=None
        self.font_name = "Gameplay.ttf"

    def bs_clicked(self):
        self.main.puzzle.solve()

class MenuCol(GridLayout):
    def __init__(self, main, **kwargs):
        super(MenuCol, self).__init__(**kwargs)
        self.padding = 5
        GridLayout.__init__(self, cols=1, rows=6)
        with self.canvas.before:
            Color(1, 0, 0)
            self.mc_bg = Rectangle()#size=self.size, pos=self.pos)
        self.bind(size=self._update_mc_bg, pos=self._update_mc_bg)
        self.status_label = StatusLabel(main)
        self.info_label = InfoLabel(main)
        self.add_widget(self.status_label)
        self.add_widget(SolverSelector(main))
        self.add_widget(ButtStart(main))
        self.add_widget(self.info_label)
        self.spacing = 15

    def _update_mc_bg(self, instance, value):
        self.mc_bg.pos = instance.pos
        self.mc_bg.size = instance.size


###################################################################################################
# Bottom Right Area
###################################################################################################

class BotRight(Image):
    def __init__(self, **kwargs):
        super(BotRight, self).__init__(**kwargs)
        Image.__init__(self, **kwargs)
        with self.canvas.before:
            Color(1, 0, 0)
            self.r = Rectangle(size_hint_x=.1, size_hint_y=.1)
        self.bind(size=self._update_r, pos=self._update_r)
        self.spacing = 50
        self.source="soduko.png"
        self.size_hint_y = 1.5

    def _update_r(self, instance, value):
        self.r.pos = instance.pos
        self.r.size = instance.size

###################################################################################################
# Main
###################################################################################################

class Main(GridLayout):
    def __init__(self, puzzle):
        GridLayout.__init__(self, cols=2, rows = 2)
        self.font_family = "Gameplay.ttf"
        self.puzzle = puzzle
        self.puzzle.gui = self
        self.pg = PuzzleGrid(self.puzzle, size_hint_x=3, size_hint_y=4)
        self.menu_col = MenuCol(self)
        self.add_widget(self.pg)
        self.add_widget(self.menu_col)
        self.add_widget(LogBoxContainer("LOgging data would be here"))
        self.add_widget(BotRight())


class SolverApp(App):

    puzzle = None

    def build(self):
        return Main(self.puzzle)
