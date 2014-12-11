from styles import chl_style, sst_style


__styles = {
        'AQUA MODIS Sea Surface Temperature': sst_style,
        'AQUA MODIS Chlorophyll Concentration': chl_style,
        'SeaWiFS Chlorophyll Concentration': chl_style,
}

def get(k):
        return __styles[k]


def makeqml(pth, style):
        f = open('{}/style.qml'.format(pth), 'w')
        f.write(style)
        f.close()
        return '{}/style.qml'.format(pth)
