with Ada.Text_IO; use Ada.Text_IO;
with Ada.Containers.Indefinite_Hashed_Maps;
with Ada.Strings.Hash;

procedure Count_Words(Input_File, Output_File : String) is
   package Word_Maps is new Ada.Containers.Indefinite_Hashed_Maps
     (String, Natural, Ada.Strings.Hash, "=");
   use Word_Maps;

   Counts : Map;
   File_In, File_Out : File_Type;
   Word : String(1..256);
   Last : Natural;
begin
   Open(File_In, In_File, Input_File);
   while not End_Of_File(File_In) loop
      Get(File_In, Word, Last);
      declare
         W : String := Word(1..Last);
      begin
         if Counts.Contains(W) then
            Counts(W) := Counts(W) + 1;
         else
            Counts.Insert(W, 1);
         end if;
      end;
   end loop;
   Close(File_In);

   Create(File_Out, Out_File, Output_File);
   for C in Counts.Iterate loop
      Put_Line(File_Out, Key(C) & ": " & Natural'Image(Element(C)));
   end loop;
   Close(File_Out);
end Count_Words;
