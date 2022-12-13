# library to load the model
import pickle
import numpy as np
from utils import *
from PIL import Image
from pytesseract import Output
import pytesseract

# load the label model 
filename = './labelize/label_model.sav'
model = pickle.load(open(filename, 'rb'))


def price_label(txts):
    """
    Given a list of texts predict for each text if it is a price or not. Return a list of price labels of the same length than the input

    Input :
    txts : list of texts

    Output :
    price_labels : list of price 
    
    """

    price_labels = []
    for txt in txts:
        # If percent of alphanumeric is superior of 40% it's a price
        if sum([s.isalpha() for s in txt])/len(txt) < 0.4:
            price_labels.append('price')
        else:
            price_labels.append('other')
    return price_labels

def modifier_label(txts):
    """
    Given a list of texts predict for each text if it is a modifier or not. Return a list of modifiers labels of the same length than the input

    Input :
    txts : list of texts

    Output :
    price_labels : list of price 
    
    """

    modifier_labels = []
    for txt in txts:
        # If percent of alphanumeric is superior of 40% it's a price
        if 'add' in txt or 'Add' in txt:
            modifier_labels.append('modifier')
        else:
            modifier_labels.append('other')
    return modifier_labels

def get_label(txts):
    """
    Labelize a list of texts except the price using the pre-trained model. Return a list of labels of the same length than the input 
    
    """
    label_types = list(model.predict(txts))
    return label_types




def get_all_label_list(txts):
    """
     Labelize a list of texts . Return a list of labels (prices and others) of the same length than the input 
    
    Input :
    -image_path : path of the image to labelize

    Output :
    -df : panda DataFrame with boxes, scores, texts, labels
    """
    # get results from ocr
    labels_types = get_label(txts)
    price_labels = price_label(txts)
    modifier_labels = modifier_label(txts)
    df = pd.DataFrame({"type":labels_types,'price':price_labels,'modifier':modifier_labels})
    df['type'] = np.where(df['price']!='other',df['price'],df['type'])
    df['type'] = np.where(df['modifier']=='modifier',df['modifier'],df['type'])
    return list(df['type'])

def label_result_from_path(img_path):
    """
    Return an panda DataFrame with boxes, scores, texts, labels for all detetcion on the input image 
    
    Input :
    -image_path : path of the image to labelize

    Output :
    -df : panda DataFrame with boxes, scores, texts, labels
    """
    # get results from ocr
    boxes,txts,scores = get_ocr_txts_boxes_scores(img_path)
    labels_types = get_label(txts)
    price_labels = price_label(txts)
    modifier_labels = modifier_label(txts)
    df = pd.DataFrame({"type":labels_types,'price':price_labels,'modifier':modifier_labels})
    df['type'] = np.where(df['price']!='other',df['price'],df['type'])
    df['type'] = np.where(df['modifier']=='modifier',df['modifier'],df['type'])
    del df['price']
    del df['modifier']
    return df


if __name__=="__main__":    
    # img_path = './demo/0016F00003jELMVBarkingDogHotel_97783642_05.11.2020BarkingDogMenu1.pdf_page_1.jpg'
    # print(label_result_from_path(img_path))
    #txts = ['margarita cocktail','service','chicken','burger','jack daniels','gluten free']
    pass
