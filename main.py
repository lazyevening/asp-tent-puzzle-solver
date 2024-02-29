from clyngor import ASP


def parse(arr, res, pattern):
    for i, row in enumerate(arr):
        for j, char in enumerate(row):
            if char.isdigit():
                res += pattern.format(i + 1, j + 1, char)
            else:
                res += pattern.format(i + 1, j + 1, f'"{char}"')
    return res


with open('in.txt', "r") as f:
    inp = f.read().rstrip('\n').lstrip('\n').lstrip(' ').rstrip(' ').split("\n")
    inp_2 = [line.split(' ') for line in inp]

asp = parse(inp_2, "", "__cell__({0}, {1}, {2}). ")
asp += """
lines(Value) :- __cell__(1,1,Value).
columns(Value) :- __cell__(1,2,Value).
rowTents(Line,Value) :- lines(Lines), Line = 1..Lines, __cell__(Line+1, 2, Value).
colTents(Index,Value) :- lines(Lines), __cell__(Lines+2, Index, Value).
"""
asp = parse(inp, asp, "__char__({0}, {1}, {2}). ")
asp += """
cell(Line, Column, Value) :-
  lines(Lines), Line = 1..Lines,
  columns(Columns), Column = 1..Columns,
  __char__(Line+1, Column, Value).

tree(Line, Column) :- cell(Line, Column, "T").
row(L) :- lines(Lines), L=1..Lines.
col(C) :- columns(Columns), C=1..Columns.
"""

asp += """
{ tent(R, C) : row(R), col(C), not tree(R, C) }.

:- rowTents(R, Num), Num != { tent(R, C) : col(C) }.
:- colTents(C, Num), Num != { tent(R, C) : row(R) }.

adjacent(R, C, RR, C) :- row(R), row(RR), col(C), RR = R+1.
adjacent(R, C, RR, C) :- row(R), row(RR), col(C), RR = R-1.
adjacent(R, C, R, CC) :- row(R), col(C), col(CC), CC = C+1.
adjacent(R, C, R, CC) :- row(R), col(C), col(CC), CC = C-1.


:- tent(R, C), tent(RR, CC), adjacent(R, C, RR, CC).
:- tent(R, C), tent(RR, CC), adjacent(RR, CC, R, C).
:- tent(R, C), tent(R+1, C+1), row(R), row(R+1), col(C), col(C+1).
:- tent(R, C), tent(R-1, C-1), row(R), row(R-1), col(C), col(C-1).
:- tent(R, C), tent(R+1, C-1), row(R), row(R+1), col(C), col(C-1).
:- tent(R, C), tent(R-1, C+1), row(R), row(R-1), col(C), col(C+1).

:- tent(R, C), { tree(RT, CT) : adjacent(R, C, RT, CT) }<1.
tent_to_one_tree(R, C) :-
    tent(R, C), 
    #count { RT2, CT2 : adjacent(R, C, RT2, CT2),
    tree(RT2, CT2) } = 1.
:- tent_count_per_tree(RT, CT, Count), Count > 1, 
   #count { R, C : tent_to_one_tree(R, C),
   adjacent(R, C, RT, CT) } > 1.
"""
result = []
answers = ASP(asp)
for answer in answers:
    for e in answer:
        if e[0] == "tent":
            print(e)
            result.append(f'{e}\n')

with open("out.txt", 'w') as f:
    f.writelines(result)
