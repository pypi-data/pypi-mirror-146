import os, sys
from dataclasses import dataclass
from typing import List, Optional

try:
    from .base import extract_item, Item
except ImportError:
    sys.path.append(os.getcwd())
    from base import extract_item, Item

gen_class_name = [
    'DOGenerator',
    'EntityGenerator',
    'ValueObjectGenerator',
    'ConverterGenerator',
    'AssemblerGenerator',
    'DTOGenerator'
]

def extract_unique_value_type(classes):
    all_items = [extract_item(c) for c in classes]
    unique_items = []
    cache = {}
    for _items in all_items:
        for item in _items:
            item: Item
            # type_idx = var_to_value_type(item.name) if item.value_type2 is None else item.value_type2
            if item.value_type in cache:
                continue
            else:
                cache[item.value_type] = 0
                unique_items.append(item)
    return unique_items


class DOGenerator:
    @staticmethod
    def gen(classes, save_dir, save_name='do_temp.py'):
        save_fn = os.path.join(save_dir, save_name)
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        with open(save_fn, 'w') as f:
            f.write('from typing import List, Optional')
            f.write('\n')
            f.write('from dataclasses import dataclass')
            f.write('\n')
            f.write('from ddd_objects.infrastructure.do import BaseDO')
            f.write('\n\n')
            for c in classes:
                items = extract_item(c)
                class_name = f'{c.__name__}DO'
                block = DOGenerator.__gen_do_class_block(class_name, items)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_do_class_block(class_name, items):
        strip1 = [
            f'    {item.name}: {item.item_type}={item.value_default_value}' 
            if not item.required
            else f'    {item.name}: {item.item_type}'
            for item in items
        ]
        strip1 = '\n'.join(strip1)
        block = f"""
@dataclass
class {class_name}(BaseDO):
{strip1}
        """
        return block


class ValueObjectGenerator:
    @staticmethod
    def gen(classes, save_dir, save_name='value_obj_temp.py'):
        save_fn = os.path.join(save_dir, save_name)
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        unique_items = extract_unique_value_type(classes)
        
        with open(save_fn, 'w') as f:
            f.write('from ddd_objects.domain.value_obj import ExpiredValueObject')
            f.write('\n\n')
            for item in unique_items:
                f.write(ValueObjectGenerator.__gen_var_class_block(item))
            f.write('\n')

    @staticmethod
    def __gen_var_class_block(item):
        block = f"""
class {item.value_type}(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, {item.life_time})
"""
        return block


class EntityGenerator:

    @staticmethod
    def gen(classes, save_dir, save_name='entity_temp.py'):
        save_fn = os.path.join(save_dir, save_name)
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        all_items = [extract_item(c) for c in classes]
        unqiue_items = extract_unique_value_type(classes)

        with open(save_fn, 'w') as f:
            f.write('from typing import List, Optional')
            f.write('\n')
            f.write('from ddd_objects.domain.entity import Entity, ExpiredEntity')
            f.write('\n')
            f.write('from .value_obj import (')
            f.write('\n')
            for item in unqiue_items:
                item: Item
                f.write(f'    {item.value_type},')
                f.write('\n')
            f.write(')')
            f.write('\n\n')
            for items, c in zip(all_items, classes):
                block = EntityGenerator.__gen_entity_class_block(c.__name__, items)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_entity_class_block(class_name, items):
        strip1 = []
        is_expired_class = False
        for item in items:
            item: Item
            if item.name == '_life_time':
                is_expired_class = True
            default = '' if item.required else f' = {item.entity_default_value}'
            strip1.append(f'        {item.name}: {item.entity_type}{default}')
            
        strip2 = [f'        self.{item.name}={item.name}' for item in items]
        strip1 = ',\n'.join(strip1)
        strip2 = '\n'.join(strip2)
        block = f"""
class {class_name}({'ExpiredEntity' if is_expired_class else 'Entity'}):
    def __init__(
        self,
{strip1}
    ):
{strip2}
        {'super().__init__(_life_time)' if is_expired_class else ''}
              
        """
        return block


class ConverterGenerator:
    @staticmethod
    def gen(classes, save_dir, save_name='converter_temp.py'):
        save_fn = os.path.join(save_dir, save_name )
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        all_items = [extract_item(c) for c in classes]
        unique_items = extract_unique_value_type(classes)
        entity_names = [c.__name__ for c in classes]

        with open(save_fn, 'w') as f:
            f.write('from typing import List')
            f.write('\n')
            f.write('from ddd_objects.infrastructure.converter import Converter')
            f.write('\n')
            f.write('from ..domain.entity import (')
            f.write('\n')
            for entity_name in entity_names:
                f.write(f'    {entity_name},')
                f.write('\n')
            f.write(')')
            f.write('\n')
            f.write('from .do import (')
            f.write('\n')
            for entity_name in entity_names:
                f.write(f'    {entity_name}DO,')
                f.write('\n')
            f.write(')')
            f.write('\n')
            f.write('from ..domain.value_obj import (')
            f.write('\n')
            for item in unique_items:
                item: Item
                f.write(f'    {item.value_type},')
                f.write('\n')
            f.write(')')
            f.write('\n\n')
            for items, c in zip(all_items, classes):
                block = ConverterGenerator.__gen_converter_class_block(c.__name__, items)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_converter_class_block(class_name, items):
        strip1 = []
        strip2 = []
        for item in items:
            item: Item
            if 'List' in item.item_type:
                strip1.append(' '*12+f'{item.name} = [{item.value_type}(m) for m in do.{item.name}]')
                strip2.append(' '*12+f'{item.name} = None if x.{item.name} is None \
else [m.get_value() for m in x.{item.name}]')
            else:
                strip1.append(' '*12+f'{item.name} = {item.value_type}(do.{item.name})')
                strip2.append(' '*12+f'{item.name} = None if x.{item.name} is None \
else x.{item.name}.get_value()')

        strip1 = ',\n'.join(strip1)
        strip2 = ',\n'.join(strip2)
        block = f"""
class {class_name}Converter(Converter):
    def to_entity(self, do: {class_name}DO):
        return {class_name}(
{strip1}
        )
    def to_do(self, x: {class_name}):
        return {class_name}DO(
{strip2}
        )
              
        """
        return block


class DTOGenerator:
    @staticmethod
    def gen(classes, save_dir, save_name='dto_temp.py'):
        save_fn = os.path.join(save_dir, save_name)
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        with open(save_fn, 'w') as f:
            f.write('from typing import List, Optional')
            f.write('\n')
            f.write('from pydantic import BaseModel')
            f.write('\n\n')
            for c in classes:
                items = extract_item(c)
                class_name = f'{c.__name__}DTO'
                block = DTOGenerator.__gen_dto_class_block(class_name, items)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_dto_class_block(class_name, items):
        strip1 = [
            f'    {item.name}: {item.item_type}={item.value_default_value}' 
            if not item.required
            else f'    {item.name}: {item.item_type}'
            for item in items
        ]
        strip1 = '\n'.join(strip1)
        block = f"""

class {class_name}(BaseModel):
{strip1}
        """
        return block


class AssemblerGenerator:
    @staticmethod
    def gen(classes, save_dir, save_name='assembler_temp.py'):
        save_fn = os.path.join(save_dir, save_name )
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        all_items = [extract_item(c) for c in classes]
        unique_items = extract_unique_value_type(classes)
        entity_names = [c.__name__ for c in classes]

        with open(save_fn, 'w') as f:
            f.write('from typing import List')
            f.write('\n')
            f.write('from ddd_objects.application.assembler import Assembler')
            f.write('\n')
            f.write('from ..domain.entity import (')
            f.write('\n')
            for entity_name in entity_names:
                f.write(f'    {entity_name},')
                f.write('\n')
            f.write(')')
            f.write('\n')
            f.write('from .dto import (')
            f.write('\n')
            for entity_name in entity_names:
                f.write(f'    {entity_name}DTO,')
                f.write('\n')
            f.write(')')
            f.write('\n')
            f.write('from ..domain.value_obj import (')
            f.write('\n')
            for item in unique_items:
                item: Item
                f.write(f'    {item.value_type},')
                f.write('\n')
            f.write(')')
            f.write('\n\n')
            for items, c in zip(all_items, classes):
                block = AssemblerGenerator.__gen_dto_class_block(c.__name__, items)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_dto_class_block(class_name, items):
        strip1, strip2 = [], []
        for item in items:
            item: Item
            if 'List' in item.item_type:
                strip1.append(' '*12+f'{item.name} = [{item.value_type}(m) for m in dto.{item.name}]')
                strip2.append(' '*12+f'{item.name} = None if x.{item.name} is None \
else [m.get_value() for m in x.{item.name}]')
            else:
                strip1.append(' '*12+f'{item.name} = {item.value_type}(dto.{item.name})')
                strip2.append(' '*12+f'{item.name} = None if x.{item.name} is None \
else x.{item.name}.get_value()')

        strip1 = ',\n'.join(strip1)
        strip2 = ',\n'.join(strip2)
        block = f"""
class {class_name}Assembler(Assembler):
    def to_entity(self, dto: {class_name}DTO):
        return {class_name}(
{strip1}
        )
    def to_dto(self, x: {class_name}):
        return {class_name}DTO(
{strip2}
        )
              
        """
        return block


if __name__ == '__main__':
    @dataclass
    class Template:
        attr0: str
        attr1: str = ('Number', 1, 1)
        attr2: List[str] = ('List[ID]', ['a'])
        attr3: Optional[str] = 'Number'
        attr4: Optional[List[str]] = 'DateTime'
    save_dir = os.path.dirname(__file__)
    DOGenerator.gen([Template], save_dir)
    ValueObjectGenerator.gen([Template], save_dir)
    EntityGenerator.gen([Template], save_dir)
    ConverterGenerator.gen([Template], save_dir)
    DTOGenerator.gen([Template], save_dir)
    AssemblerGenerator.gen([Template], save_dir)