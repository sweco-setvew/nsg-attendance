import requests
import json

from logging.config import dictConfig

from datetime import datetime, timedelta, date

token=None
expiry=None

def Q(page,expansion):
    if(expansion=='tbc'):
        return f'''{{
              guildData{{
                guild(id:483439){{
                  kara: attendance(limit:25,zoneID:1007,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }},
                  gruul_mag: attendance(limit:25,zoneID:1008,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }}
                  ssc_tk: attendance(limit:25,zoneID:1010,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }},
                  mh_bt: attendance(limit:25,zoneID:1011,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }},
                  swp: attendance(limit:25,zoneID:1013,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }}
                }}
              }}
            }}
        '''    
    else: # DEFAULT WRATH
        return f'''{{
              guildData{{
                guild(id:483439){{
                  T9: attendance(limit:25,zoneID:1018,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }},
                  T8: attendance(limit:25,zoneID:1019,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }},
                  T8: attendance(limit:25,zoneID:1017,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }},
                  VoA: attendance(limit:25,zoneID:1016,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }},
                  T7: attendance(limit:25,zoneID:1015,page:{page}){{
                    data{{
                      code,
                      players{{
                        name
                      }}
                      startTime,
                      zone{{
                       name ,id
                      }}
                    }}
                  }}         
                }}
              }}
            }}
        '''    

exp = 'wrath'
page = 1

if not token or datetime.now()>expiry: 
        f=open("secrets.json",'r')
        secrets=json.loads(f.read())   
        client_id = secrets.get('client_id')
        client_secret = secrets.get('client_secret')
        token_url = "https://classic.warcraftlogs.com/oauth/token"
        payload = dict(grant_type='client_credentials')
        r = requests.post(token_url, data=payload, auth=(client_id, client_secret))
        response=r.json()
        token=response['access_token']
        expiry=datetime.now()+timedelta(seconds=response['expires_in'])

client_url='https://classic.warcraftlogs.com/api/v2/client'
header={'Authorization':f'Bearer {token}'}

base=[]    
for run in range(4):
    print(run)
    payload={"query":Q(run+1,exp)}
    r2=requests.post(client_url, data=payload, headers=header)
    blob=r2.json()
    data=blob.get('data')
    if data:
        guildData=data.get('guildData')
        #print("a",run)
        if guildData:
            guild=guildData.get('guild')
            #print("b",run)
            if guild:
                base.append(guild)
                #print("done",run)
    else:
        print(data)

output=[]

for run in base:
    for zone in run:
        raids=run.get(zone).get("data")
        for raid in raids:
            raid_date=date.fromtimestamp(raid.get('startTime')/1000)
            iso=(raid_date-timedelta(days=2)).isocalendar()
            for raider in raid.get('players'):
                output.append(','.join([zone,str(iso[0])+';'+str(iso[1]),raider.get('name'),str(raid_date)]))
result='|'.join(output)

print(result[:50000])
