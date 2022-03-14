globals _AddSlots: (| bootstrap = (). modules = (|init=(|copy = ()|)|)|).
globals _AddSlots: (| true = 1 _IntEQ: 1. false = 0 _IntEQ: 1.|).
globals _AddSlots: (|raiseError = ()|).

globals modules _AddSlots: (|
  boolean=(|postFileIn=(| | 'postFileIn')|).
  block=(|postFileIn=(| | 'postFileIn')|).
  nil=(|postFileIn=(| | 'postFileIn')|).
  rootTraits=(|postFileIn=(| | 'postFileIn')|).
  collector=(|postFileIn=(| | 'postFileIn')|).
  collection=(|postFileIn=(| | 'postFileIn')|).
  smallInt=(|postFileIn=(| | 'postFileIn')|).
  integer=(|postFileIn=(| | 'postFileIn')|).
  integerIteration=(|postFileIn=(| | 'postFileIn')|).
  float=(|postFileIn=(| | 'postFileIn')|).
  number=(|postFileIn=(| | 'postFileIn')|).
  vector=(|postFileIn=(| | 'postFileIn')|).
  indexable=(|postFileIn=(| | 'postFileIn')|).
  defaultBehavior=(|postFileIn=(| | 'postFileIn')|).
  string=(|postFileIn=(| | 'postFileIn')|).
  setAndDictionary=(|postFileIn=(| | 'postFileIn'). parent* = lobby|).
  |).

traits _AddSlots: (|
  block = ().
  orderedOddball=(|parent* = lobby. value=(| | self)|).
  clonable = (|parent* = lobby|).
  vector = ().
  byteVector = ().
  canonicalString = ().
  mutableString = ().
  |).

bootstrap _AddSlots: (|addSlotsTo: destObj From: object = (| | destObj _AddSlots: object) |).
bootstrap _AddSlots: (|remove: slotName From: object = (| | object _RemoveSlot: slotName IfFail: [|:a. :b| object]) |).
bootstrap _AddSlots: (|define: destObj ToBe: object = (| | destObj _Define: object) |).
bootstrap _AddSlots: (|stub = (|parent* = lobby|)|).
bootstrap stub _AddSlots: (| -> n = (| | followThrough: n IfNeedToMakeObject: [|:x| x makeObject] )|).
bootstrap stub _AddSlots: (| name <- ''. object <- lobby|).

vector _AddSlots: (|parent* = traits vector|).
byteVector _AddSlots: (|parent* = traits byteVector|).
string _AddSlots: (|parent* = traits canonicalString|).
mutableString _AddSlots: (|parent* = traits mutableString|).

bootstrap stub _AddSlots: (| followThrough: n IfNeedToMakeObject: b = 
  (|r| 
    r: bootstrap stub _Clone.
    r name: n.
    
    n _IsStringIfFalse: [^object].
    r object: object _GetSlot: n.
    r
    )
  |).
  
bootstrap _AddSlots: (| setObjectAnnotationOf: object From: objWAnno = (| | object) |).
bootstrap _AddSlots: (| read: name From: dir = (| | 1) |).