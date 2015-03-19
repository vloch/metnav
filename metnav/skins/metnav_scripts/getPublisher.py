##title=get Publisher Name from  vcard
##parameters=publisher=''
acadFn      = str(publisher).split("\n")[3]
acadName    = acadFn.split(":")[1]

return acadName
