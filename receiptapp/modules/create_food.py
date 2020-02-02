from ..models import Receipt, Image, Food, Fooddetail

def seibun_to_float(s):
    try:
        float(s)
    except:
        return 0
    return float(s)

def list_to_float(list):
    for i, v in enumerate(list):
        list[i] = seibun_to_float(v)

def search_seibun(seibunlist, namelist):
    newlist = []
    for seibun in enumerate(seibunlist):
        for name in namelist:
            if seibun == name:
                num = i+1
                newlist.append[seibunlist[num]]
    return newlist

def create_food(request, receipt):
    # 各成分の配列を作る処理はcreate_food_array関数に記述
    food_array = create_food_array(post=request.POST)
    name = food_array[0]
    energy = food_array[1]
    protein = food_array[2]
    fat = food_array[3]
    carb = food_array[4]
    salt = food_array[5]
    count = food_array[6]

    amount_arr = []
    for v in count:
        amount = int(request.POST[v]) * 100
        amount_arr.append(amount)

    # food 保存の処理
    for i, v in enumerate(name):
        # info_list = list(info)
        print(i)
        print(name)
        foodbool = Food.objects.filter(food_name=v).exists()
        # food がすでにあるならそれを参照する、ないなら新規作成
        if foodbool:
            food = Food.objects.get(food_name=v)
        else:
            food = Food(food_name=v, protein=protein[i], fat=fat[i], carb=carb[i], salt=salt[i], energy=energy[i])
            food.save()
        #receipt.foods.add(food)
        # foodsはなくしてdetailから参照するように保存する
        fooddetail = Fooddetail(amount=amount_arr[i], receipt=receipt, food=food)
        fooddetail.save()
    #receipt.save()

def create_food_array(post):
    foods = post.getlist("food")

    name = []
    energy = []
    protein = []
    fat = []
    carb = []
    salt = []
    count = []

    for food in foods:
        food_str_arr = food.split(",")
        name.append(food_str_arr[0])
        energy.append(food_str_arr[1])
        protein.append(food_str_arr[2])
        fat.append(food_str_arr[3])
        carb.append(food_str_arr[4])
        salt.append(food_str_arr[5])
        count.append(food_str_arr[6])
    """
    name_list = post.getlist("name")
    energy_list= post.getlist("energy")
    protein_list = post.getlist("protein")
    fat_list = post.getlist("fat")
    carb_list = post.getlist("carb")
    salt_list = post.getlist("salt")

    print(len(name_list))
    sumlen = 0
    for i, v in enumerate(count):
        parentCount = v.split(",")[0]
        num = v.split(",")[1]
        # sumlen に 子ループのカウントを足す
        sumlen += int(num)
        # からの配列にcheckboxの数だけデータを追加する
        name.append(name_list[sumlen - 1])
        energy.append(energy_list[sumlen - 1])
        protein.append(protein_list[sumlen - 1])
        fat.append(fat_list[sumlen - 1])
        carb.append(carb_list[sumlen - 1])
        salt.append(salt_list[sumlen - 1])
        # sumlen を基準値(lenの合計)までもどす
        sumlen -= int(num)
        # indexerrorを避けるためのif
        if not (i+1) >= len(count):
            nparentCount = count[i + 1].split(",")[0]
            # 次も同じparentloop の countであればsumを次に代入せずにつぎに行く
            if parentCount == nparentCount:
                continue
            sumlen += int(post.get(str(i + 1)))
    """
    # energy = [float(v) for v in energy]
    list_to_float(energy)
    list_to_float(protein)
    list_to_float(fat)
    list_to_float(carb)
    list_to_float(salt)

    food_array = []
    food_array.append(name)
    food_array.append(energy)
    food_array.append(protein)
    food_array.append(fat)
    food_array.append(carb)
    food_array.append(salt)
    food_array.append(count)
    return food_array

def create_food_api(name, energy, protein, fat, carb, salt, amount, receipt):
    print(name)
    print(amount)

    # 数値化しないといけない？
    amount_arr = []
    for i, v in enumerate(amount):
        amount_arr.append(int(v.replace("g", "")))

    # food 保存の処理
    for i, v in enumerate(name):
        # info_list = list(info)
        print(i)
        print(name)
        foodbool = Food.objects.filter(food_name=v).exists()
        # food がすでにあるならそれを参照する、ないなら新規作成
        if foodbool:
            food = Food.objects.get(food_name=v)
        else:
            food = Food(food_name=v, protein=protein[i], fat=fat[i], carb=carb[i], salt=salt[i], energy=energy[i])
            food.save()
        #receipt.foods.add(food)
        # foodsはなくしてdetailから参照するように保存する
        fooddetail = Fooddetail(amount=amount_arr[i], receipt=receipt, food=food)
        fooddetail.save()
    #receipt.save()
