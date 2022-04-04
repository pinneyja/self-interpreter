label _AddSlots: (| p* = lobby |)
label _AddSlots: (| text = (| | _CallMethodByProxy: 'get_text' Arguments: nil) |).
label _AddSlots: (| text: t = (| | _CallMethodByProxy: 'set_text' Arguments: t) |).
label _AddSlots: (| position: pos = (| | _CallMethodByProxy: 'set_position' Arguments: pos) |).
label _AddSlots: (| position = (| | _CallMethodByProxy: 'get_position' Arguments: nil) |).
label _AddSlots: (| size: newSize = (| | _CallMethodByProxy: 'set_size' Arguments: newSize) |).
label _AddSlots: (| size = (| | _CallMethodByProxy: 'get_size' Arguments: nil) |).