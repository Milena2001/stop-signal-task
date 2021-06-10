from psychopy import visual, core, event

window = visual.Window(units="pix", color="gray", fullscr=True)
circle= visual.Circle(window, size=(120, 120), pos=(0,0), lineColor = 'white', fillColor = None)
window.flip()
circle.draw()
window.flip()
core.wait(1)