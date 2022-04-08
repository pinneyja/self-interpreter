lobby traits _AddSlots: (| gui_widget = (|
	parent* = lobby.
	position: pos = (| | _CallMethodByProxy: 'set_position' Arguments: pos).
	setPositionX: newX Y: newY = (| | position: (| x = newX. y = newY|)).
	position = (| | _CallMethodByProxy: 'get_position' Arguments: nil).
	size: newSize = (| | _CallMethodByProxy: 'set_size' Arguments: newSize).
	setSizeWidth: newWidth Height: newHeight = (| | size: (| height = newHeight. width = newWidth|)).
	size = (| | _CallMethodByProxy: 'get_size' Arguments: nil).
|) |)