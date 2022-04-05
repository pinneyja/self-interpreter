textInput _AddSlots: (| p* = lobby |)
textInput _AddSlots: (| text = (| | _CallMethodByProxy: 'get_text' Arguments: nil) |).
textInput _AddSlots: (| text: t = (| | _CallMethodByProxy: 'set_text' Arguments: t) |).
textInput _AddSlots: (| position: pos = (| | _CallMethodByProxy: 'set_position' Arguments: pos) |).
textInput _AddSlots: (| position = (| | _CallMethodByProxy: 'get_position' Arguments: nil) |).
textInput _AddSlots: (| size: newSize = (| | _CallMethodByProxy: 'set_size' Arguments: newSize) |).
textInput _AddSlots: (| size = (| | _CallMethodByProxy: 'get_size' Arguments: nil) |).