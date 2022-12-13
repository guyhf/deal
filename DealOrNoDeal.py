import random
import tkinter


class Case(object):
    def __init__(self, number, amount, game):
        self.number = number
        self.amount = amount
        self.revealed = False
        self.chosen = False
        self.game = game
        self.button = tkinter.Button(self.game.root, text = str(self.number), command=self.reveal)
        self.update_offer = game.update_offer

    def reveal(self):
        if not self.chosen:
            self.revealed = True
            self.button.config(text = f"[ ${str(self.amount)} ]")
            self.game.update_offer()

    def choose(self):
        self.chosen = True
        self.button.config(text = f"[ Your Case ]")

    def __str__(self):
        if self.revealed:
            s = f"${self.amount}"
        elif self.chosen:
            s = f"[Your Case]"
        else:
            s = f"[case {self.number}]"
        return s




    
    


class Game(object):

    def __init__(self, amounts) -> None:
        self.deal = False
        self.offer = 0
        self.root = tkinter.Tk()
        self.amounts = list(amounts)
        self.offer_var = tkinter.StringVar()
        self.offer_var.set(f"Offer is $0")
        self.offer_label = tkinter.Label(self.root, textvariable=self.offer_var)
        self.instruction_var = tkinter.StringVar()
        self.instruction_var.set("Choose 4 cases to eliminate")
        self.instruction_label = tkinter.Label(self.root, textvariable=self.instruction_var)
        self.spacer = tkinter.Label(self.root, text="", pady=4)
        self.num_to_choose = 4
        self.shuffled = list(amounts)
        random.shuffle(self.amounts)
        self.cases = []
        self.setup()

    def run(self):
        self.root.mainloop()

    def switch_screens(self):
        self.chooseBoxLabel.pack_forget()
        self.confirmBox.pack_forget()
        self.chooseBoxMenu.pack_forget()
        self.drawCases()
        self.update_offer()
        self.spacer.pack()
        #spacer is for formatting
        self.instruction_label.pack()



    def __str__(self) -> str:
        return "-".join([str(c) for c in self.cases])

    def number_revealed(self):
        n = 0
        for case in self.cases:
            if case.revealed:
                n = n + 1
        return n

    def get_chosen_case(self):
        for case in self.cases:
            if case.chosen:
                return case
        return None
 
    def displayCases(self):
        for case in self.cases:
            case_label = tkinter.Label(self.root, text=case)
            case_label.pack()

    def choiceCallback(self, selection):
        self.choice = selection

    def drawCases(self):
        self.cases = []
        for i, amount in enumerate(self.amounts, 1):
            case = Case(i, amount, self)
            case.button.pack()
            if self.choice == i:
                case.choose()
            self.cases.append(case)

    def end(self):
        self.root.destroy()

    def update_offer(self):
        total = 0
        count = 0
        for c in self.cases:
            if not c.revealed:
                total += c.amount
                count += 1
        self.offer = round((total / count) * random.uniform(.8, .9))
        self.offer_var.set(f"Offer is ${self.offer}")
        nrevealed = self.number_revealed()
        remaining = self.num_to_choose - nrevealed
        if remaining == 0:
            self.offer_screen()
        else:
            self.instruction_var.set(f"Choose {remaining} cases")

    def setup(self):
        self.root.title("Deal or No Deal!")
        self.root.geometry("800x800")
        self.choose_case()

    def choose_case(self):
        nrevealed = self.number_revealed()
        if nrevealed < 8:
            n_to_reveal = 8 - nrevealed
        self.chooseBoxLabel = tkinter.Label(
            self.root,
            text = """Welcome to Deal or No Deal!
            Choose your case, 1-10 with amounts $1-$1000
            """)
        boxChoice = tkinter.StringVar()
        boxChoiceList = range(1,11)
        self.chooseBoxMenu = tkinter.OptionMenu(self.root, boxChoice, *boxChoiceList, command = self.choiceCallback)
        self.chooseBoxLabel.pack()
        self.chooseBoxMenu.pack(expand=True)
        self.confirmBox = tkinter.Button(self.root, text = "Confirm", command = self.switch_screens)
        self.confirmBox.pack()

    def offer_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.offer_label = tkinter.Label(self.root,
                                         textvariable=self.offer_var)
        self.offer_label.pack()
        self.deal_button = tkinter.Button(self.root, text="Deal!", command=self.make_deal)
        self.deal_button.pack()
        no_deal_button = tkinter.Button(self.root, text="No Deal!", command=self.make_no_deal)
        no_deal_button.pack()
        spacer = tkinter.Label(self.root, text="", pady=4)
        spacer.pack()
        self.displayCases()


    def make_deal(self):
        newWindow = tkinter.Toplevel(self.root)
        newWindow.title("Deal is Made!")
    
        # sets the geometry of toplevel
        newWindow.geometry("500x500")
    
        tkinter.Label(newWindow,
            text =f"You win ${self.offer}").pack()

        your_case = self.get_chosen_case()
        tkinter.Label(newWindow,
            text =f"Your case had ${your_case.amount}").pack()

        # A Label widget to show in toplevel
        tkinter.Label(newWindow,
            text ="Thanks for playing!").pack()

        tkinter.Button(newWindow, text = "Done", command = self.end).pack()

    def make_no_deal(self):
        newWindow = tkinter.Toplevel(self.root)
        newWindow.title("You chose to keep your case!")
    
        # sets the geometry of toplevel
        newWindow.geometry("500x500")
    
        your_case = self.get_chosen_case()
        tkinter.Label(newWindow,
            text =f"You win ${your_case.amount}").pack()

        tkinter.Label(newWindow,
            text =f"You turned down a deal for ${self.offer}").pack()

        # A Label widget to show in toplevel
        tkinter.Label(newWindow,
            text ="Thanks for playing!").pack()

        tkinter.Button(newWindow, text = "Done", command = self.end).pack()



amounts = [1,2,5,10,25,50,100,250,500,1000]
game = Game(amounts)
game.run()