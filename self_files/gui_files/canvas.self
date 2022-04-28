canvas _AddSlots: (|
	widgets = list clone.
	parent* = traits gui_widget.
	superwidget* = mixins gui_superwidget.
    gui_parent <- nil.
	addOutliner: object = (| outliner. slotsContainer. indexableContainer. isVector. indexableLabel. |
		object _GetGUIRepresentation ifNotNil: [
			canvas removeWidget: object _GetGUIRepresentation.
		].

		outliner: container wcopy.
		outliner setSizeWidth: 0.3 Height: 0.5.
		outliner _AddSlots: (| object = object|).
		fillOutlinerSkeleton: outliner Object: object.

		slotsContainer: scrollableContainer wcopy.
		slotsContainer setSizeWidth: 1 Height: 4.
		outliner addWidget: slotsContainer.
		outliner _AddSlots: (|slotsContainer = slotsContainer|).
		fillOutlinerSlots: outliner Object: object.

		isVector: true.
		object _SizeIfFail: [isVector: false].
		isVector ifTrue: [
			indexableLabel: label clone.
			indexableLabel text: 'Indexable'.
			indexableLabel setSizeWidth: 1 Height: 0.5.
			outliner addWidget: indexableLabel.

			indexableContainer: scrollableContainer wcopy.
			indexableContainer setSizeWidth: 1 Height: 4.
			outliner addWidget: indexableContainer.
			outliner _AddSlots: (|indexableContainer = indexableContainer|).
			fillOutlinerIndexable: outliner Object: object.
		].

		addWidget: outliner.
		object _SetGUIRepresentation: outliner.
	).

	fillOutlinerSkeleton: outliner Object: object = (| buttonBar. evaluatorButton. closeButton. |
		outliner addWidget: (label clone text: object _GetName) setSizeWidth: 1 Height: 0.5.

		buttonBar: container wcopy.
		buttonBar setSizeWidth: 1 Height: 0.5.
		buttonBar orientation: 'horizontal'.
		evaluatorButton: button clone.
		evaluatorButton text: 'Evaluator'.
		evaluatorButton _AddSlots: (|onRelease = (| evaluatorContainer. input. innerButtonBar. temp. |
			evaluatorContainer: container wcopy.
			input: textInput clone.
			evaluatorContainer addWidget: input.
			innerButtonBar: container wcopy orientation: 'horizontal'.
			innerButtonBar addWidget: (button clone text: 'Get It') _AddSlots: (| input = input. onRelease = (| | canvas addOutliner: (gui_parent gui_parent gui_parent object _RunCodeInContext: input text)) |).
			innerButtonBar addWidget: (button clone text: 'Do It') _AddSlots: (| input = input. onRelease = (| | gui_parent gui_parent gui_parent object _RunCodeInContext: input text) |).
			innerButtonBar addWidget: (button clone text: 'Close') _AddSlots: (| onRelease = (| temp. | 
				temp: gui_parent gui_parent gui_parent size.
				gui_parent gui_parent gui_parent setSizeWidth: (temp width) Height: (temp height - 0.1).
				temp: gui_parent gui_parent gui_parent position.
				gui_parent gui_parent gui_parent setPositionX: (temp x) Y: (temp y + 0.1).
				gui_parent gui_parent gui_parent removeWidget: gui_parent gui_parent.
			)|).
			evaluatorContainer addWidget: innerButtonBar.
			gui_parent gui_parent addWidget: evaluatorContainer.
			temp: gui_parent gui_parent size.
			gui_parent gui_parent setSizeWidth: (temp width) Height: (temp height + 0.1).
			temp: gui_parent gui_parent position.
			gui_parent gui_parent setPositionX: (temp x) Y: (temp y - 0.1).
		)|).
		closeButton: button clone.
		closeButton text: 'Close'.
		closeButton _AddSlots: (|onRelease = (| | canvas removeWidget: gui_parent gui_parent)|).
		buttonBar addWidget: evaluatorButton.
		buttonBar addWidget: closeButton.
		outliner addWidget: buttonBar.
	).

	fillOutlinerSlots: outliner Object: object = (| slotNameVector. methodNameVector. slotsContainer. |
		slotsContainer: outliner slotsContainer.
		slotsContainer widgets do: [|:x| slotsContainer removeWidget: x].

		slotNameVector: object _GetParentSlotsAsVector.

		slotNameVector do:
			[| :slotName. slotButton. |
				slotButton: button clone.
				slotButton _AddSlots: (| textWithoutStar = slotName|).
				slotButton text: slotName , '*'.
				slotButton _AddSlots: (| onRelease = (| | canvas addOutliner: (gui_parent gui_parent object _GetSlot: textWithoutStar))|).
				slotsContainer addWidget: slotButton].

		slotNameVector: object _GetDataSlotsAsVector.

		slotNameVector do:
			[| :slotName. slotButton. |
				slotButton: button clone.
				slotButton text: slotName.
				slotButton _AddSlots: (| onRelease = (| | canvas addOutliner: (gui_parent gui_parent object _GetSlot: text))|).
				slotsContainer addWidget: slotButton].

		methodNameVector: object _GetMethodSlotsAsVector.

		methodNameVector do:
			[| :methodObject. methodContainer. methodLabel. methodCode. methodButtons. updateButton. resetButton. |
				methodLabel: label clone setSizeWidth: 0.30 Height: 1.
				methodCode: textInput clone.
				methodLabel text: methodObject name.
				methodCode _AddSlots: (| originalCode <- methodObject code|).
				methodCode text: methodObject code.

				methodButtons: container wcopy setSizeWidth: 0.1 Height: 1.
				updateButton: button clone text: ''.
				updateButton setColorR: 0.1 G: 0.7 B: 0.5 A: 1.
				updateButton _AddSlots: (| methodCode = methodCode. methodLabel = methodLabel. |).
				updateButton _AddSlots: (|onRelease = (| addSlotsCommand. | 
					addSlotsCommand: '_AddSlots: (| ' , methodLabel text , ' = (' , methodCode text , ')|)'.
					gui_parent gui_parent gui_parent gui_parent object _RunCodeInContext: addSlotsCommand.
				) |).
				resetButton: button clone text: ''.
				resetButton setColorR: 0.6 G: 0.2 B: 0.3 A: 1.
				resetButton _AddSlots: (| methodCode = methodCode |).
				resetButton _AddSlots: (|onRelease = (| | methodCode text: methodCode originalCode)|).
				methodButtons addWidget: updateButton.
				methodButtons addWidget: resetButton.

				methodContainer: container wcopy.
				methodContainer orientation: 'horizontal'.
				((methodContainer addWidget: methodLabel) addWidget: methodCode) addWidget: methodButtons.
				slotsContainer addWidget: methodContainer].
		
	).

	fillOutlinerIndexable: outliner Object: object = (| slotNameVector. methodNameVector. indexableContainer. index. buttonUtil. |
		indexableContainer: outliner indexableContainer.
		indexableContainer widgets do: [|:x| indexableContainer removeWidget: x].

		index: 0.
		object do:
			[| :valueAtIndex. indexButton. |
				indexButton: button clone.
				indexButton text: '<' , index asString , '>'.
				indexButton _AddSlots: (|
						vectorIndex = index.
						onRelease = (| | canvas addOutliner: (gui_parent gui_parent object _At: vectorIndex))
					|).
				indexableContainer addWidget: indexButton.
				index: index + 1.
			].
		
	).
|).