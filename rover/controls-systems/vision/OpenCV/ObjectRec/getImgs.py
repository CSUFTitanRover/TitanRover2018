import urllib
import urllib2
import numpy as np
import os
import cv2

def store_raw_images():
 #//image-net.org/api/text/imagenet.synset.geturls?wnid=n02960352
 #http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152
 #http://image-net.org/api/text/imagenet.synset.geturls?wnid=n02708433
 neg_images_link = ''
 neg_image_urls = urllib2.urlopen(neg_images_link).read().decode()
 pic_num = 1959
 if not os.path.exists('neg'):
  os.makedirs('neg')
 for i in neg_image_urls.split('\n'):
  try:
   #print(i)
   urllib.urlretrieve(i, "neg/"+str(pic_num)+'.jpg')
   img = cv2.imread("neg/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
   resized_image = cv2.resize(img, (100, 100))
   cv2.imwrite('neg/'+str(pic_num)+'.jpg',resized_image)
   pic_num += 1
  except Exception as e:
   print('Error',str(pic_num))
def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))


def create_pos_n_neg():
    for file_type in ['neg']:

        for img in os.listdir(file_type):

            if file_type == 'pos':
                line = file_type + '/' + img + ' 1 0 0 50 50\n'
                with open('info.dat', 'a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type + '/' + img + '\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)
create_pos_n_neg()
#find_uglies()
#store_raw_images()

opencv_createsamples -img ball2.jpg -bg bg.txt -info info/info.lst -jpgoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1600
opencv_createsamples -info info/info.lst -num 1600 -w 20 -h 20 -vec positives.vec
opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 1400 -numNeg 700 -numStages 10 -w 20 -h 20