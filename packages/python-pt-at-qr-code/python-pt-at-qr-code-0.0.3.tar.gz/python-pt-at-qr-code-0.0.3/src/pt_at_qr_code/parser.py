from .field_registry import FieldRegistry
from .exceptions import InvalidQRCode

class Parser:
  def __init__(self, human_readable_fields=False, parse_numbers=True):
    self.human_readable_fields = human_readable_fields
    self.parse_numbers = parse_numbers
    self.field_registry = FieldRegistry()

  def parse(self, string):
    pairs = string.split('*')
    
    raw_fields = {}
    fields = {}
    for f in pairs:
      k, v = f.split(':')
      field_def = self.field_registry.get_field(k)

      if field_def['t'] == 'c':
        v = float(v)
      
      raw_fields[k] = v

      if self.human_readable_fields: 
        try:
          k = field_def['h']
        except Exception as e:
          pass

      fields[k] = v

    # Check mandatory fields
    for mf in self.field_registry.get_mandatory_fields():
      if raw_fields.get(mf, None) is None:
        raise InvalidQRCode("Missing mandatory field '%s'" % mf)       

    return fields
