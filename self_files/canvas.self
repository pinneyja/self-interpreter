canvas _AddSlots: (|addWidget: widget = (| | _CallMethodByProxy: 'add_widget' Arguments: widget. widgets add: widget)|).
canvas _AddSlots: (|removeWidget: widget = (| | 
    _CallMethodByProxy: 'remove_widget' Arguments: widget.
    widgets rep findFirstLink: [|:lnk| lnk value _Eq: widget]
        IfPresent: [|:lnk| lnk remove. widgets size: widgets size - 1]
        IfAbsent: 'not found'.)|).
canvas _AddSlots: (|widgets = list copy|).