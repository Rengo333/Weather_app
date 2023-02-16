import json
import requests
import tkinter
from time import strftime
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk


def get_city_data(city, country):

    # checking input
    if city == "":
        raise Exception("no input")

    try:

        # checking if user entered country code or just a city
        if country == "":
            # using api call to get coordinates
            url_coord = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={LIMIT}&appid={API_KEY}")

        else:
            # using api call to get coordinates
            url_coord = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit={LIMIT}&appid={API_KEY}")

        # getting coordinates
        coord_data = json.loads(url_coord.content)

        # city coordinates
        lat = coord_data[0]["lat"]
        lon = coord_data[0]["lon"]

        # city name and country
        name = coord_data[0]["name"]
        country = coord_data[0]["country"]

        # getting weather info by using coordinates in an api call
        url_weather = requests.get(
            f"https://api.openweathermap.org/data/3.0/onecall?lat="
            f"{lat}&lon={lon}&exclude=minutely&appid={API_KEY}&units={units}")

        # loading weather data from json
        weather = json.loads(url_weather.content)

        # saving temp, weather and icon data from json for current weather
        current_weather1 = \
            [weather["current"]["temp"],
             weather["current"]["feels_like"],
             weather["current"]["weather"][0]["main"],
             weather["current"]["weather"][0]["description"]
             ]
        curr_icon = weather["current"]["weather"][0]["icon"]

        # saving temp, weather and icon data from json for daily weather
        daily_weather = \
            [weather["daily"][0]["temp"]["day"],
             weather["daily"][0]["temp"]["night"],
             weather["daily"][0]["temp"]["min"],
             weather["daily"][0]["temp"]["max"],
             weather["daily"][0]["weather"][0]["main"],
             weather["daily"][0]["weather"][0]["description"],
             weather["daily"][0]["weather"][0]["icon"]
             ]
        daily_icon = weather["daily"][0]["weather"][0]["icon"]

        # formatting data to display them in the app
        current_temp = f"Current Temperature: {current_weather1[0]}\n" \
                       f"Feels like: {current_weather1[1]}"
        current_weather = f"Weather: {current_weather1[2]}\n {current_weather1[3]}"

        # formatting data to display them in the app
        daily_temp = f"Day Time Temperature: {daily_weather[0]}\n" \
                     f"Night Time Temperature: {daily_weather[1]}\n" \
                     f"Min. Temperature: {daily_weather[2]}\n" \
                     f"Max. temperature: {daily_weather[3]}\n"
        today_weather = f"Weather: {daily_weather[4]}\n {daily_weather[5]}"

        # saving all the data in one variable
        data = (current_temp, daily_temp, name, country, curr_icon, daily_icon, current_weather, today_weather)

        return data

    except Exception:
        messagebox.showerror(f'error, cannot find{city}')


# showing current time and updating it
def my_time():

    time_string = strftime('%H:%M:%S %p')  # time format
    date_time_label.config(text=time_string)
    date_time_label.after(1000, my_time)  # time delay of 1000 milliseconds


def show_curr_weather():

    # used to update data when changing units
    global current_selected_func
    current_selected_func = 2

    global state
    global image_label

    # city name, temperature and weather
    city = city_name.get()
    country = (country_text.get())
    city_data = get_city_data(city, country)
    city_state_label['text'] = f'{city_data[2]}, {city_data[3]}'
    temp_label['text'] = city_data[0]
    weather_label["text"] = city_data[6]

    # checking if picture is displayed
    if not state:

        # creating image label and displaying it in tkinter window
        image = Image.open(f'icons/{city_data[4]}@2x.png')
        img = ImageTk.PhotoImage(image)
        image_label = tkinter.Label(image=img, bg='lightblue')
        image_label.image = img

        # Position image
        image_label.place(x=520, y=260)
        state = True

    elif state:
        # deleting the previous image and replacing it with a new one
        image_label.place_forget()
        image = Image.open(f'icons/{city_data[4]}@2x.png')
        img = ImageTk.PhotoImage(image)
        image_label = tkinter.Label(image=img, bg='lightblue')
        image_label.image = img

        # Position image
        image_label.place(x=520, y=260)
        state = True


# changing temperature units
def change_units():

    global units
    # fahrenheit
    if units == "metric":
        units = "imperial"
        change_units_button["text"] = "Fahrenheit"

    # celsius
    elif units == "imperial":
        units = "metric"
        change_units_button["text"] = "Celsius"

    # updating data in the app
    if current_selected_func == 1:
        show_today_weather()
    elif current_selected_func == 2:
        show_curr_weather()


def show_today_weather():

    global current_selected_func
    current_selected_func = 1
    global state
    global image_label

    # city name, temperature and weather
    city = city_name.get()
    country = (country_text.get())
    city_data = get_city_data(city, country)
    city_state_label['text'] = f'{city_data[2]}, {city_data[3]}'
    temp_label['text'] = city_data[1]
    weather_label["text"] = city_data[7]

    # checking if picture is displayed
    if not state:

        # displaying picture
        image = Image.open(f'icons/{city_data[5]}@2x.png')
        img = ImageTk.PhotoImage(image)
        image_label = tkinter.Label(image=img, bg='lightblue')
        image_label.image = img

        # Position image
        image_label.place(x=520, y=260)
        state = True

    # picture update
    elif state:

        image_label.place_forget()
        image = Image.open(f'icons/{city_data[5]}@2x.png')
        img = ImageTk.PhotoImage(image)
        image_label = tkinter.Label(image=img, bg='lightblue')
        image_label.image = img
        # Position image
        image_label.place(x=520, y=260)
        state = True


if __name__ == "__main__":

    # for safety purposes use your own generated api key at https://openweathermap.org/
    API_KEY = "YOUR_API_KEY"

    # limit of results by a single call
    LIMIT = 5

    # Units – default: kelvin, metric: Celsius, imperial: Fahrenheit
    units = "metric"

    # setting image display state
    state = False

    # tkinter app
    app = Tk()
    app.title("Weather App")
    app.geometry("700x500")
    app['bg'] = 'lightblue'

    # text field
    city_label = Label(app, text="Enter the name of any city: ", font=('bold', 12), bg='lightblue')
    city_label.place(x=170, y=70)

    # text field
    city_text_label = Label(app, text="City: ", font=('bold', 9), bg='lightblue')
    city_text_label.place(x=130, y=125)

    # entry field for the city
    city_name = StringVar()
    city_entry = Entry(app, textvariable=city_name, bg='white')
    city_entry.place(x=170, y=125)

    # text field
    country_label = Label(app, text="Optional enter country code(e.g.'GB','US'): ", font=('bold', 12), bg='lightblue')
    country_label.place(x=170, y=98)

    # entry field for the country
    country_text = StringVar()
    country_entry = Entry(app, textvariable=country_text, bg='white')
    country_entry.place(x=360, y=125)

    # text field
    country_text_label = Label(app, text="Code: ", font=('bold', 9), bg='lightblue')
    country_text_label.place(x=315, y=125)

    # show current weather button
    curr_weather_button = Button(app, text="Show current weather", width=16, command=show_curr_weather, bg='yellow')
    curr_weather_button.place(x=360, y=155)

    # show today weather button
    daily_weather_button = Button(app, text="Show todays weather", width=16, command=show_today_weather, bg='yellow')
    daily_weather_button.place(x=170, y=155)

    # button for changing the units
    change_units_button = Button(app, text="", width=8, command=change_units, bg='yellow')
    change_units_button["text"] = "Celsius"
    change_units_button.place(x=635, y=0)

    # text label showing city and a country
    city_state_label = Label(app, text='', font=('bold', 20), bg="lightblue")
    city_state_label.place(x=200, y=240)

    # temperature showing label
    temp_label = Label(app, text='', font=('bold', 13), bg="lightblue")
    temp_label.place(x=200, y=310)

    # weather showing label
    weather_label = Label(app, text='', font=('bold', 13), bg="lightblue")
    weather_label.place(x=500, y=220)

    # date and time showing label
    date_time_label = Label(app, font=('bold', 10), bg="lightblue")
    date_time_label.place(x=540, y=0)
    my_time()

    # creating loop
    app.mainloop()
