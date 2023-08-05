class FieldRegistry:
  FIELDS = {
    'A':  { 'h': 'seller_vat_number'    , 't': 's', 'r': True },
    'B':  { 'h': 'buyer_vat_number'     , 't': 's', 'r': True },
    'C':  { 'h': 'buyer_country'        , 't': 's', 'r': True },
    'D':  { 'h': 'document_type'        , 't': 's', 'r': True },
    'E':  { 'h': 'document_status'      , 't': 's', 'r': True },
    'F':  { 'h': 'document_date'        , 't': 'd', 'r': True },
    'G':  { 'h': 'document_id'          , 't': 's', 'r': True },
    'H':  { 'h': 'atcud'                , 't': 's', 'r': True },
    'L':  { 'h': 'total_vat_exempt'     , 't': 'c' },
    'M':  { 'h': 'total_stamp_duty'     , 't': 'c' },
    'N':  { 'h': 'total_vat'            , 't': 'c' },
    'O':  { 'h': 'total_gross'          , 't': 'c' },
    'P':  { 'h': 'total_tax_witholded'  , 't': 'c' },
    'Q':  { 'h': 'hash'                 , 't': 's' },
    'R':  { 'h': 'software_certificate' , 't': 's' },
    'S':  { 'h': 'other_info'           , 't': 'a' },
    'I1': {                               't': 's' },
    'I2': {                               't': 's' },
    'I3': {                               't': 's' },
    'I4': {                               't': 's' },
    'I5': {                               't': 's' },
    'I6': {                               't': 's' },
    'I7': {                               't': 's' },
    'I8': {                               't': 's' },
    'J1': {                               't': 's' },
    'J2': {                               't': 's' },
    'J3': {                               't': 's' },
    'J4': {                               't': 's' },
    'J5': {                               't': 's' },
    'J6': {                               't': 's' },
    'J7': {                               't': 's' },
    'J8': {                               't': 's' },
    'K1': {                               't': 's' },
    'K2': {                               't': 's' },
    'K3': {                               't': 's' },
    'K4': {                               't': 's' },
    'K5': {                               't': 's' },
    'K6': {                               't': 's' },
    'K7': {                               't': 's' },
    'K8': {                               't': 's' },
  }

  def get_field(self, name):
    return self.FIELDS[name]

  def get_mandatory_fields(self):
    return [x for x in self.FIELDS.keys() if self.FIELDS[x].get('r', False)]
