(bool, int?, String?) parseInt(String s) {
  var value = int.tryParse(s);
  if (value != null) {
    return (true, value, null);
  }
  return (false, null, 'Invalid integer format');
}
