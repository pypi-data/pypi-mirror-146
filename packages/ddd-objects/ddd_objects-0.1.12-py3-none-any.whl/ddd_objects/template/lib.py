import os, shutil

fn_map = {
    'do_temp.py': 'infrastructure/do.py',
    'converter_temp.py': 'infrastructure/converter.py',
    'entity_temp.py': 'domain/entity.py',
    'value_obj_temp.py': 'domain/value_obj.py',
    'dto_temp.py': 'application/dto.py',
    'assembler.py': 'application/assembler.py'
}

def replace(source_dir, fn, target=None, exclude_classes=[]):
    target_root_dir = f'{source_dir}/..'
    if target is None:
        target = fn_map[fn]
    target_fn = f'{target_root_dir}/{target}'
    source_fn = os.path.join(source_dir, fn)
    with open(target_fn, 'r') as f:
        target_classes = f.read().strip().split('\n\n')
        target_classes, target_header = _extract_class(target_classes)
    with open(source_fn, 'r') as f:
        source_classes = f.read().strip().split('\n\n')
        source_classes, source_header = _extract_class(source_classes, exclude_classes)
    target_classes.update(source_classes)
    target_classes_string = '\n'.join(target_header) + '\n\n' + '\n\n'.join(list(target_classes.values()))
    with open(target_fn, 'w') as f:
        f.write(target_classes_string)



def _extract_class(class_strings, exclude_classes=[]):
    classes = {}
    header = []
    for s in class_strings:
        first_line = s.strip().split('\n')[0]
        if first_line.startswith('class') or first_line.startswith('@dataclass'):
            if any([c in first_line for c in exclude_classes]):
                continue
            classes[first_line] = s.strip()
        else:
            header.append(s.strip())
    return classes, header
