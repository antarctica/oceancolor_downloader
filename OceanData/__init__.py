# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OceanData
                                 A QGIS plugin
 Download oceanographic datasets
                             -------------------
        begin                : 2014-08-13
        copyright            : (C) 2014 by Louise Ireland
        email                : louireland@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load OceanData class from file OceanData
    from oceandata import OceanData
    return OceanData(iface)
