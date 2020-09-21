from ..models import LineUp, ShoesData, ShoesExp, UserInfo, ServiceResult

def predict(user, tgt):

    #get tgt lineup
    tgt_data = ShoesData.objects.get(Model_code=tgt)
    tgt_lineup = tgt_data.Model_lineUp
    tgt_brand = tgt_lineup.LineUp_Brand

    #get user shoe exp 
    user_shoe_query = ShoesExp.objects.get(ShoesExp_User_id = user).values('ShoesExp_Shoe__Model_lineUp__LineUp_Model_Code','ShoesExp_Size')
    user_shoe_sizes = {}
    
    #user shoes size dict fill list
    for i in user_shoe_query:
        if i[0] not in user_shoe_sizes:
            user_shoe_sizes[i[0]] = [i[1]]
        else :
            user_shoe_sizes[i[0]].append(i[1])
    
    #user shoes list
    user_shoe_list = list(user_shoe_sizes.keys())
    #mean list
    for i in user_shoe_list:
        if len(user_shoe_sizes[i]) == 1:
            user_shoe_sizes[i] = user_shoe_sizes[i][0]
        else :
            user_shoe_sizes[i] = int(sum(user_shoe_sizes[i])/len(user_shoe_sizes[i]))
    
    #Sol 1

    #get users and vusers who have model_lineUp
    ref_users = ShoesExp.objects.filter(ShoesExp__Model_lineUp = tgt_lineup).values_list('ShoesExp_User_id',flat=True)
    ref_users = list(set(ref_users))
    ref_vusers = ShoesExp.objects.filter(ShoesExp__Model_lineUp = tgt_lineup).values_list('ShoesExp_vuser',flat=True)
    ref_vusers = list(set(ref_vusers))

    ref_users_sizes = []
    ref_count = []
    
    for i in ref_users:
        q = ShoesExp.objects.filter(ShoesExp_User_id=i).filter(ShoesExp_Shoe__Model_lineUp__LineUp_Model_Code__in = user_shoe_list)
        t = {}
        for j in q :
            t[j.LineUp_Model_Code] = j.ShoesExp_Size
        ref_users_sizes.append(t)
        ref_count.append(len(t.keys()))

    for i in ref_vusers:
        q = ShoesExp.objects.filter(ShoesExp_vuser=i).filter(ShoesExp_Shoe__Model_lineUp__LineUp_Model_Code__in = user_shoe_list)
        t = {}
        for j in q :
            t[j.LineUp_Model_Code] = j.ShoesExp_Size
        ref_users_sizes.append(t)
        ref_count.append(len(t.keys()))

    #cal adjval from user size
    adjvallist = []
    for i in ref_users_sizes:
        ks = list(i.keys())
        t = 0
        for j in keys:
            t += user_shoe_sizes[j] - i[j]
        t /= len(keys)

        adjvallist.append(t)

    #find most likely user
    mxcnt = max(ref_count)
    ref_mx_users=[]
    if mxcnt > 0:
        ref_mx_users = [i for i,val in enumerate(ref_users_sizes) if val==mxcnt]

    result = 0

    #find the same vector in db
    if len(ref_mx_users) > 0:
        for i in ref_mx_users:
            q = None
            if i < len(ref_users) :
                q = ShoesExp.objects.filter(ShoesExp_User_id=ref_users[i])
            else :
                q = ShoesExp.objects.filter(ShoesExp_vuser=ref_users[i-len(ref_users)])
            q= q.filter(ShoesExp_Shoe__Model_lineUp=tgt_lineup)
            
            t=0
            for j in q:
                t+=j.ShoesExp_Size

            t/=len(q)
            result += t + adjvallist[i]
        
        result/=len(ref_sizes)
        adj = result % 5
        result = (result//5)*5
        if adj >= 3:
            result+=5
    else :
        return -1

    return result