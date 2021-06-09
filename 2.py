from psychopy import visual
from psychopy.visual import ShapeStim

window = visual.Window(units="pix", color="gray", fullscr=False)
window.setMouseVisible(False)
arrowVert = [(-0.4,0.05),(-0.4,-0.05),(-.2,-0.05),(-.2,-0.1),(0,0),(-.2,0.1),(-.2,0.05)]
arrow = ShapeStim(window=window, vertices=arrowVert, fillColor='darkred', size=.5, lineColor='red')
arrow.draw()
window.flip()