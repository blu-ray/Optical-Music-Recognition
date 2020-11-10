from rectangle import Rectangle
from best_fit import fit
import cv2
note_step = 0.0625

note_defs = {
     -4 : ("g5", 79),
     -3 : ("f5", 77),
     -2 : ("e5", 76),
     -1 : ("d5", 74),
      0 : ("c5", 72),
      1 : ("b4", 71),
      2 : ("a4", 69),
      3 : ("g4", 67),
      4 : ("f4", 65),
      5 : ("e4", 64),
      6 : ("d4", 62),
      7 : ("c4", 60),
      8 : ("b3", 59),
      9 : ("a3", 57),
     10 : ("g3", 55),
     11 : ("f3", 53),
     12 : ("e3", 52),
     13 : ("d3", 50),
     14 : ("c3", 48),
     15 : ("b2", 47),
     16 : ("a2", 45),
     17 : ("f2", 53),
}

class Note(object):
    def __init__(self, rec, sym, staff_rec, sharp_notes = [], flat_notes = [],img = [],staff_img=[],best_scale=1):
        self.rec = rec
        self.sym = sym
        self.xpadd = 20
        self.ypadd = 50

        staff_lower, staff_upper, staff_thresh = int(best_scale*100)-20, int(best_scale*100)+20, 0.60

        after = img[ int(staff_rec.y):int(staff_rec.y + staff_rec.h), int(rec.x + rec.w):int(rec.x + 2 * rec.w)]
        after = cv2.copyMakeBorder(after,self.ypadd,self.ypadd,self.xpadd,self.xpadd,cv2.BORDER_CONSTANT,value=255) #zero padding

        locations, scale = fit(after, staff_img, staff_lower, staff_upper, staff_thresh)
        locs = []
        for i in range(len(staff_img)):
            locs.append([pt for pt in zip(*locations[i][::-1])])
        locs = [j for i in locs for j in i]

        before = img[int(staff_rec.y):int(staff_rec.y + staff_rec.h), int(rec.x - rec.w):int(rec.x)]
        before = cv2.copyMakeBorder(before,self.ypadd,self.ypadd,self.xpadd,self.xpadd, cv2.BORDER_CONSTANT, value=255)  # zero padding
        locations2, scale2 = fit(before, staff_img, staff_lower, staff_upper, staff_thresh)
        locs2 = []
        for i in range(len(staff_img)):
            locs2.append([pt for pt in zip(*locations2[i][::-1])])
        locs2 = [j for i in locs2 for j in i]

        if(len(locs)<4):
            middle = rec.y + (rec.h / 2.0)
            height = (middle - staff_rec.y) / staff_rec.h
            note_def = note_defs[int(height / note_step + 0.5)]
            print(note_def)
            print("is not accurate")
        else:
            heights = [p[1] for p in locs]
            heights2 = [q[1] for q in locs2]
            avgheight = sum(heights)/len(heights)
            print(avgheight+ staff_rec.y - self.ypadd)
            avgheight2 = sum(heights2)/len(heights2)
            print(avgheight2+ staff_rec.y - self.ypadd)
            avgheight = int((avgheight+avgheight2)/2 + 0.5)
            avgheight = avgheight + staff_rec.y - self.ypadd

            middle = rec.y + (rec.h / 2.0)
            height = (middle - (avgheight + 38*best_scale)) / (9*best_scale) #need to improve
            note_def = note_defs[int(height + 0.5) - 3]
            print("Middle of note:",(rec.x + rec.w/2),middle)
            print("Average Height of Staff:",avgheight)
            print("Distance Between Middle Average Height:",middle - avgheight)
            print("Note Steps From First Line:",height)
            print("Note Found:",note_def[0])
            print("Best Scale",best_scale)
            print("--------------")

        self.note = note_def[0]
        self.pitch = note_def[1]
        if any(n for n in sharp_notes if n.note[0] == self.note[0]):
            self.note += "#"
            self.pitch += 1
        if any(n for n in flat_notes if n.note[0] == self.note[0]):
            self.note += "b"
            self.pitch -= 1


