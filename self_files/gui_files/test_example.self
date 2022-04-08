_AddSlots: (| testContainer = container wcopy. subContainer = container wcopy. spacingContainer = container wcopy|).
testContainer setSizeWidth: 0.25 Height: 0.4.
testContainer addWidget: 
	((((subContainer setOrientationIsVertical: false) setSizeWidth: 1 Height: 0.2)
		addWidget: ((label clone text: '1') setSizeWidth: 1 Height: 1))
		addWidget: ((button clone text: '2') setSizeWidth: 1 Height: 1)).
testContainer addWidget: spacingContainer.
canvas addWidget: testContainer.
subContainer setColorR: 0.4 G: 0.1 B: 0.3 A: 1.
spacingContainer setColorR: 0.1 G: 0.2 B: 0.5 A: 1.
testContainer addWidget: (textInput clone text: '3').

'Containers are always filled in one axis. If horizontal, their subwidgets will fill their entire width, If vertical, their height will be filled'.
'To create empty space in a filled axis, add an empty container'.