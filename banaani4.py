import cv2
import numpy as np
import keyboard

#let's add some tkinter-functionality for advanced inputs
import tkinter
from tkinter import *
import matplotlib.pyplot as plt

#let's make some global variables
global image_np_with_detections
global detected_item
global detection_box_xy
global ikkuna_sijainti
global cv_ikkuna_sijainti
global cap

#let's define variable for labels
global labels
labels=['banana','carrot','orange','apple','perch','peanut','pottu','nauris','lanttu','write','more','as','many','classes','you','need']

#initialize the location of the cv image screen...
cv_ikkuna_sijainti=[500,200]

#helpful function...
def change_position(root_variable,x,y):
    root_variable.geometry("+{}+{}".format(x,y))
    root_variable.update()

#let's make a tkinter window...
ikkuna=tkinter.Tk()
ikkuna.title('CV2 assistant window...')
ikkuna_sijainti=[cv_ikkuna_sijainti[0],cv_ikkuna_sijainti[1]-150]
change_position(ikkuna,ikkuna_sijainti[0],ikkuna_sijainti[1])

#category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH+'/label_map.pbtxt')

def pollaus():
    global image_np_with_detections
    global detected_item
    global detection_box
    global ikkuna_sijainti
    global cv_ikkuna_sijainti
    global cap
    global labels

    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    painike_1['text']='Search'

    while True:
        ret, frame = cap.read()
        image_np = np.array(frame)

        #let's ask assistant window to vibrate during search...
        ikkuna_sijainti=[cv_ikkuna_sijainti[0]+np.random.randint(0,10),cv_ikkuna_sijainti[1]-150]
        change_position(ikkuna,ikkuna_sijainti[0],ikkuna_sijainti[1])

        #input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        #detections = detect_fn(input_tensor)

        #num_detections = int(detections.pop('num_detections'))
        #detections = {key: value[0, :num_detections].numpy()
        #              for key, value in detections.items()}
        #detections['num_detections'] = num_detections

        # detection_classes should be ints.
        #detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        #label_id_offset = 1
        image_np_with_detections = image_np.copy()

        #viz_utils.visualize_boxes_and_labels_on_image_array(
        #            image_np_with_detections,
        #            detections['detection_boxes'],
        #            detections['detection_classes']+label_id_offset,
        #            detections['detection_scores'],
        #            max_boxes_to_draw=3,
        #            min_score_thresh=.9,
        #            agnostic_mode=False)

        if np.random.random()<0.05:
            #here we simulate the situation where one of the classes in the globally defined labels has detected...
            detected_id=np.random.randint(0,len(labels)-1)

            #if np.random.random()>0.5:
            #    detected_item='Banana'
            #else:
            #    detected_item='Carrot'

            detected_item=labels[detected_id]

            print(detected_item + " found!")

            detection_box=[np.random.randint(100,200),np.random.randint(100,200),np.random.randint(300,400),np.random.randint(300,400)]
            alkunurkka=(detection_box[0],detection_box[1])
            loppunurkka=(detection_box[2],detection_box[3])
            image_np=cv2.rectangle(image_np,alkunurkka,loppunurkka,(0,255,0),2)
            #paikka=(alkunurkka,loppunurkka)
            vari=(255,0,0)
            fontti=cv2.FONT_HERSHEY_SIMPLEX
            fontScale=1
            image_np=cv2.putText(image_np,detected_item,alkunurkka,fontti,fontScale,vari,2,cv2.LINE_AA)

            cv2.imshow('object detection',  cv2.resize(image_np, (800, 600)))

            painike_1['text']='Continue search'

            cap.release()
            break

        else:
            cv2.imshow('object detection',  cv2.resize(image_np, (800, 600)))
            cv2.moveWindow('object detection',cv_ikkuna_sijainti[0],cv_ikkuna_sijainti[1])
            cv2.waitKey(1)

    #after while loop let's ask user for the input...
    kysymys()

def kysymys():
    global image_np_with_detections
    global detected_item
    global detection_box
    global ikkuna_sijainti
    global cv_ikkuna_sijainti

    #let's set the assistant window to correct position according to detected item..
    apu_x=cv_ikkuna_sijainti[0]+detection_box[0]-70
    apu_y=cv_ikkuna_sijainti[1]+detection_box[1]-120
    change_position(ikkuna,apu_x,apu_y)

    #and let's put the assistant window on top...
    ikkuna.lift()

def tallennatiedot():
    print("Begin to save a file...")
    user_reaction=syote.get()

    #and save it to a text file:
    tiedostonimi="jotain" + str(np.random.randint(10000,20000)) + ".txt"
    tekstitiedosto=open(tiedostonimi,"w")
    teksti="We found " + detected_item + " and ate those " + user_reaction + " ...brp!"
    tekstitiedosto.write(teksti)
    tekstitiedosto.close()
    print("...text file saved!")


    painike_1['text']='Search'
    return

def lopeta():
    global cap
    cap.release()
    print("Search stopped!")

painike_1=tkinter.Button(ikkuna,text="Start",command=pollaus,height=5,width=20)
painike_1.grid(row=0,column=0,pady=10,padx=10)
painike_1.config(height=2,width=20)

otsikko=tkinter.Label(ikkuna,text="Enter amount and press OK")
otsikko.grid(row=0,column=1,pady=5,padx=10)

painike_2=tkinter.Button(ikkuna,text="OK",command=tallennatiedot,height=5,width=20)
painike_2.grid(row=0,column=2,pady=10,padx=10)
painike_2.config(height=2,width=20)

painike_3=tkinter.Button(ikkuna,text="Stop",command=lopeta,height=5,width=20)
painike_3.grid(row=1,column=0,pady=10,padx=10)
painike_3.config(height=2,width=20)


syote=tkinter.Entry(ikkuna,width=20)
syote.grid(row=1,column=1,pady=10,padx=5)

ikkuna.mainloop()
