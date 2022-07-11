import cairo
import math
import euclid

def bisectSegments(left, center, right):
    vLeft = left - center
    vRight = right - center
    return (vRight.normalized() + vLeft.normalized()).normalized() * .9525

def drawCenterMark(context, point):
    context.move_to(point.x - .25, point.y)
    context.line_to(point.x + .25, point.y)
    context.move_to(point.x, point.y - .25)
    context.line_to(point.x, point.y + .25)
    context.stroke()

def drawGrid(context):
    context.set_line_width(.025)
    context.set_source_rgb(.25, .25, .25)
    for x in range(0, 101):
        context.move_to(x, 0)
        context.line_to(x, 50)
    for y in range(51):
        context.move_to(0, y)
        context.line_to(100, y)
    context.stroke()

def drawFrame(ptArr):
    with cairo.SVGSurface("frame.svg", 100, 50) as surface:
        surface.set_document_unit(cairo.SVG_UNIT_CM)
        centerList = []
        context = cairo.Context(surface)
        ptArr.extend([[-1 * x[0], x[1]] for x in ptArr[-2::-1]])
        ptArr = [euclid.Point2(x[0], x[1]) for x in ptArr]
        drawGrid(context)
        context.translate(50, 50)
        context.rotate(math.pi)
        context.move_to(ptArr[0][0], ptArr[0][1])
        for i in range(1, len(ptArr)):
            pt = ptArr[i]
            left = ptArr[i - 1]
            right = ptArr[1 if i + 1 >= len(ptArr) else i + 1]
            context.line_to(pt.x, pt.y)
            centerList.append(pt + bisectSegments(left, pt, right))
        context.close_path()    
        context.set_line_width(.1)
        context.set_source_rgb(0, 0, 1)
        context.stroke()
        for center in centerList:
            context.arc(center.x, center.y, .9525, 0, 2 * math.pi)
            context.set_source_rgb(0, 1, 0)
            context.stroke()
            drawCenterMark(context, center)
