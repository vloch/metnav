##parameters=text, length, ellipsis='(...)'

if len(text)>length:
   text = text[:length]
   l = text.rfind(' ')
   if l > length/2:
      text = text[:l+1]
   text += ellipsis

return text
