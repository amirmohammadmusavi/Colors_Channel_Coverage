from PIL import Image
import os , fnmatch
import time

def Channel_Coverage(IPATH='image_inputs/',OPATH=False,NAME=False,CHANGE_N=False,PART_CALCULATE=False,TAK=False,TAK_SIZE=False):
    """ 
    IPATH => input files path | OPATH => output files path
    NAME => send in url       | PART_CALCULATE => send in url if u want calculate each part
    CHANGE_N => change folder's name if already exists
    Tak => send in url if you want calculate the tak | TAK_SIZE => custome coverage limit
    """

    TIME = time.time()

    if not NAME:
        NAME = 'file'
    NAME+="-"+str(TIME) # for being unic
    start = time.time()

    if not OPATH:
        OPATH = "Output/static/Projects_Data/"
        if not os.path.exists(OPATH):
            os.makedirs(OPATH)
    # Where the photos of separated colors are placed =>
    if not os.path.exists(IPATH):
        os.makedirs(IPATH)

    # if folder already exists and user requested to change name
    if CHANGE_N and NAME:
        unic=False
        i=0
        while not unic:
            i+=1
            print("__________",OPATH+NAME+str(i))
            if not os.path.exists(OPATH+NAME+str(i)):
                NAME = NAME+str(i)
                unic=True

    # check if not file already exist
    if not os.path.exists(OPATH+NAME):
        # now we run ghostscript command for separated colors and save them as tiff files =>
        os.system(f'gs -sDEVICE=tiffsep -o {IPATH}c.tiff  {IPATH}file.pdf')
        # get all .tiff
        FILES = fnmatch.filter(os.listdir(IPATH), '*.tiff')

        # sort response
        SORT_ORDER = ["c(Cyan).tiff", "c(Magenta).tiff", "c(Yellow).tiff", "c(Black).tiff"]
        newfiles=[]
        for s in SORT_ORDER:
            for f in FILES:
                if s== f:
                    newfiles.append(s)
                    FILES.remove(f)
        newfiles+=FILES
        FILES=newfiles
        # calculate colors coverage each separately
        Tak_R = []
        all_in_percent = []
        partition_list = []
        tak_list = {}
        
        for f in FILES :

            O_FILE = Image.open(IPATH+f)
            image_sizew,image_sizeh = O_FILE.size # get width,height
            file_name=f.split('.')[0].replace('c(','').replace(')','')
            PixelCount=image_sizeh*image_sizew
            if not f == "c.tiff":
                val=0 # Collects colored pixels

                p = {
                    'p1':False,
                    'p1w':False,
                    'p2':False,
                    'p3':False,
                }

                if PART_CALCULATE:
                    partval=0
                    step = 70
                    columns = image_sizew//step
                    step_counter = 0
                    partition_size = image_sizeh*step
                    extra=(image_sizew-(step*columns))//2
                    partition_data={'name':file_name,'coverage':0,'data':[],'path':f'{OPATH}{NAME}/{file_name}.jpeg'}
                    part1=(step*step_counter)+extra
                    part2=(step*(step_counter+1))+extra

                for i in range(0, image_sizew):
                    for j in range(0, image_sizeh):
                        
                        pixVal = O_FILE.getpixel((i, j))

                        if PART_CALCULATE:
                            if i>=part1:
                                if i <= part2:
                                    
                                    if pixVal != 255 and type(pixVal) != tuple: # no white pixels
                                        partval+= 100-(pixVal/2.55)
                                    
                                else:
                                    if pixVal != 255 and type(pixVal) != tuple: # no white pixels
                                        partval+= 100-(pixVal/2.55)
                                    final_val = round(partval/partition_size)
                                    partition_data['data'].append(final_val)
                                    partval=0
                                    step_counter+=1
                                    part1=(step*step_counter)+extra
                                    part2=(step*(step_counter+1))+extra

                        if TAK and type(pixVal) != tuple:

                            if f"{(i,j)}" in tak_list:
                                tak_list[f"{(i,j)}"] += 100 - (pixVal//2.55)
                            else:
                                tak_list[f"{(i,j)}"] = 100 - (pixVal//2.55)

                        if pixVal != 255 and type(pixVal) != tuple: # no white pixels
                            if p['p1'] and j < p['p1']:
                                p['p1']=j
                            if p['p2'] and j > p['p2']:
                                p['p2']=j
                            if p['p3'] and i > p['p3']:
                                p['p3']=i

                            if not p['p1'] and not p['p1w']:
                                p['p1']=j
                                p['p1w']=i
                            elif not p['p2']:
                                if j+1 != image_sizeh:
                                    if j+1 <= image_sizeh and O_FILE.getpixel((i, j+1))==255:
                                        p['p2']=j
                                else:
                                    p['p2']=j+1
                            elif not p['p3']:
                                if i+1 != image_sizew:
                                    if i+1 <= image_sizew and O_FILE.getpixel((i+1, j))==255:
                                        p['p3']=i
                                else:
                                    p['p3']=i+1

                            val+= 100- (pixVal//2.55) # always give 0 to 255 but i just want cmyk => 0 to 100

                if PART_CALCULATE:
                    partition_list.append(partition_data)
                    partition_data['coverage']=round(val//PixelCount)

                r={'name':file_name,'coverage':round(val//PixelCount),'w':str(((image_sizew-p['p1w'])-(image_sizew-p['p3']))//2.83)+' mm','h':str(((image_sizeh-p['p1'])-(image_sizeh-p['p2']))//2.83)+' mm'}
                all_in_percent.append(r)
            
            # convert tiff to jpeg
            if OPATH:
                outfile = file_name + ".jpeg"
                im = O_FILE
                out = im.convert("RGB")
                if not os.path.exists(OPATH+NAME+"/"):
                    os.makedirs(OPATH+NAME+"/")
                
                out.save(OPATH+NAME+"/"+outfile, "JPEG", quality=100)

            O_FILE.close()
            os.remove(IPATH+f) # remove .tiff file in the end
        if TAK:
            new = Image.new(mode="RGB", size=(image_sizew,image_sizeh))
            Pixels = new.load()
            for i in range(0, image_sizew):
                for j in range(0, image_sizeh):
                    if TAK_SIZE:
                        TAK_SIZE= int(TAK_SIZE)
                        if tak_list[f"{(i,j)}"] < TAK_SIZE:
                            Pixels[i,j] = (255,255,255)
                        else:
                            Pixels[i,j] = (106,4,16)
                    else:
                        if tak_list[f"{(i,j)}"] < 200:
                            Pixels[i,j] = (255,255,255)
                        elif tak_list[f"{(i,j)}"] < 250:
                            Pixels[i,j] = (250,163,7)
                        elif tak_list[f"{(i,j)}"] < 300:
                            Pixels[i,j] = (232,93,4)
                        elif tak_list[f"{(i,j)}"] < 351:
                            Pixels[i,j] = (157,2,8) # (208,150,0)
                        elif tak_list[f"{(i,j)}"] < 400:
                            Pixels[i,j] = (106,4,16)  #(157,2,8)
                        elif tak_list[f"{(i,j)}"] < 500:
                            Pixels[i,j] = (55,6,23)
            if IPATH:
                new.save(OPATH+NAME+'/tak.jpg')
            Tak_R.append(OPATH+NAME+'/tak.jpg')
    else:
        return "AlreadyExists"
    end = time.time()
    if os.path.exists(IPATH+'file.pdf'):
        os.remove(IPATH+f'file.pdf')
    else:
        return "NoFile"
    print(end - start,'___ Core')
    FinalData = {}
    if len(FILES) > 0:
        FinalData["DefPath"]=f'{OPATH}{NAME}/c.jpeg'
    
    # add cmyk coverage if exists all 4 channel
    if all_in_percent:
        is_true=0
        CMYK=0
        for a in all_in_percent:
            if a["name"]=="Cyan" or a["name"]== "Magenta" or a["name"]== "Yellow" or a["name"]== "Black":
                is_true+=1
                print(is_true)
                CMYK+=a["coverage"]
        if is_true == 4:
            all_in_percent.append({"name":"CMYK","coverage":CMYK/4})

    FinalData["Default"]=all_in_percent
    FinalData["Tak"]=Tak_R
    FinalData["PartCal"]=partition_list
    return FinalData