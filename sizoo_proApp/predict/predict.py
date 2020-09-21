from ..models import LineUp, ShoesData, ShoesExp, UserInfo, ServiceResult

def predict(user, tgt):

    #get tgt lineup
    tgt_data = ShoesData.objects.get(id=tgt)
    tgt_lineup = tgt_data.Model_lineUp.pk
    tgt_brand = LineUp.objects.get(id=tgt_lineup).LineUp_Brand

    #get user shoe exp 
    user_shoe_query = ShoesExp.objects.filter(ShoesExp_User = user).select_related('LineUp').values('ShoesExp_Size','LineUp_Model_Code','LineUp__pk')
    user_shoe_sizes = {}
    
    user_shoe_pk_list = []


    for i in user_shoe_query:
        if i['LineUp_Model_Code'] not in user_shoe_sizes:
            user_shoe_sizes[i['LineUp_Model_Code']] = [i['ShoesExp_Size']]
        else :
            user_shoe_sizes[i['LineUp_Model_Code']].append(i['ShoesExp_Size'])
        if i['LineUp__pk'] in user_shoe_pk_list:
            user_shoe_pk_list.append(i['LineUp__pk'])

    user_shoe_list = list(user_shoe_sizes.keys())

    for i in user_shoe_list:
        if len(user_shoe_sizes[i]) == 1:
            user_shoe_sizes[i] = user_shoe_sizes[i][0]
        else :
            user_shoe_sizes[i] = int(sum(user_shoe_sizes[i])/len(user_shoe_sizes[i]))
    
    #Sol 1
    # tgt_lineup_models = tgt_data.Line_Up_models.all().values('id')
    # tgt_lineup_models = [i['id'] for i in tgt_lineup_models]

    ref_users = ShoesExp.objects.select_related('ShoeExp_Shoe').filter(Model_lineUp = tgt_data.id).values_list('ShoesExp_User',flat=True)
    ref_vusers = ShoesExp.objects.select_related('ShoeExp_Shoe').filter(Model_lineUp = tgt_data.id).values_list('ShoesExp_vuser',flat=True)
    
    ref_users_pks =[]
    ref_users_sizes = []
    ref_count = []

    for i in ref_users:
        if i is None or i in ref_users_pks:
            continue
        q = ShoesExp.objects.filter(ShoesExp_User=i).select_related('ShoesExp_Shoe').filter(Model_lineUp=user_shoe_pk_list)
        if len(q) > 0:
            t={}
            for j in q:
                t[j.LineUp_Model_Code] = j.ShoesExp_Size
            ref_users_pks.append(i)
            ref_users_sizes.append(t)
            ref_count.append(len(t.keys()))

    ref_vusers_pks =[]
    ref_vusers_sizes = []
    ref_vcount = []
    
    for i in ref_vusers:
        if i is None or i in ref_vusers_pks:
            continue
        q = ShoesExp.objects.filter(ShoesExp_vuser=i).select_related('ShoesExp_Shoe').filter(Model_lineUp=user_shoe_pk_list)
        if len(q) > 0:
            t={}
            for j in q:
                t[j.LineUp_Model_Code] = j.ShoesExp_Size
            ref_vusers_pks.append(i)
            ref_vusers_sizes.append(t)
            ref_vcount.append(len(t.keys()))

    adjvallist = []
    for i in ref_users_sizes:
        keys = list(i.keys())
        t = 0
        for j in keys:
            t = user_shoe_sizes[j]-i[j]
        t /= len(keys)

        adjvallist.append(t)

    adjvallist_v = []

    for i in ref_vusers_sizes:
        keys = list(i.keys())
        t = 0
        for j in keys:
            t = user_shoe_sizes[j]-i[j]
        t /= len(keys)

        adjvallist_v.append(t)

    # mxcnt = max(ref_count)
    # ref_sizes=[]
    # if mxcnt > 0:
    #     ref_sizes = [i for i,val in enumerate(l) if val==mxcnt]

    # result = 0

    # if len(ref_sizes) > 0:
    #     for i in ref_sizes:
    #         q = ShoesExp.objects.filter(ShoesExp_User = ref_users_pks[i]).select_related('ShoesExp_shoe').filter(Model_lineUp=tgt_lineup)
    #         t=0
    #         for j in q:
    #             t+=j.ShoesExp_Size
    #         t/=len(q)
    #         result += t + adjvallist[i]
    #     result/=len(ref_sizes)
    #     adj = result %5
    #     result = (result//5)*5
    #     if adj >= 3:
    #         result+=5
    # else :
    #     #미구현
    #     pass

    mxcnt = max(ref_count)
    ref_vsizes=[]
    if mxcnt > 0:
        ref_vsizes = [i for i,val in enumerate(l) if val==mxcnt]

    if len(ref_vsizes) > 0:
        for i in ref_sizes:
            q = ShoesExp.objects.filter(ShoesExp_User = ref_users_pks[i]).select_related('ShoesExp_shoe').filter(Model_lineUp=tgt_lineup)
            t=0
            for j in q:
                t+=j.ShoesExp_Size
            t/=len(q)
            result += t + adjvallist[i]
        result/=len(ref_sizes)
        adj = result %5
        result = (result//5)*5
        if adj >= 3:
            result+=5
    else :
        #미구현
        pass

    return result