

**cmyk_calculate**
| key | value | necessary? | method | response |
|-----|-------|------------|--------|----------|
| file | your file .pdf | :heavy_check_mark: | POST | - |
| name | your custome name | :heavy_check_mark:| GET | { ..., "Default": [ ... , {'name':**file_name**,'coverage':**int**,'w':**int(MM)**,'h':**int(MM)**} ,...] , ... } | GET |
|part_cal| 1| - | GET | { ..., "PartCal": [ ... , {'name':**file_name**,'coverage':**int**,'data':[**int**,**int**,...],'path': "path/name.jpeg"} , ... ] , ... } |
|tak|1| - | GET | { ... ,  "Tak": **path** , ...}|
| coverage | number | - | GET | same as **tak** |
| change_n | 1 | - | GET | creates a new name by adding a number to the end of this name|

**errors**:
| key | Description |
|-----|-------------|
|**ValError**|You probably forgot to send the **name** variable|
|**AlreadyExists**| You probably sent a file with this name before, so you can send **change_n**|
|**NoFile**| It means that it did not find a file, so maybe you forgot to send a file or you sent a file with the wrong format. |
