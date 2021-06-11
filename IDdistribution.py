import random

def distribution(num):
    id = [i for i in range(1, num+1)]
    random.shuffle(id)
    
    abnormal_id = open("abnormal_id.txt", 'w')
    for i in range(0,70):
        abnormal_id.write(str(id[i]) + "\n")
    abnormal_id.close()
    
    normal_id=open('normal_id.txt', 'w')
    for i in range(70, num):
        normal_id.write(str(id[i]) + "\n")
    normal_id.close()
    
    print(id)

if __name__=='__main__':
    distribution(315)