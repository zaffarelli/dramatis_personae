from collector.models.campaign import Campaign
from PIL import Image
#  exec(open('scripts/update_schemes.py').read())
all = Campaign.objects.all()

def rgb2hex(a):
    return '#{:02x}{:02x}{:02x}'.format(a[0], a[1], a[2])

for campaign in all:
    im = Image.open(f'./collector/static/collector/campaigns/{campaign.rpgsystem}/scheme.png')
    pix = im.load()
    print(f'{campaign.title} --> {campaign.rpgsystem} Ok')
    campaign.color_front = rgb2hex(pix[10, 50])
    campaign.color_back = rgb2hex(pix[330, 50])
    campaign.color_linkup = rgb2hex(pix[650, 50])
    campaign.color_linkdown = rgb2hex(pix[970, 50])
    campaign.color_counterback = rgb2hex(pix[1290, 50])
    campaign.save()
    print(f'{campaign.title} --> {campaign.rpgsystem} Ok')
