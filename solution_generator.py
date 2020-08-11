from selenium import webdriver
from Color_select_panel import full_x_paths_panel
from Color_fillings import full_x_paths_fills
from solution import moves_xpath
from commands import speaking_cmds
import time
import pyttsx3


def speak_move(M) : 

    engine = pyttsx3.init()
    engine.say(M)
    engine.runAndWait()

def fill_solve(CA) : 

    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument('--headless')


    driver = webdriver.Chrome('YOUR PATH FOR YOUR CHROME-DRIVER', chrome_options = chrome_opt)
    driver.maximize_window()

    driver.get('https://ruwix.com/online-rubiks-cube-solver-program/')


    button_view = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[3]/section/article/section/div[1]/div[2]/div[1]/div[1]/div[3]/div')
    button_view.click()
    
    try : 
       cookie_button = driver.find_element_by_xpath('/html/body/div[5]/a')
       cookie_button.click()
    except : pass  


    for i , colour in enumerate(CA) : 

        if i + 1 not in [5 , 14 , 23 , 32 , 41 , 50] : 

          panel_colour_xpath = full_x_paths_panel[colour]
          colour_select_button = driver.find_element_by_xpath(panel_colour_xpath)
          colour_select_button.click()

          colour_fill_xpath = full_x_paths_fills[i + 1]
          colour_filling_button = driver.find_element_by_xpath(colour_fill_xpath)
          colour_filling_button.click()


    button_solve = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[3]/section/article/section/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/a/div')
    button_solve.click()

    solved_url = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[3]/section/article/section/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/a')
    u = solved_url.get_attribute('href')

    alltabs = driver.window_handles
    

    for tab in alltabs : 
        driver.switch_to.window(tab)
        if driver.current_url == u : 
       
            time.sleep(10)

            for i_ , m_x in moves_xpath.items() : 
              
              try : 
                move = driver.find_element_by_xpath(m_x)
                print(move.text)

                command_ = speaking_cmds[move.text]
                speak_move(command_)

                time.sleep(1.5)

              except : pass  
            