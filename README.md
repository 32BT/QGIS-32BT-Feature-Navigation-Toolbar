# QGIS-Feature-Navigation-Toolbar
QGIS plugin for a toolbar to easily navigate a preselected set of features from any featurelayer.

<img width="223" height="41" alt="image" src="https://github.com/user-attachments/assets/693cb433-94ed-4846-9b3c-0212959d7586" />  

### Feature Navigation Toolbar  
**Overview**  
The Feature Navigation Toolbar is meant to quickly browse a prior selection of features. It will select and zoom to each successive feature. It is not much different from the tablebrowser, except that it will also autoselect the current feature. In addition, it has an internal memory which allows it to provide two important extra functions. It can append additional features outside the preselected set, and it will remember and separate between parsed and unparsed features.

Because the browser distinguishes between parsed and unparsed features it can change its browsing behavior so that unparsed features are prioritized. Sometimes you want to browse back a couple of steps and redo a feature and then recommence where you left off in the unparsed set.

**Installation**  
You can download a zipfile of the code repository using the Code-button available on this repository's github page. Decompress the zipfile into your QGIS plugins directory. The plugin management dialog can do this for you using the "Install from ZIP" option. See: https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab  
In the plugin management dialog, make sure the plugin is activated.

<img width="1075" height="432" alt="image" src="https://github.com/user-attachments/assets/b738591a-76dc-4dab-ad55-6eae993ff828" /><br/>

**Start Navigation**  
The resetbutton at the left of the toolbar allows you to start a navigation session.  

<img width="215" height="41" alt="image" src="https://github.com/user-attachments/assets/9fec5ca8-6289-4fd6-81fb-24dfe9a53858" /><br/>  

The button will be available if the active layer in the map legend is a feature layer with at least two or more features selected. If the reset is validated, the selection will be loaded and the tool will immediately jump to the first feature. The feature will be selected and the view will be zoomed appropriately. Use the navigation buttons to traverse the set of features.  

If only one feature is selected, the start-button will not be available. This is generally the case during navigation and prevents accidentally hitting the restart-button. In addition, if another browsing session is currently active, then a reset will always ask you for confirmation. If you inadvertently selected the resetbutton, or you decide to stick with the current browsing session instead, you can simply select cancel. 

<img width="426" height="177" alt="image" src="https://github.com/user-attachments/assets/2e4f7a23-f1a9-437a-9b5a-69b32ce9a4bd" /><br/><br/>

### Feature Navigation Toolbar API  
**Plugin API**  
The plugin will be available to other plugins through the iface var. If you have a plugin class with iface stored in self._iface, the navigation controller can be found as follows:

```python
navCtl = self._iface.property("32bt.NavigationController")
```  

The navigation controller has a method named "selectNextFeature" which can be called after processing a feature. This will trigger the navigation controller to zoom to and select the next feature from the original selection and update the toolbar accordingly. It also stores the current selection in the parsed set of features. Since the plugin may not necessarily be available, your code should look something like this:

```python
def selectNextFeature(self, layer):
    navCtl = self._iface.property("32bt.NavigationController")
    if navCtl: navCtl.selectNextFeature(layer)
```

Navigation only works if your layer matches the navigation layer. The current navigation layer can be fetched using the method "activeLayer":

```python
    if navCtl.activeLayer() == layer:
        # layer selection will be updated if you call selectNextFeature
    else:
        # layer selection will be cleared if you call selectNextFeature
```

Removing the selection if the layer does not match, is a "convenience" function for feedbackpurposes. If you prefer to isolate the layer responsibility, you can accomplish the same result with the following complete example:

```python
def selectNextFeature(self, layer):
    navCtl = self._iface.property("32bt.NavigationController")
    if navCtl and navCtl.activeLayer()==layer:
        navCtl.selectNextFeature(layer)
    else:
        layer.removeSelection()
```
