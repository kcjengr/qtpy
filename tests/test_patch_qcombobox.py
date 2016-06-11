from qtpy import QtGui, QtWidgets

def get_qapp(icon_path=None):
    qapp = QtWidgets.QApplication.instance()
    if qapp is None:
        qapp = QtWidgets.QApplication([''])
    return qapp


def test_patched_qcombobox():
    """
    In PySide, using Python objects as userData in QComboBox causes
    Segmentation faults under certain conditions. Even in cases where it
    doesn't, findData does not work correctly. Likewise, findData also
    does not work correctly with Python objects when using PyQt4. On the
    other hand, PyQt5 deals with this case correctly. We therefore patch
    QComboBox when using PyQt4 and PySide to avoid issues.
    """

    app = get_qapp()

    class Data(object):
        """
        Test class to store in userData. The __getitem__ is needed in order to
        reproduce the segmentation fault.
        """
        def __getitem__(self, item):
            raise ValueError("Failing")

    data1 = Data()
    data2 = Data()
    data3 = Data()
    data4 = Data()
    data5 = Data()
    data6 = Data()

    icon1 = QtGui.QIcon()
    icon2 = QtGui.QIcon()

    widget = QtWidgets.QComboBox()
    widget.addItem('a', data1)
    widget.insertItem(0, 'b', data2)
    widget.addItem('c', data1)
    widget.setItemData(2, data3)
    widget.addItem(icon1, 'd', data4)
    widget.insertItem(3, icon2, 'e', data5)
    widget.addItem(icon1, 'f')
    widget.insertItem(5, icon2, 'g')

    widget.show()

    assert widget.findData(data1) == 1
    assert widget.findData(data2) == 0
    assert widget.findData(data3) == 2
    assert widget.findData(data4) == 4
    assert widget.findData(data5) == 3
    assert widget.findData(data6) == -1

    assert widget.itemData(0) == data2
    assert widget.itemData(1) == data1
    assert widget.itemData(2) == data3
    assert widget.itemData(3) == data5
    assert widget.itemData(4) == data4
    assert widget.itemData(5) is None
    assert widget.itemData(6) is None

    assert widget.itemText(0) == 'b'
    assert widget.itemText(1) == 'a'
    assert widget.itemText(2) == 'c'
    assert widget.itemText(3) == 'e'
    assert widget.itemText(4) == 'd'
    assert widget.itemText(5) == 'g'
    assert widget.itemText(6) == 'f'