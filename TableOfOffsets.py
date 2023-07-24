"""
A table of offsets used to define the shape of a kayak
"""
class TableOfOffsets:
    """
    Stations, keel and gunwale are lists of points.
    Chines is a list of lists 
    """
    def __init__(self, stations = [], keel = [], chines = [], gunwale = [], deckridge = []) -> None:
        self._stations = stations
        self._keel_pts = keel
        self._chines_pts = chines
        self._gunwale_pts = gunwale
        self._deckridge_pts = deckridge

    def __str__(self) -> str:
        outstr = ""
        for i in range(len(self._stations)):
            outstr+= f"{self._stations[i]}\t{self._keel_pts[i]}"
            for j in range(len(self._chines_pts)):
                outstr += f"\t{self._chines_pts[j][i]}"
            outstr += f"\t{self._gunwale_pts[i]}\t{self._deckridge_pts[i]}\n"
        return outstr

    ## Be able to return iterable of frames
    @property
    def frames(self):
        frames = []
        for i in range(len(self._stations)):
            this_frame = []
            this_frame.append([self._stations[i], *self._keel_pts[i]])
            for j in range(len(self._chines)):
                this_frame.append([self._stations[i], *self._chines_pts[j][i]])
            this_frame.append([self._stations[i], *self._gunwale_pts[i]])
            this_frame.append([self._stations[i], *self._deckridge_pts[i]])
            frames.append(this_frame)
        return frames

    ## Iterable of chines
    @property
    def chines(self):
        chines = []
        for i in range(len(self._chine_pts)):
            this_chine = []
            for j in range(len(self._stations)):
                this_chine.append([self._stations[j], *self._chine_pts[i][j]])
            chines.append(this_chine)
        return chines
    
    ## Iterable of keel points
    @property
    def keel(self):
        keel = []
        for i in range(len(self._stations)):
            keel.append(self._stations[i], *self._keel_pts[i])
        return keel
    
    ## Iterable of gunwale points
    @property
    def gunwale(self):
        gunwale = []
        for i in range(len(self._stations)):
            gunwale.append(self._stations[i], *self._gunwale_pts[i])
        return gunwale
    
    ## Iterable of deckridge points
    @property
    def deckridge(self):
        deckridge = []
        for i in range(len(self._stations)):
            deckridge.append(self._stations[i], *self._deckridge_pts[i])
        return deckridge
