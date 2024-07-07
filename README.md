This module receives a PDF file ( Multipart ) as input

and returns as output:

1- The percentage used of each color (C, M, Y, K, Pantone, Spots...) Along with the photo

2- width and heught of each color channel ( For example, in the magenta channel, you have some color density in the coordinates (0,0) and you have some in the coordinates (10,20), so the width and height it gives you in the output are 20px and 10px, respectively, which are in Returns the unit of millimeters. )

3- TAK (printing term meaning high density of color)

4- In offset printing machines, there are valves to adjust the colors, the amount of adjustment of these will returns too.

## Dependencies
1- **[Ghostscript](https://ghostscript.com/releases/gsdnld.html)** 

2- **[Pillow](https://pypi.org/project/pillow/)**
```
pip install pillow
```

## Inputs
| key | value | necessary? | Desc |
|-----|-------|------------|------|
| file | your file .pdf | :heavy_check_mark: | method=post - type=multipart |
| NAME | your custome name | - | output -> { ..., "Default": [ ... , {'name':**file_name**,'coverage':**int**,'w':**int(MM)**,'h':**int(MM)**} ,...] , ... } |
|IPATH| your custome path | - | Where the input file is saved. Please note that the input PDF file must be saved as file.pdf |
|OPATH| your custome path | - | Where the output file is going to be saved |
|PART_CALCULATE| True | - | output -> { ..., "PartCal": [ ... , {'name':**file_name**,'coverage':**int**,'data':[**int**,**int**,...],'path': "path/name.jpeg"} , ... ] , ... } |
|TAK| True | - | output -> { ... ,  "Tak": **path** , ...}|
| TAK_SIZE | number | - | output -> same as **tak** |


**errors**:
| key | Description |
|-----|-------------|
|**ValError**|You probably forgot to send the **name** variable|
|**NoFile**| It means that it did not find a file, so maybe you forgot to send a file or you sent a file with the wrong format. |
