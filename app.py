import pyxel
from random import *


# --------------------
# 초기값 및 전역 변수
# --------------------


# 기본 자원
gold = 0
member = 1
cnt_fryer = 1
chicken_price = 10000
chicken_level = 1
employ_cost = [50_000_000, 80_000_000, 130_000_000, 200_000_000]

my_side = "French Fries"
side_list = ["French Fries", "Cheese Ball", "Golden Cheese Ball"]
side_prices = [0, 1000000, 100000000]
bonus_percent = [10, 20, 30]
isSpawned = False
spawn_timer = randint(1800, 5400) # 사이드 스폰 1분 ~ 3분
side_x, side_y = -1, -1
side_click_cooldown = 0 # 버그 방지용

fever_timer = 0
fever_bonus = [3, 5, 7]
fever_multi = 1

gpc = 0 #gold per click
gps = 0 #gold per second

stores = ["Pknu", "NewYork", "Earth", "Moon"]
store_prices = [250_000, 40_000_000, 120_000_000, 5_000_000_000]
store_incomes = [1_000, 20_000, 150_000, 500_000] # 1 프레임 당 지점별 수입 
store_counts = [0, 0, 0, 0] # 각 지점별 구매 개수

# 클릭 이펙트
click_list = [] # 클릭 x, 클릭 y, 타이머, 골드량

# 시간 관련 설정
day_of_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
current_day = 23
current_month = 6
current_year = 2025


# 게임 상태 관련
game_state = "playing"
print_message = ""
print_timer = 0

# 치킨 조합 관련
textures = ["Crispy", "Juicy", "Chewy", "Tender"]
styles = ["Fried", "Spicy", "Soy", "Honey"]
sub_materials = ["Kimchi", "Garlic", "Onion", "Cheese"]
chicken_name = "Original Chicken"

# 치킨 클래스: 노말 레어 에픽 레전드 
legendary_chickens = [  
    ("Chewy", "Soy", "Kimchi"),
    ("Crispy", "Fried", "Onion"),
    ("Tender", "Honey", "Garlic")
]

epic_chickens = [ 
    ("Crispy", "Honey", "Garlic"),
    ("Tender", "Soy", "Kimchi"),
    ("Juicy", "Fried", "Cheese"),
    ("Crispy", "Soy", "Cheese"),
    ("Chewy", "Fried", "Onion")
]

rare_chickens = [ 
    ("Crispy", "Spicy", "Garlic"),
    ("Juicy", "Soy", "Onion"),
    ("Tender", "Honey", "Cheese"),
    ("Chewy", "Soy", "Garlic"),
    ("Juicy", "Spicy", "Cheese"),
    ("Tender", "Soy", "Onion"),
    ("Crispy", "Fried", "Kimchi")
]

# 치킨 개발 상태
chicken_develop_step = 0
selected_texture = ""
selected_style = ""
selected_sub = ""
chicken_class = "Normal"
temp_chickname = ""
temp_class = "Normal"
temp_class_constant = 1.0
class_constant = 1.0

# 직원 전직
member_jobs = ["Crew"]
job_names = ["Hintman", "Skipman", "Saleman"]
hint = ""
light_bulb = False
bulb_x, bulb_y = -1, -1
time_travel = False
time_travel_timer = 0
tf_flash_timer = 0
sale_flash_timer = 0
gps_year = 0

# 위치 설정
fryer_positions = [
    {'x': 12,  'y': 53}, {'x': 44,  'y': 53},
    {'x': 76,  'y': 53}, {'x': 108, 'y': 53},
    {'x': 140, 'y': 53}]

member_positions = [
    {'x': 14,  'y': 73}, {'x': 46,  'y': 73},
    {'x': 78,  'y': 73}, {'x': 110, 'y': 73},
    {'x': 142, 'y': 73}]

# 안내창
guide_message = []


# --------------------
#    시스템 함수들
# --------------------


def print_gold(n):
    if n >= 1_000_000_000_000:
        return f"{n / 1_000_000_000_000:.1f}T"
    elif n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"
    elif n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    else:
        return int(n)


def chicken_upgrade(chicken_level, gold, chicken_price):
    global print_message, print_timer, game_state

    cost =  5_000_000 * (1.15 ** chicken_level)
    if gold < cost:
        print_message = f"You need {print_gold(cost -gold)} more gold."
    elif chicken_level < 100:
        gold -= cost
        chicken_price *= 1.20 #업그레이드 성공 시 치킨 가격 20% 증가
        if randint(1, 100) <= (100 - chicken_level):
            chicken_level += 1
            print_message = f"Success! → Level {chicken_level}"
        else:
            print_message = f"Fail... → Level {chicken_level}"
    else:
        print_message = "Chicken Level MAX!"

    print_timer = 60
    game_state = "waiting_message"
    return chicken_level, gold, chicken_price


def get_member(gold, member):
    global print_message, print_timer, game_state, cnt_fryer, member_jobs

    if member < cnt_fryer:
        i = len(member_jobs) - 1
        cost = employ_cost[i]
        if gold >= cost:
            gold -= cost
            member += 1
            print_message = f"member hired! (Total: {member})"
            member_jobs.append("Crew")
        else:
            print_message = f"You need {print_gold(cost -gold)} more gold."
    else:
        print_message = f"Not enough Fryer."
    print_timer = 60
    game_state = "waiting_message"
    return gold, member


def get_fryer(gold, cnt_fryer):
    global print_message, print_timer, game_state

    i = cnt_fryer - 1
    cost = employ_cost[i] // 2
    if gold >= cost:
        gold -= cost
        cnt_fryer += 1
        print_message = f"Fryer purchased! (Total: {cnt_fryer})"
    else:
        print_message = f"You need {print_gold(cost - gold)} more gold."

    print_timer = 60
    game_state = "waiting_message"
    return gold, cnt_fryer


def upgrade_side(gold, my_side):
    global print_message, print_timer, game_state

    if my_side == "Golden Cheese Ball":
        print_message = "Max UPGRADE!"
        print_timer = 60
    else:
        i = side_list.index(my_side)
        if gold >= side_prices[i + 1]:
            gold -= side_prices[i + 1]
            print_message = f"UPGRADE! {side_list[i]} ---> {side_list[i + 1]}"
            my_side = side_list[i + 1]
            print_timer = 90
        else:
            print_message = f"You need {print_gold(side_prices[i + 1] - gold)} more gold."
            print_timer = 60
    
    game_state = "waiting_message"
    return gold, my_side

    
def buy_store(index):
    global gold, print_message, print_timer, game_state

    cost = store_prices[index]
    if gold >= cost:
        gold -= cost
        if store_counts[index] < 99: # 세자리 수 방지
            store_counts[index] += 1
            store_prices[index] = int(store_prices[index] * 1.15) # 다음 구매 시 15% 비싸짐
            print_message = f"Bought {stores[index]}!"
        else:
            print_message = f"Max Store!"
    else:
        print_message = f"Need {print_gold(cost - gold)} more Gold."
    print_timer = 60
    game_state = "waiting_message"


def promote_member(gold, member):
    global print_message, print_timer, game_state, member_jobs
    global hint, light_bulb
    global current_year, time_travel, time_travel_timer, sale_flash_timer, gps_year

    cost = 100_000_000 * (1.7 ** sum(1 for job in member_jobs if job != "Crew"))
    if gold < cost:
        print_message = f"Need {print_gold(cost - gold)} more Gold."
        print_timer = 60
    else:
        available_jobs = job_names[:] 
        if member_jobs.count("Hintman") >= 1: #힌트맨 최대 한 명
            available_jobs.remove("Hintman")
        for idx in range(member):
            if member_jobs[idx] == "Crew":
                gold -= cost
                new_job = choice(available_jobs)
                member_jobs[idx] = new_job
                print_message = f"Member {idx+1} promoted to {new_job}!"
                print_timer = 90
                if new_job == "Hintman":
                    chosen = choice(legendary_chickens)
                    pairs = [(0, 1), (0, 2), (1, 2)]
                    i, j = choice(pairs)
                    hint = f"{chosen[i]} + {chosen[j]} = !!!"
                    light_bulb = True

                elif new_job == "Skipman":
                    current_year += 1
                    gps_year = gps * 365
                    gold += gps_year
                    time_travel = True
                    time_travel_timer = 90

                elif new_job == "Saleman":
                    for i in range(len(store_prices)):
                        store_prices[i] = store_prices[i] * 0.5
                        sale_flash_timer = 75
                break
        else:
            print_message = "No promotable member!"
            print_timer = 60
    game_state = "waiting_message"
    return gold


# --------------------
#    업데이트 함수
# --------------------


def update():
    global gold, chicken_level, member, cnt_fryer, chicken_price, gpc, gps
    global current_day, current_month, current_year
    global game_state, print_message, print_timer
    global chicken_develop_step, selected_texture, selected_style, selected_sub, selected
    global temp_chickname, temp_class, temp_class_constant, chicken_class, chicken_name, class_constant
    global click_list, my_side, isSpawned, spawn_timer, side_x, side_y, side_click_cooldown, fever_timer, fever_multi
    global hint, light_bulb, bulb_x, bulb_y, time_travel, time_travel_timer, tf_flash_timer, sale_flash_timer, gps_year
    global guide_message

    gpc = chicken_price * fever_multi
    gps = sum([store_counts[i] * store_incomes[i] for i in range(len(stores))]) * 30 * class_constant

    # 클릭 관련 (돈 증가, 사이드 클릭)
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        click_x , click_y = pyxel.mouse_x, pyxel.mouse_y
        if isSpawned and not side_click_cooldown and side_x <= click_x <= side_x+13 and side_y <= click_y <= side_y+13:
            isSpawned = False
            side_click_cooldown = 3 # 버그 방지용
            side_x, side_y = -1, -1 # 클릭 시, 사이드 좌표를 화면 밖으로 초기화
            fever_timer = 299
            spawn_timer = randint(1800, 5400) # 사이드 스폰 1분 ~ 3분
            for i in range(len(side_list)):
                if my_side == side_list[i]:
                    bonus_num = int(gold * bonus_percent[i]/100)
                    gold += bonus_num
                    fever_multi = fever_bonus[i]
                    click_list.append([pyxel.mouse_x, pyxel.mouse_y, 25, bonus_num])

        elif light_bulb and bulb_x <= click_x <= bulb_x+16 and bulb_y <= click_y <= bulb_y+21:
            light_bulb =False

        else: 
            for i in range(member): # 멤버 수 비례해서 클릭 이펙트 추가
                gold += gpc
                click_list.append([pyxel.mouse_x - i, pyxel.mouse_y - i*4, 25, gpc])
    if fever_timer > 0:
        fever_timer -= 1
    else:
        fever_multi = 1
    for elem in click_list[:]:
        elem[2] -= 1
    click_list = [elem for elem in click_list if elem[2] > 0]

    if side_click_cooldown > 0:
        side_click_cooldown -= 1

    if game_state == "waiting_message":
        if print_timer > 0:
            print_timer -= 1
        else:
            print_message = ""
            game_state = "playing"

    # gps 골드 더하기
    gold += gps / 30

    if game_state == "playing":
        if pyxel.btnp(pyxel.KEY_1):
            game_state = "menu_food"

        elif pyxel.btnp(pyxel.KEY_2):
            game_state = "menu_mem"

        elif pyxel.btnp(pyxel.KEY_3):
            game_state = "menu_store"

    elif game_state == "menu_food":
        if pyxel.btnp(pyxel.KEY_1): game_state = "menu_chicken"
        elif pyxel.btnp(pyxel.KEY_2): game_state = "menu_side"
        elif pyxel.btnp(pyxel.KEY_3): game_state = "menu_fryer"

    elif game_state == "menu_chicken":
        if pyxel.btnp(pyxel.KEY_1): 
            game_state = "menu_chicken_status"

        elif pyxel.btnp(pyxel.KEY_2):
            cost = 30_000_000
            if gold >= cost:
                guide_message = [
                    "Develop chicken?",
                    f"Cost: {print_gold(cost)}",
                    "1. Yes",
                    "2. No"
                ]
                game_state = "guide_chicken_develop"
            else:
                print_message = f"You need {print_gold(cost - gold)} more gold."
                print_timer = 60
                game_state = "waiting_message"

        elif pyxel.btnp(pyxel.KEY_3):
            cost = 5_000_000 * (1.15 ** chicken_level)
            guide_message = [
            "Upgrade chicken?",
            f"Cost: {print_gold(cost)}",
            "1. Yes",
            "2. No"
            ]
            game_state = "guide_chicken_upgrade"
    
    elif game_state == "menu_chicken_develop":
        if chicken_develop_step == 1:
            for i in range(len(textures)):
                if pyxel.btnp(pyxel.KEY_1 + i):
                    selected_texture = textures[i]
                    chicken_develop_step = 2
                    break

        elif chicken_develop_step == 2:
            for i in range(len(styles)):
                if pyxel.btnp(pyxel.KEY_1 + i):
                    selected_style = styles[i]
                    chicken_develop_step = 3
                    break

        elif chicken_develop_step == 3:
            for i in range(len(sub_materials)):
                if pyxel.btnp(pyxel.KEY_1 + i):
                    selected_sub   = sub_materials[i]
                    selected       = (selected_texture, selected_style, selected_sub)
                    temp_chickname = " ".join((selected)) + " chicken"

                    if selected in legendary_chickens:
                        temp_class           = "Legendary"
                        temp_class_constant  = uniform(3.50, 5.00)
                    elif selected in epic_chickens:
                        temp_class           = "Epic"
                        temp_class_constant  = uniform(2.40, 3.50)
                    elif selected in rare_chickens:
                        temp_class           = "Rare"
                        temp_class_constant  = uniform(1.50, 2.40)
                    else:
                        temp_class           = "Normal"
                        temp_class_constant  = uniform(1.00, 1.50)

                    chicken_develop_step = 4
                    break

        elif chicken_develop_step == 4:
            if pyxel.btnp(pyxel.KEY_1):  # 장착(EQUIP)
                chicken_class = temp_class
                chicken_name =  temp_chickname
                class_constant = temp_class_constant
                print_message = f"Equipped!"
                print_timer = 60
                game_state = "waiting_message"
                chicken_develop_step = 0
            elif pyxel.btnp(pyxel.KEY_2):  # 버림(Drop)
                print_message = f"Dropped!"
                print_timer = 60
                game_state = "waiting_message"
                chicken_develop_step = 0

    elif game_state == "menu_side":
        if pyxel.btnp(pyxel.KEY_1):
            game_state = "menu_side_status"
        if pyxel.btnp(pyxel.KEY_2):
            if my_side != "Golden Cheese Ball":
                i = side_list.index(my_side)
                cost = side_prices[i + 1]
                guide_message = [
                    "Upgrade Side?",
                    f"Cost: {print_gold(cost)}",
                    "1. Yes",
                    "2. No"
                ]
                game_state = "guide_side_upgrade"
            else:
                print_message = "Max UPGRADE!"
                print_timer = 60
                game_state = "waiting_message"

    elif game_state == "menu_fryer":
            if pyxel.btnp(pyxel.KEY_1):
                if cnt_fryer < 5:
                    i = cnt_fryer - 1
                    cost = employ_cost[i] // 2
                    guide_message = [
                        "Buy Fryer?",
                        f"Cost: {print_gold(cost)}",
                        "1. Yes",
                        "2. No"
                    ]
                    game_state = "guide_fryer_buy"
                else:
                    print_message = "Max Fryer!"
                    print_timer = 60
                    game_state = "waiting_message"

    elif game_state == "menu_mem":
        if pyxel.btnp(pyxel.KEY_1):  # Hire
            i = len(member_jobs) - 1
            if i < 4:
                cost = employ_cost[i]
                guide_message = [
                    "Hire a Member?",
                    f"Cost: {print_gold(cost)}",
                    "1. Yes",
                    "2. No"
                ]
                game_state = "guide_hire"
            else:
                print_message = "Max Member!"
                print_timer = 60
                game_state = "waiting_message"
                

        elif pyxel.btnp(pyxel.KEY_2):  # Promote
            cost = 100_000_000 * (1.7 ** sum(1 for job in member_jobs if job != "Crew"))
            guide_message = [
                "Promote member?",
                f"Cost: {print_gold(cost)}",
                "1. Yes",
                "2. No"
            ]
            game_state = "guide_promote"

    elif game_state == "menu_store":
        for i in range(len(stores)):
            if pyxel.btnp(pyxel.KEY_1 + i):
                buy_store(i)
    
    elif game_state == "guide_hire":
        if pyxel.btnp(pyxel.KEY_1):
            gold, member = get_member(gold, member)
        elif pyxel.btnp(pyxel.KEY_2):
            game_state = "playing"

    elif game_state == "guide_promote":
        if pyxel.btnp(pyxel.KEY_1):
            gold = promote_member(gold, member)
        elif pyxel.btnp(pyxel.KEY_2):
            game_state = "playing"
    
    elif game_state == "guide_chicken_upgrade":
        if pyxel.btnp(pyxel.KEY_1):
            chicken_level, gold, chicken_price = chicken_upgrade(chicken_level, gold, chicken_price)
        elif pyxel.btnp(pyxel.KEY_2):
            game_state = "playing"
    
    elif game_state == "guide_chicken_develop":
        if pyxel.btnp(pyxel.KEY_1):
            game_state = "menu_chicken_develop"
            chicken_develop_step = 1

        elif pyxel.btnp(pyxel.KEY_2):
            game_state = "playing"

    elif game_state == "guide_side_upgrade":
        if pyxel.btnp(pyxel.KEY_1):
            gold, my_side = upgrade_side(gold, my_side)
        elif pyxel.btnp(pyxel.KEY_2):
            game_state = "playing"

    elif game_state == "guide_fryer_buy":
        if pyxel.btnp(pyxel.KEY_1):
            gold, cnt_fryer = get_fryer(gold, cnt_fryer)
        elif pyxel.btnp(pyxel.KEY_2):
            game_state = "playing"

    # 사이드 스폰
    if not isSpawned:
        spawn_timer -= 1
        if spawn_timer <= 0:
            isSpawned = True
            side_x, side_y = randint(15, 170), randint(35, 85)

    # 힌트맨 전구 좌표
    if light_bulb:
        for i in range(len(member_jobs)): 
            if member_jobs[i] == "Hintman":
                pos = member_positions[i]
                bulb_x, bulb_y = pos['x'] + 1, pos['y'] - 23

    # 힌트맨 힌트 출력
    if hint and not light_bulb:
        print_message = hint
        print_timer = 150
        game_state = "waiting_message"
        hint = ""

    # 스킵맨 시간여행
    if time_travel:
        time_travel_timer -= 1
    if time_travel and time_travel_timer <= 0:
        time_travel = False
        tf_flash_timer = 75
    if tf_flash_timer:
        tf_flash_timer -= 1

    # 세일맨 깜빡이 타이머
    if sale_flash_timer:
        sale_flash_timer -= 1

    # 날짜 증가
    if pyxel.frame_count % 30 == 0:
        current_day += 1

    if current_day > day_of_months[current_month]:
        current_day = 1
        current_month += 1
    if current_month > 12:
        current_month = 1
        current_year += 1

    if pyxel.btnp(pyxel.KEY_Q):
        game_state = "playing"
        chicken_develop_step = 0
        print_message = ""
        print_timer = 0
        temp_chickname = ""
        temp_class = "Normal"
        temp_class_constant = 1.0


# --------------------
#     그리기 함수   
# --------------------


# 윤곽선 함수
def print_text(x, y, text, text_color, outline_color):
    pyxel.text(x-1, y, text, outline_color)
    pyxel.text(x+1, y, text, outline_color)
    pyxel.text(x, y-1, text, outline_color)
    pyxel.text(x, y+1, text, outline_color)
    pyxel.text(x, y, text, text_color)


def draw():
    pyxel.cls(0)
    pyxel.bltm(0, 0, 0, 0, 0, 200, 140)
    print_text(5, 5, f"GOLD : {print_gold(gold)}", 10, 0)
    print_text(5, 15, f"GPS  : {print_gold(gps)}/s", 7, 0)
    # 하단 창
    pyxel.rect(0, 99, 200, 41, 4)
    # 하단 창 윤곽
    pyxel.rectb(0,  99, 200, 41, 1)
    pyxel.rectb(1, 100, 198, 39, 1)
    # 하단 창 구분선
    pyxel.line(37,  99, 37,  140, 1)
    pyxel.line(38,  99, 38,  140, 1)
    pyxel.line(149, 99, 149, 140, 1)
    pyxel.line(150, 99, 150, 140, 1)
    # 하단 창 카테고리
    print_text(4, 103, "FOOD", 7, 0)
    print_text(43, 103, "STORE", 7, 0)

    # fryers 렌더링
    for i in range(cnt_fryer):
        pos = fryer_positions[i]
        pyxel.blt(pos['x'], pos['y'], 1, 23, 86, 25, 36, 7)
    
    # 멤버 렌더링
    for i in range(member): 
        pos = member_positions[i]
        if   member_jobs[i] == "Crew":
            pyxel.blt(pos['x'], pos['y'], 1, 0,  64, 16, 20, 7)
        elif member_jobs[i] == "Hintman":
            pyxel.blt(pos['x'], pos['y'], 1, 16, 64, 16, 20, 7)
        elif member_jobs[i] == "Skipman":
            pyxel.blt(pos['x'], pos['y'], 1, 32, 64, 16, 20, 7)
        elif member_jobs[i] == "Saleman":
            pyxel.blt(pos['x'], pos['y'], 1, 48, 64, 16, 20, 7)

    #치킨 슬롯
    pyxel.rectb(3, 113, 15, 15, 0)
    if   chicken_class == "Normal":
        pyxel.blt(4, 114, 1, 32, 26, 13, 13)
    elif chicken_class == "Rare":
        pyxel.blt(4, 114, 1, 45, 26, 13, 13)
    elif chicken_class == "Epic":
        pyxel.blt(4, 114, 1, 58, 26, 13, 13)
    elif chicken_class == "Legendary":
        pyxel.blt(4, 114, 1, 71, 26, 13, 13)

    #사이드 슬롯
    pyxel.rectb(20, 113, 15, 15, 0)
    if   my_side == side_list[0]:
        pyxel.blt(21, 114, 1, 32, 40, 13, 13)
    elif my_side == side_list[1]:
        pyxel.blt(21, 114, 1, 45, 40, 13, 13)
    elif my_side == side_list[2]:
        pyxel.blt(21, 114, 1, 59, 40, 13, 13)

    #지점 슬롯
    pyxel.blt(42,  112, 1, 32, 0, 20, 16, 7)
    pyxel.blt(70,  110, 1, 52, 0, 18, 18, 6)
    pyxel.blt(101, 112, 1, 70, 0, 16, 16, 7)
    pyxel.blt(128, 111, 1, 86, 0, 18, 17, 6)
    
    #지점 개수
    store_x = [49, 80, 107, 136]
    for i in range(len(stores)):
        if store_counts[i] >= 10: # 두 자리 수 위치 조정
            store_x[i] -= 2
        print_text(store_x[i], 131, f"{store_counts[i]}", 7, 0)
        
    if game_state == "playing": 
        print_text(155, 106, "1. Food", 7, 0)
        print_text(155, 117, "2. Member", 7, 0)
        print_text(155, 128, "3. Store", 7, 0)

    elif game_state == "menu_food":
        print_text(155, 106, "1. Chicken", 7, 0)
        print_text(155, 117, "2. Side", 7, 0)
        print_text(155, 128, "3. Fryer", 7, 0)

    elif game_state == "menu_chicken":
        print_text(155, 106, "1. Status", 7, 0)
        print_text(155, 117, "2. Develop", 7, 0)
        print_text(155, 128, "3. UPGRADE", 7, 0)

    elif game_state == "menu_side":
        print_text(155, 106, "1. Status", 7, 0)
        print_text(155, 117, "2. UPGRADE", 7, 0)

    elif game_state == "menu_fryer":
        print_text(155, 106, "1. Buy", 7, 0)

    elif game_state == "menu_mem":
        print_text(155, 106, "1. Hire", 7, 0)
        print_text(155, 117, "2. Promote", 7, 0)
    
    elif game_state == "menu_store":
        pyxel.rect(53, 33, 98, 55, 4)
        pyxel.rectb(53, 33, 98, 55, 1)
        pyxel.rectb(54, 34, 98, 55, 1)
        print_text(58, 38, "Press (1-4) to buy!", 7, 0)
        for i in range(len(stores)):
            print_text(58, 48 + i * 10, f"{i+1}. {stores[i]} ({print_gold(store_prices[i])})", 7, 0)

    #날짜 카운트
    print_text(152, 4, f"{current_year}-{current_month:02}-{current_day:02}", 7, 0)

    # 힌트맨 전구
    if light_bulb:
        for i in range(len(member_jobs)): 
            if member_jobs[i] == "Hintman":
                pos = member_positions[i]
                pyxel.blt(pos['x'] + 1, pos['y'] - 23, 1, 8, 36, 16, 21, 6)
                
    #사이드 스폰 
    if isSpawned:
        if   my_side == side_list[0]:
            pyxel.blt(side_x, side_y, 1, 32, 40, 13, 13, 15)
        elif my_side == side_list[1]:
            pyxel.blt(side_x, side_y, 1, 45, 40, 14, 14, 10)
        elif my_side == side_list[2]:
            pyxel.blt(side_x, side_y, 1, 59, 40, 14, 14, 3)

    if game_state == "menu_chicken_status":
        pyxel.rect( 40, 35, 127, 35, 4)
        pyxel.rectb(40, 35, 127, 35, 1)
        pyxel.rectb(41, 36, 127, 35, 1)
        print_text(45, 40, f"{chicken_name}", 7, 0)
        print_text(45, 50, f"Class : {chicken_class} (GPS x{class_constant:.2f})", 7, 0)
        print_text(45, 60, f"Level : {chicken_level} ({print_gold(chicken_price)})", 7, 0)
    
    if game_state == "menu_side_status":
        pyxel.rect( 40, 35, 99, 35, 4)
        pyxel.rectb(40, 35, 99, 35, 1)
        pyxel.rectb(41, 36, 99, 35, 1)
        print_text(45, 40, f"Golden Cheese Ball", 7, 0)
        for i in range(len(side_list)):
            if my_side == side_list[i]:
                print_text(45, 50, f"Bonus : GOLD x {bonus_percent[i]}%", 7, 0)
                print_text(45, 60, f"Fever : CLICK x {fever_bonus[i]}", 7, 0)
    
    if chicken_develop_step == 1:
        pyxel.blt(48, 22, 0, 8, 8, 96, 63, 7)
    elif chicken_develop_step == 2:
        pyxel.blt(48, 22, 0, 8, 96, 96, 63, 7)
    elif chicken_develop_step == 3:
        pyxel.blt(48, 22, 0, 120, 8, 96, 63, 7)
    elif chicken_develop_step == 4:
        pyxel.rect( 40, 35, 127, 45, 4)
        pyxel.rectb(40, 35, 127, 45, 1)
        pyxel.rectb(41, 36, 127, 45, 1)
        print_text(45, 40, f"{temp_chickname}", 7, 0)
        print_text(45, 50, f"Class : {temp_class} (GPS x{temp_class_constant:.2f})", 7, 0)
        print_text(45, 60, "1. Equip", 7, 0)
        print_text(45, 70, "2. Drop", 7, 0)
    
    date_color = 7
    if tf_flash_timer and tf_flash_timer % 10 < 5:
        date_color = 10
    print_text(152, 4, f"{current_year}-{current_month:02}-{current_day:02}", date_color, 0)

    store_color = 7
    if sale_flash_timer and sale_flash_timer % 10 < 5:
        store_color = 10
    print_text(43, 103, "STORE", store_color, 0)

    if tf_flash_timer:
        print_text(114, 4, f"+{print_gold(gps_year)}", 10, 0)
    
    if sale_flash_timer:
        print_text(65, 103, "50%", 10, 0)

    if time_travel:
        pyxel.cls(0)
        print_text(67, 40, "One Year Later. . .", 7, 0)

    if fever_timer > 0:
        fever_seconds = fever_timer // 30
        print_text(144, 13, f"({fever_seconds})fever! x{fever_multi}", 8, 0)

    if print_message:
        w = len(print_message) * 4
        x = (200 - w) // 2
        y = (140 // 2) - 4
        print_text(x, y, print_message, 7, 0)
    
    #클릭 골드 획득
    for click_x, click_y, click_timer, get_gold in click_list:
        print_text(click_x, click_y - (15 - click_timer * 3/5), f"+{print_gold(get_gold)}", 10, 0)

    # 안내창
    if game_state in [
        "guide_chicken_upgrade", "guide_fryer_buy", "guide_hire",
        "guide_chicken_develop","guide_side_upgrade", "guide_promote"]:
        pyxel.rect( 53, 33, 84, len(guide_message)*10 + 5, 4)
        pyxel.rectb(53, 33, 84, len(guide_message)*10 + 5, 1)
        pyxel.rectb(54, 34, 84, len(guide_message)*10 + 5, 1)
        for i in range(len(guide_message)):
            print_text(58, 38 + i * 10, guide_message[i], 7, 0)
            

# --------------------
#      게임 실행
# --------------------


pyxel.init(200, 140)
pyxel.colors[2]  = 0x9B111E # 빨강 그라데이션
pyxel.colors[4]  = 0x532A28 # 갈색
pyxel.colors[5]  = 0x3470A9 # 남색
pyxel.colors[6]  = 0xA6DFF8 # 백경 블루
pyxel.colors[8]  = 0xDB0008 # 빨강
pyxel.colors[12] = 0x5B5B5B # 회색 그라데이션
pyxel.colors[13] = 0x8F8F8F # 회색
pyxel.load("assets.pyxres")
pyxel.mouse(True)
pyxel.run(update, draw)