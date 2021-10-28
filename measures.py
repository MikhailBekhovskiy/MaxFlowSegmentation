from images import *

ideal_list = ['image-segments-320/cross-320.jpg',
              'image-segments-320/stone1-320.jpg']

my_list = ['parametric_research/cross-gr-320_1l1s4n.jpg',
           'parametric_research/cross-gr-320_5l1s4n.jpg',
           'parametric_research/cross-gr-320_10l1s4n.jpg',
           'parametric_research/cross-gr-320_15l1s4n.jpg',
           'parametric_research/cross-gr-320_20l1s4n.jpg',
           'parametric_research/cross-gr-320_1l5s4n.jpg',
           'parametric_research/cross-gr-320_1l10s4n.jpg',
           'parametric_research/cross-gr-320_1l15s4n.jpg',
           'parametric_research/cross-gr-320_1l20s4n.jpg',
           'parametric_research/cross-gr-320_1l1s8n.jpg',
           'parametric_research/cross-gr-320_5l1s8n.jpg',
           'parametric_research/cross-gr-320_1l5s8n.jpg',
           'parametric_research/stone1-gr-320_1l1s4n.jpg',
           'parametric_research/stone1-gr-320_5l1s4n.jpg',
           'parametric_research/stone1-gr-320_10l1s4n.jpg',
           'parametric_research/stone1-gr-320_15l1s4n.jpg',
           'parametric_research/stone1-gr-320_20l1s4n.jpg',
           'parametric_research/stone1-gr-320_1l5s4n.jpg',
           'parametric_research/stone1-gr-320_1l10s4n.jpg',
           'parametric_research/stone1-gr-320_1l15s4n.jpg',
           'parametric_research/stone1-gr-320_1l20s4n.jpg',
           'parametric_research/stone1-gr-320_1l1s8n.jpg',
           'parametric_research/stone1-gr-320_5l1s8n.jpg',
           'parametric_research/stone1-gr-320_1l5s8n.jpg'
           ]

with open('parameters_res.txt', 'a') as f:
    j = 0
    for j in range(12):
        img1 = Image.open(ideal_list[0])
        img2 = Image.open(my_list[j])
        result = adequacy(img1, img2)
        f.write(f'Comparing {ideal_list[0]} and {my_list[j]}: \n\
                Right/total ratio: {round(result[0], 3)}\t\
                Jaccard measure: {round(result[1], 3)}\n\n')
    for j in range(12, 24):
        img1 = Image.open(ideal_list[1])
        img2 = Image.open(my_list[j])
        result = adequacy(img1, img2)
        f.write(f'Comparing {ideal_list[1]} and {my_list[j]}: \n\
                Right/total ratio: {round(result[0], 3)}\t\
                Jaccard measure: {round(result[1], 3)}\n\n')
