import typer
from rich import print as rprint
from rich.console import Console
from rich.prompt import Prompt

import json
import requests

import tkinter as tk

from datetime import date, time, datetime, timedelta
# import urllib library 
from urllib.request import urlopen

version = "0.1.0"
apiurl = "https://get.api-feiertage.de/"

#infos
# https://www.dgb.de/gesetzliche-feiertage-deutschland
# https://www.api-feiertage.de/

states = [
     "bw",
     "by", 
     "be",
     "bb",
     "hb",
     "hh",
     "he",
     "mv",
     "ni",
     "nw",
     "rp",
     "sl",
     "sn",
     "st",
     "sh",
     "th"
    ]
confessions = ["rk","ev"]
wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

fronleichnamSnGemeinden = "Bautzen (nur in den Ortsteilen Bolbritz und Salzenforst), Crostwitz, Göda (nur im Ortsteil Prischwitz), Großdubrau (nur im Ortsteil Sdier), Hoyerswerda (nur im Ortsteil Dörgenhausen), Königswartha (nicht im Ortsteil Wartha), Nebelschütz, Neschwitz (nur in den Ortsteilen Neschwitz und Saritsch), Panschwitz-Kuckau, Puschwitz, Räckelwitz, Radibor, Ralbitz-Rosenthal und Wittichenau."
fronleichnamThGemeinden = "nur im im Landkreis Eichsfeld sowie in folgenden Gemeinden des Unstrut-Hainich-Kreises und des Wartburgkreises: \n Anrode (nur in den Ortsteilen Bickenriede und Zella), Brunnhartshausen (nur in den Ortsteilen Föhlritz und Steinberg), Buttlar, Dünwald (nur in den Ortsteilen Beberstedt und Hüpstedt), Geisa, Rodeberg (nur im Ortsteil Struth), Schleid, Südeichsfeld und Zella/Rhön."
def download_feiertage(args: dict):
    # args.year
    # args.state
    # args.confession
    # args.augsburg
    # args.apiurl
    
    #encode request parameters
    requestParams = {"years": args["year"], "states": args["state"]}
    if args["confession"] == "ev":
        requestParams["katholisch"] = "0"
    
    
    # store the response of URL 
    response = requests.get(apiurl, params=requestParams)
    return response.json()

def get_params():
    '''Get the parameters for the optimization'''
    
    fronleichnamSachsen = False
    fronleichnamThueringen = False
    augsburg = False
    
    rprint("Für die Optimierung benötigen wir weitere Informationen für den Feiertagsrechner. \n")
    rprint("Bitte geben Sie das Arbeitsjahr ein, für das Sie die Feiertage berechnen möchten. \n")
    year = Prompt.ask("Arbeitsjahr:", default=2021)
    state = Prompt.ask("Bitte geben Sie das Bundesland ein, für das Sie die Feiertage berechnen möchten.", choices=states)
    confession = Prompt.ask("Bitte geben Sie die Konfession ein die in ihrer Gemeinde die Mehrheit hat.:", choices=confessions)
    match state:
        case "by":
            augsburg = Prompt.ask("Leben Sie in Augsburg:", choices=["Ja", "Nein"])
            if augsburg == "Ja":
                augsburg = True
        case "sn":
            rprint("In Sachsen gibt es einige Gemeinden die einen zusätzlichen Feiertag haben. \n")
            rprint(fronleichnamSnGemeinden)
            fronleichnamSachsen = Prompt.ask("Leben Sie in einer der genannten Gemeinden?:", choices=["Ja", "Nein"])
            if fronleichnamSachsen == "Ja":
                fronleichnamSachsen = True
        case "th":
            rprint("In Thüringen gibt es einige Gemeinden die einen zusätzlichen Feiertag haben. \n")
            rprint(fronleichnamThGemeinden)
            fronleichnamThueringen = Prompt.ask("Leben Sie in einer der genannten Gemeinden?:", choices=["Ja", "Nein"])
            if fronleichnamThueringen == "Ja":
                fronleichnamThueringen = True
    noOfDays = int(Prompt.ask("Bitte geben Sie die Anzahl der Tage ein, an denen Sie arbeiten können.", default=5))
    days = []
    for i in range(noOfDays):
        days.append(Prompt.ask("Bitte geben Sie den nächsten Tag ein, an denen Sie arbeiten können. Aktuelle Liste:" + str(days).strip('()'), choices=wochentage))
    rprint("Als Wochentage wurden angegeben:",days)
    #TODO: add check for start date of work
    params = {
        "year": year,
        "state": state,
        "confession": confession,
        "augsburg": augsburg,
        "fronleichnamSachsen": fronleichnamSachsen,
        "fronleichnamThueringen": fronleichnamThueringen,
        "days": days
    }
    return params



def get_params_gui():
    '''Get the parameters for the optimization'''
    
    fronleichnamSachsen = False
    fronleichnamThueringen = False
    augsburg = False

    
    # Create the GUI window
    root = tk.Tk()
    root.title("Feiertagsrechner") 
    
    # Add a label and dropdown box for the year
    year_label = tk.Label(root, text="Arbeitsjahr:")
    year_label.pack()
    current_year = datetime.now().year
    year_var = tk.StringVar(root)
    year_dropdown = tk.OptionMenu(root, year_var, *[str(year) for year in range(current_year, current_year+12)])
    year_dropdown.pack()
    
    # Add a label and dropdown box for the state
    state_label = tk.Label(root, text="Bundesland:")
    state_label.pack()
    state_var = tk.StringVar(root)
    state_dropdown = tk.OptionMenu(root, state_var, *states)
    state_dropdown.pack()
    
    # Add a label and dropdown box for the confession
    confession_label = tk.Label(root, text="Konfession:")
    confession_label.pack()
    confession_var = tk.StringVar(root)
    confession_dropdown = tk.OptionMenu(root, confession_var, *confessions)
    confession_dropdown.pack()
    
    # Add additional elements based on the selected state
    def on_state_select(*args):
        nonlocal augsburg, fronleichnamSachsen, fronleichnamThueringen
        state = state_var.get()
        if state == "by":
            augsburg_label = tk.Label(root, text="Leben Sie in Augsburg?")
            augsburg_label.pack()
            augsburg_var = tk.StringVar(root)
            augsburg_dropdown = tk.OptionMenu(root, augsburg_var, "Ja", "Nein")
            augsburg_dropdown.pack()
            augsburg = augsburg_var.get() == "Ja"
        elif state == "sn":
            fronleichnam_label = tk.Label(root, text="Leben Sie in einer der genannten Gemeinden?")
            fronleichnam_label.pack()
            fronleichnam_var = tk.StringVar(root)
            fronleichnam_dropdown = tk.OptionMenu(root, fronleichnam_var, "Ja", "Nein")
            fronleichnam_dropdown.pack()
            fronleichnamSachsen = fronleichnam_var.get() == "Ja"
        elif state == "th":
            fronleichnam_label = tk.Label(root, text="Leben Sie in einer der genannten Gemeinden?")
            fronleichnam_label.pack()
            fronleichnam_var = tk.StringVar(root)
            fronleichnam_dropdown = tk.OptionMenu(root, fronleichnam_var, "Ja", "Nein")
            fronleichnam_dropdown.pack()
            fronleichnamThueringen = fronleichnam_var.get() == "Ja"
    state_var.trace("w", on_state_select)
    
    # Add checkboxes for the work days
    days_checkboxes = []
    for day in wochentage:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(root, text=day, variable=var)
        checkbox.pack()
        days_checkboxes.append(var)
    
    # Add a button to submit the form
    submit_button = tk.Button(root, text="Berechnen", command=root.quit, state="disabled")
    submit_button.pack()

    # Validation function to check if all required values have been set
    def validate():
        if not year_var.get() or not state_var.get() or not confession_var.get():
            submit_button.config(state="disabled")
        else:
            submit_button.config(state="normal")

    # Call the validation function whenever a value changes
    year_var.trace("w", lambda *args: validate())
    state_var.trace("w", lambda *args: validate())
    confession_var.trace("w", lambda *args: validate())

    
    # Start the GUI event loop
    root.mainloop()
    
    # Get the values from the GUI elements
    year = int(year_var.get())
    state = state_var.get()
    confession = confession_var.get()
    days = [wochentage[i] for i, var in enumerate(days_checkboxes) if var.get()]
    
    params = {
        "year": year,
        "state": state,
        "confession": confession,
        "augsburg": augsburg,
        "fronleichnamSachsen": fronleichnamSachsen,
        "fronleichnamThueringen": fronleichnamThueringen,
        "days": days
    }
    return params

def main():
    running = True
    rprint("Feiertagsrechner v" + version)
    rprint("by @mergintaim")
    args = get_params_gui()
    rprint(args)
    feiertage = download_feiertage(args)["feiertage"]
    
    # create a dictionary to keep track of how often a specific weekday is in feiertage
    weekdays_count = {
        "Montag": 0,
        "Dienstag": 0,
        "Mittwoch": 0,
        "Donnerstag": 0,
        "Freitag": 0,
        "Samstag": 0,
        "Sonntag": 0
    }
    
    # iterate through feiertage and check for every date on which weekday it is
    for feiertag in feiertage:
        weekday = wochentage[datetime.strptime(feiertag["date"], "%Y-%m-%d").weekday()]
        # increment the corresponding weekday counter
        weekdays_count[weekday] += 1
    
    # find the weekday with the maximum value
    max_weekday = max(weekdays_count, key=weekdays_count.get)
    
    # find all the weekdays that have the maximum value
    max_weekdays = [weekday for weekday in weekdays_count if weekdays_count[weekday] == weekdays_count[max_weekday]]
    
    rprint(f"Der Wochentag mit den meisten Feiertagen ({weekdays_count[max_weekday]} Feiertage) ist: {', '.join(max_weekdays)}")
    
    while(running):
        running = False

if __name__ == "__main__":
    typer.run(main)