import cv2.cv2 as cv
import os
import random
import threading
import time


def take_image_from_website_and_save_as_file(file_name, url):
    import requests

    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)
def image_search(image,num):
    import requests
    from bs4 import BeautifulSoup

    images_list = []
    r = requests.get(f'https://unsplash.com/s/photos/{image}')
    doc = BeautifulSoup(r.text,'html.parser')
    images = doc.find_all('img')
    for i in images:
        i = i['src']
        if 'images.unsplash.com' in i:
            if len(images_list) < num:
                images_list.append(i)

    if len(images_list) >= num:
        return images_list


    r = requests.get(f'https://www.google.com.my/search?q={image}&hl=en&tbm=isch&sxsrf=APq-WBuf60TYpYHilon2wvLE_4hQ2TtKCQ%3A1649476166284&source=hp&biw=1536&bih=754&ei=RgJRYv6DD-SWr7wPjMyu2AI&iflsig=AHkkrS4AAAAAYlEQVlb_1t-Pu9bihsu73cfdfrPJPJrt&ved=0ahUKEwj-vtHHiYb3AhVky4sBHQymCysQ4dUDCAc&uact=5&oq=banana&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzIICAAQsQMQgwEyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCxAxCDATIICAAQgAQQsQM6CggjEO8DEOoCECc6BwgjEO8DECc6BAgAEAM6BQgAEIAEUOQDWPoKYKsMaAFwAHgAgAEviAHyAZIBATaYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img')
    doc = BeautifulSoup(r.text,'html.parser')
    images = doc.find_all('a')
    for i in images:
        img = i.find('img')
        if img and 'https' in img['src']:
            if len(images_list) < num:
                images_list.append(img['src'])
    return images_list

nouns = ['variety', 'video', 'week', 'security', 'country', 'exam', 'movie', 'organization', 'equipment', 'physics',
         'analysis', 'policy', 'series', 'thought', 'basis', 'boyfriend', 'direction', 'strategy', 'technology', 'army',
         'camera', 'freedom', 'paper', 'environment', 'child', 'instance', 'month', 'truth', 'marketing', 'university',
         'writing', 'article', 'department', 'difference', 'goal', 'news', 'audience', 'fishing', 'growth', 'income',
         'marriage', 'user', 'combination', 'failure', 'meaning', 'medicine', 'philosophy', 'teacher', 'communication',
         'night', 'chemistry', 'disease', 'disk', 'energy', 'nation', 'road', 'role', 'soup', 'advertising', 'location',
         'success', 'addition', 'apartment', 'education', 'math', 'moment', 'painting', 'politics', 'attention',
         'decision', 'event', 'property', 'shopping', 'student', 'wood', 'competition', 'distribution', 'entertainment',
         'office', 'population', 'president', 'unit', 'category', 'cigarette', 'context', 'introduction', 'opportunity',
         'performance', 'driver', 'flight', 'length', 'magazine', 'newspaper', 'relationship', 'teaching', 'cell',
         'dealer', 'finding', 'lake', 'member', 'message', 'phone', 'scene', 'appearance', 'association', 'concept',
         'customer', 'death', 'discussion', 'housing', 'inflation', 'insurance', 'mood', 'woman', 'advice', 'blood',
         'effort', 'expression', 'importance', 'opinion', 'payment', 'reality', 'responsibility', 'situation', 'skill',
         'statement', 'wealth', 'application', 'city', 'county', 'depth', 'estate', 'foundation', 'grandmother',
         'heart', 'perspective', 'photo', 'recipe', 'studio', 'topic', 'collection', 'depression', 'imagination',
         'passion', 'percentage', 'resource', 'setting', 'ad', 'agency', 'college', 'connection', 'criticism', 'debt',
         'description', 'memory', 'patience', 'secretary', 'solution', 'administration', 'aspect', 'attitude',
         'director', 'personality', 'psychology', 'recommendation', 'response', 'selection', 'storage', 'version',
         'alcohol', 'argument', 'complaint', 'contract', 'emphasis', 'highway', 'loss', 'membership', 'possession',
         'preparation', 'steak', 'union', 'agreement', 'cancer', 'currency', 'employment', 'engineering', 'entry',
         'interaction', 'mixture', 'preference', 'region', 'republic', 'tradition', 'virus', 'actor', 'classroom',
         'delivery', 'device', 'difficulty', 'drama', 'election', 'engine', 'football', 'guidance', 'hotel', 'owner',
         'priority', 'protection', 'suggestion', 'tension', 'variation', 'anxiety', 'atmosphere', 'awareness', 'bath',
         'bread', 'candidate', 'climate', 'comparison', 'confusion', 'construction', 'elevator', 'emotion', 'employee',
         'employer', 'guest', 'height', 'leadership', 'mall', 'manager', 'operation', 'recording', 'sample',
         'transportation', 'charity', 'cousin', 'disaster', 'editor', 'efficiency', 'excitement', 'extent', 'feedback',
         'guitar', 'homework', 'leader', 'mom', 'outcome', 'permission', 'presentation', 'promotion', 'reflection',
         'refrigerator', 'resolution', 'revenue', 'session', 'singer', 'tennis', 'basket', 'bonus', 'cabinet',
         'childhood', 'church', 'clothes', 'coffee', 'dinner', 'drawing', 'hair', 'hearing', 'initiative', 'judgment',
         'lab', 'measurement', 'mode', 'mud', 'orange', 'poetry', 'police', 'possibility', 'procedure', 'queen',
         'ratio', 'relation', 'restaurant', 'satisfaction', 'sector', 'signature', 'significance', 'song', 'tooth',
         'town', 'vehicle', 'volume', 'wife', 'accident', 'airport', 'appointment', 'arrival', 'assumption', 'baseball',
         'chapter', 'committee', 'conversation', 'database', 'enthusiasm', 'error', 'explanation', 'farmer', 'gate',
         'girl', 'hall', 'historian', 'hospital', 'injury', 'instruction', 'maintenance', 'manufacturer', 'meal',
         'perception', 'pie', 'poem', 'presence', 'proposal', 'reception', 'replacement', 'revolution', 'river', 'son',
         'speech', 'tea', 'village', 'warning', 'winner', 'worker', 'writer', 'assistance', 'breath', 'buyer', 'chest',
         'chocolate', 'conclusion', 'contribution', 'cookie', 'courage', 'desk', 'drawer', 'establishment',
         'examination', 'garbage', 'grocery', 'honey', 'impression', 'improvement', 'independence', 'insect',
         'inspection', 'inspector', 'king', 'ladder', 'menu', 'penalty', 'piano', 'potato', 'profession', 'professor',
         'quantity', 'reaction', 'requirement', 'salad', 'sister', 'supermarket', 'tongue', 'weakness', 'wedding',
         'affair', 'ambition', 'analyst', 'apple', 'assignment', 'assistant', 'bathroom', 'bedroom', 'beer', 'birthday',
         'celebration', 'championship', 'cheek', 'client', 'consequence', 'departure', 'diamond', 'dirt', 'ear',
         'fortune', 'friendship', 'funeral', 'gene', 'girlfriend', 'hat', 'indication', 'intention']

STOP = False

correct = 0
wrong = 0
total = 0

def ask_input(i):
    global STOP
    global correct
    global wrong
    global total
    global variety
    global image_query
    global testing

    i = list(i)
    result = ''.join(i)
    random.shuffle(i)
    anagram = ''.join(i)

    while anagram == result:
        random.shuffle(i)
        anagram = ''.join(i)
    print(f"Anagram: {anagram}")
    response = input('Answer: ').replace(' ', '')

    if response == result:
        print('Correct! ')
        correct += 1
        total += 1
        print(f'{correct} correct in {total} word(s). Incorrect: {wrong}')
        print()
        STOP = True
    else:
        print(f'Wrong answer! The correct answer is: {result}.')
        wrong += 1
        total += 1
        print(f'{correct} correct in {total} word(s). Incorrect: {wrong}')
        print()
        STOP = True


variety = int(input('Number of images per cycle: '))

while True:
    i = random.choice(nouns)
    nouns.remove(i)
    if len(i) not in range(5, 11) or '_' in i:
        continue

    image_query = image_search(i, variety)
    variety = len(image_query)
    current = 0
    take_image_from_website_and_save_as_file('f1.jpg', image_query[current])

    img = cv.imread("f1.jpg", -1)

    dimensions = img.shape
    height = img.shape[0]
    width = img.shape[1]

    d = height / 700
    height = height / d
    width = width / d

    img = cv.resize(img, (int(width), int(height)))
    cv.imshow("GUESS", img)
    x = threading.Thread(target=ask_input, daemon=True, args=(i,))
    x.start()

    while True:
        global stop

        cv.imshow("GUESS", img)
        key = cv.waitKey(2000)
        if key == ord('q') or STOP:

            STOP = False
            cv.destroyAllWindows()
            break
        # elif key == ord('.'):

        if current >= variety - 1:
            current = 0

        else:
            current += 1

        take_image_from_website_and_save_as_file('f1.jpg', image_query[current])

        img = cv.imread("f1.jpg", -1)

        dimensions = img.shape
        height = img.shape[0]
        width = img.shape[1]

        d = height / 700
        height = height / d
        width = width / d

        img = cv.resize(img, (int(width), int(height)))
        continue

    os.remove('f1.jpg')
