mixins _AddSlots: (| gui_superwidget = (|
	addWidget: widget = (| | _CallMethodByProxy: 'add_widget' Arguments: widget. widgets add: widget. widget gui_parent: self. self).
	removeWidget: widget = (| | 
    	_CallMethodByProxy: 'remove_widget' Arguments: widget.
    	widgets remove: widget IfAbsent: ['widget not present to remove'].
		widget gui_parent: nil. self).
	wcopy = (| c. | c: clone. c _AddSlots: (| widgets = list copy|). c).
|) |).