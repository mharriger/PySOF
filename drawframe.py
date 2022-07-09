import cairo
import math
import euclid

def bisectSegments(left, center, right):
    vLeft = left - center
    vRight = right - center
    return (vRight.normalized() + vLeft.normalized()).normalized() * .9525

def drawFrame(ptArr):
    with cairo.SVGSurface("frame.svg", 200, 200) as surface:
        surface.set_document_unit(cairo.SVG_UNIT_CM)
        centerList = []
        context = cairo.Context(surface)
        ptArr.extend([[-1 * x[0], x[1]] for x in ptArr[-2::-1]])
        ptArr = [euclid.Point2(x[0], x[1]) for x in ptArr]
        context.translate(100, 100)
        context.scale(3, 3)
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