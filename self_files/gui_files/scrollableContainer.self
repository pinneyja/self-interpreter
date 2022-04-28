scrollableContainer _AddSlots: (|
	widgets = list clone.
	parent* = traits gui_widget.
	superwidget* = mixins gui_superwidget.
    gui_parent <- nil.
	orientation = (| | _CallMethodByProxy: 'get_orientation' Arguments: nil).
	orientation: orient = (| | _CallMethodByProxy: 'set_orientation_clone' Arguments: orient).
	orientationIsVertical = (| | orientation == 'vertical').
	setOrientationIsVertical: bool = (| | orientation: (bool ifTrue: ['vertical'] False: ['horizontal'])).
|).