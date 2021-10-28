from images import *

ideal_list = ['image-segments-320/banana1-320.jpg',
              'image-segments-320/banana2-320.jpg',
              'image-segments-320/banana3-320.jpg',
              'image-segments-320/book-320.jpg',
              'image-segments-320/bool-320.jpg',
              'image-segments-320/bush-320.jpg',
              'image-segments-320/ceramic-320.jpg',
              'image-segments-320/cross-320.jpg',
              'image-segments-320/doll-320.jpg',
              'image-segments-320/elefant-320.jpg',
              'image-segments-320/flower-320.jpg',
              'image-segments-320/fullmoon-320.jpg',
              'image-segments-320/grave-320.jpg',
              'image-segments-320/llama-320.jpg',
              'image-segments-320/memorial-320.jpg',
              'image-segments-320/music-320.jpg',
              'image-segments-320/person1-320.jpg',
              'image-segments-320/person2-320.jpg',
              'image-segments-320/person3-320.jpg',
              'image-segments-320/person4-320.jpg',
              'image-segments-320/person5-320.jpg',
              'image-segments-320/person6-320.jpg',
              'image-segments-320/person7-320.jpg',
              'image-segments-320/person8-320.jpg',
              'image-segments-320/scissors-320.jpg',
              'image-segments-320/sheep-320.jpg',
              'image-segments-320/stone1-320.jpg',
              'image-segments-320/stone2-320.jpg',
              'image-segments-320/teddy-320.jpg',
              'image-segments-320/tennis-320.jpg']

my_list = ['segmented_images/banana1-gr-320_1.0l5.0s4n.jpg',
           'segmented_images/banana1-gr-320_5l1s4n.jpg',
           'segmented_images/banana1-gr-320_1l1s4n.jpg',
           'segmented_images/banana1-gr-320_1l1s8n.jpg',
           'segmented_images/banana2-gr-320_1l1s4n.jpg',
           'segmented_images/banana2-gr-320_1l1s8n.jpg',
           'segmented_images/banana2-gr-320_1l5s4n.jpg',
           'segmented_images/banana2-gr-320_5l1s4n.jpg',
           'segmented_images/banana3-gr-320_1l1s4n.jpg',
           'segmented_images/banana3-gr-320_1l1s8n.jpg',
           'segmented_images/banana3-gr-320_1l5s4n.jpg',
           'segmented_images/banana3-gr-320_5l1s4n.jpg',
           'segmented_images/book-gr-320_1l10s8n.jpg',
           'segmented_images/bool-gr-320_7l4s4n.jpg',
           'segmented_images/bush-gr-320_2l20s8n.jpg',
           'segmented_images/ceramic-gr-320_1l1s4n.jpg',
           'segmented_images/cross-gr-320.jpg',
           'segmented_images/doll-gr-3201l1s4n.jpg',
           'segmented_images/elefant-gr-320.jpg',
           'segmented_images/flower-gr-320.jpg',
           'segmented_images/fullmoon-gr-320.jpg',
           'segmented_images/grave-gr-320_1l3s8n.jpg',
           'segmented_images/llama-gr-320_3l2s4n.jpg',
           'segmented_images/memorial-gr-320.jpg',
           'segmented_images/music-gr-320_1l1s8n.jpg',
           'segmented_images/person1-gr-320_1l1s4n.jpg',
           'segmented_images/person2-gr-320_1l1s8n.jpg',
           'segmented_images/person3-gr-320_5l5s4n.jpg',
           'segmented_images/person4-gr-3201l1s4n.jpg',
           'segmented_images/person5-gr-320_1l1s8n.jpg',
           'segmented_images/person6-gr-320_1l1s4n.jpg',
           'segmented_images/person7-gr-320_1l1s4n.jpg',
           'segmented_images/person8-gr-320_1l7s8n.jpg',
           'segmented_images/scissors-gr-320.jpg',
           'segmented_images/sheep-gr-320_1l1s4n.jpg',
           'segmented_images/stone1-gr-320_6l1s8n.jpg',
           'segmented_images/stone2-gr-320_1l2s4n.jpg',
           'segmented_images/teddy-gr-320_10l5s4n.jpg',
           'segmented_images/tennis-gr-320.jpg'
           ]

with open('seqmentation_adequacy.txt', 'a') as f:
    i = 0
    j = 0
    for j in range(4):
        img1 = Image.open(ideal_list[i])
        img2 = Image.open(my_list[j])
        result = adequacy(img1, img2)
        f.write(f'Comparing {ideal_list[i]} and {my_list[j]}: \n\
                Right/total ratio: {round(result[0], 3)}\t\
                Jaccard measure: {round(result[1], 3)}\n\n')
    i += 1
    for j in range(4, 8):
        img1 = Image.open(ideal_list[i])
        img2 = Image.open(my_list[j])
        result = adequacy(img1, img2)
        f.write(f'Comparing {ideal_list[i]} and {my_list[j]}: \n\
                Right/total ratio: {round(result[0], 3)}\t\
                Jaccard measure: {round(result[1], 3)}\n\n')
    i += 1
    for j in range(8, 12):
        img1 = Image.open(ideal_list[i])
        img2 = Image.open(my_list[j])
        result = adequacy(img1, img2)
        f.write(f'Comparing {ideal_list[i]} and {my_list[j]}: \n\
                Right/total ratio: {round(result[0], 3)}\t\
                Jaccard measure: {round(result[1], 3)}\n\n')
    i += 1
    for j in range(12, len(my_list)):
        img1 = Image.open(ideal_list[i])
        img2 = Image.open(my_list[j])
        result = adequacy(img1, img2)
        f.write(f'Comparing {ideal_list[i]} and {my_list[j]}: \n\
                Right/total ratio: {round(result[0], 3)}\t\
                Jaccard measure: {round(result[1], 3)}\n\n')
        i += 1