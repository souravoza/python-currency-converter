#backup plan
import requests 
from tkinter import *
import tkinter as tk
from tkinter import ttk


class RealTimeCurrencyConverter():
    def __init__(self, url):
            self.data = requests.get(url).json()
            self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency] 
  
      
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = ('Currency Converter')
        self.currency_converter = converter

        self.geometry("500x365")
        self.resizable(width=False, height=False)  # Add this line

        self.configure(bg="whitesmoke")
        self.background_image = tk.PhotoImage(file='bunny.gif')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Rest of the code...


    
        self.intro_label = Label(self, text='Currency converter', relief='raised', fg='#070700', justify=tk.CENTER, borderwidth=5)
        self.intro_label.config(font=('arial',20,'bold'))

        self.intro_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        # Bind events for the 3D relief effect and the hover transparency effect
        self.intro_label.bind('<Enter>', lambda e: self.intro_label.config(bg='white', relief='sunken'))
        self.intro_label.bind('<Leave>', lambda e: self.intro_label.config(bg=self.cget('bg'), relief='raised'))

        

        
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self, bd = 3, relief = tk.RIDGE, justify = tk.CENTER, validate='key', validatecommand=valid)
        self.converted_amount_field_label = Label(self, text = '', fg = '#070700', bg = 'ghostwhite', relief = tk.RIDGE, justify = tk.CENTER, width = 18, borderwidth = 3)

       
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("USD") # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("INR") # default value

        font = ("arial", 11, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable, values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 15, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable, values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 13, justify = tk.CENTER)

       
        self.from_currency_dropdown.place(x = 30, y= 120)
        self.amount_field.place(x = 30, y = 150)
        self.to_currency_dropdown.place(x = 340, y= 120)
        self.converted_amount_field_label.place(x = 340, y = 150)
        

        self.convert_button = Button(self, text = "Convert", fg = "#070700", activeforeground="ghostwhite", activebackground="#070700", command = self.perform) 
        self.convert_button.config(font=('arial', 11, 'bold'))
        self.convert_button.place(x = 223, y = 135)

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text = str(converted_amount))
    
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return string=="" or (string.count('.')<=1 and result is not None)

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    App(converter)
    mainloop()
