"""

Author: Sarthak Bhargava
Email: bhargavasarthak788@gmail.com

"""
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import requests
from bs4 import BeautifulSoup
import numpy as np


Builder.load_string("""

<Button>:
    font_size: 16
    bcolor: 0.3, 0.7, 0.6, 1

<MyGrid>
    labeldetails: labeldetails
    value: value
    
    GridLayout:
        cols: 1
        size: root.width, root.height
        
        GridLayout:
            cols:1
            
            Label:
                text:"Covid-19 Tracker"
                font_size: 60
            
            Label: 
                text: "By Sarthak Bhargava"
                font_size: 12
                
        GridLayout:
            cols:1
            
            Label:
                text: "Enter Full Name of State"
                bold: True
                
            GridLayout:
                cols: 2
    
                Label:
                    text: "Enter State "
                    
                TextInput:
                    id: value
                    font_size: 16
                    multiline: True
                    
                Button:
                    text : "World"
                    on_press: root.btn_world()
                    background_color: 0.1, 0, 0, 1
                
                Button:
                    text : "India"
                    on_press: root.btn_india()
                    background_color: 0.1, 0, 0, 1
                
            Button:
                text : "Get Data"
                on_press: root.btn_get()
                size_hint: 0.5,0.5

        Label:
            id: labeldetails
            font_size: 18
            text : "Search Number  of Patients(Covid - 19 Patients) "
""")

all_states =['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadar Nagar Haveli', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Tamil Nadu', 'Telengana', 'Tripura', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal']

class Covid:

    def Covid_World():

        number = []
        url = "http://www.worldometers.info/coronavirus/"
        r = requests.get(url)
        s = BeautifulSoup(r.text, "html.parser")
        data = s.find_all("div", class_="maincounter-number")

        number.append(data[0].text.strip())
        number.append(data[1].text.strip())
        number.append(data[2].text.strip())

        return number

    def Covid_India():

        extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
        URL = 'https://www.mohfw.gov.in/'
        response = requests.get(URL).content
        soup = BeautifulSoup(response, 'html.parser')
        stats = []
        all_rows = soup.find_all('tr')

        for row in all_rows:
            stat = extract_contents(row.find_all('td'))

            if stat:

                if len(stat) == 4:
                    stat = ['', *stat]
                    stats.append(stat)

                elif len(stat) == 5:
                    stats.append(stat)

        stats[-1][0] = len(stats)
        stats[-1][1] = "Total Cases"

        return stats

class MyGrid(Widget):

    labeldetails = ObjectProperty(None)
    value = ObjectProperty(None)

    def btn_india(self):

        Total_Cases_India = Covid.Covid_India()[-1][2]
        Recovered_Cases_India = Covid.Covid_India()[-1][3]
        Death_Cases_India = Covid.Covid_India()[-1][4]
        Active_Cases_India = int(Total_Cases_India) - int(Recovered_Cases_India) - int(Death_Cases_India)
        Current_Mortality_Rate = round((int(Death_Cases_India)/int(Total_Cases_India))*100,1)
        Current_Recovery_Rate = round((int(Recovered_Cases_India)/int(Total_Cases_India))*100,1)

        self.labeldetails.text = "                    India's Data\n\n" + \
                                 "Total Cases                       - " + str(Total_Cases_India) + \
                               "\nActive Cases                     - " + str(Active_Cases_India) + \
                               "\nRecovered                          - " + str(Recovered_Cases_India) + \
                               "\nDeaths                                 - " + str(Death_Cases_India) + \
                               "\nCurrent Mortatliy Rate   - " + str(Current_Mortality_Rate) + " %"\
                               "\nCurrent Recovery Rate  - " + str(Current_Recovery_Rate) + " %"

    def btn_world(self):

        Total_Cases_World = Covid.Covid_World()[0]
        Deaths_World = Covid.Covid_World()[1]
        Recovered_World = Covid.Covid_World()[2]

        self.labeldetails.text = "           World's Data  \n\nTotal Cases - " + Total_Cases_World + "\n  Recovered - " + Recovered_World + "\n        Death - " + Deaths_World


    def btn_get(self):

        self.States = self.value.text

        if self.States in all_states:
            index = (all_states.index(self.States))
            Total_Cases = Covid.Covid_India()[index][2]
            Deaths = Covid.Covid_India()[index][4]
            Recovered = Covid.Covid_India()[index][3]
            Active_Cases = int(Total_Cases) - int(Deaths) - int(Recovered)
            Current_Mortatliy_Rate = round((int(Deaths)/int(Total_Cases)) * 100,1)
            Current_Recovery_Rate = round((int(Recovered)/int(Total_Cases)) * 100,1)

            self.labeldetails.text = "            " +self.States+" \n\n" + \
                                     "Total Cases                      - " + str(Total_Cases) + \
                                   "\nActive Cases                    - "+ str(Active_Cases) +\
                                   "\nRecovered                         - " + str(Recovered)+\
                                   "\nDeaths                                - "+ str(Deaths)+ \
                                   "\nCurrent Mortatliy Rate  - "+ str(Current_Mortatliy_Rate)+" %"\
                                   "\nCurrent Recovery Rate - " + str(Current_Recovery_Rate)+" %"

        else:
            Total_Cases_World = Covid.Covid_World()[0]
            Deaths_World = Covid.Covid_World()[1]
            Recovered_World = Covid.Covid_World()[2]

            self.labeldetails.text = "Enter Wrong State\n       World's Data  \n\n    Total Cases - "+Total_Cases_World+"\n   Recovered - "+Recovered_World+"\n      Death - "+Deaths_World

class TrackerApp(App):

    def build(self):
        return MyGrid()

if __name__ == "__main__":
    TrackerApp().run()