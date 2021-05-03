class Taxon:
    def __init__(self):
        self._uid = None

    pass


# noinspection PyAttributeOutsideInit
class Taxon:
    # region Protected members
    _uid: str = ""
    _parent: Taxon = None
    _children: dict[str, Taxon] = {}
    # endregion

    # region Construction
    def __int__(self):
        pass
    # endregion
    
    # region Properties
    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, value: str):
        self._uid = value

    @property
    def parent(self) -> Taxon:
        return self._parent

    @parent.setter
    def parent(self, value: Taxon):
        self._parent = value

    @property
    def children(self) -> dict[str, Taxon]:
        return self._children
    # endregion

    # region Management
    def add_child(self, child: Taxon):
        """
        Adds a child taxon to the children dictionary
        :param child: The child to add
        :return: None
        """
        if child.uid not in self._children.keys():
            child._parent = self
            self.children[child.uid] = child
    # endregion


if __name__ == '__main__':
    t1 = Taxon()
    t1.uid = "12345"


    t2 = Taxon()
    t2.uid = "5678"

    t1.add_child(t2)

    print(t1)