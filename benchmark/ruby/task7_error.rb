def parse_int(s)
  { success: true, value: Integer(s) }
rescue ArgumentError => e
  { success: false, error: e.message }
end
