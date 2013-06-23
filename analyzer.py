import odesk
import config
from PIL import Image
import io


# Detect blackness of the picture to determine
# if we have a black screenshot
# 0 to 1, black pictures are those with > 0.9
def blackness(image_file):
    image = Image.open(image_file)
    image = image.convert('L')
    size = image.size[0] * image.size[1]
    hist = image.histogram()
    dark = sum(hist[i] for i in range(10))
    return dark / float(size)

PUBLIC_KEY = config.public_key or raw_input('Enter public key: ')
SECRET_KEY = config.secret_key or raw_input('Enter secret key: ')
USERNAME = config.username or raw_input('Enter your oDesk login: ')
PASSWORD = config.password or raw_input('Enter your oDesk password: ')
auth_token = config.auth_token or None

# Add login error handling
sessionClient = odesk.SessionClient(USERNAME, PASSWORD)
sessionClient.login()

if auth_token is None:
    client = odesk.Client(PUBLIC_KEY, SECRET_KEY)
    auth_url = client.auth.auth_url()
    print auth_url
    # TODO: Auto follow the auth link and get the frob
    #frob_detected = sessionClient.urlopen(auth_url).geturl()
    #frob_detected = frob_detected.split('?frob=')[1]
    #print frob_detected
    frob = raw_input("Input frob: ")
    auth_token, user = client.auth.get_token(frob)


client = odesk.Client(PUBLIC_KEY, SECRET_KEY, auth_token)
# TODO: Should be parametrized
start_date = 20130617
end_date = 20130624

wrong_screenshots = {}

for tDate in range(start_date, end_date):
    workdiary = client.team.get_workdiaries(config.team_name,
                                            config.user_id,
                                            date=str(tDate))
    for snapshot in workdiary[1]:
        if int(snapshot[u'activity']) <= 1:
            pass
            # low activity detection
            # Disabled until API bug is fixed
            #wrong_screenshots[snapshot[u'screenshot_img_lrg']] =\
                #int(snapshot[u'time']) - int(snapshot[u'cell_time'])
        else:
            # black screenshots detection
            responce = sessionClient.urlopen(snapshot[u'screenshot_img_lrg'])
            image = io.BytesIO(responce.read())
            blackness_level = blackness(image)
            if blackness_level > 0.9:
                wrong_screenshots[snapshot[u'screenshot_img_lrg']] =\
                    int(snapshot[u'time']) - int(snapshot[u'cell_time'])

# Recap
print "Total time taken by wrong screenshots: %f " %\
    (float(sum(wrong_screenshots.values())) / 3600)
print "Total number of wrong screenshots: %d" % (len(wrong_screenshots.keys()))
sessionClient.logout()
