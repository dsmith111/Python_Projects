import PIL
from PIL import Image, ImageDraw, ImageFont


# In[32]:


# read image and convert to RGB
ext=Image.open("readonly/msi_recruitment.gif")
ext=ext.convert('RGB')


font = ImageFont.truetype('readonly/fanwood-webfont.ttf',size= 50)

image = PIL.Image.new(ext.mode,(ext.width,ext.height+50))
image.paste(ext,(0,0))
# build a list of 9 images which have different color ranges
images=[]
m =[.1,.5,.9]
for i in range(1, 10):
    if i <=3:
        r,g,b=image.split()
        r=r.point(lambda x:x*m[i-1])
        temp=Image.merge(image.mode,[r,g,b])
        draw=ImageDraw.Draw(temp)
        draw.text((0,image.height-45),"Channel {} intensity {}".format(str(0),str(m[i-1])),font=font,fill=(int(255*m[i-1]),255,255))
        images.append(temp)
    elif i<=6 and i>3:
        r,g,b=image.split()
        g=g.point(lambda x:x*m[i-4])
        temp=Image.merge(image.mode,[r,g,b])
        draw=ImageDraw.Draw(temp)
        draw.text((0,image.height-45),"Channel {} intensity {}".format(1,m[i-4]),font=font,fill=(255,int(255*m[i-4]),255))
        images.append(temp)
    else:
        r,g,b=image.split()
        b=b.point(lambda x:x*m[i-7])
        temp=Image.merge(image.mode,[r,g,b])
        draw=ImageDraw.Draw(temp)
        draw.text((0,image.height-45),"Channel {} intensity {}".format(2,m[i-7]),font=font,fill=(255,255,int(255*m[i-7])))
        images.append(temp)
    

# create a contact sheet from different brightnesses
first_image=images[0]
contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*3,first_image.height*3))
x=0
y=0


for img in images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height
    else:
        x=x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
display(contact_sheet)


# ## HINT 1
# 
# Check out the `PIL.ImageDraw module` for helpful functions

# ## HINT 2
# 
# Did you find the `text()` function of `PIL.ImageDraw`?

# ## HINT 3
# 
# Have you seen the `PIL.ImageFont` module? Try loading the font with a size of 75 or so.

# ## HINT 4
# These hints aren't really enough, we should probably generate some more.
