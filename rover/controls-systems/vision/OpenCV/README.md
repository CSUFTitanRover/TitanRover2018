# ObjecRec

## Files and Folders 
### ball2.jpg
Is the file for the positive image of the tennis ball.
### bg.txt 
Is a list of all negative photos so that we can artificially create positives from single photo.
### cascade.xml 
Is the xml sheet that results from the training of the data it is used for the haar cascade.
### data 
This folder is the where the stages of the training populate.
### getImgs.py 

(do in this order to run as well)
#### def store_raw_images():
 
This file is an image scrapper it takes images from a specified url. It also creates a neg folder if not already, it also recises the image and renames the image allowing for multiple images to be downloaded with different names.
 
#### def find_uglies():
  This finds all the ugly photos (from broken linkes) and deletes them if the match a copy of an ugly img.
 

#### def create_pos_n_neg
  Inserts the names of the negatives into bg.tx.
 

## Terminal Commands
```
opencv_createsamples -img ball2.jpg -bg bg.txt -info info/info.lst -jpgoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1600
```
This command create artificial positives from ball2.jpg using the bg.txt as info where the negatives are. It has a max skewing angles of 0.5 to create more variation from the orignal. This allows the training to train to recognize the object in different orientations.

```
opencv_createsamples -info info/info.lst -num 1600 -w 20 -h 20 -vec positives.vec
```
This command will actually create the positives.vec file of grabing 1600 of the artificial positives at a 20x20 size 

```
opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 1400 -numNeg 700 -numStages 10 -w 20 -h 20
```
This begins the training for the Haar cascade. It utilizes both positives.vec file and bg.txt file to gain information on the pictures being compared. From the information it grabs 1400 positives and negs. 700 (The standard is to do a 2 to 1 ratio of positives and negatives) and trains them for 10 stages to reconize a 20x20.


## Developer's Notes
For this code I utilized a https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/ a bunch, most of the code can be attributed to this tutorials. I had to make some changes in the command line such as .jpg instead of pngoutput. If any issues utilize the tutorial as a ref. Training may also need to be redone, it will recognize the ball in only certain angles. I think this maybe to a couple of differnet issues including angle skewing and utilizing a low amount of artificial pos. I will try to adjust both, it was given an instruction to train 10 stages yet only trained for 6 due to the low acceptance ratio. This may be further evidence to my earllier point of low img count or skewing. 
