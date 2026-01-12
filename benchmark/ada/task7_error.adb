package body Parser is
   function Parse_Int(S : String) return Parse_Result is
   begin
      return (Success => True, Value => Integer'Value(S), Error => <>);
   exception
      when Constraint_Error =>
         return (Success => False, Value => 0, Error => "Invalid integer format");
   end Parse_Int;
end Parser;
