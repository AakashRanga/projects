l=[3,3,4,4]
j=[5,6,7,8]
l.append(5)
l.insert(3,5)
l.extend(j)
l.clear()
print(l)

# import time
# from tqdm import tqdm, trange

# for i in trange(10):
#     time.sleep(0.3)
#
# with tqdm(total=100) as pbar:
#     for i in range(10):
#         time.sleep(0.3)
#         pbar.update(10)

# pbar = tqdm(total=100)
# for i in range(10):
#     time.sleep(0.3)
#     pbar.update(10)
# pbar.close()


# my_time= int(input("Enter the time in seconds:"))
#
# for x in range(my_time,0,-1):
#     s = x%60
#     m=int(x/60)%60
#     h=int(x/3600)
#     print(f"{h:02}:{m:02}:{s:02}")
#     time.sleep(1)


# def countdown(t):
#     while t>0:
#         print(t)
#         t = t-1
#         time.sleep(1)
#     print("Ready for shipping")
#
# s = input("Enter the seconds:")
# while not s.isdigit():
#     s =input()
# s = int(s)
# countdown(s)


# prediction = "polysaccharide, mannuronic and guluronic acid units"
# product = "wound care"
# s=""
# if product == "edible water pods" and prediction == "calcium lactate or calcium chloride":
#     s="ok"
# elif product == "straws" and prediction == "Bacterial Cellulose, Rice, wheat, corn":
#     s="ok"
# elif product == "cosmetics" and prediction == "Hydrocolloids, Cellulose Gum, Sodium Stearoyl Lactylate":
#     s="ok"
# elif product == "fertilizers" and prediction == "magnesium, potassium, zinc, iron and nitrogen":
#     s="ok"
# elif product == "packages" and prediction == "essential oils, plant extracts, bacteriocins, enzymes, chitosan, organic acids,  metallic nanoparticles and chelating agents":
#     s="ok"
# elif product == "wound care" and prediction == "polysaccharide, mannuronic and guluronic acid units":
#     s="ok"
# elif product == "bio fuel" and prediction == "sulfonated graphene oxide":
#     s="ok"
#
# else:
#     s="Not satisfied"
# print(s)