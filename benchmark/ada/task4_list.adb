with Ada.Containers.Vectors;
package body List_Ops is
   package Int_Vectors is new Ada.Containers.Vectors(Natural, Integer);
   use Int_Vectors;

   function Double_Evens(Numbers : Vector) return Vector is
      Result : Vector;
   begin
      for N of Numbers loop
         if N mod 2 = 0 then
            Result.Append(N * 2);
         end if;
      end loop;
      return Result;
   end Double_Evens;
end List_Ops;
