from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits
from ruffier import test
from runner import Runner
from seconds import Seconds
from sits import Sits
txt_index = "Ваш индекс Руфье: "
txt_workheart = "Работоспособность сердца: "
txt_nodata = '''
нет данных для такого возраста'''
txt_res = [] 
txt_res.append('''низкая. 
Срочно обратитесь к врачу!''')
txt_res.append('''удовлетворительная. 
Обратитесь к врачу!''')
txt_res.append('''средняя. 
Возможно, стоит дополнительно обследоваться у врача.''')
txt_res.append('''
выше среднего''')
txt_res.append('''
высокая''')
P1 = 0
P2 = 0
P3 =0
global name
global age
global P1, P2, P3
def ruffier_index(P1, P2, P3):
    return (4 *(P1+P2+P3) -200)/10
def neud_level(age):
    norm_age = (min(age, 15) - 7) // 2
    result = 21 - norm_age * 1.5
def ruffier_result(r_index, level):
    if r_index >= level:
        return 0
    level = level - 4
    if r_index >= level:
        return 1
    level = level - 5
    if r_index >= level:
        return 2
    level = level - 5.5
    if r_index >= level:
        return 3
    return 4
    pass
class Result(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.instr = Label(text = '')
    self.on_enter = self.before
def before(self):
    final_str = txt_index + str(ruffier_index(P1, P2, P3)) + '\n' + txt_res[ruffier_result(ruffier_index(P1, P2, P3), neud_level(age))]
    self.instr.text = final_str
class Seconds(Label):
    done = BooleanProperty(False)
    def __init__(self, total, **kwargs):
        self.total = total
        self.current = 0
        super().__init__(text="Прошло секунд: 0")
    def start(self):
        Clock.schedule_interval(self.change, 1)
    def change(self, dt):
        self.current += 1
        self.text = "Прошло секунд: " + str(self.current)
        if self.current >= self.total:
            self.done = True
            return False 
    def __init__(self, total, **kwargs):
        self.total = total
        self.current = 0
        my_text = "Прошло секунд: " + str(self.current)
        super().__init__(text=my_text)
class Runner(BoxLayout):
    value = NumericProperty(0)
    finished = BooleanProperty(False)
    def __init__(self,total =10,steptime=1,**kwargs):
        self.total = total
        self.animation(Animateion(pos_hint={"top":0.1},duration=steptime/2)+Animateion(pos_hint={'top':1.0},duration=steptime/2)) 
        self.btn= Label(text="Бег")
        self.add_widget(self.btn)
        self.animation.on_progress = self.next
        super().__init__(**kwargs)
    def start(self):
        self.value =0
        self.finished=False
        self.animation.repeat=True
        self.animation.start(self.btn)
    def next(self,*args, widget, step):
        if step == 1.0:
            self.value +=1
            if self.value>=self.total:
                self.animation.repeat=False
                self.rinished = True
class PulseScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done=self.sec_finished)
    def sec_finished(self, *args):
        if self.lbl_sec.done:
            print("Таймер завершён!")
class Scr(Screen):
    def __init__(self, t_text, b_text, next_screen, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=100,spacing=10)
        bnt1 = Button(text="",size_hint(None,None),width=200,height=40)
        self.textik =Label(text='')
        self.input_field_1 = TextInput(hint_text="",size_hint_y=None,height=40)
        self.input_field_2 = TextInput(hint_text="",size_hint_y=None,height=40)
        bnt1.bind(on_press=self.goto_screen1)
        self.check_age()
        layout.add_widget(self.textik)
        layout.add_widget(self.input_field_1)
        layout.add_widget(self.input_field_2)
        layout.add_widget(bnt1)
        layout.add_widget(Label(text=t_text))
        self.add_widget(layout)
    def goto_screen1(self):
        self.manager.current = 'screen1'
    def check_age(self):
        age_text = self.input_field_2.text.strip()
        if not age_text:
            return False
        try:
            age = int(age_text)
        except ValueError:
            return False
        if 7 <= age <=100:
            return True
        else:
            return False
class Screen1(Screen,Seconds,PulseScr):
    def goto_screen2(self):
        self.manager.current = 'screen2'
class Screen2(Screen,Seconds,PulseScr):
    def goto_screen3(self):
        self.manager.current = 'screen3'
class Screen3(Screen,Seconds,PulseScr):
    def goto_screen4(self):
        self.manager.current = 'screen4'
class Screen4(Screen,Seconds,PulseScr):
class HeartCheck(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Scr(txt_instruction, 'Начать', 'p1', name='instr'))
        sm.add_widget(Scr(txt_test1, 'Далее', 'sits', name='p1'))
        sm.add_widget(Scr(txt_test2, 'Далее', 'p2', name='sits'))
        sm.add_widget(Scr(txt_test3, 'Завершить', 'result', name='p2'))
        sm.add_widget(Scr('Тут будет расчет...', 'Заново', 'instr', name='result'))
        return sm

HeartCheck().run()
