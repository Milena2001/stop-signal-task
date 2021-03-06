"""Importowanie bibliotek"""
import codecs
import csv
import random
from os.path import join
import yaml
from psychopy import visual, event, logging, gui, core
conf = yaml.load(open("config.yaml", encoding="utf-8")) #wywolywanie zmiennych z pliku konfiguracyjnego
"""Utworzenie funkcji"""
def save_data():
    """
    Zapisywanie zebranych danych do pliku csv.
    :return:
    """
    with open(join('results', datafile), "w", newline='') as df:
        write = csv.writer(df)
        write.writerows(conf["RESULTS"])

def read_text_from_file(file_name, insert=''):
    """
    Method that read message from text file, and optionally add some
    dynamically generated info.
    :param file_name: Name of file to read
    :param insert:
    :return: message
    """
    if not isinstance(file_name, str):
        logging.error('Problem with file reading, filename must be a string')
        raise TypeError('file_name must be a string')
    msg = list()
    with codecs.open(file_name, encoding='utf-8', mode='r') as data_file:
        for line in data_file:
            if not line.startswith('#'):  # if not commented line
                if line.startswith('<--insert-->'):
                    if insert:
                        msg.append(insert)
                else:
                    msg.append(line)
    return ''.join(msg)

def abort_with_error(err):
    """
    Call if an error occured.
    """
    logging.critical(err)
    raise Exception(err)

def show_info(window, file_name, insert='', key ='escape'):
    """
    Clear way to show info message into screen.
    :param win:
    :return:
    """
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(window, color='black', text=msg,
                          height=20)
    msg.draw()
    window.flip()
    key = event.waitKeys(keyList=['escape', 'return', 'space', 'left', 'right'])
    if key == ['escape']:
        abort_with_error(
            'Experiment finished by user on info screen! Esc pressed.')
    window.flip()

def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=keys)
    return key[0]

def check_exit(key='escape'):
    """
    Check (during procedure) if experimentator doesn't want to terminate.
    """
    stop = event.getKeys(keyList=[key])
    if stop:
        abort_with_error(
            'Experiment finished by user! {} pressed.'.format(key))

def part_of_experiment(n_trials, exp, fix):
    """G????wna funkcja odpowiadaj??ca za wy??wietlanie bod??c??w i zbieranie reakcji"""
    fix.draw()  # Rysowanie punktu fiksacyjnego
    core.wait(1)
    window.flip()  # Wyswietlenie punktu fiksacyjnego
    core.wait(1)
    for i in range(n_trials):
        stim_type = random.choice(list(stim.keys())) #Losowanie typu bod??ca, czyli kierunku wy??wietlania strza??ki
        circle_type = random.choice(list(circle.keys())) #Losowanie koloru okregu
        stim[stim_type].setAutoDraw(True)  # Rysowanie strzalki
        window.flip()  # Wyswietlenie strzalki
        circle[circle_type].draw() 
        window.callOnFlip(clock.reset)
        window.flip()  # Wyswietlenie strzalki w okregu
        if circle == "GO": 
            key = reactions(conf["REACTION_KEYS"])  # Czekanie na wcisniecie klawisza
            rt = clock.getTime()
            acc = "GO"
        else:
            acc = "NO GO"
            while True:
                if len(event.getKeys()) > 0 and acc and conf["STOP_TIME"] < conf["LIM_MAX"]:
                    rt = clock.getTime()
                    conf["STOP_TIME"] += 0.5
                    key = "PRESSED"
                    break
                if clock.getTime() > conf["STOP_TIME"] > conf["LIM_MIN"] and acc:
                    rt = clock.getTime()
                    conf["STOP_TIME"] -= 0.5
                    key = "NOT PRESSED"
                    break

            stim[stim_type].setAutoDraw(False)
        conf["RESULTS"].append([ID, exp, acc, rt, stim_type, key])

# ustawienia okna procedury
window = visual.Window(color="gray", units="pix", fullscr=False)
window.setMouseVisible(False)
mouse = event.Mouse(visible=True)

clock = core.Clock()
#Tworzenie bod??ca GO - strza??ki
stim = {"left": visual.TextStim(win=window, text="???", height=120, bold=True, pos=(0, 3)),
        "right": visual.TextStim(win=window, text="???", height=120, bold=True, pos=(0, 3))}
#Tworzenie sygna??u STOP i neutralnego bod??ca - okr??g czerwony i bia??y
circle = {"GO": visual.Circle(window, size=(130, 130), pos=(0, -8), lineColor='white', fillColor=None),
          "NO GO": visual.Circle(window, size=(130, 130), pos=(0, -8), lineColor='#bf1616', fillColor=None)}
#Tworzenie punktu fiksacyjnego
fix = visual.TextStim(win=window, text="+", height=80)

# Okno dialogowe zbieraj??ce informacje o uczestniku
info = {'ID': '', 'PLEC': ['M', 'K'], 'WIEK': ''}
dlg = gui.DlgFromDict(info, title='Wpisz swoje dane')
if not dlg.OK:
    print("User exited")
    core.quit()

# Og??lne ID badanych zlozone z informacji podanych w oknie dialogowym
ID = info['ID'] + info['PLEC'] + info['WIEK']

# Tworzenie nazwy pliku csv z wynikami badanego
datafile = '{}.csv'.format(ID)

# POCZ??TKOWE INFORMACJE
show_info(window, 'instrukcja og??lna.txt', insert='', key='escape')

# Informacja przed treningiem
show_info(window, 'trening.txt', insert='', key='escape')

# Cz?????? trenigowa
part_of_experiment(conf["N_TRIALS_TRAIN"], exp=False, fix=fix)

# Informacja przed pierwsz?? cz????ci?? eksperymentaln??
show_info(window, 'czesc eksperymentalna.txt', insert='', key='escape')
# Pierwsza cz?????? eksperymentalna
part_of_experiment(conf["N_TRAILS_EXP"], exp=True, fix=fix)
# Informacja o przerwie
show_info(window, 'przerwa.txt', insert='', key='escape')
# Druga cz?????? eksperymentalna
part_of_experiment(conf["N_TRAILS_EXP"], exp=True, fix=fix)
#Zapisywanie wynik??w do pliku .csv
save_data()
# Koniec procedury
show_info(window, 'koniec.txt', insert='', key='escape')


