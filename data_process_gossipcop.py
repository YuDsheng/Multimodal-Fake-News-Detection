# -*- coding: utf-8 -*-

import re
import os
from PIL import Image
import numpy as np

data_path = 'C:\\Users\\YuDsheng\\Desktop\\codes_for_paper\\MFND\\data\\mcan_data\\gossipcop\\'
#data_path = 'C:\\Users\\YuDsheng\\Desktop\\codes_for_paper\\MFND\\data\\mcan_data\\politifact\\'


original_train_data = os.path.join(data_path, 'train_original.txt')
original_test_data = os.path.join(data_path, 'test_original.txt')
original_val_data = os.path.join(data_path, 'val_original.txt')

new_train = os.path.join(data_path, 'train.txt')
new_test = os.path.join(data_path, 'test.txt')
new_val = os.path.join(data_path, 'val.txt')


image_file_list = [os.path.join(data_path, 'train_images\\fake_images\\'), os.path.join(data_path, 'train_images\\real_images\\'), 
                   os.path.join(data_path, 'test_images\\'),os.path.join(data_path, 'val_images\\')]


def makedir(new_dir):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)


def read_images(file_list):
    image_list = {} 
    #img_num = 0
    for path in file_list:
        for filename in os.listdir(path):
            try:
                img = Image.open(path + filename).convert('RGB')
                img_id = filename.split('.')[0]
                image_list[img_id] = img
                #print('ok')
                #img_num += 1
            except:
                print(path + filename)
                os.remove(path + filename)
    return image_list#, img_num



def select_image(image_num, image_id_list, image_list):
    for i in range(image_num):
        #print('list:{}'.format(image_id_list))
        image_id = image_id_list[i]
        if image_id in image_list:
            #print('Yes, img_id:{}'.format(img_id))
            return image_id
    #f_log.write(line)
    return False                   
            

def get_max_len(file):

    #Get the maximal length of sentence in dataset

    f = open(file, 'r', encoding = 'UTF-8')
    
    max_post_len = 0
    
    lines = f.readlines()
    post_num = len(lines)
    for i in range(post_num):
        post_content = list(lines[i].split('|')[1].split())
        tmp_len = len("".join(post_content))
        if tmp_len > max_post_len:
            max_post_len = tmp_len
            
    f.close()
    return max_post_len

def get_data(dataset, image_list):
    if dataset == 'train':        
        data_file = new_train
    elif dataset == 'test':
        data_file = new_test
    elif dataset == 'val':
        data_file = new_val
        
    f = open(data_file, 'r', encoding = 'UTF-8')
    lines = f.readlines()
        
    data_post_id = []
    data_post_content = []
    data_image = []
    data_label = []   
        
    data_num = len(lines)
    unmatched_num = 0
        
    for line in lines:
        post_id = line.split('|')[0]
        post_content = line.split('|')[1]
        label = line.split('|')[-1].strip()
        
        image_id_list = line.split('|')[-2].strip().split(',')
        #print(image_id_list)
        img_num = len(image_id_list)
        image_id = select_image(img_num, image_id_list, image_list)
            
        if image_id != False:
            image = image_list[image_id]
                    
            data_post_id.append(int(post_id))
            data_post_content.append(post_content)
            data_image.append(image)
            data_label.append(int(label))
                    
        else:
            unmatched_num += 1
            continue
            
    f.close()
    
    data_dic = {'post_id': np.array(data_post_id),
                'post_content': data_post_content,
                'image': data_image,
                'label': np.array(data_label)
            }
    return data_dic, data_num-unmatched_num              


if __name__ == '__main__':
    
    print(get_max_len(new_train),get_max_len(new_test),get_max_len(new_val))
    #img_list,img_num = read_images(image_file_list)
    #print(img_num)
    img_list = read_images(image_file_list)
    train, train_num = get_data('train', img_list)
    #print(train)
    test, test_num = get_data('test', img_list)
    val, val_num = get_data('val', img_list)
    print(train_num,test_num,val_num,train_num+test_num+val_num)
