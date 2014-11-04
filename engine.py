'''
  Habit game core

  Dependencies: landing_page.py
                file_parser.py
'''

#import landing_page.py
import os.path
from file_parser import *
from tkinter  import *
from tkinter.ttk import *
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders

from hack_classes import *
from landing_page import *
from generic_list import *
from work_space import *
import authenticate
from tkinter import filedialog # open/save file


class Game_Data:
    """
    Class for main game functions
    """
    def __init__(self):
        self.savefile = 'character.xml'
        self.character_data = {}
        self.character_data['firstname'] = ''
        self.character_data['lastname'] = ''
        self.character_data['birthday'] = ''
        self.token = ''
        self.parser = file_parser(self.savefile)
                
    def show_character_data(self):
        print(self.character_data)
        
    def save_data(self, character):
        """
        Saves the current character data to
        Game_Data's character_data 
        """
        self.character_data = character.serialize()
        self.character_data['firstname'] = self.firstname
        self.character_data['lastname'] = self.lastname
        self.character_data['birthday'] = self.birthday
        self.character_data['token'] = self.token
        
        print("Character data saved")
        
    def save_to_file(self):
        """
        Saves character_data to file
        """
        try:
            self.parser.update_file(self.character_data, self.savefile)
            
        except:
            self.error('Failed to write to file')
        
    def load_data(self):
        """
        Loads character_data from file with
        XML parser. Stores results into
        character_data dict
        """
        try:
            self.character_data['hacks'] = self.parser.parse_hacks()
            self.firstname = self.parser.parse_firstname()
            self.lastname = self.parser.parse_lastname()
            self.character_data['name'] = self.parser.parse_name()
            self.birthday = self.parser.parse_birthday()
            self.token = self.parser.parse_token()
            self.character_data['level'] = self.parser.parse_level()
            self.character_data['exp'] = self.parser.parse_exp()
            self.character_data['cash'] = self.parser.parse_cash()
            self.character_data['items'] = self.parser.parse_items()
        
        except:
            self.error('Failed to load data')


    def build_character(self):
        """
        Builds a character object from the Game_Data's 
        character_data. 
        """
        try:
            character_data = self.character_data
            new_character = Character(character_data['name'])
            new_character.level = character_data['level']
            new_character.exp = character_data['exp']
            new_character.cash = character_data['cash']
            
        
            for hack in character_data['hacks']:
                new_hack = Hack(hack['h_type'],
                                hack['title'],
                                hack['desc'],
                                hack['value'],
                                hack['exp'])
           
                new_character.add_hack(new_hack)
         
            for item in character_data['items']:
                new_item = Item(item['title'],
                                item['image'],
                                item['value'],
                                item['uses'],
                                item['effect'])
            
                new_character.add_item(new_item)
            
            #Resynchronize hack index
            if len(new_character.hacks.keys()) > 0:
                new_character.hack_index = max(new_character.hacks.keys())

            return new_character

        except:
            self.error("Failed to build character from" \
                       " default character data")
    
    def error(self, error_message):
        print("ERROR:", error_message)


        
def load_hacks():
    '''
    Loads hacks for character
    Used for debugging
    '''
    hack_1 = Hack('habit', 'Read More','Read more books', 50, 10)  
    hack_2 = Hack('habit', 'Veggies', 'Eat more veggies', 100, 15)
    hack_3 = Hack('habit', 'Sleep more', 'Get more sleep', 20, 5)

    hack_4 = Hack('task', 'Make dinner', 'and make it delicious', 10, 10)

    hack_5 = Hack('daily', 'Play guitar', 'hit strings in a pleasing combination', 15, 25)

    hacks = []
    hacks.append(hack_1)
    hacks.append(hack_2)
    hacks.append(hack_3)
    hacks.append(hack_4)
    hacks.append(hack_5)

    return hacks

def load_items():
    '''
    Loads items for character
    Used for debugging
    '''
    item_1 = Item('Laptop', 'laptop.jpg', 5, 1)
    item_2 = Item('CAT-5 Cable', 'cat5.jpg', 4, 15)
    item_3 = Item('SSD', 'ssd.jpg', 6, 20)

    items = []
    items.append(item_1)
    items.append(item_2)
    items.append(item_3)

    return items


# Placed here to resolve import loop issues with work_space, engine, and
# shop.
from work_space import *

class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)        
        pad = 100

        self.game_data = Game_Data()
        self.game_data.load_data()
        self.character = self.game_data.build_character()

        #Hacks and Items for debugging
        for hack in load_hacks():
            self.character.add_hack(hack)

        for item in load_items():
            self.character.add_item(item)

        self.character_name = StringVar()
        self.character_exp = StringVar()
        self.character_cash = StringVar()
        self.character_level = StringVar()

        self.update_name()
        self.update_exp()
        self.update_cash()
        self.update_level()
        
        self._geom='800x600+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        self.master = master
        self.initUI()
        self.bind_buttons()
        
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
        self.menu = Menu(self)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="New game", command=self.temp_menu_func)
        self.file_menu.add_command(label="Load game", command=self.temp_menu_func)
        self.file_menu.add_command(label="Save game", command=self.save_game)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.destroy)
        self.menu.add_cascade(label="FILE", menu=self.file_menu)

        self.edit_menu = Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label="Habits", command=self.temp_menu_func)
        self.edit_menu.add_command(label="Dailies", command=self.temp_menu_func)
        self.edit_menu.add_command(label="Tasks", command=self.temp_menu_func)
        self.menu.add_cascade(label="EDIT", menu=self.edit_menu)

        self.options_menu = Menu(self.menu, tearoff=0)
        self.options_menu.add_command(label="Game", command=self.no_where)
        self.options_menu.add_command(label="Settings", command=self.no_where)
        self.menu.add_cascade(label="OPTIONS", menu=self.options_menu)
         
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="How to play", command=self.temp_menu_func)
        self.help_menu.add_command(label="About", command=self.temp_menu_func)
        self.menu.add_cascade(label="HELP", menu=self.help_menu)

        self.master.config(menu=self.menu)

        # create banner
        self.banner = Frame(self, style='banner.TFrame', padding=0)
        self.banner.grid(row=0, column=0, columnspan=9, sticky='news')
        self.style.configure('banner.TFrame', background='black')

        logo_img = PhotoImage(file=os.path.join("assets", "art", "logo.gif"))
        logo_image = Label(self.banner, image=logo_img, style='hack_logo.TLabel', padding='7 7 7 6', cursor="hand2")
        logo_image.grid(row=0, column=0, sticky='e', padx=(0,30))
        logo_image.image = logo_img
        logo_image.bind('<Enter>', lambda e: logo_image.configure(background='#0F0F0F'))
        logo_image.bind('<Leave>', lambda e: logo_image.configure(background='black')) 
        logo_image.bind('<1>', lambda e: self.go_to_home()) 
        self.style.configure('hack_logo.TLabel', background='black')

        # make common 'menu bar' links
        def make_menu(col_number, name, function):
            menu_title = Label(self.banner, padding='12 7 12 7', cursor='hand2', text=name)
            menu_title.configure(background='black', foreground='#EBEBEB', font='arial 12 bold')
            menu_title.bind('<Enter>', lambda e: menu_title.configure(background='#0F0F0F', foreground='#FFD237'))
            menu_title.bind('<Leave>', lambda e: menu_title.configure(background='black', foreground='#EBEBEB'))
            menu_title.bind('<1>', lambda e: function())
            menu_title.grid(row=0, column=col_number+1, sticky='e')

        menu_titles = ['Home', 'Habits', 'Tasks', 'Dailies', 'List', 'Shop']
        menu_functions = [self.go_to_home,
                          self.go_to_habits,
                          self.go_to_tasks,
                          self.go_to_dailies,
                          self.go_to_generic,
                          self.go_to_shop]

        for i in range(6):
            make_menu(i, menu_titles[i], menu_functions[i])
        
        # create character data frame
        self.char_frame = Frame(self)
        self.char_frame.grid(row=2, column=0, sticky='news')
        
        self.name_label = Label(self.char_frame, text="Player Name")
        self.name_label.grid(row = 0, column = 0,sticky=W, pady=4, padx=5)
        self.name_label.configure(font='arial 12')
        
        self.name = Label(self.char_frame, textvariable = self.character_name)
        self.name.grid(row = 0, column = 1, sticky=W, pady=4, padx=5)
        self.name.configure(font='arial 12 bold')
        
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
        exp.configure(background="#283D57", font="arial 12 bold", foreground='#C5BD25')

        # add cash stats info
        
        cash_label = Label(self.stats_frame, text="cash:", style="statsLabel.TLabel")
        cash_label.grid(row = 0, column =2 ,sticky='nesw', pady=4, padx=5)
        cash = Label(self.stats_frame, textvariable= self.character_cash)
        cash.grid(row = 0, column =3, sticky='nesw', pady=4, padx=5)
        cash.configure(background="#283D57", font="arial 12 bold", foreground='#3BB623')
        
        # add level stats info
        level_label = Label(self.stats_frame, text="level:", style="statsLabel.TLabel")
        level_label.grid(row = 0, column =4 ,sticky='nesw', pady=4, padx=5)

        level = Label(self.stats_frame, textvariable = self.character_level)
        level.grid(row = 0, column =5 ,sticky='nesw', pady=4, padx=5)
        level.configure(background="#283D57", font="arial 12 bold", foreground='#FF7F2A')
        
        self.style.configure("statsLabel.TLabel", background="#283D57", font="arial 12 bold", foreground='white')
        self.style.configure("statsFrame.TFrame", background="#283D57")
        
        
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
        
        
        work_space_frame = Work_Space(self, self.character)
        generic_frame = Generic(self, self.character)
        landing_page_frame = Landing_Page(self, self.character)

        self.frames['Work_Space'] = work_space_frame
        self.frames['Generic'] = generic_frame
        self.frames['Landing_Page'] = landing_page_frame
        self.show_frame('Landing_Page')
        

    def bind_buttons(self):
        #Navigation Buttons
        landing_page = self.frames['Landing_Page']
        landing_page.go_to_habits_button.bind("<1>", lambda e : self.page_navigator('habit'))
                                                             
        landing_page.go_to_dailies_button.bind("<1>", lambda e : self.page_navigator('daily'))

        landing_page.go_to_tasks_button.bind("<1>", lambda e : self.page_navigator('task'))

    def update_cash(self):
        self.character_cash.set(str(self.character.cash))

    def update_name(self):
        self.character_name.set(self.character.name)

    def update_exp(self):
        self.character_exp.set(self.character.exp)

    def update_level(self):
        self.character_level.set(self.character.level)

    def remove_hack(self, hack_type, ID):
        #messagebox.showinfo("Hack Info", "Hack:"+hack_type+" "+str(ID))
        self.character.remove_hack(ID)
        self.redraw()
        
    def page_navigator(self, page):
        if page == 'habit':
            self.show_frame('habit')
            
        elif page == 'daily':
            self.show_frame('daily')
            
        elif page == 'task':
            self.show_frame('task')
            
        else:
            pass
    
    def redraw(self):
        """
        Redraws each area of the GUI after data is modified
        """
        self.frames['Landing_Page'].redraw(self.character)
        #self.frames['Work_Space'].redraw(self.character)
        #self.frames['Generic'].redraw(self.character)
        
        
    """ This is the default for all menu bar options,
    except for exit """
    def temp_menu_func(self):
        print("test menu")
            
    def show_frame(self, frame_class):
        '''
        Show a frame for the given frame class
        '''
        
        if frame_class in ('habit', 'daily', 'task', 'shop'):
            if self.current_visible_frame != self.frames['Work_Space']: 
                self.current_visible_frame.grid_remove()
                
            frame = self.frames['Work_Space']
            frame.grid(row = 4, column = 0, columnspan = 7,
                       rowspan = 4, sticky = 'news')

            #Adjust notebook to desired tab
            frame.select_tab(frame_class)
            self.current_visible_frame = frame
            
            
        else:
            if self.current_visible_frame != self.frames[frame_class]:
                if self.current_visible_frame != None:
                    self.current_visible_frame.grid_remove()

                frame = self.frames[frame_class]
                frame.grid(row = 4, column = 0, columnspan = 7,
                           rowspan = 4, sticky = 'news')
                self.current_visible_frame = frame
            
        
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
        
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

        
    def go_to_home(self):
        self.show_frame('Landing_Page')

    def go_to_habits(self):
        self.show_frame('habit')


    def go_to_tasks(self):
        self.show_frame('task')
        main.__subclasshook__

    def go_to_dailies(self):
        self.show_frame('daily')
        
    def go_to_shop(self):
        self.show_frame('shop')
        
    def save_game(self):
        messagebox.showinfo("Save", "Game Saved!")  
        self.game_data.save_data(self.character)
        self.game_data.save_to_file()
        
    def go_to_generic(self):
        self.show_frame('Generic')

    def no_where(self):
        messagebox.showinfo("Placeholder", "I don't have anywhere to go yet :( !")


def main():
    """
      Stub for main function
    """
    db = authenticate.db()

    #main_character = load('Tester')
   
    root = Tk()
    app = GUI(root)
    
    root.mainloop()

        
if __name__ == "__main__":
    main()

# These imports have been moved to resolve import loops between
# shop, work_space, and engine over the Item class.
from shop import *
