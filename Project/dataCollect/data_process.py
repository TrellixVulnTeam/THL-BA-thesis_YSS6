from config import config
from spider import spider
import pandas as pd
import json, pickle, traceback, os

def saveData(file_name, data):
    with open(file_name, 'wb') as fw:
        pickle.dump(data, fw)
        
def loadData(file_name):
    with open(file_name, 'rb') as fw:
        return pickle.load(fw)

class heroes(object):
    def __init__(self):
        self.heroesMetaData = 'metadata/dictheroes.data'
        self.dictHeroes = self.getHeroes()
    
    def getHeroes(self):
        return loadData(self.heroesMetaData)

    def getHeroNameById(self, id):
        return self.dictHeroes[id]['localized_name']

def changeMatchId(url, match_id):
    return url.replace("{match_id}", match_id)
    
def getMatchesDetail(request, url):
    return request.GET(url)

def main():
    Config = config('conf/config.ini')
    MatchesDetailBaseUrl = Config.getMatchesUrl()
    
    Requst = spider()
    #get parsed matches id
    MatchesIds = readMatchIdFromFile('data/match_ids.data')
    AlreadyDoneIdFile = 'tmp/AlreadyDoneId.data'
    AlreadyDoneId = []
    try:
        AlreadyDoneId = readAlreadyDoneIds(AlreadyDoneIdFile)
    except:
        traceback.print_exc()
    
    ids = list(set(MatchesIds) - set(AlreadyDoneId))
    #get matches detail by matches id
    count = 0
    for item in ids:
        retry = 0
        while retry < 3:
            try:
                MatchID = item
                StoreFileName = 'data/matchesdata/{}.data'.format(MatchID)
                if os.path.exists(StoreFileName):
                    print('file {} exists.'.format(StoreFileName))
                    AlreadyDoneId.append(MatchID)
                    break
                print('start match_id={}'.format(MatchID))
                MatchesDetailUrl = changeMatchId(MatchesDetailBaseUrl, str(MatchID))
                print(MatchesDetailUrl)
                JsonMatchesDetail = getMatchesDetail(Requst, MatchesDetailUrl)            
                saveData(StoreFileName, JsonMatchesDetail)
                AlreadyDoneId.append(MatchID)
                if count %100 == 0:
                    saveData(AlreadyDoneIdFile, AlreadyDoneId)
                break
            except:
                traceback.print_exc()
                print('exception in {}, retry {} times'.format(MatchID,retry))
                retry+=1
        count += 1
       

def get_mathes_data(f='data/matchesdata/5416234729.data'):
    #return loadData(f)
    j = loadData(f)
    #print('load %s'%f)
    '''
    print(j)
    print('--'*100)
    print(j.keys())
    print(j['radiant_win'])
    print(j['radiant_team_id'])
    print(j['dire_team_id'])
    print('--'*200)
    '''
    banpick = j['picks_bans']
    win = 0 if j['radiant_win'] == True else 1

    #print(banpick)
    bp = ['p0', 'p1', 'b0', 'b1']
    bp_dict={i:[] for i in bp}
    
    
    for i in banpick:
        is_pick = i['is_pick']
        team = i['team']
        if is_pick == True:
            if team == 0:
                bp_dict['p0'].append(i)
            else:
                bp_dict['p1'].append(i)
        else:
            if team == 0 and len(bp_dict['b0']) < 5 :
                bp_dict['b0'].append(i)
            if team == 1 and len(bp_dict['b1']) < 5 :
                bp_dict['b1'].append(i)
    data = []
    for i in bp:
        for j in bp_dict[i]:
            data.append(j['hero_id'])
    data.append(win)
    #print(data)
    return data

def main_sub():
    df = pd.DataFrame()
    count = 1
    for f in get_data_files('data/matchesdata'):
        #print('***'*30, 'filename', '***'*30)
        #print(f)
        try:
            d = get_mathes_data(f)
        except:
            continue
        #print('***'*30, 'data', '***'*30)
        #print(d)
        df = df.append([d], ignore_index=True)
        count += 1
        '''
        if count > 300:
            break
        '''
        if count % 100 == 0:
            print('count = %d'%count)

        #print('***'*30, 'dataframe', '***'*30)
    print(count)
    print(df)
    df.to_csv('data/out.csv', index=False, header=False)

def get_data_files(path):
  for root, files in os.walk(path):
        for f in files:
            yield os.path.join(root, f)


def testheroes():
    HeroesData = heroes()
    for i in range(1,10):
        print(HeroesData.getHeroNameById(i))

def get_all_match_ids(response):
    ids = []
    #for item in response['result']['matches']:
    for item in response:
        ids.append(item['match_id'])
    return ids
    
def get_next_id(ids):
    a = sorted(ids)
    if len(a) > 0:
        return a[0]
    else:
        return None

def get_match_ids():
    Requst = spider()
    res_match_ids = []
    next_id = '5584623680'
    last_id = next_id
    while True:
        url, params = gen_match_id_by_opendota(next_id)
        try:
            JsonMatches = Requst.GET(url, params)
            #print(JsonMatches)
            ids = get_all_match_ids(JsonMatches)
            add = 0
            for i in ids:
                if i not in res_match_ids:
                    res_match_ids.append(i)
                    add += 1
            print('get ids size = {}, add {} to res match ids, now size={}, now id ={}'.format(len(ids), add, len(res_match_ids), next_id))
            next_id = get_next_id(ids)
            if next_id is None:
                next_id = int(last_id) - 100
            last_id = next_id 
            
            if len(res_match_ids) > 50000:
                saveData('data/match_ids.data', res_match_ids)
        except:
            print('error')
    
    

def gen_match_id_by_auth(match_id, min_players=10):
    url='http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1'
    params = { 
        'key': 'ABF40420F06972AFCA4BCC7A68577BA0',
        'start_at_match_id': match_id,
        'min_players': min_players
    }
    print(url)
    return url, params
    

def gen_match_id_by_opendota(match_id, min_players=10):
    url='https://api.opendota.com/api/proMatches'
    params = { 
        #'key': 'ABF40420F06972AFCA4BCC7A68577BA0',
        'less_than_match_id': match_id,
        #'min_players': min_players
    }
    print(url)
    return url, params
    
def readMatchIdFromFile(file_name):
    return loadData(file_name)
    
def readAlreadyDoneIds(file_name):
    return loadData(file_name)
    
def saveAlreadyDoneIds(file_name, ids):
    return saveData(file_name, ids)
    
if __name__ == '__main__':
    #test()
    #test2()
    main()
    #testheroes()
    #get_match_ids()
    #print(readMatchIdFromFile('tmp/AlreadyDoneId.data'))
        
        
