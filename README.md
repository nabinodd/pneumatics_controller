# pneumatics_controller

# topics that will be published from keypad module : 

pneumatics/pressed
pneumatics/held
pneumatics/released


# topic to publish the saved data :
pneumatics/retrive_resp

Note : Query command won't be published, need to respond via 'retrive_resp' topic if '7' is pressed


# publishing format :
pneumatics/pressed ----> str(button name) 
ex : '4'
pneumatics/held ----> str(button_name,seconds_elapsed)
ex : '4','2' -> '4','3' -> '4','4' and so on
pneumatics/released ----> str(button_name,seconds_pressed)
ex : '4','5'


# Buttons functions according to 4 X 4 keypad layout :

1,2,3,A ----> Increase time in the text box
4,5,6,B ----> Decrease time in the text box

7 ----> Save data (displayed in the text box)
C ----> Retrive data (last stored)


