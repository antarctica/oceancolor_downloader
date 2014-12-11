sst_style = """
<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.4.0-Chugiak" minimumScale="0" maximumScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <pipe>
    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="29.129" classificationMinMaxOrigin="CumulativeCutFullExtentEstimated" band="1" classificationMin="-1.66383" type="singlebandpseudocolor">
      <rasterTransparency/>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" clip="0">
          <item alpha="255" value="-1.66383" label="-1.663830" color="#2c7bb6"/>
          <item alpha="255" value="6.03438" label="6.034378" color="#abd9e9"/>
          <item alpha="255" value="13.7326" label="13.732585" color="#ffffbf"/>
          <item alpha="255" value="21.4308" label="21.430792" color="#fdae61"/>
          <item alpha="255" value="29.129" label="29.129000" color="#d7191c"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeGreen="128" colorizeOn="0" colorizeRed="255" colorizeBlue="128" grayscaleMode="0" saturation="0" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
"""

def makeqml(pth, style):
	f = open('{}/style.qml'.format(pth), 'w')
	f.write(style)
	f.close()
	return '{}/style.qml'.format(pth)
