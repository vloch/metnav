##parameters=typeForm=''

request=context.REQUEST
types=request.get('meta_type', None)
myType=typeForm.rstrip()

typesStr=''
if types is None:
    return True
else:
    if len(types)>0:
        for a in types:
            type=a.encode('utf-8').rstrip('\r\n')
            typesStr +=type+' '

        if typesStr.find(myType)!=-1:
            return True
        else:
            return False