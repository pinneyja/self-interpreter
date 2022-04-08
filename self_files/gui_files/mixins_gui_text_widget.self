mixins _AddSlots: (| gui_text_widget = (|
	text = (| | _CallMethodByProxy: 'get_text' Arguments: nil).
	text: t = (| | _CallMethodByProxy: 'set_text' Arguments: t).
|) |)