import tkinter as tk
import os
import pygame

#ΚΛΑΣΗ
class Tamagotchi:
    def __init__(self,root_window):
        self.root=root_window
        self.root.title="My Tamagotchi Pet"
        self.hunger=100
        self.happiness=100
        self.energy=100
        self.alive=True
        pygame.mixer.init()


        

        #ΚΛΕΙΣΙΜΟ ΠΑΙΧΝΙΔΙΟΥ ΜΕ ESCAPE
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        #ΦΟΡΤΩΣΗ ΕΙΚΟΝΩΝ ΓΙΑ ΤΟ ΖΩΟ

    
        #EIKONA
        self.img_normal = tk.PhotoImage(file="normalcat.png") 
        self.img_happy = tk.PhotoImage(file="happycat.png")
        self.img_angry = tk.PhotoImage(file="angrycat.png")   
        self.img_sad = tk.PhotoImage(file="sadcat.png")
        self.img_eat=tk.PhotoImage(file="eatcat.png")
        self.img_sleep=tk.PhotoImage(file="sleepcat.png")
        self.img_dead=tk.PhotoImage(file="dead.png")


         
        #EMΦΑΝΙΣΗ ΣΤΗΝ ΟΘΟΝΗ
        self.canvas = tk.Canvas(
            self.root, 
            width=200, 
            height=200,
            bg="#F9C1C9", # Απαλό ροζ χρώμα (ή γράψε "pink")
            highlightthickness=0  
        )
        self.canvas.pack(fill="both", expand=True)

        self.cat_display = self.canvas.create_image(100, 100, image=self.img_normal)
    
        #ΣΥΝΔΕΣΗ ΤΟΥ ΠΟΝΤΙΚΟΥ ΓΙΑ DRAG AND DROP
        self.canvas.tag_bind(self.cat_display, "<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.cat_display, "<B1-Motion>", self.drag)
        self.canvas.tag_bind(self.cat_display, "<Double-1>", self.show_heart)
    
        #ΜΕΤΑΒΛΗΤΕΣ x,y ΓΙΑ DRAG AND DROP
        self.start_x=0
        self.start_y=0
        self.pass_time();

        #ΣΥΝΔΕΣΗ ΤΟΥ ΠΟΝΤΙΚΟΥ/ΚΟΥΜΠΙΩΝ
        self.root.bind("<f>", self.feed_pet) 
        self.root.bind("<s>", self.sleep_pet) 
        self.root.bind("<F>", self.feed_pet) 
        self.root.bind("<S>", self.feed_pet) 
        self.root.focus_set()

    def play_my_sound(self,file_name):
        if os.path.exists(file_name):
            pygame.mixer.Sound(file_name).play()

    #ΚΙΝΗΣΗ ΤΟΥ ΖΩΟΥ
    def start_drag(self,event):

        self.start_x=event.x
        self.start_y=event.y

    def drag(self, event):

        deltax = event.x - self.start_x
        deltay = event.y - self.start_y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    #ΚΙΝΗΣΗ ΤΗΣ ΜΠΑΛΑΣ
    
    
    #PASS TIME

    def pass_time(self):

        if not self.alive:
            return 
        
        self.hunger=max(0,self.hunger-10)
        self.energy=max(0,self.energy-5)
        self.happiness=max(0,self.happiness-5)
        print(f"HUNGER😋 {self.hunger}% | ENERGY🤪{self.energy}% | HAPINESS😁{self.happiness}%")
        
        #ΕΛΕΓΧΟΣ ΘΑΝΑΤΟΥ
        if self.energy<=0 or self.hunger<=0:
            self.alive=False;
            self.canvas.itemconfig(self.cat_display, image=self.img_dead)
            print("YOUR PET DIED.... 💀🕊🪦")
            
            return 

        self.check_mood()
        self.root.after(10000, self.pass_time)

    # CHECK MOOD

    def check_mood(self):
        if not self.alive:
            return 
        if self.hunger<30:
            print("I AM HUNGRY!!!🤬")
            self.canvas.itemconfig(self.cat_display, image=self.img_angry)

        elif self.energy<30:
            print("I WANT TO SLEEP!!!😴")
            self.canvas.itemconfig(self.cat_display, image=self.img_sad)

        elif self.happiness<50:
            print("I WANT TO PLAY!!!🥺")
            self.canvas.itemconfig(self.cat_display, image=self.img_sad)
        else:
            self.canvas.itemconfig(self.cat_display, image=self.img_normal)

    #HEART

    def show_heart(self,event):
        if self.alive:
            ###ΗΧΟΣ ΚΑΙ ΕΙΚΟΝΑ ΚΑΡΔΙΑ
            self.happiness= min (100,self.happiness+20)
            self.canvas.itemconfig(self.cat_display, image=self.img_happy)
            self.root.after(500, self.check_mood)
            self.play_my_sound("angrymeow.mp3")
            return 
    
    #SLEEP

    def sleep_pet(self,event):
        if not self.alive:
            return
        self.energy=min (100,self.energy+35)
        self.canvas.itemconfig(self.cat_display, image=self.img_sleep)
        self.root.after(10000, self.check_mood)
        self.play_my_sound("meow1.mp3")
        #ΕΙΚΟΝΑ ΚΑΙ ΤΡΑΓΟΥΔΙΙΙ
        

    # FOOD

    def feed_pet(self,event):
        if not self.alive:
            return 
        self.hunger = min(100, self.hunger + 25)
        #ΕΙΚΟΝΑ ΚΑΙ ΤΡΑΓΟΥΔΙΙΙ
        self.root.after(500, self.check_mood)
        self.canvas.itemconfig(self.cat_display, image=self.img_eat)
        self.play_my_sound("meoweating.mp3")

    #PLAY 
if __name__ == "__main__":
    root = tk.Tk()
    app = Tamagotchi(root)
    
    if os.path.exists("gia_thn_annoula_mou.mp3"):
        pygame.mixer.music.load("gia_thn_annoula_mou.mp3")
        pygame.mixer.music.play(loops=-1)
        
    root.mainloop()

    


    