from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import Weather_api
import requests


class MyWeather:
    def __init__(self, root):

        self.root = root
        self.root.title("My Weather App")
        self.root.geometry("600x600+450+100")
       
        self.root.minsize(600,600)
        self.root.config(bg="light blue")

        # ======image======

        self.search_icon = Image.open("icons/search.png")
        self.search_icon = self.search_icon.resize((20, 20), Image.ANTIALIAS)
        self.search_icon = ImageTk.PhotoImage(self.search_icon)

        # ======variable========

        self.var_search = StringVar()

        title = Label(self.root, text="Weather App", font=("convection", 30, "bold"), background="#262626",
                      foreground="White", anchor="center").place(x=0, y=0, relwidth=1, height=60)

        temp_lbl= Label(self.root, background="#033953").place(x=0, y=60, relwidth=1, height=60)

        lbl_city = Label(self.root, text="City Name", font=("bookman old style", 18, "bold"), background="#033953",
                         foreground="White", anchor="w", padx=10).place(x=20, y=60, relwidth=1, height=60)

        self.txt_city = Entry(self.root, textvariable=self.var_search, font=("dubai", 17, "bold"), background="light yellow",
                              foreground="#033953", justify="center")
        self.txt_city.place(x=180, y=75, width=260, height=30)

        btn_city = Button(self.root, cursor="hand2", image=self.search_icon, bg="white",
                          activebackground="white", bd=0, command=self.get_weather).place(x=470, y=75, width=30, height=30)

        # =====result=======

        self.lbl_city = Label(self.root, font=(
            "Sans", 20, "bold"), background="light blue", foreground="black", anchor="c", padx=5)
        self.lbl_city.place(x=0, y=140, relwidth=1, height=40)

        self.lbl_icon = Label(self.root, font=(
            "Sans", 15, "bold"), background="light blue", foreground="black", anchor="c", padx=5)
        self.lbl_icon.place(x=0, y=190, relwidth=1, height=120)

        self.lbl_wind = Label(self.root, font=(
            "Sans", 20), background="light blue", foreground="orange", anchor="c", padx=5,)
        self.lbl_wind.place(x=0, y=330, relwidth=1, height=40)

        self.lbl_temp = Label(self.root, font=(
            "Sans", 20), background="light blue", foreground="black", anchor="c", padx=5)
        self.lbl_temp.place(x=0, y=390, relwidth=1, height=40)

        self.lbl_aqi = Label(self.root, text="", font=("Sans", 22), background="light blue",
                             foreground="black", anchor="c", padx=5)
        self.lbl_aqi.place(x=0, y=470, relwidth=1, height=100)

        # ====== footer======

        footer = Label(self.root, text="", font=("Serif", 25), background="#033953",
                       foreground="White", anchor="c", padx=5).pack(side=BOTTOM, fill=X)

    def get_weather(self):

        api_key = Weather_api.api_key

        complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.var_search.get()}&appid={api_key}"

        if self.var_search.get() == "":
            self.lbl_city.config(text="")
            # icons
            self.lbl_icon.config(image="")
            # temp
            self.lbl_temp.config(text="")
            # wind
            self.lbl_wind.config(text="")
            # aqi
            self.lbl_aqi.config(text="" , bg="light blue")
            # error
            messagebox.showerror("ERROR", "ENTER CITY NAME...")

        else:
            result = requests.get(complete_url)

            if result:
                json = result.json()

                city_name = json["name"]
                country = json["sys"]["country"]
                icon = json["weather"][0]["icon"]
                temp_c = json["main"]["temp"] - 273.15
                temp_f = (json["main"]["temp"] - 273.15) * 9/5 + 32
                wind = json["weather"][0]["main"]
                

                # ======= appending to labels=========

                # city name

                self.lbl_city.config(text=city_name + " , " + country)

                # icons
                self.search_icon2 = Image.open(f"icons/{icon}.png")
                self.search_icon2 = self.search_icon2.resize(
                    (120, 120), Image.ANTIALIAS)
                self.search_icon2 = ImageTk.PhotoImage(self.search_icon2)
                self.lbl_icon.config(image=self.search_icon2)

                # temp
                self.lbl_temp.config(text=str(round(temp_c, 2)) +
                                     " ºC | " + str(round(temp_f, 2)) + " º F")
                # wind
                self.lbl_wind.config(text=wind)

                # aqi
                self.disp_aqi()
                

            else:
                self.lbl_city.config(text="")

                # icons

                self.lbl_icon.config(image="")

                # temp
                self.lbl_temp.config(text="")
                # wind
                self.lbl_wind.config(text="")

                # display aqi
                self.lbl_aqi.config(text="" , bg="light blue")

                # error

                messagebox.showerror("ERROR", "INVALID CITY NAME...")
                self.txt_city.delete(0, 'end')

    def disp_aqi(self):
        api_key = Weather_api.api_key

        complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.var_search.get()}&appid={api_key}"

        result = requests.get(complete_url)

        json = result.json()

        lat = json["coord"]["lat"]
        lon = json["coord"]["lon"]

        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

        aqi_result = requests.get(aqi_url)
        json1 = aqi_result.json()
        aqi_level = json1["list"][0]["main"]["aqi"]


        aqi_color= "light blue"

        quality = ""
        if aqi_level == 1:
            aqi_color = "#35f52f"
            quality = "Good"
             

        if aqi_level == 2:
            aqi_color = "#9cf52f"
            quality = "Fair" 
        
        if aqi_level == 3:
            aqi_color = "#d7f52f"
            quality = "Moderate" 

        if aqi_level == 4:
            aqi_color = "#f5b62f"
            quality = "Poor" 

        if aqi_level == 5:
            aqi_color = "#f5572f"
            quality = "Very Poor" 

        self.lbl_aqi.config(text= "AQI: " + str(aqi_level) +" | " + quality , bg = aqi_color )
root = Tk()

obj = MyWeather(root)

root.mainloop()
