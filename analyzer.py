import odesk
import config

PUBLIC_KEY = config.public_key or raw_input('Enter public key: ')
SECRET_KEY = config.secret_key or raw_input('Enter secret key: ')
auth_token = config.auth_token or None

if auth_token is None:
    client = odesk.Client(PUBLIC_KEY, SECRET_KEY)
    auth_url = client.auth.auth_url()
    print auth_url
    frob = raw_input("Input frob: ")
    auth_token, user = client.auth.get_token(frob)


client = odesk.Client(PUBLIC_KEY, SECRET_KEY, auth_token)

start_date = 20130617
end_date = 20130618

total_screenshots = 0
idle_time_seconds = 0

for tDate in range(start_date, end_date):
    print tDate
    workdiary = client.team.get_workdiaries(config.team_name,
                                            config.user_id,
                                            date=str(tDate))
    print workdiary[1]
    #for snapshot in workdiary[1]:
        #print "<a href='%s'>%s</a> "%(snapshot[u'screenshot_url'], snapshot[u'activity'])

        #if int(snapshot[u'activity']) <= 1:
            #print snapshot[u'screenshot_url']
            #total_screenshots += 1
            #idle_time_cell = int(snapshot[u'time']) - int(snapshot[u'cell_time'])
            #idle_time_seconds += idle_time_cell


print "Total idle screenshots: %d" % total_screenshots
print "Idle time (seconds): %d" % idle_time_seconds
