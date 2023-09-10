import pcbnew
import math

# exec(open("/home/xmrazek7/projects/RB0012-HD108-LED/LED-strip/placement.py").read())

START_X = pcbnew.FromMM(40)
START_Y = pcbnew.FromMM(70)
SPACING = pcbnew.FromMM(12)

DATA_TRACK_WIDTH = pcbnew.FromMM(0.5)
POWER_TRACK_WIDTH = pcbnew.FromMM(1.8)

STRIP_HEIGHT = pcbnew.FromMM(12)
STRIP_PADDING = pcbnew.FromMM(5)

board = pcbnew.GetBoard()

def addTrack(points, width, netcode):
    global board
    for start, end in zip(points, points[1:]):
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(start)
        track.SetEnd(end)
        track.SetWidth(width)
        track.SetNetCode(netcode)
        board.Add(track)

def addVias(points, drill, size, netcode):
    global board
    for p in points:
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(p)
        via.SetDrill(drill)
        via.SetWidth(size)
        via.SetNetCode(netcode)
        board.Add(via)

def addGraphicalLine(points, width, layer):
    global board
    for start, end in zip(points, points[1:]):
        segment = pcbnew.PCB_SHAPE()
        segment.SetShape(pcbnew.S_SEGMENT)
        segment.SetLayer(layer)
        segment.SetStart(start)
        segment.SetEnd(end)
        segment.SetWidth(width)
        board.Add(segment)

def remove(collection):
    global board
    for x in list(collection):
        board.Remove(x)


remove(board.GetTracks())
remove([x for x in board.GetDrawings() if x.GetLayer() == pcbnew.Edge_Cuts])


leds = [x for x in board.GetFootprints() if x.GetReference().startswith("D")]
leds.sort(key=lambda x: int(x.GetReference().replace("D", "")))

marks = [x for x in board.GetFootprints() if x.GetReference().startswith("MARK")]
marks.sort(key=lambda x: int(x.GetReference().replace("MARK", "")))

connectors = [x for x in board.GetFootprints() if x.GetReference().startswith("C")]
connectors.sort(key=lambda x: int(x.GetReference().replace("C", "")))

for i, (s, m) in enumerate(zip(leds, marks)):
    s.Reference().SetVisible(False)
    s.SetPosition(pcbnew.VECTOR2I(START_X + i * SPACING, START_Y))
    s.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))

    m.SetPosition(pcbnew.VECTOR2I(START_X + i * SPACING, START_Y))

    for p in s.Pads():
        number = p.GetNumber()
        padPos = p.GetPosition()
        if number == "1" or number == "6":
            dir = -1 if number == "1" else 1
            addTrack([
                padPos,
                padPos + pcbnew.VECTOR2I_MM(dir * 1.3, 0),
                padPos + pcbnew.VECTOR2I_MM(dir * (1.3 + 0.95), 0.95),
                padPos + pcbnew.VECTOR2I_MM(dir * 3.6, 0.95)],
                DATA_TRACK_WIDTH, p.GetNetCode())
        if number == "2" or number == "5":
            dir = -1 if number == "2" else 1
            addTrack([
                padPos,
                padPos + pcbnew.VECTOR2I_MM(dir * 1.3, 0),
                padPos + pcbnew.VECTOR2I_MM(dir * (1.3 + 0.75), 0.75),
                padPos + pcbnew.VECTOR2I_MM(dir * 3.6, 0.75)],
                DATA_TRACK_WIDTH, p.GetNetCode())
        if number == "4":
            addTrack([
                padPos,
                pcbnew.VECTOR2I(s.GetPosition()[0], p.GetPosition()[1]),
                s.GetPosition() + pcbnew.VECTOR2I_MM(0, -3)
            ],
            POWER_TRACK_WIDTH, p.GetNetCode())

            addVias([
                s.GetPosition() + pcbnew.VECTOR2I_MM(0, -0.75),
                s.GetPosition() + pcbnew.VECTOR2I_MM(-0.75, -0.75),
                s.GetPosition() + pcbnew.VECTOR2I_MM(0.75, -0.75),
            ], pcbnew.FromMM(0.3), pcbnew.FromMM(0.7), p.GetNetCode())
        if number == "3":
            addVias([
                p.GetPosition() + pcbnew.VECTOR2I_MM(0, -0.6),
                p.GetPosition() + pcbnew.VECTOR2I_MM(-0.75, -0.6),
                p.GetPosition() + pcbnew.VECTOR2I_MM(0.75, -0.6),
            ], pcbnew.FromMM(0.3), pcbnew.FromMM(0.7), p.GetNetCode())

for i, s in enumerate(connectors):
    s.SetPosition(pcbnew.VECTOR2I(START_X + i * SPACING - SPACING // 2, START_Y))
    s.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))

minX = connectors[0].GetPosition()[0] - STRIP_PADDING
maxX = connectors[-1].GetPosition()[0] + STRIP_PADDING

addGraphicalLine([
    pcbnew.VECTOR2I(minX, START_Y - STRIP_HEIGHT // 2),
    pcbnew.VECTOR2I(maxX, START_Y - STRIP_HEIGHT // 2),
    pcbnew.VECTOR2I(maxX, START_Y + STRIP_HEIGHT // 2),
    pcbnew.VECTOR2I(minX, START_Y + STRIP_HEIGHT // 2),
    pcbnew.VECTOR2I(minX, START_Y - STRIP_HEIGHT // 2)
], pcbnew.FromMM(0.3), pcbnew.Edge_Cuts)

pcbnew.Refresh()
