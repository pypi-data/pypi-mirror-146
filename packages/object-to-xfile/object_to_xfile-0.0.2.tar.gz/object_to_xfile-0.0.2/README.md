# Object_to_xFile

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Sachin Indoriya (c) 2022

## Examples of How To Use (Buggy Alpha Version)


```python 
from object_to_xfile.xconvertor  import XConverter

 
dummy_data = {['name':'John','age':23,'hobby':'reading'],['name':'Tom','age':23,'hobby':'coding']}

# create XConvertor object
x_convertor_obj = XConverter(dummy_data)


# for csv, call to_csv() methods
x_convertor_obj.to_csv()

# for html, call to_html() methods
x_convertor_obj.to_html()

# for excel, call to_excel() methods
x_convertor_obj.to_excel()

# for pdf, call to_pdf() methods
x_convertor_obj.to_pdf()

# for xml, call to_xml() methods
x_convertor_obj.to_xml()
```


 