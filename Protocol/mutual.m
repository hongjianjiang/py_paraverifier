const clientNUMS : 3;
type state : enum{idle, try, crit, exit};

     client: 1..clientNUMS;

var n : array [client] of state;

    x : boolean;

ruleset i : client do
rule "Try" n[i] = idle ==> begin
      n[i] := try;end;

rule "Crit"
      n[i] = try& x = true ==>begin
      n[i] := crit; x := false; end;

rule "Exit"
      n[i] = crit ==>begin
      n[i] := exit;end;


rule "Idle"
      n[i] = exit & x = false ==> begin n[i] := idle;
      x := true;end;
endruleset;

startstate
begin
 for i: client do
    n[i] := idle;
    x := true;
  endfor;
endstartstate;

ruleset i:client; j: client do
invariant "coherence"
 ! (n[i] = crit & n[j] = crit)
endruleset;
