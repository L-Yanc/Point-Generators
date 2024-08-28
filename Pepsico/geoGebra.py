from sympy import Point, Segment
from sympy.plotting import plot

##############
# Aisle No: 1
##############

P_start_0 = Point(255,281)
P_middle_0 = Point(611,325)
P_final_0 = Point(967,469)

P0_1 = Point(320.0, 249.03370786516854)
P0_2 = Point(427.5, 262.32022471910113)
P0_3 = Point(535.0, 275.6067415730337)
P0_4 = Point(676.0, 311.29213483146066)
P0_5 = Point(783.5, 354.7752808988764)
P0_6 = Point(891.0, 398.25842696629206)

P0_1.color = '#2b67bb'
P0_2.color = '#2b67bb'
P0_3.color = '#2b67bb'
P0_4.color = '#2b67bb'
P0_5.color = '#2b67bb'
P0_6.color = '#2b67bb'

P_start_0.color = '#2b5cbb'
P_middle_0.color = '#2b5cbb'
P_final_0.color = '#2b5cbb'

segment_start_middle_0 = Segment(P_start_0, P_middle_0)
segment_middle_final_0 = Segment(P_middle_0, P_final_0)

print('Distance between start and middle for aisle 1: 358.70879554312575 cm')
print('Distance between middle and final for aisle 1: 384.02083276822367 cm')
print()

##############
# Printing Palettes

lb_left_0_0 = Point(262.0754858490425, 281.87449825100526)
lb_right_0_0 = Point(356.4152971696085, 293.53447493107524)
ub_left_0_0 = Point(262.0754858490425, 401.87449825100526)
ub_right_0_0 = Point(356.4152971696085, 413.53447493107524)

palette_0_0_top = Segment(ub_right_0_0, ub_left_0_0)
palette_0_0_bottom = Segment(lb_right_0_0, lb_left_0_0)
palette_0_0_left = Segment(lb_left_0_0, ub_left_0_0)
palette_0_0_right = Segment(ub_right_0_0, lb_right_0_0)

midpoint_0_0_ub = palette_0_0_top.midpoint
midpoint_0_0_lb = palette_0_0_bottom.midpoint
palette_0_0_mid = Segment(midpoint_0_0_ub, midpoint_0_0_lb)

palette_0_0_mid.color = '#aaaaaa'

lb_left_0_1 = Point(363.490783018651, 294.4089731820805)
lb_right_0_1 = Point(457.830594339217, 306.0689498621505)
ub_left_0_1 = Point(363.490783018651, 414.4089731820805)
ub_right_0_1 = Point(457.830594339217, 426.0689498621505)

palette_0_1_top = Segment(ub_right_0_1, ub_left_0_1)
palette_0_1_bottom = Segment(lb_right_0_1, lb_left_0_1)
palette_0_1_left = Segment(lb_left_0_1, ub_left_0_1)
palette_0_1_right = Segment(ub_right_0_1, lb_right_0_1)

midpoint_0_1_ub = palette_0_1_top.midpoint
midpoint_0_1_lb = palette_0_1_bottom.midpoint
palette_0_1_mid = Segment(midpoint_0_1_ub, midpoint_0_1_lb)

palette_0_1_mid.color = '#aaaaaa'

lb_left_0_2 = Point(464.90608018825947, 306.94344811315574)
lb_right_0_2 = Point(559.2458915088255, 318.6034247932257)
ub_left_0_2 = Point(464.90608018825947, 426.94344811315574)
ub_right_0_2 = Point(559.2458915088255, 438.6034247932257)

palette_0_2_top = Segment(ub_right_0_2, ub_left_0_2)
palette_0_2_bottom = Segment(lb_right_0_2, lb_left_0_2)
palette_0_2_left = Segment(lb_left_0_2, ub_left_0_2)
palette_0_2_right = Segment(ub_right_0_2, lb_right_0_2)

midpoint_0_2_ub = palette_0_2_top.midpoint
midpoint_0_2_lb = palette_0_2_bottom.midpoint
palette_0_2_mid = Segment(midpoint_0_2_ub, midpoint_0_2_lb)

palette_0_2_mid.color = '#aaaaaa'

lb_left_0_3 = Point(617.3285069329187, 327.5598455009559)
lb_right_0_3 = Point(701.7085993718347, 361.6911188470342)
ub_left_0_3 = Point(617.3285069329187, 447.5598455009559)
ub_right_0_3 = Point(701.7085993718347, 481.6911188470342)

palette_0_3_top = Segment(ub_right_0_3, ub_left_0_3)
palette_0_3_bottom = Segment(lb_right_0_3, lb_left_0_3)
palette_0_3_left = Segment(lb_left_0_3, ub_left_0_3)
palette_0_3_right = Segment(ub_right_0_3, lb_right_0_3)

midpoint_0_3_ub = palette_0_3_top.midpoint
midpoint_0_3_lb = palette_0_3_bottom.midpoint
palette_0_3_mid = Segment(midpoint_0_3_ub, midpoint_0_3_lb)

palette_0_3_mid.color = '#aaaaaa'

lb_left_0_4 = Point(708.0371063047534, 364.2509643479901)
lb_right_0_4 = Point(792.4171987436694, 398.3822376940684)
ub_left_0_4 = Point(708.0371063047534, 484.2509643479901)
ub_right_0_4 = Point(792.4171987436694, 518.3822376940684)

palette_0_4_top = Segment(ub_right_0_4, ub_left_0_4)
palette_0_4_bottom = Segment(lb_right_0_4, lb_left_0_4)
palette_0_4_left = Segment(lb_left_0_4, ub_left_0_4)
palette_0_4_right = Segment(ub_right_0_4, lb_right_0_4)

midpoint_0_4_ub = palette_0_4_top.midpoint
midpoint_0_4_lb = palette_0_4_bottom.midpoint
palette_0_4_mid = Segment(midpoint_0_4_ub, midpoint_0_4_lb)

palette_0_4_mid.color = '#aaaaaa'

lb_left_0_5 = Point(798.745705676588, 400.9420831950243)
lb_right_0_5 = Point(883.125798115504, 435.0733565411026)
ub_left_0_5 = Point(798.745705676588, 520.9420831950242)
ub_right_0_5 = Point(883.125798115504, 555.0733565411026)

palette_0_5_top = Segment(ub_right_0_5, ub_left_0_5)
palette_0_5_bottom = Segment(lb_right_0_5, lb_left_0_5)
palette_0_5_left = Segment(lb_left_0_5, ub_left_0_5)
palette_0_5_right = Segment(ub_right_0_5, lb_right_0_5)

midpoint_0_5_ub = palette_0_5_top.midpoint
midpoint_0_5_lb = palette_0_5_bottom.midpoint
palette_0_5_mid = Segment(midpoint_0_5_ub, midpoint_0_5_lb)

palette_0_5_mid.color = '#aaaaaa'

