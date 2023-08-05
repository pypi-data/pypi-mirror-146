from .field_registry import FieldRegistry

class Parser:
  def __init__(self, human_readable_fields=False, parse_numbers=True):
    self.human_readable_fields = human_readable_fields
    self.parse_numbers = parse_numbers
    self.field_registry = FieldRegistry()

  def parse(self, string):
    pairs = string.split('*')
    
    fields = {}
    for f in pairs:
      k, v = f.split(':')
      field_def = self.field_registry.get_field(k)

      if self.human_readable_fields: 
        try:
          k = field_def['human']
        except Exception as e:
          pass

      if field_def['type'] == 'c':
        v = float(v)

      fields[k] = v

    return fields
