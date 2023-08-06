import re
from dataclasses import dataclass, _MISSING_TYPE
from typing import List, Optional

@dataclass
class Item:
    name: str
    item_type: str
    entity_type: str
    value_type: str
    default_value: int
    value_default_value: str
    entity_default_value: str
    required: bool
    life_time: int = None

def var_to_value_type(do_name):
    upper_list = ['id']
    parts = do_name.split('_')
    parts = [p.upper() if p in upper_list else p for p in parts ]
    parts = [p.capitalize() if not p.isupper() else p for p in parts]
    return ''.join(parts)

def extract_item(cls):
    class_vars = cls.__annotations__
    class_fields = cls.__dataclass_fields__
    pattern = r'List\[(.*)\]'
    items = []
    for key in class_fields:
        item_type = class_vars[key].__name__  \
            if hasattr(class_vars[key], '__name__') else str(class_vars[key]) \
            .replace('__main__.', '').replace('typing.', '')

        value_type = class_fields[key].default[0]  \
            if isinstance(class_fields[key].default, tuple) else class_fields[key].default \
            if not isinstance(class_fields[key].default, _MISSING_TYPE) else var_to_value_type(key)
        if 'List' in value_type:
            value_type =  re.search(pattern, value_type).group(1)
        if 'List' in item_type:
            entity_type = f'List[{value_type}]'
        else:
            entity_type = value_type
        if 'Optional' in item_type:
            entity_type = f'Optional[{entity_type}]'

        default_value = class_fields[key].default[1] \
            if isinstance(class_fields[key].default, tuple) and len(class_fields[key].default)>1 \
            else None

        if isinstance(class_fields[key].default, tuple) and len(class_fields[key].default)>1:
            required = False
        else:
            required = True

        if default_value is None:
            value_default_value = None
            entity_default_value = None

        elif 'List' in entity_type:
            assert isinstance(default_value, list), f"default value of {key} should be list"
            value_default_value = [f"'{v}'" if isinstance(v, str) else str(v) for v in default_value]
            entity_default_value = [f"{value_type}({v})" for v in value_default_value]
            value_default_value = f"[{','.join(value_default_value)}]"
            entity_default_value = f"[{','.join(entity_default_value)}]"
        else:
            value_default_value = f"'{default_value}'" \
                if isinstance(default_value, str) else default_value
            entity_default_value = f"{value_type}('{default_value}')" \
                if isinstance(default_value, str) else f"{value_type}({default_value})"
        life_time = class_fields[key].default[2] \
            if isinstance(class_fields[key].default, tuple) and len(class_fields[key].default)>2 \
            else None
        items.append(Item(
            key, 
            item_type, 
            entity_type, 
            value_type, 
            default_value, 
            value_default_value, 
            entity_default_value,
            required,
            life_time
        ))
 
    return items
    

if __name__ == '__main__':
    @dataclass
    class Template:
        attr0: str
        attr1: str = ('Number', 1, 1)
        attr2: List[str] = (None, 'a', 1)
        attr3: Optional[str] = 'String'
        attr4: Optional[List[str]] = 'Number'
    items = extract_item(Template)
    print(items)
