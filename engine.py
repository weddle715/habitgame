'''
  Habit game core

  Dependencies: landing_page.py
                file_parser.py
'''

#import landing_page.py
import os.path
from datetime import date #For timestamps
from file_parser import *
from tkinter  import *
from tkinter.ttk import *
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders
from work_space import *
from landing_page import *
from generic_list import *
from shop import *
import authenticate

class Character:
    """
      Class for Habit character profile

      Variables:
        name: Name of character       (string)
        cash: Total currency          (int)
        exp: Total experience points  (int)
        level: Current level          (int)
        habits: Current habits        (list of Habit objects)
        tasks:                        (list of Task objects)
        dailies:                      (list of Daily objects)
        items: Owned (soft|hard)ware  (list of Item objects)
    """
    def __init__(self, name):
        self.name = name
        self.cash = 0
        self.exp = 0
        self.level = 1
        self.habits = []
        self.tasks = []
        self.dailies = []
        self.items = []


    def serialize(self):
        """
        Serializes class properties to a dictionary 
        which can then be converted to a string
        """
        character_dict = {'name': self.name,
                          'cash': self.cash,
                          'exp' : self.exp,
                          'level' : self.level,
                          'habits': None,
                          'tasks': None,
                          'dailies': None,
                          'items': None}

        habits_list = []
        tasks_list = []
        dailies_list = []
        items_list = []
        
        for habit in self.habits:
            habits_list.append(habit.serialize())

        for task in self.tasks:
            tasks_list.append(task.serialize())

        for daily in self.dailies:
            dailies_list.append(daily.serialize())

        for item in self.items:
            items_list.append(item.serialize())

        character_dict['habits'] = habits_list
        character_dict['tasks'] = tasks_list
        character_dict['dailies'] = dailies_list
        character_dict['items'] = items_list
        
        return character_dict


    def show_info(self):
        """
        Displays the characters current information:
        Cash, name, experience, level, habits, and items
        """
        print("Player Info:")
        print("Name:       "+self.name)
        print("Cash:      $"+str(self.cash))
        print("Experience: "+str(self.exp))
        print("Level:      "+str(self.level))
        print("\n\nHabits:\n-------")
        self.show_habits()
        print("\n\nTasks:\n-------")
        self.show_tasks()
        print("\n\nDailies:\n-------")
        self.show_dailies()
        print("\n\nItems:\n------")
        self.show_items()


    def add_habit(self, habit):
        if len(self.habits) != 0:
            habit.id = len(self.habits) 
        
        self.habits.append(habit)
        return habit.ID

    def add_task(self, task):
        if len(self.tasks) != 0:
            task.id = len(self.tasks) 
        
        self.tasks.append(task)
        return task.ID

    def add_daily(self, daily):
        if len(self.dailies) != 0:
            daily.id = len(self.dailies) 
        
        self.dailies.append(daily)
        return daily.ID

    def remove_habit(self, habit_ID):
        try:
            hab_id = self.habits.pop(habit_ID).ID
            self.set_habit_IDs()
            return hab_id
        except:
            print("Hello")
            print("Invalid habit id!")
            return -1

    def remove_task(self, task_ID):
        try:
            task_id = self.tasks.pop(task_ID).ID
            self.set_task_IDs()
            return task_id
        except:
            print (task_ID)
            print("Invalid task id!")
            return -1

    def remove_daily(self, daily_ID):
        try:
            daily_id = self.dailies.pop(daily_ID).ID
            self.set_daily_IDs()
            return daily_id
        except:
            print("Hello2")

            print("Invalid daily id!")
            return -1

    def get_habit(self, habit_ID):
        try:
            habit = self.habits[habit_ID]
            return habit
        except:
            print("Error: Invalid habit id")

    def get_task(self, task_ID):
        try:
            task = self.tasks[task_ID]
            return task
        except:
            print("Error: Invalid task id")

    def get_daily(self, daily_ID):
        try:
            daily = self.dailies[daily_ID]
            return daily
        except:
            print("Error: Invalid daily id")


    def set_habit_IDs(self):     
        for habit in enumerate(self.habits):
            habit[1].ID = habit[0]

    def set_task_IDs(self):     
        for task in enumerate(self.tasks):
            task[1].ID = task[0]

    def set_daily_IDs(self):     
        for daily in enumerate(self.dailies):
            daily[1].ID = daily[0]


    def show_habit(self, habit_id):
        try:
            habit = self.habits[habit_id]
            print("Title:        " + habit.title)
            print("Description: " + habit.description)
            print("ID:          " + str(habit.ID))
            print("Timestamp:   " + str(habit.timestamp))
            print("Value:       " + str(habit.value))
            print("Exp Pts:     " + str(habit.exp))

        except:
            print("Error: Invalid habit_id")

    def show_task(self, task_id):
        try:
            task = self.tasks[task_id]
            print("Title:        " + task.title)
            print("Description: " + task.description)
            print("ID:          " + str(task.ID))
            print("Timestamp:   " + str(task.timestamp))
            print("Value:       " + str(task.value))
            print("Exp Pts:     " + str(task.exp))

        except:
            print("Error: Invalid task_id")

    def show_daily(self, daily_id):
        try:
            daily = self.dailies[daily_id]
            print("Title:        " + daily.title)
            print("Description: " + daily.description)
            print("ID:          " + str(daily.ID))
            print("Timestamp:   " + str(daily.timestamp))
            print("Value:       " + str(daily.value))
            print("Exp Pts:     " + str(daily.exp))

        except:
            print("Error: Invalid daily_id")

    def show_habits(self):
        for habit in self.habits:
            self.show_habit(habit.ID)

    def show_tasks(self):
        for task in self.tasks:
            self.show_task(task.ID)

    def show_dailies(self):
        for daily in self.dailies:
            self.show_daily(daily.ID)

    def add_item(self, item):
        if len(self.items) != 0:
            item.ID = len(self.items)
        
        self.items.append(item)
        return item.ID

    def remove_item(self, item_ID):
        try:
            item_id = self.items.pop(item_ID).ID
            self.set_item_IDs()
            return item_id
        except:
            print("Invalid item id!")
            return -1

    def get_item(self, item_ID):
        try:
            item = self.items[item_ID]
            return self.items[item_ID]
        except:
            print("Error: Invalid item ID")


    def set_item_IDs(self):
        for item in enumerate(self.items):
            item[1].ID = item[0]

 
    def show_item(self, item_ID):
        
        try:
            item = self.items[item_ID]
            print("Name:   " + item.name)
            print("ID:     " + str(item.ID))
            print("Value:  " + str(item.value))
            print("Uses:   " + str(item.uses))
        except:
            print("Error: Invalid item ID")

    def show_items(self):
        for item in self.items:
            self.show_item(item.ID)


class Habit:
    """
      Class for Individual Habits

      Variables:
        title: Name of habit                         (string)
        description: Short description of habit      (string) 
        ID: Number to hold index in                  (int)
        timestamp: Last-accessed date                (date)
        value: Cash reward/penalty                   (int)
        exp: Experience point value                  (int)
    """
    def __init__(self, title, desc, value, exp, ID=0):
        self.title = title
        self.description = desc
        self.ID = ID
        self.timestamp = date.today()
        self.value = value
        self.exp = exp

    def serialize(self):
        """
        Serializes class properties to a dictionary 
        which can be converted to a string
        """
        habit_dict = {'title':self.title,
                      'desc':self.description,
                      'ID'  :self.ID,
                      'timestamp':str(self.timestamp),
                      'value':self.value,
                      'exp':self.exp}
        
        return habit_dict


class Task:
    """
      Variables:
        title: Name of habit                         (string)
        description: Short description of habit      (string) 
        ID: Number to hold index in                  (int)
        timestamp: Last-accessed date                (date)
        value: Cash reward/penalty                   (int)
        exp: Experience point value                  (int)
    """
    def __init__(self, title, desc, value, exp, ID=0):
        self.title = title
        self.description = desc
        self.ID = ID
        self.timestamp = date.today()
        self.value = value
        self.exp = exp

    def serialize(self):
        """
        Serializes class properties to a dictionary 
        which can be converted to a string
        """
        task_dict = {'title':self.title,
                      'desc':self.description,
                      'ID'  :self.ID,
                      'timestamp':str(self.timestamp),
                      'value':self.value,
                      'exp':self.exp}
        
        return task_dict


class Daily:
    """
      Variables:
        title: Name of habit                         (string)
        description: Short description of habit      (string) 
        ID: Number to hold index in                  (int)
        timestamp: Last-accessed date                (date)
        value: Cash reward/penalty                   (int)
        exp: Experience point value                  (int)
    """
    def __init__(self, title, desc, value, exp, ID=0):
        self.title = title
        self.description = desc
        self.ID = ID
        self.timestamp = date.today()
        self.value = value
        self.exp = exp

    def serialize(self):
        """
        Serializes class properties to a dictionary 
        which can be converted to a string
        """
        daily_dict = {'title':self.title,
                      'desc':self.description,
                      'ID'  :self.ID,
                      'timestamp':str(self.timestamp),
                      'value':self.value,
                      'exp':self.exp}
        
        return daily_dict

    
class Item:
    """
      Class for purchasable software/hardware

      Variables:
        name: Name of item                                (string)
        ID: Number to hold index in itemlist              (int)
        image: Name of accompanying image                 (string)
        value: Currency value of item                     (int)
        uses: Uses before item expires [-1 for infinite]  (int)
        effect: Special function that the item performs   (function)
    """
    def __init__(self, name, image, value, uses, effect = None):
        self.name = name
        self.ID = 0
        self.image = image
        self.value = value
        self.uses = uses
        self.effect = effect

    def serialize(self):
        """
        Serializes class properties to a dictionary
        which can be converted to a string
        """
        item_dict = {'name':self.name,
                      'ID':self.ID,
                      'image':self.image,
                      'value':self.value,
                      'uses':self.uses,
                      'effect':self.effect}
        
        return item_dict


class Game_Data:
    """
    Class for main game functions
    """
    def __init__(self):
        self.savefile = 'character.xml'
        self.character_data = {}
        self.token = ''
        
    def save_data(self, character):
        """
        Saves the current character data to
        Game_Data's character_data 
        """
        self.character_data = character.serialize()
        print("Character data saved")
        
    def save_to_file(self):
        """
        Saves character_data to file
        """
        try:
            file_parser.update_file(self.character_data)
            
        except:
            self.error
        
    def load_data(self):
        """
        Loads character_data from file with
        XML parser. Stores results into
        character_data dict
        """
        try:
            data = file_parser(self.savefile)
            self.character_data['habits'] = data.parse_tasks()
            self.character_data['name'] = data.parse_name()
            self.token = data.parse_token()
            self.character_data['level'] = data.parse_level()
            self.character_data['exp'] = data.parse_exp()
            self.character_data['cash'] = data.parse_cash()
            
            #return self.build_character(self.character_data)
        
        except:
            self.error('Failed to load data')


    def build_character(self, character_data):
        """
        Builds a character object from the Game_Data's 
        character_data. 
        """
        try:
            new_character = Character(character_data['name'])
            new_character.level = character_data['level']
            new_character.exp = character_data['exp']
            new_character.cash = character_data['cash']
            
            for habit in character_data['habits']:
                new_habit = Habit(habit['title'],
                                  habit['description'],
                                  None,#value
                                  None,#exp
                                  None,#habit_type
                                  habit['index'])
            
                new_character.add_habit(new_habit)
            '''
            for item in character_data['items']:
                new_item = Item(item['name'],
                                item['image'],
                                item['value'],
                                item['uses'],
                                item['effect'])
            
                new_character.add_item(new_item)
            '''
            return new_character

        except:
            self.error("Failed to build character from" \
                       " default character data")
    
    def error(self, error_message):
        print("ERROR:", error_message)


def load(name):
    """
    Loads a default character data configuration. 
    Used for debugging
    """
    new_character = Character(name)
    
    habit_1 = Habit('Read More','Read more books', 50, 10, 0)  
    habit_2 = Habit('Veggies', 'Eat more veggies', 100, 15, 1)
    habit_3 = Habit('Sleep more', 'Get more sleep', 20, 5, 2)

    task_1 = Task('Make dinner', 'and make it delicious', 10, 10, 0)

    daily_1 = Daily('Play guitar', 'hit strings in a pleasing combination', 15, 25, 0)

    item_1 = Item('Laptop', 'laptop.jpg', 5, 1)
    item_2 = Item('CAT-5 Cable', 'cat5.jpg', 4, 15)
    item_3 = Item('SSD', 'ssd.jpg', 6, 20)

    habits = []
    tasks = []
    dailies = []
    items = []

    habits.append(habit_1)
    habits.append(habit_2)
    habits.append(habit_3)

    tasks.append(task_1)

    dailies.append(daily_1)

    items.append(item_1)
    items.append(item_2)
    items.append(item_3)

    for habit in habits:
        new_character.add_habit(habit)

    for task in tasks:
        new_character.add_task(task)

    for daily in dailies:
        new_character.add_daily(daily)

    for item in items:
        new_character.add_item(item)

    return new_character


class GUI (Frame):

    def __init__(self, master, character):
        Frame.__init__(self, master)
        
        pad = 100
        
        self.character = character
        self.character_name = StringVar()
        self.character_exp = StringVar()
        self.character_cash = StringVar()
        self.character_level = StringVar()
        self.character_name.set(self.character.name)
        self.character_exp.set(self.character.exp)
        self.character_cash.set(self.character.cash)
        self.character_level.set(self.character.level)
        self._geom='800x600+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        self.master = master
        self.initUI()

        # link the shop so it can call GUI's buy_item()
        MyShop.setApp(self)
        
    def initUI(self):
        self.grid()
        self.current_visible_frame = None
        self.master.title("Daily Hack")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(5, weight=1)
        #self.columnconfigure(0, weight = 1)
        self.columnconfigure(6, pad=7)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(9, pad=7)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(4, pad=7)


        # create menu bar with file, edit, and help drop down tabs
        # temp_menu_func is the default command for all the menu options
        menu = Menu(self)

        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="New game", command=self.temp_menu_func)
        file_menu.add_command(label="Load game", command=self.temp_menu_func)
        file_menu.add_command(label="Save game", command=self.temp_menu_func)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)
        menu.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menu, tearoff=0)
        edit_menu.add_command(label="Habits", command=self.temp_menu_func)
        edit_menu.add_command(label="Dailies", command=self.temp_menu_func)
        edit_menu.add_command(label="Tasks", command=self.temp_menu_func)
        menu.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="How to play", command=self.temp_menu_func)
        help_menu.add_command(label="About", command=self.temp_menu_func)
        menu.add_cascade(label="Help", menu=help_menu)

        #self.config(menu=menu)


        # create banner
        self.banner = Frame(self, style='banner.TFrame', padding=5)
        self.banner.grid(row=0, column=0, columnspan=9, sticky='news')
        self.style.configure('banner.TFrame', background='black')

        logo_img = PhotoImage(file=os.path.join("assets", "art", "logo.gif"))
        logo_image = Label(self.banner, image=logo_img, style='hack_logo.TLabel')
        logo_image.grid(row=0, column=3,sticky='e')
        logo_image.image = logo_img
        self.style.configure('hack_logo.TLabel', background='black')

        
        # create character data frame
        self.char_frame = Frame(self)
        self.char_frame.grid(row=2, column=0, sticky='news')
        
        name_lalel = Label(self.char_frame, text="Player Name")
        name_lalel.grid(row = 0, column = 0,sticky=W, pady=4, padx=5)
        name_lalel.configure(font='arial 12')
        
        name = Label(self.char_frame, textvariable = self.character_name)
        name.grid(row = 0, column = 1, sticky=W, pady=4, padx=5)
        name.configure(font='arial 12 bold')
        
        # load character image
        char_img = PhotoImage(file=os.path.join("assets", "art", "main.gif"))
        character_image = Label(self.char_frame, image=char_img)
        character_image.grid(row=1, column=0, stick=W, padx=5)
        character_image.image = char_img


        # create stats frame; embedded in the character frame
        statsBg = Frame(self, style="statsFrame.TFrame")
        statsBg.grid(row=1, column=0, columnspan=9, sticky='we')
        statsBg.columnconfigure(0, weight=1)
        
        self.stats_frame = Frame(statsBg, style="statsFrame.TFrame")
        self.stats_frame.grid(row=0, column=0)

        # add experience stats info
        exp_label = Label(self.stats_frame, text="exp:", style="statsLabel.TLabel")
        exp_label.grid(row=0, column=0, sticky='nesw', pady=4, padx=5)
        
        exp = Label(self.stats_frame, textvariable = self.character_exp)
        exp.grid(row = 0, column=1, sticky='nesw', pady=4, padx=5)
        exp.configure(background="#3D3D3D", font="arial 12 bold", foreground='#6AA7E2')

        # add cash stats info
        cash_label = Label(self.stats_frame, text="cash:", style="statsLabel.TLabel")
        cash_label.grid(row = 0, column =2 ,sticky='nesw', pady=4, padx=5)

        cash = Label(self.stats_frame, textvariable= self.character_cash)
        cash.grid(row = 0, column =3, sticky='nesw', pady=4, padx=5)
        cash.configure(background="#3D3D3D", font="arial 12 bold", foreground='#3BB623')

        # add level stats info
        level_label = Label(self.stats_frame, text="level:", style="statsLabel.TLabel")
        level_label.grid(row = 0, column =4 ,sticky='nesw', pady=4, padx=5)

        level = Label(self.stats_frame, textvariable = self.character_level)
        level.grid(row = 0, column =5 ,sticky='nesw', pady=4, padx=5)
        level.configure(background="#3D3D3D", font="arial 12 bold", foreground='#FF7F2A')
        
        self.style.configure("statsLabel.TLabel", background="#3D3D3D", font="arial 12 bold", foreground='white')
        self.style.configure("statsFrame.TFrame", background="#3D3D3D")
        

        '''def __init__(self, name, image, value, uses, effect = None):
        self.name = name
        self.ID = 0
        self.image = image
        self.value = value
        self.uses = uses
        self.effect = effect'''
        
        '''
        #manual test for update
        item_test = Item('SSD', 'ssd.jpg', 6, 1)    
        self.complete_habit(1)
        self.buy_item(item_test)
        self.use_item(0)
        self.character.show_info()
        '''

        mb=  Menubutton(self, text="Options")
        mb.grid(row = 0, column = 6, sticky = E)
        mb.menu  =  Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
    
        mayoVar  = IntVar()
        ketchVar = IntVar()
        mb.menu.add_command( label="Home", command = self.home)
        mb.menu.add_command( label="Habits", command = self.habit)
        mb.menu.add_command( label="Dailies", command = self.dailies )
        mb.menu.add_command( label="Tasks", command = self.task )
        mb.menu.add_command( label="Shop", command = self.buy )
        mb.menu.add_command ( label="Game", command = self.no_where)
        mb.menu.add_command(label = "List", command = self.generic)
        mb.menu.add_command( label="Settings", command = self.no_where)

        # footer
        footer_frame_bg = Frame(self, style='footer.TFrame', padding=3)
        footer_frame_bg.grid(row=10, column=0, columnspan=7, sticky= (W, E))
        footer_frame_bg.columnconfigure(0, weight=1)

        # centered frame; holds logo and copyright text
        footer_frame = Frame(footer_frame_bg, style='footer.TFrame')
        footer_frame.grid()
        
        self.style.configure('footer.TFrame', background='black')

        # archetype logo 
        archetype_img = PhotoImage(file=os.path.join("assets", "art", "Archetype.gif"))
        archetype_logo = Label(footer_frame, image=archetype_img, padding="0 0 5 0")
        archetype_logo.grid(row=0, column=0, sticky=(N, E, W, S))
        archetype_logo.image = archetype_img
        archetype_logo.configure(background = 'black', foreground = 'white', anchor = CENTER)
        
        footer = Label(footer_frame, text="Copyright 2014")
        footer.grid(row=0, column=1, sticky = (N, E, W, S))
        footer.configure(background = 'black', foreground = 'white', anchor = CENTER, font='arial 12')

 
        self.frames = {}
        
        # Add main frames to grid for geometry memory
        # then remove them

        work_space_frame = Work_Space(self, self.character)
        generic_frame = Generic(self, self.character)
        landing_page_frame = Landing_Page(self, self.character)

        self.frames[Work_Space] = work_space_frame
        self.frames[Generic] = generic_frame
        self.frames[Landing_Page] = landing_page_frame
        
        self.show_frame(Landing_Page)

    """ This is the default for all menu bar options, except for exit """
    def temp_menu_func(self):
        print("test menu")
            
    def show_frame(self, c):
        '''
        Show a frame for the given class
        '''
        
        if c in ('habit', 'daily', 'task', 'shop'):
            if self.current_visible_frame != self.frames[Work_Space]: 
                self.current_visible_frame.grid_remove()
                
            frame = self.frames[Work_Space]
            frame.grid(row = 4, column = 0, columnspan = 7,
                       rowspan = 4, sticky = 'news')

            #Adjust notebook to desired tab
            frame.select_tab(c)
            self.current_visible_frame = frame
            
            
        else:
            if self.current_visible_frame != self.frames[c]:
                if self.current_visible_frame != None:
                    self.current_visible_frame.grid_remove()

                frame = self.frames[c]
                frame.grid(row = 4, column = 0, columnspan = 7,
                           rowspan = 4, sticky = 'news')
                self.current_visible_frame = frame
            
        
        
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
    
    def complete_habit(self, habit_ID):
        habit = self.character.get_habit(habit_ID)
        self.character.cash += habit.value
        self.character.exp += habit.exp
        self.character.remove_habit(habit_ID)
        self.character.set_habit_IDs()
        self.character_exp.set(self.character.exp)
        self.character_cash.set(self.character.cash)
       
        
    def use_item(self, item_ID):
        self.character.items[item_ID].uses -= 1
        if self.character.items[item_ID].uses == 0:
            self.character.remove_item(item_ID)
            self.character.set_item_IDs()
            
    def buy_item(self, item):
        if self.character.cash >= item.value:    
            self.character.add_item(item)
            self.character.cash -= item.value
            self.character.set_item_IDs()
            self.character_cash.set(self.character.cash)
            print(item.name + " bought!")
        else:
           print("Not enough cash for " + item.name + "!")

        
    def home(self):
        #Currently this goes no where, need to fix the grid_forget issue first
        self.show_frame(Landing_Page)

    def habit(self):

        self.show_frame('habit')
        

    def task(self):
        self.show_frame('task')
        

    def dailies(self):
        self.show_frame('daily')
        
    def buy(self):
        self.show_frame('shop')
        
    def generic(self):
        self.show_frame(Generic)

    def no_where(self):
        messagebox.showinfo("Placeholder", "I don't have anywhere to go yet :( !")


def main():
    """
      Stub for main function
    """

    db = authenticate.db()

    main_character = load('Tester')
   
    #Display current character's info
    #main_character.show_info()
    root = Tk()
    app = GUI(root, main_character)
    
    root.mainloop()
    

    

        
if __name__ == "__main__":
    main()

