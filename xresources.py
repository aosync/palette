import palette
import motif
import sys

with open(sys.argv[1]) as file:
    PAL = palette.palette(file)

def gen(name, id):
    id -= 1
    
    bg = motif.Variations(PAL[id])

    print("*%sbackground: %s" % (name, bg.bg.dump_srgb()))
    print("*%sforeground: %s" % (name, bg.fg.dump_srgb()))
    print("*%stopShadowColor: %s" % (name, bg.ts.dump_srgb()))
    print("*%sbottomShadorColor: %s" % (name, bg.bs.dump_srgb()))

gen("", 5)

a = motif.Variations(PAL[4])
print("*highlightColor: %s" % (a.fg.dump_srgb()))
print("*highlightTextColor: %s" % (a.bg.dump_srgb())) 

gen("Form*Label*", 2)
gen("Form*Text*", 4)
gen("Form*Text*Scrollbar*", 2)
gen("Text*", 4)
gen("Text*ThreeD*", 2)
gen("Text*Scrollbar*", 2)
gen("Viewport.", 2)
gen("Command.", 2)
gen("Toggle.", 2)
gen("MenuButton.", 2)
gen("SimpleMenu.", 2)
gen("List*", 4)
gen("Box.", 2)
gen("Label.", 4)
gen("Scrollbar.", 2)
gen("SimpleMenu*MenuLabel*", 4)
gen("Dialog.", 4)
gen("Form*", 2)
gen("Form*Viewport*", 4)
gen("Form*Viewport*Scrollbar*", 2)

genm = gen

genm("XmLabelGadget*", 6)
genm("XmSelectionBox.", 6)
genm("XmRowColumn*", 6)
genm("XmTextField.", 4)
genm("XmPushButtonGadget*", 6)
genm("XmFileSelectionBox*XmList.", 4)
genm("XmFileSelectionBox*XmScrolledWindow.XmScrollbar.", 6)
genm("XmFileSelectionBox*XmScrolledWindow.", 6)
genm("XmFileSelectionBox*XmSeparatorGadget.", 6)
genm("XmFileSelectionBox*XmForm.", 6)
genm("XmMessageBox.", 6)
genm("XmMessageBox*XmSeparatorGadget.", 6)

# TODO

genm("XmForm.XmLabelGadget.", 5)
genm("XmForm.XmRowColumn.", 5)
genm("XmForm.XmRowColumn.XmPushButton.", 5)
genm("XmForm.XmRowColumn.XmToggleButton.", 5)
genm("XmForm.XmRowColumn.XmLabelGadget.", 5)
genm("XmForm.XmFrame.XmLabelGadget.", 5)
genm("XmForm.menubar.", 6)
genm("XmFrame.XmScrolledWindow.DtTerm.", 4)
genm("XmMainWindow.XmFrame.XmRowColumn.", 5)
genm("XmMainWindow*XmText.", 4)
genm("XmMainWindow*XmFrame.XmRowColumn.", 5)
genm("XmMainWindow*XmScrolledWindow*XmDrawingArea.", 5)
genm("XmMainWindow*XmScrolledWindow*XmList.", 4)
genm("XmMainWindow*XmScrolledWindow*XmConainer.", 5)
genm("XmMainWindow*XmScrolledWindow.XmClipWindow.XmContainer.XmIconGadget.", 5)
genm("XmMainWindow*XmRowColumn.", 6)

t = motif.Variations(PAL[3])
print("XTerm*background: %s" % (t.bg.dump_srgb()))
print("XTerm*foreground: %s" % (t.fg.dump_srgb()))
