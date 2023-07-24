from turtle import circle
import cairo
import math
import euclid
from scipy import interpolate

CUTOFF_OFFSET = 1.3

def bisectAngle(left, center, right):
    vLeft = left - center
    vRight = right - center
    return (vRight.normalized() + vLeft.normalized()).normalized()

def lineMidpoint(line):
    """Return the euclid.Point2 that is the midpoint of the euclid.Line2 line"""
    return euclid.Point2(line.p1.x - (line.p1.x - line.p2.x) / 2.0, line.p1.y + abs(line.p1.y - line.p2.y) / 2.0)

def perpendicularBisector(left, right):
    """Returns the euclid.Line2 which bisects the line segment defined by euclid.Point2's left and right"""
    if left.x < 0:
        left,right = right,left
    v = left - right
    v2 = euclid.Vector2(v.y, -1 * v.x)
    mp = lineMidpoint(euclid.Line2(left, right))
    return euclid.Line2(mp, euclid.Point2(mp.x + v2.x, mp.y + v2.y))

def findCutoffLine(left, center, right, offset):
    bisector = bisectAngle(left, center, right) * offset
    v2 = euclid.Vector2(bisector.y, -1 * bisector.x)
    l = euclid.Line2(bisector + center, bisector + center + v2)
    print(l, l.intersect(euclid.Line2(left, center)))
    #if l.intersect(euclid.Line2(left, center)):
    #    return euclid.LineSegment2(l.intersect(euclid.Line2(left, center)), l.intersect(euclid.Line2(right, center)))
    vLeft = (left - center).normalize() * offset
    vRight = (right - center).normalize() * offset
    return euclid.Line2(center + vLeft, center + vRight)

def findReliefArcMidpoint(left, right):
    if left.x < 0:
        left,right = right,left
    v = left - right
    v2 = euclid.Vector2(v.y, -1 * v.x)
    v2 = v2.normalize() * (left - right).magnitude() * .1
    return lineMidpoint(euclid.Line2(left, right)) + (math.copysign(1, right.x) * v2)

def findReliefArcCenter(left, right):
    mp = findReliefArcMidpoint(left, right)
    l1 = perpendicularBisector(left, mp)
    l2 = perpendicularBisector(mp, right)
    return l1.intersect(l2)

def drawCenterMark(context, point):
    context.move_to(point.x - .25, point.y)
    context.line_to(point.x + .25, point.y)
    context.move_to(point.x, point.y - .25)
    context.line_to(point.x, point.y + .25)
    context.stroke()

def drawLine(context, line):
    context.move_to(line.p1.x, line.p1.y)
    context.line_to(line.p2.x, line.p2.y)
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
    width = max([x[0] for x in ptArr])* 2 + 1
    height = (max([x[1] for x in ptArr]) - min([x[1] for x in ptArr])) + 2
    with cairo.SVGSurface("frame.svg", width, height) as surface:
        surface.set_document_unit(cairo.SVG_UNIT_CM)
        centerList = []
        list2 = []
        list3 = []
        list4 = []
        context = cairo.Context(surface)
        ptArr.extend([[-1 * x[0], x[1]] for x in ptArr[-2::-1]])
        ptArr = [euclid.Point2(x[0], x[1]) for x in ptArr]
        drawGrid(context)
        context.translate(width / 2, max([x[1] for x in ptArr]) + 1)
        context.rotate(math.pi)
        context.move_to(ptArr[0][0], ptArr[0][1])
        for i in range(1, len(ptArr)):
            pt = ptArr[i]
            left = ptArr[i - 1]
            right = ptArr[1 if i + 1 >= len(ptArr) else i + 1]
            context.line_to(pt.x, pt.y)
            centerList.append(pt + (bisectAngle(left, pt, right) * .9525))
            #list2.append(findReliefArcMidpoint(pt, right))
            #list3.append(findReliefArcCenter(left, pt, right))
            list4.append([left, pt, right])
        context.close_path()    
        context.set_line_width(.1)
        context.set_source_rgb(0, 0, 1)
        context.stroke()
        for center in centerList:
            context.arc(center.x, center.y, .9525, 0, 2 * math.pi)
            context.set_source_rgb(0, 1, 0)
            context.stroke()
            drawCenterMark(context, center)
        tempList = [findCutoffLine(x[0], x[1], x[2], CUTOFF_OFFSET) for x in list4]
        cutoffPairList = []
        for i in range(len(tempList)):
            cutoffPairList.append([tempList[i].p2, tempList[(i + 1) % len(tempList)].p1])
        context.set_source_rgb(1, 1, 0)
        for line in tempList:
            drawLine(context, line)
        for points in cutoffPairList:
            drawCenterMark(context, points[0])
            drawCenterMark(context, points[1])
            list2.append(findReliefArcMidpoint(points[0], points[1]))
            list3.append(findReliefArcCenter(points[0], points[1]))
        context.set_source_rgb(1, 0, 0)
        for i in range(len(list2)):
            drawCenterMark(context, list2[i])
            drawCenterMark(context, list3[i])
            context.arc(list3[i].x, list3[i].y, (list2[i] - list3[i]).magnitude(), 0, 2 * math.pi)
            context.stroke()

def drawKeel(ptArr):
    width = max([x[0] for x in ptArr]) + 1
    height = max([x[1] for x in ptArr]) + 1
    print(width, height)
    with cairo.SVGSurface("keel.svg", width, height) as surface:
        surface.set_document_unit(cairo.SVG_UNIT_CM)
        context = cairo.Context(surface)
        drawGrid(context)
        context.translate(width, height - 1)
        context.rotate(math.pi)
        context.set_line_width(.1)
        context.set_source_rgb(0, 0, 1)
        for i in range(len(ptArr)):
            pt1 = ptArr[i]
            pt2 = ptArr[(i + 1) % len(ptArr)]
            drawCenterMark(context, euclid.Point2(pt1[0], pt1[1]))
            context.move_to(pt1[0], pt1[1])
            context.curve_to(pt1[0] + 1, pt1[1], pt2[0] - 1, pt2[1], pt2[0], pt2[1])