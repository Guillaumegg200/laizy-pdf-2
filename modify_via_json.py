from utils import *

from detector.predict import *

color_list = ['#BFD8D5','#F9D4C2','#F7EBC5','#C4DEF2','#C2D3F2','#FEC8D8','#D0DFBD','#CABFDE','#E0CBBD','#FFF8E6','#FFE2DE','#ADB2C5','#B5CFD1','#D9E4E6','#F9CBA5','#FDE2BB','#FEF2E6','#95C7CC','#9A9A9A','#800000','#008000','#000080','#808000','#800080','#008080','#C0C0C0','#808080','#9999FF','#993366','#FFFFCC','#CCFFFF','#660066','#FF8080','#0066CC','#CCCCFF','#000080','#FF00FF','#FFFF00','#00FFFF','#800080','#800000','#008080','#0000FF','#00CCFF','#CCFFFF','#CCFFCC','#FFFF99','#99CCFF','#FF99CC','#CC99FF','#FFCC99','#3366FF','#33CCCC','#99CC00','#FFCC00','#FF9900','#FF6600','#666699','#969696','#003366','#339966','#003300','#333300','#993300','#993366','#333399','#FFFFFF','#FF0000','#00FF00','#0000FF','#FFFF00','#FF00FF','#00FFFF']





def get_item_boxes_from_path(via_json_path):
    """
    From the path of a via json containing boxes of items boxes return all the boxes

    Input :
    - via_json_path : path to the json file containing boxes

    Output :
    boxes_by_file : dictionnary conatining for each key (filename) a list of all boxes
    """
    via_json_dict = read_json(via_json_path)
    boxes_by_file = {}
    for file in via_json_dict:
        item_boxes = []
        for region in via_json_dict[file]['regions']:
            if region['region_attributes']['regions'] == 'item':
                x,y,w,h = region['shape_attributes']['x'],region['shape_attributes']['y'],region['shape_attributes']['width'],region['shape_attributes']['height']
                item_boxes.append([x,y,w,h])
        boxes_by_file[via_json_dict[file]['filename']] = item_boxes   
    return boxes_by_file

def get_item_boxes(via_json_dict):
    """
    From a via json containing boxes of items boxes return all the boxes

    Input :
    - via_json :json file containing boxes

    Output :
    boxes_by_file : dictionnary conatining for each key (filename) a list of all boxes
    """
    boxes_by_file = {}
    for file in via_json_dict:
        item_boxes = []
        for region in via_json_dict[file]['regions']:
            if region['region_attributes']['regions'] == 'item':
                x,y,w,h = region['shape_attributes']['x'],region['shape_attributes']['y'],region['shape_attributes']['width'],region['shape_attributes']['height']
                item_boxes.append([x,y,w,h])
        boxes_by_file[via_json_dict[file]['filename']] = item_boxes   
    return boxes_by_file

def get_section_boxes_from_path(via_json_path):
    """
    From the path of a via json containing boxes of items boxes return all the boxes

    Input :
    - via_json_path : path to the json file containing boxes

    Output :
    boxes_by_file : dictionnary conatining for each key (filename) a list of all boxes
    """
    via_json_dict = read_json(via_json_path)
    boxes_by_file = {}
    for file in via_json_dict:
        item_boxes = []
        for region in via_json_dict[file]['regions']:
            if region['region_attributes']['regions'] == 'section':
                x,y,w,h = region['shape_attributes']['x'],region['shape_attributes']['y'],region['shape_attributes']['width'],region['shape_attributes']['height']
                item_boxes.append([x,y,w,h])
        boxes_by_file[via_json_dict[file]['filename']] = item_boxes   
    return boxes_by_file

def get_section_boxes(via_json_dict):
    """
    From a via json containing boxes of items boxes return all the boxes

    Input :
    - via_json :json file containing boxes

    Output :
    boxes_by_file : dictionnary conatining for each key (filename) a list of all boxes
    """
    boxes_by_file = {}
    for file in via_json_dict:
        item_boxes = []
        for region in via_json_dict[file]['regions']:
            if region['region_attributes']['regions'] == 'section':
                x,y,w,h = region['shape_attributes']['x'],region['shape_attributes']['y'],region['shape_attributes']['width'],region['shape_attributes']['height']
                item_boxes.append([x,y,w,h])
        boxes_by_file[via_json_dict[file]['filename']] = item_boxes   
    return boxes_by_file

def find_closest_box(box,boxes):
    """
    Find the item box which the box is the most probable to belong

    Input :
    box Coordonate of the input box (x,y,w,h)
    boxes : list of the boxes of all items or sections

    Output :
    j_max coordinates of the box otherwise -1

    """
    #max surface and the correspondent box
    s_max,j_max = 0,-1
    # coordonates of the box
    x,y,w,h = box[0],box[1],box[2],box[3]
    for j,item_box in enumerate(boxes):

        #coordonnate of the item box
        xi,yi,wi,hi = item_box[0],item_box[1],item_box[2],item_box[3]
        if x > xi + wi:
            s = 0
        elif x + w < xi:
            s = 0
        else:
            if y + h < yi:
                s=0
            elif y > yi + hi:
                s=0
            else:
                # width of the shared box
                bw = min(x+w,xi+wi) - max(x,xi)
                #height of the share box
                hb = min(y+h,yi+hi) - max(y,yi)
                # Compute the surface
                s = hb*bw
        if s > s_max:
            j_max = j
            s_max = s
    if s_max > 0.5*h*w:
        return j_max
    else:
        return -1





def read_text_via_from_path(DIR,via_label_json_path):
    """
    Given a json file and the path of the folder containing all the image in this json_file return a dictionnary de pandaDataframe with labels, texts and boxes in all the image and the keys are the name of the images

    Input :
    DIT : folder path containing images of the json
    via_json_path : json from via containing labels of the boxes

    Ourput:
    res : dictionnary of pd
    
    """
    via_label_json_dict = read_json(via_label_json_path)
    res = {}
    
    for file in via_label_json_dict:
        labels,txts,boxes = [],[],[]
        filename = via_label_json_dict[file]['filename']
        for region in via_label_json_dict[file]['regions']:
            label = region['region_attributes']['regions']
            x,y,w,h = region['shape_attributes']['x'],region['shape_attributes']['y'],region['shape_attributes']['width'],region['shape_attributes']['height']
            box = [x,y,w,h]
            img_path = DIR + '/' + filename
            im = Image.open(img_path)
            im_w,im_h = im.size
            im_crop = im.crop((max(0,x-0.10*w), max(0,y-0.10*h), min(im_w,x+1.10*w), min(im_h,y+1.10*h)))
            im_crop.save(DIR + '/test.jpg')
            result = ocr_results(DIR + '/test.jpg')
            os.remove(DIR + '/test.jpg')
            txt = ' '.join([line[1][0] for line in result])
            #txt = pytesseract.image_to_string(im_crop)
            txts.append(txt)
            boxes.append(box)
            labels.append(label)
        res[filename] = {'labels':labels,'txts':txts,'boxes':boxes}
    return res



def read_text_via(DIR,via_label_json_dict):
    """
    Given a json file and the path of the folder containing all the image in this json_file return a dictionnary de pandaDataframe with labels, texts and boxes in all the image and the keys are the name of the images

    Input :
    DIT : folder path containing images of the json
    via_label_json_dict : json from via containing labels of the boxes

    Ourput:
    res : dictionnary of pd
    
    """
    res = {}
    
    for file in via_label_json_dict:
        labels,txts,boxes = [],[],[]
        filename = via_label_json_dict[file]['filename']
        for region in via_label_json_dict[file]['regions']:
            label = region['region_attributes']['regions']
            x,y,w,h = region['shape_attributes']['x'],region['shape_attributes']['y'],region['shape_attributes']['width'],region['shape_attributes']['height']
            box = [x,y,w,h]
            img_path = DIR + '/' + filename
            im = Image.open(img_path)
            im_w,im_h = im.size
            im_crop = im.crop((max(0,x-0.10*w), max(0,y-0.10*h), min(im_w,x+1.10*w), min(im_h,y+1.10*h)))
            im_crop.save(DIR + '/test.jpg')
            result = ocr_results(DIR + '/test.jpg')
            os.remove(DIR + '/test.jpg')
            txt = ' '.join([line[1][0] for line in result])
            #txt = pytesseract.image_to_string(im_crop)
            txts.append(txt)
            boxes.append(box)
            labels.append(label)
        res[filename] = {'labels':labels,'txts':txts,'boxes':boxes}
    return res

def group_item_from_path(DIR,via_label_json_path,via_item_json_path):
    """
    
    Input :
    -DIR : path to the images in the json
    - via_label_json_path : json file containing boxes of texts via VIA
    - via_item_json_path : json file containing boxes of items via VIA
    
    Output:

    - df : panda Dataframe where texts are grouped
    """
    dict_item_boxes = get_item_boxes_from_path(via_item_json_path)
    dict_section_boxes = get_section_boxes_from_path(via_item_json_path)

    dict_df_labels  = read_text_via_from_path(DIR,via_label_json_path)
    page = 0
    df_group_texts = pd.DataFrame()   
    for filename in dict_df_labels.keys():
        item_boxes = dict_item_boxes[filename]
        section_boxes = dict_section_boxes[filename]
        df = pd.DataFrame(dict_df_labels[filename])
        df['group'] = -1
        boxes = list(df['boxes'])
        for i,box in enumerate(boxes):
            #region_attributes = {"section":False,"price":False,"dish":False,"description":False}
            x,y,w,h = box[0],box[1],box[2],box[3]
            box = [x,y,w,h]
            j_max = find_closest_box(box,item_boxes)
            df['group'][i] = j_max
            
            j_max = find_closest_box(box,section_boxes)
            df['section'][i] = j_max
  
            df['page'] = page
        page+=1
        df_group_texts = pd.concat([df_group_texts,df])
    return df_group_texts


def modify_df_group(df):
    df = df.loc[((df['group']!=-1)|(df['section']!=-1))][['group','section','page','txts','labels']].copy()
    df = df[['group','section','page','txts','labels']].copy()
    df = df.copy().pivot_table(index=['page','section','group'], columns='labels', values='txts',aggfunc=lambda x: ' '.join(x))
    for column in ['category','name','description','price','modifier','dietary']:
        if column not in df.columns:
            df[column] = ''
    df = df[['category','name','description','price','modifier','dietary']].reset_index()
    df['category'] = df['category'].fillna('')
    df = df.merge(df[['section','page','category']].groupby(['page','section']).agg({'category': lambda x : ' '.join(x.unique())}).rename(columns = {'category':'category_name'}),how = 'left',on = ['page','section'])
    df = df.sort_values(['page','section','name'])
    for c in ['name','description','category_name','modifier']:
        df[c] = df[c].fillna('')
        df[c] = df[c].apply(clean_text)
        df[c] = df[c].apply(lambda x: string.capwords(x))
    df = df.explode('price').reset_index(drop=True)
    return df

def group_item(DIR,dict_df_labels,dict_item_boxes,dict_section_boxes):
    """
    
    Input :
    -DIR : path to the images in the json
    - via_label_json_path : json file containing boxes of texts via VIA
    - via_item_json_path : json file containing boxes of items via VIA
    
    Output:

    - df : panda Dataframe where texts are grouped
    """

    page = 0
    df_group_texts = pd.DataFrame()   
    for filename in dict_df_labels.keys():
        item_boxes = dict_item_boxes[filename]
        section_boxes = dict_section_boxes[filename]
        df = pd.DataFrame(dict_df_labels[filename])
        df['group'] = -1
        df['section'] = -1
        boxes = list(df['boxes'])
        for i,box in enumerate(boxes):
            #region_attributes = {"section":False,"price":False,"dish":False,"description":False}
            x,y,w,h = box[0],box[1],box[2],box[3]
            box = [x,y,w,h]
            j_max = find_closest_box(box,item_boxes)
            df['group'][i] = j_max
            
            j_max = find_closest_box(box,section_boxes)
            df['section'][i] = j_max
  
            df['page'] = page

        page+=1
        df_group_texts = pd.concat([df_group_texts,df])
    

    df_group_pivot = modify_df_group(df_group_texts)
    df_formatted_menu = format_menu(df_group_pivot)
    save_final_excel(DIR,df_formatted_menu)



def color_row(row,category_color):
    return(['background-color: {}'.format(category_color[row.loc['Color']]) for r in row])

def format_menu(df_group_pivot):
    """
    Given the pandaFrame in output of modify_df_group format the excel in the way of menu builders use it

    Inout :
    df_group_pivot : Panda DatFrame

    Output :
    Panda Dataframe formatted
    """

    df = pd.DataFrame({'Type':np.nan,'Master Product Name':df_group_pivot['name'],"Internal Name":np.nan,'Description':df_group_pivot['description'],'Variant Name':np.nan,'Price':df_group_pivot['price'],'SKU':np.nan,'Category':df_group_pivot['category_name'],'Modifier':df_group_pivot['modifier'],'Diatery':df_group_pivot['dietary'],'Color':df_group_pivot['section']+ df_group_pivot['page']})
    category_color = {}
    for i,category in enumerate(df['Color'].unique()):
        category_color[category] = color_list[i]
    df = df.style.apply(lambda x : color_row(x,category_color),axis = 1)
    return df

def save_final_excel(DIR,df):
    """
    Fron a pandaDataFrame save an excel

    Input :
    df : PandaDataFrame

    Output :
    None

    """
    column_width = 60
    writer = pd.ExcelWriter(DIR + '/menu_template.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Products', index=False)
    for column in ['Master Product Name','Description','Category']:
            col_idx = df.columns.get_loc(column)
            writer.sheets['Products'].set_column(col_idx, col_idx, column_width)
    writer.save()


if __name__=="__main__":
    #print(group_item_from_path(DIR = "../Menu building/demo",via_label_json_path = "../Menu building/demo/pdf_json.json",via_item_json_path = "../Menu building/demo/item_demo_json.json"))
    # pdf_path = './0016F00003jELMVBarkingDogHotel_97783642_05.11.2020BarkingDogMenu1.pdf'
    # print(demo_excel(pdf_path,'./temp'))
    #create_final_excel()
    pass